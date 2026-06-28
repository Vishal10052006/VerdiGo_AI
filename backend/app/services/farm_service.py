"""
Farm Service

This module contains all business logic related to Farms.

Responsibilities:
- Create farm
- Prevent duplicate farms
- Validate farmer profile exists

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
from app.models.farm import Farm

from app.schemas.farm import (
    FarmCreate,
    FarmUpdate,
    FarmResponse,
)

from app.repositories import (
    farmer_repository,
    farm_repository,
)

from app.core.exceptions import (
    BadRequestException,
    NotFoundException,
)


# ============================================================================
# Create Farm
# ============================================================================

def create_farm(
    db: Session,
    current_user: User,
    request: FarmCreate,
) -> dict:
    """
    Create a farm for the authenticated farmer.
    """

    # ------------------------------------------------------------------------
    # Get Farmer Profile
    # ------------------------------------------------------------------------

    farmer_profile = farmer_repository.get_by_user_id(
        db=db,
        user_id=current_user.id,
    )

    if farmer_profile is None:
        raise NotFoundException(
            message="Farmer profile not found."
        )

    # ------------------------------------------------------------------------
    # Prevent Duplicate Farm
    # ------------------------------------------------------------------------

    existing_farm = farm_repository.get_by_farmer_profile_id(
        db=db,
        farmer_profile_id=farmer_profile.id,
    )

    if existing_farm:
        raise BadRequestException(
            message="Farm already exists."
        )

    # ------------------------------------------------------------------------
    # Create Farm Model
    # ------------------------------------------------------------------------

    farm = Farm(
        farmer_profile_id=farmer_profile.id,
        farm_name=request.farm_name,
        land_area=request.land_area,
        land_unit=request.land_unit,
        soil_type=request.soil_type,
        latitude=request.latitude,
        longitude=request.longitude,
    )

    # ------------------------------------------------------------------------
    # Save Farm
    # ------------------------------------------------------------------------

    farm = farm_repository.create(
        db=db,
        farm=farm,
    )

    # ------------------------------------------------------------------------
    # Return Response
    # ------------------------------------------------------------------------

    return {
        "success": True,
        "message": "Farm created successfully.",
        "data": FarmResponse.model_validate(
            farm,
            from_attributes=True,
        ),
    }


# ============================================================================
# Update Farm
# ============================================================================

def update_farm(
    db: Session,
    current_user: User,
    request: FarmUpdate,
) -> dict:
    """
    Update the authenticated farmer's farm.
    """

    # ------------------------------------------------------------------------
    # Get Farmer Profile
    # ------------------------------------------------------------------------

    farmer_profile = farmer_repository.get_by_user_id(
        db=db,
        user_id=current_user.id,
    )

    if farmer_profile is None:
        raise NotFoundException(
            message="Farmer profile not found."
        )

    # ------------------------------------------------------------------------
    # Get Farm
    # ------------------------------------------------------------------------

    farm = farm_repository.get_by_farmer_profile_id(
        db=db,
        farmer_profile_id=farmer_profile.id,
    )

    if farm is None:
        raise NotFoundException(
            message="Farm not found."
        )

    # ------------------------------------------------------------------------
    # Update Farm
    # ------------------------------------------------------------------------

    updated_farm = farm_repository.update(
        db=db,
        farm=farm,
        data=request.model_dump(exclude_unset=True),
    )

    # ------------------------------------------------------------------------
    # Return Response
    # ------------------------------------------------------------------------

    return {
        "success": True,
        "message": "Farm updated successfully.",
        "data": FarmResponse.model_validate(
            updated_farm,
            from_attributes=True,
        ),
    }


# ============================================================================
# Get Farm
# ============================================================================

def get_farm(
    db: Session,
    current_user: User,
) -> FarmResponse:
    """
    Retrieve the authenticated farmer's farm.
    """

    # ------------------------------------------------------------------------
    # Get Farmer Profile
    # ------------------------------------------------------------------------

    farmer_profile = farmer_repository.get_by_user_id(
        db=db,
        user_id=current_user.id,
    )

    if farmer_profile is None:
        raise NotFoundException(
            message="Farmer profile not found."
        )

    # ------------------------------------------------------------------------
    # Get Farm
    # ------------------------------------------------------------------------

    farm = farm_repository.get_by_farmer_profile_id(
        db=db,
        farmer_profile_id=farmer_profile.id,
    )

    if farm is None:
        raise NotFoundException(
            message="Farm not found."
        )

    # ------------------------------------------------------------------------
    # Return Response
    # ------------------------------------------------------------------------

    return FarmResponse.model_validate(
        farm,
        from_attributes=True,
    )