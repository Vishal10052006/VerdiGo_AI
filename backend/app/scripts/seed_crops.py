"""
Seed Crops

One-time / re-runnable script to populate the crops master
table with baseline agronomic data.

⚠️ Yield and temperature figures are placeholders based on
general agronomic knowledge — verify against ICAR / state
agriculture department data before production use.

Usage:
    python -m app.scripts.seed_crops

Module:
Phase 1 → Module 6 → Crop Recommendation

Author: VerdiGO Backend Team
"""

from app.database.database import SessionLocal
from app.models.crop import Crop
from app.enums.soil_type import SoilTypeEnum
from app.enums.season import SeasonEnum
from app.enums.water_requirement import WaterRequirementEnum


CROPS = [
    dict(
        name="Rice",
        suitable_soil_types=[SoilTypeEnum.CLAY, SoilTypeEnum.ALLUVIAL, SoilTypeEnum.LOAMY],
        suitable_seasons=[SeasonEnum.KHARIF],
        suitable_states=None,
        water_requirement=WaterRequirementEnum.HIGH,
        ideal_temp_min=20, ideal_temp_max=35,
        growth_duration_days=120,
        expected_yield_per_acre="20-25 quintals (verify locally)",
    ),
    dict(
        name="Wheat",
        suitable_soil_types=[SoilTypeEnum.ALLUVIAL, SoilTypeEnum.LOAMY, SoilTypeEnum.BLACK],
        suitable_seasons=[SeasonEnum.RABI],
        suitable_states=None,
        water_requirement=WaterRequirementEnum.MEDIUM,
        ideal_temp_min=10, ideal_temp_max=25,
        growth_duration_days=140,
        expected_yield_per_acre="16-20 quintals (verify locally)",
    ),
    dict(
        name="Maize",
        suitable_soil_types=[SoilTypeEnum.ALLUVIAL, SoilTypeEnum.LOAMY, SoilTypeEnum.RED],
        suitable_seasons=[SeasonEnum.KHARIF, SeasonEnum.ZAID],
        suitable_states=None,
        water_requirement=WaterRequirementEnum.MEDIUM,
        ideal_temp_min=18, ideal_temp_max=32,
        growth_duration_days=100,
        expected_yield_per_acre="20-24 quintals (verify locally)",
    ),
    dict(
        name="Cotton",
        suitable_soil_types=[SoilTypeEnum.BLACK, SoilTypeEnum.ALLUVIAL],
        suitable_seasons=[SeasonEnum.KHARIF],
        suitable_states=["Maharashtra", "Gujarat", "Madhya Pradesh", "Telangana"],
        water_requirement=WaterRequirementEnum.MEDIUM,
        ideal_temp_min=21, ideal_temp_max=35,
        growth_duration_days=180,
        expected_yield_per_acre="6-8 quintals lint (verify locally)",
    ),
    dict(
        name="Sugarcane",
        suitable_soil_types=[SoilTypeEnum.ALLUVIAL, SoilTypeEnum.LOAMY, SoilTypeEnum.BLACK],
        suitable_seasons=[SeasonEnum.ZAID, SeasonEnum.KHARIF],
        suitable_states=["Uttar Pradesh", "Maharashtra", "Karnataka", "Tamil Nadu"],
        water_requirement=WaterRequirementEnum.HIGH,
        ideal_temp_min=20, ideal_temp_max=35,
        growth_duration_days=365,
        expected_yield_per_acre="300-350 quintals (verify locally)",
    ),
    dict(
        name="Soybean",
        suitable_soil_types=[SoilTypeEnum.BLACK, SoilTypeEnum.LOAMY],
        suitable_seasons=[SeasonEnum.KHARIF],
        suitable_states=["Madhya Pradesh", "Maharashtra", "Rajasthan"],
        water_requirement=WaterRequirementEnum.MEDIUM,
        ideal_temp_min=20, ideal_temp_max=30,
        growth_duration_days=100,
        expected_yield_per_acre="8-10 quintals (verify locally)",
    ),
    dict(
        name="Groundnut",
        suitable_soil_types=[SoilTypeEnum.SANDY, SoilTypeEnum.RED, SoilTypeEnum.LOAMY],
        suitable_seasons=[SeasonEnum.KHARIF, SeasonEnum.ZAID],
        suitable_states=["Gujarat", "Andhra Pradesh", "Tamil Nadu", "Rajasthan"],
        water_requirement=WaterRequirementEnum.LOW,
        ideal_temp_min=20, ideal_temp_max=30,
        growth_duration_days=110,
        expected_yield_per_acre="8-10 quintals (verify locally)",
    ),
    dict(
        name="Bajra (Pearl Millet)",
        suitable_soil_types=[SoilTypeEnum.SANDY, SoilTypeEnum.RED, SoilTypeEnum.UNKNOWN],
        suitable_seasons=[SeasonEnum.KHARIF],
        suitable_states=["Rajasthan", "Gujarat", "Haryana", "Uttar Pradesh"],
        water_requirement=WaterRequirementEnum.LOW,
        ideal_temp_min=25, ideal_temp_max=35,
        growth_duration_days=80,
        expected_yield_per_acre="6-8 quintals (verify locally)",
    ),
    dict(
        name="Jowar (Sorghum)",
        suitable_soil_types=[SoilTypeEnum.BLACK, SoilTypeEnum.RED, SoilTypeEnum.LOAMY],
        suitable_seasons=[SeasonEnum.KHARIF, SeasonEnum.RABI],
        suitable_states=["Maharashtra", "Karnataka", "Madhya Pradesh"],
        water_requirement=WaterRequirementEnum.LOW,
        ideal_temp_min=20, ideal_temp_max=32,
        growth_duration_days=110,
        expected_yield_per_acre="7-9 quintals (verify locally)",
    ),
    dict(
        name="Chickpea (Chana)",
        suitable_soil_types=[SoilTypeEnum.BLACK, SoilTypeEnum.ALLUVIAL, SoilTypeEnum.LOAMY],
        suitable_seasons=[SeasonEnum.RABI],
        suitable_states=None,
        water_requirement=WaterRequirementEnum.LOW,
        ideal_temp_min=10, ideal_temp_max=25,
        growth_duration_days=110,
        expected_yield_per_acre="8-10 quintals (verify locally)",
    ),
    dict(
        name="Mustard",
        suitable_soil_types=[SoilTypeEnum.ALLUVIAL, SoilTypeEnum.LOAMY],
        suitable_seasons=[SeasonEnum.RABI],
        suitable_states=["Rajasthan", "Haryana", "Uttar Pradesh", "Madhya Pradesh"],
        water_requirement=WaterRequirementEnum.LOW,
        ideal_temp_min=10, ideal_temp_max=25,
        growth_duration_days=130,
        expected_yield_per_acre="6-8 quintals (verify locally)",
    ),
    dict(
        name="Potato",
        suitable_soil_types=[SoilTypeEnum.LOAMY, SoilTypeEnum.SANDY, SoilTypeEnum.ALLUVIAL],
        suitable_seasons=[SeasonEnum.RABI],
        suitable_states=["Uttar Pradesh", "West Bengal", "Bihar", "Punjab"],
        water_requirement=WaterRequirementEnum.MEDIUM,
        ideal_temp_min=15, ideal_temp_max=25,
        growth_duration_days=90,
        expected_yield_per_acre="80-100 quintals (verify locally)",
    ),
]


def seed_crops() -> None:
    """
    Insert crops if they don't already exist (by name).
    Safe to re-run.
    """

    db = SessionLocal()

    try:
        inserted = 0
        skipped = 0

        for crop_data in CROPS:

            existing = (
                db.query(Crop)
                .filter(Crop.name == crop_data["name"])
                .first()
            )

            if existing:
                skipped += 1
                continue

            db.add(Crop(**crop_data))
            inserted += 1

        db.commit()

        print(f"✅ Seeded {inserted} crops, skipped {skipped} existing.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_crops()