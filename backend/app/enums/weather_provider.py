"""
Weather Provider Enum

Defines all supported weather data providers.

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from enum import Enum


# ============================================================================
# Weather Provider Enum
# ============================================================================

class WeatherProviderEnum(str, Enum):
    """
    Enumeration representing supported weather providers.
    """

    WEATHER_API = "weatherapi"

    OPEN_METEO = "openmeteo"