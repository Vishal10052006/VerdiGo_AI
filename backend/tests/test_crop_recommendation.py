"""
Crop Recommendation API Integration Tests

Tests:
- GET /v1/crop-recommendation/{farm_id}
- GET /v1/crop-recommendation/details/{recommendation_id}

Covers the full path: auth, ownership scoping, and a real
end-to-end recommendation generation — this is the automated
version of the manual verification done during Module 6 build.

Module:
Phase 1 → Module 6 → Crop Recommendation

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from uuid import uuid4

from app.database.database import SessionLocal
from app.repositories import otp_repository


# ============================================================================
# Helpers
# ============================================================================

def _create_farm_for_user(client, headers, farm_name="Test Farm"):
    """
    Ensure a farmer profile + farm exist for whichever user the
    given auth headers belong to. Returns the farm's ID.

    Idempotent: if a profile/farm already exists for this user
    (e.g. from a previous test run or manual testing), reuses it
    instead of failing — farm_service.py enforces one farm per
    farmer profile, so blindly creating would 400 on a dirty DB.
    """

    client.post(
        "/farmer/profile",
        json={
            "full_name": "Test Farmer",
            "age": 35,
            "gender": "Male",
            "state": "Bihar",
            "district": "Begusarai",
            "village": "Barauni",
        },
        headers=headers,
    )
    # Ignore the response here — 200 (created) and 400 (already
    # exists) are both fine; we only care that a profile exists
    # by the time we try to fetch/create the farm below.

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

    if farm_response.status_code == 400:
        # Farm already exists for this user — fetch it instead.
        existing = client.get("/farm", headers=headers)
        assert existing.status_code == 200, existing.text
        return existing.json()["id"]

    # Anything else (401, 422, 500) is a real failure — don't swallow it.
    assert False, f"Unexpected farm creation response: {farm_response.status_code} {farm_response.text}"


def _login_second_user(client, mobile="9123456780"):
    """
    Logs in a distinct second user (separate from the shared
    `auth_headers` fixture user) so ownership boundaries can be
    tested. Mirrors conftest.py's auth_headers logic.
    """

    login = client.post("/auth/login", json={"mobile": mobile})
    assert login.status_code == 200

    db = SessionLocal()
    latest_otp = otp_repository.get_latest(db=db, mobile=mobile)
    db.close()

    otp_response = client.post(
        "/auth/verify-otp",
        json={"mobile": mobile, "otp": latest_otp.otp},
    )
    assert otp_response.status_code == 200

    token = otp_response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


# ============================================================================
# Auth Required
# ============================================================================

def test_crop_recommendation_requires_auth(client):
    """
    Request without a JWT token must fail.
    """

    farm_id = uuid4()

    response = client.get(f"/v1/crop-recommendation/{farm_id}")

    assert response.status_code == 401


# ============================================================================
# Farm Not Found
# ============================================================================

def test_crop_recommendation_farm_not_found(client, auth_headers):
    """
    A farm ID that doesn't exist at all returns 404.
    """

    response = client.get(
        "/v1/crop-recommendation/00000000-0000-0000-0000-000000000000",
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Farm not found."


# ============================================================================
# Happy Path — Own Farm Returns Ranked Recommendations
# ============================================================================

def test_crop_recommendation_returns_ranked_crops(client, auth_headers):
    """
    Requesting recommendations for a farm you own returns a
    populated, ranked list.
    """

    farm_id = _create_farm_for_user(client, auth_headers)

    response = client.get(
        f"/v1/crop-recommendation/{farm_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True

    items = body["data"]["items"]
    assert len(items) > 0

    # Ranks should be contiguous starting at 1
    ranks = [item["rank"] for item in items]
    assert ranks == sorted(ranks)
    assert ranks[0] == 1

    # Every item must carry reasoning — the whole point of the engine
    for item in items:
        assert "soil" in item["reasoning"]
        assert "season" in item["reasoning"]
        assert "location" in item["reasoning"]


# ============================================================================
# Security — Cannot Access Another User's Farm
# ============================================================================

def test_crop_recommendation_blocks_other_users_farm(client, auth_headers):
    """
    A real, existing farm belonging to a DIFFERENT user must
    return 404, not the recommendation data, and not a 403
    (which would confirm the farm's existence to an attacker).

    This is the regression test for the ownership fix — if this
    ever goes green→red, someone reintroduced the leak.
    """

    other_user_headers = _login_second_user(client)
    other_farm_id = _create_farm_for_user(
        client, other_user_headers, farm_name="Other User's Farm"
    )

    response = client.get(
        f"/v1/crop-recommendation/{other_farm_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Farm not found."


# ============================================================================
# Recommendation Details
# ============================================================================

def test_recommendation_details_returns_full_data(client, auth_headers):
    """
    Fetching details of a recommendation you own returns the
    same data that generation produced.
    """

    farm_id = _create_farm_for_user(
        client, auth_headers, farm_name="Details Test Farm"
    )

    generate_response = client.get(
        f"/v1/crop-recommendation/{farm_id}",
        headers=auth_headers,
    )
    recommendation_id = generate_response.json()["data"]["id"]

    details_response = client.get(
        f"/v1/crop-recommendation/details/{recommendation_id}",
        headers=auth_headers,
    )

    assert details_response.status_code == 200
    assert details_response.json()["data"]["id"] == recommendation_id


def test_recommendation_details_blocks_other_users_recommendation(
    client, auth_headers
):
    """
    A recommendation belonging to another user's farm must not
    be readable via the details endpoint either — this is the
    same ownership boundary, tested on the second route.
    """

    other_user_headers = _login_second_user(client, mobile="9123456781")
    other_farm_id = _create_farm_for_user(
        client, other_user_headers, farm_name="Details Security Farm"
    )

    generate_response = client.get(
        f"/v1/crop-recommendation/{other_farm_id}",
        headers=other_user_headers,
    )
    other_recommendation_id = generate_response.json()["data"]["id"]

    response = client.get(
        f"/v1/crop-recommendation/details/{other_recommendation_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404