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
        Fetch current weather. Signature intentionally matches
        WeatherAPIClient.get_current_weather(latitude, longitude) —
        WeatherProviderManager calls both clients interchangeably
        through the same fallback path and requires matching call
        signatures.
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
            response = client.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()

    # ------------------------------------------------------------------------
    # Forecast Weather
    # ------------------------------------------------------------------------

    def get_forecast(
        self,
        latitude: float,
        longitude: float,
        days: int = 5,
    ) -> dict:
        """
        Fetch weather forecast. Requests every field
        WeatherNormalizer.normalize_openmeteo_forecast() consumes
        (temperature min/max, precipitation, humidity mean, max wind,
        weather code) — previously several of these were missing,
        causing a KeyError the first time this path's data reached
        the normalizer.
        """

        endpoint = f"{self.base_url}/forecast"

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "forecast_days": days,
            "daily": (
                "temperature_2m_max,"
                "temperature_2m_min,"
                "precipitation_sum,"
                "relative_humidity_2m_mean,"
                "wind_speed_10m_max,"
                "weather_code"
            ),
            "timezone": "auto",
        }

        with httpx.Client(timeout=self.timeout) as client:
            response = client.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()