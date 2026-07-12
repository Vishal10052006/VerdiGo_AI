"""
Weather Schemas

Defines all request and response schemas for the
Weather Intelligence module.

Responsibilities:
- Current Weather Response
- Forecast Response
- Advisory Response
- Provider Status Response
- Refresh Response
- Generic API Response

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from datetime import datetime, date
from typing import Generic, TypeVar

from uuid import UUID
from pydantic import ConfigDict

from pydantic import BaseModel
from pydantic.generics import GenericModel

from app.enums.advisory_severity import AdvisorySeverityEnum
from app.enums.advisory_type import AdvisoryTypeEnum
from app.enums.weather_provider import WeatherProviderEnum

# ============================================================================
# Generic Response Type
# ============================================================================

T = TypeVar("T")


# ============================================================================
# Generic API Response
# ============================================================================

class ApiResponse(GenericModel, Generic[T]):
    """
    Standard API response wrapper used across
    the Weather Intelligence module.
    """

    success: bool

    message: str

    data: T


# ============================================================================
# Current Weather Schema
# ============================================================================

class CurrentWeatherSchema(BaseModel):
    """
    Unified current weather response.
    """

    temperature: float

    humidity: int

    wind_speed: float

    condition: str

    rainfall: float = 0

    provider: WeatherProviderEnum

    fetched_at: datetime


# ============================================================================
# Forecast Day Schema
# ============================================================================

class ForecastDaySchema(BaseModel):
    """
    Weather forecast for a single day.
    """

    date: date

    min_temperature: float

    max_temperature: float

    rainfall: float = 0

    humidity: int

    wind_speed: float

    condition: str


# ============================================================================
# Forecast Response Schema
# ============================================================================

class ForecastResponseSchema(BaseModel):
    """
    Multi-day weather forecast.
    """

    provider: WeatherProviderEnum

    generated_at: datetime

    forecast: list[ForecastDaySchema]


# ============================================================================
# Advisory Schema
# ============================================================================

class AdvisorySchema(BaseModel):
    """
    Single farming advisory.
    """

    type: AdvisoryTypeEnum

    severity: AdvisorySeverityEnum

    title: str

    message: str


# ============================================================================
# Advisory Response Schema
# ============================================================================

class AdvisoryResponseSchema(BaseModel):
    """
    Weather advisory response.
    """

    generated_at: datetime

    advisories: list[AdvisorySchema]

# ============================================================================
# Advisory History Item Schema
# ============================================================================

class AdvisoryHistoryItemSchema(BaseModel):
    """
    Single advisory history record.
    """

    id: UUID

    type: AdvisoryTypeEnum

    severity: AdvisorySeverityEnum

    title: str

    message: str

    is_read: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# ============================================================================
# Advisory History Response Schema
# ============================================================================

class AdvisoryHistoryResponseSchema(BaseModel):
    """
    Advisory history response.
    """

    advisories: list[AdvisoryHistoryItemSchema]

# ============================================================================
# Provider Status Schema
# ============================================================================

class ProviderStatusSchema(BaseModel):
    """
    Active weather provider information.
    """

    primary_provider: WeatherProviderEnum

    fallback_provider: WeatherProviderEnum

    active_provider: WeatherProviderEnum

    fallback_used: bool

    last_updated: datetime


# ============================================================================
# Refresh Weather Request Schema
# ============================================================================

class RefreshWeatherRequestSchema(BaseModel):
    """
    Manual weather refresh request.
    """

    force_refresh: bool = False


# ============================================================================
# Refresh Weather Response Schema
# ============================================================================

class RefreshWeatherResponseSchema(BaseModel):
    """
    Manual refresh response.
    """

    success: bool

    message: str

    weather: CurrentWeatherSchema