import pytest

from conftest import TODAY_URL, make_config
from maczine_reddit.reddit import RedditClient
from reddit_stubs import INFO, empty_reads, history_url, info_for, listing, post, token_ok

BARE = "https://mactechsolutionsllc.com/maczine/vulnerability-scanning-cadence-nist-800-171"


@pytest.fixture
def client(mocked, session):
    token_ok(mocked)
    c = RedditClient(session, make_config())
    c.authenticate()
    return c


def test_none_found(mocked, client):
    empty_reads(mocked)
    assert client.find_existing(TODAY_URL) is None


def test_found_by_url_index_in_our_subreddit(mocked, client):
    info_for(mocked, TODAY_URL, post(TODAY_URL, author="someone_else"))
    assert client.find_existing(TODAY_URL) == "https://www.reddit.com/r/MacZine/comments/abc123/x/"


def test_found_by_url_index_by_us_elsewhere(mocked, client):
    info_for(mocked, TODAY_URL, post(TODAY_URL, subreddit="cmmc"))
    assert client.find_existing(TODAY_URL).startswith("https://www.reddit.com/r/cmmc/")


def test_someone_elses_post_in_another_subreddit_is_not_ours(mocked, client):
    info_for(mocked, TODAY_URL, post(TODAY_URL, subreddit="cmmc", author="stranger"))
    info_for(mocked, BARE)
    mocked.get(history_url(), json=listing())
    assert client.find_existing(TODAY_URL) is None


def test_found_under_www_less_variant(mocked, client):
    info_for(mocked, TODAY_URL)
    info_for(mocked, BARE, post(BARE))
    assert client.find_existing(TODAY_URL)


@pytest.mark.parametrize(
    "posted",
    [
        TODAY_URL + "/",
        TODAY_URL + "?utm_source=reddit",
        TODAY_URL.replace("https://", "http://"),
        BARE + "#top",
    ],
)
def test_found_in_history_despite_url_differences(mocked, client, posted):
    mocked.get(INFO, json=listing())
    mocked.get(history_url(), json=listing(post("https://example.com/other"), post(posted, pid="hist1")))
    assert client.find_existing(TODAY_URL) == "https://www.reddit.com/r/MacZine/comments/hist1/x/"


def test_similar_slug_is_not_a_duplicate(mocked, client):
    mocked.get(INFO, json=listing())
    mocked.get(history_url(), json=listing(post(TODAY_URL + "-part-2")))
    assert client.find_existing(TODAY_URL) is None


def test_info_result_with_different_url_ignored(mocked, client):
    # /api/info can return loose matches; only an exact normalized match counts.
    mocked.get(INFO, json=listing(post("https://www.mactechsolutionsllc.com/maczine/other")))
    mocked.get(history_url(), json=listing())
    assert client.find_existing(TODAY_URL) is None
