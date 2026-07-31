#!/usr/bin/env node
// Verify that every article whose publish date has arrived is actually
// live on the site.
//
// Publication is date-gated: the site shows an article once its
// `publishedAt` is in the past, so nothing needs to run for a piece to
// go live. This script exists for the failures that gating cannot
// prevent — the PR never got merged, the sync webhook dropped a push,
// a deploy broke the route. Those are silent, and a queued article
// nobody notices is missing is the whole risk of scheduling ahead.
//
// Exits non-zero when something that should be live is not.

import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs'
import { join } from 'node:path'
import matter from 'gray-matter'

const SITE = process.env.MACZINE_SITE_URL || 'https://www.mactechsolutionsllc.com'
const ARTICLES = join(process.cwd(), 'articles')

// Compare dates only. `publishedAt` carries a specific release time
// (8:00 AM Pacific), but this script only needs to know whether that
// day has arrived — the workflow's cron already runs late enough in
// the day (16:20 UTC) that anything dated today has cleared its gate.
const today = new Date()
today.setUTCHours(23, 59, 59, 999)

const expected = []
for (const slug of readdirSync(ARTICLES)) {
  if (!statSync(join(ARTICLES, slug)).isDirectory()) continue
  const file = join(ARTICLES, slug, 'index.md')
  if (!existsSync(file)) continue

  const { data } = matter(readFileSync(file, 'utf8'))
  if (data.draft === true) continue

  const publishedAt = new Date(data.publishedAt)
  if (Number.isNaN(publishedAt.getTime()) || publishedAt > today) continue

  // YAML parses a bare date into a Date; keep the ISO day for output.
  expected.push({
    slug,
    issue: data.issue ?? null,
    publishedAt: publishedAt.toISOString().split('T')[0],
  })
}

expected.sort((a, b) => (a.issue ?? 0) - (b.issue ?? 0))

const missing = []
for (const article of expected) {
  const url = `${SITE}/maczine/${article.slug}`
  let status = 0
  try {
    const res = await fetch(url, {
      redirect: 'follow',
      signal: AbortSignal.timeout(20_000),
    })
    status = res.status
  } catch (err) {
    status = `error: ${err.message}`
  }
  const ok = status === 200
  const num = article.issue ? String(article.issue).padStart(3, '0') : ' — '
  console.log(`${ok ? 'ok  ' : 'MISS'}  ${num}  ${article.publishedAt}  ${article.slug}  (${status})`)
  if (!ok) missing.push({ ...article, status })
}

console.log(`\n${expected.length} article(s) past their publish date — ${missing.length} not live`)

if (missing.length > 0) {
  console.error(
    '\nThese articles should be live and are not. Usual causes, in order of' +
      '\nlikelihood: the PR was never merged, the site sync webhook missed the' +
      '\npush (re-push to retrigger), or the site deploy is failing.\n',
  )
  for (const m of missing) console.error(`  ${m.slug} — due ${m.publishedAt} — ${m.status}`)
  process.exit(1)
}
