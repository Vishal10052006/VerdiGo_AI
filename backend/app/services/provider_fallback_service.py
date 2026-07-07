"""
Provider Fallback Service

Determines when weather providers should automatically
switch to a fallback provider.

Responsibilities:
- Detect recoverable failures
- Select fallback provider
- Hide fallback rules
- Centralize provider switching logic

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

import httpx

from app.config.settings import settings


# ============================================================================
# Provider Fallback Service
# ============================================================================

class ProviderFallbackService:
    """
    Business logic for provider fallback decisions.
    """

    # ------------------------------------------------------------------------
    # Primary Provider
    # ------------------------------------------------------------------------

    def get_primary_provider(self) -> str:
        """
        Return configured primary provider.
        """

        return settings.PRIMARY_WEATHER_PROVIDER

    # ------------------------------------------------------------------------
    # Fallback Provider
    # ------------------------------------------------------------------------

    def get_fallback_provider(self) -> str:
        """
        Return configured fallback provider.
        """

        return settings.FALLBACK_WEATHER_PROVIDER

    # ------------------------------------------------------------------------
    # Determine Fallback
    # ------------------------------------------------------------------------

    def should_fallback(
        self,
        exception: Exception,
    ) -> bool:
        """
        Determine whether a provider fallback should occur.
        """

        # Timeout
        if isinstance(
            exception,
            httpx.TimeoutException,
        ):
            return True

        # Network Failure
        if isinstance(
            exception,
            httpx.ConnectError,
        ):
            return True

        # HTTP Errors
        if isinstance(
            exception,
            httpx.HTTPStatusError,
        ):

            status_code = exception.response.status_code

            # Recoverable provider errors
            return status_code in (
                429,
                500,
                502,
                503,
                504,
            )

        return False

    # ------------------------------------------------------------------------
    # Provider Name
    # ------------------------------------------------------------------------

    def next_provider(self) -> str:
        """
        Return configured fallback provider.
        """

        return self.get_fallback_provider()