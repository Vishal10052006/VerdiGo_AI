# backend/tests/test_chat_rate_limit.py
"""
Chat Rate Limit Tests

Module:
Phase 1 → Module 7 → AI Chat Assistant
"""

from unittest.mock import patch

from app.database.database import SessionLocal
from app.repositories import otp_repository


def _login_isolated_user(client, mobile):
    """
    Logs in a farmer with a mobile number unique to this test so
    the daily message count can't be polluted by other tests that
    ran earlier in the same session using the shared auth_headers
    fixture's mobile number.
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


def _create_farm_for_user(client, headers):
    client.post(
        "/farmer/profile",
        json={
            "full_name": "Rate Limit Farmer",
            "age": 30,
            "gender": "Male",
            "state": "Bihar",
            "district": "Begusarai",
            "village": "Barauni",
        },
        headers=headers,
    )
    client.post(
        "/farm",
        json={
            "farm_name": "Rate Limit Farm",
            "land_area": 5,
            "land_unit": "Acre",
            "soil_type": "Alluvial",
            "latitude": 25.4358,
            "longitude": 86.1347,
        },
        headers=headers,
    )


def test_exceeding_daily_limit_returns_429(client):
    """
    Once AI_DAILY_MESSAGE_LIMIT is exceeded, further messages
    are rejected with 429 without hitting the AI provider.

    Uses a dedicated mobile number (not the shared auth_headers
    fixture) so this farmer's message count starts at zero,
    regardless of what other tests ran earlier in the session.
    """

    headers = _login_isolated_user(client, mobile="9555512345")
    _create_farm_for_user(client, headers)

    with patch("app.config.settings.settings.AI_DAILY_MESSAGE_LIMIT", 2):
        first = client.post(
            "/v1/chat/message", json={"message": "msg one"}, headers=headers
        )
        assert first.status_code == 200

        second = client.post(
            "/v1/chat/message", json={"message": "msg two"}, headers=headers
        )
        assert second.status_code == 200

        third = client.post(
            "/v1/chat/message", json={"message": "msg three"}, headers=headers
        )
        assert third.status_code == 429