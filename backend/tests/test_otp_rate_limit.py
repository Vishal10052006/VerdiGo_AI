"""
OTP Send Rate Limit Tests

Regression test for the Module 1 security review finding:
/auth/send-otp had no request-level rate limit and could be used
to SMS-bomb a number or exhaust SMS provider budget.

Module:
Phase 1 → Module 1 → Authentication (Hardening)

Author: VerdiGO Backend Team
"""

from unittest.mock import patch

from app.database.database import SessionLocal
from sqlalchemy import text


def _clear_otp_rate_limits():
    db = SessionLocal()
    try:
        db.execute(text("DELETE FROM otp_rate_limits"))
        db.commit()
    finally:
        db.close()


def test_send_otp_within_limit_succeeds(client):
    _clear_otp_rate_limits()

    with patch("app.config.settings.settings.OTP_SEND_MAX_REQUESTS", 3), \
         patch("app.config.settings.settings.OTP_SEND_WINDOW_MINUTES", 10):

        for _ in range(3):
            response = client.post(
                "/auth/send-otp", json={"mobile": "9111111111"}
            )
            assert response.status_code == 200


def test_send_otp_exceeding_limit_returns_429(client):
    _clear_otp_rate_limits()

    with patch("app.config.settings.settings.OTP_SEND_MAX_REQUESTS", 2), \
         patch("app.config.settings.settings.OTP_SEND_WINDOW_MINUTES", 10):

        mobile = "9222222222"

        first = client.post("/auth/send-otp", json={"mobile": mobile})
        assert first.status_code == 200

        second = client.post("/auth/send-otp", json={"mobile": mobile})
        assert second.status_code == 200

        third = client.post("/auth/send-otp", json={"mobile": mobile})
        assert third.status_code == 429


def test_send_otp_rate_limit_is_per_mobile(client):
    """
    Rate limiting one mobile number must not block a different one —
    otherwise a single attacker could DoS all OTP sends platform-wide.
    """

    _clear_otp_rate_limits()

    with patch("app.config.settings.settings.OTP_SEND_MAX_REQUESTS", 1), \
         patch("app.config.settings.settings.OTP_SEND_WINDOW_MINUTES", 10):

        blocked_mobile = "9333333333"
        other_mobile = "9444444444"

        first = client.post("/auth/send-otp", json={"mobile": blocked_mobile})
        assert first.status_code == 200

        blocked = client.post("/auth/send-otp", json={"mobile": blocked_mobile})
        assert blocked.status_code == 429

        unaffected = client.post("/auth/send-otp", json={"mobile": other_mobile})
        assert unaffected.status_code == 200


def test_login_endpoint_also_rate_limited(client):
    """
    /auth/login shares login_user() with /auth/send-otp, so it must
    be covered by the same limit — otherwise an attacker just uses
    the other endpoint to bypass it.
    """

    _clear_otp_rate_limits()

    with patch("app.config.settings.settings.OTP_SEND_MAX_REQUESTS", 1), \
         patch("app.config.settings.settings.OTP_SEND_WINDOW_MINUTES", 10):

        mobile = "9555555555"

        first = client.post("/auth/login", json={"mobile": mobile})
        assert first.status_code == 200

        second = client.post("/auth/login", json={"mobile": mobile})
        assert second.status_code == 429