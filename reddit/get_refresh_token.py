"""One-time helper: authorize the bot account and obtain a permanent refresh token.

Run locally, signed in to Reddit as the bot account in your browser:

    REDDIT_CLIENT_ID=... REDDIT_CLIENT_SECRET=... python get_refresh_token.py

It opens Reddit's consent page, catches the redirect on
http://localhost:8080/callback, and exchanges the code for a refresh token.
With --set-secret it pipes the token straight into the GitHub secret via the
gh CLI, so it never appears on screen; otherwise it prints it once.
"""

from __future__ import annotations

import argparse
import http.server
import os
import secrets
import subprocess
import sys
import urllib.parse
import webbrowser

import requests

AUTHORIZE_URL = "https://www.reddit.com/api/v1/authorize"
TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
REDIRECT_URI = "http://localhost:8080/callback"
SCOPES = "identity read history submit"
USER_AGENT = "script:com.mactechsolutionsllc.maczine-reddit.setup:v1.0.0"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--set-secret", metavar="OWNER/REPO",
                        help="store the token as REDDIT_REFRESH_TOKEN in this repo with `gh secret set`")
    args = parser.parse_args()

    client_id = os.environ.get("REDDIT_CLIENT_ID", "").strip()
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET", "").strip()
    if not client_id or not client_secret:
        print("Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET in the environment first.", file=sys.stderr)
        return 2

    state = secrets.token_urlsafe(16)
    url = AUTHORIZE_URL + "?" + urllib.parse.urlencode({
        "client_id": client_id,
        "response_type": "code",
        "state": state,
        "redirect_uri": REDIRECT_URI,
        "duration": "permanent",
        "scope": SCOPES,
    })

    result: dict[str, str] = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802 - stdlib name
            query = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(self.path).query))
            result.update(query)
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Done. You can close this tab and return to the terminal.")

        def log_message(self, *_: object) -> None:
            pass

    print("Opening Reddit's consent page. Make sure you are signed in as the BOT account.")
    print(f"If no browser opens, visit:\n  {url}\n")
    webbrowser.open(url)
    with http.server.HTTPServer(("127.0.0.1", 8080), Handler) as server:
        while "code" not in result and "error" not in result:
            server.handle_request()

    if result.get("state") != state:
        print("State mismatch; aborting.", file=sys.stderr)
        return 1
    if "error" in result:
        print(f"Reddit returned an error: {result['error']}", file=sys.stderr)
        return 1

    resp = requests.post(
        TOKEN_URL,
        auth=(client_id, client_secret),
        data={"grant_type": "authorization_code", "code": result["code"], "redirect_uri": REDIRECT_URI},
        headers={"User-Agent": USER_AGENT},
        timeout=15,
    )
    body = resp.json() if resp.headers.get("Content-Type", "").startswith("application/json") else {}
    token = body.get("refresh_token")
    if resp.status_code != 200 or not token:
        print(f"Token exchange failed (HTTP {resp.status_code}, {body.get('error', 'no refresh_token')}).",
              file=sys.stderr)
        return 1

    print(f"Granted scopes: {body.get('scope')}")
    if args.set_secret:
        subprocess.run(["gh", "secret", "set", "REDDIT_REFRESH_TOKEN", "-R", args.set_secret],
                       input=token.encode(), check=True)
        print(f"Stored REDDIT_REFRESH_TOKEN in {args.set_secret}.")
    else:
        print("\nREDDIT_REFRESH_TOKEN (store it as a GitHub secret, then clear your terminal):\n")
        print(token)
    return 0


if __name__ == "__main__":
    sys.exit(main())
