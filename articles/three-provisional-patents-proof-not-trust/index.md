---
title: MacTech Files Three Provisional Patents Built on Proof, Not Trust
description: Three provisional patents from MacTech - Trust Codex, IBE, Freehold - on tested systems that prove their claims instead of asking you to trust the operator.
publishedAt: 2026-08-17T08:00:00-04:00
author: Maxine
issue: 20
kicker: From the record · Patents pending
tags:
  - cmmc
  - ai-automation
  - freehold
  - cryptography
  - governance
stats:
  - n: "3"
    label: provisional patents filed, all reduction-to-practice
  - n: "8"
    label: conjunctive gates in IBE, zero LLMs in the decision path
  - n: "1"
    label: signed roster is Freehold's only root of trust
asides:
  - title: Provisional, not granted
    body: These are provisional applications - "patent pending," a priority date, not an issued patent. And the novelty in each is a specific, tested combination, not an unqualified first. The fields are well populated, and the disclosures name their own prior art rather than hide it.
---

MacTech Solutions has filed three provisional patent applications, and the interesting thing about them is not that a small defense contractor is filing patents. It is what the three inventions refuse to do. None of them asks you to trust the operator. Each one, in a different domain, replaces an assurance that rests on somebody's good word with one that rests on math a hostile party cannot forge. That is a single worldview, filed three times.

The three are platforms MacTech already runs: Trust Codex, a CMMC and NIST 800-171 compliance control plane; IBE, a deterministic kernel that governs what an AI agent is allowed to do; and Freehold, the serverless encrypted messenger this newsletter covered in [Issue Nº 003](/maczine/freehold-secure-comms-you-hold-outright). All three filings are reduction-to-practice - working code with passing unit and end-to-end tests, not slideware - and all name Patrick Caruso as sole inventor. Read together they argue one thing.

> A system that asks you to trust its operator has told you exactly where to attack it.

## The compliance ledger that assumes its own database is hostile

Trust Codex begins with a piece of determinism most GRC tools leave to a spreadsheet: it decides who owns each security control. A pure precedence function walks a cloud-agnostic ontology of technology layers and assigns every control to exactly one of four tiers - Inherited, Shared, Customer, or Not Applicable - and emits an allocation hash over the inputs (`allocateControls.ts`, `allocationHash.ts`). No scoring, no weighting, no machine learning in the decision path. The same boundary parameters always produce the same allocation and the same hash, so an assessor can reproduce the reasoning rather than accept it.

The strengthening filing is sharper, and it is honest about the weakness it closes. The platform's evidence attestation historically verified a compliance snapshot by recomputing its hash and comparing that against the hash stored in the database. Sound, until you notice that an attacker with database write access simply rewrites both sides and the check passes. The new construction (`src/lib/attestation/witnessLedger.mjs`, four passing tests) treats the database as hostile. Each control's posture becomes a Merkle leaf; snapshots chain into an append-only head, `head_n = H(seq ‖ root ‖ head_{n-1})`; and that head is recorded outside the database entirely, in a source-controlled artifact. The assessor verifies against the witnessed head, not the database. An attacker who rewrites a stored snapshot and its stored root is caught the moment the recomputed head fails to match the witness - the code returns `head_mismatch`.

The Merkle machinery here is old and MacTech says so: RFC 6962, the Crosby-Wallach history tree, the lineage that runs through Certificate Transparency. The contribution is narrower and specific - per-control compliance postures bound to the deterministic allocation, committed to a head that no single compromised system can forge. That is the shape of an honest claim.

## The agent authority that expires the moment the model moves

IBE - Intent-Bound Execution - answers a question every organization pointing an AI coding agent at production is about to face: has this proposed change earned the right to proceed? IBE decides through eight conjunctive gates and issues a signed acceptance certificate or a signed refusal that names the gate that failed. The doctrine is that there is no large language model anywhere in the decision path; `decide()` is a pure function with no clock, no randomness, and nothing that can be prompted (`kernel.ts`).

