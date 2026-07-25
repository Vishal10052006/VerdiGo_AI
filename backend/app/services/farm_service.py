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
from app.services.dashboard import invalidate_dashboard_cache


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

    DESIGN DECISION (Phase 1 MVP): one farm per farmer profile.
    FarmerProfile.farms is modeled as a list (SQLAlchemy relationship)
    to support multi-farm in a future phase without a schema migration,
    but business logic here intentionally caps it at 1 for Phase 1 —
    Dashboard, Weather, and Crop Recommendation all currently assume
    a single "primary farm" per farmer. Lifting this cap later requires:
      1. Removing the `existing_farm` check below
      2. Changing GET /farm to return a list, not a single object
      3. Adding a farm_id selector to Dashboard/Weather/Chat context
    Do not remove this check without addressing all three.
    """

    farmer_profile = farmer_repository.get_by_user_id(
        db=db, user_id=current_user.id,
    )

    if farmer_profile is None:
        raise NotFoundException(message="Farmer profile not found.")

    existing_farm = farm_repository.get_by_farmer_profile_id(
        db=db, farmer_profile_id=farmer_profile.id,
    )

    if existing_farm:
        raise BadRequestException(
            message=(
                "Farm already exists. Phase 1 supports one farm per "
                "farmer profile. Use PUT /farm to update it instead."
            )
        )

    farm = Farm(
        farmer_profile_id=farmer_profile.id,
        farm_name=request.farm_name,
        land_area=request.land_area,
        land_unit=request.land_unit,
        soil_type=request.soil_type,
        latitude=request.latitude,
        longitude=request.longitude,
    )

    farm = farm_repository.create(db=db, farm=farm)
    invalidate_dashboard_cache(current_user.id)

    return {
        "success": True,
        "message": "Farm created successfully.",
        "data": FarmResponse.model_validate(farm, from_attributes=True),
    }


def update_farm(
    db: Session,
    current_user: User,
    request: FarmUpdate,
) -> dict:
    """
    Partially update the authenticated farmer's farm.
    Only fields present in `request` (exclude_unset) are changed —
    now actually meaningful since FarmUpdate makes every field Optional.
    """

    farmer_profile = farmer_repository.get_by_user_id(
        db=db, user_id=current_user.id,
    )

    if farmer_profile is None:
        raise NotFoundException(message="Farmer profile not found.")

    farm = farm_repository.get_by_farmer_profile_id(
        db=db, farmer_profile_id=farmer_profile.id,
    )
    invalidate_dashboard_cache(current_user.id)

    if farm is None:
        raise NotFoundException(message="Farm not found.")

    update_data = request.model_dump(exclude_unset=True, exclude_none=True)

    updated_farm = farm_repository.update(db=db, farm=farm, data=update_data)

    return {
        "success": True,
        "message": "Farm updated successfully.",
        "data": FarmResponse.model_validate(updated_farm, from_attributes=True),
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