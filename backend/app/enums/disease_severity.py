"""
Disease Severity Enum

Module: Phase 1 → Module 8 → Disease Detection
Author: VerdiGO Backend Team
"""

from enum import Enum


class DiseaseSeverityEnum(str, Enum):
    NONE = "none"          # healthy plant
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"