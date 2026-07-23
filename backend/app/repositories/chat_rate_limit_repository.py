# backend/app/repositories/chat_rate_limit_repository.py
"""
Chat Rate Limit Repository

Atomic, race-safe per-farmer daily message counting.

Uses Postgres INSERT ... ON CONFLICT DO UPDATE so two concurrent
requests from the same farmer can't both read count=N and both
proceed — the increment happens in a single round-trip, guarded
by the DB's own row-level locking on the unique constraint.

Module:
Phase 1 → Module 7 → AI Chat Assistant

Author: VerdiGO Backend Team
"""

from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.chat_rate_limit import ChatRateLimit


def increment_and_get_count(
    db: Session,
    farmer_profile_id: UUID,
    usage_date: date | None = None,
) -> int:
    """
    Atomically increment today's message count for a farmer and
    return the NEW count (post-increment) in one round-trip.

    First call of the day inserts a row with message_count=1.
    Subsequent calls increment the existing row.
    """

    usage_date = usage_date or date.today()

    stmt = (
        insert(ChatRateLimit)
        .values(
            farmer_profile_id=farmer_profile_id,
            usage_date=usage_date,
            message_count=1,
        )
        .on_conflict_do_update(
            index_elements=["farmer_profile_id", "usage_date"],
            set_={"message_count": ChatRateLimit.message_count + 1},
        )
        .returning(ChatRateLimit.message_count)
    )

    result = db.execute(stmt)
    db.commit()

    return result.scalar_one()


def get_today_count(
    db: Session,
    farmer_profile_id: UUID,
    usage_date: date | None = None,
) -> int:
    """
    Read-only count check (no increment). Useful for a future
    'usage remaining' endpoint without mutating state.
    """

    usage_date = usage_date or date.today()

    row = db.execute(
        select(ChatRateLimit.message_count).where(
            ChatRateLimit.farmer_profile_id == farmer_profile_id,
            ChatRateLimit.usage_date == usage_date,
        )
    ).scalar_one_or_none()

    return row or 0