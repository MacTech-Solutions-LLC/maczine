import pytest

from maczine_reddit.urls import canonical_url, is_maczine_article, normalize_url

BASE = "https://mactechsolutionsllc.com/maczine/slug"


@pytest.mark.parametrize(
    "url",
    [
        "https://www.mactechsolutionsllc.com/maczine/slug",
        "http://www.mactechsolutionsllc.com/maczine/slug",
        "https://mactechsolutionsllc.com/maczine/slug/",
        "https://WWW.MacTechSolutionsLLC.com/maczine/slug",
        "https://www.mactechsolutionsllc.com/maczine/slug?utm_source=reddit&utm_medium=social",
        "https://www.mactechsolutionsllc.com/maczine/slug?fbclid=abc&gclid=x&ref=hn",
        "https://www.mactechsolutionsllc.com/maczine/slug#section-2",
        "  https://www.mactechsolutionsllc.com/maczine/slug/?mc_cid=1#top ",
        "https://www.mactechsolutionsllc.com:443/maczine/slug",
    ],
)
def test_variants_normalize_equal(url):
    assert normalize_url(url) == BASE


def test_path_case_and_meaningful_query_are_kept():
    assert normalize_url("https://x.com/Maczine/Slug") == "https://x.com/Maczine/Slug"
    assert normalize_url("https://x.com/a?b=2&a=1&utm_x=9") == "https://x.com/a?a=1&b=2"
    assert normalize_url(BASE) != normalize_url(BASE + "-two")


def test_canonical_keeps_host_but_cleans():
    assert (canonical_url("http://www.mactechsolutionsllc.com/maczine/slug/?utm_source=x#f")
            == "https://www.mactechsolutionsllc.com/maczine/slug")


@pytest.mark.parametrize(
    "url,ok",
    [
        ("https://www.mactechsolutionsllc.com/maczine/slug", True),
        ("https://mactechsolutionsllc.com/maczine/slug", True),
        ("https://www.mactechsolutionsllc.com/maczine", False),
        ("https://www.mactechsolutionsllc.com/maczine/", False),
        ("https://www.mactechsolutionsllc.com/maczine/feed.xml", False),
        ("https://www.mactechsolutionsllc.com/blog/slug", False),
        ("https://evil.example/maczine/slug", False),
        ("https://mactechsolutionsllc.com.evil.example/maczine/slug", False),
        ("ftp://www.mactechsolutionsllc.com/maczine/slug", False),
        ("https://www.mactechsolutionsllc.com:8443/maczine/slug", False),
    ],
)
def test_is_maczine_article(url, ok):
    assert is_maczine_article(url) is ok
