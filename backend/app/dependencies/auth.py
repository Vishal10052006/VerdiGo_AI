from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from sqlalchemy.orm import Session

from app.core.exceptions import (
    UnauthorizedException,
    ForbiddenException,
)

from app.database.database import get_db
from app.models.user import User
from app.repositories import user_repository, revocation_repository
from app.services.jwt_service import verify_token


bearer_scheme = HTTPBearer(auto_error=True)


def verify_access_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> dict:
    """
    Verify the access token's signature, type, and
    check it hasn't been revoked via logout.
    """

    payload = verify_token(
        token=credentials.credentials,
        token_type="access",
    )

    if payload is None:
        raise UnauthorizedException()

    # Reject if this exact token was blacklisted on logout,
    # even if it hasn't naturally expired yet.
    if revocation_repository.is_access_token_blacklisted(
        db=db,
        jti=payload["jti"],
    ):
        raise UnauthorizedException(message="Session has been logged out.")

    return payload


def verify_refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> dict:
    """
    Verify the refresh token and confirm it's still
    active in the refresh_tokens table.
    """

    payload = verify_token(
        token=credentials.credentials,
        token_type="refresh",
    )

    if payload is None:
        raise UnauthorizedException()

    if not revocation_repository.is_refresh_token_valid(
        db=db,
        jti=payload["jti"],
    ):
        raise UnauthorizedException(message="Refresh token has been revoked.")

    return payload


def get_current_user(
    payload: dict = Depends(verify_access_token),
    db: Session = Depends(get_db),
) -> User:

    user = user_repository.get_by_id(
        db=db,
        user_id=payload["sub"],
    )

    if user is None:
        raise UnauthorizedException()

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:

    if not current_user.is_active:
        raise ForbiddenException()

    return current_user


def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:

    if current_user.role != "admin":
        raise ForbiddenException()

    return current_user