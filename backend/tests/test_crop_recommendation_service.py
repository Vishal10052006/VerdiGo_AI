"""
Crop Recommendation Engine Tests

Module:
Phase 1 → Module 6 → Crop Recommendation

Author: VerdiGO Backend Team
"""

from types import SimpleNamespace

from app.services.crop_recommendation_service import CropRecommendationService
from app.enums.season import SeasonEnum
from app.enums.soil_type import SoilTypeEnum
from app.enums.water_requirement import WaterRequirementEnum


def make_crop(name, soils, seasons, states=None, water=WaterRequirementEnum.LOW):
    return SimpleNamespace(
        name=name,
        suitable_soil_types=soils,
        suitable_seasons=seasons,
        suitable_states=states,
        water_requirement=water,
    )


def test_soil_score_match_and_mismatch():
    service = CropRecommendationService(db=None)
    crop = make_crop("Rice", [SoilTypeEnum.CLAY], [SeasonEnum.KHARIF])

    assert service._score_soil(crop, SoilTypeEnum.CLAY) == 100.0
    assert service._score_soil(crop, SoilTypeEnum.SANDY) == 0.0


def test_season_score_match_and_mismatch():
    service = CropRecommendationService(db=None)
    crop = make_crop("Wheat", [SoilTypeEnum.LOAMY], [SeasonEnum.RABI])

    assert service._score_season(crop, SeasonEnum.RABI) == 100.0
    assert service._score_season(crop, SeasonEnum.KHARIF) == 0.0


def test_location_score_all_india_vs_restricted():
    service = CropRecommendationService(db=None)

    all_india_crop = make_crop("Wheat", [SoilTypeEnum.LOAMY], [SeasonEnum.RABI], states=None)
    assert service._score_location(all_india_crop, "Bihar") == 100.0

    restricted_crop = make_crop(
        "Cotton", [SoilTypeEnum.BLACK], [SeasonEnum.KHARIF],
        states=["Maharashtra", "Gujarat"],
    )
    assert service._score_location(restricted_crop, "Maharashtra") == 100.0
    assert service._score_location(restricted_crop, "Bihar") == 50.0


def test_fallback_returns_nonempty_when_no_match():
    service = CropRecommendationService(db=None)
    crops = [
        make_crop("A", [SoilTypeEnum.SANDY], [SeasonEnum.ZAID], water=WaterRequirementEnum.LOW),
        make_crop("B", [SoilTypeEnum.CLAY], [SeasonEnum.KHARIF], water=WaterRequirementEnum.HIGH),
    ]
    fallback = service._fallback_crops(crops)

    assert len(fallback) > 0
    assert fallback[0][0].water_requirement == WaterRequirementEnum.LOW  # lowest water first