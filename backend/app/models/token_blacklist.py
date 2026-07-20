"""
Token Blacklist Model

Stores access-token JTIs that have been explicitly revoked
(via logout) before their natural expiry. Checked on every
authenticated request.

Rows are safe to purge once expires_at has passed — run
`delete_expired_blacklist_entries` on a schedule (cron / background job).

Module:
Phase 1 → Module 1 → Authentication (Hardening)

Author: VerdiGO Backend Team
"""

import uuid

from sqlalchemy import Column, DateTime, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base import Base


class TokenBlacklist(Base):
    """
    Represents a revoked access token, identified by its JTI.
    """

    __tablename__ = "token_blacklist"

    __table_args__ = (
        Index("idx_blacklist_jti", "jti"),
        Index("idx_blacklist_expiry", "expires_at"),
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    jti = Column(
        String(64),
        nullable=False,
        unique=True,
        index=True,
    )

    # Mirrors the token's own expiry so cleanup jobs know
    # when it's safe to delete this row (token would be
    # invalid anyway after this point).
    expires_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )