"""
Notification Repository

Module: Phase 1 → Module 9 → Notifications
Author: VerdiGO Backend Team
"""

from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.notification import Notification


def create(db: Session, notification: Notification) -> Notification:
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def get_for_farmer(
    db: Session,
    farmer_profile_id: UUID,
    skip: int = 0,
    limit: int = 20,
    unread_only: bool = False,
) -> list[Notification]:
    query = db.query(Notification).filter(
        Notification.farmer_profile_id == farmer_profile_id
    )

    if unread_only:
        query = query.filter(Notification.is_read.is_(False))

    return (
        query.order_by(Notification.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_by_id_for_farmer(
    db: Session, notification_id: UUID, farmer_profile_id: UUID
) -> Notification | None:
    """Ownership-scoped lookup — same 404-not-403 pattern as every other module."""
    return (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.farmer_profile_id == farmer_profile_id,
        )
        .first()
    )


def get_unread_count(db: Session, farmer_profile_id: UUID) -> int:
    return (
        db.query(func.count(Notification.id))
        .filter(
            Notification.farmer_profile_id == farmer_profile_id,
            Notification.is_read.is_(False),
        )
        .scalar()
    ) or 0


def mark_read(db: Session, notification: Notification) -> Notification:
    if not notification.is_read:
        notification.is_read = True
        notification.read_at = func.now()
        db.commit()
        db.refresh(notification)
    return notification


def mark_all_read(db: Session, farmer_profile_id: UUID) -> int:
    updated = (
        db.query(Notification)
        .filter(
            Notification.farmer_profile_id == farmer_profile_id,
            Notification.is_read.is_(False),
        )
        .update({"is_read": True, "read_at": func.now()}, synchronize_session=False)
    )
    db.commit()
    return updated