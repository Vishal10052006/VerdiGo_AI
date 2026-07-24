"""
Notification Routes

Module: Phase 1 → Module 9 → Notifications
Author: VerdiGO Backend Team
"""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.common import SuccessResponse
from app.schemas.notification import (
    NotificationListResponseSchema,
    NotificationResponseSchema,
    UnreadCountResponseSchema,
    MarkReadResponseSchema,
)
from app.services.notification_service import NotificationService
from app.repositories import farmer_repository
from app.core.exceptions import NotFoundException
from app.utils.response import success_response


router = APIRouter(prefix="/v1/notifications", tags=["Notifications"])


def _get_farmer_profile_id(db: Session, user_id: UUID) -> UUID:
    farmer_profile = farmer_repository.get_by_user_id(db=db, user_id=user_id)
    if farmer_profile is None:
        raise NotFoundException(message="Farmer profile not found.")
    return farmer_profile.id


@router.get("", response_model=SuccessResponse[NotificationListResponseSchema])
def get_notifications(
    skip: int = 0,
    limit: int = 20,
    unread_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve paginated notifications for the authenticated farmer."""
    farmer_profile_id = _get_farmer_profile_id(db, current_user.id)
    service = NotificationService(db)

    notifications = service.get_notifications(
        farmer_profile_id, skip, limit, unread_only
    )
    unread_count = service.get_unread_count(farmer_profile_id)

    return success_response(
        schema=NotificationListResponseSchema,
        data={
            "notifications": [
                NotificationResponseSchema.model_validate(n) for n in notifications
            ],
            "unread_count": unread_count,
        },
        message="Notifications retrieved successfully.",
    )


@router.get("/unread-count", response_model=SuccessResponse[UnreadCountResponseSchema])
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lightweight endpoint for the badge — poll this, not the full list."""
    farmer_profile_id = _get_farmer_profile_id(db, current_user.id)
    count = NotificationService(db).get_unread_count(farmer_profile_id)

    return success_response(
        schema=UnreadCountResponseSchema,
        data={"unread_count": count},
        message="Unread count retrieved successfully.",
    )


@router.patch("/{notification_id}/read", response_model=SuccessResponse[NotificationResponseSchema])
def mark_read(
    notification_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    farmer_profile_id = _get_farmer_profile_id(db, current_user.id)
    notification = NotificationService(db).mark_as_read(notification_id, farmer_profile_id)

    return success_response(
        schema=NotificationResponseSchema,
        data=NotificationResponseSchema.model_validate(notification),
        message="Notification marked as read.",
    )


@router.patch("/read-all", response_model=SuccessResponse[MarkReadResponseSchema])
def mark_all_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    farmer_profile_id = _get_farmer_profile_id(db, current_user.id)
    count = NotificationService(db).mark_all_as_read(farmer_profile_id)

    return success_response(
        schema=MarkReadResponseSchema,
        data={"marked_count": count},
        message="All notifications marked as read.",
    )