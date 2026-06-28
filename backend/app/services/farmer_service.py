"""
Farmer Service

This module contains all business logic related to Farmer Profiles.

Responsibilities:
- Create farmer profile
- Update farmer profile
- Retrieve farmer profile
- Prevent duplicate profiles

Module:
Phase 1 → Module 2 → Farmer Registration

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.farmer_profile import FarmerProfile

from app.schemas.farmer import (
    FarmerProfileCreate,
    FarmerProfileUpdate,
    FarmerProfileResponse,
)

from app.repositories import farmer_repository

from app.core.exceptions import (
    BadRequestException,
    NotFoundException,
)


# ============================================================================
# Create Farmer Profile
# ============================================================================

def create_farmer_profile(
    db: Session,
    current_user: User,
    request: FarmerProfileCreate,
) -> dict:
    """
    Create a farmer profile for the authenticated user.
    """

    # ------------------------------------------------------------------------
    # Check if profile already exists
    # ------------------------------------------------------------------------

    existing_profile = farmer_repository.get_by_user_id(
        db=db,
        user_id=current_user.id,
    )

    if existing_profile:
        raise BadRequestException(
            message="Farmer profile already exists."
        )

    # ------------------------------------------------------------------------
    # Create Farmer Profile Model
    # ------------------------------------------------------------------------

    farmer_profile = FarmerProfile(
        user_id=current_user.id,
        full_name=request.full_name,
        age=request.age,
        gender=request.gender,
        state=request.state,
        district=request.district,
        village=request.village,
        profile_completed=False,
    )

    # ------------------------------------------------------------------------
    # Save Profile
    # ------------------------------------------------------------------------

    farmer_profile = farmer_repository.create(
        db=db,
        farmer_profile=farmer_profile,
    )

    # ------------------------------------------------------------------------
    # Return Response
    # ------------------------------------------------------------------------

    return {
        "success": True,
        "message": "Farmer profile created successfully.",
        "data": farmer_profile,
    }


# ============================================================================
# Get Farmer Profile
# ============================================================================

def get_farmer_profile(
    db: Session,
    current_user: User,
) -> FarmerProfile:
    """
    Retrieve the authenticated user's farmer profile.
    """

    farmer_profile = farmer_repository.get_by_user_id(
        db=db,
        user_id=current_user.id,
    )

    if farmer_profile is None:
        raise NotFoundException(
            message="Farmer profile not found."
        )

    return FarmerProfileResponse.model_validate(
        farmer_profile,
        from_attributes=True,
    )


# ============================================================================
# Update Farmer Profile
# ============================================================================

def update_farmer_profile(
    db: Session,
    current_user: User,
    request: FarmerProfileUpdate,
) -> dict:
    """
    Update the authenticated user's farmer profile.
    """

    farmer_profile = farmer_repository.get_by_user_id(
        db=db,
        user_id=current_user.id,
    )

    if farmer_profile is None:
        raise NotFoundException(
            message="Farmer profile not found."
        )

    updated_profile = farmer_repository.update(
        db=db,
        farmer_profile=farmer_profile,
        data=request.model_dump(exclude_unset=True),
    )

    return {
        "success": True,
        "message": "Farmer profile updated successfully.",
        "data": FarmerProfileResponse.model_validate(
            updated_profile,
            from_attributes=True,
        ),
    }