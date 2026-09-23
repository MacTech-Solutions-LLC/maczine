#!/usr/bin/env bash
# One command that does every configuration step for the MacZine Reddit
# poster: refresh token, GitHub secrets, a dry run, the first live post,
# and turning the schedule on.
#
#   cd reddit && ./setup.sh
#
# What it needs from you: the client ID and secret of the approved Reddit
# app, the bot account name, and the subreddit. Nothing you type is echoed
# or logged, and the refresh token goes straight into a GitHub secret
# without ever being printed.
#
# Safe to re-run. Every step asks before it changes anything.

set -euo pipefail

REPO="${REPO:-MacTech-Solutions-LLC/maczine}"
WORKFLOW="post-to-reddit.yml"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bold() { printf '\033[1m%s\033[0m\n' "$1"; }
ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; }
warn() { printf '  \033[33m!\033[0m %s\n' "$1"; }
die()  { printf '\033[31mError:\033[0m %s\n' "$1" >&2; exit 1; }

ask() {  # ask "prompt" "default" -> echoes the answer
  local prompt="$1" default="${2:-}" reply
  if [ -n "$default" ]; then
    read -r -p "$prompt [$default]: " reply </dev/tty
    echo "${reply:-$default}"
  else
    read -r -p "$prompt: " reply </dev/tty
    echo "$reply"
  fi
}

confirm() {  # confirm "question" -> 0 for yes
  local reply
  read -r -p "$1 [y/N] " reply </dev/tty
  [[ "$reply" =~ ^[Yy] ]]
}

# --- preflight --------------------------------------------------------------

bold "MacZine → Reddit setup"
echo "Repository: $REPO"
echo

command -v gh >/dev/null || die "the GitHub CLI (gh) is not installed: brew install gh"
gh auth status >/dev/null 2>&1 || die "gh is not signed in: run 'gh auth login'"
gh repo view "$REPO" >/dev/null 2>&1 || die "no access to $REPO with the current gh account"
PYTHON="${PYTHON:-python3}"
command -v "$PYTHON" >/dev/null || die "python3 not found"

if [ ! -d "$HERE/.venv" ]; then
  echo "Creating a local virtualenv..."
  "$PYTHON" -m venv "$HERE/.venv"
fi
"$HERE/.venv/bin/pip" install -q -r "$HERE/requirements.txt"
ok "dependencies ready"
echo

# --- 1. credentials ---------------------------------------------------------

bold "1. Reddit app credentials"
cat <<'TXT'
   From https://www.reddit.com/prefs/apps, signed in as the BOT account:
   the client ID is the string just under the app's name, and the secret
   is the field labelled "secret". Nothing you paste here is displayed.
TXT

read -r -p "   Client ID: " CLIENT_ID </dev/tty
[ -n "$CLIENT_ID" ] || die "client ID is required"
read -r -s -p "   Client secret (hidden): " CLIENT_SECRET </dev/tty; echo
[ -n "$CLIENT_SECRET" ] || die "client secret is required"

USERNAME="$(ask '   Bot account name (without u/)')"
[ -n "$USERNAME" ] || die "bot account name is required"
SUBREDDIT="$(ask '   Subreddit to post to (without r/)')"
[ -n "$SUBREDDIT" ] || die "subreddit is required"
FLAIR="$(ask '   Post flair template ID (optional, Enter to skip)' 'none')"
echo

# --- 2. refresh token -------------------------------------------------------

bold "2. Authorize the bot account"
echo "   A browser window will open Reddit's consent page."
echo "   Make sure the browser is signed in as u/$USERNAME, then click Allow."
echo
if confirm "   Get a refresh token now?"; then
  REDDIT_CLIENT_ID="$CLIENT_ID" REDDIT_CLIENT_SECRET="$CLIENT_SECRET" \
    "$HERE/.venv/bin/python" "$HERE/get_refresh_token.py" --set-secret "$REPO" \
    || die "authorization failed; see the message above"
  ok "REDDIT_REFRESH_TOKEN stored (never displayed)"
