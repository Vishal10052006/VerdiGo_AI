"""
OTP Rate Limit Model

Tracks OTP send requests per mobile number to prevent SMS-bombing
and SMS budget exhaustion (send-otp was previously unlimited —
Module 1 review finding).

One row per mobile number. `window_start` marks when the current
counting window began; the repository decides whether to reset it
(window expired) or increment it (still inside window). This is a
fixed-window limiter, not sliding — appropriate for OTP-scale abuse
(bursts over minutes), and far simpler than a sliding log while
still race-safe via atomic upsert.

Module:
Phase 1 → Module 1 → Authentication (Hardening)

Author: VerdiGO Backend Team
"""

import uuid

from sqlalchemy import Column, DateTime, Index, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base import Base


class OTPRateLimit(Base):
    """
    Per-mobile-number OTP send rate limit tracker.
    """

    __tablename__ = "otp_rate_limits"

    __table_args__ = (
        Index("idx_otp_rate_limit_mobile", "mobile"),
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    mobile = Column(
        String(20),
        nullable=False,
        unique=True,
    )

    window_start = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    request_count = Column(
        Integer,
        nullable=False,
        default=0,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )