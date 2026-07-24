"""
Admin Panel Schemas

Module: Phase 1 → Module 10 → Admin Panel
Author: VerdiGO Backend Team
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.enums.admin import AdminRoleEnum
from app.enums.soil_type import SoilTypeEnum


# ============================================================================
# Auth
# ============================================================================

class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class AdminResponse(BaseModel):
    id: UUID
    email: str
    full_name: str
    role: AdminRoleEnum
    is_active: bool
    last_login_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class AdminLoginResponse(BaseModel):
    success: bool = True
    access_token: str
    admin: AdminResponse


# ============================================================================
# Farmer Management
# ============================================================================

class FarmerListItemSchema(BaseModel):
    user_id: UUID
    farmer_profile_id: UUID | None = None
    full_name: str | None = None
    mobile: str
    state: str | None = None
    district: str | None = None
    total_farms: int
    profile_completed: bool
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FarmerListResponseSchema(BaseModel):
    farmers: list[FarmerListItemSchema]
    total: int
    page: int
    page_size: int


class FarmerDetailFarmSchema(BaseModel):
    id: UUID
    farm_name: str
    land_area: float
    soil_type: SoilTypeEnum
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)


class FarmerDetailSchema(BaseModel):
    user_id: UUID
    mobile: str
    email: str | None = None
    is_active: bool
    created_at: datetime

    full_name: str | None = None
    age: int | None = None
    state: str | None = None
    district: str | None = None
    village: str | None = None
    profile_completed: bool = False

    farms: list[FarmerDetailFarmSchema] = []


class UpdateFarmerStatusRequest(BaseModel):
    is_active: bool


# ============================================================================
# Analytics
# ============================================================================

class AnalyticsOverviewSchema(BaseModel):
    total_farmers: int
    active_farmers: int
    total_farms: int
    profile_completion_rate: float  # %
    new_farmers_last_7_days: int
    new_farmers_last_30_days: int

    total_crop_recommendations: int
    total_disease_detections: int
    total_chat_messages: int

    soil_type_distribution: dict[str, int]
    state_distribution: dict[str, int]


class DailySignupPointSchema(BaseModel):
    date: str  # YYYY-MM-DD
    count: int


class GrowthAnalyticsSchema(BaseModel):
    days: int
    signups: list[DailySignupPointSchema]