"""
Season Service Tests

Module:
Phase 1 → Module 6 → Crop Recommendation

Author: VerdiGO Backend Team
"""

from datetime import date

from app.services.season_service import SeasonService
from app.enums.season import SeasonEnum


def test_kharif_months():
    for month in (6, 7, 8, 9, 10):
        result = SeasonService.get_current_season(date(2026, month, 15))
        assert result == SeasonEnum.KHARIF, f"month {month} should be KHARIF"


def test_rabi_months():
    for month in (11, 12, 1, 2):
        result = SeasonService.get_current_season(date(2026, month, 15))
        assert result == SeasonEnum.RABI, f"month {month} should be RABI"


def test_zaid_months():
    for month in (3, 4, 5):
        result = SeasonService.get_current_season(date(2026, month, 15))
        assert result == SeasonEnum.ZAID, f"month {month} should be ZAID"


def test_defaults_to_today_when_no_date_given():
    # Just confirm it doesn't error and returns a valid enum member
    result = SeasonService.get_current_season()
    assert result in SeasonEnum