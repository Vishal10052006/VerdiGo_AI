"""
Season Service

Determines the current Indian agricultural season from
today's date so the farmer never has to specify it manually.

Module:
Phase 1 → Module 6 → Crop Recommendation

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from datetime import date

from app.enums.season import SeasonEnum


# ============================================================================
# Season Service
# ============================================================================

class SeasonService:
    """
    Resolves the current cropping season from a calendar date.
    """

    @staticmethod
    def get_current_season(
        reference_date: date | None = None,
    ) -> SeasonEnum:
        """
        Determine season from month.

        Kharif: Jun - Oct (monsoon sown)
        Rabi:   Nov - Feb (winter sown)
        Zaid:   Mar - May (summer, irrigation dependent)

        Accepts an optional reference_date so callers (and tests)
        can resolve the season for any date, not just today —
        this is what makes T6.10's "unit test month boundaries"
        checklist item possible without mocking datetime globally.
        """

        today = reference_date or date.today()
        month = today.month

        if month in (6, 7, 8, 9, 10):
            return SeasonEnum.KHARIF

        if month in (11, 12, 1, 2):
            return SeasonEnum.RABI

        # 3, 4, 5
        return SeasonEnum.ZAID