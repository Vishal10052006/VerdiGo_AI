"""
Advisory Type Enum

Defines agriculture advisory categories.

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from enum import Enum


# ============================================================================
# Advisory Type Enum
# ============================================================================

class AdvisoryTypeEnum(str, Enum):
    """
    Types of agriculture advisories.
    """

    RAIN = "rain"
    IRRIGATION = "irrigation"
    HEAT = "heat"
    FROST = "frost"
    WIND = "wind"
    HUMIDITY = "humidity"
    DISEASE = "disease"
    WEATHER_SUMMARY = "weather_summary"
    TEMPERATURE = "temperature"