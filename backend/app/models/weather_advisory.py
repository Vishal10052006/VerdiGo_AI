"""
Weather Advisory Model

Stores AI-generated weather advisories for farms.

Responsibilities:
- Store generated advisories
- Track advisory severity
- Track read/unread status
- Maintain advisory history

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text,
    Index,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base
from app.enums.advisory_type import AdvisoryTypeEnum
from app.enums.advisory_severity import AdvisorySeverityEnum


# ============================================================================
# Weather Advisory Model
# ============================================================================

class WeatherAdvisory(Base):
    """
    Stores AI-generated weather advisories.
    """

    # ------------------------------------------------------------------------
    # Table Configuration
    # ------------------------------------------------------------------------

    __tablename__ = "weather_advisories"

    __table_args__ = (

        Index(
            "idx_advisory_farm",
            "farm_id",
        ),

        Index(
            "idx_advisory_created",
            "created_at",
        ),

        Index(
            "idx_advisory_read",
            "is_read",
        ),

        Index(
            "idx_advisory_severity",
            "severity",
        ),

    )

    # ------------------------------------------------------------------------
    # Primary Key
    # ------------------------------------------------------------------------

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # ------------------------------------------------------------------------
    # Farm Reference
    # ------------------------------------------------------------------------

    farm_id = Column(
        UUID(as_uuid=True),
        ForeignKey("farms.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ------------------------------------------------------------------------
    # Advisory Information
    # ------------------------------------------------------------------------

    advisory_type = Column(
        Enum(AdvisoryTypeEnum),
        nullable=False,
    )

    severity = Column(
        Enum(AdvisorySeverityEnum),
        nullable=False,
    )

    title = Column(
        String(150),
        nullable=False,
    )

    message = Column(
        Text,
        nullable=False,
    )

    # ------------------------------------------------------------------------
    # Read Status
    # ------------------------------------------------------------------------

    is_read = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    read_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ------------------------------------------------------------------------
    # Audit Fields
    # ------------------------------------------------------------------------

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # ------------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------------

    farm = relationship(
        "Farm",
        back_populates="weather_advisories",
    )