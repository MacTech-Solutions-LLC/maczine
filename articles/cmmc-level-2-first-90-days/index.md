---
title: "The First 90 Days of a CMMC Level 2 Program"
description: "A practitioner's sequence for the first 90 days of CMMC Level 2: scope the CUI boundary, baseline against NIST 800-171, and start evidence discipline early."
publishedAt: 2026-07-26
author: MacTech Solutions
tags:
  - cmmc
  - nist-800-171
  - cui
---

Most CMMC Level 2 programs don't fail at assessment — they fail in the
first quarter, when the scoping decisions and documentation habits that
determine everything downstream get made by default instead of on purpose.
Here is the sequence we run with new clients, and why the order matters.

## Days 0–30: Scope before you spend

The single most expensive mistake in CMMC preparation is buying controls
for systems that never needed to be in scope.

**Find the CUI first.** Not "where could CUI be" — where it actually is.
Pull your active DoD contracts and look for the DFARS 252.204-7012 clause
and CUI markings in the deliverable flow. Trace how that data enters your
environment, who touches it, and where it rests. Every system in that path
is in scope; everything else is a candidate for isolation.

**Shrink the boundary aggressively.** A CUI enclave — a segmented
environment where CUI lives and the rest of your business doesn't — is
almost always cheaper than certifying your whole network. Ten workstations
in an enclave beats two hundred in scope. This decision has to come first
because it changes the denominator on every control that follows.

**Name an owner.** Not a committee. One person with the authority to make
scoping calls and the calendar time to run the program. CMMC efforts
without a single accountable owner reliably stall at the
self-assessment stage.

## Days 30–60: Baseline honestly

With a boundary drawn, assess the enclave against all 110 NIST SP 800-171
requirements. Two rules make this useful instead of theater:

1. **Score it like an assessor would.** "We mostly do this" is NOT MET.
   The DoD assessment methodology is binary per objective — partial credit
   only exists in your POA&M, not your score.
2. **Write the finding down even when it hurts.** Your SPRS score is a
   legal representation of this baseline. An honest 88 with a credible
   POA&M is defensible; an optimistic 110 is a False Claims Act exposure.

The output of this phase is three documents that will live for the rest of
the program: a System Security Plan skeleton describing the boundary and
each control's implementation status, a POA&M listing every gap with an
owner and a date, and your initial SPRS submission.

## Days 60–90: Build evidence discipline, not binders

The habit that separates programs that pass from programs that panic is
started here: **evidence is captured when the work happens, not
reconstructed before the assessment.**

- Screenshots, configs, and log samples go into an organized evidence
  store, named by control, dated, as changes are made
- Recurring controls (access reviews, training, scans) get calendar
  entries with the evidence artifact as the meeting's required output
- The SSP gets updated in the same change window as the system — a
  document-as-you-build rule, borrowed from RMF practice, that is
  dramatically cheaper than document-after-the-fact

By day 90 you are not assessment-ready — nobody is in one quarter. What
you have is a scoped boundary that caps your cost, an honest score that
caps your legal exposure, and an evidence pipeline that compounds instead
of a binder that rots.

## Where programs actually stall

Three patterns we see repeatedly: scoping revisited every month because
leadership never signed off on the enclave decision; the POA&M treated as
a wish list with no dates or owners; and evidence collection deferred
until an assessment date forces a six-month archaeology project. All three
are quarter-one failures wearing quarter-four costumes.

---

*MacTech Solutions runs [CMMC readiness assessments](/readiness) and
builds [CUI enclave architectures](/cui-enclave-architecture) for DoD
primes and subcontractors. If you're starting your 90 days,
[talk to us](/contact) before you buy anything.*
