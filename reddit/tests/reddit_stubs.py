"""Helpers that stub Reddit's endpoints on a `responses` mock."""

from __future__ import annotations

from responses import matchers

from maczine_reddit.reddit import API_BASE, TOKEN_URL

INFO = f"{API_BASE}/api/info"
SUBMIT = f"{API_BASE}/api/submit"


def history_url(user: str = "MacZineBot") -> str:
    return f"{API_BASE}/user/{user}/submitted"


def post(url: str, subreddit: str = "MacZine", author: str = "MacZineBot", pid: str = "abc123") -> dict:
    return {"kind": "t3", "data": {"url": url, "subreddit": subreddit, "author": author,
                                   "permalink": f"/r/{subreddit}/comments/{pid}/x/"}}


def listing(*posts: dict) -> dict:
    return {"kind": "Listing", "data": {"children": list(posts)}}


def token_ok(rsps, scope: str = "identity read history submit") -> None:
    rsps.post(TOKEN_URL, json={"access_token": "ACCESS-TOKEN-SECRET", "token_type": "bearer",
                               "expires_in": 86400, "scope": scope})


def empty_reads(rsps) -> None:
    rsps.get(INFO, json=listing())
    rsps.get(history_url(), json=listing())


def submit_ok(rsps, permalink: str = "https://www.reddit.com/r/MacZine/comments/new1/x/") -> None:
    rsps.post(SUBMIT, json={"json": {"errors": [], "data": {"url": permalink, "id": "new1", "name": "t3_new1"}}})


def submit_error(rsps, code: str, msg: str = "nope") -> None:
    rsps.post(SUBMIT, json={"json": {"errors": [[code, msg, "url"]]}})


def info_for(rsps, url: str, *posts: dict) -> None:
    rsps.get(INFO, match=[matchers.query_param_matcher({"url": url, "limit": "100"})], json=listing(*posts))
