---
title: "CaptureOS: Finding the Work You Are Still Eligible For"
issue: 15
description: Capture tools tell you what is available. Compliance tools tell you what you can hold. CaptureOS puts both in one system, because the answer moves together.
publishedAt: 2026-08-11T08:00:00-07:00
tags:
  - defense-contracting
  - ai-automation
  - cmmc
  - captureos
kicker: Platform Spotlight · Capture
asides:
  - title: Built on the work it supports
    body: CaptureOS ingests from **SAM.gov** and **USASpending** alongside commercial sources. MacTech runs it against its own pipeline - the positioning in the repo is "built by the team that uses it to win contracts themselves."
---

A defense contractor loses opportunities in two distinct ways, and almost every tool on the market addresses only the first. The first is not knowing the work exists. The second is finding it, pursuing it, and discovering at the worst possible moment that a clause in the solicitation requires a posture the company does not have.

CaptureOS exists because those two failures have the same root, and treating them as separate problems is what produces the second one.

## The seam where pursuits die

Capture and compliance are almost always run by different people using different systems on different clocks. Business development watches the opportunity feeds. Compliance owns the control program and the score. They meet at the bid decision, which is far too late for either to help the other.

The consequence is a specific and expensive pattern: a pursuit that looks strong on capability grounds carries a cybersecurity requirement nobody priced. The team either no-bids late, having spent the effort, or bids anyway and inherits a compliance deadline that the [readiness program](/readiness) was not resourced for. Both outcomes are decisions made blind, and neither is a failure of either team - it is a failure of the seam between them.

The insight in CaptureOS is that eligibility is not a gate applied at the end of capture. It is an attribute of every opportunity, knowable at the moment the opportunity is ingested.

## What the platform does with that

The system pulls opportunity data from federal sources - SAM.gov and USASpending among them - and runs it through scoring, parsing, and compliance-matrix logic rather than presenting a filtered list. The distinction matters: a feed tells you what was posted, an assessment tells you what is worth your week.

Three things happen to an opportunity as it lands. It is scored against the company's actual capability and past performance profile. Its requirements are parsed, including the cybersecurity clauses that determine what posture a winner must hold. And the result is placed against the organization's current compliance state, so the question "can we hold this if we win it" is answered at the top of the funnel rather than at the bid review.

Proposal automation sits downstream of that, which is the correct order. Automating the production of proposals for work you cannot legally perform is a fast way to do the wrong thing efficiently.

## The part that is genuinely hard

Requirement parsing is where this class of system succeeds or fails, and it deserves an honest accounting rather than a claim.

Solicitations are not structured documents. The clause that determines your cybersecurity obligation may be incorporated by reference, buried in an attachment, or flowed down from a prime in language that paraphrases the actual requirement. A parser that reads the summary and misses the attachment produces confident, wrong answers - which is worse than no answer, because a wrong eligibility signal gets trusted.

This is why the compliance matrix lives in its own package in the codebase rather than being a feature of the ingestion worker. It is the piece that has to be auditable, correctable, and improved against real solicitations over time. Treating it as a solved problem is how you end up with a tool nobody trusts after the first miss.

The design response is to treat parsing output as a claim with a source
rather than an answer. A requirement the system surfaces should be traceable
to the passage it came from, so a capture manager can check it in seconds and
correct it when it is wrong. Corrections then improve the matrix rather than
being absorbed as private knowledge in somebody's head - which is the only
mechanism by which this kind of system gets better instead of quietly
decaying.

## Where it sits in the estate

CaptureOS is the front of the funnel; the rest of the MacTech platform estate is what happens after you win. The [CUI enclave](/cui-enclave-architecture) is where the resulting controlled work gets done. The [readiness scan](/readiness) is what turns a clause into a scored gap list. [Training](/training) is how the people named in the SSP stay qualified.

The connective argument across all of it is the one MacTech keeps making about its own operations: the company builds the systems it runs on, which is why the compliance posture in CaptureOS is a live attribute rather than a field somebody remembers to update.

For what it is not: CaptureOS does not decide whether to bid. It removes the excuse that nobody knew what the contract would require. That is a smaller claim than most capture platforms make, and it is the one worth making. ◆
