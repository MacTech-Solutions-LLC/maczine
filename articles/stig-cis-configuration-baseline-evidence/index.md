---
title: "STIG, CIS, or Your Own Build: What Counts as a Baseline"
description: A DISA STIG, a CIS Benchmark, or your own build standard satisfies NIST 800-171 3.4.1 - if it's applied, evidenced, and watched for drift.
publishedAt: 2026-08-27T08:00:00-04:00
author: Maxine
issue: 28
kicker: Field Report · Configuration Management
tags:
  - stig
  - cis
  - configuration-management
  - nist-800-171
stats:
  - n: "5"
    label: points each 3.4.1 and 3.4.2 carries in the DoD Assessment Methodology - among the heaviest weights any single requirement gets
  - n: "2,029"
    label: DISA STIG rules in MacTech's reference service, across RHEL 8, RHEL 9, Windows 11, Windows Server 2022, and Cisco IOS Router NDM
  - n: "4"
    label: artifacts an assessor asks for to evidence a baseline - most programs walk in with one
asides:
  - title: What a vendor default actually fails
    body: An unmodified factory image is not the absence of a baseline - it is someone else's baseline, tuned for compatibility across every customer that vendor has, not for a CUI boundary. 3.4.2 asks you to enforce settings you chose. A default you never touched fails that test even when it happens to be reasonably secure.
---

Ask a program manager how their servers are configured and the honest answer, more often than not, is "to best practices" - a phrase that satisfies nobody, least of all the assessor sitting across the table from 3.4.1 and 3.4.2. Both are 5-point requirements in the DoD Assessment Methodology, among the heaviest weights any single control carries, and both get hand-waved with a confidence that has nothing behind it. A baseline is not a philosophy. It is a specific, documented, enforced configuration for each type of system you run, with every departure from it written down and a way of noticing when reality drifts away from the document. Here is the sequence that gets you there, in the order an assessor actually walks it.

## What actually qualifies as a baseline

Start with the question readers actually have, because it is simpler than the anxiety around it suggests: a DISA Security Technical Implementation Guide, a CIS Benchmark, or your own documented build standard all qualify. None of the three is mandated for a contractor's own network. STIGs bind systems operating under an Authorization to Operate through the Risk Management Framework; a contractor's internal boundary is scoped differently, and nothing in NIST SP 800-171 names DISA's catalog by number. What 3.4.1 and 3.4.2 require is that you pick one, document it per system type, and apply it - a RHEL 9 database server and a Windows 11 workstation each get their own defined configuration, not one aspirational paragraph covering both.

An assessor will accept any of the three sources, and picking one is mostly a question of what you already run. A shop standardized on Red Hat and Windows Server gains real leverage from adopting DISA's STIGs outright, because the check and fix text already exists at the level of individual registry keys and configuration lines. CIS Benchmarks cover a wider vendor list and read a shade less prescriptive. A homegrown build standard is legitimate too, provided it specifies settings at the same granularity the other two do - "harden the OS" is not a setting, and neither is a screenshot of a checklist nobody re-ran since the box was imaged.

## What an assessor will not accept

Two things fail regardless of which source you picked. The first is a vendor default left unmodified - not because a default is automatically insecure, but because 3.4.2 asks you to enforce settings you chose, and a setting nobody touched was not chosen. The second, more common failure is a baseline that exists in a Word document and nowhere else: a hardening guide written once during procurement, filed, and never run against the machines it describes. An assessor's method is to sample - pull applied configuration off a live host and compare it to the document - and a baseline that only exists on paper fails the moment that sample is taken. The document has to be a description of what the machines actually are, not what someone once intended them to be.

## Build the deviation register before the assessor finds it for you

No real environment holds a benchmark line for line. An application needs a service the STIG disables by default; a monitoring agent needs a port the CIS Benchmark closes; a legacy client can't negotiate the cipher suite the hardening guide mandates. That gap is not the failure. Every mature program has one somewhere. What separates a mature program from a failed one is whether the gap is written down with a rationale and a compensating control, or whether the assessor finds it first by running a scan you didn't run yourself.

A deviation register does three things for every departure: names the specific rule or setting not being enforced, states why - the business or technical reason the strict setting can't hold - and records what stands in its place, whether that's a compensating control, a network-layer restriction, or an accepted risk signed by someone with the authority to accept it. A register with zero entries is not a sign of a perfectly held baseline. In an environment running real applications, it is usually a sign nobody has looked closely enough to find the gaps that are already there.

> A deviation nobody wrote down isn't a secret you kept. It's a finding you handed the assessor for free.

## Baselines rot: catch drift with 3.4.3 and 3.11.2

Baselines pass on day one and rot quietly afterward, and that decay - not the initial build - is the actual failure mode auditors see most. A patch changes a default. An administrator opens a port under deadline pressure and forgets to close it. A new server gets imaged from a golden template that was itself never updated after the last STIG release. None of this shows up unless something is watching for it, which is why 3.4.1 and 3.4.2 don't stand alone - they lean on 3.4.3, change control, and 3.11.2, vulnerability scanning, as the mechanisms that notice.

"Regularly" is not a cadence an assessor will credit. A working program runs credentialed vulnerability scans on a fixed schedule - monthly is the common floor for a CUI boundary - and re-checks applied configuration against the baseline on its own cycle, quarterly at minimum and tighter around any DISA STIG or CIS Benchmark release. Every scan finding that traces back to a configuration setting, not a missing patch, either gets remediated on a tracked timeline or becomes a new line in the deviation register. Change control closes the loop: nothing that alters a baselined setting ships without a ticket, and the ticket is the record that connects the drift back to a decision someone made on purpose.

## The four artifacts, and why most programs have one

Strip the whole program down to what an assessor actually asks for and it is four things: the baseline document itself, specifying settings per system type; applied-configuration output pulled from a representative sample of hosts, proving the document and the machines agree; the deviation register, with a rationale and a compensating control behind every entry; and the change tickets that authorized each deviation and each subsequent modification. Most programs that fail this control on assessment day have written the first artifact and stopped. The other three are where the actual evidence lives, and they're also where a MacTech [readiness assessment](/readiness) spends most of its time, because a gap in any one of the four reads to an assessor exactly like a gap in the whole control.

## Running RMF and CMMC evidence off the same checklist

For a contractor running both an ATO under RMF and a CMMC program, the STIG format does double duty. DISA's .ckl checklist is the standard artifact for documenting compliance against a specific STIG, rule by rule, and it is the format a Security Control Assessor expects to see under RMF. The general case for treating RMF and CMMC as one evidence problem instead of two separate ones was [made here in Issue Nº 012](/maczine/rmf-ato-and-cmmc-one-system); configuration baselines are one of the cleanest places to apply it, because the same .ckl output that proves a system to a Security Control Assessor is also the applied-configuration artifact a C3PAO wants for 3.4.1 and 3.4.2. MacTech's own STIG reference service tracks 2,029 rules across RHEL 8, RHEL 9, Windows 11, Windows Server 2022, and Cisco IOS Router NDM, with per-rule check and fix text, NIST control mappings, and export to that same .ckl format - one baseline, evidenced once, read by both programs.

The document you already wrote is not the finish line. It's the first of four artifacts, and the only one that doesn't change once the ink dries. Programs that treat it as the whole answer are the ones an assessor spends the least time being polite to. [Talk to a director](/contact) if your baseline evidence currently lives in one file instead of four.
