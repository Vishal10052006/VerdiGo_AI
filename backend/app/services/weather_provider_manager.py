"""
Weather Provider Manager

Coordinates all weather providers and automatically switches
between them when failures occur.

Responsibilities:
- Select provider
- Automatic fallback
- Retry requests
- Request logging
- Transparent provider switching

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

import time

import httpx

from sqlalchemy.orm import Session

from app.config.settings import settings

from app.constants.weather import (
    WEATHER_API,
    OPEN_METEO,
    RETRYABLE_STATUS_CODES,
)

from app.enums.weather_provider import WeatherProviderEnum

from app.models.weather_provider_request_log import (
    WeatherProviderRequestLog,
)

from app.services.openmeteo_client import OpenMeteoClient
from app.services.weather_logging_service import (
    WeatherLoggingService,
)
from app.services.weatherapi_client import WeatherAPIClient


# ============================================================================
# Weather Provider Manager
# ============================================================================

class WeatherProviderManager:
    """
    Coordinates all weather providers and automatically
    switches between them when failures occur.
    """

    def __init__(
        self,
        db: Session,
    ):
        """
        Initialize provider manager.
        """

        self.weatherapi = WeatherAPIClient()

        self.openmeteo = OpenMeteoClient()

        self.logging_service = WeatherLoggingService(db)

        self.primary_provider = (
            settings.PRIMARY_WEATHER_PROVIDER
        )

        self.fallback_provider = (
            settings.FALLBACK_WEATHER_PROVIDER
        )

    # ------------------------------------------------------------------------
    # Provider Selection
    # ------------------------------------------------------------------------

    def _get_provider(
        self,
        provider_name: WeatherProviderEnum | str,
    ):
        """
        Return configured weather provider.
        """

        providers = {

            WEATHER_API: self.weatherapi,

            OPEN_METEO: self.openmeteo,

        }

        try:

            return providers[provider_name]

        except KeyError as exc:

            raise ValueError(
                f"Unsupported weather provider: {provider_name}"
            ) from exc

    # ------------------------------------------------------------------------
    # Provider Request Logging
    # ------------------------------------------------------------------------

    def _log_request(
        self,
        provider: str,
        start_time: float,
        status_code: int,
        fallback_used: bool,
        error_message: str | None = None,
    ) -> None:
        """
        Save provider request log.
        """

        response_time = int(

            (time.perf_counter() - start_time) * 1000

        )

        self.logging_service.save_log(

            WeatherProviderRequestLog(

                provider_name=WeatherProviderEnum(
                    provider,
                ),

                response_time_ms=response_time,

                status_code=status_code,

                fallback_used=fallback_used,

                error_message=error_message,

            )

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
        Retrieve current weather with automatic provider fallback.
        """

        provider = self._get_provider(
            self.primary_provider,
        )

        start_time = time.perf_counter()

        try:

            data = provider.get_current_weather(
                latitude,
                longitude,
            )

            # ------------------------------------------------------------
            # Log Successful Request
            # ------------------------------------------------------------

            self._log_request(
                provider=self.primary_provider,
                start_time=start_time,
                status_code=200,
                fallback_used=False,
            )

            return {

                "provider": self.primary_provider,

                "data": data,

            }

        # ------------------------------------------------------------
        # HTTP Errors
        # ------------------------------------------------------------

        except httpx.HTTPStatusError as exc:

            status_code = exc.response.status_code

            self._log_request(
                provider=self.primary_provider,
                start_time=start_time,
                status_code=status_code,
                fallback_used=True,
                error_message=str(exc),
            )

            # Retry only for retryable errors

            if status_code in RETRYABLE_STATUS_CODES:

                fallback_provider = self._get_provider(
                    self.fallback_provider,
                )

                fallback_start = time.perf_counter()

                try:
                    fallback_data = fallback_provider.get_current_weather(
                        latitude,
                        longitude,
                    )
                except Exception:
                    # Log fallback failure
                    raise

                self._log_request(
                    provider=self.fallback_provider,
                    start_time=fallback_start,
                    status_code=200,
                    fallback_used=True,
                )

                return {

                    "provider": self.fallback_provider,

                    "data": fallback_data,

                }

            raise

        # ------------------------------------------------------------
        # Timeout / Connection Errors
        # ------------------------------------------------------------

        except (
            httpx.TimeoutException,
            httpx.ConnectError,
        ):

            self._log_request(
                provider=self.primary_provider,
                start_time=start_time,
                status_code=503,
                fallback_used=True,
                error_message="Connection Timeout",
            )

            fallback_provider = self._get_provider(
                self.fallback_provider,
            )

            fallback_start = time.perf_counter()

            try:
                fallback_data = fallback_provider.get_current_weather(
                    latitude,
                    longitude,
                )
            except Exception:
                # Log fallback failure
                raise

            self._log_request(
                provider=self.fallback_provider,
                start_time=fallback_start,
                status_code=200,
                fallback_used=True,
            )

            return {

                "provider": self.fallback_provider,

                "data": fallback_data,

            }
        
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
        Retrieve weather forecast with automatic provider fallback.
        """

        provider = self._get_provider(
            self.primary_provider,
        )

        start_time = time.perf_counter()

        try:

            data = provider.get_forecast(
                latitude,
                longitude,
                days,
            )

            # ------------------------------------------------------------
            # Log Successful Request
            # ------------------------------------------------------------

            self._log_request(
                provider=self.primary_provider,
                start_time=start_time,
                status_code=200,
                fallback_used=False,
            )

            return {

                "provider": self.primary_provider,

                "data": data,

            }

        # ------------------------------------------------------------
        # HTTP Errors
        # ------------------------------------------------------------

        except httpx.HTTPStatusError as exc:

            status_code = exc.response.status_code

            self._log_request(
                provider=self.primary_provider,
                start_time=start_time,
                status_code=status_code,
                fallback_used=True,
                error_message=str(exc),
            )

            # Retry only for retryable errors

            if status_code in RETRYABLE_STATUS_CODES:

                fallback_provider = self._get_provider(
                    self.fallback_provider,
                )

                fallback_start = time.perf_counter()

                fallback_data = fallback_provider.get_forecast(
                    latitude,
                    longitude,
                    days,
                )

                self._log_request(
                    provider=self.fallback_provider,
                    start_time=fallback_start,
                    status_code=200,
                    fallback_used=True,
                )

                return {

                    "provider": self.fallback_provider,

                    "data": fallback_data,

                }

            raise

        # ------------------------------------------------------------
        # Timeout / Connection Errors
        # ------------------------------------------------------------

        except (
            httpx.TimeoutException,
            httpx.ConnectError,
        ):

            self._log_request(
                provider=self.primary_provider,
                start_time=start_time,
                status_code=503,
                fallback_used=True,
                error_message="Connection Timeout",
            )

            fallback_provider = self._get_provider(
                self.fallback_provider,
            )

            fallback_start = time.perf_counter()

            fallback_data = fallback_provider.get_forecast(
                latitude,
                longitude,
                days,
            )

            self._log_request(
                provider=self.fallback_provider,
                start_time=fallback_start,
                status_code=200,
                fallback_used=True,
            )

            return {

                "provider": self.fallback_provider,

                "data": fallback_data,

            }
        
    # ------------------------------------------------------------------------
    # Health Check
    # ------------------------------------------------------------------------

    def health_check(self) -> bool:
        """
        Verify whether the primary weather provider
        is properly configured.
        """

        return bool(
            settings.WEATHERAPI_API_KEY
        )