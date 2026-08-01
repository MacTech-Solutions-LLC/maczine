---
title: "Freehold: Secure Comms You Hold Outright"
description: "Peer-to-peer encrypted chat, calls and 2 GB file transfer for small DIB teams - post-quantum, air-gap ready, 800-171 evidence built in. Free, open source."
publishedAt: 2026-07-22T08:00:00-07:00
issue: 3
author: MacTech Solutions
tags:
  - freehold
  - secure-communications
  - cui
  - nist-800-171
  - post-quantum
kicker: Field Report · Secure Communications
stats:
  - n: "$0"
    label: per seat, per month, forever - MIT licensed
  - n: "<60s"
    label: two laptops, one LAN, zero config, zero internet
  - n: "2 GB"
    label: resumable, hash-verified file transfers
asides:
  - title: Why "Freehold"
    body: A **freehold** is property held outright - no landlord, no rent, no one who can let themselves in. That is the architecture, in one word.
  - title: The lineage
    body: Freehold is built on the **chat-tunnel** protocol - the wire keeps the old name so existing installs upgrade in place. Nothing re-keys, nothing moves.
---

Every small defense contractor we work with has the same conversation
problem. The program traffic that actually runs the shop - "the crucible
pour moved to Friday," "QA hold on lot 47," a 300 MB fixture model - lives
somewhere between text messages that violate the records rules and a
cloud messenger subscription that costs real money, holds your metadata,
and stops working the moment the network does.

For a ten-person sub, the cloud option runs roughly $5–15 per user per
month, with retention and e-discovery typically locked in the premium
tier - call it $1,800 a year plus procurement friction. And cross-org
collaboration, the daily reality of a sub on three primes' programs,
means admin-gated federation negotiated pair by pair.

Freehold is the third option: comms your team **owns** - like the shop
floor, like the machines on it.

## What it is

Freehold is peer-to-peer encrypted chat, calls, and file transfer for
small teams that handle sensitive work. There is no server, no account,
no per-seat rent, and no third party holding your metadata. Your identity
is a cryptographic key generated on your machine; peers connect directly,
NAT holepunching included. It is MIT licensed and open source.

The name is the thesis. A *freehold* is property held outright - no
landlord, no rent, no one who can let themselves in.

## Sovereign by architecture, not by policy

There is nothing to breach, subpoena, or bill you, because there is no
vendor infrastructure at all. Every link runs the Noise protocol with an
independent **hybrid post-quantum layer** (ML-KEM-768, FIPS 203) inside
it - a fresh key for every message and periodic re-keying, so traffic
recorded today stays unreadable to tomorrow's computers. That matters
against CNSA 2.0 timelines, and it is ahead of where the incumbent cloud
messengers publicly are.

Team trust is a **roster signed by your team lead's key** - and policy
(retention, expiry caps, marking banners, mandatory at-rest encryption)
is enforced by every member's machine, not suggested by an admin console.
A sub on three primes' programs simply follows three rosters at once;
where they overlap, the strictest policy wins.

Every channel message also carries its **author's own signature**. When a
message reaches you relayed through a teammate, authorship is proof, not
trust - a tampered relay is refused outright and logged in a
tamper-evident audit chain.

## Built for the places clouds can't go

Two laptops on one network segment find each other in under a minute with
zero configuration and zero internet - the discovery beacon carries no
identity at all. Run your own one-file bootstrap node and nothing is ever
announced on any public network. Teammates who opt in can carry channel
messages to people you never overlap with, signatures intact.

Files match the mission: **2 GB chunked transfers** that survive a
dropped link, a killed process, and a restart - resuming where they
stopped and hash-verified on both ends. Denied, disrupted, intermittent,
limited connectivity is the design point, not the failure mode.

## Compliance without a cloud

This is the part that matters at assessment time. One command exports a
**signed evidence bundle** - verified audit chain, roster policy,
retention settings, crypto inventory - mapped to NIST SP 800-171 control
families, and verifiable offline by a third party with nothing but
Node.js. Drop it in an SSP; hand it to a C3PAO.

**Records channels** resolve the retention-versus-ephemerality tension
the DoD IG has documented, instead of dodging it: roster policy can
declare a channel append-only, deletion and self-destruct are refused on
every member's machine, and signed, timestamped transcripts export on
demand - while everything outside records channels stays as ephemeral as
the team wants. CUI marking banners are enforced on both ends of a
conversation.

Even the traffic-metadata claims ship with a review procedure: the app
states exactly what a network observer can and cannot see, and includes a
packet-capture verifier so a reviewer who does not trust the claim can
check it against real bytes.

## A real daily driver

None of this would matter if the tool lost to convenience. The web UI is
a full Slack-style client - channels, threads, reactions, editing,
unread badges, @mentions, desktop notifications, search, voice and video
calls, screen sharing - plus a complete terminal client. One identity
spans up to eight machines, and a stolen laptop can be revoked
account-wide, at which point it stops receiving ciphertext entirely.

At rest, an optional vault encrypts identity, history and files under a
passphrase-derived key, with idle auto-relock, a duress passphrase that
destroys everything and opens an innocent-looking empty account, and a
dead-man switch for abandoned machines.

## Deployment: five minutes, no IT department

Node.js is the only prerequisite. Double-click the launcher, copy your
UID from the sidebar, send it to a teammate over any channel you already
trust, and add theirs. The mutual add is the entire trust ceremony -
verify with matching emoji fingerprints on your first call. No port
forwarding, no firewall tickets, no server to stand up. A team lead who
wants managed policy exports one roster file; everyone imports it. That
is the whole admin story.

## What Freehold does not claim

We would rather you hear the limits from us. There is **no formal
accreditation** - no IL4/IL5, no FedRAMP. Where a contract mandates an
accredited tool, Freehold is the disconnected-operations, cross-org,
records-honest complement, not a compliance substitute; confirm CUI usage
with your FSO. It is built for program teams of tens, not thousands of
seats. It is desktop-only today. And no messenger survives a compromised
endpoint, a peer who leaks what you sent, or a forgotten vault
passphrase - there is no recovery, because nobody else holds your keys.

Every capability above is enforced by the protocol and proven by an
automated end-to-end test gate - 21 suites that spawn real nodes over the
real network and try to break the claim. That discipline, more than any
single feature, is the product.

## Get it

Freehold is free and open source ([repository](https://github.com/WELCOMETOTHETRIBE/chat-tunnel)).
If you want help piloting it on a program team - posture review included -
[start a conversation](/contact).
