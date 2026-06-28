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

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums.land_unit import LandUnitEnum
from app.enums.soil_type import SoilTypeEnum


# ============================================================================
# Create Farm Request
# ============================================================================

class FarmCreate(BaseModel):
    """
    Request schema for creating a farm.
    """

    farm_name: str
    land_area: float
    land_unit: LandUnitEnum
    soil_type: SoilTypeEnum
    latitude: float
    longitude: float


# ============================================================================
# Update Farm Request
# ============================================================================

class FarmUpdate(BaseModel):
    """
    Request schema for updating a farm.
    """

    farm_name: str
    land_area: float
    land_unit: LandUnitEnum
    soil_type: SoilTypeEnum
    latitude: float
    longitude: float


# ============================================================================
# Farm Response
# ============================================================================

class FarmResponse(BaseModel):
    """
    Response schema for Farm.
    """

    id: UUID
    farmer_profile_id: UUID

    farm_name: str
    land_area: float
    land_unit: LandUnitEnum
    soil_type: SoilTypeEnum

    latitude: float
    longitude: float

    model_config = ConfigDict(
        from_attributes=True
    )