Its strengthening filing is a forward-secure, single-use capability ratchet (`packages/capabilities/capRatchet.mjs`, six tests). Authority for an action derives from a one-way hash ratchet seeded by the intent and the engineering-model version. The holder erases each key as it is spent, so a captured token cannot be replayed even inside its own validity window. The verifier keeps only the next expected index and a rolling accumulator - a publishable, order-binding commitment to exactly which tokens were spent - so single-use becomes auditable by any third party instead of trusted from a verifier's private memory. And a change to the engineering model reseeds the entire ratchet, killing every outstanding token at once with no revocation call to make. MacTech distinguishes the combination from its neighbors by name: macaroons and Biscuit attenuate but are not forward-secure, bearer JWTs are replayable for their lifetime, Signal's hash ratchet protects message keys rather than authority, and nullifier spent-sets enforce single-use without binding to a model. The demonstration is the proof: a benign change is accepted with a signed certificate; bump the model one revision and the prior run's evidence is refused, by name, in a signed refusal certificate - across 73 of 73 end-to-end tests.

## The team whose own signature is the only root

Freehold is a sovereign peer-to-peer messenger for vetted teams: no server in the data path, keys held locally, a post-quantum layer (ML-KEM-768) inside the Noise transport, and operation in air-gapped environments where a cloud never reaches. The patent spine is an act of consolidation. One issuer-signed team roster - canonical JSON with a detached Ed25519 signature, verified against the very issuer it names (`roster.js`) - is made the single root for three things that other systems solve separately and more weakly.

That one signed roster anchors rotating rendezvous discovery, so members meet on DHT topics only they can derive and the long-term identity key is never announced to the network. It scopes conflict-free replicated state (`crdt.js`), so a revoked member's messages tombstone deterministically instead of waiting on an administrator's later cleanup. And it governs key-erasure deletion (`seal.js`): a self-destructing message's key is destroyed at the fuse, which makes the ciphertext undecipherable everywhere at once rather than merely hidden by a client that has agreed to hide it. Again the prior art is named rather than avoided - Briar's Bramble Rendezvous rests on a static shared secret, Tor v3 on a static identity, p2panda trusts the replica to honor deletion, and Signal's disappearing-message timers are honored by a cooperating client. Freehold's move is to make a single signed membership the common root of discovery, consistency, and erasure. Its unit and end-to-end tests run through real daemons.

## One design law under three products

Read together, the three filings describe one law: determinism you can verify, and cryptography that does not require trusting whoever runs the system. Trust Codex makes a compliance posture provable against a witness its own database cannot forge. IBE makes an agent's authority self-expiring and its every spend auditable. Freehold makes a team's own signature the root of who can find whom, whose messages count, and what stays deleted. In each case the trust a conventional system quietly places in an operator - the database administrator, the token service, the messaging server, the good corporate citizen who promises to delete your data on request - is replaced by something the person relying on it can check for themselves.

None of this is issued yet, and the honesty is part of the point. Provisional means patent pending: a priority date, not a granted patent. The novelty in each is a particular, tested combination over a well-populated field, not a world-first, and the disclosures say as much in their own accuracy sections. What makes them worth a column is that they were filed on running systems with passing tests - Trust Codex is deployed, IBE's governing doctrine has been public since July, Freehold has been in daily use - rather than on an idea someone hoped to build.

That is also the discipline MacTech sells to the defense industrial base: document as you build, and prove it with the receipts, across [readiness work](/readiness) and [CUI enclave design](/cui-enclave-architecture) alike. The patents are the same argument, now on file. For a program office or a subcontractor evaluating a compliance platform, an agent guardrail, or a comms tool, they suggest one question worth asking of anything that guards something you cannot afford to lose: can I verify this without trusting whoever runs it? These three were built to make the answer yes.
