"""
Weather Helper Utilities

Common helper functions used throughout the Weather
Intelligence module.

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

from datetime import datetime, timedelta


def calculate_expiry(minutes: int) -> datetime:
    """
    Returns cache expiry timestamp.
    """

    return datetime.utcnow() + timedelta(minutes=minutes)