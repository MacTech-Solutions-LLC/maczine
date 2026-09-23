import assert from 'node:assert/strict';
import { describe, it } from 'node:test';

import { runPoster, type PostedPost, type PosterDeps } from './poster.ts';

const TODAY_URL = 'https://www.mactechsolutionsllc.com/maczine/vulnerability-scanning';
const TITLE = 'Issue Nº 040 - Vulnerability Scanning';
const NOW = new Date('2026-09-22T15:05:00Z');

const feed = (pubDate = 'Tue, 22 Sep 2026 12:00:00 GMT', slug = 'vulnerability-scanning'): string =>
  `<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>MacZine</title>
     <item><title>${TITLE}</title>
       <link>https://www.mactechsolutionsllc.com/maczine/${slug}</link>
       <pubDate>${pubDate}</pubDate></item>
   </channel></rss>`;

type Harness = {
  deps: PosterDeps;
  submitted: { title: string; url: string; flairId?: string }[];
  memory: Map<string, string>;
};

const harness = (overrides: Partial<PosterDeps> = {}, subredditPosts: PostedPost[] = []): Harness => {
  const submitted: Harness['submitted'] = [];
  const memory = new Map<string, string>();
  const posts = [...subredditPosts];

  const deps: PosterDeps = {
    subredditName: 'MacZine',
    now: NOW,
    fetchText: async () => feed(),
    recentPosts: async () => posts,
    submitLink: async (opts) => {
      submitted.push({ title: opts.title, url: opts.url, ...(opts.flairId ? { flairId: opts.flairId } : {}) });
      const post: PostedPost = { id: 't3_new1', url: opts.url, permalink: '/r/MacZine/comments/new1/x/' };
      posts.push(post);
      return post;
    },
    remember: async (key, value) => void memory.set(key, value),
    recall: async (key) => memory.get(key),
    ...overrides,
  };
  return { deps, submitted, memory };
};

describe('runPoster', () => {
  it('posts a new article as a link post', async () => {
    const { deps, submitted, memory } = harness();
    const outcome = await runPoster(deps);

    assert.equal(outcome.status, 'POSTED');
    assert.equal(outcome.permalink, 'https://www.reddit.com/r/MacZine/comments/new1/x/');
    assert.deepEqual(submitted, [{ title: TITLE, url: TODAY_URL }]);
    assert.equal(memory.size, 1);
  });

  it('passes the flair through when one is configured', async () => {
    const { deps, submitted } = harness({ flairId: 'flair-1' });
    await runPoster(deps);
    assert.equal(submitted[0]!.flairId, 'flair-1');
  });

  it('does nothing on a second run the same morning', async () => {
    const { deps, submitted } = harness();
    assert.equal((await runPoster(deps)).status, 'POSTED');

    const second = await runPoster(deps);
    assert.equal(second.status, 'ALREADY_POSTED');
    assert.equal(submitted.length, 1);
  });

  it('finds a post made by hand, even with a messier URL', async () => {
    const byHand: PostedPost = {
      id: 't3_hand',
      url: `${TODAY_URL}/?utm_source=newsletter`,
      permalink: '/r/MacZine/comments/hand/x/',
    };
    const { deps, submitted } = harness({}, [byHand]);

    const outcome = await runPoster(deps);
    assert.equal(outcome.status, 'ALREADY_POSTED');
    assert.equal(outcome.permalink, 'https://www.reddit.com/r/MacZine/comments/hand/x/');
    assert.equal(submitted.length, 0);
  });

  it('does not treat a different article as a duplicate', async () => {
    const other: PostedPost = { id: 't3_other', url: `${TODAY_URL}-part-2`, permalink: '/r/MacZine/c/o/' };
    const { deps, submitted } = harness({}, [other]);
    assert.equal((await runPoster(deps)).status, 'POSTED');
    assert.equal(submitted.length, 1);
  });

  it('checks Reddit before retrying when the submit errors', async () => {
    const posts: PostedPost[] = [];
    const { deps, submitted } = harness({
      submitLink: async (opts) => {
        submittedCount++;
        posts.push({ id: 't3_landed', url: opts.url, permalink: '/r/MacZine/comments/landed/x/' });
        throw new Error('502 Bad Gateway');
      },
      recentPosts: async () => posts,
    });
    let submittedCount = 0;

    const outcome = await runPoster(deps);
    assert.equal(outcome.status, 'ALREADY_POSTED');
    assert.match(outcome.message, /502/);
    assert.equal(submittedCount, 1);
    assert.equal(submitted.length, 0);
  });

  it('reports a genuine rejection', async () => {
    const { deps } = harness({
      submitLink: async () => {
        throw new Error('SUBREDDIT_NOTALLOWED');
      },
    });
    const outcome = await runPoster(deps);
    assert.equal(outcome.status, 'POST_REJECTED');
    assert.match(outcome.message, /SUBREDDIT_NOTALLOWED/);
  });

  it('posts nothing when the newest issue is stale', async () => {
    const { deps, submitted } = harness({ fetchText: async () => feed('Fri, 18 Sep 2026 12:00:00 GMT', 'fri') });
    assert.equal((await runPoster(deps)).status, 'NO_NEW_ARTICLE');
    assert.equal(submitted.length, 0);
  });

  it('posts nothing when the feed is unreachable', async () => {
    const { deps, submitted } = harness({
      fetchText: async () => {
        const { FeedUnavailableError } = await import('./feed.ts');
        throw new FeedUnavailableError('feed returned HTTP 503');
      },
    });
    const outcome = await runPoster(deps);
    assert.equal(outcome.status, 'FEED_UNAVAILABLE');
    assert.equal(submitted.length, 0);
  });

  it('posts nothing when the feed is malformed', async () => {
    const { deps, submitted } = harness({ fetchText: async () => '<html>nope</html>' });
    assert.equal((await runPoster(deps)).status, 'FEED_MALFORMED');
    assert.equal(submitted.length, 0);
  });

  it('dry run checks for duplicates but never submits', async () => {
    const { deps, submitted } = harness({ dryRun: true });
    const outcome = await runPoster(deps);
    assert.equal(outcome.status, 'DRY_RUN');
    assert.match(outcome.message, /r\/MacZine/);
    assert.equal(submitted.length, 0);
  });
});
