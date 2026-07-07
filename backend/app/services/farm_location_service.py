"""
Farm Location Service

Provides farm location information for weather services.

Responsibilities:
- Validate farm existence
- Validate farm status
- Retrieve GPS coordinates
- Hide repository implementation

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories import farm_repository


# ============================================================================
# Farm Location Service
# ============================================================================

class FarmLocationService:
    """
    Business logic for farm location retrieval.
    """

    def __init__(self, db: Session):
        """
        Initialize service.

        Args:
            db: SQLAlchemy database session.
        """

        self.db = db

    # ------------------------------------------------------------------------
    # Get Farm
    # ------------------------------------------------------------------------

    def get_farm(
        self,
        farm_id: UUID,
    ):
        """
        Retrieve a farm by ID.

        Raises:
            ValueError: If farm does not exist.
        """

        farm = farm_repository.get_by_id(
            db=self.db,
            farm_id=farm_id,
        )

        if farm is None:
            raise ValueError(
                "Farm not found."
            )

        return farm

    # ------------------------------------------------------------------------
    # Get Coordinates
    # ------------------------------------------------------------------------

    def get_coordinates(
        self,
        farm_id: UUID,
    ) -> tuple[float, float]:
        """
        Retrieve farm GPS coordinates.
        """

        farm = self.get_farm(farm_id)

        return (
            farm.latitude,
            farm.longitude,
        )

    # ------------------------------------------------------------------------
    # Get Latitude
    # ------------------------------------------------------------------------

    def get_latitude(
        self,
        farm_id: UUID,
    ) -> float:
        """
        Retrieve farm latitude.
        """

        farm = self.get_farm(farm_id)

        return farm.latitude

    # ------------------------------------------------------------------------
    # Get Longitude
    # ------------------------------------------------------------------------

    def get_longitude(
        self,
        farm_id: UUID,
    ) -> float:
        """
        Retrieve farm longitude.
        """

        farm = self.get_farm(farm_id)

        return farm.longitude