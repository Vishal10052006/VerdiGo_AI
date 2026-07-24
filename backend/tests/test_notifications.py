"""
Notification API Integration Tests

Tests:
- GET    /v1/notifications
- GET    /v1/notifications/unread-count
- PATCH  /v1/notifications/{notification_id}/read
- PATCH  /v1/notifications/read-all

Covers: auth requirement, farmer-profile requirement, ownership
isolation, unread-count correctness, idempotency of mark-all-read,
pagination boundaries, and the weather/disease auto-notify triggers.

Module:
Phase 1 → Module 9 → Notifications

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from uuid import uuid4
from unittest.mock import patch

from app.database.database import SessionLocal
from app.repositories import otp_repository
from app.models.notification import Notification
from app.enums.notification import NotificationTypeEnum, NotificationSeverityEnum


# ============================================================================
# Helpers
# ============================================================================

def _create_farm_for_user(client, headers, farm_name="Notif Test Farm"):
    """
    Ensure a farmer profile + farm exist for the given auth headers.
    Idempotent — mirrors the helper in test_crop_recommendation.py /
    test_chat.py so a dirty DB from earlier tests doesn't break this.
    """

    client.post(
        "/farmer/profile",
        json={
            "full_name": "Notif Test Farmer",
            "age": 30,
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

    if farm_response.status_code == 400:
        existing = client.get("/farm", headers=headers)
        assert existing.status_code == 200, existing.text
        return existing.json()["id"]

    assert False, (
        f"Unexpected farm creation response: "
        f"{farm_response.status_code} {farm_response.text}"
    )


def _login_second_user(client, mobile="9123456799"):
    """
    Logs in a distinct second user so ownership boundaries can be
    tested. Mirrors conftest.py's auth_headers logic exactly.
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


def _get_farmer_profile_id(mobile: str):
    """
    Directly resolve a farmer_profile_id from the DB by mobile —
    used to seed notifications without going through weather/disease
    flows for pure CRUD/pagination/isolation tests.
    """

    from app.repositories import user_repository, farmer_repository

    db = SessionLocal()
    try:
        user = user_repository.get_by_mobile(db=db, mobile=mobile)
        profile = farmer_repository.get_by_user_id(db=db, user_id=user.id)
        return profile.id
    finally:
        db.close()


