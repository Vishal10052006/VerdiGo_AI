"""
JWT Service

Responsibilities:
- Issue access/refresh tokens with a unique jti (JWT ID)
- Decode & verify tokens
- jti enables server-side revocation (blacklist / refresh table)

Module:
Phase 1 → Module 1 → Authentication

Author: VerdiGO Backend Team
"""

import uuid
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.config.settings import settings


def _new_jti() -> str:
    """Generate a unique token identifier."""
    return uuid.uuid4().hex


def create_access_token(user_id: str) -> tuple[str, str, datetime]:
    """
    Create an access token.

    Returns:
        (token, jti, expires_at) — jti/expires_at let the caller
        blacklist this exact token later if needed.
    """

    jti = _new_jti()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": user_id,
        "jti": jti,
        "exp": expire,
        "type": "access",
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return token, jti, expire


def create_refresh_token(user_id: str) -> tuple[str, str, datetime]:
    """
    Create a refresh token.

    Returns:
        (token, jti, expires_at) — caller persists (user_id, jti, expires_at)
        in the refresh_tokens table so it can be revoked later.
    """

    jti = _new_jti()
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    payload = {
        "sub": user_id,
        "jti": jti,
        "exp": expire,
        "type": "refresh",
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return token, jti, expire


def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload

    except JWTError:
        return None


def verify_token(token: str, token_type: str = "access") -> dict | None:
    payload = decode_token(token)

    if payload is None:
        return None

    if payload.get("type") != token_type:
        return None

    # jti is mandatory on every token issued after this change.
    # Tokens without it (pre-migration) are rejected — forces
    # re-login instead of silently trusting an unrevocable token.
    if not payload.get("jti"):
        return None

    return payload