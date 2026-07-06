"""
Weather Constants

Centralized constants used across the Weather Intelligence module.

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Cache Configuration
# ============================================================================

DEFAULT_CACHE_DURATION_MINUTES = 30

# ============================================================================
# Request Configuration
# ============================================================================

DEFAULT_TIMEOUT_SECONDS = 10

MAX_RETRY_ATTEMPTS = 2

# ============================================================================
# Supported Providers
# ============================================================================

WEATHER_API = "weatherapi"

OPEN_METEO = "openmeteo"


MAX_RETRY_ATTEMPTS = 2

RETRYABLE_STATUS_CODES = (
    429,
    500,
    502,
    503,
    504,
)