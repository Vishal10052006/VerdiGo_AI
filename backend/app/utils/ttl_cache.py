"""
TTL Cache

Minimal thread-safe in-process cache with per-key expiry.

LIMITATION: this cache lives in a single process's memory. It is NOT
shared across multiple Gunicorn/Uvicorn workers or multiple deployed
instances — each process has its own independent cache. This is fine
for Phase 1 (single-instance Railway/Render deployment) but must be
replaced with Redis (or similar shared cache) before horizontally
scaling to multiple app instances, or a farmer could see stale data
from one instance while another instance has already invalidated it.
Tracked for Phase 2 infra work.

Module:
Shared Utility

Author: VerdiGO Backend Team
"""

# ============================================================================
# Imports
# ============================================================================

import time
import threading
from typing import Any


# ============================================================================
# TTL Cache
# ============================================================================

class TTLCache:
    """
    Simple key -> (value, expires_at) store with lazy expiry
    (checked on read, not via a background sweep).
    """

    def __init__(self):
        self._store: dict[str, tuple[Any, float]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------------
    # Get
    # ------------------------------------------------------------------------

    def get(self, key: str) -> Any | None:
        """
        Return the cached value for `key`, or None if missing/expired.
        """

        with self._lock:
            entry = self._store.get(key)

            if entry is None:
                return None

            value, expires_at = entry

            if time.monotonic() >= expires_at:
                del self._store[key]
                return None

            return value

    # ------------------------------------------------------------------------
    # Set
    # ------------------------------------------------------------------------

    def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        """
        Store `value` under `key`, expiring after `ttl_seconds`.
        """

        with self._lock:
            self._store[key] = (
                value,
                time.monotonic() + ttl_seconds,
            )

    # ------------------------------------------------------------------------
    # Invalidate
    # ------------------------------------------------------------------------

    def invalidate(self, key: str) -> None:
        """
        Remove a single key from the cache, if present.
        """

        with self._lock:
            self._store.pop(key, None)

    # ------------------------------------------------------------------------
    # Invalidate By Prefix
    # ------------------------------------------------------------------------

    def invalidate_prefix(self, prefix: str) -> None:
        """
        Remove all keys starting with `prefix`. Used when a farmer
        updates their profile/farm and every cached variant for that
        user (dashboard, overview, etc.) needs to drop at once.
        """

        with self._lock:
            keys_to_remove = [
                k for k in self._store if k.startswith(prefix)
            ]
            for k in keys_to_remove:
                del self._store[k]


# ============================================================================
# Module-Level Singleton
#
# One shared instance per process — imported wherever caching is needed.
# Deliberately not a per-request object; the whole point is persistence
# across requests within the same process.
# ============================================================================

dashboard_cache = TTLCache()