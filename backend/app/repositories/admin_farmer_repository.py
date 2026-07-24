# backend/app/repositories/admin_farmer_repository.py
"""
Admin Farmer Management Repository

Read-heavy queries scoped for the admin panel — joins User +
FarmerProfile + Farm counts. Kept separate from farmer_repository.py
since that one serves the farmer-facing app with different shapes.

Module: Phase 1 → Module 10 → Admin Panel
Author: VerdiGO Backend Team
"""

from uuid import UUID

from sqlalchemy import func, or_
from sqlalchemy.orm import Session, joinedload

from app.models.user import User
from app.models.farmer_profile import FarmerProfile
from app.models.farm import Farm


def search_farmers(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    search: str | None = None,
    state: str | None = None,
    is_active: bool | None = None,
) -> tuple[list[dict], int]:
    """
    Paginated, filterable farmer list for the admin table.
    Returns (rows, total_count).
    """

    base_query = (
        db.query(
            User.id.label("user_id"),
            FarmerProfile.id.label("farmer_profile_id"),
            FarmerProfile.full_name,
            User.mobile,
            FarmerProfile.state,
            FarmerProfile.district,
            FarmerProfile.profile_completed,
            User.is_active,
            User.created_at,
            func.count(Farm.id).label("total_farms"),
        )
        .outerjoin(FarmerProfile, FarmerProfile.user_id == User.id)
        .outerjoin(Farm, Farm.farmer_profile_id == FarmerProfile.id)
        .filter(User.role == "farmer")
    )

    if search:
        like = f"%{search.strip()}%"
        base_query = base_query.filter(
            or_(
                FarmerProfile.full_name.ilike(like),
                User.mobile.ilike(like),
            )
        )

    if state:
        base_query = base_query.filter(FarmerProfile.state.ilike(state))

    if is_active is not None:
        base_query = base_query.filter(User.is_active.is_(is_active))

    grouped = base_query.group_by(
        User.id,
        FarmerProfile.id,
        FarmerProfile.full_name,
        User.mobile,
        FarmerProfile.state,
        FarmerProfile.district,
        FarmerProfile.profile_completed,
        User.is_active,
        User.created_at,
    )

    total = grouped.count()

    rows = (
        grouped.order_by(User.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [dict(row._mapping) for row in rows], total


def get_farmer_detail(db: Session, user_id: UUID) -> User | None:
    return (
        db.query(User)
        .options(
            joinedload(User.farmer_profile).joinedload(FarmerProfile.farms)
        )
        .filter(User.id == user_id, User.role == "farmer")
        .first()
    )


def set_active_status(db: Session, user: User, is_active: bool) -> User:
    user.is_active = is_active
    db.commit()
    db.refresh(user)
    return user