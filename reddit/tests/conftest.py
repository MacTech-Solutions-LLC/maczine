from __future__ import annotations

from datetime import datetime, timezone

import pytest
import requests
import responses as responses_lib

from maczine_reddit import retry
from maczine_reddit.config import Config

FEED_URL = "https://www.mactechsolutionsllc.com/maczine/feed.xml"
NOW = datetime(2026, 9, 22, 15, 5, tzinfo=timezone.utc)  # Tue 08:05 PDT


def item(title: str, slug: str, pub: str, guid: bool = True) -> str:
    link = f"https://www.mactechsolutionsllc.com/maczine/{slug}"
    g = f"<guid isPermaLink=\"true\">{link}</guid>" if guid else ""
    return f"<item><title>{title}</title><link>{link}</link>{g}<description>d</description><pubDate>{pub}</pubDate></item>"


def feed(*items: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel>'
        "<title>MacZine</title><link>https://www.mactechsolutionsllc.com/maczine</link>"
        + "".join(items)
        + "</channel></rss>"
    )


TODAY = item("Issue Nº 040 - Vulnerability Scanning", "vulnerability-scanning-cadence-nist-800-171",
             "Tue, 22 Sep 2026 12:00:00 GMT")
YESTERDAY = item("Issue Nº 039 - Tabletop", "incident-response-tabletop-exercise", "Mon, 21 Sep 2026 12:00:00 GMT")
TODAY_URL = "https://www.mactechsolutionsllc.com/maczine/vulnerability-scanning-cadence-nist-800-171"


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    slept: list[float] = []
    monkeypatch.setattr(retry, "sleep", slept.append)
    return slept


@pytest.fixture
def mocked():
    # assert_all_requests_are_fired off: not every test exercises every stub.
    # Any request WITHOUT a stub raises, so no test can reach the real Reddit.
    with responses_lib.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        yield rsps


@pytest.fixture
def session():
    with requests.Session() as s:
        yield s


def make_config(**overrides) -> Config:
    base = dict(
        dry_run=False,
        feed_url=FEED_URL,
        client_id="cid-123456",
        client_secret="csecret-abcdef",
        refresh_token="rtoken-zyxwvu",
        username="MacZineBot",
        subreddit="MacZine",
    )
    base.update(overrides)
    return Config(**base)
