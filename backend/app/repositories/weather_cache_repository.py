"""
Weather Cache Repository

Handles all database operations related to weather cache.

Responsibilities:
- Read cached weather
- Create cache
- Update cache
- Delete cache
- Remove expired cache

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
from app.enums.weather_type import WeatherTypeEnum


# ============================================================================
# Weather Cache Repository
# ============================================================================

class WeatherCacheRepository:
    """
    Repository for WeatherCache database operations.
    """

    def __init__(self, db: Session):
        """
        Initialize repository.

        Args:
            db: SQLAlchemy database session.
        """

        self.db = db

    # ------------------------------------------------------------------------
    # Get Active Cache
    # ------------------------------------------------------------------------

    def get_active_cache(
        self,
        farm_id: UUID,
        weather_type: WeatherTypeEnum,
    ) -> WeatherCache | None:
        """
        Return active and non-expired cache.
        """

        return (
            self.db.query(WeatherCache)
            .filter(
                WeatherCache.farm_id == farm_id,
                WeatherCache.weather_type == weather_type,
                WeatherCache.is_active.is_(True),
                WeatherCache.expires_at > datetime.now(timezone.utc),
            )
            .first()
        )

    # ------------------------------------------------------------------------
    # Create Cache
    # ------------------------------------------------------------------------

    def create_cache(
        self,
        cache: WeatherCache,
    ) -> WeatherCache:
        """
        Create weather cache.
        """

        self.db.add(cache)
        self.db.commit()
        self.db.refresh(cache)

        return cache

    # ------------------------------------------------------------------------
    # Update Cache
    # ------------------------------------------------------------------------

    def update_cache(
        self,
        cache: WeatherCache,
    ) -> WeatherCache:
        """
        Update weather cache.
        """

        self.db.commit()
        self.db.refresh(cache)

        return cache

    # ------------------------------------------------------------------------
    # Delete Cache
    # ------------------------------------------------------------------------

    def delete_cache(
        self,
        cache: WeatherCache,
    ) -> None:
        """
        Delete weather cache.
        """

        self.db.delete(cache)
        self.db.commit()

    # ------------------------------------------------------------------------
    # Delete Expired Cache
    # ------------------------------------------------------------------------

    def delete_expired_cache(
        self,
    ) -> int:
        """
        Remove expired cache entries.

        Returns:
            Number of deleted rows.
        """

        deleted = (
            self.db.query(WeatherCache)
            .filter(
                WeatherCache.expires_at <= datetime.utcnow(),
            )
            .delete()
        )

        self.db.commit()

        return deleted