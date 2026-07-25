# backend/app/services/admin_auth_service.py — fixed

# backend/app/services/admin_auth_service.py
"""
Admin Auth Service

Module: Phase 1 → Module 10 → Admin Panel
Author: VerdiGO Backend Team
"""

import bcrypt
from sqlalchemy.orm import Session

from app.repositories import admin_repository
from app.services.jwt_service import create_access_token
from app.core.exceptions import UnauthorizedException, TooManyRequestsException
from app.utils.rate_limiter import admin_login_limiter
from app.constants.admin import (
    ADMIN_LOGIN_MAX_ATTEMPTS_PER_WINDOW,
    ADMIN_LOGIN_WINDOW_SECONDS,
)

_BCRYPT_MAX_BYTES = 72  # bcrypt's hard limit — enforce explicitly, don't rely on a library to catch it


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")

    if len(password_bytes) > _BCRYPT_MAX_BYTES:
        raise ValueError(f"Password must be at most {_BCRYPT_MAX_BYTES} bytes.")

    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False


def login_admin(db: Session, email: str, password: str) -> dict:
    """
    FIX: rate-limited per email (not per-IP — deliberate choice; an
    attacker rotating IPs against one known admin email is the more
    realistic threat model here than one IP spraying many emails, and
    per-email keying also naturally protects against distributed
    credential-stuffing on a single account without needing IP
    tracking/proxied-header trust concerns).

    Limit is checked and incremented BEFORE the password comparison —
    so even a correct password submitted after the window is exceeded
    is rejected, preventing an attacker who's found the right password
    on attempt 6 from an unthrottled 5-attempt lockout getting through.
    """

    email_normalized = email.lower().strip()

    if not admin_login_limiter.is_allowed(
        key=email_normalized,
        max_calls=ADMIN_LOGIN_MAX_ATTEMPTS_PER_WINDOW,
        window_seconds=ADMIN_LOGIN_WINDOW_SECONDS,
    ):
        retry_after = admin_login_limiter.seconds_until_next_allowed(
            key=email_normalized, window_seconds=ADMIN_LOGIN_WINDOW_SECONDS,
        )
        raise TooManyRequestsException(
            message=(
                f"Too many login attempts. Please try again in "
                f"{retry_after} seconds."
            )
        )

    admin = admin_repository.get_by_email(db=db, email=email_normalized)

    if admin is None or not verify_password(password, admin.password_hash):
        raise UnauthorizedException(message="Invalid email or password.")

    if not admin.is_active:
        raise UnauthorizedException(message="This admin account has been deactivated.")

    access_token, _jti, _exp = create_access_token(f"admin:{admin.id}")

    admin_repository.update_last_login(db=db, admin=admin)

    return {"access_token": access_token, "admin": admin}