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


# ============================================================================
# Get Dashboard Summary
# ============================================================================

def get_dashboard_summary(
    db: Session,
    user_id: UUID,
) -> DashboardDataSchema | None:
    """
    Retrieve dashboard summary for the authenticated user.
    """

    print("=" * 60)
    print("Dashboard Service User ID:", user_id)

    farmer_profile = get_dashboard_data(db, user_id)

    print("Dashboard Repository Result:", farmer_profile)
    print("=" * 60)

    if farmer_profile is None:
        return None

    # ============================================================================
    # Handle Missing Farm
    # ============================================================================

    farms = []
    primary_farm = None

    if farmer_profile.farms:

        farms = [
            FarmInfoSchema.model_validate(farm)
            for farm in farmer_profile.farms
        ]

        first_farm = farmer_profile.farms[0]

        primary_farm = PrimaryFarmSchema(
            id=first_farm.id,
            farm_name=first_farm.farm_name,
            village=farmer_profile.village,
            district=farmer_profile.district,
            state=farmer_profile.state,
        )

    weather = None

    if primary_farm:

        weather_service = WeatherService(db)

        weather_data = weather_service.get_current_weather(
            farm_id=first_farm.id,
            latitude=first_farm.latitude,
            longitude=first_farm.longitude,
        )

        weather = CurrentWeatherSchema.model_validate(
            weather_data
        )

    registered_days = (
        datetime.now(farmer_profile.created_at.tzinfo)
        - farmer_profile.created_at
    ).days

    if farmer_profile.profile_completed:
        completion_percentage = 100 if farms else 50
    else:
        completion_percentage = 0

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

    return DashboardDataSchema(
        farmer=farmer,
        primary_farm=primary_farm,
        farms=farms,
        statistics=statistics,
        weather=weather,
    )