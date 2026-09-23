"""Bounded exponential backoff shared by the feed and Reddit clients."""

from __future__ import annotations

import logging
import time

log = logging.getLogger(__name__)

ATTEMPTS = 4          # first try + 3 retries
BASE_DELAY = 2.0      # 2s, 4s, 8s
MAX_DELAY = 60.0
TIMEOUT = 15          # seconds, every HTTP request


def delay_for(attempt: int, hint: float | None = None) -> float:
    """Seconds to wait before retry number `attempt` (1-based). A server hint
    (Retry-After) wins when it is longer, but never beyond MAX_DELAY."""
    backoff = BASE_DELAY * (2 ** (attempt - 1))
    if hint is not None and hint > backoff:
        backoff = hint
    return min(backoff, MAX_DELAY)


def wait(attempt: int, reason: str, hint: float | None = None) -> None:
    seconds = delay_for(attempt, hint)
    log.warning("%s; retrying in %.0fs (attempt %d of %d)", reason, seconds, attempt + 1, ATTEMPTS)
    sleep(seconds)


def sleep(seconds: float) -> None:  # patched in tests
    time.sleep(seconds)
