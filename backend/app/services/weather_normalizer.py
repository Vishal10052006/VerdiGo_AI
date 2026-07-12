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

            "fetched_at": current["last_updated"],
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

            "fetched_at": current.get("time"),
        }
    

    # ------------------------------------------------------------------------
    # Normalize WeatherAPI Forecast
    # ------------------------------------------------------------------------

    @staticmethod
    def normalize_weatherapi_forecast(
        data: dict,
    ) -> dict:
        """
        Normalize WeatherAPI forecast response into
        VerdiGO's unified forecast format.
        """

        forecast_days = []

        for day in data["forecast"]["forecastday"]:

            forecast_days.append({

                "date": day["date"],

                "min_temperature": day["day"]["mintemp_c"],

                "max_temperature": day["day"]["maxtemp_c"],

                "rainfall": day["day"]["totalprecip_mm"],

                "humidity": day["day"]["avghumidity"],

                "wind_speed": day["day"]["maxwind_kph"],

                "condition": day["day"]["condition"]["text"],

            })

        return {

            "provider": "weatherapi",

            "generated_at": data["location"]["localtime"],

            "forecast": forecast_days,

        }
    

    # ------------------------------------------------------------------------
    # Normalize Open-Meteo Forecast
    # ------------------------------------------------------------------------

    @staticmethod
    def normalize_openmeteo_forecast(
        data: dict,
    ) -> dict:
        """
        Normalize Open-Meteo forecast response into
        VerdiGO's unified forecast format.
        """

        daily = data["daily"]

        forecast_days = []

        for index, forecast_date in enumerate(daily["time"]):

            forecast_days.append({

                "date": forecast_date,

                "min_temperature": daily["temperature_2m_min"][index],

                "max_temperature": daily["temperature_2m_max"][index],

                "rainfall": daily["precipitation_sum"][index],

                "humidity": daily["relative_humidity_2m_mean"][index],

                "wind_speed": daily["wind_speed_10m_max"][index],

                "condition": OPEN_METEO_WEATHER_CODES.get(
                    daily["weather_code"][index],
                    "Unknown",
                ),

            })

        return {

            "provider": "openmeteo",

            "generated_at": daily["time"][0],

            "forecast": forecast_days,

        }