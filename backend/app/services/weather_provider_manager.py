"""
Weather Provider Manager

Coordinates all weather providers and automatically switches
between them when failures occur.

Responsibilities:
- Select provider
- Automatic fallback
- Retry requests
- Transparent provider switching

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

import httpx

from app.config.settings import settings

from app.constants.weather import (
    WEATHER_API,
    OPEN_METEO,
    RETRYABLE_STATUS_CODES,
)

from app.services.weatherapi_client import WeatherAPIClient
from app.services.openmeteo_client import OpenMeteoClient


# ============================================================================
# Weather Provider Manager
# ============================================================================

class WeatherProviderManager:
    """
    Coordinates weather providers and handles automatic fallback.
    """

    def __init__(self):
        """
        Initialize all supported weather providers.
        """

        self.weatherapi = WeatherAPIClient()
        self.openmeteo = OpenMeteoClient()

    # ------------------------------------------------------------------------
    # Provider Selection
    # ------------------------------------------------------------------------

    def _get_provider(self, provider_name: str):
        """
        Returns configured weather provider instance.
        """

        if provider_name == WEATHER_API:
            return self.weatherapi

        if provider_name == OPEN_METEO:
            return self.openmeteo

        raise ValueError(
            f"Unsupported weather provider: {provider_name}"
        )

    # ------------------------------------------------------------------------
    # Current Weather
    # ------------------------------------------------------------------------

    def get_current_weather(
        self,
        latitude: float,
        longitude: float,
    ) -> dict:
        """
        Returns current weather with automatic fallback.
        """

        primary = settings.PRIMARY_WEATHER_PROVIDER
        fallback = settings.FALLBACK_WEATHER_PROVIDER

        provider = self._get_provider(primary)

        try:

            return provider.get_current_weather(
                latitude,
                longitude,
            )

        except httpx.HTTPStatusError as exc:

            status_code = exc.response.status_code

            # Retry using fallback provider for recoverable errors
            if status_code in RETRYABLE_STATUS_CODES:

                fallback_provider = self._get_provider(fallback)

                return fallback_provider.get_current_weather(
                    latitude,
                    longitude,
                )

            # Authentication/configuration errors should surface
            raise

        except (
            httpx.TimeoutException,
            httpx.ConnectError,
        ):

            # Retry using fallback provider
            fallback_provider = self._get_provider(fallback)

            return fallback_provider.get_current_weather(
                latitude,
                longitude,
            )

    # ------------------------------------------------------------------------
    # Forecast Weather
    # ------------------------------------------------------------------------

    def get_forecast(
        self,
        latitude: float,
        longitude: float,
        days: int = 3,
    ) -> dict:
        """
        Returns weather forecast with automatic fallback.
        """

        primary = settings.PRIMARY_WEATHER_PROVIDER
        fallback = settings.FALLBACK_WEATHER_PROVIDER

        provider = self._get_provider(primary)

        try:

            return provider.get_forecast(
                latitude,
                longitude,
                days,
            )

        except httpx.HTTPStatusError as exc:

            status_code = exc.response.status_code

            # Retry using fallback provider for recoverable errors
            if status_code in RETRYABLE_STATUS_CODES:

                fallback_provider = self._get_provider(fallback)

                return fallback_provider.get_forecast(
                    latitude,
                    longitude,
                    days,
                )

            raise

        except (
            httpx.TimeoutException,
            httpx.ConnectError,
        ):

            # Retry using fallback provider
            fallback_provider = self._get_provider(fallback)

            return fallback_provider.get_forecast(
                latitude,
                longitude,
                days,
            )

    # ------------------------------------------------------------------------
    # Health Check
    # ------------------------------------------------------------------------

    def health_check(self) -> bool:
        """
        Verify WeatherAPI configuration.
        """

        return bool(settings.WEATHERAPI_API_KEY)