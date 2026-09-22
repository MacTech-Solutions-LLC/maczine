import logging

import pytest

from conftest import FEED_URL, NOW, TODAY, TODAY_URL, YESTERDAY, feed, make_config
from maczine_reddit import main
from maczine_reddit.main import Outcome, RedactSecrets, run
from maczine_reddit.reddit import TOKEN_URL
from reddit_stubs import INFO, SUBMIT, empty_reads, history_url, listing, post, submit_error, submit_ok, token_ok


def submits(mocked) -> int:
    return sum(call.request.url.startswith(SUBMIT) for call in mocked.calls)


def test_posts_new_article(mocked, session, caplog):
    caplog.set_level(logging.INFO)
    mocked.get(FEED_URL, body=feed(TODAY, YESTERDAY))
    token_ok(mocked)
    empty_reads(mocked)
    submit_ok(mocked)
    assert run(make_config(), session, NOW) is Outcome.POSTED
    assert submits(mocked) == 1
    assert "Reddit submission successful." in caplog.text
    assert "No existing submission found." in caplog.text


def test_already_posted_is_noop(mocked, session, caplog):
    caplog.set_level(logging.INFO)
    mocked.get(FEED_URL, body=feed(TODAY))
    token_ok(mocked)
    mocked.get(INFO, json=listing(post(TODAY_URL)))
    assert run(make_config(), session, NOW) is Outcome.ALREADY_POSTED
    assert submits(mocked) == 0
    assert "Article already posted; no action required." in caplog.text
    assert Outcome.ALREADY_POSTED.exit_code == 0


def test_second_run_same_morning_does_not_duplicate(mocked, session):
    mocked.get(FEED_URL, body=feed(TODAY))
    token_ok(mocked)
    empty_reads(mocked)
    submit_ok(mocked)
    assert run(make_config(), session, NOW) is Outcome.POSTED
    # Reddit now knows the post.
    mocked.replace("GET", INFO, json=listing(post(TODAY_URL)))
    assert run(make_config(), session, NOW) is Outcome.ALREADY_POSTED
    assert submits(mocked) == 1


def test_already_sub_from_reddit_is_noop(mocked, session):
    mocked.get(FEED_URL, body=feed(TODAY))
    token_ok(mocked)
    empty_reads(mocked)
    submit_error(mocked, "ALREADY_SUB")
    assert run(make_config(), session, NOW) is Outcome.ALREADY_POSTED


def test_no_new_article(mocked, session):
    mocked.get(FEED_URL, body=feed(YESTERDAY))
    later = NOW.replace(day=23, hour=12)  # yesterday's issue is now 48h old
    assert run(make_config(), session, later) is Outcome.NO_NEW_ARTICLE
    assert not any(c.request.url.startswith(TOKEN_URL) for c in mocked.calls)


def test_dry_run_without_credentials(mocked, session, caplog):
    caplog.set_level(logging.INFO)
    mocked.get(FEED_URL, body=feed(TODAY))
    cfg = make_config(dry_run=True, client_id="", client_secret="", refresh_token="", subreddit="")
    assert run(cfg, session, NOW) is Outcome.DRY_RUN
    assert len(mocked.calls) == 1
    assert "DRY RUN" in caplog.text and "No Reddit submission performed." in caplog.text


def test_dry_run_with_credentials_checks_duplicates_but_never_submits(mocked, session, caplog):
    caplog.set_level(logging.INFO)
    mocked.get(FEED_URL, body=feed(TODAY))
    token_ok(mocked)
    empty_reads(mocked)
    assert run(make_config(dry_run=True), session, NOW) is Outcome.DRY_RUN
    assert submits(mocked) == 0
    assert "r/MacZine" in caplog.text and TODAY_URL in caplog.text


