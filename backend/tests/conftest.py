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