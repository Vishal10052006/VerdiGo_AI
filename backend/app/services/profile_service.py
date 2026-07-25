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
from app.services.storage import get_storage_provider
from app.utils.image_processing import resize_and_compress_profile_image
from app.constants.profile import PROFILE_IMAGE_OUTPUT_EXTENSION

from app.services.dashboard import invalidate_dashboard_cache


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
    Partially update farmer profile.
    Only fields explicitly sent by the client are changed — this now
    works correctly because FarmerProfileUpdate makes every field
    Optional (see schemas/farmer.py fix).
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
        exclude_unset=True,
        exclude_none=True,
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
    invalidate_dashboard_cache(user_id)

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

    Pipeline: validate extension/size -> decode + resize + compress
    (image_processing.py) -> save via storage abstraction (local/R2) ->
    delete old image -> update DB.

    Images are always re-encoded to JPEG at a capped resolution
    (PROFILE_IMAGE_MAX_DIMENSION, see constants/profile.py) regardless
    of upload format/size — fixes the prior gap where a 5MB avatar was
    stored byte-for-byte as uploaded.
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
        file.filename or ""
    )[1].lower()

    if extension not in settings.ALLOWED_IMAGE_EXTENSIONS:
        raise ValueError(
            "Invalid image format."
        )

    # ------------------------------------------------------------
    # Validate File Size (pre-compression cap — reject absurdly
    # large uploads before we spend CPU decoding them)
    # ------------------------------------------------------------
    contents = file.file.read()
    file.file.seek(0)

    if not contents:
        raise ValueError(
            "Uploaded file is empty."
        )

    if len(contents) > settings.MAX_IMAGE_SIZE:
        raise ValueError(
            "Image exceeds maximum size of 5 MB."
        )

    # ------------------------------------------------------------
    # Resize + Compress
    #
    # This is also a second, stronger validation layer than the
    # extension check: Pillow will raise (caught and re-raised as
    # ValueError) if `contents` isn't actually a decodable image,
    # e.g. someone renaming a .exe to .jpg to get past the extension
    # filter. The extension check alone never caught that.
    # ------------------------------------------------------------
    processed_bytes = resize_and_compress_profile_image(contents)

    # ------------------------------------------------------------
    # Delete Previous Image (best-effort, via storage provider)
    # ------------------------------------------------------------
    storage = get_storage_provider()

    if user.profile_image_url:
        storage.delete(user.profile_image_url)

    # ------------------------------------------------------------
    # Generate Unique Filename + Save via Storage Provider
    #
    # Always .jpg now, regardless of upload extension — output is
    # normalized to PROFILE_IMAGE_OUTPUT_FORMAT (JPEG) by the resize
    # step above, so the stored filename must match the actual bytes.
    # ------------------------------------------------------------
    filename = f"{uuid.uuid4()}{PROFILE_IMAGE_OUTPUT_EXTENSION}"

    image_url = storage.save(
        file_bytes=processed_bytes,
        filename=filename,
        folder="profile",
    )

    # ------------------------------------------------------------
    # Update Database
    # ------------------------------------------------------------
    profile_repository.update_profile_image(
        db=db,
        user=user,
        profile_image_url=image_url,
    )
    invalidate_dashboard_cache(user_id)

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