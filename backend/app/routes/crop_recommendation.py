"""
Crop Recommendation Routes

Responsibilities:
- Generate crop recommendations for a farm
- Retrieve a previously generated recommendation's details

Module:
Phase 1 → Module 6 → Crop Recommendation

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.common import SuccessResponse
from app.schemas.crop import CropRecommendationResponseSchema
from app.services.crop_recommendation_service import CropRecommendationService
from app.utils.response import success_response


router = APIRouter(
    prefix="/v1/crop-recommendation",
    tags=["Crop Recommendation"],
)


# ============================================================================
# Get Crop Recommendations (generates a fresh run)
# ============================================================================

@router.get(
    "/{farm_id}",
    response_model=SuccessResponse[CropRecommendationResponseSchema],
    summary="Get Crop Recommendations",
)
def get_crop_recommendations(
    farm_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate and return ranked crop recommendations for a farm,
    based on soil type, current season, and location.

    404 if the farm doesn't exist OR doesn't belong to the
    authenticated user — both cases are indistinguishable to
    the caller by design.
    """

    service = CropRecommendationService(db)

    recommendation = service.generate_recommendations(
        farm_id=farm_id,
        user_id=current_user.id,
    )

    return success_response(
        schema=CropRecommendationResponseSchema,
        data=CropRecommendationResponseSchema.model_validate(recommendation),
        message="Crop recommendations generated successfully.",
    )


# ============================================================================
# Recommendation Details API
# ============================================================================

@router.get(
    "/details/{recommendation_id}",
    response_model=SuccessResponse[CropRecommendationResponseSchema],
    summary="Recommendation Details",
)
def get_recommendation_details(
    recommendation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve full details of a previously generated recommendation
    run, scoped to the authenticated user's own farms.
    """

    service = CropRecommendationService(db)

    recommendation = service.get_recommendation_details(
        recommendation_id=recommendation_id,
        user_id=current_user.id,
    )

    return success_response(
        schema=CropRecommendationResponseSchema,
        data=CropRecommendationResponseSchema.model_validate(recommendation),
        message="Recommendation details retrieved successfully.",
    )