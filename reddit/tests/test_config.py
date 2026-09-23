import pytest

from maczine_reddit.config import DEFAULT_FEED_URL, ConfigError, load_config

FULL = {
    "REDDIT_CLIENT_ID": "cid-123456",
    "REDDIT_CLIENT_SECRET": "csecret-abcdef",
    "REDDIT_REFRESH_TOKEN": "rtoken-zyxwvu",
    "REDDIT_USERNAME": "MacZineBot",
    "REDDIT_SUBREDDIT": "r/MacZine",
    "DRY_RUN": "false",
}


def test_full_live_config():
    cfg = load_config(FULL)
    assert not cfg.dry_run
    assert cfg.subreddit == "MacZine"
    assert cfg.feed_url == DEFAULT_FEED_URL
    assert cfg.max_age_hours == 36
    assert cfg.flair_id == ""
    assert cfg.has_reddit_credentials


def test_dry_run_is_the_default():
    assert load_config({}).dry_run is True


def test_dry_run_needs_no_credentials():
    cfg = load_config({"DRY_RUN": "true"})
    assert not cfg.has_reddit_credentials


@pytest.mark.parametrize("missing", list(k for k in FULL if k.startswith("REDDIT_")))
def test_live_run_reports_each_missing_key(missing):
    env = {k: v for k, v in FULL.items() if k != missing}
    with pytest.raises(ConfigError, match=missing):
        load_config(env)


def test_missing_key_error_never_leaks_values():
    env = dict(FULL, REDDIT_USERNAME="")
    with pytest.raises(ConfigError) as exc:
        load_config(env)
    for value in ("cid-123456", "csecret-abcdef", "rtoken-zyxwvu"):
        assert value not in str(exc.value)


def test_repr_hides_secrets():
    text = repr(load_config(FULL))
    for value in ("cid-123456", "csecret-abcdef", "rtoken-zyxwvu"):
        assert value not in text


@pytest.mark.parametrize("raw,ok", [("48", 48.0), ("", 36.0), ("abc", None), ("0", None), ("500", None)])
def test_max_age(raw, ok):
    env = {"MAX_ARTICLE_AGE_HOURS": raw}
    if ok is None:
        with pytest.raises(ConfigError):
            load_config(env)
    else:
        assert load_config(env).max_age_hours == ok


def test_bad_dry_run_value():
    with pytest.raises(ConfigError):
        load_config({"DRY_RUN": "maybe"})


def test_whitespace_and_prefixes_trimmed():
    cfg = load_config(dict(FULL, REDDIT_SUBREDDIT=" /r/MacZine/ ", REDDIT_USERNAME="u/MacZineBot",
                           REDDIT_FLAIR_ID=" f1 "))
    assert cfg.subreddit == "MacZine" and cfg.username == "MacZineBot" and cfg.flair_id == "f1"
