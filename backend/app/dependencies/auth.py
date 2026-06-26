from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.exceptions import (
    UnauthorizedException,
    ForbiddenException,
)
from app.database.database import get_db
from app.models.user import User
from app.repositories import user_repository
from app.services.jwt_service import verify_token


# =====================================================
# OAuth2 Authentication Scheme
#
# Extracts JWT from:
# Authorization: Bearer <access_token>
#
# tokenUrl is used by Swagger/OpenAPI to know
# where the login endpoint is.
# =====================================================
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# =====================================================
# Verify Access Token
#
# - Decode JWT
# - Verify signature
# - Verify expiration
# - Verify token type == "access"
#
# Returns:
#     Decoded JWT payload
# =====================================================
def verify_access_token(
    token: str = Depends(oauth2_scheme)
) -> dict:

    payload = verify_token(
        token=token,
        token_type="access"
    )

    if payload is None:
        raise UnauthorizedException()

    return payload


# =====================================================
# Verify Refresh Token
#
# Used only while creating
# a new access token.
# =====================================================
def verify_refresh_token(
    token: str = Depends(oauth2_scheme)
) -> dict:

    payload = verify_token(
        token=token,
        token_type="refresh"
    )

    if payload is None:
        raise UnauthorizedException()

    return payload


# =====================================================
# Current User Dependency
#
# Flow:
#
# Authorization Header
#        ↓
# OAuth2PasswordBearer
#        ↓
# Verify Access Token
#        ↓
# Get User ID from payload["sub"]
#        ↓
# Fetch latest user from database
#        ↓
# Return User model
#
# NOTE:
# Never trust JWT alone.
# Always fetch the latest user from the database.
# =====================================================
def get_current_user(
    payload: dict = Depends(verify_access_token),
    db: Session = Depends(get_db)
) -> User:

    user = user_repository.get_by_id(
        db=db,
        user_id=UUID(payload["sub"])
    )

    if user is None:
        raise UnauthorizedException()

    return user


# =====================================================
# Active User Dependency
#
# Ensures the authenticated user
# has an active account.
#
# Future use:
# Protect normal application routes.
# =====================================================
def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:

    if not current_user.is_active:
        raise ForbiddenException(
            detail="User account is inactive."
        )

    return current_user


# =====================================================
# Admin User Dependency
#
# Ensures the authenticated user
# has administrator privileges.
#
# Future use:
# Admin dashboard
# User management
# Analytics
# =====================================================
def get_current_admin_user(
    current_user: User = Depends(get_current_active_user)
) -> User:

    if current_user.role != "admin":
        raise ForbiddenException(
            detail="Admin access required."
        )

    return current_user