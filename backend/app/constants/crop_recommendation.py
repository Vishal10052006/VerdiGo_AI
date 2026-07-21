"""
Crop Recommendation Constants

Scoring weights and thresholds for the rule-based
recommendation engine.

Module:
Phase 1 → Module 6 → Crop Recommendation

Author: VerdiGO Backend Team
"""

# ============================================================================
# Scoring Weights (must sum to 1.0)
# ============================================================================

SOIL_WEIGHT = 0.40
SEASON_WEIGHT = 0.35
LOCATION_WEIGHT = 0.25

# ============================================================================
# Result Configuration
# ============================================================================

MAX_RECOMMENDATIONS = 5

MIN_SCORE_THRESHOLD = 20  # below this, a crop is excluded entirely

# ============================================================================
# Season Date Ranges (month numbers)
# ============================================================================

SEASON_MONTH_RANGES = {
    "kharif": (6, 10),
    "rabi": (11, 2),   # wraps year boundary
    "zaid": (3, 5),
}