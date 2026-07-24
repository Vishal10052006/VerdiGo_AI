"""
Feature Rate Limit Model

Generic per-farmer, per-feature, per-day usage counter.
Replaces the single-purpose ChatRateLimit pattern so any
future paid-AI feature (disease, pest, etc.) reuses this
same table instead of duplicating it.

Module: Shared Infrastructure
Author: VerdiGO Backend Team
"""

import uuid

from sqlalchemy import Column, Date, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base import Base


class FeatureRateLimit(Base):
    __tablename__ = "feature_rate_limits"

    __table_args__ = (
        Index(
            "idx_feature_rate_limit_lookup",
            "farmer_profile_id", "feature", "usage_date",
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    farmer_profile_id = Column(
        UUID(as_uuid=True),
        ForeignKey("farmer_profiles.id", ondelete="CASCADE"),
        nullable=False,
    )

    # e.g. "disease_detection", "pest_detection", "chat"
    feature = Column(String(50), nullable=False)

    usage_date = Column(Date, nullable=False)

    usage_count = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )