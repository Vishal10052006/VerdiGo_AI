"""
Gender Enum

Defines the supported gender values for farmer profiles.

Module:
Phase 1 → Module 2 → Farmer Registration

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from enum import Enum


# ============================================================================
# Gender Enum
# ============================================================================

class GenderEnum(str, Enum):
    """
    Enumeration representing supported farmer genders.
    """

    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"