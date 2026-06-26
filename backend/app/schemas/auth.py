from pydantic import BaseModel, Field
from app.schemas.user import UserResponse


class SendOTPRequest(BaseModel):
    mobile: str = Field(
        ...,
        min_length=10,
        max_length=15
    )


class VerifyOTPRequest(BaseModel):
    mobile: str = Field(
        ...,
        min_length=10,
        max_length=15
    )

    otp: str = Field(
        ...,
        min_length=6,
        max_length=6
    )


class LoginRequest(BaseModel):
    mobile: str = Field(
        ...,
        min_length=10,
        max_length=15
    )


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(
        ...,
        min_length=1
    )


class OTPResponse(BaseModel):
    success: bool = True
    message: str


class LoginResponse(BaseModel):
    success: bool = True
    access_token: str
    refresh_token: str
    user: UserResponse