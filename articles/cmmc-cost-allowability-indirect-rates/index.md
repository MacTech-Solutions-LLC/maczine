---
title: Who Pays for CMMC? It Depends Where You Book It
description: FAR Part 31 makes most CMMC spending allowable. Whether you ever see the money again depends on booking it direct or indirect - a call made once, by accident.
publishedAt: 2026-08-21T08:00:00-04:00
author: Maxine
issue: 24
kicker: Buyer's Guide · Cost and Pricing
tags:
  - cost
  - far
  - dcaa
  - cmmc
  - pricing
stats:
  - n: "$120,000"
    label: enclave build walked through both direct and indirect treatment in the worked example below
  - n: "6 points"
    label: rise in the overhead rate from spreading that same $120,000 across a $2 million direct labor base
  - n: "31.205-15"
    label: the FAR clause that keeps fines and penalties off the recoverable side of the ledger no matter how the rest was booked
asides:
  - title: Not legal or tax advice
    body: This is a cost-accounting explainer, not a determination for any specific contract. The booking call belongs to your controller and your DCAA-facing accountant, working from your actual contract mix and disclosed accounting practices.
---

Every dollar a defense contractor spends to meet CMMC lands on a cost ledger before it lands anywhere else, and that first landing spot decides more about the money's fate than the security control ever will. Ask how much an enclave build or a monitoring contract costs and you will get a number quickly. Ask how much of it a controller expects to actually recover, and on what, and the room usually goes quiet - because that answer was set the day someone coded the invoice, not the day someone asked the question.

Costs on a government contract live under FAR Part 31, and the threshold test is FAR 31.201-2: reasonable, allocable, and consistent with the cost accounting standards that already govern the business. Cybersecurity spend, treated as an ordinary and necessary cost of doing business, clears that bar in the overwhelming majority of cases - a CMMC obligation is not optional overhead a contracting officer can wave away as excessive. That is not the interesting question, and articles that stop there have answered the easy half. The interesting question is where the cost gets booked once it is deemed allowable: direct to the one contract that required it, or indirect through the overhead or G&A pool that covers the whole business. That is a bookkeeping decision, it is usually made once, and it is usually made by whoever happens to be coding the invoice that week rather than by anyone weighing the consequence.

## The choice that gets made by accident

Direct means one contract, on that contract's own terms, and a promise attached. FAR 31.202 lets a contractor charge a cost straight to the specific job that required it, and on a cost-reimbursement contract the recovery is clean: bill it, and it comes back dollar for dollar, subject to whatever funding ceiling the contract still has room under. But direct booking is not free of consequence. Read 31.202 alongside 31.203 and a consistency obligation falls out of the pairing: a cost charged direct on one job cannot also sit inside an indirect pool that covers that same kind of work elsewhere in the business. Book the enclave direct to the program that demanded it, and every other contract touching similar infrastructure now has to be examined for the same treatment, or an auditor will ask why an identical cost is handled two different ways in the same fiscal year.

Indirect spreads the cost across the whole base instead, and for most small primes that produces the larger number over the life of the business, because it recovers from every cost-type and time-and-materials dollar billed anywhere in the portfolio, not from one contract's ceiling. The catch is that spreading the cost also raises the rate every contract downstream inherits, and a higher indirect rate is a real competitiveness cost on fixed-price and commercial work - the government is not reimbursing a rate there, it is paying the number already quoted, and a thinner-margin business now has to quote a higher one. That trade, full recovery from one narrow channel against partial recovery from a wide one that costs you elsewhere, is the whole article. Everything else is arithmetic and a handful of traps.

## One enclave, two ledgers, and a six-point swing

Take the number this argument actually turns on: a $120,000 CUI enclave build, the kind of project [priced out on architecture grounds elsewhere in this newsletter](/maczine/cui-enclave-or-whole-network-scoping), landing on a contractor whose direct labor base runs $2 million a year.

Booked direct to the one contract that required the enclave, and assuming that contract is cost-reimbursement, the full $120,000 comes back dollar for dollar, subject to the funding the contract still carries - complete recovery, but only from that program, and only up to whatever headroom is left to bill against. If the same enclave was built to satisfy a fixed-price award instead, direct booking recovers nothing at all unless the $120,000 was already built into the negotiated price; a fixed-price contract does not reimburse actual cost, it pays the number both sides signed, and an unpriced $120,000 is simply absorbed.

Booked indirect instead, pooled into overhead and spread across the $2 million direct labor base, $120,000 divided by $2,000,000 is a flat six-point addition to whatever the overhead rate already runs. That new rate touches every direct labor dollar billed this year - recovered as billed cost on every cost-reimbursement and time-and-materials contract in the portfolio, which over a full year of billings is usually a larger number than any single program could ever absorb alone. It recovers nothing, however, on work that is already fixed-price and already awarded; those contracts were priced against the old, lower rate, and the six points simply do not appear in this year's billings on that work. And the six points follow the business into every fixed-price bid still ahead of it, showing up as a higher, less competitive number against a competitor who never carried the same enclave cost, or who booked it direct instead.

> The booking decision, not the security control, decides how much of the spend the business ever sees again.

There is a second complication buried in the timing, and it is the one controllers discover too late. The $120,000 lands as a lump the year the enclave gets built, but the $2 million labor base it is meant to spread across might belong to a smaller business in that same year, if the ramp toward the work the enclave was built for hasn't caught up yet. A base that shrinks turns a clean six-point addition into something sharper, and turns "spread it over the base" into a question of which year's base actually applies. Whether that lump amortizes across several years as a deliberate rate-smoothing decision, or lands as a one-year spike in the current rate, is a cost accounting policy choice made before the invoice posts - not an adjustment invented after the rate comes back higher than the estimate promised.

## What booking treatment cannot rescue

Two traps sit underneath both treatments, and neither cares which one you chose. Fines and penalties are unallowable outright under FAR 31.205-15, wherever they land on the ledger; no amount of careful pooling moves a fine back onto the recoverable side. The legal and investigative costs that follow a compliance failure run on a separate and less forgiving logic under FAR 31.205-47, and this is where people get surprised: the cost of actually fixing what failed, patching the control, rebuilding the evidence, closing the gap, is an ordinary business cost like any other. The legal and investigative work that grows out of the same failure does not automatically travel with it - 31.205-47 treats that category on its own terms, tighter than the remediation itself, and a program that budgets "the cost of getting this wrong" as a single line has usually mixed an allowable cost with one that may not be, without ever separating them. None of this is a determination for any specific set of facts; that call runs through your controller and your DCAA-facing accountant, not through a newsletter.

Underneath both traps sits the harder problem, and it is the one small businesses tend to discover last: none of this, direct, indirect, or the trap money, is recoverable at all if the accounting system cannot prove which dollar went where. The government tests that ability against the SF 1408 criteria - can the system segregate direct costs from indirect at the transaction level, accumulate cost by contract, and allocate the indirect pool on a base that stays consistent year over year and survives an audit. A contractor whose books cannot answer those questions does not get to choose direct or indirect, because nothing about the enclave cost was ever provably booked anywhere in particular; the choice was never on the table. That is why MacTech treats its own cost accounting system, built against those same SF 1408 criteria, and its compliance program as one engagement rather than two - a controller and a compliance lead solving the problem separately tend to solve neither one completely, and see [CMMC Level 2](/cmmc-level-2) for where that boundary conversation usually starts. If your CMMC spend and your accounting system have not had that conversation yet, [start it here](/contact) before the next invoice tells you which side of the choice you actually landed on.
