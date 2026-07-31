---
title: The 72-Hour Clock in DFARS 252.204-7012, Hour by Hour
issue: 11
description: DFARS 7012 gives you 72 hours to report a cyber incident to DoD. Walking the clock hour by hour shows where contractors actually lose the time.
publishedAt: 2026-08-05T08:00:00-07:00
tags:
  - dfars
  - cmmc
  - incident-response
  - cui
kicker: Field Report · Incident Response
stats:
  - n: "72 hrs"
    label: from discovery to a report filed with DoD under DFARS 252.204-7012
  - n: "3"
    label: CMMC incident response controls a tabletop can evidence at once
asides:
  - title: Discovery, not confirmation
    body: The clock starts on **discovery** of a cyber incident, not on confirmation that CUI was affected. Waiting for certainty is the single most common way the window is lost.
---

Seventy-two hours sounds generous until you walk it. The DFARS 252.204-7012 reporting clock does not start when you understand what happened, and it does not pause while you find out. It starts on discovery, and the organizations that miss it are almost never the ones that did not care — they are the ones that spent the first two days trying to be sure.

Here is where the time actually goes.

## Hour 0 — someone notices something

The clock starts here, and this is the first place it is lost, because "discovery" rarely announces itself. An endpoint agent fires an alert at 2 a.m. A user mentions offhand that a file looked strange. A backup job fails in a way that is unusual rather than routine.

None of those feel like the start of a regulatory obligation, and that is exactly the problem. The organizations that meet the deadline are the ones where somebody is empowered to say *this is an incident, the clock is running* before anyone knows the severity. That is a governance decision made months in advance, not a judgment call made at 2 a.m.

## Hours 1–8 — the wrong question

The instinct is to determine whether CUI was affected. It is the wrong first question, because it can take days to answer and the reporting requirement does not wait for it.

The right first move is parallel, not sequential: begin containment and begin the report at the same time. The report does not require certainty. It requires what you know, and "scope under investigation" is an acceptable state to report from. Contractors who treat the report as the final word on the incident rather than the opening entry consistently file late, and lateness is the violation — not incompleteness.

## Hours 8–24 — the medium-assurance credential problem

This is the hour range where unprepared organizations discover an administrative obstacle nobody planned for. Reporting goes to DIBNet, and it requires a DoD-approved medium-assurance certificate.

That credential takes time to obtain. If the first time anyone in the company looks into it is during an incident, the 72-hour window will close during the procurement process. It is the most avoidable failure in the entire sequence and it is startlingly common — a compliance problem masquerading as a paperwork problem, solvable on any quiet Tuesday months before it matters.

## Hours 24–72 — evidence, while it still exists

The remaining window is for assembling what the report needs: affected systems, the technique if known, the data at risk. The constraint here is not analysis, it is retention.

Logs that rolled over yesterday cannot be reconstructed today. An organization with 30 days of centralized, tamper-evident logging inside its [CUI boundary](/cui-enclave-architecture) writes this section from evidence. One relying on whatever happens to remain on the affected host writes it from inference, and inference is what a later investigation will take apart.

The reporting requirement also carries a preservation obligation — images and monitoring data must be kept for 90 days. Organizations that reimage first and report second have satisfied their instinct and violated their contract.

## What the report is not

Two misreadings cost contractors more than any technical gap.

The first is treating the report as an admission. It is not a finding of
fault, a breach notification, or a determination that CUI was compromised. It
is a notification that an incident affecting a covered system was discovered.
Organizations that route the decision through counsel for days before filing
have applied the correct instinct to the wrong instrument.

The second is treating it as final. The report is an opening entry against a
72-hour deadline, not the conclusion of an investigation that has barely
started. Filing with what you know and supplementing as you learn is the
designed behavior — not a fallback for when you are unprepared.

## The rehearsal

Every failure above is procedural, and procedural failures are found by rehearsal or by incident. There is no third option.

A tabletop exercise is the cheap version. Run it against the clock rather than against the scenario: start at discovery, force the team to decide when the clock started, make somebody produce the DIBNet credential, ask what logs exist for the affected system. The exercise will surface the credential gap and the retention gap in an afternoon, which is the entire point — those are the two that cost you the deadline, and neither is visible from a policy document.

It also happens to be efficient compliance. A properly run tabletop produces evidence for three CMMC incident-response controls at once, which is why [we build them as a fixed-scope engagement](/incident-response-tabletop) rather than a workshop.

The clock is the part of DFARS 7012 that cannot be remediated after the fact. Everything else in a compliance program can be improved on a POA&M. A missed report is simply missed. ◆
