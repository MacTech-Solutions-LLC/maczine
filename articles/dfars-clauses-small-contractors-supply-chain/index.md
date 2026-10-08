---
title: Six DFARS Clauses Beyond 7012 That Sink Small Contractors
description: "Specialty metals, Buy American, counterfeit parts, covered telecom, export control, IUID and WAWF: the trigger, duty, failure mode and flow-down of each."
publishedAt: 2026-10-15T08:00:00-04:00
author: Patrick Caruso
issue: 57
kicker: Reference · DFARS
tags:
  - dfars
  - supply-chain
  - flow-down
  - specialty-metals
  - counterfeit-parts
  - export-control
  - iuid
stats:
  - n: "5th"
    label: tier of the supplier whose Chinese-origin alloy stopped F-35 deliveries in 2022, according to Lockheed Martin
  - n: "65%"
    label: domestic component cost a manufactured end product must exceed under DFARS 252.225-7001 for deliveries in 2024 through 2028, rising to 75% in 2029
  - n: "3"
    label: business days to report covered defense telecom equipment at dibnet.dod.mil under DFARS 252.204-7018
asides:
  - title: Clause versions cited
    body: Clause titles and dates are as published on acquisition.gov under DFARS Change 5/7/2026. The FAR's broader Section 889 telecom prohibition (52.204-25 in the codified FAR) is being restructured under the Revolutionary FAR Overhaul, so check the solicitation's own clause list before relying on a FAR number. The DFARS clauses below are unaffected by that rewrite.
  - title: Why 252.244-7001 is not on the list
    body: The purchasing system clause bites hardest on contractors large enough to be Cost Accounting Standards-covered, which is also where 252.246-7007's counterfeit detection system requirement applies. A small firm usually meets both as a subcontractor, through the flow-downs below, not as a direct obligation.
---

Most small defense contractors who lose money on a DFARS clause do not lose it on cybersecurity. They lose it on a clause that governs a fact they never held: where a titanium bar was melted, who made a voltage regulator, which country sewed a pouch, whether a part number on a drawing carries a data matrix. The four cyber clauses get a compliance budget and a named owner, and MacZine has already [walked them in order](/maczine/solicitation-compliance-clause-scan). The six below get neither. Each is a supply chain clause dressed as a contract term, and each puts the obligation on the company that signed while the evidence sits with a supplier who signed nothing. They are ordered here by what failure costs, from a late invoice to a prison sentence.

## The invoice that will not post: 252.211-7003 and 252.232-7003

Take a twelve-person machine shop that ships a $6,000 assembly against a DoD delivery order and submits its invoice. Item Unique Identification and Valuation, 252.211-7003, applies to every delivered item with a government unit acquisition cost of $5,000 or more, plus anything the schedule or an attachment names, including embedded parts and serially managed items. The item needs a unique identifier in a two-dimensional data matrix, placed per MIL-STD-130 and verified machine-readable, and the identifier data is reported at delivery through the receiving report in Wide Area WorkFlow. The companion clause, 252.232-7003, requires that payment requests and receiving reports go through WAWF electronically, with a receiving report at each delivery; paper is allowed only with the contracting officer's written approval.

That pairing is the failure mode. A shop that never marked the part has no identifier to put on the receiving report, which is the same document its payment rides on, and the fix means getting the part back and marking it. Nobody is debarred. The cash just waits. IUID flows down to any subcontract for an item that requires a UII, commercial products included. The WAWF clause has no flow-down paragraph, because nobody but the prime gets paid through it.

## The broker part bought to make schedule: 252.246-7008

In 2012 the Senate Armed Services Committee reported 1,800 cases of suspect counterfeit electronic parts in DoD supply transactions from 2009 and 2010, more than a million individual parts, turning up in the C-130J, the C-27J, the SH-60B and the P-8A. The rules that followed are why a small electronics assembler now inherits a sourcing hierarchy it may not know it signed.

The detection-system clause, 252.246-7007, applies only to contractors covered by Cost Accounting Standards, and for those primes a deficient system can mean purchasing system disapproval and withheld payments. That is why they flow it hard. Its sibling, 252.246-7008, Sources of Electronic Parts, carries no such limit. Buy from the original manufacturer or its authorized distributors first; failing that, from suppliers you have vetted and whose parts you answer for; and only as a last resort from anyone else, in which case you notify the contracting officer in writing and inspect, test and authenticate the parts. Without traceability back to the manufacturer, the testing becomes mandatory. The quiet failure is a buyer pulling an obsolete part from an independent broker to save a delivery date, with no notice and no test record. The clause flows down to every subcontract for electronic parts or assemblies containing them, commercial ones included, unless the sub is the original manufacturer.

