/**
 * Read the MacZine RSS feed and decide which issue, if any, should be posted.
 *
 * Pure apart from `fetchFeed`, which takes the fetcher as an argument, so all
 * of it can be unit tested without the Devvit runtime.
 */

import { XMLParser } from 'fast-xml-parser';

import { canonicalUrl, isMacZineArticle } from './urls.ts';

export const FEED_URL = 'https://www.mactechsolutionsllc.com/maczine/feed.xml';

/** How long after publication an issue still counts as new. */
export const MAX_ARTICLE_AGE_HOURS = 36;

/** A feed stamped slightly ahead of our clock is fine; further out is not. */
const FUTURE_TOLERANCE_MS = 10 * 60 * 1000;

const FETCH_TIMEOUT_MS = 15_000;
const FETCH_ATTEMPTS = 3;

export type Article = {
  readonly title: string;
  readonly url: string;
  readonly guid: string;
  readonly published: Date;
  readonly description: string;
};

export class FeedUnavailableError extends Error {}
export class FeedMalformedError extends Error {}

type Fetcher = (url: string, init?: RequestInit) => Promise<Response>;

const sleep = (ms: number): Promise<void> => new Promise((resolve) => setTimeout(resolve, ms));

/** GET the feed, retrying timeouts, 429 and 5xx with exponential backoff. */
export const fetchFeed = async (
  fetcher: Fetcher = fetch,
  url: string = FEED_URL,
  attempts: number = FETCH_ATTEMPTS,
  wait: (ms: number) => Promise<void> = sleep
): Promise<string> => {
  let reason = 'feed request failed';
  for (let attempt = 1; attempt <= attempts; attempt++) {
    try {
      const response = await fetcher(url, {
        headers: { accept: 'application/rss+xml, application/xml' },
        signal: AbortSignal.timeout(FETCH_TIMEOUT_MS),
      });
      if (response.ok) return await response.text();
      // 4xx other than 429 will not fix itself; fail now.
      if (response.status !== 429 && response.status < 500) {
        throw new FeedUnavailableError(`feed returned HTTP ${response.status}`);
      }
      reason = `feed returned HTTP ${response.status}`;
    } catch (error) {
      if (error instanceof FeedUnavailableError) throw error;
      reason = `feed request failed (${error instanceof Error ? error.name : 'unknown'})`;
    }
    if (attempt === attempts) break;
    const delay = 2000 * 2 ** (attempt - 1);
    console.warn(`${reason}; retrying in ${delay / 1000}s (attempt ${attempt + 1} of ${attempts})`);
    await wait(delay);
  }
  throw new FeedUnavailableError(reason);
};

const text = (value: unknown): string => {
  if (typeof value === 'string') return value.trim();
  if (typeof value === 'number') return String(value);
  // fast-xml-parser gives { '#text': ..., '@_attr': ... } for elements with attributes
  if (value && typeof value === 'object' && '#text' in value) {
    return text((value as Record<string, unknown>)['#text']);
  }
  return '';
};

const asArray = (value: unknown): unknown[] =>
  value === undefined || value === null ? [] : Array.isArray(value) ? value : [value];

/** Parse RSS 2.0. Throws FeedMalformedError when nothing usable is in it. */
export const parseFeed = (xml: string): Article[] => {
  let parsed: Record<string, unknown>;
  try {
    parsed = new XMLParser({
      ignoreAttributes: false,
      attributeNamePrefix: '@_',
      processEntities: true,
      htmlEntities: true,
      trimValues: true,
    }).parse(xml) as Record<string, unknown>;
  } catch (error) {
    throw new FeedMalformedError(
      `feed is not valid XML: ${error instanceof Error ? error.message : 'unknown error'}`
    );
  }

  const rss = parsed?.['rss'] as Record<string, unknown> | undefined;
  const channel = rss?.['channel'] as Record<string, unknown> | undefined;
  if (!channel) throw new FeedMalformedError('feed is not RSS 2.0 (no <rss><channel>)');

  const items = asArray(channel['item']) as Record<string, unknown>[];
  if (items.length === 0) throw new FeedMalformedError('feed contains no items');

  const articles: Article[] = [];
  items.forEach((item, index) => {
    const title = text(item['title']).replace(/\s+/g, ' ');
    const link = text(item['link']);
    const published = new Date(text(item['pubDate']));
    if (!title || !link || Number.isNaN(published.getTime())) {
      console.warn(`skipping feed item ${index}: missing title, link or valid pubDate`);
      return;
    }
    articles.push({
      title,
      url: canonicalUrl(link),
      guid: text(item['guid']) || link,
      published,
      description: text(item['description']),
    });
  });

  if (articles.length === 0) {
    throw new FeedMalformedError('feed has items but none with a title, link and valid pubDate');
  }
  return articles;
};

export type Selection =
  | { readonly kind: 'article'; readonly article: Article }
  | { readonly kind: 'none'; readonly reason: string };

/**
 * The newest article if it is current enough to post.
 *
 * Newest is decided by pubDate, not feed order. An article that is too old,
 * dated in the future, or not on MacZine's path is never returned: when in
 * doubt, post nothing.
 */
export const selectLatest = (
  articles: readonly Article[],
  now: Date = new Date(),
  maxAgeHours: number = MAX_ARTICLE_AGE_HOURS
): Selection => {
  const latest = articles.reduce((best, a) => (a.published > best.published ? a : best));
  if (!isMacZineArticle(latest.url)) {
    throw new FeedMalformedError(`newest item links outside MacZine: ${latest.url}`);
  }
  const ageMs = now.getTime() - latest.published.getTime();
  if (ageMs < -FUTURE_TOLERANCE_MS) {
    return {
      kind: 'none',
      reason: `newest article is dated in the future (${latest.published.toISOString()})`,
    };
  }
  if (ageMs > maxAgeHours * 3600 * 1000) {
    const hours = (ageMs / 3600000).toFixed(1);
    return { kind: 'none', reason: `newest article is ${hours}h old, over the ${maxAgeHours}h limit` };
  }
  return { kind: 'article', article: latest };
};
