"""
Farm Model

This module defines the Farm database model.

Responsibilities:
- Store farm information.
- Link farms to a farmer profile.
- Store land details and GPS coordinates.

Module:
Phase 1 → Module 2 → Farmer Registration

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Numeric,
    String,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base
from app.enums.land_unit import LandUnitEnum
from app.enums.soil_type import SoilTypeEnum


# ============================================================================
# Farm Model
# ============================================================================

class Farm(Base):
    """
    Represents a farm owned by a farmer.

    Relationships:
        FarmerProfile (1) --------> Farm (Many)
    """

    # ------------------------------------------------------------------------
    # Table Configuration
    # ------------------------------------------------------------------------

    __tablename__ = "farms"

    # ------------------------------------------------------------------------
    # Primary Key
    # ------------------------------------------------------------------------

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # ------------------------------------------------------------------------
    # Foreign Key
    # ------------------------------------------------------------------------

    farmer_profile_id = Column(
        UUID(as_uuid=True),
        ForeignKey("farmer_profiles.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ------------------------------------------------------------------------
    # Farm Information
    # ------------------------------------------------------------------------

    farm_name = Column(
        String(100),
        nullable=False,
    )

    land_area = Column(
        Numeric(10, 2),
        nullable=False,
    )

    land_unit = Column(
        Enum(LandUnitEnum),
        nullable=True,
    )

    soil_type = Column(
        Enum(SoilTypeEnum),
        nullable=False,
    )

    # ------------------------------------------------------------------------
    # GPS Location
    # ------------------------------------------------------------------------

    latitude = Column(
        Float,
        nullable=False,
    )

    longitude = Column(
        Float,
        nullable=False,
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

    farmer_profile = relationship(
        "FarmerProfile",
        back_populates="farms",
    )

    # ------------------------------------------------------------------------
    # Weather Relationships
    # ------------------------------------------------------------------------

    weather_cache = relationship(
        "WeatherCache",
        back_populates="farm",
        cascade="all, delete-orphan",
    )

    weather_advisories = relationship(
        "WeatherAdvisory",
        back_populates="farm",
        cascade="all, delete-orphan",
    )

    # Add alongside weather_advisories relationship
    disease_detections = relationship(
        "DiseaseDetection",
        back_populates="farm",
        cascade="all, delete-orphan",
    )