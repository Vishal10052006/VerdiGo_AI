from fastapi import HTTPException, status


# =====================================================
# Generic Exceptions
# =====================================================

class BadRequestException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )


class UnauthorizedException(HTTPException):
    def __init__(self, message: str = "Unauthorized."):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message
        )


class ForbiddenException(HTTPException):
    def __init__(self, message: str = "Forbidden."):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )


class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )


# =====================================================
# Authentication Exceptions
# =====================================================

class InvalidOTPException(BadRequestException):
    def __init__(self):
        super().__init__("Invalid OTP.")


class OTPExpiredException(BadRequestException):
    def __init__(self):
        super().__init__("OTP has expired.")


class InvalidTokenException(UnauthorizedException):
    def __init__(self):
        super().__init__("Invalid or expired token.")