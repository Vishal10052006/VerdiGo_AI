"""
Farm Repository

This module contains all database operations related to Farms.

Responsibilities:
- Create farm
- Retrieve farm
- Update farm

Module:
Phase 1 → Module 2 → Farmer Registration

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.farm import Farm
from app.models.farmer_profile import FarmerProfile


# ============================================================================
# Create Farm
# ============================================================================

def create(
    db: Session,
    farm: Farm,
) -> Farm:
    """
    Create a new farm.
    """

    db.add(farm)
    db.commit()
    db.refresh(farm)

    return farm


# ============================================================================
# Get Farm By Farmer Profile ID
# ============================================================================

def get_by_farmer_profile_id(
    db: Session,
    farmer_profile_id: UUID,
) -> Farm | None:
    """
    Retrieve a farm using the farmer profile ID.
    """

    return (
        db.query(Farm)
        .filter(Farm.farmer_profile_id == farmer_profile_id)
        .first()
    )


# ============================================================================
# Get Farm By ID
# ============================================================================

def get_by_id(
    db: Session,
    farm_id: UUID,
) -> Farm | None:
    """
    Retrieve a farm by its ID.
    """

    return (
        db.query(Farm)
        .filter(Farm.id == farm_id)
        .first()
    )


# ============================================================================
# Get Farm By ID, Scoped To Owner
# ============================================================================

def get_by_id_for_user(
    db: Session,
    farm_id: UUID,
    user_id: UUID,
) -> Farm | None:
    """
    Retrieve a farm by ID, but only if it belongs to the given
    user's farmer profile. Returns None (→ 404, not 403) if the
    farm exists but belongs to someone else — this avoids leaking
    farm existence to unauthorized users.
    """

    return (
        db.query(Farm)
        .join(FarmerProfile, Farm.farmer_profile_id == FarmerProfile.id)
        .filter(
            Farm.id == farm_id,
            FarmerProfile.user_id == user_id,
        )
        .first()
    )


# ============================================================================
# Update Farm
# ============================================================================

def update(
    db: Session,
    farm: Farm,
    data: dict,
) -> Farm:
    """
    Update an existing farm.
    """

    for key, value in data.items():
        setattr(farm, key, value)

    db.commit()
    db.refresh(farm)

    return farm


# ============================================================================
# Get All Farms By Farmer Profile ID
# ============================================================================

def get_all_by_farmer_profile_id(
    db: Session,
    farmer_profile_id: UUID,
) -> list[Farm]:
    """
    Retrieve all farms belonging to a farmer profile.
    """

    return (
        db.query(Farm)
        .filter(Farm.farmer_profile_id == farmer_profile_id)
        .all()
    )