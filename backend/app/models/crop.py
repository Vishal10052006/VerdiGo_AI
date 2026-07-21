"""
Crop Model

Master reference table for crop metadata used by the
Crop Recommendation engine.

Responsibilities:
- Store crop agronomic requirements
- Enable soil / season / region based matching

Module:
Phase 1 → Module 6 → Crop Recommendation

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

import uuid

from sqlalchemy import (
    ARRAY,
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.base import Base
from app.enums.soil_type import SoilTypeEnum
from app.enums.season import SeasonEnum
from app.enums.water_requirement import WaterRequirementEnum


# ============================================================================
# Crop Model
# ============================================================================

class Crop(Base):
    """
    Master crop data used as the recommendation engine's
    knowledge base.
    """

    # ------------------------------------------------------------------------
    # Table Configuration
    # ------------------------------------------------------------------------

    __tablename__ = "crops"

    # ------------------------------------------------------------------------
    # Primary Key
    # ------------------------------------------------------------------------

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # ------------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------------

    name = Column(
        String(100),
        nullable=False,
        unique=True,
    )

    # ------------------------------------------------------------------------
    # Matching Criteria
    # ------------------------------------------------------------------------

    suitable_soil_types = Column(
        ARRAY(Enum(SoilTypeEnum)),
        nullable=False,
    )

    suitable_seasons = Column(
        ARRAY(Enum(SeasonEnum)),
        nullable=False,
    )

    # NULL/empty = suitable across all Indian states
    suitable_states = Column(
        ARRAY(String(100)),
        nullable=True,
    )

    # ------------------------------------------------------------------------
    # Agronomic Attributes
    # ------------------------------------------------------------------------

    water_requirement = Column(
        Enum(WaterRequirementEnum),
        nullable=False,
    )

    ideal_temp_min = Column(
        Float,
        nullable=True,
    )

    ideal_temp_max = Column(
        Float,
        nullable=True,
    )

    growth_duration_days = Column(
        Integer,
        nullable=False,
    )

    expected_yield_per_acre = Column(
        String(50),
        nullable=True,
    )

    # ------------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------------

    is_active = Column(
        Boolean,
        default=True,
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