# MacZine poster

A scheduled app that posts MacTech Solutions' own daily newsletter, MacZine, to
the MacTech community as a link post. It is installed by the MacTech moderator
team on their own subreddit to syndicate the community's own newsletter. It has
no user interface: it reads one RSS feed and submits at most one link post per
weekday.

## What it does

MacZine publishes one article every weekday. Each weekday morning the app:

1. Reads the MacZine RSS feed.
2. Takes the newest article by publication date, and stops unless that article
   is under 36 hours old, is not dated in the future, and is on
   mactechsolutionsllc.com's `/maczine/` path.
3. Checks whether that article is already in the subreddit, both in its own
   record of what it posted and in the subreddit's recent posts, so an article
   a moderator posted by hand is recognised too.
4. If it is not there, submits a link post: the article's exact title, the
   article's URL, nothing else. No comment, no promotional text.
5. Logs the outcome.

The scheduled task runs several times each weekday morning, because the first
run may find nothing (a late publication) and because a missed run should still
be recoverable. Only the first run of a morning posts. Every run after it finds
the post and does nothing.

## Why it needs fetch

The article's title and URL exist only in the MacZine RSS feed. There is no way
to learn what today's article is from inside Reddit, so the app has to read the
feed. It is a public, unauthenticated, standards-formatted syndication feed for
the publication this app posts, served by the same organisation that operates
the app and moderates the destination subreddit. Nothing is sent outward: the
app makes one HTTP GET and reads the response.

## Fetch Domains

The following domain is requested for this app:

- `www.mactechsolutionsllc.com` — the MacZine RSS feed
  (`https://www.mactechsolutionsllc.com/maczine/feed.xml`), read once per
  scheduled run to get the title and URL of the newest article. It is a public
  RSS 2.0 feed belonging to MacTech Solutions LLC, who operate this app. The
  request is a plain GET. No user data, no Reddit data and no request body is
  ever sent to this domain.

Terms: https://www.mactechsolutionsllc.com/terms

Privacy Policy: https://www.mactechsolutionsllc.com/privacy

## Installing and configuring

1. Install the app on the subreddit you moderate.
2. Open the app's install settings. All of them are optional:

| Setting | Default | What it does |
| --- | --- | --- |
| MacZine RSS feed URL | the MacZine feed | The feed to read. Must be https, and its host must be an allow-listed domain. |
| Post flair template ID | empty | Flair applied to the post. Blank means no flair. |
| Dry run | off | When on, the app reads the feed and logs what it would post, without posting. Useful right after install. |

3. Optionally use the subreddit menu item **Post the latest MacZine issue** to
   run it once by hand and confirm the result.

The schedule then runs by itself. No other maintenance is needed.

## How moderators control it

- Turn on **Dry run** to stop it posting without uninstalling it.
- Use the menu item to post an issue immediately if a morning was missed.
- Uninstall to stop it entirely.

Posts are created by this app's account, which installation makes a moderator
of the subreddit. The app never posts as a user, and it never reads or stores
anything about the people in the subreddit.

## Data it stores

One Redis key per posted article URL, holding the permalink of the post it
created, so a later run the same morning does not post the same article twice.
Keys expire after 180 days. No user data of any kind is stored.

## Outcomes in the logs

Every run logs the time it fired and one `RESULT=` line:

| Result | Meaning |
| --- | --- |
| `POSTED` | A new article was posted; the permalink follows. |
| `ALREADY_POSTED` | The article is already in the subreddit. Nothing was done. |
| `NO_NEW_ARTICLE` | The newest article is too old, or dated in the future. |
| `DRY_RUN` | Dry run is on; the run says what it would have posted. |
| `FEED_UNAVAILABLE` | The feed could not be read after retries. Nothing was posted. |
| `FEED_MALFORMED` | The feed was not usable RSS, or its newest item linked off-site. |
| `POST_REJECTED` | Reddit refused the post; the error follows. |

Transient failures (5xx, timeouts) are retried up to three times with
exponential backoff, then left until the next scheduled run.

## Development

```bash
npm install
npm run test:unit    # 54 tests, no network
npm run test:types
npm run lint
npm run build
npm run dev          # devvit playtest, needs a test subreddit under 200 members
```

The feed parsing, freshness window, URL comparison and posting decision live in
`src/server/maczine/` as plain functions with every Reddit and Redis call
injected, so they are tested without the Devvit runtime. `src/server/index.ts`
is only the wiring: the scheduled task, the moderator menu item, and the real
clients.

Uploading: `npm run deploy` runs the type-check, the linter and `devvit upload`.
