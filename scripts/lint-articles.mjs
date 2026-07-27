#!/usr/bin/env node
/**
 * Frontmatter lint for MacZine articles. Mirrors the validation the
 * website's sync endpoint applies, so a green PR here can't fail to
 * publish there.
 *
 * Errors fail CI; warnings print but pass.
 */
import { readdirSync, readFileSync, statSync, existsSync } from 'node:fs'
import { join } from 'node:path'
import matter from 'gray-matter'

const ROOT = new URL('..', import.meta.url).pathname
const ARTICLES = join(ROOT, 'articles')
const SLUG_RE = /^[a-z0-9]+(?:-[a-z0-9]+)*$/

let errors = 0
let warnings = 0

const err = (slug, msg) => {
  console.error(`  ERROR  ${slug}: ${msg}`)
  errors++
}
const warn = (slug, msg) => {
  console.warn(`  warn   ${slug}: ${msg}`)
  warnings++
}

if (!existsSync(ARTICLES)) {
  console.error('articles/ directory not found')
  process.exit(1)
}

const dirs = readdirSync(ARTICLES).filter((d) =>
  statSync(join(ARTICLES, d)).isDirectory(),
)

for (const slug of dirs) {
  if (!SLUG_RE.test(slug)) {
    err(slug, 'directory name must be kebab-case (lowercase letters, digits, hyphens)')
  }

  const md = join(ARTICLES, slug, 'index.md')
  const mdx = join(ARTICLES, slug, 'index.mdx')
  const file = existsSync(md) ? md : existsSync(mdx) ? mdx : null
  if (!file) {
    err(slug, 'missing index.md')
    continue
  }

  let data, content
  try {
    ;({ data, content } = matter(readFileSync(file, 'utf8')))
  } catch (e) {
    err(slug, `frontmatter failed to parse: ${e.message}`)
    continue
  }

  for (const field of ['title', 'description', 'publishedAt']) {
    if (!data[field]) err(slug, `missing required frontmatter field: ${field}`)
  }
  if (data.publishedAt && Number.isNaN(new Date(data.publishedAt).getTime())) {
    err(slug, `publishedAt "${data.publishedAt}" is not a valid date`)
  }
  if (data.tags && !Array.isArray(data.tags)) {
    err(slug, 'tags must be a YAML list')
  }
  if (data.issue !== undefined && (!Number.isInteger(data.issue) || data.issue < 1)) {
    err(slug, `issue must be a positive integer, got "${data.issue}"`)
  }
  if (data.kicker !== undefined && typeof data.kicker !== 'string') {
    err(slug, 'kicker must be a string')
  }
  if (data.stats !== undefined) {
    if (!Array.isArray(data.stats) || data.stats.some((s) => !s || !s.n || !s.label)) {
      err(slug, 'stats must be a list of { n, label } entries')
    } else if (data.stats.length > 4) {
      warn(slug, `${data.stats.length} stats — the margin rail fits 3–4 comfortably`)
    }
  }
  if (data.asides !== undefined) {
    if (!Array.isArray(data.asides) || data.asides.some((a) => !a || !a.title || !a.body)) {
      err(slug, 'asides must be a list of { title, body } entries')
    }
  }

  if (data.title && String(data.title).length > 70) {
    warn(slug, `title is ${String(data.title).length} chars — Google truncates around 60–70`)
  }
  if (data.description && String(data.description).length > 160) {
    warn(slug, `description is ${String(data.description).length} chars — SERPs truncate around 155–160`)
  }
  if (content.trim().length < 300) {
    warn(slug, 'body is under 300 chars — thin content rarely ranks')
  }
  if (/^#\s/m.test(content)) {
    warn(slug, 'body contains an h1 (`# `) — the title already renders as h1; use `##`')
  }
}

console.log(
  `\n${dirs.length} article(s) checked — ${errors} error(s), ${warnings} warning(s)`,
)
process.exit(errors > 0 ? 1 : 0)
