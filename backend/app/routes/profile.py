"""
Profile API Routes

This module exposes APIs for Farmer Profile Management.

Responsibilities:
- Retrieve complete farmer profile
- Update farmer profile
- Upload profile image

Module:
Phase 1 → Module 3 → Farmer Profile

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.services import profile_service

from app.schemas.profile import (
    ProfileDetailsSuccessResponse,
    ProfileImageUploadRequest,
    ProfileImageUploadResponse,
    ProfileImageUploadSuccessResponse,
)

from app.schemas.farmer import (
    FarmerProfileUpdate,
    FarmerProfileSuccessResponse,
)
from fastapi import UploadFile, File


# ============================================================================
# Router
# ============================================================================

router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
)


# ============================================================================
# Get Complete Profile
# ============================================================================

@router.get(
    "/me",
    response_model=ProfileDetailsSuccessResponse,
    status_code=status.HTTP_200_OK,
)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve the authenticated user's complete profile.
    """

    try:

        profile = profile_service.get_profile(
            db=db,
            user_id=current_user.id,
        )

        return ProfileDetailsSuccessResponse(
            success=True,
            message="Profile retrieved successfully.",
            data=profile,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    

# ============================================================================
# Update Farmer Profile
# ============================================================================

@router.put(
    "/me",
    response_model=FarmerProfileSuccessResponse,
    status_code=status.HTTP_200_OK,
)
def update_profile(
    profile_data: FarmerProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update the authenticated user's farmer profile.
    """

    try:

        updated_profile = profile_service.update_profile(
            db=db,
            user_id=current_user.id,
            profile_data=profile_data,
        )

        return FarmerProfileSuccessResponse(
            success=True,
            message="Profile updated successfully.",
            data=updated_profile,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    

# ============================================================================
# Upload Profile Image
# ============================================================================

@router.post(
    "/upload-image",
    response_model=ProfileImageUploadSuccessResponse,
    status_code=status.HTTP_200_OK,
)
def upload_profile_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload or update the authenticated user's profile image.
    """

    try:

        image_url = profile_service.upload_profile_image(
            db=db,
            user_id=current_user.id,
            file=file,
        )

        return ProfileImageUploadSuccessResponse(
            success=True,
            message="Profile image uploaded successfully.",
            data=ProfileImageUploadResponse(
                profile_image_url=image_url,
            ),
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )