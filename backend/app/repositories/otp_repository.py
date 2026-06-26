from datetime import datetime, timezone

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.otp import OTP


def create(db: Session, otp: OTP) -> OTP:
    db.add(otp)
    db.commit()
    db.refresh(otp)

    return otp


def get_latest(db: Session, mobile: str) -> OTP | None:
    return (
        db.query(OTP)
        .filter(OTP.mobile == mobile)
        .order_by(desc(OTP.created_at))
        .first()
    )


def mark_used(db: Session, otp: OTP) -> OTP:
    otp.is_used = True

    db.commit()
    db.refresh(otp)

    return otp


def increment_attempt(
    db: Session,
    otp: OTP
) -> OTP:

    otp.attempt_count += 1

    db.commit()
    db.refresh(otp)

    return otp


def delete_expired(db: Session) -> int:
    deleted_count = (
        db.query(OTP)
        .filter(
            OTP.expiry_time < datetime.now(timezone.utc)
        )
        .delete()
    )

    db.commit()

    return deleted_count