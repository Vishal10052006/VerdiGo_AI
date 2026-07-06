"""
WeatherAPI Client

Handles communication with WeatherAPI.com.

Responsibilities:
- Fetch current weather
- Fetch weather forecast
- Handle request timeout
- Return raw WeatherAPI response

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
# WeatherAPI Client
# ============================================================================

class WeatherAPIClient:
    """
    Client for communicating with WeatherAPI.com.
    """

    def __init__(self):
        """
        Initialize WeatherAPI configuration.
        """

        if not settings.WEATHERAPI_API_KEY:
            raise ValueError(
                "WEATHERAPI_API_KEY is not configured."
            )

        self.base_url = settings.WEATHERAPI_BASE_URL
        self.api_key = settings.WEATHERAPI_API_KEY
        self.timeout = settings.WEATHER_REQUEST_TIMEOUT

    # ------------------------------------------------------------------------
    # Current Weather
    # ------------------------------------------------------------------------

    def get_current_weather(
        self,
        latitude: float,
        longitude: float,
    ) -> dict:
        """
        Fetch current weather from WeatherAPI.
        """

        endpoint = f"{self.base_url}/current.json"

        params: dict = {
            "key": self.api_key,
            "q": f"{latitude},{longitude}",
        }

        with httpx.Client(timeout=self.timeout) as client:

            response = client.get(
                endpoint,
                params=params,
            )

            response.raise_for_status()

            return response.json()

    # ------------------------------------------------------------------------
    # Forecast Weather
    # ------------------------------------------------------------------------

    def get_forecast(
        self,
        latitude: float,
        longitude: float,
        days: int = 3,
    ) -> dict:
        """
        Fetch forecast weather from WeatherAPI.
        """

        endpoint = f"{self.base_url}/forecast.json"

        params: dict = {
            "key": self.api_key,
            "q": f"{latitude},{longitude}",
            "days": days,
        }

        with httpx.Client(timeout=self.timeout) as client:

            response = client.get(
                endpoint,
                params=params,
            )

            response.raise_for_status()

            return response.json()