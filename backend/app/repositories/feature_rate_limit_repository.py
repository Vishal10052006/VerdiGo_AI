"""
Feature Rate Limit Repository

Atomic, race-safe per-farmer-per-feature daily counting via
Postgres INSERT ... ON CONFLICT DO UPDATE (same pattern as
chat_rate_limit_repository.py — proven, keeping it consistent).

Module: Shared Infrastructure
Author: VerdiGO Backend Team
"""

from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.feature_rate_limit import FeatureRateLimit


def increment_and_get_count(
    db: Session,
    farmer_profile_id: UUID,
    feature: str,
    usage_date: date | None = None,
) -> int:
    """
    Atomically increment today's usage count for (farmer, feature)
    and return the NEW count in one round-trip.
    """

    usage_date = usage_date or date.today()

    stmt = (
        insert(FeatureRateLimit)
        .values(
            farmer_profile_id=farmer_profile_id,
            feature=feature,
            usage_date=usage_date,
            usage_count=1,
        )
        .on_conflict_do_update(
            index_elements=["farmer_profile_id", "feature", "usage_date"],
            set_={"usage_count": FeatureRateLimit.usage_count + 1},
        )
        .returning(FeatureRateLimit.usage_count)
    )

    result = db.execute(stmt)
    db.commit()

    return result.scalar_one()


def get_today_count(
    db: Session,
    farmer_profile_id: UUID,
    feature: str,
    usage_date: date | None = None,
) -> int:
    usage_date = usage_date or date.today()

    row = db.execute(
        select(FeatureRateLimit.usage_count).where(
            FeatureRateLimit.farmer_profile_id == farmer_profile_id,
            FeatureRateLimit.feature == feature,
            FeatureRateLimit.usage_date == usage_date,
        )
    ).scalar_one_or_none()

    return row or 0