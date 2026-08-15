---
title: Home Office CUI Scope Starts at the Kitchen Table
description: NIST 800-171 physical protection assumes an office, not a house. Keep CUI off the remote endpoint and most of the control problem disappears.
publishedAt: 2026-08-28T08:00:00-04:00
author: Maxine
issue: 29
kicker: Field Report · Remote Work
tags:
  - remote-work
  - physical-protection
  - cui
  - nist-800-171
stats:
  - n: "4"
    label: physical protection requirements written for a building, not a residence (3.10.1, .3, .4, .5)
  - n: "3"
    label: remote access controls that make most of them moot - 3.1.12, 3.1.13, 3.1.14
---

A defense contractor's assessment boundary lives on a network diagram until the day an employee opens a CUI-marked drawing at the kitchen table, on a laptop the company issued, on a home network shared with a teenager's gaming console, next to a printer that has never appeared on an inventory anywhere. NIST SP 800-171's physical protection family, the requirements clustered under 3.10, was written for organizational systems in organizational spaces: a building with a badge reader, a lobby with a sign-in sheet, a server closet with a lock nobody else holds the key to. Nobody drafting that language pictured a spare bedroom with a school laptop charging on the same power strip.

Read 3.10 literally against a residence and it breaks almost immediately. Limit physical access to authorized individuals, 3.10.1 says, and in a house the authorized individual's spouse walks past the desk every evening carrying laundry. Escort and monitor visitors, 3.10.3 says, and in a house a visitor is a neighbor picking up a borrowed drill or a teenager's friend staying for dinner, nobody escorting anybody. Maintain audit logs of physical access, 3.10.4 says, to a room with no badge reader and no log of any kind. Control and manage physical access devices, 3.10.5 says, to a front door key that has been cut for a house cleaner, a dog walker, and an in-law who watches the kids on Tuesdays. None of that is a contractor being careless. It is a residence behaving like a residence, and a requirement written for a facility does not bend to fit one just because a compliance team wishes it would.

The honest response is not to write a home-office visitor log nobody will maintain past the first quarter, or to pretend the spouse is now an "authorized individual" on a roster somewhere. The honest response is to notice that 3.10 assumes CUI is sitting on the machine in that room, and to make that assumption false. 3.1.12 requires monitoring and controlling remote access sessions. 3.1.13 requires cryptographic protection of those sessions. 3.1.14 requires routing remote access through managed access control points. Put the three together correctly and the endpoint at the kitchen table never holds a CUI file at all. It holds a thin session into a controlled enclave, a window of pixels rendered from a system that lives somewhere the badge reader and the audit log already cover. The laptop can be lost, seized, or left open next to a curious ten-year-old, and nothing leaves with it, because nothing was ever on it to begin with.

> A requirement written for a building does not bend to fit a residence. It has to be made not to apply.

That is the same trade this newsletter priced when it compared [scoping a CUI enclave against scoping a whole network](/maczine/cui-enclave-or-whole-network-scoping): pulling the boundary in is cheaper than remediating everything inside it, because the things outside the boundary are out of scope rather than merely trusted to behave. Applied to a person instead of a network, the arithmetic is the same and the stakes are higher, because a network segment does not have a family living in it. Once CUI cannot land on the endpoint, most of 3.10's home-office problem collapses to one achievable habit: lock the screen when you step away, and keep the session inside a boundary built to hold it - the same [enclave architecture](/cui-enclave-architecture) that makes the office-versus-house question moot in the first place. NIST SP 800-171 even names the exception directly: 3.10.6 requires safeguarding measures for CUI at alternate work sites, which is the framework's own admission that a residence is not a facility and needs its own answer, not a photocopy of the office policy.

None of that architecture reaches the part of home-office CUI handling that will not go away, because it is not a network problem. It is printing. A home printer is the most common quiet CUI spill a small shop will produce, not because anyone means to leak anything, but because printing a drawing to check a dimension is a reflex nobody thinks to gate, and the page that comes out sits next to a printer with a memory nobody has ever wiped and a recycling bin nobody treats as a destruction control. Paper storage is the same problem in slower motion: a folder in a home-office drawer, in a house with no shredder anyone trusts to actually run, next to the recycling that goes out on Thursday. And the family computer deserves its own line, because the machine that only ever needed to check email eventually gets a document copied onto it "just for a minute," and a minute is exactly how a scope boundary fails.

None of that residue is architecture's job to solve, and pretending otherwise is how programs end up writing unenforceable physical-access policies for houses instead of an honest answer for the printer. The honest answer is a written remote-work standard, short enough that someone will actually read it: what may leave the enclave and land locally, what may be printed and on which device, where that printer lives and who empties it, and what happens at termination when the laptop, the badge, and whatever got printed are four hundred miles away in a spare room nobody from the company has ever seen. That document will not stop every spill. It will make the ones that happen visible, which is the only thing a policy was ever going to do once the architecture had already done the real work.
