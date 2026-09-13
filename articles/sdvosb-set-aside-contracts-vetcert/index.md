---
title: "SDVOSB Set-Aside Contracts After VetCert: Where the Money Goes"
description: SDVOSB set-aside contracts now require SBA VetCert, and the FAR overhaul made them a contracting officer's choice. What FY2025 data shows for cyber.
publishedAt: 2026-09-18T08:00:00-04:00
author: Matthew Davis
issue: 38
kicker: Explainer · Federal Capture
tags:
  - sdvosb
  - set-asides
  - federal-contracting
  - capture
  - usaspending
stats:
  - n: "$56.6B"
    label: obligated in FY2025 under NAICS 541512 and 541519 combined, per USASpending
  - n: "5.01%"
    label: of federal prime contract dollars went to SDVOSBs in FY2025, against a 5 percent goal
  - n: "$5M"
    label: ceiling on a government-wide SDVOSB sole-source award outside manufacturing NAICS codes
asides:
  - title: What the data tool could not show
    body: The USASpending figures here came through MacTech's federal-market MCP server, which filters by NAICS, agency, keyword, and date but not by set-aside type. A keyword search for "SDVOSB" in the same codes and year matched under $1 million - a measure of how award descriptions are written, not of set-aside volume. USASpending's own API documents a set-aside type filter; that is the query to run for the real split.
---

In fiscal year 2025, which ran from October 2024 through September 2025, federal agencies obligated $31.7 billion under NAICS 541512, Computer Systems Design Services, and another $24.9 billion under 541519, Other Computer Related Services - the two codes under which a great deal of federal cybersecurity services work is classified. That is $56.6 billion, according to USASpending data. The Department of Defense accounted for $18.0 billion of it. The second-largest buyer was the Department of Veterans Affairs, at $6.3 billion, just ahead of GSA at $6.0 billion.

Government-wide, service-disabled veteran-owned small businesses took 5.01 percent of prime contract dollars that year, according to the SBA scorecard figures the Congressional Research Service reported, against a statutory goal of 5 percent. The goal was cleared by one hundredth of a point.

SDVOSB set-aside contracts now go only to firms the SBA has certified through its VetCert program. Outside VA, the choice to use one is a contracting officer's discretion, capped at $5 million for a sole-source award in non-manufacturing codes. At VA, federal statute still puts SDVOSBs first. Who qualifies got stricter; when the program must be used got looser. Those two changes pull against each other.

## Certification closed the door the goal was propping open

For most of the program's life, a firm could call itself an SDVOSB and compete for set-asides everywhere except VA, which ran its own verification through the Center for Verification and Evaluation. Section 862 of the FY2021 National Defense Authorization Act ended that arrangement. The SBA took over certification from VA on January 1, 2023, under what it now calls the Veteran Small Business Certification program, or VetCert, codified at 13 CFR part 128.

The grace period has run out. A firm that filed a complete application by December 31, 2023 could keep self-certifying for non-VA set-asides while SBA decided its case; one that had not filed lost that ability on January 1, 2024. SBA allowed self-certification for subcontracting and goaling purposes until December 22, 2024. The overhauled FAR makes the check mechanical: under the revised 19.106-1(b), the contracting officer must confirm the offeror is designated in SAM as an SDVOSB certified by SBA.

At the same time, Congress raised the bar. The FY2024 NDAA, Public Law 118-31, changed the government-wide SDVOSB goal in 15 U.S.C. 644(g) from 3 percent to 5 percent, and a companion provision stopped agencies from counting awards to uncertified firms toward it. The FY2025 scorecard measured agencies against 5 percent, and the result was 5.01.

The pool of firms eligible for SDVOSB credit shrank to the certified ones while the target rose by two-thirds. For a certified veteran-owned cybersecurity contractor, that is leverage: every dollar an agency awards to you counts toward a goal it barely met. For a prime, it means subcontract credit now depends on the sub's SBA certification, not its self-representation, and a teaming partner's certification status belongs in the same diligence file as its SPRS score.

## The FAR overhaul made SDVOSB set-aside contracts a choice, not a first step

The Revolutionary FAR Overhaul rewrote Part 19 in model deviation text released September 26, 2025. The Defense Department adopted it through Class Deviation 2026-O0037, which directed contracting officers to use the revised Part 19 and a rewritten DFARS Part 219 effective February 1, 2026.

