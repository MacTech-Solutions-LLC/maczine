"""URL normalization, so the same article compares equal however it was written."""

from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ALLOWED_HOSTS = {"mactechsolutionsllc.com", "www.mactechsolutionsllc.com"}
ARTICLE_PATH_PREFIX = "/maczine/"

_TRACKING_EXACT = {"fbclid", "gclid", "dclid", "msclkid", "ref", "ref_src", "igshid", "yclid"}
_TRACKING_PREFIXES = ("utm_", "mc_")


def _is_tracking(key: str) -> bool:
    k = key.lower()
    return k in _TRACKING_EXACT or k.startswith(_TRACKING_PREFIXES)


def normalize_url(url: str) -> str:
    """Comparison key: https, bare lowercase host, no trailing slash, fragment
    or tracking parameters; remaining query parameters sorted."""
    parts = urlsplit(url.strip())
    host = (parts.hostname or "").lower().removeprefix("www.")
    if parts.port and parts.port not in (80, 443):
        host = f"{host}:{parts.port}"
    path = parts.path.rstrip("/") or ""
    query = sorted((k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if not _is_tracking(k))
    return urlunsplit(("https", host, path, urlencode(query), ""))


def canonical_url(url: str) -> str:
    """The URL to submit: the feed link as published, forced to https, with
    tracking parameters, fragment and trailing slash removed. The host is
    kept as-is so the post points at the exact live address."""
    parts = urlsplit(url.strip())
    query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if not _is_tracking(k)]
    return urlunsplit(("https", parts.netloc.lower(), parts.path.rstrip("/"), urlencode(query), ""))


def is_maczine_article(url: str) -> bool:
    """True only for an article page on MacTech's own site."""
    parts = urlsplit(url.strip())
    if parts.scheme not in ("http", "https"):
        return False
    if (parts.hostname or "").lower() not in ALLOWED_HOSTS or parts.port not in (None, 80, 443):
        return False
    slug = parts.path.removeprefix(ARTICLE_PATH_PREFIX).strip("/")
    return parts.path.startswith(ARTICLE_PATH_PREFIX) and bool(slug) and slug != "feed.xml"
