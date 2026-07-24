"""
Notification Schemas

Module: Phase 1 → Module 9 → Notifications
Author: VerdiGO Backend Team
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums.notification import NotificationTypeEnum, NotificationSeverityEnum


class NotificationResponseSchema(BaseModel):
    id: UUID
    type: NotificationTypeEnum
    severity: NotificationSeverityEnum
    title: str
    message: str
    related_entity_id: UUID | None = None
    related_entity_type: str | None = None
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NotificationListResponseSchema(BaseModel):
    notifications: list[NotificationResponseSchema]
    unread_count: int


class UnreadCountResponseSchema(BaseModel):
    unread_count: int


class MarkReadResponseSchema(BaseModel):
    marked_count: int