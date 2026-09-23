import assert from 'node:assert/strict';
import { describe, it } from 'node:test';

import {
  FeedMalformedError,
  FeedUnavailableError,
  fetchFeed,
  parseFeed,
  selectLatest,
  type Article,
} from './feed.ts';

const item = (title: string, slug: string, pubDate: string): string => `
  <item>
    <title>${title}</title>
    <link>https://www.mactechsolutionsllc.com/maczine/${slug}</link>
    <guid isPermaLink="true">https://www.mactechsolutionsllc.com/maczine/${slug}</guid>
    <description>d</description>
    <pubDate>${pubDate}</pubDate>
  </item>`;

const feed = (...items: string[]): string =>
  `<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel>
     <title>MacZine</title>${items.join('')}</channel></rss>`;

const TODAY = item('Issue Nº 040 - Vulnerability Scanning', 'vulnerability-scanning', 'Tue, 22 Sep 2026 12:00:00 GMT');
const YESTERDAY = item('Issue Nº 039 - Tabletop', 'tabletop', 'Mon, 21 Sep 2026 12:00:00 GMT');
const TODAY_URL = 'https://www.mactechsolutionsllc.com/maczine/vulnerability-scanning';

// Tuesday 08:05 Pacific, the first scheduled run of the morning.
const NOW = new Date('2026-09-22T15:05:00Z');

const article = (selection: ReturnType<typeof selectLatest>): Article => {
  assert.equal(selection.kind, 'article');
  assert.ok(selection.kind === 'article');
  return selection.article;
};

describe('parseFeed', () => {
  it('reads title, link, guid, date and description', () => {
    const articles = parseFeed(feed(TODAY, YESTERDAY));
    assert.equal(articles.length, 2);
    assert.equal(articles[0]!.title, 'Issue Nº 040 - Vulnerability Scanning');
    assert.equal(articles[0]!.url, TODAY_URL);
    assert.equal(articles[0]!.guid, TODAY_URL);
    assert.equal(articles[0]!.published.toISOString(), '2026-09-22T12:00:00.000Z');
    assert.equal(articles[0]!.description, 'd');
  });

  it('handles the production feed shape: namespaces, CDATA and entities', () => {
    const xml = `<?xml version="1.0" encoding="UTF-8"?>
      <rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
        <channel><title>MacZine</title>
          <atom:link href="https://www.mactechsolutionsllc.com/maczine/feed.xml" rel="self"/>
          <item>
            <title>Issue N&#186; 040 - A &amp; B</title>
            <link>https://www.mactechsolutionsllc.com/maczine/a-and-b</link>
            <guid isPermaLink="true">https://www.mactechsolutionsllc.com/maczine/a-and-b</guid>
            <content:encoded><![CDATA[<p>body</p>]]></content:encoded>
            <pubDate>Tue, 22 Sep 2026 12:00:00 GMT</pubDate>
            <dc:creator xmlns:dc="http://purl.org/dc/elements/1.1/">Patrick</dc:creator>
          </item>
        </channel></rss>`;
    const articles = parseFeed(xml);
    assert.equal(articles.length, 1);
    assert.equal(articles[0]!.title, 'Issue Nº 040 - A & B');
  });

  it('converts a numeric-offset pubDate to UTC', () => {
    const [a] = parseFeed(feed(item('T', 's', 'Tue, 22 Sep 2026 08:00:00 -0400')));
    assert.equal(a!.published.toISOString(), '2026-09-22T12:00:00.000Z');
  });

  it('skips unusable items but keeps the good ones', () => {
    const articles = parseFeed(feed(item('T', 's', 'garbage'), YESTERDAY));
    assert.deepEqual(
      articles.map((a) => a.title),
      ['Issue Nº 039 - Tabletop']
    );
  });

  const bad: [string, string][] = [
    ['not xml at all', 'plain text'],
    ['<html><body>502 Bad Gateway</body></html>', 'an error page'],
    ["<rss version='2.0'><channel></channel></rss>", 'no items'],
    [feed('<item><title>no link</title></item>'), 'no usable items'],
    [feed(item('T', 's', 'not a date')), 'no valid dates'],
  ];
  for (const [xml, label] of bad) {
    it(`refuses ${label}`, () => {
      assert.throws(() => parseFeed(xml), FeedMalformedError);
    });
  }
});

describe('selectLatest', () => {
  it('picks the newest by date, not by feed order', () => {
    assert.equal(article(selectLatest(parseFeed(feed(YESTERDAY, TODAY)), NOW)).url, TODAY_URL);
  });

  it('still posts later the same day when an earlier run was missed', () => {
    const late = new Date('2026-09-22T23:00:00Z');
    assert.equal(article(selectLatest(parseFeed(feed(TODAY)), late)).url, TODAY_URL);
  });

  it("does not repost Friday's issue on Monday", () => {
    const friday = parseFeed(feed(item('Fri', 'fri', 'Fri, 18 Sep 2026 12:00:00 GMT')));
    const monday = new Date('2026-09-21T15:05:00Z');
    assert.equal(selectLatest(friday, monday).kind, 'none');
  });

  it('ignores an article dated in the future', () => {
    const tomorrow = parseFeed(feed(item('Tomorrow', 't', 'Wed, 23 Sep 2026 12:00:00 GMT')));
    assert.equal(selectLatest(tomorrow, NOW).kind, 'none');
  });

  it('tolerates a few minutes of clock skew', () => {
    const justBefore = new Date('2026-09-22T11:55:00Z');
    assert.equal(selectLatest(parseFeed(feed(TODAY)), justBefore).kind, 'article');
  });

  it('fails closed when the newest item links off-site', () => {
    const xml = feed(
      `<item><title>x</title><link>https://evil.example/maczine/x</link>
       <pubDate>Tue, 22 Sep 2026 12:00:00 GMT</pubDate></item>`
    );
    assert.throws(() => selectLatest(parseFeed(xml), NOW), FeedMalformedError);
  });
});

describe('fetchFeed', () => {
  const noWait = async (): Promise<void> => {};
  const response = (status: number, body = ''): Response => new Response(body, { status });

  it('retries a 5xx and then succeeds', async () => {
    const statuses = [500, 503, 200];
    let calls = 0;
    const fetcher = async (): Promise<Response> => {
      const status = statuses[calls++]!;
      return response(status, status === 200 ? feed(TODAY) : 'error');
    };
    const xml = await fetchFeed(fetcher, 'https://example.com/feed.xml', 3, noWait);
    assert.match(xml, /Vulnerability/);
    assert.equal(calls, 3);
  });

  it('gives up after the last attempt', async () => {
    const fetcher = async (): Promise<Response> => response(502);
    await assert.rejects(() => fetchFeed(fetcher, 'https://example.com/feed.xml', 2, noWait), FeedUnavailableError);
  });

  it('does not retry a 404', async () => {
    let calls = 0;
    const fetcher = async (): Promise<Response> => {
      calls++;
      return response(404);
    };
    await assert.rejects(() => fetchFeed(fetcher, 'https://example.com/feed.xml', 3, noWait), FeedUnavailableError);
    assert.equal(calls, 1);
  });

  it('retries a thrown network error', async () => {
    let calls = 0;
    const fetcher = async (): Promise<Response> => {
      calls++;
      if (calls === 1) throw new Error('network down');
      return response(200, feed(TODAY));
    };
    assert.match(await fetchFeed(fetcher, 'https://example.com/feed.xml', 3, noWait), /Vulnerability/);
    assert.equal(calls, 2);
  });
});
