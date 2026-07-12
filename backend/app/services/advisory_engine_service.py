"""
Advisory Engine Service

Generates farming advisories based on normalized
weather data.

Responsibilities:
- Analyze weather conditions
- Generate advisories
- Assign severity
- Return advisory list

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from app.enums.advisory_severity import AdvisorySeverityEnum
from app.enums.advisory_type import AdvisoryTypeEnum
from app.constants.advisory import (
    HIGH_TEMPERATURE_THRESHOLD,
    FROST_TEMPERATURE_THRESHOLD,
    HIGH_HUMIDITY_THRESHOLD,
    HIGH_WIND_SPEED_THRESHOLD,
    RAINFALL_THRESHOLD,
)

# ============================================================================
# Advisory Engine Service
# ============================================================================

class AdvisoryEngineService:
    """
    Generates farming advisories.
    """

    def generate_advisories(
        self,
        weather: dict,
    ) -> list[dict]:
        """
        Generate advisories from normalized weather.
        """

        advisories = []

        # ------------------------------------------------------------
        # High Temperature
        # ------------------------------------------------------------

        if weather["temperature"] >= HIGH_TEMPERATURE_THRESHOLD:

            advisories.append({

                "type": AdvisoryTypeEnum.HEAT,

                "severity": AdvisorySeverityEnum.HIGH,

                "title": "High Temperature",

                "message": (
                    "Avoid irrigation during "
                    "peak afternoon hours."
                ),
            })

        # ------------------------------------------------------------
        # Frost
        # ------------------------------------------------------------

        if weather["temperature"] <= FROST_TEMPERATURE_THRESHOLD:

            advisories.append({

                "type": AdvisoryTypeEnum.FROST,

                "severity": AdvisorySeverityEnum.HIGH,

                "title": "Frost Alert",

                "message": (
                    "Protect crops from frost."
                ),
            })

        # ------------------------------------------------------------
        # High Humidity
        # ------------------------------------------------------------

        if weather["humidity"] >= HIGH_HUMIDITY_THRESHOLD:

            advisories.append({

                "type": AdvisoryTypeEnum.DISEASE,

                "severity": AdvisorySeverityEnum.MODERATE,

                "title": "Disease Risk",

                "message": (
                    "High humidity may increase "
                    "fungal disease risk."
                ),
            })

        # ------------------------------------------------------------
        # Strong Wind
        # ------------------------------------------------------------

        if weather["wind_speed"] >= HIGH_WIND_SPEED_THRESHOLD:

            advisories.append({

                "type": AdvisoryTypeEnum.WIND,

                "severity": AdvisorySeverityEnum.MODERATE,

                "title": "Strong Wind",

                "message": (
                    "Avoid pesticide spraying "
                    "during strong winds."
                ),
            })

        # ------------------------------------------------------------
        # Rainfall
        # ------------------------------------------------------------

        if weather["rainfall"] >= RAINFALL_THRESHOLD:

            advisories.append({

                "type": AdvisoryTypeEnum.IRRIGATION,

                "severity": AdvisorySeverityEnum.LOW,

                "title": "Rain Expected",

                "message": (
                    "Irrigation is not required."
                ),
            })

        return advisories