"""
Season Enum

Defines India's agricultural cropping seasons.

Module:
Phase 1 → Module 6 → Crop Recommendation

Author: VerdiGO Backend Team
"""

from enum import Enum


class SeasonEnum(str, Enum):
    """
    Indian agricultural seasons.
    """

    KHARIF = "kharif"    # Jun - Oct (monsoon sown)
    RABI = "rabi"          # Nov - Feb (winter sown)
    ZAID = "zaid"          # Mar - May (summer, irrigation dependent)