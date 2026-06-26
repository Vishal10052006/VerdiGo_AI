from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.auth import (
    SendOTPRequest,
    VerifyOTPRequest,
    LoginRequest,
    RefreshTokenRequest,
    OTPResponse,
    LoginResponse,
)
from app.schemas.common import SuccessResponse

from app.services.auth_service import (
    login_user,
    verify_otp,
    logout_user,
    refresh_access_token,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/send-otp",
    response_model=OTPResponse,
)
def send_otp(
    request: SendOTPRequest,
    db: Session = Depends(get_db),
):
    return login_user(
        db=db,
        mobile=request.mobile,
    )


@router.post(
    "/verify-otp",
    response_model=LoginResponse,
)
def verify_otp_route(
    request: VerifyOTPRequest,
    db: Session = Depends(get_db),
):
    return verify_otp(
        db=db,
        mobile=request.mobile,
        otp=request.otp,
    )


@router.post(
    "/login",
    response_model=OTPResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    return login_user(
        db=db,
        mobile=request.mobile,
    )


@router.post(
    "/logout",
    response_model=SuccessResponse,
)
def logout():
    return logout_user()


@router.post(
    "/refresh",
    response_model=SuccessResponse,
)
def refresh(
    request: RefreshTokenRequest,
):
    return refresh_access_token(
        refresh_token=request.refresh_token,
    )