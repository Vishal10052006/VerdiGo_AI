"""
Weather Advisory Repository

Handles all database operations related to
weather advisories.

Responsibilities:
- Store advisories
- Retrieve advisories
- Update advisory status
- Delete advisories

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.weather_advisory import WeatherAdvisory
from app.enums.advisory_severity import AdvisorySeverityEnum
from app.enums.advisory_type import AdvisoryTypeEnum


# ============================================================================
# Weather Advisory Repository
# ============================================================================

class WeatherAdvisoryRepository:
    """
    Repository for WeatherAdvisory database operations.
    """

    def __init__(self, db: Session):
        """
        Initialize repository.

        Args:
            db: SQLAlchemy database session.
        """

        self.db = db

    # ------------------------------------------------------------------------
    # Create Advisory
    # ------------------------------------------------------------------------

    def create(
        self,
        advisory: WeatherAdvisory,
    ) -> WeatherAdvisory:
        """
        Store a new weather advisory.
        """

        self.db.add(advisory)
        self.db.commit()
        self.db.refresh(advisory)

        return advisory

    # ------------------------------------------------------------------------
    # Get Advisory By ID
    # ------------------------------------------------------------------------

    def get_by_id(
        self,
        advisory_id: UUID,
    ) -> WeatherAdvisory | None:
        """
        Retrieve advisory by ID.
        """

        return (
            self.db.query(WeatherAdvisory)
            .filter(
                WeatherAdvisory.id == advisory_id
            )
            .first()
        )

    # ------------------------------------------------------------------------
    # Get Advisories By Farm
    # ------------------------------------------------------------------------

    def get_by_farm(
        self,
        farm_id: UUID,
    ) -> list[WeatherAdvisory]:
        """
        Retrieve advisories for a farm.
        """

        return (
            self.db.query(WeatherAdvisory)
            .filter(
                WeatherAdvisory.farm_id == farm_id
            )
            .order_by(
                WeatherAdvisory.created_at.desc()
            )
            .all()
        )

    # ------------------------------------------------------------------------
    # Get Unread Advisories
    # ------------------------------------------------------------------------

    def get_unread(
        self,
        farm_id: UUID,
    ) -> list[WeatherAdvisory]:
        """
        Retrieve unread advisories.
        """

        return (
            self.db.query(WeatherAdvisory)
            .filter(
                WeatherAdvisory.farm_id == farm_id,
                WeatherAdvisory.is_read.is_(False),
            )
            .order_by(
                WeatherAdvisory.created_at.desc()
            )
            .all()
        )

    # ------------------------------------------------------------------------
    # Mark Advisory As Read
    # ------------------------------------------------------------------------

    def mark_as_read(
        self,
        advisory: WeatherAdvisory,
    ) -> WeatherAdvisory:
        """
        Mark advisory as read.
        """

        advisory.is_read = True

        self.db.commit()
        self.db.refresh(advisory)

        return advisory

    # ------------------------------------------------------------------------
    # Delete Advisory
    # ------------------------------------------------------------------------

    def delete(
        self,
        advisory: WeatherAdvisory,
    ) -> None:
        """
        Delete an advisory.
        """

        self.db.delete(advisory)
        self.db.commit()

    # ------------------------------------------------------------------------
    # Latest Advisory
    # ------------------------------------------------------------------------

    def get_latest(
        self,
        farm_id: UUID,
    ) -> WeatherAdvisory | None:
        """
        Retrieve latest advisory for a farm.
        """

        return (
            self.db.query(WeatherAdvisory)
            .filter(
                WeatherAdvisory.farm_id == farm_id
            )
            .order_by(
                WeatherAdvisory.created_at.desc()
            )
            .first()
        )
    
    # ------------------------------------------------------------------------
    # Get Farm Advisories
    # ------------------------------------------------------------------------

    def get_farm_advisories(
        self,
        farm_id: UUID,
        skip: int = 0,
        limit: int = 20,
        severity: AdvisorySeverityEnum | None = None,
        advisory_type: AdvisoryTypeEnum | None = None,
        sort_order: str = "desc",
    ):
        """
        Return advisory history for a farm.
        """

        query = (
            self.db.query(WeatherAdvisory)
            .filter(
                WeatherAdvisory.farm_id == farm_id,
            )
        )

        # ------------------------------------------------------------
        # Filter by Severity
        # ------------------------------------------------------------

        if severity:
            query = query.filter(
                WeatherAdvisory.severity == severity,
            )

        # ------------------------------------------------------------
        # Filter by Advisory Type
        # ------------------------------------------------------------

        if advisory_type:
            query = query.filter(
                WeatherAdvisory.advisory_type == advisory_type,
            )

        # ------------------------------------------------------------
        # Sorting
        # ------------------------------------------------------------

        if sort_order.lower() == "asc":
            query = query.order_by(
                WeatherAdvisory.created_at.asc(),
            )
        else:
            query = query.order_by(
                WeatherAdvisory.created_at.desc(),
            )

        # ------------------------------------------------------------
        # Pagination
        # ------------------------------------------------------------

        return (
            query.offset(skip)
            .limit(limit)
            .all()
        )