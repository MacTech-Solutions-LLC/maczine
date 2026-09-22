"""Minimal Reddit OAuth client: refresh-token auth, duplicate lookup, link submit.

Only the endpoints this job needs, over plain HTTPS, so every response can be
mocked in tests. Tokens live in memory and are never logged.
"""

from __future__ import annotations

import logging
from typing import Any, Callable

import requests

from maczine_reddit import __version__, retry
from maczine_reddit.config import Config
from maczine_reddit.urls import normalize_url

log = logging.getLogger(__name__)

TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
API_BASE = "https://oauth.reddit.com"
MAX_TITLE = 300          # Reddit rejects longer titles
HISTORY_LIMIT = 100      # max page size for /user/{name}/submitted


class RedditError(Exception):
    """Base class. `code` is Reddit's error code when it gave one."""

    def __init__(self, message: str, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code


class RedditAuthError(RedditError):
    """Credentials were refused (bad client, revoked or expired refresh token)."""


class RedditRejected(RedditError):
    """Reddit understood the request and refused it (403, submit errors)."""


class RedditRateLimited(RedditError):
    """Still rate limited after bounded retries."""


class RedditUnavailable(RedditError):
    """Network failure or 5xx after bounded retries."""


class AlreadySubmitted(RedditError):
    """Reddit refused the submit because this link is already in the subreddit."""


def user_agent(username: str) -> str:
    # Reddit's required format: <platform>:<app ID>:<version> (by /u/<username>)
    return f"github-actions:com.mactechsolutionsllc.maczine-reddit:v{__version__} (by /u/{username or 'unknown'})"


def _retry_after(resp: requests.Response) -> float | None:
    for header in ("Retry-After", "X-Ratelimit-Reset"):
        value = resp.headers.get(header)
        if value:
            try:
                return float(value)
            except ValueError:
                continue
    return None


class RedditClient:
    def __init__(self, session: requests.Session, cfg: Config) -> None:
        self._session = session
        self._cfg = cfg
        self._token: str | None = None
        self._session.headers["User-Agent"] = user_agent(cfg.username)

    # -- auth -------------------------------------------------------------

    def authenticate(self) -> None:
        """Exchange the refresh token for a short-lived access token."""
        data = {"grant_type": "refresh_token", "refresh_token": self._cfg.refresh_token}
        resp = self._send(
            lambda: self._session.post(
                TOKEN_URL,
                data=data,
                auth=(self._cfg.client_id, self._cfg.client_secret),
                timeout=retry.TIMEOUT,
            ),
            what="token request",
        )
        if resp.status_code in (400, 401, 403):
            raise RedditAuthError(f"Reddit refused the credentials (HTTP {resp.status_code})")
        body = self._json(resp)
        if "error" in body or not body.get("access_token"):
            # e.g. {"error": "invalid_grant"} for a revoked/expired refresh token
            raise RedditAuthError(f"Reddit refused the refresh token ({body.get('error', 'no access_token')})",
                                  code=str(body.get("error", "")) or None)
        self._token = body["access_token"]
        scopes = set(str(body.get("scope", "")).replace(",", " ").split())
        missing = {"submit", "read", "history"} - scopes if scopes and "*" not in scopes else set()
        if missing:
            raise RedditAuthError("refresh token lacks required scopes: " + ", ".join(sorted(missing)))

    # -- reads ------------------------------------------------------------

    def find_existing(self, url: str) -> str | None:
        """Permalink of an existing post of `url` by us or in our subreddit, else None.

        Two independent sources, so either one missing a post is not enough to
        cause a duplicate: Reddit's by-URL index (/api/info), and our own
        recent submissions compared on normalized URL.
        """
        target = normalize_url(url)
        me = self._cfg.username.lower()
        sub = self._cfg.subreddit.lower()

        for variant in _url_variants(url):
            for post in self._listing("/api/info", {"url": variant, "limit": 100}):
                if normalize_url(post.get("url", "")) != target:
                    continue
                if str(post.get("subreddit", "")).lower() == sub or str(post.get("author", "")).lower() == me:
                    return _permalink(post)

        for post in self._listing(f"/user/{self._cfg.username}/submitted",
                                  {"limit": HISTORY_LIMIT, "sort": "new", "raw_json": 1}):
            if normalize_url(post.get("url", "")) == target:
                return _permalink(post)
        return None

    # -- write ------------------------------------------------------------

    def submit_link(self, title: str, url: str) -> str:
        """Submit a link post and return its permalink.

        Raises AlreadySubmitted if Reddit reports the link is already there.
        The submit itself is never blindly retried: if the outcome of a POST
        is unknown (timeout, 5xx), Reddit is checked for the post first.
        """
        if not title or len(title) > MAX_TITLE:
            raise RedditRejected(f"title length {len(title)} is outside Reddit's 1-{MAX_TITLE} limit")
        data: dict[str, Any] = {
            "api_type": "json",
            "kind": "link",
            "sr": self._cfg.subreddit,
            "title": title,
            "url": url,
            "resubmit": "false",
            "sendreplies": "false",
        }
        if self._cfg.flair_id:
            data["flair_id"] = self._cfg.flair_id

        for attempt in range(1, retry.ATTEMPTS + 1):
            try:
                resp = self._session.post(f"{API_BASE}/api/submit", data=data,
                                          headers=self._auth(), timeout=retry.TIMEOUT)
            except (requests.Timeout, requests.ConnectionError) as exc:
                resp, reason = None, f"submit failed ({type(exc).__name__}); outcome unknown"
            else:
                if resp.status_code == 429:
                    reason = "submit rate limited (HTTP 429)"
                elif resp.status_code >= 500:
                    reason = f"submit returned HTTP {resp.status_code}; outcome unknown"
                else:
                    return self._submit_result(resp)
            if attempt == retry.ATTEMPTS:
                if resp is not None and resp.status_code == 429:
                    raise RedditRateLimited(reason)
                raise RedditUnavailable(reason)
            retry.wait(attempt, reason, _retry_after(resp) if resp is not None else None)
            if resp is None or resp.status_code >= 500:
                existing = self.find_existing(url)
                if existing:
                    log.info("post appeared despite the failed response")
                    return existing
        raise AssertionError("unreachable")

    def _submit_result(self, resp: requests.Response) -> str:
        self._raise_for_status(resp)
        body = self._json(resp).get("json", {})
        errors = body.get("errors") or []
        if errors:
            code = str(errors[0][0]) if errors[0] else "UNKNOWN"
            message = "; ".join(" ".join(str(p) for p in e[:2]) for e in errors)
            if code == "ALREADY_SUB":
                raise AlreadySubmitted(message, code=code)
            if code == "RATELIMIT":
                raise RedditRateLimited(message, code=code)
            raise RedditRejected(message, code=code)
        data = body.get("data") or {}
        link = data.get("url") or ""
        if not link:
            raise RedditRejected("submit returned no post URL")
        return link

    # -- plumbing ---------------------------------------------------------

    def _auth(self) -> dict[str, str]:
        if not self._token:
            raise RedditAuthError("not authenticated")
        return {"Authorization": f"bearer {self._token}"}

    def _listing(self, path: str, params: dict[str, Any]) -> list[dict[str, Any]]:
        resp = self._send(
            lambda: self._session.get(f"{API_BASE}{path}", params=params,
                                      headers=self._auth(), timeout=retry.TIMEOUT),
            what=f"GET {path}",
        )
        self._raise_for_status(resp)
        body = self._json(resp)
        children = body.get("data", {}).get("children", []) if isinstance(body, dict) else []
        return [c.get("data", {}) for c in children if c.get("kind") == "t3"]

    def _send(self, call: Callable[[], requests.Response], what: str) -> requests.Response:
        """Run an idempotent request, retrying timeouts, 429 and 5xx."""
        for attempt in range(1, retry.ATTEMPTS + 1):
            try:
                resp = call()
            except (requests.Timeout, requests.ConnectionError) as exc:
                resp, reason = None, f"{what} failed ({type(exc).__name__})"
            else:
                self._note_ratelimit(resp)
                if resp.status_code != 429 and resp.status_code < 500:
                    return resp
                reason = f"{what} returned HTTP {resp.status_code}"
            if attempt == retry.ATTEMPTS:
                if resp is not None and resp.status_code == 429:
                    raise RedditRateLimited(reason)
                raise RedditUnavailable(reason)
            retry.wait(attempt, reason, _retry_after(resp) if resp is not None else None)
        raise AssertionError("unreachable")

    @staticmethod
    def _note_ratelimit(resp: requests.Response) -> None:
        remaining = resp.headers.get("X-Ratelimit-Remaining")
        try:
            if remaining is not None and float(remaining) < 5:
                log.warning("Reddit rate-limit budget low: %s requests remaining", remaining)
        except ValueError:
            pass

    @staticmethod
    def _raise_for_status(resp: requests.Response) -> None:
        if resp.status_code == 401:
            raise RedditAuthError("Reddit rejected the access token (HTTP 401)")
        if resp.status_code == 403:
            raise RedditRejected("Reddit refused access (HTTP 403): check the account can post in the subreddit",
                                 code="FORBIDDEN")
        if resp.status_code == 404:
            raise RedditRejected("Reddit returned HTTP 404: check the subreddit and username", code="NOT_FOUND")
        if resp.status_code >= 400:
            raise RedditRejected(f"Reddit returned HTTP {resp.status_code}")

    @staticmethod
    def _json(resp: requests.Response) -> dict[str, Any]:
        try:
            body = resp.json()
        except ValueError:
            raise RedditUnavailable(f"Reddit returned non-JSON (HTTP {resp.status_code})") from None
        return body if isinstance(body, dict) else {}


def _url_variants(url: str) -> list[str]:
    """The same article written the ways it could have been submitted."""
    norm = normalize_url(url)                   # https://host/path
    bare = norm.split("://", 1)[1]
    variants = [url, f"https://{bare}", f"https://www.{bare}"]
    seen: list[str] = []
    for v in variants:
        if v not in seen:
            seen.append(v)
    return seen


def _permalink(post: dict[str, Any]) -> str:
    link = str(post.get("permalink", ""))
    return f"https://www.reddit.com{link}" if link.startswith("/") else link
