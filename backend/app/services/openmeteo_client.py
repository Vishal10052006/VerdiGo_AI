"""
Open-Meteo Client

Handles communication with Open-Meteo.

Responsibilities:
- Fetch current weather
- Fetch weather forecast
- Return raw provider response

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
# Open-Meteo Client
# ============================================================================

class OpenMeteoClient:
    """
    Client for communicating with Open-Meteo.
    """

    def __init__(self):
        """
        Initialize provider configuration.
        """

        self.base_url = settings.OPENMETEO_BASE_URL
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
        Fetch current weather.
        """

        endpoint = f"{self.base_url}/forecast"

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "wind_speed_10m,"
                "weather_code"
            ),
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
        Fetch weather forecast.
        """

        endpoint = f"{self.base_url}/forecast"

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "forecast_days": days,
            "daily": (
                "temperature_2m_max,"
                "temperature_2m_min,"
                "precipitation_sum"
            ),
            "timezone": "auto",
        }

        with httpx.Client(timeout=self.timeout) as client:

            response = client.get(
                endpoint,
                params=params,
            )

            response.raise_for_status()

            return response.json()