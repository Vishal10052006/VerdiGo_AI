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


# ============================================================================
# OTP Send Rate Limiting
#
# Previously /auth/send-otp had NO throttling whatsoever — an attacker
# (or a buggy retry loop on the frontend) could call it in a tight loop,
# either exhausting your SMS provider budget or spamming an arbitrary
# phone number with OTP texts (harassment vector against a number that
# isn't even the attacker's). OTP verification itself has attempt
# counting (OTP_MAX_ATTEMPTS in settings), but that only limits guessing
# an already-sent OTP — it does nothing to stop OTP *send* spam.
# ============================================================================

OTP_SEND_MAX_PER_WINDOW = 5       # max OTP sends per phone number per window
OTP_SEND_WINDOW_SECONDS = 600     # 10 minutes