from datetime import datetime, timedelta, timezone

import pytest
import requests

from conftest import FEED_URL, NOW, TODAY, TODAY_URL, YESTERDAY, feed, item
from maczine_reddit import rss


def test_parses_items():
    articles = rss.parse_feed(feed(TODAY, YESTERDAY))
    assert len(articles) == 2
    a = articles[0]
    assert a.title == "Issue Nº 040 - Vulnerability Scanning"
    assert a.url == TODAY_URL
    assert a.guid == TODAY_URL
    assert a.published == datetime(2026, 9, 22, 12, 0, tzinfo=timezone.utc)
    assert a.description == "d"


def test_parses_real_feed_shape_with_namespaces_and_cdata():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel><title>MacZine</title>
    <atom:link href="https://www.mactechsolutionsllc.com/maczine/feed.xml" rel="self" type="application/rss+xml"/>
    <item>
      <title>Issue N&#186; 040 - A &amp; B</title>
      <link>https://www.mactechsolutionsllc.com/maczine/a-and-b</link>
      <guid isPermaLink="true">https://www.mactechsolutionsllc.com/maczine/a-and-b</guid>
      <content:encoded><![CDATA[<p>x</p>]]></content:encoded>
      <pubDate>Tue, 22 Sep 2026 12:00:00 GMT</pubDate>
      <dc:creator xmlns:dc="http://purl.org/dc/elements/1.1/">Patrick</dc:creator>
    </item>
  </channel></rss>"""
    [a] = rss.parse_feed(xml.encode())
    assert a.title == "Issue Nº 040 - A & B"


def test_missing_guid_falls_back_to_link():
    [a] = rss.parse_feed(feed(item("T", "s", "Tue, 22 Sep 2026 12:00:00 GMT", guid=False)))
    assert a.guid.endswith("/maczine/s")


def test_numeric_offset_pubdate_converted_to_utc():
    [a] = rss.parse_feed(feed(item("T", "s", "Tue, 22 Sep 2026 08:00:00 -0400")))
    assert a.published == datetime(2026, 9, 22, 12, 0, tzinfo=timezone.utc)


@pytest.mark.parametrize(
    "xml",
    [
        "not xml at all",
        "<rss><channel><item>",                       # truncated
        "<html><body>502 Bad Gateway</body></html>",  # error page
        "<rss version='2.0'><channel></channel></rss>",  # no items
        feed("<item><title>no link</title></item>"),  # no usable items
        feed(item("T", "s", "not a date")),
    ],
)
def test_malformed_feeds_raise(xml):
    with pytest.raises(rss.FeedMalformed):
        rss.parse_feed(xml)


def test_entity_expansion_is_refused():
    bomb = ('<?xml version="1.0"?><!DOCTYPE r [<!ENTITY a "aaaa"><!ENTITY b "&a;&a;&a;">]>'
            "<rss><channel><item><title>&b;</title></item></channel></rss>")
    with pytest.raises(rss.FeedMalformed):
        rss.parse_feed(bomb)


def test_bad_item_skipped_good_kept():
    articles = rss.parse_feed(feed(item("T", "s", "garbage"), YESTERDAY))
    assert [a.title for a in articles] == ["Issue Nº 039 - Tabletop"]


# -- selection --------------------------------------------------------------

def test_selects_newest_by_date_not_order():
    articles = rss.parse_feed(feed(YESTERDAY, TODAY))
    assert rss.select_latest(articles, NOW, 36).url == TODAY_URL


def test_too_old_returns_none():
    articles = rss.parse_feed(feed(YESTERDAY))
    assert rss.select_latest(articles, NOW + timedelta(hours=20), 36) is None


def test_friday_issue_not_new_on_monday():
    fri = rss.parse_feed(feed(item("Fri", "fri", "Fri, 18 Sep 2026 12:00:00 GMT")))
    monday_0805_pdt = datetime(2026, 9, 21, 15, 5, tzinfo=timezone.utc)
    assert rss.select_latest(fri, monday_0805_pdt, 36) is None


def test_missed_morning_run_still_catches_up_same_day():
    articles = rss.parse_feed(feed(TODAY))
    late = datetime(2026, 9, 22, 23, 0, tzinfo=timezone.utc)
    assert rss.select_latest(articles, late, 36).url == TODAY_URL


def test_future_dated_article_not_posted():
    articles = rss.parse_feed(feed(item("Tomorrow", "t", "Wed, 23 Sep 2026 12:00:00 GMT")))
    assert rss.select_latest(articles, NOW, 36) is None


def test_small_clock_skew_tolerated():
    articles = rss.parse_feed(feed(TODAY))
    assert rss.select_latest(articles, datetime(2026, 9, 22, 11, 55, tzinfo=timezone.utc), 36) is not None


def test_foreign_link_fails_closed():
    xml = feed("<item><title>x</title><link>https://evil.example/maczine/x</link>"
               "<pubDate>Tue, 22 Sep 2026 12:00:00 GMT</pubDate></item>")
    with pytest.raises(rss.FeedMalformed):
        rss.select_latest(rss.parse_feed(xml), NOW, 36)


# -- fetching ---------------------------------------------------------------

def test_fetch_retries_5xx_then_succeeds(mocked, session, no_sleep):
    mocked.get(FEED_URL, status=500)
    mocked.get(FEED_URL, status=503)
    mocked.get(FEED_URL, body=feed(TODAY))
    assert b"Vulnerability" in rss.fetch_feed(session, FEED_URL)
    assert no_sleep == [2.0, 4.0]


def test_fetch_gives_up_after_bounded_retries(mocked, session, no_sleep):
    mocked.get(FEED_URL, status=502)
    with pytest.raises(rss.FeedUnavailable):
        rss.fetch_feed(session, FEED_URL)
    assert len(no_sleep) == 3


def test_fetch_timeout_retried(mocked, session):
    mocked.get(FEED_URL, body=requests.Timeout())
    mocked.get(FEED_URL, body=feed(TODAY))
    assert rss.fetch_feed(session, FEED_URL)


def test_fetch_404_not_retried(mocked, session, no_sleep):
    mocked.get(FEED_URL, status=404)
    with pytest.raises(rss.FeedUnavailable, match="404"):
        rss.fetch_feed(session, FEED_URL)
    assert no_sleep == []
