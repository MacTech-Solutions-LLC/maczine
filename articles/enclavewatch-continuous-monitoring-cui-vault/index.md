---
title: "EnclaveWatch: Monitoring a CUI Vault Without Draining It"
issue: 16
description: Continuous monitoring usually means shipping logs somewhere central. Inside a CUI boundary that is the one thing you should not do. EnclaveWatch inverts it.
publishedAt: 2026-08-12T08:00:00-07:00
tags:
  - cui
  - cui-enclave
  - cmmc
  - governance
kicker: Platform Spotlight · Enclave Monitoring
asides:
  - title: What crosses the boundary
    body: EnclaveWatch exports **signed acknowledgement packages** to the Codex governance platform. Raw enclave logs stay inside the vault. The governance side learns that a review happened and what it concluded — not what was in the records.
---

There is an architectural contradiction at the center of most CUI compliance programs, and it is usually resolved in the wrong direction.

Continuous monitoring wants evidence centralized: one dashboard, one retention policy, one place an auditor can look. A CUI boundary wants the opposite — controlled data stays inside a defined perimeter, and every path out is a path that has to be justified. Ship your enclave's audit logs to a central platform and you have solved monitoring by widening the boundary you spent months narrowing.

EnclaveWatch is what happens when you refuse to resolve that contradiction by moving the data.

## Running the monitor inside the perimeter

EnclaveWatch runs as a service *inside* the vault. It collects and retains raw audit evidence locally, validates OS and Azure technical-control posture against a check catalog, and keeps the records where they already are.

The design consequence is that the enclave stops needing an outbound evidence path. Nothing about monitoring requires CUI-adjacent audit data to traverse the boundary, which means the boundary stays as small as it was designed to be — the property that made the enclave worth building in the [first place](/cui-enclave-architecture).

What leaves is deliberately thin: signed acknowledgement packages exported to the Codex governance platform. Governance learns that a review occurred, who performed it, and what it found. It does not receive the underlying logs. An auditor asking "was this reviewed, by whom, and what was concluded" gets a signed answer; an auditor asking to see the records goes into the enclave, which is where they should have to go.

## Drift is the thing you are actually watching for

Most enclaves are configured correctly on day one. The interesting question is day two hundred.

Configuration drift is not dramatic. It is a group policy amended for a project that ended. An exception granted for a vendor that finished its work. A baseline that stayed accurate while the systems underneath it moved. None of these announce themselves, and none of them will surface in a control narrative written eighteen months ago and never revisited.

EnclaveWatch treats drift validation as the primary job rather than a side effect of log collection. The probes are PowerShell — `os-controls.ps1` and `azure-controls.ps1` — deployed into the environment and run against a check catalog, which matters more than it sounds: the checks are configuration, not code, so what is being validated is legible to the ISSO who owns the outcome rather than buried in a binary.

The output is findings and POA&M recommendations, which is the correct output. A monitoring tool that produces alerts hands the ISSO a triage problem. One that produces findings mapped to the [remediation artifact](/maczine/system-security-plan-assessors-actually-read) they already maintain hands them work they can act on.

## The weekly review is the control

Here is the part that resists automation, and EnclaveWatch is built around admitting it.

The system supports weekly ISSO review. It does not perform the review. A human looks at what drifted, decides what it means, and signs — and the signature is what gets exported. That is not a limitation to be engineered away; it is the control. Continuous monitoring requirements are satisfied by a person accepting or rejecting a posture, and a platform that signs on their behalf has automated away the only part with accountability attached.

What the tooling removes is the part that was never valuable: assembling the evidence, chasing the drift, and reconstructing three months later what the environment looked like at the time of review.

## What it does not claim

EnclaveWatch validates technical control posture for a bounded vault. It is not a SIEM, it does not replace an assessment, and it has no opinion about systems outside the enclave — which for an organization that scoped honestly is most of the estate.

It is also, deliberately, a local service rather than a SaaS product. That constraint is the whole point: a monitoring platform you reach across the boundary is a monitoring platform that has a path across the boundary.

The vault ecosystem it belongs to is described at [CUI enclave architecture](/cui-enclave-architecture); [talk to a director](/contact) if you are running an enclave and currently monitoring it by exporting its logs somewhere else. ◆
