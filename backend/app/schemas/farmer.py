"""
Farmer Schemas

This module defines all Pydantic schemas used for Farmer Profile APIs.

Responsibilities:
- Validate incoming farmer profile data (full on create, partial on update).
- Serialize farmer profile responses.
- Provide request/response models for FastAPI.

Module:
Phase 1 → Module 2 → Farmer Registration

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from typing import Optional
from uuid import UUID
import re

from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
    model_validator,
)

from app.enums.gender import GenderEnum
from app.schemas.common import SuccessResponse


# ============================================================================
# Shared Field-Level Validators
#
# Extracted as free functions (not classmethods) so both FarmerProfileCreate
# (fields required) and FarmerProfileUpdate (fields Optional) can reuse the
# exact same validation rules without duplicating regex/length logic.
# Each Update validator skips validation when the value is None — i.e. the
# client didn't send that field at all.
# ============================================================================

def _validate_name(value: str) -> str:
    value = value.strip()

    if len(value) < 3:
        raise ValueError("Name must be at least 3 characters.")

    if len(value) > 100:
        raise ValueError("Name cannot exceed 100 characters.")

    if not re.fullmatch(r"[A-Za-z .'-]+", value):
        raise ValueError(
            "Name can contain only alphabets, spaces, dots, hyphens, and apostrophes."
        )

    return value


def _validate_age(value: int) -> int:
    if value < 8:
        raise ValueError("Age must be at least 8 years.")

    if value > 120:
        raise ValueError("Age cannot exceed 120 years.")

    return value


def _validate_state(value: str) -> str:
    value = value.strip()

    if len(value) < 2:
        raise ValueError("State must be at least 2 characters.")

    if len(value) > 100:
        raise ValueError("State cannot exceed 100 characters.")

    if not re.fullmatch(r"[A-Za-z .&'-]+", value):
        raise ValueError(
            "State can contain only alphabets, spaces, dots, hyphens, apostrophes, and '&'."
        )

    return value


def _validate_district(value: str) -> str:
    value = value.strip()

    if len(value) < 2:
        raise ValueError("District must be at least 2 characters.")

    if len(value) > 100:
        raise ValueError("District cannot exceed 100 characters.")

    if not re.fullmatch(r"[A-Za-z .&'-]+", value):
        raise ValueError(
            "District can contain only alphabets, spaces, dots, hyphens, apostrophes, and '&'."
        )

    return value


def _validate_village(value: str) -> str:
    value = value.strip()

    if len(value) < 2:
        raise ValueError("Village must be at least 2 characters.")

    if len(value) > 100:
        raise ValueError("Village cannot exceed 100 characters.")

    if not re.fullmatch(r"[A-Za-z0-9 .&'-]+", value):
        raise ValueError(
            "Village can contain only alphabets, numbers, spaces, dots, hyphens, apostrophes, and '&'."
        )

    return value


def _normalize_gender(value):
    if isinstance(value, str):
        value = value.strip().capitalize()
    return value


# ============================================================================
# Create Farmer Profile Request — ALL FIELDS REQUIRED
#
# Registration must supply the complete profile; there is no "partial
# create." Kept as an independent model (not inherited from a shared Base)
# so tightening/loosening Update rules later can never accidentally
# loosen Create rules too — the historical bug pattern this whole fix
# is guarding against.
# ============================================================================

class FarmerProfileCreate(BaseModel):
    full_name: str
    age: int
    gender: GenderEnum
    state: str
    district: str
    village: str

    @field_validator("full_name")
    @classmethod
    def _name(cls, v: str) -> str:
        return _validate_name(v)

    @field_validator("age")
    @classmethod
    def _age(cls, v: int) -> int:
        return _validate_age(v)

    @field_validator("gender", mode="before")
    @classmethod
    def _gender(cls, v):
        return _normalize_gender(v)

    @field_validator("state")
    @classmethod
    def _state(cls, v: str) -> str:
        return _validate_state(v)

    @field_validator("district")
    @classmethod
    def _district(cls, v: str) -> str:
        return _validate_district(v)

    @field_validator("village")
    @classmethod
    def _village(cls, v: str) -> str:
        return _validate_village(v)


# ============================================================================
# Update Farmer Profile Request — TRUE PARTIAL UPDATE
#
# Every field is Optional[...] = None. This is the actual fix: previously
# FarmerProfileUpdate inherited from FarmerProfileBase where every field
# was required, so `profile_data.model_dump(exclude_unset=True)` in
# farmer_service.update_farmer_profile() never actually excluded anything
# meaningful — clients were forced to resend the entire profile on every
# PUT even though the endpoint's intent (and `exclude_unset` usage) implied
# partial updates were supported.
#
# A `model_validator` rejects a request where the client sent an empty
# body — that's a 422 ("nothing to update"), not a silent no-op 200.
# ============================================================================

class FarmerProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[GenderEnum] = None
    state: Optional[str] = None
    district: Optional[str] = None
    village: Optional[str] = None

    @field_validator("full_name")
    @classmethod
    def _name(cls, v: Optional[str]) -> Optional[str]:
        return _validate_name(v) if v is not None else v

    @field_validator("age")
    @classmethod
    def _age(cls, v: Optional[int]) -> Optional[int]:
        return _validate_age(v) if v is not None else v

    @field_validator("gender", mode="before")
    @classmethod
    def _gender(cls, v):
        return _normalize_gender(v) if v is not None else v

    @field_validator("state")
    @classmethod
    def _state(cls, v: Optional[str]) -> Optional[str]:
        return _validate_state(v) if v is not None else v

    @field_validator("district")
    @classmethod
    def _district(cls, v: Optional[str]) -> Optional[str]:
        return _validate_district(v) if v is not None else v

    @field_validator("village")
    @classmethod
    def _village(cls, v: Optional[str]) -> Optional[str]:
        return _validate_village(v) if v is not None else v

    @model_validator(mode="after")
    def _at_least_one_field(self):
        fields = ("full_name", "age", "gender", "state", "district", "village")
        if all(getattr(self, f) is None for f in fields):
            raise ValueError(
                "At least one field must be provided to update the profile."
            )
        return self


# ============================================================================
# Farmer Profile Response
# ============================================================================

class FarmerProfileResponse(BaseModel):
    """
    Response schema returned after creating, updating, or fetching
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