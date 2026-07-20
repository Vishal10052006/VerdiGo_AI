import logging
from datetime import datetime, timezone
from urllib import request
import json

from sqlalchemy.orm import Session

from app.config.settings import settings
from app.models.user import User
from app.repositories import (
    otp_repository,
    user_repository,
    revocation_repository,
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


def send_otp_sms(mobile: str, otp: str) -> None:

    if not settings.SMS_PROVIDER_URL:
        if settings.DEBUG:
            logger.info("OTP for %s: %s", mobile, otp)
            return
        raise RuntimeError("SMS provider is not configured")

    payload = json.dumps(
        {
            "mobile": mobile,
            "message": f"Your VerdiGO AI OTP is {otp}",
            "sender_id": settings.SMS_SENDER_ID,
        }
    ).encode("utf-8")

    headers = {"Content-Type": "application/json"}

    if settings.SMS_PROVIDER_API_KEY:
        headers["Authorization"] = f"Bearer {settings.SMS_PROVIDER_API_KEY}"

    sms_request = request.Request(
        settings.SMS_PROVIDER_URL,
        data=payload,
        headers=headers,
        method="POST",
    )

    with request.urlopen(sms_request, timeout=5) as response:
        if response.status >= 400:
            raise RuntimeError("SMS provider rejected OTP request")


def register_user(db: Session, mobile: str) -> User:

    user = user_repository.get_by_mobile(db=db, mobile=mobile)

    if user:
        return user

    new_user = User(
        mobile=mobile,
        auth_provider="otp",
        language="hi",
        role="farmer",
        is_verified=True,
        is_active=True,
    )

    return user_repository.create(db=db, user=new_user)


def login_user(db: Session, mobile: str) -> dict:

    otp = otp_service.generate_otp()

    otp_service.save_otp(db=db, mobile=mobile, otp=otp)

    send_otp_sms(mobile=mobile, otp=otp)

    return {"message": "OTP sent successfully"}


def verify_otp(db: Session, mobile: str, otp: str) -> dict:

    latest_otp = otp_repository.get_latest(db=db, mobile=mobile)

    if latest_otp is None:
        raise BadRequestException(message="OTP not found.")

    if latest_otp.is_used:
        raise BadRequestException(message="OTP already used.")

    if not otp_service.check_expiry(db, mobile):
        raise BadRequestException(message="OTP expired.")

    if not otp_service.check_attempts(db, mobile):
        raise BadRequestException(message="Maximum OTP attempts exceeded.")

    if not otp_service.validate_otp(db, mobile, otp):
        otp_repository.increment_attempt(db=db, otp=latest_otp)
        raise BadRequestException(message="Invalid OTP.")

    otp_repository.mark_used(db=db, otp=latest_otp)

    user = register_user(db=db, mobile=mobile)

    # ------------------------------------------------------------
    # Issue Tokens (now carrying jti)
    # ------------------------------------------------------------

    access_token, _access_jti, _access_exp = jwt_service.create_access_token(
        str(user.id)
    )

    refresh_token, refresh_jti, refresh_exp = jwt_service.create_refresh_token(
        str(user.id)
    )

    # Persist the refresh token so it can be revoked on logout.
    revocation_repository.store_refresh_token(
        db=db,
        user_id=user.id,
        jti=refresh_jti,
        expires_at=refresh_exp,
    )

    return {
        "success": True,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user,
    }


def refresh_access_token(db: Session, refresh_token: str) -> dict:

    payload = jwt_service.verify_token(refresh_token, token_type="refresh")

    if payload is None:
        raise UnauthorizedException(message="Invalid refresh token.")

    if not revocation_repository.is_refresh_token_valid(
        db=db,
        jti=payload["jti"],
    ):
        raise UnauthorizedException(
            message="Refresh token has been revoked. Please log in again."
        )

    access_token, _jti, _exp = jwt_service.create_access_token(payload["sub"])

    return {"success": True, "access_token": access_token}


def logout_user(
    db: Session,
    access_token_payload: dict,
    refresh_token: str | None,
) -> dict:
    """
    Real server-side logout:
    - Blacklists the current access token (rejected immediately on next request)
    - Revokes the refresh token so it can't be used to mint new access tokens
    """

    # Blacklist the access token that made this request.
    # jose decodes "exp" as a raw unix timestamp (int), so convert it.
    exp_value = access_token_payload["exp"]
    expires_at = (
        exp_value
        if isinstance(exp_value, datetime)
        else datetime.fromtimestamp(exp_value, tz=timezone.utc)
    )

    revocation_repository.blacklist_access_token(
        db=db,
        jti=access_token_payload["jti"],
        expires_at=expires_at,
    )

    # Revoke the refresh token if the client sent one.
    if refresh_token:
        payload = jwt_service.verify_token(refresh_token, token_type="refresh")
        if payload:
            revocation_repository.revoke_refresh_token(
                db=db,
                jti=payload["jti"],
            )

    return {
        "success": True,
        "message": "Logged out successfully",
        "data": {},
    }