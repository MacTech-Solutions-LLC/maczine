/**
 * One run: read the feed, decide, check for a duplicate, post.
 *
 * Every Reddit and Redis call comes in through `PosterDeps`, so the whole
 * decision path is unit tested with fakes and no Devvit runtime.
 */

import {
  FeedMalformedError,
  FeedUnavailableError,
  fetchFeed,
  parseFeed,
  selectLatest,
  type Article,
} from './feed.ts';
import { normalizeUrl } from './urls.ts';

/** How long to remember that a URL was posted. Comfortably past the age window. */
const MEMORY_SECONDS = 60 * 60 * 24 * 180;

export type PostedPost = {
  readonly id: string;
  readonly url?: string;
  readonly permalink?: string;
};

export type PosterDeps = {
  readonly subredditName: string;
  readonly fetchText: () => Promise<string>;
  readonly recentPosts: () => Promise<readonly PostedPost[]>;
  readonly submitLink: (opts: {
    subredditName: string;
    title: string;
    url: string;
    flairId?: string;
  }) => Promise<PostedPost>;
  readonly remember: (key: string, value: string, ttlSeconds: number) => Promise<void>;
  readonly recall: (key: string) => Promise<string | undefined>;
  readonly now?: Date;
  readonly dryRun?: boolean;
  readonly flairId?: string;
  readonly maxAgeHours?: number;
};

export type Outcome = {
  readonly status:
    | 'POSTED'
    | 'ALREADY_POSTED'
    | 'NO_NEW_ARTICLE'
    | 'DRY_RUN'
    | 'FEED_UNAVAILABLE'
    | 'FEED_MALFORMED'
    | 'POST_REJECTED';
  readonly message: string;
  readonly article?: Article;
  readonly permalink?: string;
};

const ok = (status: Outcome['status']): boolean =>
  status === 'POSTED' || status === 'ALREADY_POSTED' || status === 'NO_NEW_ARTICLE' || status === 'DRY_RUN';

export const isSuccess = (outcome: Outcome): boolean => ok(outcome.status);

const memoryKey = (url: string): string => `posted:${normalizeUrl(url)}`;

const permalinkOf = (post: PostedPost): string =>
  post.permalink?.startsWith('/') ? `https://www.reddit.com${post.permalink}` : (post.permalink ?? post.id);

/**
 * Has this article already been posted?
 *
 * Two independent sources, so one of them missing it is not enough to cause a
 * duplicate: what this app remembers posting, and what is actually in the
 * subreddit right now (which also catches posts made by hand).
 */
const findExisting = async (deps: PosterDeps, url: string): Promise<string | undefined> => {
  const remembered = await deps.recall(memoryKey(url));
  if (remembered) return remembered;

  const target = normalizeUrl(url);
  for (const post of await deps.recentPosts()) {
    if (post.url && normalizeUrl(post.url) === target) return permalinkOf(post);
  }
  return undefined;
};

export const runPoster = async (deps: PosterDeps): Promise<Outcome> => {
  const now = deps.now ?? new Date();

  let articles: Article[];
  try {
    articles = parseFeed(await deps.fetchText());
  } catch (error) {
    if (error instanceof FeedUnavailableError) {
      return { status: 'FEED_UNAVAILABLE', message: error.message };
    }
    if (error instanceof FeedMalformedError) {
      return { status: 'FEED_MALFORMED', message: error.message };
    }
    throw error;
  }

  let selection;
  try {
    selection = selectLatest(articles, now, deps.maxAgeHours);
  } catch (error) {
    if (error instanceof FeedMalformedError) {
      return { status: 'FEED_MALFORMED', message: error.message };
    }
    throw error;
  }
  if (selection.kind === 'none') {
    return { status: 'NO_NEW_ARTICLE', message: selection.reason };
  }

  const article = selection.article;
  const existing = await findExisting(deps, article.url);
  if (existing) {
    return {
      status: 'ALREADY_POSTED',
      message: 'Article already posted; no action required.',
      article,
      permalink: existing,
    };
  }

  if (deps.dryRun) {
    return {
      status: 'DRY_RUN',
      message: `Would post "${article.title}" (${article.url}) to r/${deps.subredditName}`,
      article,
    };
  }

  let post: PostedPost;
  try {
    post = await deps.submitLink({
      subredditName: deps.subredditName,
      title: article.title,
      url: article.url,
      ...(deps.flairId ? { flairId: deps.flairId } : {}),
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    // The post may have landed before the error; never blindly resubmit.
    const landed = await findExisting(deps, article.url);
    if (landed) {
      return {
        status: 'ALREADY_POSTED',
        message: `submit reported an error (${message}) but the post is there`,
        article,
        permalink: landed,
      };
    }
    return { status: 'POST_REJECTED', message, article };
  }

  const permalink = permalinkOf(post);
  await deps.remember(memoryKey(article.url), permalink, MEMORY_SECONDS);
  return { status: 'POSTED', message: 'Reddit submission successful.', article, permalink };
};

/** The real feed fetcher. The URL must be on the app's allow-listed domain. */
export const liveFetchText = async (feedUrl?: string): Promise<string> =>
  feedUrl ? fetchFeed(fetch, feedUrl) : fetchFeed();
