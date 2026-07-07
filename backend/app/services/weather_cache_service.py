"""
Weather Cache Service

Provides business logic for weather cache management.

Responsibilities:
- Retrieve cached weather
- Validate cache expiration
- Save weather cache
- Update cached weather
- Delete expired cache

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.weather_cache import WeatherCache
from app.repositories.weather_cache_repository import WeatherCacheRepository


# ============================================================================
# Weather Cache Service
# ============================================================================

class WeatherCacheService:
    """
    Business logic for weather cache management.
    """

    def __init__(self, db: Session):
        """
        Initialize service.

        Args:
            db: SQLAlchemy database session.
        """

        self.repository = WeatherCacheRepository(db)

    # ------------------------------------------------------------------------
    # Retrieve Valid Cache
    # ------------------------------------------------------------------------

    def get_valid_cache(
        self,
        farm_id: UUID,
        weather_type: str,
    ) -> WeatherCache | None:
        """
        Return cached weather if it exists and has not expired.
        """

        cache = self.repository.get_valid_cache(
            farm_id=farm_id,
            weather_type=weather_type,
        )

        if cache is None:
            return None

        if cache.expires_at <= datetime.now(timezone.utc):
            return None

        return cache

    # ------------------------------------------------------------------------
    # Save Cache
    # ------------------------------------------------------------------------

    def save_cache(
        self,
        cache: WeatherCache,
    ) -> WeatherCache:
        """
        Store new weather cache.
        """

        return self.repository.create(cache)

    # ------------------------------------------------------------------------
    # Update Cache
    # ------------------------------------------------------------------------

    def update_cache(
        self,
        cache: WeatherCache,
    ) -> WeatherCache:
        """
        Update existing weather cache.
        """

        return self.repository.update(cache)

    # ------------------------------------------------------------------------
    # Delete Cache
    # ------------------------------------------------------------------------

    def delete_cache(
        self,
        cache: WeatherCache,
    ) -> None:
        """
        Remove cached weather.
        """

        self.repository.delete(cache)

    # ------------------------------------------------------------------------
    # Delete Expired Cache
    # ------------------------------------------------------------------------

    def cleanup_expired_cache(self) -> int:
        """
        Delete expired cache records.

        Returns:
            Number of deleted cache entries.
        """

        return self.repository.delete_expired()

    # ------------------------------------------------------------------------
    # Force Refresh
    # ------------------------------------------------------------------------

    def invalidate_cache(
        self,
        farm_id: UUID,
        weather_type: str,
    ) -> None:
        """
        Remove cached weather so that fresh data
        is fetched from the provider.
        """

        cache = self.repository.get_valid_cache(
            farm_id=farm_id,
            weather_type=weather_type,
        )

        if cache:
            self.repository.delete(cache)