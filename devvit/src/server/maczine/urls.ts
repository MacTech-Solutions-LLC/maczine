/**
 * URL handling, so the same article compares equal however it was written.
 *
 * Pure functions: no Devvit runtime, so they can be unit tested directly.
 */

export const ALLOWED_HOSTS = ['mactechsolutionsllc.com', 'www.mactechsolutionsllc.com'];
export const ARTICLE_PATH_PREFIX = '/maczine/';

const TRACKING_EXACT = new Set([
  'fbclid',
  'gclid',
  'dclid',
  'msclkid',
  'ref',
  'ref_src',
  'igshid',
  'yclid',
]);
const TRACKING_PREFIXES = ['utm_', 'mc_'];

const isTracking = (key: string): boolean => {
  const k = key.toLowerCase();
  return TRACKING_EXACT.has(k) || TRACKING_PREFIXES.some((p) => k.startsWith(p));
};

const parse = (url: string): URL | undefined => {
  try {
    return new URL(url.trim());
  } catch {
    return undefined;
  }
};

const cleanQuery = (url: URL): string => {
  const kept = [...url.searchParams.entries()].filter(([k]) => !isTracking(k));
  kept.sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0));
  const params = new URLSearchParams(kept);
  const query = params.toString();
  return query ? `?${query}` : '';
};

/**
 * The comparison key: https, bare lowercase host, no trailing slash, no
 * fragment, no tracking parameters, remaining parameters sorted. Returns ''
 * for anything unparseable, which never equals a real article.
 */
export const normalizeUrl = (url: string): string => {
  const parsed = parse(url);
  if (!parsed) return '';
  const host = parsed.hostname.toLowerCase().replace(/^www\./, '');
  const port = parsed.port && parsed.port !== '80' && parsed.port !== '443' ? `:${parsed.port}` : '';
  const path = parsed.pathname.replace(/\/+$/, '');
  return `https://${host}${port}${path}${cleanQuery(parsed)}`;
};

/**
 * The URL actually submitted: the feed link as published, forced to https,
 * without tracking parameters, fragment or trailing slash. The host is kept
 * as-is so the post points at the exact live address.
 */
export const canonicalUrl = (url: string): string => {
  const parsed = parse(url);
  if (!parsed) return '';
  const path = parsed.pathname.replace(/\/+$/, '');
  return `https://${parsed.host.toLowerCase()}${path}${cleanQuery(parsed)}`;
};

/** True only for an article page on MacTech's own site. */
export const isMacZineArticle = (url: string): boolean => {
  const parsed = parse(url);
  if (!parsed) return false;
  if (parsed.protocol !== 'https:' && parsed.protocol !== 'http:') return false;
  if (!ALLOWED_HOSTS.includes(parsed.hostname.toLowerCase())) return false;
  if (parsed.port && parsed.port !== '80' && parsed.port !== '443') return false;
  if (!parsed.pathname.startsWith(ARTICLE_PATH_PREFIX)) return false;
  const slug = parsed.pathname.slice(ARTICLE_PATH_PREFIX.length).replace(/^\/+|\/+$/g, '');
  return slug.length > 0 && slug !== 'feed.xml';
};

/** Do two URLs point at the same article? */
export const sameArticle = (a: string, b: string): boolean => {
  const left = normalizeUrl(a);
  return left !== '' && left === normalizeUrl(b);
};
