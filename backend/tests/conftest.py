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