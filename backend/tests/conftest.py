"""
Pytest Configuration

Shared fixtures for Weather Intelligence API tests.

Responsibilities:
- Test client
- Database session
- Authentication helpers

Module:
Phase 1 → Module 5 → T5.4 Testing

Author: VerdiGO Backend Team
"""
import os
from dotenv import load_dotenv

from sqlalchemy import text

load_dotenv(".env.test", override=True)

# ============================================================================
# Imports
# ============================================================================

import pytest
from app.enums.chat import AIProviderEnum
from app.services.ai import ai_provider_manager as ai_provider_manager_module

from fastapi.testclient import TestClient

from app.main import app

import uuid

from app.database.database import SessionLocal
from app.repositories import otp_repository

from unittest.mock import patch

# ============================================================================
# Test Client
# ============================================================================

@pytest.fixture
def client():
    """
    Return FastAPI TestClient.
    """

    return TestClient(app)


@pytest.fixture
def auth_headers(client):
    """
    Login and return JWT headers.
    """

    mobile = "8969367007"

    login = client.post(
        "/auth/login",
        json={
            "mobile": mobile,
        },
    )

    assert login.status_code == 200

    # Read latest OTP from database
    db = SessionLocal()

    latest_otp = otp_repository.get_latest(
        db=db,
        mobile=mobile,
    )

    db.close()

    otp = client.post(
        "/auth/verify-otp",
        json={
            "mobile": mobile,
            "otp": latest_otp.otp,
        },
    )

    assert otp.status_code == 200

    token = otp.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }

FAKE_AI_REPLY = "Based on your soil and season, irrigate every 5-7 days."

@pytest.fixture(autouse=True)
def mock_ai_provider(monkeypatch):
    """
    Replace AIProviderManager.generate_response with a stub so tests
    never call real Gemini/OpenAI APIs. Autouse — applies to every
    test in this file without needing to be requested explicitly.

    Lives in conftest.py (not test_chat.py) so it's shared across
    ALL test files in this session, including test_chat_rate_limit.py.
    """

    def _fake_generate_response(self, system_prompt, history, user_message):
        return {
            "text": FAKE_AI_REPLY,
            "tokens": 42,
            "provider": AIProviderEnum.GEMINI,
            "response_time_ms": 250,
        }

    monkeypatch.setattr(
        ai_provider_manager_module.AIProviderManager,
        "generate_response",
        _fake_generate_response,
    )

FAKE_VISION_RESULT = {
    "is_healthy": False,
    "disease_name": "Leaf Blight",
    "confidence": 87.0,
    "severity": "moderate",
    "treatment": ["Apply copper-based fungicide.", "Remove affected leaves."],
    "prevention_tips": ["Avoid overhead watering.", "Ensure good air circulation."],
    "crop_identified": "Tomato",
}


@pytest.fixture(autouse=True)
def mock_gemini_vision(monkeypatch):
    """
    Stub GeminiVisionClient.analyze_image so disease/pest detection
    tests never call real Gemini Vision (cost + flakiness).
    """
    def _fake_analyze_image(self, image_bytes, mime_type):
        return {"result": dict(FAKE_VISION_RESULT), "tokens": 120}

    monkeypatch.setattr(
        "app.services.ai.gemini_vision_client.GeminiVisionClient.analyze_image",
        _fake_analyze_image,
    )


@pytest.fixture(autouse=True)
def _reset_daily_rate_limits():
    """
    Reset per-farmer daily usage counters before every test.

    Autouse so no test file has to remember to request it — matches the
    pattern already used by mock_ai_provider / mock_gemini_vision above.
    """
    db = SessionLocal()
    try:
        db.execute(text("DELETE FROM feature_rate_limits"))
        db.execute(text("DELETE FROM chat_rate_limits"))
        db.commit()
    finally:
        db.close()

    yield