"""
Water Requirement Enum

Module:
Phase 1 → Module 6 → Crop Recommendation

Author: VerdiGO Backend Team
"""

from enum import Enum


class WaterRequirementEnum(str, Enum):
    """
    Relative water demand of a crop.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"