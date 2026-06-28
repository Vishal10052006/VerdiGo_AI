"""
Soil Type Enum

Defines supported soil types for farm registration.

Module:
Phase 1 → Module 2 → Farmer Registration

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from enum import Enum


# ============================================================================
# Soil Type Enum
# ============================================================================

class SoilTypeEnum(str, Enum):
    """
    Enumeration representing supported soil types.
    """

    CLAY = "Clay"
    SANDY = "Sandy"
    LOAMY = "Loamy"
    SILTY = "Silty"
    BLACK = "Black"
    RED = "Red"
    LATERITE = "Laterite"
    ALLUVIAL = "Alluvial"
    MOUNTAIN = "Mountain"
    UNKNOWN = "Unknown"