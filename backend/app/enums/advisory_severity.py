"""
Advisory Severity Enum

Defines advisory severity levels.

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from enum import Enum


# ============================================================================
# Advisory Severity Enum
# ============================================================================

class AdvisorySeverityEnum(str, Enum):
    """
    Severity of generated advisory.
    """

    LOW = "low"

    MODERATE = "moderate"

    HIGH = "high"

    CRITICAL = "critical"