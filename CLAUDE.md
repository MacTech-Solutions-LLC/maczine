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

1. Create `articles/<slug>/index.md`. The directory name is the URL slug:
   kebab-case, keyword-rich, date-free (`cmmc-scoping-pitfalls`, not
   `2026-08-post`). Never rename an existing article's directory.
2. Frontmatter — required: `title` (≤70 chars ideal), `description`
   (≤160 chars, written as the SERP meta description), `publishedAt`
   (YYYY-MM-DD, today). Optional: `author`, `tags` (lowercase list),
   `kicker`, `stats`, `asides`, `issue`, `draft`. See README.md for exact
   shapes.
3. **The catalog** (see README "The catalog"): if the commission says this
   is a full **Issue**, set `issue:` to the next free number — check every
   existing article's frontmatter for the highest taken number; lint fails
   duplicates. If it's a **Field Note** (announcements, shorter pieces),
   omit `issue` entirely. When the commission doesn't say, default to
   Field Note.
4. Run `npm install && npm run lint` and fix every error and, ideally,
   every warning before opening the PR.

## Voice and structure

Practitioner-grade, field-report register — the reader is a defense
contractor or program-office engineer who has real work to do:

- Concrete over abstract; numbers, clause references, and named artifacts
  over adjectives. No marketing fluff, no "in today's fast-paced world".
- 700–1400 words. `##` section headings (the title owns the h1) — the site
  renders them as numbered section heads.
- The first paragraph gets a drop cap on the site — open with a strong,
  complete sentence, not a fragment or a list.
- At most one `>` blockquote — it renders as the ruled pull quote.
- `stats` (up to 3–4) and `asides` frontmatter feed the margin rail — use
  them when the material has real numbers or sidebar-worthy context.
- Honesty sections ("What it does not claim", "Where programs stall") are
  a house signature — include one when the topic supports it.
- Link to site pages where natural: `/readiness`, `/contact`,
  `/cmmc-level-2`, `/cui-enclave-architecture`, `/maczine/<other-slug>`.
  Internal links are part of the SEO job.

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

## Hard rules

- Branch prefix `maczine/` (e.g. `maczine/cmmc-scoping-pitfalls`).
- One article per PR. Don't edit other articles, scripts/, template/,
  .github/, or any `field-copy.*` (CI owns those).
- Don't add dependencies.
- PR body: one-paragraph summary + which references you actually read +
  the proposed catalog placement (Issue Nº or Field Note).
- Never merge the PR yourself; never push to main.
