"""
Dashboard Service

Business logic for the Dashboard module.

Responsibilities:
- Fetch dashboard information.
- Aggregate farmer information.
- Aggregate farm information.
- Aggregate dashboard statistics.

Module:
Phase 1 → Module 6 → User Dashboard

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories import (
    farmer_repository,
    farm_repository,
)
from app.schemas.dashboard import (
    DashboardDataSchema,
    DashboardStatisticsSchema,
)


# ============================================================================
# Dashboard Service
# ============================================================================

def get_dashboard_data(
    db: Session,
    current_user: User,
) -> DashboardDataSchema:
    """
    Returns complete dashboard data for the authenticated user.
    """

    # ------------------------------------------------------------------------
    # Farmer Information
    # ------------------------------------------------------------------------

    farmer = farmer_repository.get_by_user_id(
        db=db,
        user_id=current_user.id,
    )

    # ------------------------------------------------------------------------
    # Farm Information
    # ------------------------------------------------------------------------

    farms = farm_repository.get_all_by_farmer_profile_id(
        db=db,
        farmer_profile_id=farmer.id,
    )

    # ------------------------------------------------------------------------
    # Dashboard Statistics
    # ------------------------------------------------------------------------

    registered_days = (
        datetime.now(timezone.utc) - current_user.created_at
    ).days

    statistics = DashboardStatisticsSchema(
        profile_completed=farmer.is_profile_completed,
        total_farms=len(farms),
        registered_days=registered_days,
        completion_percentage=100 if farmer.is_profile_completed else 50,
    )

    # ------------------------------------------------------------------------
    # Dashboard Response
    # ------------------------------------------------------------------------

    return DashboardDataSchema(
        farmer=farmer,
        farms=farms,
        statistics=statistics,
    )