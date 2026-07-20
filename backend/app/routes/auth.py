"""
Authentication API Routes
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.auth import (
    SendOTPRequest,
    VerifyOTPRequest,
    LoginRequest,
    RefreshTokenRequest,
    LogoutRequest,
    OTPResponse,
    LoginResponse,
    RefreshResponse,
)
from app.schemas.common import SuccessResponse
from app.schemas.user import UserResponse

from app.models.user import User

from app.dependencies.auth import get_current_user, verify_access_token

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


@router.post("/send-otp", response_model=OTPResponse)
def send_otp(request: SendOTPRequest, db: Session = Depends(get_db)):
    return login_user(db=db, mobile=request.mobile)


@router.post("/verify-otp", response_model=LoginResponse)
def verify_otp_route(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    return verify_otp(db=db, mobile=request.mobile, otp=request.otp)


@router.post("/login", response_model=OTPResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db=db, mobile=request.mobile)


@router.post("/logout", response_model=SuccessResponse[dict])
def logout(
    request: LogoutRequest,
    db: Session = Depends(get_db),
    access_payload: dict = Depends(verify_access_token),
):
    """
    Logs the user out server-side:
    - Blacklists the current access token
    - Revokes the supplied refresh token
    """

    return logout_user(
        db=db,
        access_token_payload=access_payload,
        refresh_token=request.refresh_token,
    )


@router.post("/refresh", response_model=RefreshResponse)
def refresh(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    return refresh_access_token(db=db, refresh_token=request.refresh_token)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user