@pytest.mark.parametrize(
    "setup,expected",
    [
        (lambda m: m.get(FEED_URL, status=500), Outcome.RSS_UNAVAILABLE),
        (lambda m: m.get(FEED_URL, body="<html>oops</html>"), Outcome.RSS_MALFORMED),
        (lambda m: (m.get(FEED_URL, body=feed(TODAY)), m.post(TOKEN_URL, status=401)), Outcome.REDDIT_AUTH),
        (lambda m: (m.get(FEED_URL, body=feed(TODAY)), token_ok(m), empty_reads(m),
                    submit_error(m, "SUBREDDIT_NOTALLOWED")), Outcome.REDDIT_REJECTED),
        (lambda m: (m.get(FEED_URL, body=feed(TODAY)), token_ok(m), m.get(INFO, status=429)), Outcome.RATE_LIMITED),
        (lambda m: (m.get(FEED_URL, body=feed(TODAY)), token_ok(m), m.get(INFO, status=503)),
         Outcome.REDDIT_UNAVAILABLE),
    ],
)
def test_error_outcomes_fail_the_job(mocked, session, setup, expected):
    setup(mocked)
    outcome = run(make_config(), session, NOW)
    assert outcome is expected
    assert outcome.exit_code != 0
    assert submits(mocked) == 0 or expected is Outcome.REDDIT_REJECTED


def test_exit_codes_distinct_for_errors():
    errors = [o for o in Outcome if o.kind == "ERROR"]
    assert len({o.exit_code for o in errors}) == len(errors)
    assert all(o.exit_code == 0 for o in Outcome if o.kind != "ERROR")


def test_redaction_filter_scrubs_messages_and_tracebacks():
    record = logging.LogRecord("x", logging.ERROR, __file__, 1, "token is %s", ("rtoken-zyxwvu",), None)
    RedactSecrets(("rtoken-zyxwvu",)).filter(record)
    assert record.getMessage() == "token is [REDACTED]"
    try:
        raise ValueError("boom csecret-abcdef")
    except ValueError:
        import sys
        rec = logging.LogRecord("x", logging.ERROR, __file__, 1, "fail", None, sys.exc_info())
    RedactSecrets(("csecret-abcdef",)).filter(rec)
    assert "csecret-abcdef" not in rec.getMessage() and "[REDACTED]" in rec.getMessage()


def test_cli_live_run_never_logs_secrets(mocked, monkeypatch, capsys):
    env = {
        "DRY_RUN": "false", "REDDIT_CLIENT_ID": "cid-123456", "REDDIT_CLIENT_SECRET": "csecret-abcdef",
        "REDDIT_REFRESH_TOKEN": "rtoken-zyxwvu", "REDDIT_USERNAME": "MacZineBot", "REDDIT_SUBREDDIT": "MacZine",
    }
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    monkeypatch.setattr(main, "datetime", _FrozenDatetime)
    mocked.get(FEED_URL, body=feed(TODAY))
    token_ok(mocked)
    empty_reads(mocked)
    submit_ok(mocked)
    logging.getLogger().handlers.clear()
    assert main.cli() == 0
    out = capsys.readouterr().out
    assert "RESULT=POSTED" in out
    for secret in ("cid-123456", "csecret-abcdef", "rtoken-zyxwvu", "ACCESS-TOKEN-SECRET"):
        assert secret not in out


def test_cli_config_error_exit_code(monkeypatch):
    monkeypatch.setenv("DRY_RUN", "false")
    for k in ("REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_REFRESH_TOKEN", "REDDIT_USERNAME",
              "REDDIT_SUBREDDIT"):
        monkeypatch.delenv(k, raising=False)
    assert main.cli() == 2


def test_step_summary_written(mocked, session, tmp_path, monkeypatch):
    summary = tmp_path / "summary.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))
    mocked.get(FEED_URL, body=feed(TODAY))
    token_ok(mocked)
    empty_reads(mocked)
    submit_ok(mocked)
    run(make_config(), session, NOW)
    assert "Posted" in summary.read_text()


class _FrozenDatetime:
    """Stands in for datetime inside main so cli() sees a fixed 'now'."""

    @staticmethod
    def now(tz=None):
        return NOW
