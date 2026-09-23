"""Configuration, read once from the environment."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Mapping

DEFAULT_FEED_URL = "https://www.mactechsolutionsllc.com/maczine/feed.xml"
DEFAULT_MAX_AGE_HOURS = 36.0

# Needed to talk to Reddit at all. A live run requires every one of them;
# a dry run uses them if present and otherwise skips the duplicate check.
REDDIT_KEYS = (
    "REDDIT_CLIENT_ID",
    "REDDIT_CLIENT_SECRET",
    "REDDIT_REFRESH_TOKEN",
    "REDDIT_USERNAME",
    "REDDIT_SUBREDDIT",
)

_TRUE = {"1", "true", "yes", "on"}
_FALSE = {"0", "false", "no", "off", ""}


class ConfigError(Exception):
    """Configuration is missing or invalid. Messages name keys, never values."""


@dataclass(frozen=True)
class Config:
    dry_run: bool
    feed_url: str = DEFAULT_FEED_URL
    max_age_hours: float = DEFAULT_MAX_AGE_HOURS
    client_id: str = field(default="", repr=False)
    client_secret: str = field(default="", repr=False)
    refresh_token: str = field(default="", repr=False)
    username: str = ""
    subreddit: str = ""
    flair_id: str = ""

    @property
    def has_reddit_credentials(self) -> bool:
        return all(
            (self.client_id, self.client_secret, self.refresh_token, self.username, self.subreddit)
        )

    @property
    def secrets(self) -> tuple[str, ...]:
        """Values that must never reach a log line."""
        return tuple(s for s in (self.client_id, self.client_secret, self.refresh_token) if s)


def _bool(env: Mapping[str, str], key: str, default: bool) -> bool:
    raw = env.get(key)
    if raw is None:
        return default
    value = raw.strip().lower()
    if value in _TRUE:
        return True
    if value in _FALSE:
        return False
    raise ConfigError(f"{key} must be true or false")


def _subreddit(raw: str) -> str:
    name = raw.strip().strip("/")
    for prefix in ("r/", "R/"):
        if name.startswith(prefix):
            name = name[len(prefix):]
    return name


def load_config(env: Mapping[str, str] | None = None) -> Config:
    env = os.environ if env is None else env
    # Default to dry run: a misconfigured environment should never post.
    dry_run = _bool(env, "DRY_RUN", default=True)

    raw_age = env.get("MAX_ARTICLE_AGE_HOURS", "").strip()
    try:
        max_age = float(raw_age) if raw_age else DEFAULT_MAX_AGE_HOURS
    except ValueError:
        raise ConfigError("MAX_ARTICLE_AGE_HOURS must be a number") from None
    if not 0 < max_age <= 24 * 7:
        raise ConfigError("MAX_ARTICLE_AGE_HOURS must be between 0 and 168")

    values = {k: env.get(k, "").strip() for k in REDDIT_KEYS}
    if not dry_run:
        missing = [k for k, v in values.items() if not v]
        if missing:
            raise ConfigError("missing required configuration: " + ", ".join(missing))

    return Config(
        dry_run=dry_run,
        feed_url=env.get("FEED_URL", "").strip() or DEFAULT_FEED_URL,
        max_age_hours=max_age,
        client_id=values["REDDIT_CLIENT_ID"],
        client_secret=values["REDDIT_CLIENT_SECRET"],
        refresh_token=values["REDDIT_REFRESH_TOKEN"],
        username=values["REDDIT_USERNAME"].removeprefix("u/").removeprefix("/u/"),
        subreddit=_subreddit(values["REDDIT_SUBREDDIT"]),
        flair_id=env.get("REDDIT_FLAIR_ID", "").strip(),
    )