## The SAM checkbox nobody re-read: 252.204-7018

The covered telecom clause is narrower than its reputation. Under 252.204-7018 the prohibition reaches equipment, systems or services for DoD's nuclear deterrence and homeland defense missions that use Huawei or ZTE gear, or gear from an entity tied to the Chinese or Russian government, as a substantial or essential component or as critical technology. The paperwork reaches much further. Provision 252.204-7016 asks every offeror to represent in SAM whether it *does* or *does not* provide covered defense telecom equipment or services to the government, and the clause requires a report at dibnet.dod.mil within three business days of finding covered equipment during performance, with mitigation detail within thirty.

The failure here is rarely a purchase. It is a "does not" checked years ago by someone who never inventoried the cameras, routers and modules inside what the company actually delivers. A representation is a statement to the government, and a stale one is a false one. The clause flows to all subcontracts and other contractual instruments, commercial included.

## The alloy five tiers down: 252.225-7009

In September 2022 the Pentagon and Lockheed Martin disclosed that F-35 deliveries had stopped. A magnet in a Honeywell turbomachine contained a samarium-cobalt alloy produced in China, and Lockheed Martin said the alloy came from a fifth-tier supplier. Deliveries resumed only after the under secretary for acquisition and sustainment signed a national security waiver.

The clause behind that halt, 252.225-7009, requires that specialty metals in delivered items (certain steels, nickel and cobalt alloys, titanium, zirconium) be melted or produced in the United States, its outlying areas or a qualifying country. There are exceptions for electronic components, many commercial off-the-shelf items and a minimal-content allowance of 2 percent of an item's specialty metal by weight.

> The 2 percent exception does not cover high-performance magnets, which is exactly where the F-35 failed.

A program the size of the F-35 can get a waiver. A small machine shop that bought titanium bar stock on price, from a mill it never asked about, gets a nonconforming delivery to explain, and no waiver authority to call. The clause flows down to subcontracts for items containing specialty metals, commercial products included, and a prime may adjust only the minimal-content paragraph to manage it at its own level.

## The certificate signed on a supplier's word: 252.225-7001

London Bridge Trading Company of Virginia Beach agreed in November 2023 to pay nearly $2.1 million to resolve False Claims Act allegations that it sold DoD textile gear made in Peru, Mexico and China as American-made, in some cases swapping out the foreign labels. The case was brought by an employee, who shares in the recovery. That is the loud version.

The quiet version sits in the arithmetic of 252.225-7001, Buy American and Balance of Payments Program. A manufactured end product counts as domestic only if its U.S. and qualifying-country components exceed 65 percent of component cost for items delivered in 2024 through 2028, rising to 75 percent from 2029, and components of unknown origin are treated as foreign. A COTS end product is exempt from the component test. Everything else depends on origin data your suppliers may not have given you, behind a certificate you signed in the offer. The clause carries no flow-down paragraph, and that is the trap: the obligation stays with whoever certified the end product.

## The graduate student in the lab: 252.225-7048

In 2009 a retired University of Tennessee professor was sentenced to four years in federal prison for Arms Export Control Act violations. He had been working with Atmospheric Glow Technologies, a small Knoxville company, on an Air Force contract to develop plasma actuators for drone wings, and he let foreign graduate students work with the technical data. Under the ITAR, releasing technical data to a foreign person is an export even when nobody leaves the country.

Clause 252.225-7048 is short. Comply with the ITAR and the EAR, register with the State Department where the ITAR requires it, and include the substance of the clause in all subcontracts. It adds no obligation the law did not already impose, and says so. What it adds is notice: once it is in the contract, nobody can claim they did not know the work was export-controlled.

Every failure in this piece was decided at a purchase order, not at contract review. The mill cert, the distributor's authorization letter, the country of origin, the part's identifier and the citizenship of the person handling the drawing are all facts the small contractor has to collect from someone else and keep, or rebuild under deadline when a contracting officer asks. A shop that writes the flow-downs into its purchase order terms and refuses to receive material without the record has done the work. One that reads the clauses for the first time when the payment stalls has not. If you want a second set of eyes on the flow-down terms your purchase orders actually carry, [start that conversation](/contact).
