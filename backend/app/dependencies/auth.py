from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.exceptions import ForbiddenException

from app.core.security import verify_token


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/verify-otp"
)


def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    payload = verify_token(token)

    return payload


def get_current_active_user(
    current_user: dict = Depends(get_current_user)
):
    return current_user


def get_current_admin(
    current_user: dict = Depends(get_current_user)
):
    if current_user.get("role") != "admin":
        raise ForbiddenException()

    return current_user