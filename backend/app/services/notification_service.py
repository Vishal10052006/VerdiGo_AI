"""
Notification Service

Public API for creating and reading notifications. Other services
(weather, disease) call `NotificationService.notify(...)` directly —
kept deliberately simple (no event bus/queue) since MVP scale
doesn't need it; swap for a pub/sub if notification sources grow
past a handful of callers.

Module: Phase 1 → Module 9 → Notifications
Author: VerdiGO Backend Team
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.enums.notification import NotificationTypeEnum, NotificationSeverityEnum
from app.models.notification import Notification
from app.repositories import notification_repository
from app.core.exceptions import NotFoundException


class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------------
    # Create (called internally by other services)
    # ------------------------------------------------------------------------

    def notify(
        self,
        farmer_profile_id: UUID,
        type: NotificationTypeEnum,
        severity: NotificationSeverityEnum,
        title: str,
        message: str,
        related_entity_id: UUID | None = None,
        related_entity_type: str | None = None,
    ) -> Notification:
        notification = Notification(
            farmer_profile_id=farmer_profile_id,
            type=type,
            severity=severity,
            title=title,
            message=message,
            related_entity_id=related_entity_id,
            related_entity_type=related_entity_type,
        )

        return notification_repository.create(self.db, notification)

    # ------------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------------

    def get_notifications(
        self,
        farmer_profile_id: UUID,
        skip: int = 0,
        limit: int = 20,
        unread_only: bool = False,
    ) -> list[Notification]:
        return notification_repository.get_for_farmer(
            self.db, farmer_profile_id, skip, limit, unread_only
        )

    def get_unread_count(self, farmer_profile_id: UUID) -> int:
        return notification_repository.get_unread_count(self.db, farmer_profile_id)

    # ------------------------------------------------------------------------
    # Mark Read
    # ------------------------------------------------------------------------

    def mark_as_read(
        self, notification_id: UUID, farmer_profile_id: UUID
    ) -> Notification:
        notification = notification_repository.get_by_id_for_farmer(
            self.db, notification_id, farmer_profile_id
        )
        if notification is None:
            raise NotFoundException(message="Notification not found.")

        return notification_repository.mark_read(self.db, notification)

    def mark_all_as_read(self, farmer_profile_id: UUID) -> int:
        return notification_repository.mark_all_read(self.db, farmer_profile_id)