from pydantic import BaseModel, Field
from app.schemas.user import UserResponse


class SendOTPRequest(BaseModel):
    mobile: str = Field(..., min_length=10, max_length=15)


class VerifyOTPRequest(BaseModel):
    mobile: str = Field(..., min_length=10, max_length=15)
    otp: str = Field(..., min_length=6, max_length=6)


class LoginRequest(BaseModel):
    mobile: str = Field(..., min_length=10, max_length=15)


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., min_length=1)


class LogoutRequest(BaseModel):
    """
    Refresh token is optional so logout still works (and blacklists
    the access token) even if the client lost the refresh token —
    but pass it whenever available for full revocation.
    """
    refresh_token: str | None = None


class OTPResponse(BaseModel):
    success: bool = True
    message: str


class LoginResponse(BaseModel):
    success: bool = True
    access_token: str
    refresh_token: str
    user: UserResponse


class RefreshResponse(BaseModel):
    success: bool = True
    access_token: str