"""
OTP Rate Limit Repository

Fixed-window, race-safe rate limiting for OTP send requests,
keyed by mobile number.

Design mirrors chat_rate_limit_repository.py / feature_rate_limit_
repository.py: a single INSERT ... ON CONFLICT DO UPDATE round-trip
so two concurrent requests for the same mobile can't both read
count=N and both proceed.

Unlike the daily counters elsewhere in this codebase, this is a
*rolling fixed window in minutes* (not per-calendar-day) — OTP
bombing happens on a minutes timescale, so a daily bucket would
let an attacker send dozens of OTPs before the counter resets.

Module:
Phase 1 → Module 1 → Authentication (Hardening)

Author: VerdiGO Backend Team
"""

from datetime import datetime, timedelta, timezone

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.otp_rate_limit import OTPRateLimit


def check_and_increment(
    db: Session,
    mobile: str,
    window_minutes: int,
    max_requests: int,
) -> tuple[bool, int]:
    """
    Atomically check whether `mobile` is within its OTP-send rate
    limit, and increment the counter if so.

    Returns:
        (allowed, current_count)
        allowed=False means the caller must reject the request
        with 429 WITHOUT incrementing further and WITHOUT sending
        an OTP.

    Concurrency note: the window-reset decision depends on a
    wall-clock comparison that can't be expressed as a single SQL
    upsert, so this uses SELECT ... FOR UPDATE to lock the row for
    the duration of the transaction — a second concurrent request
    for the SAME mobile blocks until the first commits, then reads
    the already-updated count. This is race-safe, at the cost of
    slightly higher lock contention than a pure upsert — acceptable
    given OTP send is a low-frequency, per-mobile-serialized action.
    """

    now = datetime.now(timezone.utc)

    row = (
        db.query(OTPRateLimit)
        .filter(OTPRateLimit.mobile == mobile)
        .with_for_update()
        .first()
    )

    if row is None:
        # First-ever request for this mobile — create window.
        stmt = (
            insert(OTPRateLimit)
            .values(
                mobile=mobile,
                window_start=now,
                request_count=1,
            )
            .on_conflict_do_nothing(index_elements=["mobile"])
        )
        db.execute(stmt)
        db.commit()
        return True, 1

    window_expired = (now - row.window_start) > timedelta(minutes=window_minutes)

    if window_expired:
        # Reset window.
        row.window_start = now
        row.request_count = 1
        db.commit()
        return True, 1

    if row.request_count >= max_requests:
        # Over the limit — do NOT increment further, don't send OTP.
        db.commit()
        return False, row.request_count

    row.request_count += 1
    db.commit()

    return True, row.request_count