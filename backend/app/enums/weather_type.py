"""
Weather Type Enum

Defines supported weather request types.

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from enum import Enum


# ============================================================================
# Weather Type Enum
# ============================================================================

class WeatherTypeEnum(str, Enum):
    """
    Types of weather data.
    """

    CURRENT = "current"

    FORECAST = "forecast"