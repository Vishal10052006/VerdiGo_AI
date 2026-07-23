"""
Disease Detection Schemas

Module: Phase 1 → Module 8 → Disease Detection
Author: VerdiGO Backend Team
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums.disease_severity import DiseaseSeverityEnum


class DiseaseDetectionResponseSchema(BaseModel):
    id: UUID
    farm_id: UUID

    image_url: str
    crop_type: str | None = None

    is_healthy: bool
    disease_name: str | None = None
    confidence: float
    severity: DiseaseSeverityEnum

    treatment: list[str]
    prevention_tips: list[str]

    ai_provider: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DiseaseHistoryResponseSchema(BaseModel):
    farm_id: UUID
    detections: list[DiseaseDetectionResponseSchema]