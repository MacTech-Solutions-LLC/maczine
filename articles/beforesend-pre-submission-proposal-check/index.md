---
title: "BeforeSend: The Proposal Check That Refuses to Guess Green"
description: BeforeSend tests a proposal packet against its solicitation before submission. What it verifies, what it hands to a human, and what it never checks.
publishedAt: 2026-11-12T08:00:00-05:00
author: Maxine
issue: 76
kicker: Platform Spotlight · Proposals
tags:
  - beforesend
  - proposals
  - capture
  - ai-automation
  - federal-contracting
stats:
  - n: "3"
    label: verdicts a run can return - DO NOT SEND, ANALYSIS INCOMPLETE, READY FOR FINAL REVIEW - and none of them is "ready to submit"
  - n: "13"
    label: deterministic check kinds, plus one semantic kind that always ends in human review
  - n: "0.92"
    label: trigram similarity a model-extracted rule's quote must reach against the source page, or it cannot verify anything on its own
asides:
  - title: The packet does not stay forever
    body: Each submission carries a retention policy - keep, or purge 30, 90 or 365 days after the last change - and a daily job enforces it. A purge blanks page text, form values and quotes but keeps filenames, hashes, findings, verdicts and the audit trail, so the record of what was checked outlives the documents themselves.
---

A small contractor rarely loses a proposal at the evaluation table. It loses it the night before, at the mailroom, to a technical volume that runs two pages long, a cover letter that names last year's solicitation number, or an attachment the narrative cites and nobody uploaded. Evaluators do not score those packets down; many never score them at all. The work that went into the bid was real, and the reason it failed is clerical, which is the most expensive kind of reason because it was entirely preventable.

The usual defense is a tired person with a checklist at 11 p.m. BeforeSend, the pre-submission validation platform MacTech runs at [beforesend.mactechsolutionsllc.com](https://beforesend.mactechsolutionsllc.com/), is a bet that most of that checklist can be turned into tests, and that the rest should be named as untested rather than quietly ticked. Its own README puts the posture in one sentence: the system never guesses green.

## A proposal built to fail

The clearest way to see what BeforeSend does is the packet MacTech wrote to break it. The repository generates a fictional solicitation and two response packets, one clean and one seeded with eleven deliberate flaws, and the end-to-end suite fails unless the flawed packet comes back DO NOT SEND with every flaw found and the clean one comes back READY FOR FINAL REVIEW. The flaws are the ones that cost real bids.

The technical volume runs 24 pages against its limit. Because page count is read from the PDF's structure, that finding is verified, not estimated. A Word file gets different treatment: the engine reports Word's own saved page count but will not pass a document on it, since pagination depends on the printer and the fonts, and it asks for the PDF that will actually be submitted.

The offer form's signature field is empty, and that is a blocking failure. The cover letter has a signature line but no fillable field, so the engine cannot tell whether someone signed it in ink, and it says so, routing the page to a human instead of guessing. Even a filled field is reported with the caveat that its cryptographic validity was not checked.

The cover letter cites solicitation DFL-26-R-0024 where the rules say DFL-26-R-0042, two digits transposed. Identifiers are canonicalized - case and spacing stripped - and compared across every document, so the transposition surfaces as a conflict with both quotes attached. The same cross-document comparison catches a total price that reads $4,250,000 in one place and $4,255,000 in another, and a start date given as January 5, 2027 in one document and 02/01/2027 in another.

The pricing workbook's typed total does not match its own rows. The engine recomputes the sum from the cells and flags a total that is a hard-coded number rather than a formula. If the workbook was never recalculated, the result is UNKNOWN with the fix spelled out - open it and save it - not a silent pass. An insurance certificate expired on 09/30/2026, caught by a date comparison. The narrative cites an Appendix G that does not exist in the packet. A past performance attachment is missing outright.

Two flaws show the engine's judgment about its own limits. Dollar amounts in the technical volume, where the rules forbid pricing, come back as human review rather than failure, because an amount is not always a price. And a subcontractor disclosure is required only because the packet names a subcontractor; the engine derives that fact, triggers the conditional requirement, and fails it when the disclosure is absent. Requirements that do not apply are shown folded away, never counted as passes.

> The engine treats "I could not tell" as a finding, not a footnote, and a run with an unreadable file cannot come back green at all.

That is the verdict logic in plain terms. An unreadable document, a failed stage, or an empty requirement set ends the run ANALYSIS INCOMPLETE. Any blocking requirement not satisfied, and not waived, ends it DO NOT SEND. Everything else is READY FOR FINAL REVIEW, and there is deliberately no verdict called ready to submit. A run also produces a manifest with a SHA-256 hash of each file reviewed, so the team can later show exactly which bytes the check saw.

## Where the model works, and where it is not allowed to

Most of the above needs no AI. Someone has to turn the solicitation into requirements, though, and that is the one job BeforeSend hands to a model: read Section L, the instructions, the checklist, and propose structured, editable requirements, each with a verbatim quote and a page label. Code then searches the source page for that quote. An exact or near-exact match passes the gate; anything below the 0.92 similarity threshold is marked source-unverified, kept for review, and barred from producing a verified finding until a person confirms it. The model's documentation is blunt that it is never the source of truth for a page count, a sum, a hash, a comparison, a file's existence or a signature. That is the right division of labor for anyone who has read MacZine on [what a signature on an AI-assisted proposal certifies](/maczine/ai-federal-proposal-writing-rules).

The business decision sits in whose key pays. Each organization connects its own Anthropic or OpenAI account under Settings. The key is tested with a live call before it is saved, sealed with AES-256-GCM, never returned by any endpoint, and shown thereafter as its last four characters. A key that cannot be decrypted is treated as no key, never quietly swapped for MacTech's own account. Each call's tokens and estimated cost are logged, and identical requests are answered from a per-tenant cache rather than billed twice. For a small firm that means the model spend lands on its own provider invoice, where it can see it and cap it. With no key at all, every deterministic check still runs; requirements are imported or entered by hand on the Requirements screen.

## What it will not catch

Honesty about scope is the point of the product, so it belongs in this column too. BeforeSend does not measure type size, line spacing or margins. A volume set in 10-point type against a 12-point rule will pass its page limit and nothing will object. It has no concept of CUI. It will not tell you whether a page needs a banner or whether a portion marking is right; a user could write a requirement that gathers every passage mentioning CUI for a reviewer, but nothing verifies the marking, and nothing in its security documentation presents it as a place to hold CUI-marked material. That question belongs to [the marking decision](/maczine/what-makes-a-file-cui-marking-decontrol) and to an enclave, not a preflight tool. It confirms a representations document is present and its signature field filled; it does not check SAM.gov or whether your reps are current. Semantic questions - does the management approach address transition risk - always end with evidence gathered and a human deciding. And filename rules are enforced only when someone has written the pattern down as a requirement.

None of that weakens the case. It locates it. BeforeSend sits late in a pipeline MacZine has covered from the front: [reading the clauses before the bid decision](/maczine/solicitation-compliance-clause-scan) and finding the work in [CaptureOS](/maczine/captureos-federal-capture-pipeline). It runs as a MacTech Suite app, so access is decided by the Suite's identity hub per organization, and its tests assert that one tenant asking for another's submission gets a 404 and no data.

The verdict it is proudest of is the modest one. READY FOR FINAL REVIEW means the clerical failures that kill bids have been tested, and the judgments a machine should not make have been put in front of the person who signs. That handoff, not a green light, is what a small contractor should want at 11 p.m. If you would like to run a live packet through it, [tell us about the submission](/contact).
