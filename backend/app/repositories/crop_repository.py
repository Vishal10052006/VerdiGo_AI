"""
Crop Repository

Database operations for crops and crop recommendations.

Module:
Phase 1 → Module 6 → Crop Recommendation

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from app.models.crop import Crop
from app.models.crop_recommendation import (
    CropRecommendation,
    CropRecommendationItem,
)


# ============================================================================
# Crops
# ============================================================================

def get_active_crops(db: Session) -> list[Crop]:
    """
    Retrieve all active crops for scoring.
    """

    return (
        db.query(Crop)
        .filter(Crop.is_active.is_(True))
        .all()
    )


def get_by_id(db: Session, crop_id: UUID) -> Crop | None:
    """
    Retrieve a single crop by ID.
    """

    return (
        db.query(Crop)
        .filter(Crop.id == crop_id)
        .first()
    )


# ============================================================================
# Recommendations
# ============================================================================

def save_recommendation(
    db: Session,
    recommendation: CropRecommendation,
) -> CropRecommendation:
    """
    Persist a recommendation run along with its items
    (cascades via the relationship's `items` list).
    """

    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)

    return recommendation


def get_recommendation_by_id(
    db: Session,
    recommendation_id: UUID,
) -> CropRecommendation | None:
    """
    Retrieve a recommendation run with crop details eagerly loaded,
    avoiding N+1 queries when the API serializes each item's crop.
    """

    return (
        db.query(CropRecommendation)
        .options(
            selectinload(CropRecommendation.items)
            .selectinload(CropRecommendationItem.crop)
        )
        .filter(CropRecommendation.id == recommendation_id)
        .first()
    )


def get_latest_for_farm(
    db: Session,
    farm_id: UUID,
) -> CropRecommendation | None:
    """
    Retrieve the most recent recommendation run for a farm.
    """

    return (
        db.query(CropRecommendation)
        .options(
            selectinload(CropRecommendation.items)
            .selectinload(CropRecommendationItem.crop)
        )
        .filter(CropRecommendation.farm_id == farm_id)
        .order_by(CropRecommendation.generated_at.desc())
        .first()
    )