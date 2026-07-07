"""
Weather Logging Service

Stores weather provider request logs for monitoring
and observability.

Responsibilities:
- Log provider requests
- Log provider failures
- Track response time
- Track fallback usage

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from sqlalchemy.orm import Session

from app.models.weather_provider_request_log import (
    WeatherProviderRequestLog,
)

from app.enums.weather_provider import (
    WeatherProviderEnum,
)

from app.repositories.weather_provider_log_repository import (
    WeatherProviderLogRepository,
)


# ============================================================================
# Weather Logging Service
# ============================================================================

class WeatherLoggingService:
    """
    Handles weather provider request logging.
    """

    def __init__(
        self,
        db: Session,
    ):
        """
        Initialize repository.
        """

        self.repository = WeatherProviderLogRepository(db)

    # ------------------------------------------------------------------------
    # Log Request
    # ------------------------------------------------------------------------

    def log_request(
        self,
        provider: WeatherProviderEnum,
        status_code: int,
        response_time_ms: int,
        fallback_used: bool = False,
    ) -> WeatherProviderRequestLog:
        """
        Store a weather provider request log.
        """

        log = WeatherProviderRequestLog(
            provider_name=provider,
            status_code=status_code,
            response_time_ms=response_time_ms,
            fallback_used=fallback_used,
        )

        return self.repository.create_log(log)

    # ------------------------------------------------------------------------
    # Log Success
    # ------------------------------------------------------------------------

    def log_success(
        self,
        provider: WeatherProviderEnum,
        response_time_ms: int,
    ) -> WeatherProviderRequestLog:
        """
        Log successful provider request.
        """

        return self.log_request(
            provider=provider,
            status_code=200,
            response_time_ms=response_time_ms,
            fallback_used=False,
        )

    # ------------------------------------------------------------------------
    # Log Failure
    # ------------------------------------------------------------------------

    def log_failure(
        self,
        provider: WeatherProviderEnum,
        status_code: int,
        response_time_ms: int,
        fallback_used: bool = False,
    ) -> WeatherProviderRequestLog:
        """
        Log failed provider request.
        """

        return self.log_request(
            provider=provider,
            status_code=status_code,
            response_time_ms=response_time_ms,
            fallback_used=fallback_used,
        )