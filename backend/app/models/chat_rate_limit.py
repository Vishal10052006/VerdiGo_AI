# backend/app/models/chat_rate_limit.py
"""
Chat Rate Limit Model

Tracks per-farmer, per-day AI chat message counts to enforce
AI_DAILY_MESSAGE_LIMIT and control provider API cost.

One row per (farmer_profile_id, usage_date) — enforced by a
unique constraint so the atomic upsert in the repository can't
create duplicates under concurrent requests.

Module:
Phase 1 → Module 7 → AI Chat Assistant

Author: VerdiGO Backend Team
"""

import uuid

from sqlalchemy import Column, Date, DateTime, ForeignKey, Index, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base import Base


class ChatRateLimit(Base):
    __tablename__ = "chat_rate_limits"

    __table_args__ = (
        Index("idx_chat_rate_limit_farmer_date", "farmer_profile_id", "usage_date"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    farmer_profile_id = Column(
        UUID(as_uuid=True),
        ForeignKey("farmer_profiles.id", ondelete="CASCADE"),
        nullable=False,
    )

    usage_date = Column(Date, nullable=False)

    message_count = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )