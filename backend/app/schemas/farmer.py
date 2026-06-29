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
import re

from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
)

from app.enums.gender import GenderEnum
from app.schemas.common import SuccessResponse


# ============================================================================
# Farmer Profile Base
# ============================================================================

class FarmerProfileBase(BaseModel):
    """
    Base schema containing shared farmer profile fields
    and validation logic.
    """

    full_name: str
    age: int
    gender: GenderEnum
    state: str
    district: str
    village: str

    # ------------------------------------------------------------------------
    # Name Validation
    # ------------------------------------------------------------------------

    @field_validator("full_name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        """
        Validate farmer full name.
        """

        value = value.strip()

        if len(value) < 3:
            raise ValueError(
                "Name must be at least 3 characters."
            )

        if len(value) > 100:
            raise ValueError(
                "Name cannot exceed 100 characters."
            )

        if not re.fullmatch(r"[A-Za-z .'-]+", value):
            raise ValueError(
                "Name can contain only alphabets, spaces, dots, hyphens, and apostrophes."
            )

        return value

    # ------------------------------------------------------------------------
    # Age Validation
    # ------------------------------------------------------------------------

    @field_validator("age")
    @classmethod
    def validate_age(cls, value: int) -> int:
        """
        Validate farmer age.
        """

        if value < 8:
            raise ValueError(
                "Age must be at least 8 years."
            )

        if value > 120:
            raise ValueError(
                "Age cannot exceed 120 years."
            )

        return value

    # ------------------------------------------------------------------------
    # Gender Validation
    # ------------------------------------------------------------------------

    @field_validator("gender", mode="before")
    @classmethod
    def validate_gender(cls, value):
        """
        Normalize gender before enum validation.
        """

        if isinstance(value, str):
            value = value.strip().capitalize()

        return value

    # ------------------------------------------------------------------------
    # State Validation
    # ------------------------------------------------------------------------

    @field_validator("state")
    @classmethod
    def validate_state(cls, value: str) -> str:
        """
        Validate state name.
        """

        value = value.strip()

        if len(value) < 2:
            raise ValueError(
                "State must be at least 2 characters."
            )

        if len(value) > 100:
            raise ValueError(
                "State cannot exceed 100 characters."
            )

        if not re.fullmatch(r"[A-Za-z .&'-]+", value):
            raise ValueError(
                "State can contain only alphabets, spaces, dots, hyphens, apostrophes, and '&'."
            )

        return value

    # ------------------------------------------------------------------------
    # District Validation
    # ------------------------------------------------------------------------

    @field_validator("district")
    @classmethod
    def validate_district(cls, value: str) -> str:
        """
        Validate district name.
        """

        value = value.strip()

        if len(value) < 2:
            raise ValueError(
                "District must be at least 2 characters."
            )

        if len(value) > 100:
            raise ValueError(
                "District cannot exceed 100 characters."
            )

        if not re.fullmatch(r"[A-Za-z .&'-]+", value):
            raise ValueError(
                "District can contain only alphabets, spaces, dots, hyphens, apostrophes, and '&'."
            )

        return value

    # ------------------------------------------------------------------------
    # Village Validation
    # ------------------------------------------------------------------------

    @field_validator("village")
    @classmethod
    def validate_village(cls, value: str) -> str:
        """
        Validate village name.
        """

        value = value.strip()

        if len(value) < 2:
            raise ValueError(
                "Village must be at least 2 characters."
            )

        if len(value) > 100:
            raise ValueError(
                "Village cannot exceed 100 characters."
            )

        if not re.fullmatch(r"[A-Za-z0-9 .&'-]+", value):
            raise ValueError(
                "Village can contain only alphabets, numbers, spaces, dots, hyphens, apostrophes, and '&'."
            )

        return value


# ============================================================================
# Create Farmer Profile Request
# ============================================================================

class FarmerProfileCreate(FarmerProfileBase):
    """
    Request schema for creating a farmer profile.
    """

    pass


# ============================================================================
# Update Farmer Profile Request
# ============================================================================

class FarmerProfileUpdate(FarmerProfileBase):
    """
    Request schema for updating a farmer profile.
    """

    pass


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


# ============================================================================
# Success Response
# ============================================================================

class FarmerProfileSuccessResponse(SuccessResponse):
    """
    Standard success response returned for Farmer Profile APIs.
    """

    data: FarmerProfileResponse