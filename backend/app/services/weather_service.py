"""
Weather Service

Acts as the single entry point for all weather-related
operations in VerdiGO.

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from uuid import UUID
from sqlalchemy.orm import Session

from app.constants.weather import (
    WEATHER_API,
    OPEN_METEO,
)
from app.enums.weather_type import WeatherTypeEnum

from app.services.weather_provider_manager import WeatherProviderManager
from app.services.weather_normalizer import WeatherNormalizer
from app.services.weather_cache_service import WeatherCacheService


# ============================================================================
# Weather Service
# ============================================================================

class WeatherService:
    """
    Central service for all weather operations.
    """

    def __init__(self, db: Session):
        self.provider_manager = WeatherProviderManager(db)
        self.cache_service = WeatherCacheService(db)

    # ------------------------------------------------------------------------
    # Current Weather
    # ------------------------------------------------------------------------

    def get_current_weather(
        self,
        farm_id: UUID,
        latitude: float,
        longitude: float,
    ) -> dict:
        """
        Retrieve normalized current weather.

        FIX: caching now happens for BOTH providers (WeatherAPI and
        Open-Meteo), not just WeatherAPI. Previously only the
        WeatherAPI branch called cache_service.save_weather(...); the
        Open-Meteo branch just returned normalized data without ever
        caching it — meaning every current-weather request served by
        the Open-Meteo fallback bypassed the cache entirely, hitting
        the external API on every single call regardless of
        WEATHER_CACHE_MINUTES. This was the *inverse* of get_forecast's
        bug (which only cached Open-Meteo, not WeatherAPI) — the two
        methods had inconsistent, seemingly arbitrary caching logic
        with no shared rationale. Both methods now cache both
        providers identically.
        """

        cache = self.cache_service.get_valid_cache(
            farm_id=farm_id,
            weather_type=WeatherTypeEnum.CURRENT,
        )

        if cache:
            return cache.weather_data

        response = self.provider_manager.get_current_weather(
            latitude,
            longitude,
        )

        provider = response["provider"]
        raw_data = response["data"]

        if provider == WEATHER_API:
            normalized_weather = WeatherNormalizer.normalize_weatherapi(
                raw_data,
            )
        elif provider == OPEN_METEO:
            normalized_weather = WeatherNormalizer.normalize_openmeteo(
                raw_data,
            )
        else:
            raise ValueError(
                f"Unsupported weather provider: {provider}"
            )

        self.cache_service.save_weather(
            farm_id=farm_id,
            provider=provider,
            weather_type=WeatherTypeEnum.CURRENT,
            latitude=latitude,
            longitude=longitude,
            weather_data=normalized_weather,
        )

        return normalized_weather

    # ------------------------------------------------------------------------
    # Forecast Weather
    # ------------------------------------------------------------------------

    def get_forecast(
        self,
        farm_id: UUID,
        latitude: float,
        longitude: float,
        days: int = 5,
    ) -> dict:
        """
        Retrieve normalized weather forecast.

        FIX: same caching-symmetry fix as get_current_weather above —
        previously only the Open-Meteo branch cached; WeatherAPI
        forecast responses were returned raw, uncached, on every call.
        """

        cache = self.cache_service.get_valid_cache(
            farm_id=farm_id,
            weather_type=WeatherTypeEnum.FORECAST,
        )

        if cache:
            return cache.weather_data

        response = self.provider_manager.get_forecast(
            latitude,
            longitude,
            days,
        )

        provider = response["provider"]
        raw_data = response["data"]

        if provider == WEATHER_API:
            normalized_weather = WeatherNormalizer.normalize_weatherapi_forecast(
                raw_data,
            )
        elif provider == OPEN_METEO:
            normalized_weather = WeatherNormalizer.normalize_openmeteo_forecast(
                raw_data,
            )
        else:
            raise ValueError(
                f"Unsupported weather provider: {provider}"
            )

        self.cache_service.save_weather(
            farm_id=farm_id,
            provider=provider,
            weather_type=WeatherTypeEnum.FORECAST,
            latitude=latitude,
            longitude=longitude,
            weather_data=normalized_weather,
        )

        return normalized_weather

    # ------------------------------------------------------------------------
    # Refresh Current Weather
    # ------------------------------------------------------------------------

    def refresh_current_weather(
        self,
        farm_id: UUID,
        latitude: float,
        longitude: float,
    ) -> dict:
        """
        Force refresh current weather by clearing cache.
        """

        self.cache_service.invalidate_cache(
            farm_id=farm_id,
            weather_type=WeatherTypeEnum.CURRENT,
        )

        return self.get_current_weather(
            farm_id=farm_id,
            latitude=latitude,
            longitude=longitude,
        )