The small business rule of two survived. Revised 19.104-1(a) says that above the micro-purchase threshold the contracting officer must set a contract aside for small business when there is a reasonable expectation of offers from two or more responsible small businesses competitive on price, quality, and delivery.

The SDVOSB set-aside is permissive. Revised 19.106-2 says a contracting officer may restrict competition to SDVOSBs when market research supports a reasonable expectation of two or more SDVOSB offers at a fair market price, and must consider an SDVOSB set-aside before an SDVOSB sole source. If no acceptable SDVOSB offer arrives, the set-aside is withdrawn and the requirement goes to small business generally.

What is missing is the part the old text had. The codified FAR 19.203(c) told contracting officers, above the simplified acquisition threshold, to first consider the socioeconomic programs - 8(a), HUBZone, SDVOSB, WOSB - before an ordinary small business set-aside. The overhauled Part 19 carries no such instruction. It says only, at 19.104-1(e), that the small business set-aside requirement does not preclude an award under those programs. Some practitioners read that as small business now taking priority. The text is quieter than that: it removes the nudge and leaves the decision with the contracting officer.

> The rules got stricter about who qualifies and looser about when the program must be used.

The sole-source ceiling is where the dollars get specific. Under revised 19.106-3, an SDVOSB sole source is available when the contracting officer does not expect two SDVOSB offers, the firm is responsible, the price is fair, and the award including options does not exceed $8.5 million in manufacturing NAICS codes or $5 million in any other. Both codes measured above fall in the second group. A multi-year managed security requirement can outgrow $5 million once its option years are priced in.

Above that line, veteran-owned competition for cyber work runs through set-asides, and through multiple-award vehicles with a veteran-owned pool. A keyword search of award records through [MacTech's federal-market server](/mcp/federal-market) turned up examples: Justice Department delivery orders placed through its ITSS-5 SDVOSB contract holders, a TSA order under the SDVOSB track of NITAAC's CIO-SP3, and a SEWP V order in the vehicle's SDVOSB group. On vehicles like those, revised 19.111-2 is blunt. Whether to set an order aside is the contracting officer's discretion and, with narrow exceptions, not a basis for protest. For a firm, the moment that decides an order is winning a place in the pool. That is a capture decision made years before any single order, and the kind of pipeline work that [CaptureOS was built to hold](/maczine/captureos-federal-capture-pipeline).

## At VA, the rule of two still says shall

Public Law 109-461 wrote VA's Veterans First program into 38 U.S.C. 8127, and that statute is not a FAR provision the overhaul could soften. Section 8127(d) directs VA contracting officers to restrict competition to veteran-owned small businesses when they reasonably expect two or more such firms to offer at a fair and reasonable price that offers best value. In *Kingdomware Technologies v. United States* in 2016, a unanimous Supreme Court held that the rule of two is mandatory, and that it reaches even orders VA places under existing Federal Supply Schedule contracts. VA's regulation, at VAAR 819.7005, puts SDVOSBs first, veteran-owned small businesses second, and the other small business programs after them. Its SDVOSB sole-source authority, at 819.7008, carries its own $5 million ceiling.

So the same $56.6 billion market runs under two different instructions. At VA, the $6.3 billion it obligated in these two codes in FY2025 sits under a statutory priority for veteran-owned firms. At DoD, the $18.0 billion sits under a regulation that permits an SDVOSB set-aside, requires a contracting officer to decide, and no longer tells that officer to look at the program first.

What the available data cannot yet say is how much of either pile went through an SDVOSB set-aside; the tools used here do not filter by set-aside type, and this piece does not invent the split. That query, run agency by agency, is the number a veteran-owned firm should pull before choosing which customer to chase, and it belongs beside the [pre-bid read of compliance clauses](/maczine/solicitation-compliance-clause-scan) any serious bid decision already requires.

MacTech Solutions sits on the firm side of that ledger: it is a Service-Disabled Veteran-Owned Small Business verified through SBA's VetCert program, and its [SDVOSB cybersecurity services](/sdvosb-cybersecurity-services) page lists both codes measured above among the NAICS codes it works under. Its offerings are catalogued in the [MacTech Market](/market).

For a contracting officer, the practical consequence is documentation. A decision to use or skip an SDVOSB set-aside for cyber work now rests on market research, and the agency's goal math is the reason to do it carefully. For a prime, it is the certification check on every teaming partner claimed toward a subcontracting goal. For a veteran-owned firm, certification is now the entry ticket, not the advantage. The advantage is being findable in the market research that decides whether a set-aside happens at all.
