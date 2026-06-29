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
)

from app.enums.land_unit import LandUnitEnum
from app.enums.soil_type import SoilTypeEnum


# ============================================================================
# Farm Base
# ============================================================================

class FarmBase(BaseModel):
    """
    Base schema containing shared farm fields
    and validation logic.
    """

    farm_name: str
    land_area: float
    land_unit: Optional[LandUnitEnum] = None
    soil_type: SoilTypeEnum
    latitude: float
    longitude: float

    # ------------------------------------------------------------------------
    # Farm Name Validation
    # ------------------------------------------------------------------------

    @field_validator("farm_name")
    @classmethod
    def validate_farm_name(cls, value: str) -> str:
        """
        Validate farm name.
        """

        value = value.strip()

        if len(value) < 2:
            raise ValueError(
                "Farm name must be at least 2 characters."
            )

        if len(value) > 100:
            raise ValueError(
                "Farm name cannot exceed 100 characters."
            )
        
        if not re.fullmatch(r"[A-Za-z0-9 .&'-]+", value):
            raise ValueError(
                "Farm name can contain only alphabets, numbers, spaces, dots, hyphens, apostrophes, and '&'."
            )

        return value


    # ------------------------------------------------------------------------
    # Land Area Validation
    # ------------------------------------------------------------------------

    @field_validator("land_area")
    @classmethod
    def validate_land_area(cls, value: float) -> float:
        """
        Validate farm land area.
        """

        if value <= 0:
            raise ValueError(
                "Land area must be greater than 0."
            )

        if value > 100000:
            raise ValueError(
                "Land area cannot exceed 100000."
            )

        return value

    # ------------------------------------------------------------------------
    # Land Unit Validation
    # ------------------------------------------------------------------------

    @field_validator("land_unit", mode="before")
    @classmethod
    def validate_land_unit(cls, value):
        """
        Normalize land unit before enum validation.
        Accepts Acre, acre, ACRE, etc.
        """

        if value is None:
            return value

        if isinstance(value, str):
            value = value.strip().capitalize()

        return value

    # ------------------------------------------------------------------------
    # Soil Type Validation
    # ------------------------------------------------------------------------

    @field_validator("soil_type", mode="before")
    @classmethod
    def validate_soil_type(cls, value):
        """
        Normalize soil type before enum validation.
        Accepts Clay, clay, CLAY, etc.
        """

        if isinstance(value, str):
            value = value.strip().capitalize()

        return value

    # ------------------------------------------------------------------------
    # Latitude Validation
    # ------------------------------------------------------------------------

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, value: float) -> float:
        """
        Validate farm latitude.
        """

        if value < -90:
            raise ValueError(
                "Latitude must be greater than or equal to -90."
            )

        if value > 90:
            raise ValueError(
                "Latitude must be less than or equal to 90."
            )

        return value

    # ------------------------------------------------------------------------
    # Longitude Validation
    # ------------------------------------------------------------------------

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, value: float) -> float:
        """
        Validate farm longitude.
        """

        if value < -180:
            raise ValueError(
                "Longitude must be greater than or equal to -180."
            )

        if value > 180:
            raise ValueError(
                "Longitude must be less than or equal to 180."
            )

        return value


# ============================================================================
# Create Farm Request
# ============================================================================

class FarmCreate(FarmBase):
    """
    Request schema for creating a farm.
    """

    pass


# ============================================================================
# Update Farm Request
# ============================================================================

class FarmUpdate(FarmBase):
    """
    Request schema for updating a farm.
    """

    pass


# ============================================================================
# Farm Response
# ============================================================================

class FarmResponse(BaseModel):
    """
    Response schema returned after creating or fetching
    farm information.
    """

    id: UUID
    farmer_profile_id: UUID

    farm_name: str
    land_area: float
    land_unit: Optional[LandUnitEnum] = None
    soil_type: SoilTypeEnum

    latitude: float
    longitude: float

    model_config = ConfigDict(
        from_attributes=True
    )