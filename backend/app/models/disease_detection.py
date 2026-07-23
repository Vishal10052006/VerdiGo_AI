"""
Disease Detection Model

Stores every AI Vision disease-detection run so results are
auditable, reviewable in history, and reusable as future
ML training data (same rationale as CropRecommendation).

Module: Phase 1 → Module 8 → Disease Detection
Author: VerdiGO Backend Team
"""

import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    JSON,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base
from app.enums.disease_severity import DiseaseSeverityEnum


class DiseaseDetection(Base):
    """
    A single AI Vision disease-detection run for a farm.
    """

    __tablename__ = "disease_detections"

    __table_args__ = (
        Index("idx_disease_detection_farm", "farm_id"),
        Index("idx_disease_detection_created", "created_at"),
        Index("idx_disease_detection_severity", "severity"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    farm_id = Column(
        UUID(as_uuid=True),
        ForeignKey("farms.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ------------------------------------------------------------
    # Input
    # ------------------------------------------------------------

    image_url = Column(String(500), nullable=False)

    crop_type = Column(String(100), nullable=True)

    # ------------------------------------------------------------
    # AI Result
    # ------------------------------------------------------------

    is_healthy = Column(Boolean, nullable=False, default=False)

    disease_name = Column(String(150), nullable=True)

    confidence = Column(Float, nullable=False, default=0.0)

    severity = Column(
        Enum(DiseaseSeverityEnum),
        nullable=False,
        default=DiseaseSeverityEnum.NONE,
    )

    # list[str] each — kept as JSON, not a related table: these are
    # generated text, not queryable/reusable entities like Crop is.
    treatment = Column(JSON, nullable=False, default=list)

    prevention_tips = Column(JSON, nullable=False, default=list)

    ai_provider = Column(String(20), nullable=False, default="gemini")

    # ------------------------------------------------------------
    # Audit
    # ------------------------------------------------------------

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # ------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------

    farm = relationship("Farm", back_populates="disease_detections")