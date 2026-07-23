# backend/tests/test_weather_authenticated.py
"""
Weather API Tests

Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""


def _create_farm_for_user(client, headers, farm_name="Weather Test Farm"):
    client.post(
        "/farmer/profile",
        json={
            "full_name": "Weather Test Farmer",
            "age": 35,
            "gender": "Male",
            "state": "Bihar",
            "district": "Begusarai",
            "village": "Barauni",
        },
        headers=headers,
    )

    farm_response = client.post(
        "/farm",
        json={
            "farm_name": farm_name,
            "land_area": 5,
            "land_unit": "Acre",
            "soil_type": "Alluvial",
            "latitude": 25.4358,
            "longitude": 86.1347,
        },
        headers=headers,
    )

    if farm_response.status_code == 200:
        return farm_response.json()["data"]["id"]

    existing = client.get("/farm", headers=headers)
    assert existing.status_code == 200, existing.text
    return existing.json()["id"]


def test_get_current_weather(auth_headers, client):
    """
    Current weather endpoint should return weather
    when authenticated, for a farm the user actually owns.
    """

    farm_id = _create_farm_for_user(client, auth_headers)

    response = client.get(
        f"/v1/weather/current/{farm_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert "data" in body
    assert "temperature" in body["data"]