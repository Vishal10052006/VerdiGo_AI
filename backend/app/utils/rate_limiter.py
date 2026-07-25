"""
Simple In-Process Rate Limiter (Sliding Window)

Same single-instance limitation as utils/ttl_cache.py — this is NOT
shared across multiple app instances/workers. For Phase 1's single
deployed instance this is a real, functioning throttle; before scaling
to multiple instances, replace with a Redis-backed limiter (e.g.
sliding-window counter via Redis INCR + EXPIRE) so the limit is
enforced globally, not per-process.

Module:
Shared Utility

Author: VerdiGO Backend Team
"""

import time
import threading


class SlidingWindowRateLimiter:
    """
    Tracks timestamps of recent actions per key. `is_allowed()` prunes
    timestamps older than the window, then checks if the remaining
    count is still under the limit.
    """

    def __init__(self):
        self._store: dict[str, list[float]] = {}
        self._lock = threading.Lock()

    def is_allowed(self, key: str, max_calls: int, window_seconds: int) -> bool:
        """
        Returns True and records this call if under the limit,
        False (and does NOT record) if the limit is already reached —
        so a blocked attempt doesn't itself count toward future windows.
        """

        now = time.monotonic()
        cutoff = now - window_seconds

        with self._lock:
            timestamps = self._store.get(key, [])
            timestamps = [t for t in timestamps if t > cutoff]

            if len(timestamps) >= max_calls:
                self._store[key] = timestamps
                return False

            timestamps.append(now)
            self._store[key] = timestamps
            return True

    def seconds_until_next_allowed(self, key: str, window_seconds: int) -> int:
        """
        Best-effort estimate of how long until the oldest recorded
        timestamp ages out of the window — used to build a helpful
        "try again in N seconds" message.
        """

        with self._lock:
            timestamps = self._store.get(key, [])
            if not timestamps:
                return 0

            oldest = min(timestamps)
            remaining = window_seconds - (time.monotonic() - oldest)
            return max(0, int(remaining))


# Module-level singletons — one shared limiter per concern, so OTP-send
# throttling and admin-login throttling (added below) don't share state.
otp_send_limiter = SlidingWindowRateLimiter()
admin_login_limiter = SlidingWindowRateLimiter()