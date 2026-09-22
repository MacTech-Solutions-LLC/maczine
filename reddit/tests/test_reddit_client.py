import pytest
import requests

from conftest import TODAY_URL, make_config
from maczine_reddit.reddit import (
    TOKEN_URL,
    AlreadySubmitted,
    RedditAuthError,
    RedditClient,
    RedditRateLimited,
    RedditRejected,
    RedditUnavailable,
    user_agent,
)
from reddit_stubs import INFO, SUBMIT, empty_reads, history_url, listing, post, submit_error, submit_ok, token_ok


def _client(session, **cfg):
    return RedditClient(session, make_config(**cfg))


def test_user_agent_format():
    assert user_agent("MacZineBot") == \
        "github-actions:com.mactechsolutionsllc.maczine-reddit:v1.0.0 (by /u/MacZineBot)"


def test_token_request_uses_basic_auth_and_refresh_grant(mocked, session):
    token_ok(mocked)
    _client(session).authenticate()
    req = mocked.calls[0].request
    assert req.headers["Authorization"].startswith("Basic ")
    assert "grant_type=refresh_token" in req.body
    assert "MacZineBot" in req.headers["User-Agent"]


@pytest.mark.parametrize("status", [400, 401, 403])
def test_auth_http_errors(mocked, session, status):
    mocked.post(TOKEN_URL, status=status, json={"message": "Unauthorized"})
    with pytest.raises(RedditAuthError):
        _client(session).authenticate()


def test_invalid_grant(mocked, session):
    mocked.post(TOKEN_URL, json={"error": "invalid_grant"})
    with pytest.raises(RedditAuthError, match="invalid_grant"):
        _client(session).authenticate()


def test_missing_scope(mocked, session):
    token_ok(mocked, scope="identity read")
    with pytest.raises(RedditAuthError, match="history, submit"):
        _client(session).authenticate()


def test_auth_error_never_contains_secrets(mocked, session):
    mocked.post(TOKEN_URL, status=401)
    with pytest.raises(RedditAuthError) as exc:
        _client(session).authenticate()
    for secret in ("cid-123456", "csecret-abcdef", "rtoken-zyxwvu"):
        assert secret not in str(exc.value)


def test_submit_success_sends_link_post(mocked, session):
    token_ok(mocked)
    submit_ok(mocked)
    c = _client(session, flair_id="flair-1")
    c.authenticate()
    assert c.submit_link("Title", TODAY_URL).endswith("/comments/new1/x/")
    body = mocked.calls[-1].request.body
    for part in ("kind=link", "sr=MacZine", "resubmit=false", "flair_id=flair-1", "api_type=json"):
        assert part in body
    assert mocked.calls[-1].request.headers["Authorization"] == "bearer ACCESS-TOKEN-SECRET"


def test_submit_without_flair_omits_it(mocked, session):
    token_ok(mocked)
    submit_ok(mocked)
    c = _client(session)
    c.authenticate()
    c.submit_link("Title", TODAY_URL)
    assert "flair_id" not in mocked.calls[-1].request.body


def test_already_sub(mocked, session):
    token_ok(mocked)
    submit_error(mocked, "ALREADY_SUB", "that link has already been submitted")
    c = _client(session)
    c.authenticate()
    with pytest.raises(AlreadySubmitted):
        c.submit_link("Title", TODAY_URL)


@pytest.mark.parametrize("code", ["SUBREDDIT_NOTALLOWED", "NO_LINKS", "BAD_URL"])
def test_submit_rejections(mocked, session, code):
    token_ok(mocked)
    submit_error(mocked, code)
    c = _client(session)
    c.authenticate()
    with pytest.raises(RedditRejected) as exc:
        c.submit_link("Title", TODAY_URL)
    assert exc.value.code == code


def test_submit_ratelimit_error_code(mocked, session):
    token_ok(mocked)
    submit_error(mocked, "RATELIMIT", "you are doing that too much")
    c = _client(session)
    c.authenticate()
    with pytest.raises(RedditRateLimited):
        c.submit_link("Title", TODAY_URL)


def test_submit_403(mocked, session):
    token_ok(mocked)
    mocked.post(SUBMIT, status=403, json={})
    c = _client(session)
    c.authenticate()
    with pytest.raises(RedditRejected, match="403"):
        c.submit_link("Title", TODAY_URL)


def test_title_too_long_fails_closed(mocked, session):
    token_ok(mocked)
    c = _client(session)
    c.authenticate()
    with pytest.raises(RedditRejected):
        c.submit_link("x" * 301, TODAY_URL)
    assert not any(call.request.url.startswith(SUBMIT) for call in mocked.calls)


def test_429_honours_retry_after_then_succeeds(mocked, session, no_sleep):
    token_ok(mocked)
    mocked.get(INFO, status=429, headers={"Retry-After": "30"})
    mocked.get(INFO, json=listing())
    mocked.get(history_url(), json=listing())
    c = _client(session)
    c.authenticate()
    assert c.find_existing(TODAY_URL) is None
    assert no_sleep[0] == 30.0


def test_429_persistent_gives_up(mocked, session, no_sleep):
    token_ok(mocked)
    mocked.get(INFO, status=429, headers={"Retry-After": "600"})
    c = _client(session)
    c.authenticate()
    with pytest.raises(RedditRateLimited):
        c.find_existing(TODAY_URL)
    assert len(no_sleep) == 3 and max(no_sleep) == 60.0


def test_submit_5xx_rechecks_before_retrying(mocked, session):
    """A POST that 502s may still have created the post; never blindly resend."""
    token_ok(mocked)
    mocked.post(SUBMIT, status=502)
    mocked.get(INFO, json=listing(post(TODAY_URL, pid="landed")))
    c = _client(session)
    c.authenticate()
    assert c.submit_link("Title", TODAY_URL).endswith("/comments/landed/x/")
    assert sum(call.request.url.startswith(SUBMIT) for call in mocked.calls) == 1


def test_submit_timeout_then_retry_succeeds(mocked, session):
    token_ok(mocked)
    mocked.post(SUBMIT, body=requests.ConnectionError())
    empty_reads(mocked)
    submit_ok(mocked)
    c = _client(session)
    c.authenticate()
    assert c.submit_link("Title", TODAY_URL).endswith("/new1/x/")


def test_submit_persistent_5xx(mocked, session):
    token_ok(mocked)
    mocked.post(SUBMIT, status=503)
    empty_reads(mocked)
    c = _client(session)
    c.authenticate()
    with pytest.raises(RedditUnavailable):
        c.submit_link("Title", TODAY_URL)
    assert sum(call.request.url.startswith(SUBMIT) for call in mocked.calls) == 4


def test_listing_401(mocked, session):
    token_ok(mocked)
    mocked.get(INFO, status=401)
    c = _client(session)
    c.authenticate()
    with pytest.raises(RedditAuthError):
        c.find_existing(TODAY_URL)
