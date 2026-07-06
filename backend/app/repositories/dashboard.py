"""
Dashboard Repository

This module contains all database operations related to the Dashboard.

Responsibilities:
- Retrieve dashboard data
- Load farmer profile
- Load related farms

Module:
Phase 1 → Module 4 → Dashboard

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.models.farmer_profile import FarmerProfile


# ============================================================================
# Get Dashboard Data
# ============================================================================

def get_dashboard_data(
    db: Session,
    user_id: UUID,
) -> FarmerProfile | None:
    """
    Retrieve dashboard data for the authenticated user.

    Returns:
        FarmerProfile | None
    """

    return (
        db.query(FarmerProfile)
        .options(
            selectinload(FarmerProfile.farms),
            selectinload(FarmerProfile.user),
        )
        .filter(
            FarmerProfile.user_id == user_id
        )
        .first()
    )