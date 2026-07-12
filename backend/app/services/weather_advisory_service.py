"""
Weather Advisory Service

Provides business logic for weather advisories.

Responsibilities:
- Retrieve advisory history
- Future advisory operations
- Mark advisory as read
- Advisory filtering
- Advisory pagination

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.weather_advisory_repository import (
    WeatherAdvisoryRepository,
)
from app.enums.advisory_severity import AdvisorySeverityEnum
from app.enums.advisory_type import AdvisoryTypeEnum


# ============================================================================
# Weather Advisory Service
# ============================================================================

class WeatherAdvisoryService:
    """
    Business logic for weather advisories.
    """

    def __init__(
        self,
        db: Session,
    ):
        """
        Initialize advisory service.
        """

        self.repository = WeatherAdvisoryRepository(db)

    # ------------------------------------------------------------------------
    # Advisory History
    # ------------------------------------------------------------------------

    def get_advisory_history(
        self,
        farm_id: UUID,
        skip: int = 0,
        limit: int = 20,
        severity: AdvisorySeverityEnum | None = None,
        advisory_type: AdvisoryTypeEnum | None = None,
        sort_order: str = "desc",
    ):
        """
        Retrieve advisory history for a farm.
        """

        return self.repository.get_farm_advisories(
            farm_id=farm_id,
            skip=skip,
            limit=limit,
            severity=severity,
            advisory_type=advisory_type,
            sort_order=sort_order,
        )