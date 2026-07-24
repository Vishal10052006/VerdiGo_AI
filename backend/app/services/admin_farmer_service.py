# backend/app/services/admin_farmer_service.py
"""
Admin Farmer Management Service

Module: Phase 1 → Module 10 → Admin Panel
Author: VerdiGO Backend Team
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories import admin_farmer_repository
from app.core.exceptions import NotFoundException


DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


def list_farmers(
    db: Session,
    page: int = 1,
    page_size: int = DEFAULT_PAGE_SIZE,
    search: str | None = None,
    state: str | None = None,
    is_active: bool | None = None,
) -> dict:
    page = max(page, 1)
    page_size = min(max(page_size, 1), MAX_PAGE_SIZE)

    rows, total = admin_farmer_repository.search_farmers(
        db=db,
        skip=(page - 1) * page_size,
        limit=page_size,
        search=search,
        state=state,
        is_active=is_active,
    )

    return {"farmers": rows, "total": total, "page": page, "page_size": page_size}


def get_farmer_detail(db: Session, user_id: UUID) -> dict:
    user = admin_farmer_repository.get_farmer_detail(db=db, user_id=user_id)

    if user is None:
        raise NotFoundException(message="Farmer not found.")

    profile = user.farmer_profile

    return {
        "user_id": user.id,
        "mobile": user.mobile,
        "email": user.email,
        "is_active": user.is_active,
        "created_at": user.created_at,
        "full_name": profile.full_name if profile else None,
        "age": profile.age if profile else None,
        "state": profile.state if profile else None,
        "district": profile.district if profile else None,
        "village": profile.village if profile else None,
        "profile_completed": profile.profile_completed if profile else False,
        "farms": profile.farms if profile else [],
    }


def set_farmer_status(db: Session, user_id: UUID, is_active: bool) -> dict:
    user = admin_farmer_repository.get_farmer_detail(db=db, user_id=user_id)

    if user is None:
        raise NotFoundException(message="Farmer not found.")

    updated = admin_farmer_repository.set_active_status(db=db, user=user, is_active=is_active)

    return get_farmer_detail(db=db, user_id=updated.id)