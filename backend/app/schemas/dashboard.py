"""
Dashboard Schemas

This module defines all Pydantic schemas used by Dashboard APIs.

Responsibilities:
- Validate dashboard responses.
- Serialize dashboard data.

Module:
Phase 1 → Module 4 → Dashboard

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from app.enums.land_unit import LandUnitEnum
from app.enums.soil_type import SoilTypeEnum
from app.schemas.weather import CurrentWeatherSchema


# ============================================================================
# Farmer Information Schema
# ============================================================================

class FarmerInfoSchema(BaseModel):
    """
    Farmer information displayed on the dashboard.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    full_name: str
    profile_image_url: str | None = None
    mobile: str
    village: str
    district: str
    state: str


# ============================================================================
# Farm Information Schema
# ============================================================================

class FarmInfoSchema(BaseModel):
    """
    Farm information displayed on the dashboard.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    farm_name: str
    land_area: Decimal
    land_unit: LandUnitEnum | None = None
    soil_type: SoilTypeEnum


# ============================================================================
# Primary Farm Schema
# ============================================================================

class PrimaryFarmSchema(BaseModel):
    """
    Primary farm displayed on the dashboard.
    """

    id: UUID

    farm_name: str

    village: str

    district: str

    state: str

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================================
# Dashboard Statistics Schema
# ============================================================================

class DashboardStatisticsSchema(BaseModel):
    """
    Dashboard statistics.
    """

    model_config = ConfigDict(from_attributes=True)

    profile_completed: bool
    total_farms: int
    registered_days: int
    completion_percentage: int


# ============================================================================
# Farmer Overview Response
# ============================================================================

class FarmerOverviewResponse(BaseModel):
    """
    Farmer overview response.
    """

    model_config = ConfigDict(from_attributes=True)

    farmer: FarmerInfoSchema
    farms: list[FarmInfoSchema]


# ============================================================================
# Dashboard Data Schema
# ============================================================================

class DashboardDataSchema(BaseModel):
    """
    Complete dashboard response payload.
    """

    model_config = ConfigDict(from_attributes=True)

    farmer: FarmerInfoSchema

    primary_farm: PrimaryFarmSchema | None = None

    farms: list[FarmInfoSchema]

    statistics: DashboardStatisticsSchema

    # ============================================================================
    # Future Modules (Placeholders)
    # ============================================================================

    weather: CurrentWeatherSchema | None = None

    recommendations: list[Any] = Field(default_factory=list)

    notifications: list[Any] = Field(default_factory=list)

    crop_recommendations: list[Any] = Field(default_factory=list)

    disease_alerts: list[Any] = Field(default_factory=list)

    recent_activities: list[Any] = Field(default_factory=list)

    ai_assistant: dict[str, Any] | None = None