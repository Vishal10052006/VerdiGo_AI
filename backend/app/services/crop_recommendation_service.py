"""
Crop Recommendation Service

Core rule-based recommendation engine. Scores every active
crop against a farm's soil type, current season, and state,
then persists and returns the ranked top N.

Responsibilities:
- Soil Analysis Logic
- Season Logic
- Location Logic
- Weighted score aggregation & ranking
- Fallback when nothing clears the threshold
- Persist recommendation run

Module:
Phase 1 → Module 6 → Crop Recommendation

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from uuid import UUID

from sqlalchemy.orm import Session

from app.constants.crop_recommendation import (
    SOIL_WEIGHT,
    SEASON_WEIGHT,
    LOCATION_WEIGHT,
    MAX_RECOMMENDATIONS,
    MIN_SCORE_THRESHOLD,
)
from app.enums.season import SeasonEnum
from app.models.crop import Crop
from app.models.crop_recommendation import (
    CropRecommendation,
    CropRecommendationItem,
)
from app.repositories import crop_repository, farm_repository
from app.services.season_service import SeasonService
from app.core.exceptions import NotFoundException

from app.enums.water_requirement import WaterRequirementEnum


# ============================================================================
# Crop Recommendation Service
# ============================================================================

class CropRecommendationService:
    """
    Rule-based crop recommendation engine.
    """

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------------
    # Soil Analysis Logic
    # ------------------------------------------------------------------------

    def _score_soil(self, crop: Crop, farm_soil_type) -> float:
        """
        Binary match: 100 if the farm's soil type is in the crop's
        suitable list, else 0. Soil compatibility isn't a "partial
        credit" attribute agronomically — a crop either tolerates
        a soil type or it doesn't.
        """

        if farm_soil_type in crop.suitable_soil_types:
            return 100.0

        return 0.0

    # ------------------------------------------------------------------------
    # Season Logic
    # ------------------------------------------------------------------------

    def _score_season(
        self,
        crop: Crop,
        current_season: SeasonEnum,
    ) -> float:
        """
        Binary match: 100 if the crop is sown in the current
        season, else 0.
        """

        if current_season in crop.suitable_seasons:
            return 100.0

        return 0.0

    # ------------------------------------------------------------------------
    # Location Logic
    # ------------------------------------------------------------------------

    def _score_location(self, crop: Crop, farm_state: str) -> float:
        """
        100 if the crop has no state restriction (all-India) or the
        farm's state is explicitly listed. Partial credit (50) if
        the crop has a state list that doesn't include this state —
        still shown, just deprioritized, since state boundaries
        aren't hard agronomic limits like soil is.
        """

        if not crop.suitable_states:
            return 100.0

        normalized_states = [
            s.strip().lower() for s in crop.suitable_states
        ]

        if farm_state.strip().lower() in normalized_states:
            return 100.0

        return 50.0

    # ------------------------------------------------------------------------
    # Reasoning Builder
    # ------------------------------------------------------------------------

    def _build_reasoning(
        self,
        crop: Crop,
        farm_soil_type,
        farm_state: str,
        current_season: SeasonEnum,
        soil_score: float,
        season_score: float,
        location_score: float,
    ) -> dict:
        """
        Human-readable explanation for each score component.
        Kept separate from scoring so scoring stays pure/testable
        and reasoning text can change without touching the engine.
        """

        return {
            "soil": (
                f"{crop.name} grows well in {farm_soil_type.value} soil."
                if soil_score == 100
                else f"{crop.name} is not typically suited to {farm_soil_type.value} soil."
            ),
            "season": (
                f"Ideal sowing season is {current_season.value}, matching now."
                if season_score == 100
                else f"{crop.name} is usually sown outside the {current_season.value} season."
            ),
            "location": (
                f"Well suited to {farm_state}."
                if location_score == 100
                else f"Grown nationally; regional data for {farm_state} is limited."
            ),
        }

    # ------------------------------------------------------------------------
    # Weighted Ranking + Top-N
    # ------------------------------------------------------------------------

    def _rank_crops(
        self,
        farm,
        current_season: SeasonEnum,
        active_crops: list[Crop],
    ) -> list[tuple[Crop, float, dict]]:
        """
        Score every active crop and return them sorted by total
        weighted score, descending. Crops below MIN_SCORE_THRESHOLD
        are excluded entirely.
        """

        scored: list[tuple[Crop, float, dict]] = []

        for crop in active_crops:

            soil_score = self._score_soil(crop, farm.soil_type)
            season_score = self._score_season(crop, current_season)
            location_score = self._score_location(
                crop, farm.farmer_profile.state
            )

            total_score = (
                soil_score * SOIL_WEIGHT
                + season_score * SEASON_WEIGHT
                + location_score * LOCATION_WEIGHT
            )

            if total_score < MIN_SCORE_THRESHOLD:
                continue

            reasoning = self._build_reasoning(
                crop=crop,
                farm_soil_type=farm.soil_type,
                farm_state=farm.farmer_profile.state,
                current_season=current_season,
                soil_score=soil_score,
                season_score=season_score,
                location_score=location_score,
            )

            scored.append((crop, total_score, reasoning))

        scored.sort(key=lambda entry: entry[1], reverse=True)

        return scored[:MAX_RECOMMENDATIONS]

    # ------------------------------------------------------------------------
    # Fallback When Nothing Matches
    # ------------------------------------------------------------------------

    # Explicit ordinal order — do NOT sort by .value (alphabetical
    # sorting of "low"/"medium"/"high" is wrong: "high" < "low" alphabetically).
    _WATER_REQUIREMENT_ORDER = {
        WaterRequirementEnum.LOW: 0,
        WaterRequirementEnum.MEDIUM: 1,
        WaterRequirementEnum.HIGH: 2,
    }

    def _fallback_crops(
        self,
        active_crops: list[Crop],
    ) -> list[tuple[Crop, float, dict]]:
        """
        When no crop clears MIN_SCORE_THRESHOLD (e.g. an unusual
        soil/season combo with no seeded match), surface the
        lowest-water, most broadly tolerant crops rather than
        returning an empty list. A farmer opening the app should
        never see nothing.
        """

        fallback_pool = sorted(
            active_crops,
            key=lambda c: self._WATER_REQUIREMENT_ORDER[c.water_requirement],
        )[:MAX_RECOMMENDATIONS]

        return [
            (
                crop,
                float(MIN_SCORE_THRESHOLD),
                {
                    "soil": "No strong soil match found for your farm.",
                    "season": "No crops perfectly match the current season.",
                    "location": "Showing general-purpose fallback crops.",
                },
            )
            for crop in fallback_pool
        ]

    # ------------------------------------------------------------------------
    # Generate Recommendations (public entrypoint)
    # ------------------------------------------------------------------------

    def generate_recommendations(
        self,
        farm_id: UUID,
        user_id: UUID,
    ) -> CropRecommendation:
        """
        Run the full engine for a farm and persist the result.
        Farm lookup is scoped to the requesting user — attempting
        to generate recommendations for another user's farm
        returns a 404, same as if the farm didn't exist.
        """

        farm = farm_repository.get_by_id_for_user(
            db=self.db,
            farm_id=farm_id,
            user_id=user_id,
        )

        if farm is None:
            raise NotFoundException(message="Farm not found.")

        current_season = SeasonService.get_current_season()

        active_crops = crop_repository.get_active_crops(db=self.db)

        top_results = self._rank_crops(
            farm=farm,
            current_season=current_season,
            active_crops=active_crops,
        )

        if not top_results:
            top_results = self._fallback_crops(active_crops)

        # ----------------------------------------------------------------
        # Persist
        # ----------------------------------------------------------------

        recommendation = CropRecommendation(
            farm_id=farm_id,
            season=current_season,
            source="rule_based",
        )

        for rank, (crop, score, reasoning) in enumerate(top_results, start=1):
            recommendation.items.append(
                CropRecommendationItem(
                    crop_id=crop.id,
                    score=round(score, 2),
                    rank=rank,
                    reasoning=reasoning,
                )
            )

        return crop_repository.save_recommendation(
            db=self.db,
            recommendation=recommendation,
        )

    # ------------------------------------------------------------------------
    # Get Recommendation Details
    # ------------------------------------------------------------------------

    def get_recommendation_details(
        self,
        recommendation_id: UUID,
        user_id: UUID,
    ) -> CropRecommendation:
        """
        Fetch a previously generated recommendation run, scoped to
        the requesting user via the farm it belongs to.
        """

        recommendation = crop_repository.get_recommendation_by_id(
            db=self.db,
            recommendation_id=recommendation_id,
        )

        if recommendation is None:
            raise NotFoundException(message="Recommendation not found.")

        owned_farm = farm_repository.get_by_id_for_user(
            db=self.db,
            farm_id=recommendation.farm_id,
            user_id=user_id,
        )

        if owned_farm is None:
            raise NotFoundException(message="Recommendation not found.")

        return recommendation