"""
Profile Repository

This module contains all database operations related to
Farmer Profile Management.

Responsibilities:
- Retrieve complete farmer profile
- Update farmer profile
- Update profile image
- Calculate profile completion

Module:
Phase 1 → Module 3 → Farmer Profile

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from dataclasses import fields
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.farmer_profile import FarmerProfile
from app.models.farm import Farm


# ============================================================================
# Get Complete Profile
# ============================================================================

def get_complete_profile(
    db: Session,
    user_id: UUID,
) -> dict | None:
    """
    Retrieve the complete farmer profile including:
    - User
    - Farmer Profile
    - All Farms
    """

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        return None

    farmer_profile = (
        db.query(FarmerProfile)
        .filter(FarmerProfile.user_id == user_id)
        .first()
    )

    farms = []

    if farmer_profile:
        farms = (
            db.query(Farm)
            .filter(Farm.farmer_profile_id == farmer_profile.id)
            .all()
        )

    return {
        "user": user,
        "farmer_profile": farmer_profile,
        "farms": farms,
    }


# ============================================================================
# Update Farmer Profile
# ============================================================================

def update_profile(
    db: Session,
    farmer_profile: FarmerProfile,
    data: dict,
) -> FarmerProfile:
    """
    Update farmer profile details.
    """

    for key, value in data.items():
        setattr(farmer_profile, key, value)

    db.commit()
    db.refresh(farmer_profile)

    return farmer_profile


# ============================================================================
# Update Profile Image
# ============================================================================

def update_profile_image(
    db: Session,
    user: User,
    profile_image_url: str,
) -> User:
    """
    Update the user's profile image.
    """

    user.profile_image_url = profile_image_url

    db.commit()
    db.refresh(user)

    return user


# ============================================================================
# Get User
# ============================================================================

def get_user(
    db: Session,
    user_id: UUID,
) -> User | None:
    """
    Retrieve user by ID.
    """

    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


# ============================================================================
# Get Farmer Profile
# ============================================================================

def get_farmer_profile(
    db: Session,
    user_id: UUID,
) -> FarmerProfile | None:
    """
    Retrieve farmer profile by user ID.
    """

    return (
        db.query(FarmerProfile)
        .filter(FarmerProfile.user_id == user_id)
        .first()
    )


# ============================================================================
# Get Farms
# ============================================================================

def get_farms(
    db: Session,
    farmer_profile_id: UUID,
) -> list[Farm]:
    """
    Retrieve all farms belonging to a farmer.
    """

    return (
        db.query(Farm)
        .filter(Farm.farmer_profile_id == farmer_profile_id)
        .all()
    )


# ============================================================================
# Calculate Profile Completion
# ============================================================================

def get_profile_completion(
    user: User,
    farmer_profile: FarmerProfile | None,
    farms: list[Farm],
) -> int:
    """
    Calculate farmer profile completion percentage.
    """

    fields = [
        bool(user.profile_image_url),
        bool(farmer_profile),
        bool(farms),
        bool(user.email),
        bool(
            farmer_profile
            and farmer_profile.state
            and farmer_profile.district
            and farmer_profile.village
        ),
    ]

    completed = sum(fields)
    total_fields = len(fields)

    return int((completed / total_fields) * 100)