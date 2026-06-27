"""
Authentication API Routes

This module exposes all endpoints required for OTP-based
authentication and JWT authorization in VerdiGO AI.

Responsibilities:
- Send OTP
- Verify OTP
- Login
- Logout
- Refresh Access Token
- Return Current Authenticated User
"""

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
    RefreshResponse
)
from app.schemas.common import SuccessResponse
from app.schemas.user import UserResponse

from app.models.user import User

from app.dependencies.auth import get_current_user

from app.services.auth_service import (
    login_user,
    verify_otp,
    logout_user,
    refresh_access_token,
)


# =====================================================
# Authentication Router
#
# Handles all authentication-related APIs.
#
# Available Endpoints:
#
# POST  /auth/send-otp
# POST  /auth/verify-otp
# POST  /auth/login
# POST  /auth/logout
# POST  /auth/refresh
# GET   /auth/me
# =====================================================
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# =====================================================
# Send OTP
#
# Sends an OTP to the user's mobile number.
#
# Flow:
# Mobile Number
#        ↓
# Generate OTP
#        ↓
# Save OTP
#        ↓
# Send SMS
# =====================================================
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


# =====================================================
# Verify OTP
#
# Verifies the OTP entered by the user.
#
# On Success:
# • Registers user (if new)
# • Creates Access Token
# • Creates Refresh Token
#
# Returns authenticated user information.
# =====================================================
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


# =====================================================
# Login
#
# Requests a new OTP for an existing or new user.
#
# This endpoint behaves the same as /send-otp.
# It exists to provide a cleaner authentication API.
# =====================================================
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


# =====================================================
# Logout
#
# Currently performs client-side logout.
#
# Future Improvements:
# • Token blacklist
# • Refresh token revocation
# • Session invalidation
# =====================================================
@router.post(
    "/logout",
    response_model=SuccessResponse,
)
def logout():
    return logout_user()


# =====================================================
# Refresh Access Token
#
# Uses a valid Refresh Token
# to generate a new Access Token.
#
# Future Use:
# • Validate refresh token against stored sessions
# • Rotate refresh tokens after each refresh
# • Revoke refresh token on logout or suspicious activity
#
# Access Token Expired
#          ↓
# Refresh Token
#          ↓
# New Access Token
# =====================================================
@router.post(
    "/refresh",
    response_model=RefreshResponse,
)
def refresh(
    request: RefreshTokenRequest,
):
    return refresh_access_token(
        refresh_token=request.refresh_token,
    )


# =====================================================
# Current User
#
# Returns the currently authenticated user.
#
# Authentication Flow:
#
# Authorization Header
#          ↓
# OAuth2PasswordBearer
#          ↓
# Verify Access Token
#          ↓
# Extract User ID (sub)
#          ↓
# Load User From Database
#          ↓
# Return User Profile
#
# Used by:
# • Mobile App Startup
# • Dashboard
# • Profile Screen
# • Token Validation
# =====================================================
@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user
