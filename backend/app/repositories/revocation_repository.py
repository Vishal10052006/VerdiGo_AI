"""
Revocation Repository

Database operations for refresh token tracking and
access token blacklisting.

Module:
Phase 1 → Module 1 → Authentication (Hardening)

Author: VerdiGO Backend Team
"""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken
from app.models.token_blacklist import TokenBlacklist


# ============================================================================
# Refresh Token Tracking
# ============================================================================

def store_refresh_token(
    db: Session,
    user_id: UUID,
    jti: str,
    expires_at: datetime,
) -> RefreshToken:
    """
    Persist a newly issued refresh token.
    """

    record = RefreshToken(
        user_id=user_id,
        jti=jti,
        expires_at=expires_at,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


def is_refresh_token_valid(db: Session, jti: str) -> bool:
    """
    Check whether a refresh token is still valid
    (exists, not revoked, not expired).
    """

    record = (
        db.query(RefreshToken)
        .filter(RefreshToken.jti == jti)
        .first()
    )

    if record is None:
        return False

    if record.revoked:
        return False

    if record.expires_at <= datetime.now(timezone.utc):
        return False

    return True


def revoke_refresh_token(db: Session, jti: str) -> None:
    """
    Revoke a single refresh token (used on logout).
    """

    record = (
        db.query(RefreshToken)
        .filter(RefreshToken.jti == jti)
        .first()
    )

    if record is None:
        return

    record.revoked = True
    record.revoked_at = datetime.now(timezone.utc)

    db.commit()


def revoke_all_refresh_tokens_for_user(db: Session, user_id: UUID) -> int:
    """
    Revoke every active refresh token for a user
    (used for "logout everywhere" / password reset / account compromise).
    """

    updated = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked.is_(False),
        )
        .update(
            {
                "revoked": True,
                "revoked_at": datetime.now(timezone.utc),
            }
        )
    )

    db.commit()

    return updated


# ============================================================================
# Access Token Blacklist
# ============================================================================

def blacklist_access_token(
    db: Session,
    jti: str,
    expires_at: datetime,
) -> None:
    """
    Blacklist an access token so it's rejected immediately,
    even though it hasn't naturally expired yet.
    """

    exists = (
        db.query(TokenBlacklist)
        .filter(TokenBlacklist.jti == jti)
        .first()
    )

    if exists:
        return

    db.add(
        TokenBlacklist(
            jti=jti,
            expires_at=expires_at,
        )
    )
    db.commit()


def is_access_token_blacklisted(db: Session, jti: str) -> bool:
    """
    Check whether an access token has been blacklisted.
    """

    return (
        db.query(TokenBlacklist)
        .filter(TokenBlacklist.jti == jti)
        .first()
        is not None
    )


def delete_expired_blacklist_entries(db: Session) -> int:
    """
    Cleanup job — remove blacklist rows for tokens that would
    have expired naturally anyway. Safe to run on a schedule.
    """

    deleted = (
        db.query(TokenBlacklist)
        .filter(TokenBlacklist.expires_at <= datetime.now(timezone.utc))
        .delete()
    )

    db.commit()

    return deleted