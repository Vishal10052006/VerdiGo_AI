import random
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.config.settings import settings
from app.models.otp import OTP
from app.repositories import otp_repository


def generate_otp() -> str:
    return "".join(
        random.choices(
            "0123456789",
            k=settings.OTP_LENGTH
        )
    )


def save_otp(
    db: Session,
    mobile: str,
    otp: str
) -> OTP:

    expiry_time = datetime.now(timezone.utc) + timedelta(
        minutes=settings.OTP_EXPIRE_MINUTES
    )

    otp_record = OTP(
        mobile=mobile,
        otp=otp,
        expiry_time=expiry_time
    )

    return otp_repository.create(
        db=db,
        otp=otp_record
    )


def validate_otp(
    db: Session,
    mobile: str,
    entered_otp: str
) -> bool:

    latest_otp = otp_repository.get_latest(
        db=db,
        mobile=mobile
    )

    if latest_otp is None:
        return False

    return latest_otp.otp == entered_otp


def check_expiry(
    db: Session,
    mobile: str
) -> bool:

    latest_otp = otp_repository.get_latest(
        db=db,
        mobile=mobile
    )

    if latest_otp is None:
        return False

    return latest_otp.expiry_time > datetime.now(timezone.utc)


def check_attempts(
    db: Session,
    mobile: str
) -> bool:

    latest_otp = otp_repository.get_latest(
        db=db,
        mobile=mobile
    )

    if latest_otp is None:
        return False

    return (
        latest_otp.attempt_count
        < settings.OTP_MAX_ATTEMPTS
    )