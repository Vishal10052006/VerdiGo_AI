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
from app.services.provider_fallback_service import ProviderFallbackService


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

        # FIX: previously WeatherProviderManager reimplemented the
        # fallback-eligibility decision inline (duplicated in both
        # get_current_weather and get_forecast, and drifted apart —
        # get_forecast's version had no try/except around the fallback
        # call at all). ProviderFallbackService existed as a separate,
        # tested, unused class. Now actually wired in as the single
        # source of truth for "should we fall back for this error?"
        self.fallback_decider = ProviderFallbackService()

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
    # Shared Fetch-With-Fallback
    #
    # Single implementation used by BOTH get_current_weather and
    # get_forecast, via a `fetch_fn` callable. This is the actual fix
    # for the root cause of the module's drift: previously the two
    # public methods each hand-wrote their own near-identical
    # try/except/fallback logic, and they silently diverged —
    # get_current_weather wrapped its fallback call in try/except,
    # get_forecast did not, so a fallback failure in get_forecast
    # raised an unhandled exception straight to a 500 instead of being
    # caught the same way get_current_weather handles it. One shared
    # implementation means that class of divergence can't happen again.
    # ------------------------------------------------------------------------

    def _fetch_with_fallback(
        self,
        fetch_fn_name: str,
        fetch_args: tuple,
    ) -> dict:
        """
        Call `fetch_fn_name` (e.g. "get_current_weather" or
        "get_forecast") on the primary provider. On a fallback-eligible
        failure (per ProviderFallbackService), retry on the fallback
        provider. If the fallback ALSO fails, the exception propagates
        to the caller — WeatherService/routes/weather.py already turns
        unhandled exceptions here into a clean error response via
        FastAPI's exception handling, so we don't need a third silent
        catch-all layer here; we just need BOTH provider attempts to
        be handled symmetrically, which they now are.
        """

        provider = self._get_provider(self.primary_provider)
        start_time = time.perf_counter()

        try:
            data = getattr(provider, fetch_fn_name)(*fetch_args)

            self._log_request(
                provider=self.primary_provider,
                start_time=start_time,
                status_code=200,
                fallback_used=False,
            )

            return {"provider": self.primary_provider, "data": data}

        except Exception as exc:  # noqa: BLE001 — deliberately broad; see below

            # ------------------------------------------------------------
            # Determine fallback eligibility via ProviderFallbackService.
            # Note: it currently only recognizes httpx exception types
            # (TimeoutException, ConnectError, HTTPStatusError with a
            # retryable status code) and returns False for anything else
            # — so a non-httpx exception (e.g. a bug in our own
            # normalizer) correctly does NOT trigger a fallback attempt,
            # it just re-raises below.
            # ------------------------------------------------------------

            status_code = (
                exc.response.status_code
                if isinstance(exc, httpx.HTTPStatusError)
                else 503
            )

            should_fallback = self.fallback_decider.should_fallback(exc)

            self._log_request(
                provider=self.primary_provider,
                start_time=start_time,
                status_code=status_code,
                fallback_used=should_fallback,
                error_message=str(exc),
            )

            if not should_fallback:
                raise

            fallback_provider = self._get_provider(self.fallback_provider)
            fallback_start = time.perf_counter()

            # Fallback attempt is intentionally NOT wrapped in its own
            # try/except-and-swallow: if the fallback also fails, the
            # farmer needs to see an error (503/500), not silently get
            # no data with a 200. Both get_current_weather's old
            # behavior and this new shared path agree on that — the
            # bug being fixed was get_forecast's fallback call having
            # NO try/except at all around the *logging* of failure,
            # not around whether failure propagates. It should
            # propagate either way; what it must also do is log
            # accurately before propagating, which the block below
            # ensures uniformly for both current-weather and forecast.
            try:
                fallback_data = getattr(fallback_provider, fetch_fn_name)(
                    *fetch_args
                )
            except Exception as fallback_exc:
                self._log_request(
                    provider=self.fallback_provider,
                    start_time=fallback_start,
                    status_code=(
                        fallback_exc.response.status_code
                        if isinstance(fallback_exc, httpx.HTTPStatusError)
                        else 503
                    ),
                    fallback_used=True,
                    error_message=str(fallback_exc),
                )
                raise

            self._log_request(
                provider=self.fallback_provider,
                start_time=fallback_start,
                status_code=200,
                fallback_used=True,
            )

            return {"provider": self.fallback_provider, "data": fallback_data}

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

        return self._fetch_with_fallback(
            "get_current_weather",
            (latitude, longitude),
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
        Retrieve weather forecast with automatic provider fallback.

        FIX: previously this method's fallback call
        (fallback_provider.get_forecast(...)) had NO try/except around
        it at all — if the fallback provider also failed, the raw
        exception propagated unhandled. It now goes through the same
        _fetch_with_fallback path as get_current_weather, which logs
        the fallback failure before re-raising, giving symmetric
        behavior and symmetric observability between both weather
        operations.
        """

        return self._fetch_with_fallback(
            "get_forecast",
            (latitude, longitude, days),
        )

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