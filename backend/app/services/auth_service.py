import json
import logging
from urllib import request
from sqlalchemy.orm import Session
from app.config.settings import settings
from app.models.user import User
from app.repositories import (
    otp_repository,
    user_repository,
)
from app.services import (
    jwt_service,
    otp_service,
)
from app.core.exceptions import (
    BadRequestException,
    UnauthorizedException,
)
logger = logging.getLogger(__name__)


def send_otp_sms(
    mobile: str,
    otp: str
) -> None:

    if not settings.SMS_PROVIDER_URL:
        if settings.DEBUG:
            logger.info("OTP for %s: %s", mobile, otp)
            return

        raise RuntimeError("SMS provider is not configured")

    payload = json.dumps({
        "mobile": mobile,
        "message": f"Your VerdiGO AI OTP is {otp}",
        "sender_id": settings.SMS_SENDER_ID
    }).encode("utf-8")

    headers = {
        "Content-Type": "application/json"
    }

    if settings.SMS_PROVIDER_API_KEY:
        headers["Authorization"] = f"Bearer {settings.SMS_PROVIDER_API_KEY}"

    sms_request = request.Request(
        settings.SMS_PROVIDER_URL,
        data=payload,
        headers=headers,
        method="POST"
    )

    with request.urlopen(sms_request, timeout=5) as response:
        if response.status >= 400:
            raise RuntimeError("SMS provider rejected OTP request")


def register_user(
    db: Session,
    mobile: str
) -> User:

    user = user_repository.get_by_mobile(
        db=db,
        mobile=mobile
    )

    if user:
        return user

    new_user = User(
        mobile=mobile,
        auth_provider="otp",
        language="hi",
        role="farmer",
        is_verified=True,
        is_active=True
    )

    return user_repository.create(
        db=db,
        user=new_user
    )

def login_user(
    db: Session,
    mobile: str
) -> dict:

    otp = otp_service.generate_otp()

    otp_service.save_otp(
        db=db,
        mobile=mobile,
        otp=otp
    )

    send_otp_sms(
        mobile=mobile,
        otp=otp
    )

    return {
        "message": "OTP sent successfully"
    }


def verify_otp(
    db: Session,
    mobile: str,
    otp: str
) -> dict:

    latest_otp = otp_repository.get_latest(
        db=db,
        mobile=mobile
    )

    if latest_otp is None:
        raise BadRequestException(
            message="OTP not found."
        )
    
    if latest_otp.is_used:
        raise BadRequestException(
            message="OTP already used."
        )

    if not otp_service.check_expiry(db, mobile):
        raise BadRequestException(
            message="OTP expired."
        )

    if not otp_service.check_attempts(db, mobile):
        raise BadRequestException(
            message="Maximum OTP attempts exceeded."
        )

    if not otp_service.validate_otp(
        db,
        mobile,
        otp
    ):
        otp_repository.increment_attempt(
            db=db,
            otp=latest_otp
        )

        raise BadRequestException(
            message="Invalid OTP."
        )

    otp_repository.mark_used(
        db=db,
        otp=latest_otp
    )

    user = register_user(
        db=db,
        mobile=mobile
    )
    print("=" * 60)
    print("VERIFY OTP")
    print("Mobile :", mobile)
    print("User ID:", user.id)
    print("=" * 60)

    access_token = jwt_service.create_access_token(
        str(user.id)
    )

    refresh_token = jwt_service.create_refresh_token(
        str(user.id)
    )

    return {
        "success": True,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user
    }


def refresh_access_token(
    refresh_token: str
) -> dict:

    payload = jwt_service.verify_token(
        refresh_token,
        token_type="refresh"
    )

    if payload is None:
        raise UnauthorizedException(
            message="Invalid refresh token."
        )

    access_token = jwt_service.create_access_token(
        payload["sub"]
    )

    return {
        "success": True,
        "access_token": access_token
    }


def logout_user() -> dict:
    return {
        "success": True,
        "message": "Logged out successfully",
        "data": {}
    }
