from enum import Enum


class UserRole(str, Enum):
    FARMER = "farmer"
    ADMIN = "admin"


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class OTPStatus(str, Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    EXPIRED = "expired"


class AuthMessage:
    OTP_SENT = "OTP sent successfully."
    OTP_VERIFIED = "OTP verified successfully."
    INVALID_OTP = "Invalid OTP."
    OTP_EXPIRED = "OTP has expired."
    USER_CREATED = "User registered successfully."
    LOGIN_SUCCESS = "Login successful."
    UNAUTHORIZED = "Unauthorized."
    FORBIDDEN = "Forbidden."