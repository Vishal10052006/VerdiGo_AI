"""
Weather Provider Log Repository

Handles all database operations related to weather
provider request logs.

Responsibilities:
- Store provider requests
- Retrieve request history
- Count requests
- Delete old logs

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from datetime import datetime, timezone, timedelta

from sqlalchemy.orm import Session

from app.models.weather_provider_request_log import (
    WeatherProviderRequestLog,
)


# ============================================================================
# Weather Provider Log Repository
# ============================================================================

class WeatherProviderLogRepository:
    """
    Repository for WeatherProviderRequestLog database operations.
    """

    def __init__(self, db: Session):
        """
        Initialize repository.

        Args:
            db: SQLAlchemy database session.
        """

        self.db = db

    # ------------------------------------------------------------------------
    # Create Log
    # ------------------------------------------------------------------------

    def create_log(
        self,
        log: WeatherProviderRequestLog,
    ) -> WeatherProviderRequestLog:
        """
        Store a provider request log.
        """

        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)

        return log

    # ------------------------------------------------------------------------
    # Get Recent Logs
    # ------------------------------------------------------------------------

    def get_recent_logs(
        self,
        limit: int = 100,
    ) -> list[WeatherProviderRequestLog]:
        """
        Retrieve recent provider logs.
        """

        return (
            self.db.query(WeatherProviderRequestLog)
            .order_by(
                WeatherProviderRequestLog.created_at.desc()
            )
            .limit(limit)
            .all()
        )

    # ------------------------------------------------------------------------
    # Count Requests
    # ------------------------------------------------------------------------

    def count_requests(
        self,
    ) -> int:
        """
        Count total provider requests.
        """

        return (
            self.db.query(WeatherProviderRequestLog)
            .count()
        )

    # ------------------------------------------------------------------------
    # Delete Old Logs
    # ------------------------------------------------------------------------

    def delete_old_logs(
        self,
        retention_days: int = 30,
    ) -> int:
        """
        Delete logs older than the retention period.

        Returns:
            Number of deleted rows.
        """

        cutoff = (
            datetime.now(timezone.utc)
            - timedelta(days=retention_days)
        )

        deleted = (
            self.db.query(WeatherProviderRequestLog)
            .filter(
                WeatherProviderRequestLog.created_at < cutoff,
            )
            .delete()
        )

        self.db.commit()

        return deleted