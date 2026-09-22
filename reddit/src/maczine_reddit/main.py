"""Entry point: feed -> newest current article -> duplicate check -> submit."""

from __future__ import annotations

import logging
import os
import sys
from datetime import datetime, timezone
from enum import Enum

import requests

from maczine_reddit import rss
from maczine_reddit.config import Config, ConfigError, load_config
from maczine_reddit.reddit import (
    AlreadySubmitted,
    RedditAuthError,
    RedditClient,
    RedditRateLimited,
    RedditRejected,
    RedditUnavailable,
)

log = logging.getLogger("maczine_reddit")


class Outcome(Enum):
    """Result of one run, and the process exit code it maps to."""

    POSTED = ("SUCCESS", "new article posted", 0)
    ALREADY_POSTED = ("NOOP", "article already posted", 0)
    NO_NEW_ARTICLE = ("NOOP", "no sufficiently new article available", 0)
    DRY_RUN = ("NOOP", "dry run, nothing submitted", 0)
    CONFIG = ("ERROR", "configuration invalid", 2)
    RSS_UNAVAILABLE = ("ERROR", "RSS unavailable", 10)
    RSS_MALFORMED = ("ERROR", "malformed RSS", 11)
    REDDIT_AUTH = ("ERROR", "Reddit authentication failed", 20)
    REDDIT_REJECTED = ("ERROR", "Reddit rejected the request", 21)
    RATE_LIMITED = ("ERROR", "rate limited", 22)
    REDDIT_UNAVAILABLE = ("ERROR", "Reddit unavailable", 23)
    UNEXPECTED = ("ERROR", "unexpected exception", 1)

    def __init__(self, kind: str, label: str, exit_code: int) -> None:
        self.kind = kind
        self.label = label
        self.exit_code = exit_code


class RedactSecrets(logging.Filter):
    """Belt and braces: scrub known secret values from every log record."""

    def __init__(self, secrets: tuple[str, ...]) -> None:
        super().__init__()
        self._secrets = tuple(s for s in secrets if len(s) >= 4)

    def filter(self, record: logging.LogRecord) -> bool:
        if self._secrets:
            message = record.getMessage()
            if record.exc_info:
                # Tracebacks can carry request data; flatten them so they are scrubbed too.
                message += "\n" + logging.Formatter().formatException(record.exc_info)
                record.exc_info, record.exc_text = None, None
            for secret in self._secrets:
                message = message.replace(secret, "[REDACTED]")
            record.msg, record.args = message, None
        return True


def run(cfg: Config, session: requests.Session, now: datetime | None = None) -> Outcome:
    now = now or datetime.now(timezone.utc)

    log.info("Fetching MacZine RSS: %s", cfg.feed_url)
    try:
        articles = rss.parse_feed(rss.fetch_feed(session, cfg.feed_url))
        article = rss.select_latest(articles, now, cfg.max_age_hours)
    except rss.FeedUnavailable as exc:
        log.error("RSS unavailable: %s", exc)
        return Outcome.RSS_UNAVAILABLE
    except rss.FeedMalformed as exc:
        log.error("Malformed RSS: %s", exc)
        return Outcome.RSS_MALFORMED

    if article is None:
        log.info("No sufficiently new article available; no action required.")
        return Outcome.NO_NEW_ARTICLE

    log.info("Latest article:\n  Title: %s\n  URL: %s\n  Published: %s",
             article.title, article.url, article.published.isoformat())

    if cfg.dry_run and not cfg.has_reddit_credentials:
        log.info("Reddit credentials not configured; skipping duplicate check.")
        _print_dry_run(cfg, article, checked=False)
        return Outcome.DRY_RUN

    client = RedditClient(session, cfg)
    try:
        client.authenticate()
        log.info("Checking Reddit for existing submission...")
        existing = client.find_existing(article.url)
        if existing:
            log.info("Article already posted; no action required.\n  Reddit URL: %s", existing)
            return Outcome.ALREADY_POSTED
        log.info("No existing submission found.")

        if cfg.dry_run:
            _print_dry_run(cfg, article, checked=True)
            return Outcome.DRY_RUN

        log.info("Submitting article to r/%s...", cfg.subreddit)
        try:
            permalink = client.submit_link(article.title, article.url)
        except AlreadySubmitted:
            log.info("Article already posted; no action required. (Reddit reported ALREADY_SUB)")
            return Outcome.ALREADY_POSTED
        log.info("Reddit submission successful.\n  Reddit URL: %s", permalink)
        _summary(f"Posted [{article.title}]({article.url}) to r/{cfg.subreddit}: {permalink}")
        return Outcome.POSTED
    except RedditAuthError as exc:
        log.error("Reddit authentication failed: %s", exc)
        return Outcome.REDDIT_AUTH
    except RedditRateLimited as exc:
        log.error("Rate limited by Reddit: %s", exc)
        return Outcome.RATE_LIMITED
    except RedditRejected as exc:
        log.error("Reddit rejected the request: %s", exc)
        return Outcome.REDDIT_REJECTED
    except RedditUnavailable as exc:
        log.error("Reddit unavailable: %s", exc)
        return Outcome.REDDIT_UNAVAILABLE


def _print_dry_run(cfg: Config, article: rss.Article, checked: bool) -> None:
    destination = f"r/{cfg.subreddit}" if cfg.subreddit else "(REDDIT_SUBREDDIT not set)"
    log.info(
        "DRY RUN\n\nArticle:\n  \"%s\"\n\nURL:\n  %s\n\nDestination:\n  %s\n\nDuplicate check: %s\n\n"
        "No Reddit submission performed.",
        article.title, article.url, destination,
        "performed, none found" if checked else "skipped (no credentials)",
    )


def _summary(line: str) -> None:
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")


def cli() -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
    try:
        cfg = load_config()
    except ConfigError as exc:
        log.error("Configuration error: %s", exc)
        outcome = Outcome.CONFIG
    else:
        for handler in logging.getLogger().handlers:
            handler.addFilter(RedactSecrets(cfg.secrets))
        log.info("Mode: %s", "DRY RUN" if cfg.dry_run else "LIVE")
        try:
            with requests.Session() as session:
                outcome = run(cfg, session)
        except Exception:  # noqa: BLE001 - last line of defence; report and fail
            log.exception("Unexpected error")
            outcome = Outcome.UNEXPECTED
    result = f"RESULT={outcome.name} ({outcome.kind}: {outcome.label})"
    log.info(result)
    _summary(f"**{result}**")
    return outcome.exit_code