else
  warn "skipped: the job cannot post until REDDIT_REFRESH_TOKEN is set"
fi
echo

# --- 3. the other secrets ---------------------------------------------------

bold "3. GitHub secrets"
printf '%s' "$CLIENT_ID"     | gh secret set REDDIT_CLIENT_ID     -R "$REPO"
printf '%s' "$CLIENT_SECRET" | gh secret set REDDIT_CLIENT_SECRET -R "$REPO"
printf '%s' "$USERNAME"      | gh secret set REDDIT_USERNAME      -R "$REPO"
printf '%s' "$SUBREDDIT"     | gh secret set REDDIT_SUBREDDIT     -R "$REPO"
ok "client ID, secret, username and subreddit stored"
if [ "$FLAIR" != "none" ] && [ -n "$FLAIR" ]; then
  printf '%s' "$FLAIR" | gh secret set REDDIT_FLAIR_ID -R "$REPO"
  ok "flair stored"
fi
unset CLIENT_SECRET
echo

# --- 4. dry run -------------------------------------------------------------

run_workflow() {  # run_workflow true|false -> prints the RESULT line
  local dry="$1" before after id
  before="$(gh run list -R "$REPO" -w "$WORKFLOW" -L 1 --json databaseId -q '.[0].databaseId // 0')"
  gh workflow run "$WORKFLOW" -R "$REPO" -f dry_run="$dry" >/dev/null
  printf '   waiting for the run to start'
  for _ in $(seq 1 30); do
    sleep 4; printf '.'
    after="$(gh run list -R "$REPO" -w "$WORKFLOW" -L 1 --json databaseId -q '.[0].databaseId // 0')"
    [ "$after" != "$before" ] && break
  done
  echo
  id="$after"
  [ "$id" = "$before" ] && { warn "the run did not appear; check the Actions tab"; return 1; }
  gh run watch "$id" -R "$REPO" --exit-status >/dev/null 2>&1 || true
  gh run view "$id" -R "$REPO" --log 2>/dev/null | grep -E "RESULT=|Reddit URL:|Article:|URL:|Destination:" | sed 's/^[^ ]* *//' | sed 's/^/   /'
  gh run view "$id" -R "$REPO" --json conclusion -q '.conclusion'
}

bold "4. Dry run (posts nothing)"
if confirm "   Run it?"; then
  conclusion="$(run_workflow true | tee /dev/tty | tail -1)"
  [ "$conclusion" = "success" ] || die "the dry run failed; see the log above or the Actions tab"
  ok "dry run succeeded"
else
  warn "skipped"
fi
echo

# --- 5. first live post -----------------------------------------------------

bold "5. First live post"
echo "   This posts today's MacZine issue to r/$SUBREDDIT for real."
if confirm "   Post it now?"; then
  conclusion="$(run_workflow false | tee /dev/tty | tail -1)"
  [ "$conclusion" = "success" ] || die "the live run failed; see the log above or the Actions tab"
  ok "done: check r/$SUBREDDIT"
else
  warn "skipped"
fi
echo

# --- 6. turn the schedule on ------------------------------------------------

bold "6. Weekday schedule"
echo "   Until this is switched on, scheduled runs are dry runs."
if confirm "   Turn the schedule on (posts every weekday morning)?"; then
  gh variable set REDDIT_SCHEDULED_DRY_RUN -R "$REPO" -b "false"
  ok "live: the next run is the following weekday at 08:05 Pacific"
else
  gh variable set REDDIT_SCHEDULED_DRY_RUN -R "$REPO" -b "true" >/dev/null
  warn "left in dry-run mode; re-run this script, or set the variable, when you are ready"
fi
echo

bold "Setup complete"
gh secret list -R "$REPO" | sed 's/^/  /'
echo
echo "  Watch it: gh run list -R $REPO -w $WORKFLOW"
