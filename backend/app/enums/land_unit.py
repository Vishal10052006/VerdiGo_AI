"""
Land Unit Enum

Defines supported land measurement units.

Module:
Phase 1 → Module 2 → Farmer Registration

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from enum import Enum


# ============================================================================
# Land Unit Enum
# ============================================================================

class LandUnitEnum(str, Enum):
    """
    Enumeration representing supported land units.
    """

    ACRE = "Acre"
    HECTARE = "Hectare"
    BIGHA = "Bigha"