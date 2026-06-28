"""
Farmer Schemas

This module defines all Pydantic schemas used for Farmer Profile APIs.

Responsibilities:
- Validate incoming farmer profile data.
- Serialize farmer profile responses.
- Provide request/response models for FastAPI.

Module:
Phase 1 → Module 2 → Farmer Registration

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums.gender import GenderEnum

from app.schemas.common import SuccessResponse

class FarmerProfileSuccessResponse(SuccessResponse):
    data: FarmerProfileResponse


# ============================================================================
# Create Farmer Profile Request
# ============================================================================

class FarmerProfileCreate(BaseModel):
    """
    Request schema for creating a farmer profile.
    """

    full_name: str
    age: int
    gender: GenderEnum
    state: str
    district: str
    village: str


# ============================================================================
# Update Farmer Profile Request
# ============================================================================

class FarmerProfileUpdate(BaseModel):
    """
    Request schema for updating a farmer profile.
    """

    full_name: str
    age: int
    gender: GenderEnum
    state: str
    district: str
    village: str


# ============================================================================
# Farmer Profile Response
# ============================================================================

class FarmerProfileResponse(BaseModel):
    """
    Response schema returned after creating or fetching
    a farmer profile.
    """

    id: UUID
    user_id: UUID

    full_name: str
    age: int
    gender: GenderEnum

    state: str
    district: str
    village: str

    profile_completed: bool

    model_config = ConfigDict(
        from_attributes=True
    )