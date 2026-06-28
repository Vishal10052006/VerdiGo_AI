"""
Farm API Routes

This module exposes all endpoints related to Farm management.

Responsibilities:
- Create Farm

Module:
Phase 1 → Module 2 → Farmer Registration

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.common import SuccessResponse
from app.schemas.farm import (
    FarmCreate,
    FarmUpdate,
    FarmResponse,
)

from app.services.farm_service import (
    create_farm,
    update_farm,
    get_farm,
)


# ============================================================================
# Farm Router
# ============================================================================

router = APIRouter(
    prefix="/farm",
    tags=["Farm"],
)


# ============================================================================
# Create Farm
# ============================================================================

@router.post(
    "",
    response_model=SuccessResponse,
)
def create_farm_route(
    request: FarmCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a farm for the authenticated user.
    """

    return create_farm(
        db=db,
        current_user=current_user,
        request=request,
    )


# ============================================================================
# Update Farm
# ============================================================================

@router.put(
    "",
    response_model=SuccessResponse,
)
def update(
    request: FarmUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update the authenticated farmer's farm.
    """

    return update_farm(
        db=db,
        current_user=current_user,
        request=request,
    )


# ============================================================================
# Get Farm
# ============================================================================

@router.get(
    "",
    response_model=FarmResponse,
)
def get_farm_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get the authenticated farmer's farm.
    """

    return get_farm(
        db=db,
        current_user=current_user,
    )