"""
Refresh Token Model

Persists issued refresh tokens so they can be revoked
server-side on logout. Without this table, JWTs are
stateless and logout can only ever be client-side.

Responsibilities:
- Track every issued refresh token by its JTI (not the raw token)
- Allow revocation on logout
- Allow revocation of all sessions (e.g. "logout everywhere")

Module:
Phase 1 → Module 1 → Authentication (Hardening)

Author: VerdiGO Backend Team
"""

import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class RefreshToken(Base):
    """
    Represents a single issued refresh token session.
    """

    __tablename__ = "refresh_tokens"

    __table_args__ = (
        Index("idx_refresh_token_jti", "jti"),
        Index("idx_refresh_token_user", "user_id"),
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # JWT ID — unique identifier embedded in the token's "jti" claim.
    # We never store the raw token itself.
    jti = Column(
        String(64),
        nullable=False,
        unique=True,
        index=True,
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    revoked = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    expires_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    revoked_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    user = relationship("User")