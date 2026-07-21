"""
Crop Recommendation Models

Stores the output of each recommendation engine run so
results are auditable, cacheable, and reusable as future
ML training data.

Module:
Phase 1 → Module 6 → Crop Recommendation

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
    Integer,
    JSON,
    String,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base
from app.enums.season import SeasonEnum


# ============================================================================
# Crop Recommendation Model
# ============================================================================

class CropRecommendation(Base):
    """
    A single recommendation "run" for a farm.
    """

    # ------------------------------------------------------------------------
    # Table Configuration
    # ------------------------------------------------------------------------

    __tablename__ = "crop_recommendations"

    __table_args__ = (

        Index(
            "idx_crop_reco_farm",
            "farm_id",
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
    # Run Metadata
    # ------------------------------------------------------------------------

    season = Column(
        Enum(SeasonEnum),
        nullable=False,
    )

    # Future-proofing: lets us swap in an ML engine later
    # without changing the API contract.
    source = Column(
        String(20),
        default="rule_based",
        nullable=False,
    )

    generated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
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

    # ------------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------------

    farm = relationship(
        "Farm",
    )

    items = relationship(
        "CropRecommendationItem",
        back_populates="recommendation",
        cascade="all, delete-orphan",
        order_by="CropRecommendationItem.rank",
    )


# ============================================================================
# Crop Recommendation Item Model
# ============================================================================

class CropRecommendationItem(Base):
    """
    A single ranked crop suggestion within a recommendation run.
    """

    # ------------------------------------------------------------------------
    # Table Configuration
    # ------------------------------------------------------------------------

    __tablename__ = "crop_recommendation_items"

    __table_args__ = (

        Index(
            "idx_crop_reco_items_reco",
            "recommendation_id",
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
    # Foreign Keys
    # ------------------------------------------------------------------------

    recommendation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("crop_recommendations.id", ondelete="CASCADE"),
        nullable=False,
    )

    crop_id = Column(
        UUID(as_uuid=True),
        ForeignKey("crops.id"),
        nullable=False,
    )

    # ------------------------------------------------------------------------
    # Scoring
    # ------------------------------------------------------------------------

    score = Column(
        Float,
        nullable=False,
    )

    rank = Column(
        Integer,
        nullable=False,
    )

    # {"soil": "...", "season": "...", "location": "..."}
    reasoning = Column(
        JSON,
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

    # ------------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------------

    recommendation = relationship(
        "CropRecommendation",
        back_populates="items",
    )

    crop = relationship(
        "Crop",
    )