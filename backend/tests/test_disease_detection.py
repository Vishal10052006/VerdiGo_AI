"""
Disease Detection API Integration Tests

Tests:
- POST /v1/disease/detect/{farm_id}
- GET  /v1/disease/history/{farm_id}
- GET  /v1/disease/details/{detection_id}

Mirrors test_crop_recommendation.py's structure: auth, ownership
scoping, validation, happy path, and the disease-specific paths
(low confidence override, rate limit, vision failure).

Module: Phase 1 → Module 8 → Disease Detection
Author: VerdiGO Backend Team
"""

import io
import time
from unittest.mock import patch
from uuid import uuid4

import httpx
import pytest

from app.database.database import SessionLocal
from app.repositories import otp_repository
from tests.conftest import FAKE_VISION_RESULT


# ============================================================================
# Helpers
# ============================================================================

def _create_farm_for_user(client, headers, farm_name="Disease Test Farm"):
    client.post(
        "/farmer/profile",
        json={
            "full_name": "Disease Test Farmer",
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

    if farm_response.status_code == 400:
        existing = client.get("/farm", headers=headers)
        assert existing.status_code == 200, existing.text
        return existing.json()["id"]

    assert False, f"Unexpected farm creation response: {farm_response.status_code} {farm_response.text}"


def _login_second_user(client, mobile="9123456799"):
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

    return {"Authorization": f"Bearer {otp_response.json()['access_token']}"}


def _fake_image_file(name="leaf.jpg", content=b"fake-image-bytes"):
    return {"file": (name, io.BytesIO(content), "image/jpeg")}


# ============================================================================
# Auth Required
# ============================================================================

def test_detect_requires_auth(client):
    response = client.post(
        f"/v1/disease/detect/{uuid4()}", files=_fake_image_file()
    )
    assert response.status_code == 401


def test_history_requires_auth(client):
    response = client.get(f"/v1/disease/history/{uuid4()}")
    assert response.status_code == 401


# ============================================================================
# Farm Not Found
# ============================================================================

def test_detect_farm_not_found(client, auth_headers):
    response = client.post(
        "/v1/disease/detect/00000000-0000-0000-0000-000000000000",
        files=_fake_image_file(),
        headers=auth_headers,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Farm not found."


# ============================================================================
# Validation
# ============================================================================

def test_detect_rejects_unsupported_extension(client, auth_headers):
    farm_id = _create_farm_for_user(client, auth_headers)

    response = client.post(
        f"/v1/disease/detect/{farm_id}",
        files=_fake_image_file(name="leaf.gif"),
        headers=auth_headers,
    )
    assert response.status_code == 400


def test_detect_rejects_empty_file(client, auth_headers):
    farm_id = _create_farm_for_user(client, auth_headers)

    response = client.post(
        f"/v1/disease/detect/{farm_id}",
        files=_fake_image_file(content=b""),
        headers=auth_headers,
    )
    assert response.status_code == 400


def test_detect_rejects_oversized_file(client, auth_headers):
    farm_id = _create_farm_for_user(client, auth_headers)
    oversized = b"x" * (9 * 1024 * 1024)  # 9MB > 8MB limit

    response = client.post(
        f"/v1/disease/detect/{farm_id}",
        files=_fake_image_file(content=oversized),
        headers=auth_headers,
    )
    assert response.status_code == 400


# ============================================================================
# Happy Path
# ============================================================================

def test_detect_returns_diagnosis(client, auth_headers):
    farm_id = _create_farm_for_user(client, auth_headers)

    response = client.post(
        f"/v1/disease/detect/{farm_id}",
        files=_fake_image_file(),
        headers=auth_headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True

    data = body["data"]
    assert data["disease_name"] == FAKE_VISION_RESULT["disease_name"]
    assert data["severity"] == FAKE_VISION_RESULT["severity"]
    assert data["is_healthy"] is False
    assert len(data["treatment"]) > 0
    assert data["image_url"] is not None


# ============================================================================
# Low Confidence Override
# ============================================================================

def test_detect_low_confidence_marked_inconclusive(client, auth_headers, monkeypatch):
    farm_id = _create_farm_for_user(client, auth_headers)

    low_confidence_result = dict(FAKE_VISION_RESULT, confidence=10.0)

    def _fake_low_confidence(self, image_bytes, mime_type):
        return {"result": low_confidence_result, "tokens": 100}

    monkeypatch.setattr(
        "app.services.ai.gemini_vision_client.GeminiVisionClient.analyze_image",
        _fake_low_confidence,
    )

    response = client.post(
        f"/v1/disease/detect/{farm_id}",
        files=_fake_image_file(),
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert "Inconclusive" in data["disease_name"]


# ============================================================================
# Vision Service Failure
# ============================================================================

def test_detect_returns_503_when_vision_unavailable(client, auth_headers, monkeypatch):
    farm_id = _create_farm_for_user(client, auth_headers)

    def _raise_timeout(self, image_bytes, mime_type):
        raise httpx.TimeoutException("Gemini Vision timed out")

    monkeypatch.setattr(
        "app.services.ai.gemini_vision_client.GeminiVisionClient.analyze_image",
        _raise_timeout,
    )

    response = client.post(
        f"/v1/disease/detect/{farm_id}",
        files=_fake_image_file(),
        headers=auth_headers,
    )

    assert response.status_code == 503


# ============================================================================
# Rate Limiting
# ============================================================================

def test_detect_exceeding_daily_limit_returns_429(client):
    unique_mobile = f"9{int(time.time()) % 1000000000}"
    headers = _login_second_user(client, mobile=unique_mobile)
    farm_id = _create_farm_for_user(client, headers, farm_name="Rate Limit Farm")

    with patch("app.config.settings.settings.AI_DAILY_VISION_LIMIT", 1):
        first = client.post(
            f"/v1/disease/detect/{farm_id}", files=_fake_image_file(), headers=headers
        )
        assert first.status_code == 200

        second = client.post(
            f"/v1/disease/detect/{farm_id}", files=_fake_image_file(), headers=headers
        )
        assert second.status_code == 429


# ============================================================================
# Security — Cannot Access Another User's Farm
# ============================================================================

def test_detect_blocks_other_users_farm(client, auth_headers):
    other_headers = _login_second_user(client, mobile="9123456798")
    other_farm_id = _create_farm_for_user(
        client, other_headers, farm_name="Other User's Farm"
    )

    response = client.post(
        f"/v1/disease/detect/{other_farm_id}",
        files=_fake_image_file(),
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Farm not found."


# ============================================================================
# History
# ============================================================================

def test_history_returns_ordered_detections(client, auth_headers):
    farm_id = _create_farm_for_user(client, auth_headers, farm_name="History Farm")

    client.post(
        f"/v1/disease/detect/{farm_id}", files=_fake_image_file(), headers=auth_headers
    )
    client.post(
        f"/v1/disease/detect/{farm_id}", files=_fake_image_file(), headers=auth_headers
    )

    response = client.get(f"/v1/disease/history/{farm_id}", headers=auth_headers)

    assert response.status_code == 200
    detections = response.json()["data"]["detections"]
    assert len(detections) >= 2

    timestamps = [d["created_at"] for d in detections]
    assert timestamps == sorted(timestamps, reverse=True)


def test_history_blocks_other_users_farm(client, auth_headers):
    other_headers = _login_second_user(client, mobile="9123456797")
    other_farm_id = _create_farm_for_user(
        client, other_headers, farm_name="History Security Farm"
    )

    response = client.get(f"/v1/disease/history/{other_farm_id}", headers=auth_headers)
    assert response.status_code == 404


# ============================================================================
# Detection Details
# ============================================================================

def test_details_blocks_other_users_detection(client, auth_headers):
    other_headers = _login_second_user(client, mobile="9123456796")
    other_farm_id = _create_farm_for_user(
        client, other_headers, farm_name="Details Security Farm"
    )

    detect_response = client.post(
        f"/v1/disease/detect/{other_farm_id}",
        files=_fake_image_file(),
        headers=other_headers,
    )
    other_detection_id = detect_response.json()["data"]["id"]

    response = client.get(
        f"/v1/disease/details/{other_detection_id}", headers=auth_headers
    )
    assert response.status_code == 404