def _seed_notification(
    farmer_profile_id,
    title="Test Alert",
    message="Test message",
    severity=NotificationSeverityEnum.HIGH,
    type=NotificationTypeEnum.WEATHER,
    is_read=False,
):
    """
    Directly inserts a notification row, bypassing the service layer.
    Used so pagination/isolation/mark-read tests don't depend on the
    weather/disease trigger paths being correct — those are tested
    separately below.
    """

    db = SessionLocal()
    try:
        notification = Notification(
            farmer_profile_id=farmer_profile_id,
            type=type,
            severity=severity,
            title=title,
            message=message,
            is_read=is_read,
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification.id
    finally:
        db.close()


# ============================================================================
# Auth Required
# ============================================================================

def test_get_notifications_requires_auth(client):
    response = client.get("/v1/notifications")
    assert response.status_code == 401


def test_unread_count_requires_auth(client):
    response = client.get("/v1/notifications/unread-count")
    assert response.status_code == 401


def test_mark_read_requires_auth(client):
    response = client.patch(f"/v1/notifications/{uuid4()}/read")
    assert response.status_code == 401


def test_mark_all_read_requires_auth(client):
    response = client.patch("/v1/notifications/read-all")
    assert response.status_code == 401


# ============================================================================
# Farmer Profile Not Found
# ============================================================================

def test_get_notifications_without_farmer_profile_returns_404(client):
    """
    A logged-in user with no farmer profile yet gets a clean 404,
    same pattern as chat and crop recommendation.
    """

    headers = _login_second_user(client, mobile="9988001122")

    response = client.get("/v1/notifications", headers=headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Farmer profile not found."


# ============================================================================
# Ownership Isolation
# ============================================================================

def test_notifications_list_only_returns_own_notifications(client, auth_headers):
    """
    A farmer must never see another farmer's notifications in the
    list response — regression test for the ownership boundary.
    """

    _create_farm_for_user(client, auth_headers)
    own_profile_id = _get_farmer_profile_id("8969367007")  # matches conftest auth_headers mobile
    _seed_notification(own_profile_id, title="My Own Alert")

    other_headers = _login_second_user(client, mobile="9123456701")
    _create_farm_for_user(client, other_headers, farm_name="Other Farm")
    other_profile_id = _get_farmer_profile_id("9123456701")
    _seed_notification(other_profile_id, title="Someone Else's Alert")

    response = client.get("/v1/notifications", headers=auth_headers)

    assert response.status_code == 200

    titles = [n["title"] for n in response.json()["data"]["notifications"]]
    assert "My Own Alert" in titles
    assert "Someone Else's Alert" not in titles


def test_mark_read_blocks_other_users_notification(client, auth_headers):
    """
    Attempting to mark someone else's notification as read must
    return 404, not 403 — avoids confirming the notification's
    existence to an unauthorized caller (same pattern as farm/chat).
    """

    other_headers = _login_second_user(client, mobile="9123456702")
    _create_farm_for_user(client, other_headers, farm_name="Isolation Farm")
    other_profile_id = _get_farmer_profile_id("9123456702")
    other_notification_id = _seed_notification(other_profile_id, title="Private Alert")

    _create_farm_for_user(client, auth_headers)

    response = client.patch(
        f"/v1/notifications/{other_notification_id}/read",
        headers=auth_headers,
    )

    assert response.status_code == 404


# ============================================================================
# Unread Count Correctness
# ============================================================================

def test_unread_count_decrements_after_mark_read(client, auth_headers):
    _create_farm_for_user(client, auth_headers)
    profile_id = _get_farmer_profile_id("8969367007")

    notif_id = _seed_notification(profile_id, title="Decrement Test")

    before = client.get("/v1/notifications/unread-count", headers=auth_headers)
    before_count = before.json()["data"]["unread_count"]
    assert before_count >= 1

    mark_response = client.patch(
        f"/v1/notifications/{notif_id}/read", headers=auth_headers
    )
    assert mark_response.status_code == 200
    assert mark_response.json()["data"]["is_read"] is True

    after = client.get("/v1/notifications/unread-count", headers=auth_headers)
    after_count = after.json()["data"]["unread_count"]

    assert after_count == before_count - 1


def test_marking_already_read_notification_is_a_noop(client, auth_headers):
    """
    Marking an already-read notification again must not double-count
    or error — repository guards on `if not notification.is_read`.
    """

    _create_farm_for_user(client, auth_headers)
    profile_id = _get_farmer_profile_id("8969367007")
    notif_id = _seed_notification(profile_id, title="Double Mark Test")

    first = client.patch(f"/v1/notifications/{notif_id}/read", headers=auth_headers)
    assert first.status_code == 200

    count_after_first = client.get(
        "/v1/notifications/unread-count", headers=auth_headers
    ).json()["data"]["unread_count"]

    second = client.patch(f"/v1/notifications/{notif_id}/read", headers=auth_headers)
    assert second.status_code == 200

    count_after_second = client.get(
        "/v1/notifications/unread-count", headers=auth_headers
    ).json()["data"]["unread_count"]

    assert count_after_first == count_after_second


# ============================================================================
# Mark All Read — Idempotency
# ============================================================================

def test_mark_all_read_is_idempotent(client, auth_headers):
    _create_farm_for_user(client, auth_headers)
    profile_id = _get_farmer_profile_id("8969367007")

    _seed_notification(profile_id, title="Bulk Alert 1")
    _seed_notification(profile_id, title="Bulk Alert 2")

    first = client.patch("/v1/notifications/read-all", headers=auth_headers)
    assert first.status_code == 200
    assert first.json()["data"]["marked_count"] >= 2

    # Second call should mark ZERO more — everything is already read
    second = client.patch("/v1/notifications/read-all", headers=auth_headers)
    assert second.status_code == 200
    assert second.json()["data"]["marked_count"] == 0

    unread = client.get(
        "/v1/notifications/unread-count", headers=auth_headers
    ).json()["data"]["unread_count"]
    assert unread == 0


# ============================================================================
# Pagination — No Cross-Farmer Leakage
# ============================================================================

def test_pagination_does_not_leak_other_farmers_rows(client, auth_headers):
    """
    Even with skip/limit, a farmer must never receive another
    farmer's notification rows by paging past their own count.
    """

    _create_farm_for_user(client, auth_headers)
    own_profile_id = _get_farmer_profile_id("8969367007")

    for i in range(3):
        _seed_notification(own_profile_id, title=f"Own Alert {i}")

    other_headers = _login_second_user(client, mobile="9123456703")
    _create_farm_for_user(client, other_headers, farm_name="Pagination Farm")
    other_profile_id = _get_farmer_profile_id("9123456703")
    _seed_notification(other_profile_id, title="Should Never Appear")

    # Page far beyond the caller's own notification count
    response = client.get(
        "/v1/notifications",
        params={"skip": 0, "limit": 100},
        headers=auth_headers,
    )

    assert response.status_code == 200
    titles = [n["title"] for n in response.json()["data"]["notifications"]]
    assert "Should Never Appear" not in titles


def test_pagination_respects_limit(client, auth_headers):
    _create_farm_for_user(client, auth_headers)
    profile_id = _get_farmer_profile_id("8969367007")

    for i in range(5):
        _seed_notification(profile_id, title=f"Limit Test {i}")

    response = client.get(
        "/v1/notifications",
        params={"skip": 0, "limit": 2},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]["notifications"]) == 2


# ============================================================================
# Weather Trigger — Severity Threshold
# ============================================================================

def test_high_severity_weather_advisory_creates_notification(client, auth_headers):
    """
    A HIGH/CRITICAL advisory must produce a notification row.
    We force HIGH temperature conditions via the advisory engine's
    real threshold rather than mocking, so this also guards against
    a future threshold-constant change silently breaking the trigger.
    """

    farm_id = _create_farm_for_user(client, auth_headers, farm_name="Weather Notif Farm")
    profile_id = _get_farmer_profile_id("8969367007")

    before_count = client.get(
        "/v1/notifications/unread-count", headers=auth_headers
    ).json()["data"]["unread_count"]

    # Force weather data through the normalizer path with a HIGH-temp
    # reading so generate_advisories() emits a "high" severity item.
    with patch(
        "app.services.weather_service.WeatherService.get_current_weather",
        return_value={
            "provider": "openmeteo",
            "temperature": 45,  # above HIGH_TEMPERATURE_THRESHOLD (40)
            "feels_like": None,
            "humidity": 40,
            "wind_speed": 5,
            "pressure": None,
            "visibility": None,
            "uv_index": None,
            "rainfall": 0,
            "condition": "Clear Sky",
            "fetched_at": "2026-07-24T10:00:00Z",
        },
    ):
        response = client.get(
            f"/v1/weather/advisory/{farm_id}",
            headers=auth_headers,
        )

    assert response.status_code == 200

    after_count = client.get(
        "/v1/notifications/unread-count", headers=auth_headers
    ).json()["data"]["unread_count"]

    assert after_count > before_count

    notifications = client.get(
        "/v1/notifications", headers=auth_headers
    ).json()["data"]["notifications"]

    assert any(n["type"] == "weather" and n["severity"] == "high" for n in notifications)


def test_low_severity_weather_advisory_does_not_create_notification(client, auth_headers):
    """
    Mild weather (no thresholds crossed) must NOT create a
    notification — only HIGH/CRITICAL advisories are notify-worthy.
    """

    farm_id = _create_farm_for_user(client, auth_headers, farm_name="Mild Weather Farm")

    before_count = client.get(
        "/v1/notifications/unread-count", headers=auth_headers
    ).json()["data"]["unread_count"]

    with patch(
        "app.services.weather_service.WeatherService.get_current_weather",
        return_value={
            "provider": "openmeteo",
            "temperature": 25,  # mild — no thresholds crossed
            "feels_like": None,
            "humidity": 50,
            "wind_speed": 5,
            "pressure": None,
            "visibility": None,
            "uv_index": None,
            "rainfall": 0,
            "condition": "Clear Sky",
            "fetched_at": "2026-07-24T10:00:00Z",
        },
    ):
        response = client.get(
            f"/v1/weather/advisory/{farm_id}",
            headers=auth_headers,
        )

    assert response.status_code == 200

    after_count = client.get(
        "/v1/notifications/unread-count", headers=auth_headers
    ).json()["data"]["unread_count"]

    assert after_count == before_count


# ============================================================================
# Disease Trigger — Confidence Threshold
# ============================================================================

def test_disease_detection_above_threshold_creates_notification(client, auth_headers, tmp_path):
    """
    A non-healthy detection with confidence >= MIN_CONFIDENCE_THRESHOLD
    must create a notification with the real detection.id attached.
    """

    farm_id = _create_farm_for_user(client, auth_headers, farm_name="Disease Notif Farm")

    before_count = client.get(
        "/v1/notifications/unread-count", headers=auth_headers
    ).json()["data"]["unread_count"]

    fake_image = tmp_path / "leaf.jpg"
    fake_image.write_bytes(b"\xff\xd8\xff\xe0fake-jpeg-bytes")

    with patch(
        "app.services.ai.gemini_vision_client.GeminiVisionClient.analyze_image",
        return_value={
            "result": {
                "is_healthy": False,
                "disease_name": "Leaf Blight",
                "confidence": 85,
                "severity": "high",
                "treatment": ["Apply recommended fungicide."],
                "prevention_tips": ["Ensure proper field drainage."],
                "crop_identified": "Wheat",
            },
            "tokens": 120,
        },
    ):
        with open(fake_image, "rb") as f:
            response = client.post(
                f"/v1/disease/detect/{farm_id}",
                files={"file": ("leaf.jpg", f, "image/jpeg")},
                headers=auth_headers,
            )

    assert response.status_code == 200
    detection_id = response.json()["data"]["id"]

    after_count = client.get(
        "/v1/notifications/unread-count", headers=auth_headers
    ).json()["data"]["unread_count"]

    assert after_count > before_count

    notifications = client.get(
        "/v1/notifications", headers=auth_headers
    ).json()["data"]["notifications"]

    disease_notifs = [n for n in notifications if n["type"] == "disease"]
    assert len(disease_notifs) >= 1
    # related_entity_id must point at the REAL saved detection, not None —
    # regression test for the detection.id-before-commit bug.
    assert any(n["related_entity_id"] == detection_id for n in disease_notifs)


def test_healthy_disease_detection_does_not_create_notification(client, auth_headers, tmp_path):
    """
    A healthy-plant result must not create a notification.
    """

    farm_id = _create_farm_for_user(client, auth_headers, farm_name="Healthy Plant Farm")

    before_count = client.get(
        "/v1/notifications/unread-count", headers=auth_headers
    ).json()["data"]["unread_count"]

    fake_image = tmp_path / "healthy.jpg"
    fake_image.write_bytes(b"\xff\xd8\xff\xe0fake-jpeg-bytes")

    with patch(
        "app.services.ai.gemini_vision_client.GeminiVisionClient.analyze_image",
        return_value={
            "result": {
                "is_healthy": True,
                "disease_name": None,
                "confidence": 95,
                "severity": "none",
                "treatment": [],
                "prevention_tips": ["Maintain regular watering schedule."],
                "crop_identified": "Wheat",
            },
            "tokens": 100,
        },
    ):
        with open(fake_image, "rb") as f:
            response = client.post(
                f"/v1/disease/detect/{farm_id}",
                files={"file": ("healthy.jpg", f, "image/jpeg")},
                headers=auth_headers,
            )

    assert response.status_code == 200

    after_count = client.get(
        "/v1/notifications/unread-count", headers=auth_headers
    ).json()["data"]["unread_count"]

    assert after_count == before_count


def test_low_confidence_disease_detection_does_not_create_notification(
    client, auth_headers, tmp_path
):
    """
    A non-healthy result BELOW MIN_CONFIDENCE_THRESHOLD is treated as
    inconclusive by the service and must not create a notification —
    we don't want to alarm a farmer over a low-confidence guess.
    """

    farm_id = _create_farm_for_user(client, auth_headers, farm_name="Low Confidence Farm")

    before_count = client.get(
        "/v1/notifications/unread-count", headers=auth_headers
    ).json()["data"]["unread_count"]

    fake_image = tmp_path / "blurry.jpg"
    fake_image.write_bytes(b"\xff\xd8\xff\xe0fake-jpeg-bytes")

    with patch(
        "app.services.ai.gemini_vision_client.GeminiVisionClient.analyze_image",
        return_value={
            "result": {
                "is_healthy": False,
                "disease_name": "Possible Rust",
                "confidence": 20,  # below MIN_CONFIDENCE_THRESHOLD (35)
                "severity": "moderate",
                "treatment": ["Consult local KVK."],
                "prevention_tips": ["Retake photo in better lighting."],
                "crop_identified": "Wheat",
            },
            "tokens": 90,
        },
    ):
        with open(fake_image, "rb") as f:
            response = client.post(
                f"/v1/disease/detect/{farm_id}",
                files={"file": ("blurry.jpg", f, "image/jpeg")},
                headers=auth_headers,
            )

    assert response.status_code == 200

    after_count = client.get(
        "/v1/notifications/unread-count", headers=auth_headers
    ).json()["data"]["unread_count"]

    assert after_count == before_count