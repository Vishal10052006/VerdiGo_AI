"""
Weather Routes

Provides REST APIs for the Weather Intelligence module.

Responsibilities:
- Current Weather
- Forecast
- Weather Advisories
- Provider Status
- Refresh Weather

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from uuid import UUID

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.common import SuccessResponse

from app.schemas.weather import (
    CurrentWeatherSchema,
    ForecastResponseSchema,
    AdvisoryResponseSchema,
    ProviderStatusSchema,
    AdvisoryHistoryResponseSchema,
)
from app.services.weather_advisory_service import (
    WeatherAdvisoryService,
)
from app.enums.advisory_severity import AdvisorySeverityEnum
from app.enums.advisory_type import AdvisoryTypeEnum

from app.services.weather_service import WeatherService
from app.services.farm_location_service import FarmLocationService
from app.services.advisory_engine_service import AdvisoryEngineService

from app.utils.response import success_response

from datetime import datetime, timezone

from app.enums.advisory_severity import AdvisorySeverityEnum
from app.enums.advisory_type import AdvisoryTypeEnum

# ============================================================================
# Router Configuration
# ============================================================================

router = APIRouter(
    prefix="/v1/weather",
    tags=["Weather v1"],
)

# ============================================================================
# Services
# ============================================================================

advisory_service = AdvisoryEngineService()

# ============================================================================
# Get Current Weather
# ============================================================================

@router.get(
    "/current/{farm_id}",
    response_model=SuccessResponse[CurrentWeatherSchema],
    summary="Get Current Weather",
)
def get_current_weather(
    farm_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    """
    Retrieve the current weather for a farm.

    Workflow:
    - Authenticate user
    - Validate farm
    - Retrieve GPS coordinates
    - Fetch normalized weather
    - Return response
    """

    weather_service = WeatherService(db)

    # ------------------------------------------------------------------------
    # Resolve Farm Coordinates
    # ------------------------------------------------------------------------

    latitude, longitude = _get_farm_coordinates(
        db=db,
        farm_id=farm_id,
    )

    # ------------------------------------------------------------------------
    # Retrieve Weather
    # ------------------------------------------------------------------------

    weather = weather_service.get_current_weather(
        farm_id=farm_id,
        latitude=latitude,
        longitude=longitude,
    )

    return success_response(
        schema=CurrentWeatherSchema,
        data=weather,
        message="Current weather fetched successfully.",
    )


# ============================================================================
# Get Weather Forecast
# ============================================================================

@router.get(
    "/forecast/{farm_id}",
    response_model=SuccessResponse[ForecastResponseSchema],
    summary="Get Weather Forecast",
)
def get_weather_forecast(
    farm_id: UUID,
    days: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve the weather forecast for a farm.
    """

    weather_service = WeatherService(db)

    # ------------------------------------------------------------------------
    # Resolve Farm Coordinates
    # ------------------------------------------------------------------------

    latitude, longitude = _get_farm_coordinates(
        db=db,
        farm_id=farm_id,
    )

    # ------------------------------------------------------------------------
    # Retrieve Forecast
    # ------------------------------------------------------------------------

    forecast = weather_service.get_forecast(
        farm_id=farm_id,
        latitude=latitude,
        longitude=longitude,
        days=days,
    )

    # ------------------------------------------------------------------------
    # Return Response
    # ------------------------------------------------------------------------

    return success_response(
        schema=ForecastResponseSchema,
        data=forecast,
        message="Weather forecast retrieved successfully.",
    )


# ============================================================================
# Get Weather Advisories
# ============================================================================

@router.get(
    "/advisory/{farm_id}",
    response_model=SuccessResponse[AdvisoryResponseSchema],
    summary="Get Weather Advisories",
)
def get_weather_advisories(
    farm_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate farming advisories based on the
    current weather conditions.
    """

    # ------------------------------------------------------------------------
    # Resolve Farm Coordinates
    # ------------------------------------------------------------------------


    latitude, longitude = _get_farm_coordinates(
        db=db,
        farm_id=farm_id,
    )

    # ------------------------------------------------------------------------
    # Retrieve Current Weather
    # ------------------------------------------------------------------------

    weather_service = WeatherService(db)
    weather = weather_service.get_current_weather(
        farm_id=farm_id,
        latitude=latitude,
        longitude=longitude,
    )

    # ------------------------------------------------------------------------
    # Generate Advisories
    # ------------------------------------------------------------------------

    advisories = advisory_service.generate_advisories(
        weather=weather,
    )

    # ------------------------------------------------------------------------
    # Build Response
    # ------------------------------------------------------------------------

    response = {
        "generated_at": weather["fetched_at"],
        "advisories": advisories,
    }

    # ------------------------------------------------------------------------
    # Return Response
    # ------------------------------------------------------------------------

    return success_response(
        schema=AdvisoryResponseSchema,
        data=response,
        message="Weather advisories generated successfully.",
    )

# ============================================================================
# Get Advisory History
# ============================================================================

@router.get(
    "/advisories/{farm_id}",
    response_model=SuccessResponse[AdvisoryHistoryResponseSchema],
    summary="Get Advisory History",
)
def get_advisory_history(
    farm_id: UUID,
    skip: int = 0,
    limit: int = 20,
    severity: AdvisorySeverityEnum | None = None,
    advisory_type: AdvisoryTypeEnum | None = None,
    sort_order: str = "desc",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve advisory history for a farm.
    """

    advisory_service = WeatherAdvisoryService(db)

    advisories = advisory_service.get_advisory_history(
        farm_id=farm_id,
        skip=skip,
        limit=limit,
        severity=severity,
        advisory_type=advisory_type,
        sort_order=sort_order,
    )

    return success_response(
        schema=AdvisoryHistoryResponseSchema,
        data={
            "advisories": advisories,
        },
        message="Advisory history retrieved successfully.",
    )

# ============================================================================
# Helper Functions
# ============================================================================

def _get_farm_coordinates(
    db: Session,
    farm_id: UUID,
) -> tuple[float, float]:
    """
    Retrieve farm coordinates.
    """

    location_service = FarmLocationService(db)

    return location_service.get_coordinates(
        farm_id=farm_id,
    )


# ============================================================================
# Weather Provider Status
# ============================================================================

@router.get(
    "/provider-status",
    response_model=SuccessResponse[ProviderStatusSchema],
    summary="Weather Provider Status",
)
def get_provider_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve weather provider status.
    """

    weather_service = WeatherService(db)

    response = {
        "primary_provider": weather_service.provider_manager.primary_provider,
        "fallback_provider": weather_service.provider_manager.fallback_provider,
        "active_provider": weather_service.provider_manager.primary_provider,
        "fallback_used": False,
        "last_updated": datetime.now(timezone.utc),
    }

    return success_response(
        schema=ProviderStatusSchema,
        data=response,
        message="Provider status retrieved successfully.",
    )

# ============================================================================
# Refresh Weather
# ============================================================================

@router.post(
    "/refresh/{farm_id}",
    response_model=SuccessResponse[CurrentWeatherSchema],
    summary="Refresh Weather",
)
def refresh_weather(
    farm_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Force refresh weather by clearing cache and
    fetching fresh data.
    """

    weather_service = WeatherService(db)

    latitude, longitude = _get_farm_coordinates(
        db=db,
        farm_id=farm_id,
    )

    weather = weather_service.refresh_current_weather(
        farm_id=farm_id,
        latitude=latitude,
        longitude=longitude,
    )

    return success_response(
        schema=CurrentWeatherSchema,
        data=weather,
        message="Weather refreshed successfully.",
    )