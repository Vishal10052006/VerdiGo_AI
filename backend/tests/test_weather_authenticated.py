"""
Weather API Tests

Phase 1 → Module 5 → Weather Intelligence

Author: VerdiGO Backend Team
"""

# ============================================================================
# Current Weather (Authenticated)
# ============================================================================


def test_get_current_weather(auth_headers, client):
    """
    Current weather endpoint should return weather
    when authenticated.
    """

    farm_id = "9f2da35c-6c17-49d3-8067-ad9e5e9760b3"

    response = client.get(
        f"/v1/weather/current/{farm_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert "data" in body
    assert "temperature" in body["data"]