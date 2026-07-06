"""
Open-Meteo Weather Codes

Maps Open-Meteo weather codes to human-readable descriptions.

Module:
Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Open-Meteo Weather Code Mapping
# ============================================================================

OPEN_METEO_WEATHER_CODES = {

    # Clear
    0: "Clear Sky",

    # Clouds
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",

    # Fog
    45: "Fog",
    48: "Depositing Rime Fog",

    # Drizzle
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Dense Drizzle",

    # Freezing Drizzle
    56: "Light Freezing Drizzle",
    57: "Dense Freezing Drizzle",

    # Rain
    61: "Slight Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",

    # Freezing Rain
    66: "Light Freezing Rain",
    67: "Heavy Freezing Rain",

    # Snow
    71: "Slight Snow",
    73: "Moderate Snow",
    75: "Heavy Snow",
    77: "Snow Grains",

    # Rain Showers
    80: "Rain Showers",
    81: "Heavy Rain Showers",
    82: "Violent Rain Showers",

    # Snow Showers
    85: "Snow Showers",
    86: "Heavy Snow Showers",

    # Thunderstorm
    95: "Thunderstorm",
    96: "Thunderstorm with Hail",
    99: "Severe Thunderstorm with Hail",
}