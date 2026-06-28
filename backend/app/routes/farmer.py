"""
Farmer API Routes

This module exposes all endpoints related to Farmer Profile
management in VerdiGO AI.

Responsibilities:
- Create Farmer Profile
- Update Farmer Profile
- Get Farmer Profile
"""

# ============================================================================
# Imports
# ============================================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.farmer import (
    FarmerProfileCreate,
    FarmerProfileUpdate,
    FarmerProfileResponse,
    FarmerProfileSuccessResponse,
)

from app.services.farmer_service import (
    create_farmer_profile,
    update_farmer_profile,
    get_farmer_profile,
)

from app.schemas.common import SuccessResponse


# ============================================================================
# Farmer Router
# ============================================================================

router = APIRouter(
    prefix="/farmer",
    tags=["Farmer"],
)


# ============================================================================
# Create Farmer Profile
# ============================================================================
@router.post(
    "/profile",
    response_model=FarmerProfileSuccessResponse,
)
def create_profile(
    request: FarmerProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a farmer profile for the authenticated user.
    """

    return create_farmer_profile(
        db=db,
        current_user=current_user,
        request=request,
    )


# ============================================================================
# Update Farmer Profile
# ============================================================================
@router.put(
    "/profile",
    response_model=FarmerProfileSuccessResponse,
)
def update_profile(
    request: FarmerProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update the authenticated user's farmer profile.
    """

    return update_farmer_profile(
        db=db,
        current_user=current_user,
        request=request,
    )


# ============================================================================
# Get Farmer Profile
# ============================================================================
@router.get(
    "/profile",
    response_model=FarmerProfileResponse,
)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get the authenticated user's farmer profile.
    """

    return get_farmer_profile(
        db=db,
        current_user=current_user,
    )