"""
Farm Schemas

This module defines all Pydantic schemas used for Farm APIs.

Responsibilities:
- Validate incoming farm data.
- Serialize farm responses.

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

from app.enums.land_unit import LandUnitEnum
from app.enums.soil_type import SoilTypeEnum


# ============================================================================
# Shared Field Validators (reusable across Create + Update)
# ============================================================================

def _validate_farm_name(value: str) -> str:
    value = value.strip()
    if len(value) < 2:
        raise ValueError("Farm name must be at least 2 characters.")
    if len(value) > 100:
        raise ValueError("Farm name cannot exceed 100 characters.")
    if not re.fullmatch(r"[A-Za-z0-9 .&'-]+", value):
        raise ValueError(
            "Farm name can contain only alphabets, numbers, spaces, dots, hyphens, apostrophes, and '&'."
        )
    return value


def _validate_land_area(value: float) -> float:
    if value <= 0:
        raise ValueError("Land area must be greater than 0.")
    if value > 100000:
        raise ValueError("Land area cannot exceed 100000.")
    return value


def _validate_latitude(value: float) -> float:
    if value < -90 or value > 90:
        raise ValueError("Latitude must be between -90 and 90.")
    return value


def _validate_longitude(value: float) -> float:
    if value < -180 or value > 180:
        raise ValueError("Longitude must be between -180 and 180.")
    return value


# ============================================================================
# Farm Create (all fields required — creating a farm needs full data)
# ============================================================================

class FarmCreate(BaseModel):
    farm_name: str
    land_area: float
    land_unit: Optional[LandUnitEnum] = None
    soil_type: SoilTypeEnum
    latitude: float
    longitude: float

    @field_validator("farm_name")
    @classmethod
    def _name(cls, v):
        return _validate_farm_name(v)

    @field_validator("land_area")
    @classmethod
    def _area(cls, v):
        return _validate_land_area(v)

    @field_validator("land_unit", mode="before")
    @classmethod
    def _unit(cls, v):
        if isinstance(v, str):
            v = v.strip().capitalize()
        return v

    @field_validator("soil_type", mode="before")
    @classmethod
    def _soil(cls, v):
        if isinstance(v, str):
            v = v.strip().capitalize()
        return v

    @field_validator("latitude")
    @classmethod
    def _lat(cls, v):
        return _validate_latitude(v)

    @field_validator("longitude")
    @classmethod
    def _lng(cls, v):
        return _validate_longitude(v)


# ============================================================================
# Farm Update — TRUE PARTIAL UPDATE
#
# Every field is Optional. Only fields explicitly sent by the client are
# validated and applied. This fixes the bug where `exclude_unset=True` in
# farm_service.update_farm() was a no-op because the old schema required
# every field, forcing clients to resend the entire farm on every PUT.
# ============================================================================

class FarmUpdate(BaseModel):
    farm_name: Optional[str] = None
    land_area: Optional[float] = None
    land_unit: Optional[LandUnitEnum] = None
    soil_type: Optional[SoilTypeEnum] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @field_validator("farm_name")
    @classmethod
    def _name(cls, v):
        return _validate_farm_name(v) if v is not None else v

    @field_validator("land_area")
    @classmethod
    def _area(cls, v):
        return _validate_land_area(v) if v is not None else v

    @field_validator("land_unit", mode="before")
    @classmethod
    def _unit(cls, v):
        if isinstance(v, str):
            v = v.strip().capitalize()
        return v

    @field_validator("soil_type", mode="before")
    @classmethod
    def _soil(cls, v):
        if isinstance(v, str):
            v = v.strip().capitalize()
        return v

    @field_validator("latitude")
    @classmethod
    def _lat(cls, v):
        return _validate_latitude(v) if v is not None else v

    @field_validator("longitude")
    @classmethod
    def _lng(cls, v):
        return _validate_longitude(v) if v is not None else v

    @model_validator(mode="after")
    def _at_least_one_field(self):
        if all(
            getattr(self, f) is None
            for f in ("farm_name", "land_area", "land_unit", "soil_type", "latitude", "longitude")
        ):
            raise ValueError("At least one field must be provided to update the farm.")
        return self


# ============================================================================
# Farm Response
# ============================================================================

class FarmResponse(BaseModel):
    id: UUID
    farmer_profile_id: UUID
    farm_name: str
    land_area: float
    land_unit: Optional[LandUnitEnum] = None
    soil_type: SoilTypeEnum
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)