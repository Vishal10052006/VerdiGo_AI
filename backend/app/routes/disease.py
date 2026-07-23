"""
Disease Detection Routes

Module: Phase 1 → Module 8 → Disease Detection
Author: VerdiGO Backend Team
"""

from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.common import SuccessResponse
from app.schemas.disease import (
    DiseaseDetectionResponseSchema,
    DiseaseHistoryResponseSchema,
)
from app.services.disease_detection_service import DiseaseDetectionService
from app.utils.response import success_response


router = APIRouter(prefix="/v1/disease", tags=["Disease Detection"])


# ============================================================================
# Detect Disease
# ============================================================================
@router.post(
    "/detect/{farm_id}",
    response_model=SuccessResponse[DiseaseDetectionResponseSchema],
    summary="Detect Crop Disease",
)
def detect_disease(
    farm_id: UUID,
    file: UploadFile = File(...),
    crop_type: str | None = Form(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload a crop/leaf image and get an AI Vision diagnosis:
    disease name, severity, confidence, treatment & prevention tips.
    """

    service = DiseaseDetectionService(db)

    detection = service.detect(
        farm_id=farm_id,
        user_id=current_user.id,
        file=file,
        crop_type=crop_type,
    )

    return success_response(
        schema=DiseaseDetectionResponseSchema,
        data=DiseaseDetectionResponseSchema.model_validate(detection),
        message="Disease analysis completed successfully.",
    )


# ============================================================================
# Detection History
# ============================================================================
@router.get(
    "/history/{farm_id}",
    response_model=SuccessResponse[DiseaseHistoryResponseSchema],
    summary="Disease Detection History",
)
def get_disease_history(
    farm_id: UUID,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = DiseaseDetectionService(db)

    detections = service.get_history(
        farm_id=farm_id,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
    )

    return success_response(
        schema=DiseaseHistoryResponseSchema,
        data={
            "farm_id": farm_id,
            "detections": [
                DiseaseDetectionResponseSchema.model_validate(d) for d in detections
            ],
        },
        message="Disease detection history retrieved successfully.",
    )


# ============================================================================
# Detection Details
# ============================================================================
@router.get(
    "/details/{detection_id}",
    response_model=SuccessResponse[DiseaseDetectionResponseSchema],
    summary="Detection Details",
)
def get_detection_details(
    detection_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = DiseaseDetectionService(db)

    detection = service.get_detection(
        detection_id=detection_id,
        user_id=current_user.id,
    )

    return success_response(
        schema=DiseaseDetectionResponseSchema,
        data=DiseaseDetectionResponseSchema.model_validate(detection),
        message="Detection details retrieved successfully.",
    )