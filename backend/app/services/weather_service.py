"""
Weather Service

Acts as the single entry point for all weather-related
operations in VerdiGO.

Responsibilities:
- Retrieve current weather
- Retrieve weather forecast
- Coordinate provider manager
- Normalize provider responses

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from app.constants.weather import (
    WEATHER_API,
    OPEN_METEO,
)

from app.services.weather_provider_manager import WeatherProviderManager
from app.services.weather_normalizer import WeatherNormalizer


# ============================================================================
# Weather Service
# ============================================================================

class WeatherService:
    """
    Central service for all weather operations.
    """

    def __init__(self):
        """
        Initialize weather service dependencies.
        """

        self.provider_manager = WeatherProviderManager()

    # ------------------------------------------------------------------------
    # Current Weather
    # ------------------------------------------------------------------------

    def get_current_weather(
        self,
        latitude: float,
        longitude: float,
    ) -> dict:
        """
        Retrieve normalized current weather.
        """

        response = self.provider_manager.get_current_weather(
            latitude,
            longitude,
        )

        provider = response["provider"]
        raw_data = response["data"]

        if provider == WEATHER_API:

            return WeatherNormalizer.normalize_weatherapi(
                raw_data,
            )

        if provider == OPEN_METEO:

            return WeatherNormalizer.normalize_openmeteo(
                raw_data,
            )

        raise ValueError(
            f"Unsupported weather provider: {provider}"
        )

    # ------------------------------------------------------------------------
    # Forecast Weather
    # ------------------------------------------------------------------------

    def get_forecast(
        self,
        latitude: float,
        longitude: float,
        days: int = 5,
    ) -> dict:
        """
        Retrieve normalized weather forecast.
        """

        response = self.provider_manager.get_forecast(
            latitude,
            longitude,
            days,
        )

        provider = response["provider"]
        raw_data = response["data"]

        if provider == WEATHER_API:

            return WeatherNormalizer.normalize_weatherapi(
                raw_data,
            )

        if provider == OPEN_METEO:

            return WeatherNormalizer.normalize_openmeteo(
                raw_data,
            )

        raise ValueError(
            f"Unsupported weather provider: {provider}"
        )