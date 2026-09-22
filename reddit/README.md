# MacZine → Reddit poster

Posts each new MacZine issue to MacTech's subreddit as a link post, every
weekday, with no one involved.

## What it does

A GitHub Actions job runs several times each weekday morning (Pacific). Each run:

1. Fetches the MacZine RSS feed (`https://www.mactechsolutionsllc.com/maczine/feed.xml`).
2. Picks the newest issue by `pubDate`, and stops if the issue is too old,
   dated in the future, or links anywhere but `mactechsolutionsllc.com/maczine/…`.
3. Asks Reddit whether that URL is already posted, either by this account or
   in the target subreddit.
4. If it is not, submits a link post. The title is the issue title, exactly
   as published. The URL is the issue URL.
5. Logs the outcome and exits. An issue that is already posted, or no new
   issue, is a green run. Real failures turn the run red.

The first run of the morning posts, and the later runs find the post and do
nothing.

## Architecture

```
MacZine RSS ──► GitHub Actions (Mon–Fri, 08:05 / 08:15 / 08:30 / 09:00 / 10:30 America/Los_Angeles)
                    │
                    ▼
          parse feed, pick newest by pubDate
                    │
       too old / future / off-site? ──yes──► NOOP (green)
                    │ no
                    ▼
   Reddit: /api/info?url=…  +  /user/<bot>/submitted
                    │
          already there? ──yes──► NOOP "Article already posted; no action required."
                    │ no
                    ▼
     DRY_RUN? ──yes──► print what would be posted (green)
                    │ no
                    ▼
     POST /api/submit  kind=link  resubmit=false ──► SUCCESS + Reddit URL
```

**Why there is no database.** Reddit is the record of what has been posted.
Duplicates are blocked at three levels:

1. **Two lookups before submitting.** Reddit's by-URL index and the bot's
   own submission history are both checked, comparing normalized URLs.
   Normalization forces https, ignores `www.`, trailing slashes and
   `#fragments`, and drops `utm_*`, `fbclid`, `gclid`, `mc_*` and `ref`.
2. **`resubmit=false` on the submit.** Reddit refuses a link that is already
   in the subreddit (`ALREADY_SUB`), and the job treats that as a no-op.
3. **One run at a time.** A `concurrency` group means two runs never
   overlap. If a submit times out or gets a 5xx, the job checks Reddit for
   the post before it tries again.

**Freshness.** An issue counts as new for `MAX_ARTICLE_AGE_HOURS` (default
36) after its `pubDate`.
- A missed 8:05 run still posts that day's issue at 8:15, 10:30, or on a
  manual run later.
- Friday's issue is about 72 hours old by Monday, so it is never reposted.
- The schedule does not run on weekends.

**Release time.** MacZine issues actually go live at **8:00 AM Eastern**
(5:00 AM Pacific), the `publishedAt` gate in the content repo. Posting
starts at 8:05 AM Pacific, so each issue has been live for about 3 hours
by then. To post earlier, change the cron times in
`.github/workflows/post-to-reddit.yml`.

## Setup

### 1. Reddit account and subreddit

1. Create a dedicated Reddit account for the bot, for example `MacZineBot`.
   Verify its email and turn on two-factor authentication. The job never
   uses the password: it uses a refresh token, so 2FA does not get in the
   way.
2. Create MacTech's subreddit, or use the existing one. Make the bot
   account a **moderator**, or at least an approved user.
3. Post only to MacTech's own subreddit. Reddit's spam rules target
   accounts that mostly post their own links into community subreddits,
   and a daily bot doing that gets banned. `REDDIT_SUBREDDIT` can point
   anywhere, but keep it on MacTech's own community.

### 2. Request Reddit API access (manual step)

Since **November 2025**, Reddit's
[Responsible Builder Policy](https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy)
requires approval **before** any new app can use the API. Self-service
creation at `reddit.com/prefs/apps` no longer works for new developers.
This step cannot be automated, and the job cannot post until it is done.

To file the request:

