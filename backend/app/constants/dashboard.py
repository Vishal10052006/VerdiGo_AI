"""
Dashboard Constants

Module:
Phase 1 → Module 4 → Dashboard
"""

# ============================================================================
# Success Messages
# ============================================================================

DASHBOARD_LOADED = "Dashboard loaded successfully."

FARMER_OVERVIEW_LOADED = "Farmer overview loaded successfully."


# ============================================================================
# Error Messages
# ============================================================================

FARMER_PROFILE_NOT_FOUND = "Farmer profile not found."

FARM_NOT_FOUND = "Farm information not found."


# ============================================================================
# Cache Configuration
# ============================================================================

# Short TTL — dashboard data (farm info, profile completion, weather) does
# not change second-to-second. 60s balances "feels live" against cutting
# repeated DB hits when a farmer refreshes/reopens the dashboard rapidly.
# Weather itself has its own longer-lived cache (WEATHER_CACHE_MINUTES) —
# this cache wraps the *whole assembled response*, avoiding the farm/user
# join + profile-completion recomputation on every hit, not just the
# weather API call.
DASHBOARD_CACHE_TTL_SECONDS = 60