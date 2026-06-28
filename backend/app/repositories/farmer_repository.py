"""
Farmer Repository

This module contains all database operations related to Farmer Profiles.

Responsibilities:
- Create farmer profile
- Retrieve farmer profile
- Update farmer profile

Module:
Phase 1 → Module 2 → Farmer Registration

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.farmer_profile import FarmerProfile


# ============================================================================
# Create Farmer Profile
# ============================================================================

def create(
    db: Session,
    farmer_profile: FarmerProfile,
) -> FarmerProfile:
    """
    Create a new farmer profile.
    """

    db.add(farmer_profile)
    db.commit()
    db.refresh(farmer_profile)

    return farmer_profile


# ============================================================================
# Get Farmer Profile By User ID
# ============================================================================

def get_by_user_id(
    db: Session,
    user_id: UUID,
) -> FarmerProfile | None:
    """
    Retrieve a farmer profile using the authenticated user's ID.
    """

    return (
        db.query(FarmerProfile)
        .filter(FarmerProfile.user_id == user_id)
        .first()
    )


# ============================================================================
# Get Farmer Profile By ID
# ============================================================================

def get_by_id(
    db: Session,
    profile_id: UUID,
) -> FarmerProfile | None:
    """
    Retrieve a farmer profile by its ID.
    """

    return (
        db.query(FarmerProfile)
        .filter(FarmerProfile.id == profile_id)
        .first()
    )


# =====================================================
# Update Farmer Profile
#
# Updates an existing farmer profile.
# =====================================================
def update(
    db: Session,
    farmer_profile: FarmerProfile,
    data: dict,
) -> FarmerProfile:

    # Update only the provided fields
    for key, value in data.items():
        setattr(farmer_profile, key, value)

    db.commit()
    db.refresh(farmer_profile)

    return farmer_profile