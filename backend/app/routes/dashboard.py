"""
Dashboard Routes

Module:
Phase 1 → Module 4 → Dashboard
"""

# ============================================================================
# Imports
# ============================================================================

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user

from app.schemas.common import SuccessResponse, ErrorResponse

from app.services.dashboard import (
    get_dashboard_summary as dashboard_summary_service,
)
from app.constants.dashboard import (
    DASHBOARD_LOADED,
    FARMER_PROFILE_NOT_FOUND,
    FARMER_OVERVIEW_LOADED
)

from app.schemas.dashboard import FarmerOverviewResponse

from app.models.user import User


# ============================================================================
# Router
# ============================================================================

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


# ============================================================================
# Dashboard Summary
# ============================================================================

@router.get(
    "",
    response_model=SuccessResponse,
    responses={404: {"model": ErrorResponse}},
)
def get_dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SuccessResponse:
    """
    Dashboard Summary API.
    """

    dashboard = dashboard_summary_service(
        db=db,
        user_id=current_user.id,
    )

    if dashboard is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=FARMER_PROFILE_NOT_FOUND,
        )

    return SuccessResponse(
        message=DASHBOARD_LOADED,
        data=dashboard,
    )


# ============================================================================
# Farmer Overview
# ============================================================================

@router.get(
    "/overview",
    response_model=SuccessResponse,
    responses={404: {"model": ErrorResponse}},
)
def farmer_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SuccessResponse:
    """
    Farmer Overview API.
    """

    dashboard = dashboard_summary_service(
        db=db,
        user_id=current_user.id,
    )

    if dashboard is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=FARMER_PROFILE_NOT_FOUND,
        )

    return SuccessResponse(
        message=FARMER_OVERVIEW_LOADED,
        data=FarmerOverviewResponse(
            farmer=dashboard.farmer,
            farms=dashboard.farms,
        ),
    )