1. Sign in as the bot account.
2. Go to Reddit Help's developer / Data API support request, linked from
   [Developer Platform & Accessing Reddit Data](https://support.reddithelp.com/hc/en-us/articles/14945211791892-Developer-Platform-Accessing-Reddit-Data).
3. Choose the Data API access request, and describe the use case exactly:

> **App description:** Automated publisher for MacTech Solutions' own daily MacZine cybersecurity articles.
>
> **What it does:** Once per weekday, submits one link post, the title and URL of that day's MacZine article from mactechsolutionsllc.com, to our own subreddit r/<YourSubreddit>, which our account moderates. Before posting it checks the account's own submissions and /api/info to avoid duplicates.
>
> **Volume:** 1 post per weekday; under 20 API requests per day in total.
>
> **Scopes:** `identity`, `read`, `history`, `submit`.
>
> **Data use:** No Reddit data is collected, stored, redistributed, or used for training. Non-commercial use of the API (we post our own free articles).
>
> **Account:** u/<bot account>, operated by MacTech Solutions LLC.

File one request, from the account that will post. The policy prohibits
multiple requests for the same use case. Then wait for the answer.

### 3. Create the app (after approval)

At <https://www.reddit.com/prefs/apps>, signed in as the bot account,
choose **create app**:

- **Name:** `MacZine Publisher`
- **Type:** `web app`
- **Description:** Automated publisher for MacTech Solutions' own daily MacZine cybersecurity articles.
- **Redirect URI:** `http://localhost:8080/callback`

Save it. The **client ID** is the string under the app name. The
**client secret** is labelled `secret`.

### 4. Get a refresh token (once)

On your own machine, signed in to Reddit **as the bot account** in the
default browser:

```bash
cd reddit
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
REDDIT_CLIENT_ID=… REDDIT_CLIENT_SECRET=… \
  .venv/bin/python get_refresh_token.py --set-secret MacTech-Solutions-LLC/maczine
```

Approve the consent page. The script requests a **permanent** token with
scopes `identity read history submit`. With `--set-secret`, it stores
`REDDIT_REFRESH_TOKEN` directly with the `gh` CLI, so the token never
appears on screen. Without the flag, it prints the token once.

### 5. GitHub secrets and variables

Set these under **Settings → Secrets and variables → Actions** in
`MacTech-Solutions-LLC/maczine`, or with `gh secret set NAME -R MacTech-Solutions-LLC/maczine`:

| Secret                 | Required | Purpose                                                                                              |
| ---------------------- | -------- | ---------------------------------------------------------------------------------------------------- |
| `REDDIT_CLIENT_ID`     | yes      | The approved app's client ID                                                                         |
| `REDDIT_CLIENT_SECRET` | yes      | The app's secret                                                                                     |
| `REDDIT_REFRESH_TOKEN` | yes      | Permanent refresh token from step 4                                                                  |
| `REDDIT_USERNAME`      | yes      | Bot account name, without `u/`. Used for the User-Agent and the submission-history duplicate check |
| `REDDIT_SUBREDDIT`     | yes      | Destination, without `r/`, e.g. `MacZine`                                                            |
| `REDDIT_FLAIR_ID`      | no       | Post flair template ID. Leave it unset for no flair                                                  |

| Variable                   | Default          | Purpose                                                                          |
| -------------------------- | ---------------- | -------------------------------------------------------------------------------- |
| `REDDIT_SCHEDULED_DRY_RUN` | unset = **true** | Scheduled runs only post when this is `false`                                    |
| `MAX_ARTICLE_AGE_HOURS`    | `36`             | How long after `pubDate` an issue still counts as new (0 to 168)                 |

Secrets are passed only to the one step that needs them. GitHub masks them
in logs, the code never logs them, and a logging filter scrubs them from
anything that slips through, tracebacks included.

### 6. Dry run

In the **Actions** tab, open **Post MacZine to Reddit**, choose
**Run workflow**, and leave **dry_run** ticked. The log shows the article,
the destination, and the result of a real duplicate check against Reddit,
and it posts nothing:

```
DRY RUN

Article:
  "Issue Nº 040 - Vulnerability Scanning Under NIST 800-171: How Often Is Enough?"

URL:
  https://www.mactechsolutionsllc.com/maczine/vulnerability-scanning-cadence-nist-800-171

Destination:
  r/MacZine

Duplicate check: performed, none found

No Reddit submission performed.
RESULT=DRY_RUN (NOOP: dry run, nothing submitted)
```

The dry run works with no Reddit secrets at all. It then skips the
duplicate check and says so, which is useful while approval is pending.

### 7. First live post

Run the workflow again with **dry_run** unticked. Check that the post
appears in the subreddit. Then run it once more and confirm the log says
`Article already posted; no action required.`

### 8. Turn on the schedule

Set the repository variable `REDDIT_SCHEDULED_DRY_RUN` to `false`. Until
you do, scheduled runs are dry runs, so the schedule never posts before
you decide it should.

## Outcomes and exit codes

Every run ends with one `RESULT=` line, which is also written to the job summary.

| Result               | Meaning                                                   | Exit |
| -------------------- | --------------------------------------------------------- | ---- |
| `POSTED`             | SUCCESS: new article posted                               | 0    |
| `ALREADY_POSTED`     | NOOP: article already on Reddit                           | 0    |
| `NO_NEW_ARTICLE`     | NOOP: newest issue too old or future-dated                | 0    |
| `DRY_RUN`            | NOOP: dry run                                             | 0    |
| `CONFIG`             | ERROR: missing or invalid configuration (names the keys)  | 2    |
| `RSS_UNAVAILABLE`    | ERROR: feed unreachable after retries                     | 10   |
| `RSS_MALFORMED`      | ERROR: feed not valid RSS, or newest item links off-site  | 11   |
| `REDDIT_AUTH`        | ERROR: Reddit refused the credentials                     | 20   |
| `REDDIT_REJECTED`    | ERROR: Reddit refused the post (403, submit error code)   | 21   |
| `RATE_LIMITED`       | ERROR: still rate limited after retries                   | 22   |
| `REDDIT_UNAVAILABLE` | ERROR: Reddit 5xx or network failure after retries        | 23   |
| `UNEXPECTED`         | ERROR: unexpected exception (traceback in log, scrubbed)  | 1    |

Transient failures (feed 5xx, Reddit 429 or 5xx, timeouts) are retried up
to 3 times with exponential backoff: 2s, 4s, 8s. A `Retry-After` header is
honoured, capped at 60s. There is no endless retrying.

## Testing

```bash
cd reddit
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest
```

Every HTTP call in the tests goes through `responses`, and any request
without a stub raises. No test can reach Reddit or post anything. CI runs
the same suite on every PR that touches `reddit/`.

## Local execution

```bash
cd reddit
cp .env.example .env        # fill in; never commit it
set -a; . ./.env; set +a
PYTHONPATH=src .venv/bin/python -m maczine_reddit
```

`DRY_RUN` defaults to `true` when unset, so a local run posts only when
you set `DRY_RUN=false` explicitly.

## Troubleshooting

**Approval still pending.** Only dry runs work. Leave
`REDDIT_SCHEDULED_DRY_RUN` unset and the schedule stays green in dry-run
mode.

**`REDDIT_AUTH` / 401 / `invalid_grant`**
- The refresh token was revoked, or it was issued for a different client.
  This happens if the app was deleted, you revoked access under
  *Preferences → Apps*, or the secret was regenerated. Re-run
  `get_refresh_token.py`.
- *"lacks required scopes"*: the token was granted without
  `submit`/`read`/`history`. Re-run the helper.
- A 401 on the token request means `REDDIT_CLIENT_ID` or
  `REDDIT_CLIENT_SECRET` is wrong.

**`REDDIT_REJECTED` / 403 / `SUBREDDIT_NOTALLOWED`.** The bot is not allowed
to post there. Make it a moderator or approved user of the subreddit. The
same fix applies to `NO_LINKS`, which means the subreddit only allows text
posts: change that in the subreddit settings. `NOT_FOUND` means
`REDDIT_SUBREDDIT` or `REDDIT_USERNAME` is misspelt.

**`RATE_LIMITED` / 429 / `RATELIMIT`.** This job makes fewer than 20
requests a day, so a rate limit usually means a new, low-karma account.
Reddit throttles those accounts' posting ("you are doing that too much").
Moderator status in the subreddit removes the throttle. The next
scheduled run retries automatically.

**`RSS_UNAVAILABLE` / `RSS_MALFORMED`.** Check that
<https://www.mactechsolutionsllc.com/maczine/feed.xml> loads in a browser.
The job posts nothing when the feed looks wrong. Once the site is fixed,
re-run the workflow manually. The issue still posts as long as it is under
`MAX_ARTICLE_AGE_HOURS` old.

**Duplicate behaviour.** Re-running is always safe. If an issue was posted
by hand, the job finds it through Reddit's URL index and does nothing.
Reposting on purpose is not supported: delete the old post, or post it
manually.

**GitHub scheduler delay.** Scheduled runs often start late at peak, and
sometimes by more than an hour. That is why there are five runs, ending
at 10:30. If a whole morning is missed, run the workflow manually with
**dry_run** unticked. GitHub also disables schedules in a public repo
after 60 days with no repository activity. MacZine commits daily, so this
does not happen in practice, but it is the first thing to check if runs
stop appearing.

**`NO_NEW_ARTICLE` on a weekday.** The newest issue is older than
`MAX_ARTICLE_AGE_HOURS`, so nothing was released today. Check the queue in
`articles/` for a missing or draft issue. The `verify-published` workflow
flags that too.
