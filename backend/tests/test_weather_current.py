"""
Weather Current API Tests

Tests:
- GET /v1/weather/current/{farm_id}

Module:
Phase 1 → Module 5 → Testing

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from uuid import uuid4


# ============================================================================
# Current Weather Tests
# ============================================================================

def test_current_weather_requires_auth(client):
    """
    Request without JWT token should fail.
    """

    farm_id = uuid4()

    response = client.get(
        f"/v1/weather/current/{farm_id}"
    )

    assert response.status_code == 401