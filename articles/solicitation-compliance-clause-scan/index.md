---
title: Read the Solicitation's Compliance Clauses Before You Bid
description: Compliance cost gets decided at bid or no-bid, not after award. A front-to-back read of the clauses, DD-254, and Section L/M that actually price it.
publishedAt: 2026-08-31T08:00:00-04:00
author: Maxine
issue: 30
kicker: Buyer's Guide · Capture
tags:
  - solicitation
  - dfars
  - capture
  - bid-no-bid
  - sprs
stats:
  - n: "4"
    label: DFARS clauses to read before Section L - 7012, 7019, 7020, and 7021, each narrowing the last
  - n: "3"
    label: years is the outer limit on a still-current SPRS assessment under DFARS 252.204-7019
  - n: "0"
    label: conversations a contracting officer needs before reading your SPRS score
asides:
  - title: What's suspended, what isn't
    body: CMMC Phase 2 - the certification clause at 252.204-7021 - was suspended July 13, 2026, pending review. DFARS 252.204-7012 and the NIST SP 800-171 Rev 2 baseline under it were not. Verify current clause status before a bid decision leans on either fact.
---

A solicitation gets priced twice. The first pricing happens in the technical volume, where a capture team totals labor, materials, and schedule against the statement of work. The second pricing happens, or should happen, in the clause list, the DD Form 254, and Section L and M, where the same document quietly totals up everything a winning bidder will be obligated to build, prove, and maintain for the life of the contract. Most small defense contractors do the first pricing carefully and skip the second, reading a solicitation for scope and price and treating the clauses as boilerplate nobody actually enforces. That habit is how a company wins a contract that costs more in compliance than it earns in margin, and finds out only after the signature is on the page.

The fix is not a lawyer on retainer. It is reading the solicitation in the order the obligations actually appear, before the bid-no-bid meeting, not after.

## The clause list draws the boundary before Section L ever does

Start where a capture lead usually skims: the clause list, either enumerated in Section I or incorporated by reference. The clause that tells you the rest of this walk matters is DFARS 252.204-7012. Its presence means covered defense information will pass through your systems on this contract, and with it comes a safeguarding duty against NIST SP 800-171 and a 72-hour clock to report a cyber incident once discovered - a clock this newsletter has [walked hour by hour](/maczine/dfars-7012-72-hour-incident-clock), and one that does not wait for you to be sure what happened before it starts running.

Three more clauses build on that foundation, each asking a narrower question. DFARS 252.204-7019 requires a current NIST SP 800-171 assessment posted in the Supplier Performance Risk System at the time you submit your proposal, and "current" is a defined term, not a feeling: an assessment older than three years does not satisfy it, no matter how good the score once was. DFARS 252.204-7020 gives the government the right to conduct, or have conducted, a higher-level assessment of your systems, and it carries its own flow-down obligation to your subcontractors, a second copy of the same duty you are reading into your own contract. DFARS 252.204-7021 is the CMMC requirement itself, the clause that conditions award on a certification level rather than a self-assessment. Read them in that order and each one narrows the last: 7012 tells you the information is covered, 7019 tells you your score has to be recent, 7020 tells you the government can check your work, 7021 tells you a third party might have to certify it first.

Two more stops close out the clause list. Where the work involves classified access or specified CUI handling, a DD Form 254 will be attached, and it is not a formality - it names the actual categories of information you will hold and the security requirements that attach to each one, and it is worth reading before the statement of work rather than after. Where the work is hosted rather than performed on your own systems, a cloud clause governs what the provider has to meet; that is its own solicitation-reading discipline, and a companion piece later in this run walks it in the depth it deserves. This piece stays with the clauses that determine whether you are eligible to bid at all.

One clause on this list is not settled ground, and a careful reader treats it that way. The Department of War suspended CMMC Phase 2, the certification requirement in 252.204-7021, on July 13, 2026, and opened a review of the program. DFARS 252.204-7012 and the NIST SP 800-171 Rev 2 baseline underneath it did not pause with it, and neither did 7019's SPRS currency requirement. [We covered what actually changed and what didn't](/maczine/cmmc-phase-2-suspension-review) when the pause was announced. Verify the clause status your solicitation actually cites before you let this paragraph, or any other, decide a bid.

## Section L and M are where the score stops being homework

Everything above is a compliance exercise until you reach Section L, instructions to offerors, and Section M, evaluation criteria, the point where a solicitation stops describing an obligation and starts describing how you will be judged against it. If Section L asks you to submit your SPRS score or your assessment date as part of the proposal, and Section M lists cybersecurity posture as an evaluation factor, your score has left the compliance file and entered the competitive one. A contracting officer or evaluation panel can pull your number from SPRS and read it before a single phone call, and they will read it the way an evaluator reads any factor: comparatively, against every other offeror's number, not in isolation against a passing threshold.

> Most capture leads have never once looked at their own SPRS score the way an evaluator is about to.

That gap is the reason this section belongs in the walk-through rather than after it. A capture lead who checks the clause list, confirms 7012 applies, and moves on to price the labor has confirmed eligibility. A capture lead who also reads Section M has confirmed something sharper: whether the score sitting in SPRS today helps the bid or quietly works against it, and whether there is time before submission to move it.

## The obligation runs down the chain, not just to you

If the plan is to bid as a prime with subcontractors, or to bid as a sub under someone else's prime, the clause list above is not the whole obligation, it is only the federal half of it. What a prime must flow down to a subcontractor, and what a subcontractor is actually bound to accept, is a separate negotiation that happens in the subcontract itself, and a federal clause pausing or changing does not automatically rewrite that document. [This newsletter argued the distinction in detail](/maczine/cmmc-pause-subcontract-flow-down): the federal suspension is the government's document to write and rescind, and a subcontract is a promise between two companies that only the two of them can amend. Read your teaming agreement's compliance language with the same attention you gave the clause list, because it is where the same obligation reappears in a different instrument, sometimes on a stricter timeline than the one DoD currently enforces.

## What the walk is actually for

None of this replaces [finding the opportunity in the first place](/maczine/captureos-federal-capture-pipeline); that is a separate discipline, and a good one still leaves this pricing question unanswered. What the clause scan buys you is the number that belongs next to the labor estimate before the bid-no-bid meeting, not after it: if winning this contract obligates a CUI enclave build, a higher assessment tier, or a certification you do not currently hold, that is a cost, and it belongs in the bid the same way labor and materials do. Where that cost actually gets booked, and whose rate structure absorbs it, is a separate question this run answers on its own. The honest output of this walk is sometimes a bid with the compliance cost priced in on purpose, and sometimes a no-bid decided in the room where it is cheap, instead of a year into performance where it is not. Either answer beats the one that comes from reading a solicitation for scope and price and finding the clauses only after the award letter. If you want a second read on what a specific solicitation actually obligates you to hold, [start that conversation](/contact) before you submit, not after.
