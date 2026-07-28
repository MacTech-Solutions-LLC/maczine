# MacZine — agent authoring contract

You are writing for **MacZine**, the MacTech Solutions article newsletter,
published at mactechsolutionsllc.com/maczine. Articles here are commissioned
via GitHub issues (usually filed from the MacTech Suite's Press Room) that
mention @claude with a brief. Your job: turn the brief into a publishable
article PR that passes lint and honors the catalog.

## The one-paragraph model

Merge to `main` = published. A webhook mirrors `articles/` into the
customer site within seconds and CI renders a press-room PDF next to the
article. You NEVER merge your own PR — a human pulls that trigger.

## Writing an article

0. **Read the back catalog first.** Before you draft a line, list
   `articles/` and read the `title`, `description`, and `tags`
   frontmatter of every existing article. MacZine does not republish
   itself — see "Never repeat a published topic" below. A commission
   that duplicates a published piece is answered with a comment on the
   issue, not a PR.
1. Create `articles/<slug>/index.md`. The directory name is the URL slug:
   kebab-case, keyword-rich, date-free (`cmmc-scoping-pitfalls`, not
   `2026-08-post`). Never rename an existing article's directory.
2. Frontmatter — required: `title` (≤70 chars ideal), `description`
   (≤160 chars, written as the SERP meta description), `publishedAt`
   (YYYY-MM-DD, today). Optional: `author`, `tags` (lowercase list),
   `kicker`, `stats`, `asides`, `issue`, `draft`. See README.md for exact
   shapes.
3. **The catalog** (see README "The catalog"): MacZine runs ONE series —
   every article that publishes is a numbered Issue. Set `issue:` to the
   next free number: the highest taken across every existing article's
   frontmatter, plus one. Lint fails a duplicate, and it fails a
   non-draft article with no number at all. Commissions from the Press
   Room state the number outright — verify it is still free before you
   use it. Numbers run in publication order (001 is the first piece
   MacZine ever ran), which is exactly how the site sorts the index, so
   never renumber an existing article to make room.
4. Run `npm install && npm run lint` and fix every error and, ideally,
   every warning before opening the PR.

## Never repeat a published topic

Every article must be a topic MacZine has not already run. The back
catalog in `articles/` is the authority — including `draft: true` pieces
(hidden, but written) and any open PR on this repo.

A commission is a **duplicate** when an existing article already makes
the same central argument about the same subject, even under a different
headline, slug, or news hook. Two pieces on the same CMMC pause, or two
spotlights on the same platform, are duplicates no matter how differently
they are worded.

When the commission is a duplicate, **do not write it**. Instead:

- Comment on the commission issue naming the existing article (slug and
  title) and what it already covers.
- Offer the sharpest genuinely-new angle you can see — a development the
  existing piece predates, a different reader (program office vs.
  subcontractor), a consequence the original left unresolved — and ask
  the editor to confirm before you draft.
- If the commission explicitly acknowledges the earlier piece and asks
  for a follow-up, write it: open by linking
  `/maczine/<earlier-slug>`, state plainly what has changed since, and
  do not re-argue ground the earlier article already covered.

A near-duplicate is worse than no article: it splits search rankings
between two MacTech pages and tells a returning reader the newsletter
has nothing new. When in doubt, ask on the issue.

## The house writer

Article commissions are written by **Maxine**, the MacZine Editorialist —
read `.claude/agents/maxine.md` BEFORE drafting and write in
that persona (NYT editorial-page spine, Forbes business clarity, the
MacTech platform estate as your beat). The rules below still bind; the
persona shapes the prose on top of them.

## Voice and structure

Practitioner-grade, field-report register — the reader is a defense
contractor or program-office engineer who has real work to do:

- Concrete over abstract; numbers, clause references, and named artifacts
  over adjectives. No marketing fluff, no "in today's fast-paced world".
- 700–1400 words. `##` section headings (the title owns the h1) — the site
  renders them as ruled heads in your own sentence-case wording.
- The first paragraph gets a drop cap on the site — open with a strong,
  complete sentence, not a fragment or a list.
- At most one `>` blockquote — it renders as the ruled pull quote.
- `stats` (up to 3–4) and `asides` frontmatter feed the margin rail — use
  them when the material has real numbers or sidebar-worthy context.
- Link to site pages where natural: `/readiness`, `/contact`,
  `/cmmc-level-2`, `/cui-enclave-architecture`, `/maczine/<other-slug>`.
  Internal links are part of the SEO job.

## Structure: never the same shape twice

MacZine is an editorial page, not a template. Readers who open two issues
in a row must not see the same skeleton. **Before you outline, read the
last three published articles** (`articles/*/index.md`, most recent
`publishedAt` first) and deliberately build a different shape than they
used. Vary all of it:

- **Head count.** Two heads over long, argued stretches. Six over a
  procedural walk-through. Sometimes none at all — a 900-word column can
  run as continuous prose with a single pull quote as its hinge.
- **Head wording.** Sentence-case phrases that carry meaning ("The pause
  isn't the only rulemaking in flight"), not generic labels
  ("Background", "Analysis", "Conclusion"). Never a bare numeral.
- **Shape.** Chronology, single-argument build, question-and-answer,
  case-in-point, counter-argument-first, annotated timeline — pick the
  one the material wants.
- **No boilerplate closers.** "What it does not claim" and "Where
  programs stall" are tools, not a house signature: use one when the
  piece genuinely has limits worth naming, and not otherwise. Two
  consecutive articles must not end the same way.
- **Lists earn their place.** A numbered list is for genuinely ordered
  steps. If a section could read as prose, write it as prose — a piece
  that is mostly bullets reads as a slide deck, and it gets sent back.

## Referencing MacTech repos

Commissions list source repos under a "Reference material" heading, with
context. All live in the `MacTech-Solutions-LLC` GitHub org. Your token
only reaches THIS repo — read the others via public endpoints:

- `https://raw.githubusercontent.com/MacTech-Solutions-LLC/<repo>/main/README.md`
- `https://api.github.com/repos/MacTech-Solutions-LLC/<repo>` (description,
  topics) and `/contents/<path>` for specific files

If a referenced repo is private (e.g. mactech-suite-platform,
mactech-design), those fetches 404 — rely on the context pasted into the
commission issue instead, and say so in the PR description rather than
inventing details. **Never fabricate capabilities, numbers, or quotes.**
Everything stated as fact must come from the commission brief, a readable
repo, or the live site.

## Inspiration links & agent-drafted titles

Some commissions include an **Inspiration link** — a page whose topic the
article must engage with. Read it first, then write an ORIGINAL MacTech
piece that extends, applies, or respectfully disagrees with it for the
defense-industrial-base reader. Never summarize the source as the
article, never copy its phrasing; at most one short quote (<15 words)
with attribution and a link. If the link is unreachable, say so in the
PR and write from the brief alone.

Some commissions carry **no working title on purpose** ("you draft the
headline"). Derive it from the angle: ≤70 characters, keywords
front-loaded, plain-spoken — a strong claim or a specific question, not
clickbait.

## YAML frontmatter trap (this has bitten twice — read it)

Any frontmatter value that BEGINS with a `"` character must be wrapped in
single quotes, or YAML treats the opening quote as the scalar delimiter
and the rest of the line breaks the parse — the article then fails lint
AND silently drops out of the site sync:

```yaml
# WRONG — parse error or swallowed text
body: "Department of War" is the renamed DoD.
# RIGHT
body: '"Department of War" is the renamed DoD.'
```

A title containing a colon has the same problem for a different reason —
YAML reads `Title: subtitle` as a nested mapping and the parse fails:

```yaml
# WRONG — "mapping values are not allowed here"
title: EnclaveWatch: Monitoring a CUI Vault
# RIGHT
title: "EnclaveWatch: Monitoring a CUI Vault"
```

Platform-spotlight headlines take this shape constantly. Quote them.

Run `npm run lint` (or hand-check against `scripts/lint-articles.mjs`)
before every PR; a red lint means the article will not publish.

## Hard rules

- Never write a topic the catalog already covers — check `articles/`
  first and answer duplicates on the issue instead of in a PR.
- Never reuse the previous article's structure. Different head count,
  different shape, no stock closing section.
- Branch prefix `maczine/` (e.g. `maczine/cmmc-scoping-pitfalls`).
- One article per PR. Don't edit other articles, scripts/, template/,
  .github/, or any `field-copy.*` (CI owns those).
- Don't add dependencies.
- PR body: one-paragraph summary + which references you actually read +
  the issue number you claimed.
- Never merge the PR yourself; never push to main.
