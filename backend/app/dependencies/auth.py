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
from app.repositories import user_repository
from app.services.jwt_service import verify_token


# =====================================================
# HTTP Bearer Authentication Scheme
#
# Reads JWT from:
#
# Authorization: Bearer <access_token>
#
# Used by all protected APIs.
# =====================================================
bearer_scheme = HTTPBearer(
    auto_error=True
)


# =====================================================
# Verify Access Token
#
# Flow:
# Authorization Header
#        ↓
# HTTPBearer
#        ↓
# Extract JWT
#        ↓
# Verify Signature
#        ↓
# Verify Expiry
#        ↓
# Verify Token Type
#        ↓
# Return JWT Payload
# =====================================================
def verify_access_token(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    )
) -> dict:

    print("=" * 60)
    print("Authorization Scheme:", credentials.scheme)
    print("Received Token:", credentials.credentials)
    print("=" * 60)

    payload = verify_token(
        token=credentials.credentials,
        token_type="access"
    )

    print("Decoded Payload:", payload)

    if payload is None:
        raise UnauthorizedException()

    return payload


# =====================================================
# Verify Refresh Token
#
# Used only while issuing
# a new access token.
# =====================================================
def verify_refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    )
) -> dict:

    payload = verify_token(
        token=credentials.credentials,
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
# HTTPBearer
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
        user_id=payload["sub"]
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
# Future Use:
# Protect application routes.
# =====================================================
def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:

    if not current_user.is_active:
        raise ForbiddenException()

    return current_user


# =====================================================
# Admin User Dependency
#
# Ensures the authenticated user
# has administrator privileges.
#
# Future Use:
# - Admin Dashboard
# - User Management
# - Analytics
# =====================================================
def get_current_admin_user(
    current_user: User = Depends(get_current_active_user)
) -> User:

    if current_user.role != "admin":
        raise ForbiddenException()

    return current_user