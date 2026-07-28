# MacZine

Content repo for **MacZine**, the MacTech Solutions article newsletter,
published at [mactechsolutionsllc.com/maczine](https://www.mactechsolutionsllc.com/maczine).

This repo is the **source of truth** for articles. On every push to `main`,
a GitHub webhook triggers the website's `/api/maczine/sync` endpoint, which
mirrors `articles/` into the site's database and revalidates the pages.
Publishing never requires a website deploy.

## Publishing workflow

1. Branch, add `articles/<slug>/index.md`
2. Open a PR — CI lints the frontmatter
3. Merge to `main` — the article is live on the site within seconds

To unpublish, delete the article directory (or set `draft: true`) and merge.

## Article format

Each article is a directory under `articles/`. The directory name is the
URL slug (kebab-case, lowercase — it becomes
`mactechsolutionsllc.com/maczine/<slug>`, so make it keyword-rich and
date-free; changing it later breaks inbound links).

```
articles/
  cmmc-level-2-first-90-days/
    index.md        ← required
    cover.png       ← optional assets, referenced relatively
```

### Frontmatter

```yaml
---
title: The First 90 Days of a CMMC Level 2 Program   # required, ≤70 chars ideal
description: What to actually do first — scoping, …  # required, ≤160 chars ideal (this is the meta description)
publishedAt: 2026-07-26                               # required, YYYY-MM-DD
author: MacTech Solutions                             # optional, defaults to org
tags:                                                 # optional, lowercase
  - cmmc
  - nist-800-171
coverImage: ./cover.png                               # optional, relative or absolute
draft: false                                          # optional; true = not synced
issue: 3                                              # REQUIRED unless draft; "Issue Nº 003"
kicker: Field Report · Secure Communications          # optional; defaults to first tag
stats:                                                # optional; margin-rail big stats
  - n: "$0"
    label: per seat, per month, forever
asides:                                               # optional; margin-rail asides
  - title: Why "Freehold"
    body: A **freehold** is property held outright.
---
```

Body is GitHub-flavored Markdown. Relative image links
(`![diagram](./flow.png)`) resolve to this repo's raw content on the site.

### SEO notes

- `title` renders as the page `<title>` and the article h1 — front-load keywords
- `description` is the SERP meta description — write it for click-through
- Use `##` for section headings (the h1 is taken by the title)
- Internal links to the site (`/cmmc-level-2`, `/readiness`) pass link equity — use them

## The catalog: one numbered series

Every article that publishes is a numbered issue. There is no second
series — the old unnumbered "Field Notes" are gone, folded into the run.

- `issue:` is **required** on any article without `draft: true`. Lint
  fails a missing number and a duplicate one.
- Numbers run in **publication order** — `issue: 1` is the first piece
  MacZine ever ran, and the newest issue always holds the highest
  number. The site sorts the index by this field, so the numerals and
  the order a reader sees are the same thing.
- A number is **earned at publish**, not at authorship. A draft carries
  no `issue:`; it takes the next free one when it goes live (the Press
  Room's unhide action assigns it automatically). That is what keeps the
  printed run gap-free.
- Numbers are never reused and never reshuffled. To add a piece, take
  the next number — don't renumber anything to make room.

## Field copies (the press-room PDF)

Every article merged to `main` automatically gets a **field copy** — the
MacZine press-room layout (warm paper, ink navy, one burnt-orange accent,
serif column + margin rail) — rendered by CI and committed as
`articles/<slug>/field-copy.pdf`. The same design language renders the
article on the website.

- `scripts/build-article.mjs` fills the layout from markdown + frontmatter
  (issue stamp, kicker, rail stats/asides come from the fields above)
- `template/maczine-article.html` is the definitive hand-balanced edition —
  for a showcase issue, craft the sheets by hand there and render with
  `scripts/render-pdf.mjs`

```
node scripts/build-article.mjs articles/<slug> --pdf   # one article
node scripts/build-article.mjs --all --pdf             # everything
```

## Linting locally

```
npm install
npm run lint
```

## PDF edition (MacZine article template)

`template/maczine-article.html` is the definitive print template — and its
first pilot (the Freehold field report). Design language: warm paper, ink
navy, one burnt-orange editorial accent; serif reading column plus a
margin rail for asides, stamps and big stats. To produce a new article
PDF, copy the file, replace the blocks marked `✂ SLOT`, balance content
across `.sheet` blocks (one per page), then:

```bash
node scripts/render-pdf.mjs template/renders/<slug>.html
```

No dependencies — the script uses locally installed Chrome/Chromium/Edge.
