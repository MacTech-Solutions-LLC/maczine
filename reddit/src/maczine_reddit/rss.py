"""Fetch and parse the MacZine RSS feed, and pick the article to post."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from xml.etree.ElementTree import Element, ParseError

import requests
from defusedxml import ElementTree
from defusedxml.common import DefusedXmlException

from maczine_reddit import retry
from maczine_reddit.urls import canonical_url, is_maczine_article

log = logging.getLogger(__name__)

# A feed stamped a little ahead of the runner's clock is fine; anything
# further out is not "published" and is not posted.
FUTURE_TOLERANCE = timedelta(minutes=10)


class FeedUnavailable(Exception):
    """The feed could not be fetched."""


class FeedMalformed(Exception):
    """The feed was fetched but is not usable RSS."""


@dataclass(frozen=True)
class Article:
    title: str
    url: str
    guid: str
    published: datetime
    description: str = ""


def fetch_feed(session: requests.Session, url: str) -> bytes:
    """GET the feed, retrying timeouts, connection errors, 429 and 5xx."""
    for attempt in range(1, retry.ATTEMPTS + 1):
        try:
            resp = session.get(url, timeout=retry.TIMEOUT, headers={"Accept": "application/rss+xml, application/xml"})
        except (requests.Timeout, requests.ConnectionError) as exc:
            reason = f"feed request failed ({type(exc).__name__})"
        else:
            if resp.status_code == 200:
                return resp.content
            if resp.status_code != 429 and resp.status_code < 500:
                raise FeedUnavailable(f"feed returned HTTP {resp.status_code}")
            reason = f"feed returned HTTP {resp.status_code}"
        if attempt == retry.ATTEMPTS:
            raise FeedUnavailable(reason)
        retry.wait(attempt, reason)
    raise AssertionError("unreachable")


def _text(item: Element, tag: str) -> str:
    node = item.find(tag)
    return (node.text or "").strip() if node is not None else ""


def _parse_date(raw: str) -> datetime | None:
    if not raw:
        return None
    try:
        dt = parsedate_to_datetime(raw)
    except (TypeError, ValueError, IndexError):
        return None
    if dt.tzinfo is None:  # RFC 822 "-0000" means UTC with unknown origin
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def parse_feed(xml: bytes | str) -> list[Article]:
    """Parse RSS 2.0. Raises FeedMalformed when nothing usable is in it."""
    try:
        root = ElementTree.fromstring(xml)
    except (ParseError, DefusedXmlException) as exc:
        raise FeedMalformed(f"feed is not valid XML: {exc}") from None
    channel = root.find("channel")
    if root.tag != "rss" or channel is None:
        raise FeedMalformed("feed is not RSS 2.0 (no <rss><channel>)")
    items = channel.findall("item")
    if not items:
        raise FeedMalformed("feed contains no items")

    articles: list[Article] = []
    for index, item in enumerate(items):
        title = " ".join(_text(item, "title").split())
        link = _text(item, "link")
        published = _parse_date(_text(item, "pubDate"))
        if not (title and link and published):
            log.warning("skipping feed item %d: missing title, link or valid pubDate", index)
            continue
        articles.append(
            Article(
                title=title,
                url=canonical_url(link),
                guid=_text(item, "guid") or link,
                published=published,
                description=_text(item, "description"),
            )
        )
    if not articles:
        raise FeedMalformed("feed has items but none with a title, link and valid pubDate")
    return articles


def select_latest(articles: list[Article], now: datetime, max_age_hours: float) -> Article | None:
    """The newest article if it is current enough to post, else None.

    Newest is decided by pubDate, not feed order. An article that is too old,
    dated in the future, or not on MacTech's MacZine path is never returned:
    when in doubt, do not post.
    """
    latest = max(articles, key=lambda a: a.published)
    age = now - latest.published
    if not is_maczine_article(latest.url):
        raise FeedMalformed(f"newest item links outside MacZine: {latest.url}")
    if age < -FUTURE_TOLERANCE:
        log.warning("newest article is dated in the future (%s); not posting", latest.published.isoformat())
        return None
    if age > timedelta(hours=max_age_hours):
        log.info(
            "newest article is %.1fh old, over the %.0fh limit",
            age.total_seconds() / 3600,
            max_age_hours,
        )
        return None
    return latest
