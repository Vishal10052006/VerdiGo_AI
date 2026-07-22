"""
Crop Recommendation Schemas

Response contracts for the Crop Recommendation module.

Module:
Phase 1 → Module 6 → Crop Recommendation

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.enums.season import SeasonEnum
from app.enums.water_requirement import WaterRequirementEnum


# ============================================================================
# Reasoning Schema
# ============================================================================

class CropReasoningSchema(BaseModel):
    """
    Human-readable explanation behind a crop's score.
    """

    soil: str
    season: str
    location: str


# ============================================================================
# Crop Summary Schema
# ============================================================================

class CropSummarySchema(BaseModel):
    """
    Minimal crop info shown inside a recommendation item.
    Deliberately excludes internal fields like suitable_soil_types /
    suitable_seasons — the frontend needs display data, not the
    engine's matching criteria.
    """

    id: UUID
    name: str
    water_requirement: WaterRequirementEnum
    growth_duration_days: int
    expected_yield_per_acre: str | None = None

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# Recommendation Item Schema
# ============================================================================

class CropRecommendationItemSchema(BaseModel):
    """
    A single ranked crop suggestion within a recommendation run.
    """

    id: UUID
    rank: int
    score: float
    crop: CropSummarySchema
    reasoning: CropReasoningSchema

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# Recommendation Response Schema
# ============================================================================

class CropRecommendationResponseSchema(BaseModel):
    """
    Full response for GET crop recommendations / recommendation details.
    """

    id: UUID
    farm_id: UUID
    season: SeasonEnum
    source: str
    generated_at: datetime
    items: list[CropRecommendationItemSchema]

    model_config = ConfigDict(from_attributes=True)