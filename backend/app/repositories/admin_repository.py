# backend/app/repositories/admin_repository.py
"""
Admin Repository

Module: Phase 1 → Module 10 → Admin Panel
Author: VerdiGO Backend Team
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.admin_user import AdminUser


def get_by_email(db: Session, email: str) -> AdminUser | None:
    return db.query(AdminUser).filter(AdminUser.email == email).first()


def get_by_id(db: Session, admin_id: UUID) -> AdminUser | None:
    return db.query(AdminUser).filter(AdminUser.id == admin_id).first()


def update_last_login(db: Session, admin: AdminUser) -> AdminUser:
    from sqlalchemy.sql import func

    admin.last_login_at = func.now()
    db.commit()
    db.refresh(admin)
    return admin


def create(db: Session, admin: AdminUser) -> AdminUser:
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin