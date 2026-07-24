"""
Notification Model

Stores all in-app notifications for a farmer — weather alerts,
disease alerts, and future system/crop notifications.

Design note: farmer_profile_id (not user_id) is the FK, matching
the ownership pattern used by Farm, ChatConversation, etc. — every
other user-facing resource in this codebase is scoped through
FarmerProfile, so Notification follows the same convention for
consistent ownership-check code across repositories.

Module: Phase 1 → Module 9 → Notifications
Author: VerdiGO Backend Team
"""

import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base
from app.enums.notification import NotificationTypeEnum, NotificationSeverityEnum


class Notification(Base):
    """
    A single in-app notification delivered to a farmer.
    """

    __tablename__ = "notifications"

    __table_args__ = (
        Index("idx_notification_farmer", "farmer_profile_id"),
        Index("idx_notification_farmer_read", "farmer_profile_id", "is_read"),
        Index("idx_notification_created", "created_at"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    farmer_profile_id = Column(
        UUID(as_uuid=True),
        ForeignKey("farmer_profiles.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ------------------------------------------------------------
    # Content
    # ------------------------------------------------------------

    type = Column(Enum(NotificationTypeEnum), nullable=False)

    severity = Column(
        Enum(NotificationSeverityEnum),
        nullable=False,
        default=NotificationSeverityEnum.INFO,
    )

    title = Column(String(150), nullable=False)

    message = Column(Text, nullable=False)

    # Optional pointer to the source record (weather_advisory.id,
    # disease_detection.id, etc.) so the frontend can deep-link
    # "View Details" without a separate join table per source type.
    related_entity_id = Column(UUID(as_uuid=True), nullable=True)

    related_entity_type = Column(String(50), nullable=True)

    # ------------------------------------------------------------
    # Read Status
    # ------------------------------------------------------------

    is_read = Column(Boolean, default=False, nullable=False)

    read_at = Column(DateTime(timezone=True), nullable=True)

    # ------------------------------------------------------------
    # Audit
    # ------------------------------------------------------------

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # ------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------

    farmer_profile = relationship("FarmerProfile")