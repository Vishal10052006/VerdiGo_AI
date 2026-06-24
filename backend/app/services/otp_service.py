import random

from sqlalchemy.orm import Session

from app.models.otp import OTP


def save_otp(db: Session, mobile: str):

    otp = str(random.randint(100000, 999999))

    otp_record = OTP(
        mobile=mobile,
        otp=otp
    )

    db.add(otp_record)
    db.commit()
    db.refresh(otp_record)

    return otp_record


def verify_otp(
    db: Session,
    mobile: str,
    otp: str
):

    otp_record = (
        db.query(OTP)
        .filter(
            OTP.mobile == mobile,
            OTP.otp == otp
        )
        .order_by(OTP.created_at.desc())
        .first()
    )

    return otp_record