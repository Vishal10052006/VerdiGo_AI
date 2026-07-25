"""
Dashboard Service

This module contains all business logic related to the Dashboard.

Responsibilities:
- Retrieve dashboard data
- Calculate dashboard statistics
- Build dashboard response

Module:
Phase 1 → Module 4 → Dashboard

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.dashboard import get_dashboard_data
from app.repositories import profile_repository
from app.schemas.dashboard import (
    DashboardDataSchema,
    DashboardStatisticsSchema,
    FarmerInfoSchema,
    FarmInfoSchema,
    PrimaryFarmSchema,
)
from app.services.weather_service import WeatherService
from app.schemas.weather import (
    CurrentWeatherSchema,
)
from app.utils.ttl_cache import dashboard_cache
from app.constants.dashboard import DASHBOARD_CACHE_TTL_SECONDS


# ============================================================================
# Cache Key Helper
# ============================================================================

def _cache_key(user_id: UUID) -> str:
    return f"dashboard:{user_id}"


# ============================================================================
# Invalidate Dashboard Cache
#
# Call this from anywhere that mutates data the dashboard reflects:
# farmer_service.update_farmer_profile, farm_service.create_farm/update_farm,
# profile_service.upload_profile_image. Without this, a farmer who edits
# their profile could see stale data for up to DASHBOARD_CACHE_TTL_SECONDS.
# ============================================================================

def invalidate_dashboard_cache(user_id: UUID) -> None:
    """
    Drop the cached dashboard for a specific user. Safe to call even
    if nothing is cached for them (no-op).
    """

    dashboard_cache.invalidate(_cache_key(user_id))


# ============================================================================
# Get Dashboard Summary
# ============================================================================

def get_dashboard_summary(
    db: Session,
    user_id: UUID,
) -> DashboardDataSchema | None:
    """
    Retrieve dashboard summary for the authenticated user.

    Cached in-process for DASHBOARD_CACHE_TTL_SECONDS to avoid
    re-running the farm/user join and profile-completion calculation
    on every dashboard load/refresh. Weather still respects its own
    independent cache inside WeatherService — this cache wraps the
    *entire assembled response*, so a cache hit here skips weather
    lookup too (which is itself already cached, so this is a second,
    coarser layer on top, not a duplicate of it).
    """

    cache_key = _cache_key(user_id)

    cached = dashboard_cache.get(cache_key)
    if cached is not None:
        return cached

    farmer_profile = get_dashboard_data(db, user_id)

    if farmer_profile is None:
        return None

    # ============================================================================
    # Handle Missing Farm
    # ============================================================================

    farms = []
    primary_farm = None
    primary_farm_model = None

    if farmer_profile.farms:

        farms = [
            FarmInfoSchema.model_validate(farm)
            for farm in farmer_profile.farms
        ]

        primary_farm_model = farmer_profile.farms[0]

        primary_farm = PrimaryFarmSchema(
            id=primary_farm_model.id,
            farm_name=primary_farm_model.farm_name,
            village=farmer_profile.village,
            district=farmer_profile.district,
            state=farmer_profile.state,
        )

    # ============================================================================
    # Weather (best-effort)
    # ============================================================================

    weather = None

    if primary_farm_model is not None:

        weather_service = WeatherService(db)

        weather_data = weather_service.get_current_weather(
            farm_id=primary_farm_model.id,
            latitude=primary_farm_model.latitude,
            longitude=primary_farm_model.longitude,
        )

        weather = CurrentWeatherSchema.model_validate(
            weather_data
        )

    registered_days = (
        datetime.now(farmer_profile.created_at.tzinfo)
        - farmer_profile.created_at
    ).days

    # ============================================================================
    # Profile Completion — single source of truth
    # ============================================================================

    completion_percentage = profile_repository.get_profile_completion(
        user=farmer_profile.user,
        farmer_profile=farmer_profile,
        farms=farmer_profile.farms,
    )

    statistics = DashboardStatisticsSchema(
        profile_completed=farmer_profile.profile_completed,
        total_farms=len(farms),
        registered_days=registered_days,
        completion_percentage=completion_percentage,
    )

    farmer = FarmerInfoSchema(
        id=farmer_profile.id,
        full_name=farmer_profile.full_name,
        profile_image_url=(
            farmer_profile.user.profile_image_url
            if farmer_profile.user
            else None
        ),
        mobile=(
            farmer_profile.user.mobile
            if farmer_profile.user
            else ""
        ),
        village=farmer_profile.village,
        district=farmer_profile.district,
        state=farmer_profile.state,
    )

    result = DashboardDataSchema(
        farmer=farmer,
        primary_farm=primary_farm,
        farms=farms,
        statistics=statistics,
        weather=weather,
    )

    dashboard_cache.set(cache_key, result, DASHBOARD_CACHE_TTL_SECONDS)

    return result