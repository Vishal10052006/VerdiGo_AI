"""
Profile Service

This module contains all business logic related to
Farmer Profile Management.

Responsibilities:
- Retrieve complete farmer profile
- Update farmer profile
- Upload profile image
- Calculate profile completion

Module:
Phase 1 → Module 3 → Farmer Profile

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories import profile_repository
from app.schemas.farmer import FarmerProfileUpdate


# ============================================================================
# Get Complete Profile
# ============================================================================

def get_profile(
    db: Session,
    user_id: UUID,
) -> dict:
    """
    Retrieve the complete farmer profile.
    """

    profile = profile_repository.get_complete_profile(
        db=db,
        user_id=user_id,
    )

    if profile is None:
        raise ValueError(
            "Farmer profile not found."
        )

    completion = profile_repository.get_profile_completion(
        user=profile["user"],
        farmer_profile=profile["farmer_profile"],
        farms=profile["farms"],
    )

    profile["profile_completion"] = completion

    return profile


# ============================================================================
# Update Farmer Profile
# ============================================================================

def update_profile(
    db: Session,
    user_id: UUID,
    profile_data: FarmerProfileUpdate,
):
    """
    Update farmer profile.
    """

    farmer_profile = profile_repository.get_farmer_profile(
        db=db,
        user_id=user_id,
    )

    if farmer_profile is None:
        raise ValueError(
            "Farmer profile not found."
        )

    data = profile_data.model_dump(
        exclude_unset=True
    )

    if not data:
        raise ValueError(
            "No fields provided for update."
        )

    updated_profile = profile_repository.update_profile(
        db=db,
        farmer_profile=farmer_profile,
        data=data,
    )

    return updated_profile


# ============================================================================
# Upload Profile Image
# ============================================================================

def upload_profile_image(
    db: Session,
    user_id: UUID,
    profile_image_url: str,
):
    """
    Update user's profile image.
    """

    user = profile_repository.get_user(
        db=db,
        user_id=user_id,
    )

    if user is None:
        raise ValueError(
            "User not found."
        )

    profile_image_url = profile_image_url.strip()

    if not profile_image_url:
        raise ValueError(
            "Profile image URL cannot be empty."
        )

    return profile_repository.update_profile_image(
        db=db,
        user=user,
        profile_image_url=profile_image_url,
    )


# ============================================================================
# Calculate Profile Completion
# ============================================================================

def calculate_profile_completion(
    db: Session,
    user_id: UUID,
) -> int:
    """
    Calculate profile completion percentage.
    """

    profile = profile_repository.get_complete_profile(
        db=db,
        user_id=user_id,
    )

    if profile is None:
        raise ValueError(
            "Farmer profile not found."
        )

    completion = profile_repository.get_profile_completion(
        user=profile["user"],
        farmer_profile=profile["farmer_profile"],
        farms=profile["farms"],
    )

    if completion < 0 or completion > 100:
        raise ValueError(
            "Invalid profile completion."
        )

    return completion