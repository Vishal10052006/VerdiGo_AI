"""
Chat API Integration Tests

Tests:
- POST /v1/chat/message
- GET  /v1/chat/history/{conversation_id}
- GET  /v1/chat/conversations

Covers: auth requirement, ownership scoping (can't read another
farmer's conversation), happy-path message flow, conversation
continuation, and graceful provider-failure handling.

AI provider calls are mocked — these tests must never hit the
real Gemini/OpenAI APIs (cost, flakiness, and API keys shouldn't
be required to run the test suite / CI).

Module:
Phase 1 → Module 7 → AI Chat Assistant

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

from uuid import uuid4

import pytest

from app.database.database import SessionLocal
from app.repositories import otp_repository
from app.services.ai import ai_provider_manager as ai_provider_manager_module
from tests.conftest import FAKE_AI_REPLY


def _create_farm_for_user(client, headers, farm_name="Test Farm"):
    """
    Ensure a farmer profile + farm exist for the given auth headers.
    Mirrors the helper in test_crop_recommendation.py — idempotent,
    reuses existing profile/farm on a dirty DB.
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


def _login_second_user(client, mobile="9123456790"):
    """
    Logs in a distinct second user so ownership boundaries can be
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

def test_send_message_requires_auth(client):
    """
    Request without a JWT token must fail.
    """

    response = client.post(
        "/v1/chat/message",
        json={"message": "What should I plant this season?"},
    )

    assert response.status_code == 401


def test_get_history_requires_auth(client):
    conversation_id = uuid4()

    response = client.get(f"/v1/chat/history/{conversation_id}")

    assert response.status_code == 401


def test_list_conversations_requires_auth(client):
    response = client.get("/v1/chat/conversations")

    assert response.status_code == 401


# ============================================================================
# Farmer Profile Not Found
# ============================================================================

def test_send_message_without_farmer_profile_returns_404(client):
    """
    A logged-in user with no farmer profile yet should get a clean
    404, not a 500 — chat depends on farmer context existing.
    """

    headers = _login_second_user(client, mobile="9988776600")

    response = client.post(
        "/v1/chat/message",
        json={"message": "Hello"},
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Farmer profile not found."


# ============================================================================
# Happy Path — Send Message (New Conversation)
# ============================================================================

def test_send_message_creates_new_conversation(client, auth_headers):
    """
    Sending a message with no conversation_id creates a new
    conversation and returns the AI's (mocked) reply.
    """

    _create_farm_for_user(client, auth_headers)

    response = client.post(
        "/v1/chat/message",
        json={"message": "What should I plant this season?"},
        headers=auth_headers,
    )

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True

    data = body["data"]
    assert data["conversation_id"] is not None

    message = data["message"]
    assert message["role"] == "assistant"
    assert message["content"] == FAKE_AI_REPLY
    assert message["ai_provider"] == "gemini"


# ============================================================================
# Happy Path — Continue Existing Conversation
# ============================================================================

def test_send_message_continues_existing_conversation(client, auth_headers):
    """
    Passing a conversation_id from a prior message appends to the
    same conversation rather than creating a new one.
    """

    _create_farm_for_user(client, auth_headers)

    first = client.post(
        "/v1/chat/message",
        json={"message": "What crop suits black soil?"},
        headers=auth_headers,
    )
    assert first.status_code == 200
    conversation_id = first.json()["data"]["conversation_id"]

    second = client.post(
        "/v1/chat/message",
        json={
            "conversation_id": conversation_id,
            "message": "And what about fertilizer for it?",
        },
        headers=auth_headers,
    )

    assert second.status_code == 200
    assert second.json()["data"]["conversation_id"] == conversation_id


# ============================================================================
# Message Validation
# ============================================================================

def test_send_empty_message_is_rejected(client, auth_headers):
    _create_farm_for_user(client, auth_headers)

    response = client.post(
        "/v1/chat/message",
        json={"message": "   "},
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_send_oversized_message_is_rejected(client, auth_headers):
    _create_farm_for_user(client, auth_headers)

    response = client.post(
        "/v1/chat/message",
        json={"message": "a" * 1001},
        headers=auth_headers,
    )

    assert response.status_code == 422


# ============================================================================
# Chat History
# ============================================================================

def test_get_history_returns_messages_in_order(client, auth_headers):
    _create_farm_for_user(client, auth_headers)

    send_response = client.post(
        "/v1/chat/message",
        json={"message": "How much water does wheat need?"},
        headers=auth_headers,
    )
    conversation_id = send_response.json()["data"]["conversation_id"]

    history_response = client.get(
        f"/v1/chat/history/{conversation_id}",
        headers=auth_headers,
    )

    assert history_response.status_code == 200

    messages = history_response.json()["data"]["messages"]
    assert len(messages) == 2  # user message + assistant reply

    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"


def test_get_history_nonexistent_conversation_returns_404(client, auth_headers):
    _create_farm_for_user(client, auth_headers)

    response = client.get(
        f"/v1/chat/history/{uuid4()}",
        headers=auth_headers,
    )

    assert response.status_code == 404


# ============================================================================
# Security — Cannot Read Another User's Conversation
# ============================================================================

def test_cannot_access_other_users_conversation_history(client, auth_headers):
    """
    A conversation belonging to a DIFFERENT farmer must return 404,
    not the message data and not a 403 (which would confirm the
    conversation's existence to an attacker). Same ownership
    pattern as the crop recommendation module.
    """

    other_headers = _login_second_user(client, mobile="9123456791")
    _create_farm_for_user(client, other_headers, farm_name="Other User's Farm")

    other_send = client.post(
        "/v1/chat/message",
        json={"message": "Private question about my farm"},
        headers=other_headers,
    )
    other_conversation_id = other_send.json()["data"]["conversation_id"]

    response = client.get(
        f"/v1/chat/history/{other_conversation_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_cannot_continue_other_users_conversation(client, auth_headers):
    """
    Attempting to send a message using someone else's
    conversation_id must not succeed and must not leak whether
    that conversation exists.
    """

    other_headers = _login_second_user(client, mobile="9123456792")
    _create_farm_for_user(client, other_headers, farm_name="Yet Another Farm")

    other_send = client.post(
        "/v1/chat/message",
        json={"message": "Should stay private"},
        headers=other_headers,
    )
    other_conversation_id = other_send.json()["data"]["conversation_id"]

    _create_farm_for_user(client, auth_headers)

    response = client.post(
        "/v1/chat/message",
        json={
            "conversation_id": other_conversation_id,
            "message": "Trying to hijack this conversation",
        },
        headers=auth_headers,
    )

    assert response.status_code == 404


# ============================================================================
# List Conversations
# ============================================================================

def test_list_conversations_returns_only_own_conversations(client, auth_headers):
    _create_farm_for_user(client, auth_headers)

    client.post(
        "/v1/chat/message",
        json={"message": "First conversation"},
        headers=auth_headers,
    )

    other_headers = _login_second_user(client, mobile="9123456793")
    _create_farm_for_user(client, other_headers, farm_name="Isolated Farm")
    client.post(
        "/v1/chat/message",
        json={"message": "Should not appear in the first user's list"},
        headers=other_headers,
    )

    response = client.get("/v1/chat/conversations", headers=auth_headers)

    assert response.status_code == 200

    conversations = response.json()["data"]
    assert isinstance(conversations, list)
    assert len(conversations) >= 1

    titles = [c["title"] for c in conversations]
    assert "Should not appear in the first user's list" not in titles


# ============================================================================
# Provider Failure Handling
# ============================================================================

def test_send_message_when_ai_provider_raises_returns_502(client, auth_headers, monkeypatch):
    """
    If both Gemini and OpenAI fail (simulated here by making
    generate_response raise), the API should surface a clean
    error rather than a raw 500 stack trace to the farmer.

    NOTE: this test documents EXPECTED behavior. If it's currently
    failing, it means the graceful-failure handling flagged in the
    tracker ("both AI providers down") hasn't been implemented in
    ChatService yet — that's the next task, not a test bug.
    """

    def _raise(*args, **kwargs):
        raise ConnectionError("Both Gemini and OpenAI are unreachable")

    monkeypatch.setattr(
        ai_provider_manager_module.AIProviderManager,
        "generate_response",
        _raise,
    )

    _create_farm_for_user(client, auth_headers)

    response = client.post(
        "/v1/chat/message",
        json={"message": "Is it going to rain tomorrow?"},
        headers=auth_headers,
    )

    # Expect a handled error (502/503), not an unhandled 500.
    assert response.status_code in (502, 503)