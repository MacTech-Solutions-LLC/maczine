---
title: Enclave or Whole Network? The Scoping Decision, Priced
issue: 10
description: Scoping CMMC Level 2 to a CUI enclave or to your whole network is a cost decision disguised as an architecture decision. Here is how the two actually compare.
publishedAt: 2026-08-04T08:00:00-04:00
tags:
  - cui
  - cui-enclave
  - cmmc
  - compliance
kicker: Buyer's Guide · CUI Handling
stats:
  - n: "110"
    label: controls you must satisfy - across whatever you put in scope
  - n: "1"
    label: boundary decision that sets the cost of every other decision
---

Every CMMC Level 2 program makes one decision that determines the cost of all the others, and most organizations make it by accident. The decision is where the assessment boundary sits: around a purpose-built enclave that holds CUI, or around the network you already have.

It presents as an architecture question. It is a cost question, and the costs are not close.

## The comparison nobody puts in writing

| | CUI enclave | Whole network |
|---|---|---|
| Systems in scope | The ones you deliberately put there | Everything, including what you forgot |
| Cost driver | Building the enclave once | Remediating every legacy system |
| Who feels it | Users who handle CUI | Everyone |
| Failure mode | Users route around a boundary that is too painful | Scope creeps until the assessment slips |
| Evidence story | One environment, one set of logs | Many environments, reconciled by hand |

The right-hand column is not wrong in principle. For an organization whose entire business is a single DoD program, whose systems were built recently and uniformly, and whose staff all handle CUI anyway, drawing the boundary around the network is honest and simpler. That organization exists. It is rarer than the number of contractors who assume they are it.

## Why the enclave usually wins on arithmetic

The enclave wins because 110 controls applied to eleven systems is a different project from 110 controls applied to a hundred and eleven - and because the hundred and eleven include the accounting server nobody has patched since it was installed, the shop-floor machine running an OS that is out of support, and the executive who will not accept multifactor authentication.

None of those are cybersecurity problems in the abstract. They become cybersecurity problems the moment your boundary encloses them, and each one is a finding, a remediation, and a line on a [POA&M](/maczine/system-security-plan-assessors-actually-read) that a C3PAO will ask about.

Pulling the boundary in does not make those systems secure. It makes them *out of scope*, which is a different and much cheaper claim to defend - provided the boundary is real.

## The condition that makes it real

That proviso carries the entire argument, so it deserves to be stated plainly: an enclave is only a boundary if CUI cannot leave it during normal work.

Not "should not." Cannot. The controls that make this true are the unglamorous ones - restricted clipboard and drive redirection, blocked removable media, egress controls, identity that does not span the boundary. If any of those is missing, you have not built an enclave. You have built a place where CUI is *supposed* to live, and users will discover the gap within a week because doing their job requires it.

This is the failure mode that gives enclaves a bad reputation. An enclave too painful to work in does not fail closed; it fails by being circumvented, and circumvention puts CUI back on the network you scoped out - where you now have no controls at all, because you scoped them out too. That outcome is strictly worse than never having built the enclave.

So the real question is not "enclave or network." It is whether you can build an enclave that people will actually work inside. If the answer is no - because the workflow genuinely requires tools that cannot live there - then the whole-network path is the honest one, and pretending otherwise buys you a boundary that exists only on paper.

## Deciding

Three questions settle it in most organizations.

What fraction of your staff touches CUI? Under a third, the enclave almost always wins. Approaching all of them, the boundary is doing less work than it costs.

How old is your estate? Every system predating your compliance obligation is a remediation bill you avoid by scoping it out.

Can the CUI work be done in a controlled environment? Not "would people prefer to" - can it. If a critical tool cannot run inside the enclave, that is a design constraint to solve before you commit, not a surprise to discover after.

MacTech builds bounded CUI enclaves as a product rather than a bespoke project - the architecture is described at [CUI enclave architecture](/cui-enclave-architecture), and [a readiness scan](/readiness) will tell you which side of this decision your environment is actually on. ◆
