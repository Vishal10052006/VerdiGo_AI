"""
Weather Normalizer

Converts responses from different weather providers into a
single VerdiGO weather format.

Responsibilities:
- Normalize WeatherAPI responses
- Normalize Open-Meteo responses
- Return provider-independent weather data

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from app.constants.weather_codes import OPEN_METEO_WEATHER_CODES


# ============================================================================
# Weather Normalizer
# ============================================================================

class WeatherNormalizer:
    """
    Converts provider-specific weather responses into
    VerdiGO's common response format.
    """

    # ------------------------------------------------------------------------
    # WeatherAPI Normalization
    # ------------------------------------------------------------------------

    @staticmethod
    def normalize_weatherapi(data: dict) -> dict:
        """
        Normalize WeatherAPI response.
        """

        current = data["current"]
        location = data["location"]

        return {

            "provider": "weatherapi",

            "latitude": location["lat"],
            "longitude": location["lon"],

            "temperature": current["temp_c"],
            "feels_like": current["feelslike_c"],

            "humidity": current["humidity"],

            "wind_speed": current["wind_kph"],

            "pressure": current["pressure_mb"],

            "visibility": current["vis_km"],

            "uv_index": current["uv"],

            "rainfall": current["precip_mm"],

            "condition": current["condition"]["text"],

            "observed_at": current["last_updated"],
        }

    # ------------------------------------------------------------------------
    # Open-Meteo Normalization
    # ------------------------------------------------------------------------

    @staticmethod
    def normalize_openmeteo(data: dict) -> dict:
        """
        Normalize Open-Meteo response.
        """

        current = data["current"]

        weather_code = current.get("weather_code")

        return {

            "provider": "openmeteo",

            "latitude": data["latitude"],
            "longitude": data["longitude"],

            "temperature": current.get("temperature_2m"),

            # Open-Meteo does not provide feels-like in the current endpoint
            "feels_like": None,

            "humidity": current.get("relative_humidity_2m"),

            "wind_speed": current.get("wind_speed_10m"),

            # Optional fields depending on requested parameters
            "pressure": current.get("surface_pressure"),

            "visibility": current.get("visibility"),

            "uv_index": current.get("uv_index"),

            "rainfall": current.get("rain", 0),

            "condition": OPEN_METEO_WEATHER_CODES.get(
                weather_code,
                "Unknown",
            ),

            "observed_at": current.get("time"),
        }