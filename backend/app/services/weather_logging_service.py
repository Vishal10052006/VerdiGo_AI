"""
Weather Logging Service

Provides business logic for weather provider request logging.

Responsibilities:
- Log provider requests
- Retrieve provider logs
- Count provider requests
- Cleanup old logs

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
from app.enums.weather_provider import WeatherProviderEnum

from app.repositories.weather_provider_log_repository import (
    WeatherProviderLogRepository,
)


# ============================================================================
# Weather Logging Service
# ============================================================================

class WeatherLoggingService:
    """
    Business logic for provider request logging.
    """

    def __init__(
        self,
        db: Session,
    ):
        """
        Initialize logging service.
        """

        self.repository = WeatherProviderLogRepository(db)

    # ------------------------------------------------------------------------
    # Save Log
    # ------------------------------------------------------------------------

    def save_log(
        self,
        log: WeatherProviderRequestLog,
    ) -> WeatherProviderRequestLog:
        """
        Store provider request log.
        """

        return self.repository.create_log(log)

    # ------------------------------------------------------------------------
    # Recent Logs
    # ------------------------------------------------------------------------

    def get_recent_logs(
        self,
        limit: int = 100,
    ) -> list[WeatherProviderRequestLog]:
        """
        Retrieve recent provider logs.
        """

        return self.repository.get_recent_logs(limit)

    # ------------------------------------------------------------------------
    # Latest Request
    # ------------------------------------------------------------------------

    def get_latest_request(
        self,
    ) -> WeatherProviderRequestLog | None:
        """
        Retrieve latest provider request.
        """

        return self.repository.get_latest_request()

    # ------------------------------------------------------------------------
    # Count Requests
    # ------------------------------------------------------------------------

    def count_requests(
        self,
    ) -> int:
        """
        Count total provider requests.
        """

        return self.repository.count_requests()

    # ------------------------------------------------------------------------
    # Count Failures
    # ------------------------------------------------------------------------

    def count_failures(
        self,
        provider_name: WeatherProviderEnum,
    ) -> int:
        """
        Count failed provider requests.
        """

        return self.repository.count_failures(
            provider_name,
        )

    # ------------------------------------------------------------------------
    # Cleanup Logs
    # ------------------------------------------------------------------------

    def cleanup_logs(
        self,
        retention_days: int = 30,
    ) -> int:
        """
        Delete old provider logs.
        """

        return self.repository.delete_old_logs(
            retention_days,
        )