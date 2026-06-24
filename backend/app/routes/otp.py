from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.otp import SendOTPRequest
from app.database.database import get_db
from app.services.otp_service import save_otp

from app.schemas.otp import (
    SendOTPRequest,
    VerifyOTPRequest
)

from app.services.otp_service import (
    save_otp,
    verify_otp
)

router = APIRouter(
    prefix="/otp",
    tags=["OTP"]
)


@router.post("/send")
def send_otp(
    data: SendOTPRequest,
    db: Session = Depends(get_db)
):
    otp_record = save_otp(
        db=db,
        mobile=data.mobile
    )

    return {
        "mobile": otp_record.mobile,
        "otp": otp_record.otp,
        "message": "OTP generated and saved"
    }

@router.post("/verify")
def verify_otp_route(
    data: VerifyOTPRequest,
    db: Session = Depends(get_db)
):

    otp_record = verify_otp(
        db=db,
        mobile=data.mobile,
        otp=data.otp
    )

    if not otp_record:
        return {
            "verified": False,
            "message": "Invalid OTP"
        }

    return {
        "verified": True,
        "message": "OTP verified successfully"
    }