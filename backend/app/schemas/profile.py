"""
Profile Schemas

This module defines all Pydantic schemas used for Farmer Profile APIs.

Responsibilities:
- Serialize complete farmer profile responses.
- Serialize profile image upload responses.
- Reuse existing User, Farmer, and Farm schemas.

Module:
Phase 1 → Module 3 → Farmer Profile

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from pydantic import (
    BaseModel,
    ConfigDict,
)

from app.schemas.common import SuccessResponse
from app.schemas.user import UserPublicResponse
from app.schemas.farmer import FarmerProfileResponse
from app.schemas.farm import FarmResponse
from typing import List


# ============================================================================
# Profile Details Response
# ============================================================================

class ProfileDetailsResponse(BaseModel):
    """
    Complete profile response returned by
    GET /profile/me.

    Combines user account, farmer profile,
    and farm information into a single response.
    """

    user: UserPublicResponse

    farmer_profile: FarmerProfileResponse

    farms: List[FarmResponse]

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================================
# Profile Details Success Response
# ============================================================================

class ProfileDetailsSuccessResponse(SuccessResponse):
    """
    Standard success response returned for
    Profile Details APIs.
    """

    data: ProfileDetailsResponse


# ============================================================================
# Profile Image Upload Request
# ============================================================================

class ProfileImageUploadRequest(BaseModel):
    """
    Request schema used to upload
    or update the user's profile image.
    """

    profile_image_url: str


# ============================================================================
# Profile Image Upload Response
# ============================================================================

class ProfileImageUploadResponse(BaseModel):
    """
    Response returned after successfully
    uploading a profile image.
    """

    profile_image_url: str

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================================
# Profile Image Upload Success Response
# ============================================================================

class ProfileImageUploadSuccessResponse(SuccessResponse):
    """
    Standard success response returned after
    uploading a profile image.
    """

    data: ProfileImageUploadResponse