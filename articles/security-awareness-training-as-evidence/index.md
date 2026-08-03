---
title: Your Training Records Are Compliance Evidence. Are They?
issue: 17
description: Three CMMC controls turn security awareness training into an evidence problem. Most organizations do the training and fail the control anyway.
publishedAt: 2026-08-13T08:00:00-04:00
tags:
  - cmmc
  - nist-800-171
  - training
  - compliance
kicker: Explainer · Workforce
asides:
  - title: Role-based, not generic
    body: The control asks that personnel are trained for **their assigned duties**. A systems administrator with CUI access and a warehouse clerk without it should not receive identical training - and identical records suggest nobody looked.
---

*"We do annual security awareness training."* Every contractor says it, most of them truthfully, and a surprising number still take a finding on the control. The training is not the problem. The record of it is.

Three questions separate an organization that trains its people from one that can prove it, and they are worth asking before an assessor asks them.

**Can you show who was trained, on what, and when?** Not a completion percentage - a per-person record with a date, tied to a specific curriculum version.

**Was the training relevant to what that person actually does?** The requirement is role-based. Identical training for an administrator with enclave access and a clerk without it is a signal that roles were never analyzed.

**What happened to the people who did not complete it?** This is the one that fails programs. A completion rate of 94% is not evidence of a control operating; it is evidence of six people who did not do the thing, and the assessor's next question is what you did about them.

## Why the record is harder than the training

The training itself is a solved problem. Content exists, vendors are plentiful, and an hour of anyone's time is not a difficult ask. The difficulty is that the evidence has to survive the passage of time in a way most organizations never plan for.

An assessment happens well after the training. What gets examined is not the session but the residue of it, and the residue is usually spread across a spreadsheet somebody maintained, an email thread confirming attendance, and a vendor portal that shows current status but not historical state. Reconstructing "who had completed which version as of last March" from those three sources is an afternoon of work at best and impossible at worst.

The insider-threat and role-specific requirements make it harder still, because now the record has to show not just completion but *appropriateness* - that the person received training matched to their duties. That is a claim about the curriculum design, not just the attendance list, and it needs to have been true at the time rather than argued afterward.

## What an auditable training system has to do

This is why MacTech's [training platform](/training) is built around learning objects, curricula, and assignments as distinct concepts rather than as a course catalog with a completion checkbox.

The separation is what makes the evidence work. Learning objects - articles, slide decks, videos, quizzes, attestations - are the content. A curriculum composes them into a path. An assignment binds a curriculum to a person or group with a due date. Because those are separate records, the system can answer the historical question: this person was assigned this curriculum, composed of these objects, on this date, and completed it on that one.

Two further properties matter for compliance specifically. Attestations are a first-class object type, which is how you evidence that someone acknowledged a policy rather than merely watched a video about it. And audit logging covers system events, so the record of the record is itself defensible - a detail that sounds excessive until an assessor asks whether completion dates could have been edited.

Multi-tenancy and role-based access are there for a related reason: an organization running training for its own staff and for a subcontractor's needs those populations separated, with the evidence separable too.

## The honest limit

None of this makes anyone more secure by itself. Training records are evidence of an activity, and the activity is only as good as the content and the seriousness with which people take it. A perfect audit trail documenting a curriculum nobody paid attention to satisfies the control and protects nothing.

That is worth saying plainly, because the compliance framing tempts organizations toward optimizing the record rather than the outcome. The control exists because people are the path most incidents actually take - the [72-hour incident clock](/maczine/dfars-7012-72-hour-incident-clock) usually starts with something a person clicked. The record is how you prove you addressed that. It is not the addressing.

Build both. But if you only have the training and not the record, an assessor will conclude you have neither, and they will be within their rights. ◆
