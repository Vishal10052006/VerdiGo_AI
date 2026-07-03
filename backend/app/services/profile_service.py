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

import os
import uuid

from fastapi import UploadFile

from app.config.settings import settings

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
    file: UploadFile,
) -> str:
    """
    Upload and update the user's profile image.
    """

    # ------------------------------------------------------------
    # Validate User
    # ------------------------------------------------------------
    user = profile_repository.get_user(
        db=db,
        user_id=user_id,
    )

    if user is None:
        raise ValueError(
            "User not found."
        )

    # ------------------------------------------------------------
    # Validate File Extension
    # ------------------------------------------------------------
    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if extension not in settings.ALLOWED_IMAGE_EXTENSIONS:
        raise ValueError(
            "Invalid image format."
        )

    # ------------------------------------------------------------
    # Validate File Size
    # ------------------------------------------------------------
    contents = file.file.read()
    file.file.seek(0)

    if len(contents) > settings.MAX_IMAGE_SIZE:
        raise ValueError(
            "Image exceeds maximum size of 5 MB."
        )

    # ------------------------------------------------------------
    # Generate Unique Filename
    # ------------------------------------------------------------
    filename = f"{uuid.uuid4()}{extension}"

    file_path = os.path.join(
        settings.PROFILE_UPLOAD_DIR,
        filename,
    )

    # ------------------------------------------------------------
    # Delete Previous Image
    # ------------------------------------------------------------
    if user.profile_image_url:

        old_file = user.profile_image_url.replace(
            "/uploads/profile/",
            "",
        )

        old_path = os.path.join(
            settings.PROFILE_UPLOAD_DIR,
            old_file,
        )

        if os.path.exists(old_path):
            os.remove(old_path)

    # ------------------------------------------------------------
    # Save Image
    # ------------------------------------------------------------
    with open(file_path, "wb") as image:

        image.write(contents)

    # ------------------------------------------------------------
    # Public URL
    # ------------------------------------------------------------
    image_url = f"/uploads/profile/{filename}"

    # ------------------------------------------------------------
    # Update Database
    # ------------------------------------------------------------
    profile_repository.update_profile_image(
        db=db,
        user=user,
        profile_image_url=image_url,
    )

    return image_url


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