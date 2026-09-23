import assert from 'node:assert/strict';
import { describe, it } from 'node:test';

import { canonicalUrl, isMacZineArticle, normalizeUrl, sameArticle } from './urls.ts';

const BASE = 'https://mactechsolutionsllc.com/maczine/slug';

describe('normalizeUrl', () => {
  const variants = [
    'https://www.mactechsolutionsllc.com/maczine/slug',
    'http://www.mactechsolutionsllc.com/maczine/slug',
    'https://mactechsolutionsllc.com/maczine/slug/',
    'https://WWW.MacTechSolutionsLLC.com/maczine/slug',
    'https://www.mactechsolutionsllc.com/maczine/slug?utm_source=reddit&utm_medium=social',
    'https://www.mactechsolutionsllc.com/maczine/slug?fbclid=abc&gclid=x&ref=hn',
    'https://www.mactechsolutionsllc.com/maczine/slug#section-2',
    '  https://www.mactechsolutionsllc.com/maczine/slug/?mc_cid=1#top ',
    'https://www.mactechsolutionsllc.com:443/maczine/slug',
  ];

  for (const url of variants) {
    it(`treats ${url.trim()} as the same article`, () => {
      assert.equal(normalizeUrl(url), BASE);
    });
  }

  it('keeps meaningful query parameters, sorted', () => {
    assert.equal(normalizeUrl('https://x.com/a?b=2&a=1&utm_x=9'), 'https://x.com/a?a=1&b=2');
  });

  it('keeps path case and does not conflate different slugs', () => {
    assert.notEqual(normalizeUrl(BASE), normalizeUrl(`${BASE}-part-2`));
    assert.equal(normalizeUrl('https://x.com/Maczine/Slug'), 'https://x.com/Maczine/Slug');
  });

  it('returns an empty string for junk, which never matches', () => {
    assert.equal(normalizeUrl('not a url'), '');
    assert.equal(sameArticle('not a url', 'also not a url'), false);
  });
});

describe('canonicalUrl', () => {
  it('keeps the published host but strips tracking, fragment and trailing slash', () => {
    assert.equal(
      canonicalUrl('http://www.mactechsolutionsllc.com/maczine/slug/?utm_source=x#f'),
      'https://www.mactechsolutionsllc.com/maczine/slug'
    );
  });
});

describe('isMacZineArticle', () => {
  const cases: [string, boolean][] = [
    ['https://www.mactechsolutionsllc.com/maczine/slug', true],
    ['https://mactechsolutionsllc.com/maczine/slug', true],
    ['https://www.mactechsolutionsllc.com/maczine', false],
    ['https://www.mactechsolutionsllc.com/maczine/', false],
    ['https://www.mactechsolutionsllc.com/maczine/feed.xml', false],
    ['https://www.mactechsolutionsllc.com/blog/slug', false],
    ['https://evil.example/maczine/slug', false],
    ['https://mactechsolutionsllc.com.evil.example/maczine/slug', false],
    ['ftp://www.mactechsolutionsllc.com/maczine/slug', false],
    ['https://www.mactechsolutionsllc.com:8443/maczine/slug', false],
  ];

  for (const [url, expected] of cases) {
    it(`${expected ? 'accepts' : 'rejects'} ${url}`, () => {
      assert.equal(isMacZineArticle(url), expected);
    });
  }
});
