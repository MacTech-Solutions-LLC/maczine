---
title: "AI Proposal Writing for Government Contracts: What's Allowed"
description: AI proposal writing for government contracts is generally allowed. Certifying what the model invented is not. Three scenarios, three controls.
publishedAt: 2026-10-01T08:00:00-04:00
author: Matthew Davis
issue: 47
kicker: Explainer · AI and Proposals
tags:
  - ai
  - proposals
  - capture
  - false-claims-act
  - federal-contracting
stats:
  - n: "3729(b)(1)"
    label: the False Claims Act definition under which reckless disregard of the truth counts as knowing - no specific intent to defraud required
  - n: "Sept. 25, 2025"
    label: the NIH receipt date from which grant applications substantially developed by AI are not treated as the applicants' original ideas
  - n: "May 7, 2025"
    label: the date GAO warned, in Raven Investigations, that filings citing non-existent authority may draw sanctions
asides:
  - title: The AI clause everyone cites is about performance
    body: In March 2026 GSA released a draft GSAR clause, 552.239-7001, "Basic Safeguarding of Artificial Intelligence Systems," aimed at Multiple Award Schedule contracts for AI capabilities. As law-firm analyses of the draft describe it, its disclosure duties attach to AI tools used in contract performance, not to how an offeror wrote its bid. Check the clause's current status before a bid decision leans on it.
---

The question capture teams keep asking about generative AI is the wrong one. They want to know whether they are allowed to use it on a proposal, as if the risk lived in the drafting. For most federal procurements, AI proposal writing for government contracts is not the problem - the signature is. An offeror that submits a proposal is representing that what it says is true, and no regulation, statute, or evaluator will split that responsibility with the model that produced the paragraph.

Here is the direct answer. MacZine could find no FAR or DFARS clause that bars an offeror from drafting a proposal with generative AI, or that requires the offeror to disclose that it did. Where rules for generative AI in federal proposals exist at all, they are emerging solicitation by solicitation, and the most visible federal AI clause so far governs AI used in contract performance rather than AI used to write the bid. Grants run stricter. NIH announced in July 2025 that it will not treat applications substantially developed by AI as the applicants' original ideas, effective for the September 25, 2025 receipt date, and NSF has encouraged proposers since December 2023, without requiring it, to say how generative AI was used. Those are grant policies, not FAR rules, but they show the direction of travel.

What no policy changes is liability for what goes out the door. 18 U.S.C. 1001 reaches knowingly and willfully false material statements made within the jurisdiction of a federal agency. The False Claims Act asks less: under 31 U.S.C. 3729(b)(1), acting in reckless disregard of the truth counts as acting knowingly, with no proof of specific intent to defraud, and under a fraudulent-inducement theory a contract won on a material misrepresentation can make the claims paid under it false. Neither statute cares which tool typed the sentence. Three ordinary proposal moments show where that bites.

## AI proposal writing and the technical approach nobody on staff wrote

Picture a small cyber firm nine days from a task order deadline. The volume lead feeds the performance work statement and a folder of old proposals into a commercial AI tool and gets back a fluent, well-organized technical approach in an afternoon. Nothing about that is prohibited, and a model is a reasonable first-draft engine for structure and connective prose.

The rule that governs this volume is not about AI at all. FAR 15.305 requires the agency to evaluate proposals solely on the factors and subfactors the solicitation specifies, and machine authorship is not one of them. That disposes of a myth that circulates in capture shops - that evaluators run detectors and toss anything that trips one. The opposite myth, that nobody can tell and so it is safe, fails for the same reason. A technical approach assembled from generic patterns tends to restate the requirement instead of offering a method for meeting it, and evaluators assign strengths for specifics an offeror can back up, not for polish. The AI-shaped proposal loses the way weak proposals always have: quietly, on the merits.

The sharper break is in the folder. Suppose it includes nonpublic documents the firm received while supporting the same agency on a different contract. A retrieval-backed tool will surface that material into a competitive proposal without saying where it came from. FAR subpart 9.5 treats source selection information unavailable to other competitors as a source of unfair competitive advantage, and 41 U.S.C. 2102 bars anyone from knowingly obtaining contractor bid or proposal information or source selection information before award. The model cannot tell which paragraph in its context was government-furnished. The engineer who worked the other contract can.

So the control here is an owner, not a tool ban: one named person per volume who reads every page, can defend each method it promises, and knows the provenance of everything that went into the model's context.

## Past performance that happened only in the model

Now picture the same team handing the tool three contract numbers and a page of notes and asking for polished past performance write-ups and key personnel resumes. This is where generative AI is most tempting and most dangerous, because the output looks exactly like what Section L asks for - quantified outcomes, crisp narratives, a certification here, a clearance there - and some of it may not be true. Models fill gaps with plausible detail. A note that says "improved patching" can come back as a percentage reduction nobody measured. A resume can acquire a credential its subject never earned.

Procurement forums have already seen unverified model output. In Raven Investigations & Security Consulting, decided May 7, 2025, GAO found quotations in a pro se protester's filing that could not be traced to the decisions they were attributed to, and it warned that citing non-existent authority may result in sanctions; the protester acknowledged the problems stemmed partly from AI-assisted tools. That was a protest filing rather than a proposal, but the failure is identical, and a past performance evaluator holds an advantage the model lacks. FAR 15.305 lets the government weigh the references an offeror supplies against information it obtains from other sources, and agencies keep their own contractor evaluations in CPARS.

An invented metric in that volume is not a typo; it is a statement in a document submitted to win a contract. Caught before award, a single fabricated figure costs credibility. A pattern of them, left in because nobody looked, invites the question the False Claims Act's reckless-disregard standard was written to ask.

> The model will never sign the proposal. Someone at your company will, and the law reads that signature, not the prompt history.

The control is a claims-verification pass run by someone other than the drafter. Every number, date, dollar value, certification, clearance, and named customer in the past performance and key personnel sections gets traced to a source document - the contract, a CPARS evaluation, a signed letter of commitment - before the volume closes. A claim that cannot be traced comes out.

## A compliance matrix that dropped a shall

The third moment feels safest. Picture a capture manager using AI for RFP response triage, pasting a long solicitation into a tool and asking for a compliance matrix.

Two things break. The first is the paste. A solicitation package can carry attachments marked CUI, technical data with export-control restrictions, or a teaming partner's proprietary pricing that arrived under a nondisclosure agreement. Whether any of it may enter a commercial tool is decided by obligations already on your contracts and agreements, and MacZine has walked [the cloud clause that answers the CUI question](/maczine/ai-tools-cui-dfars-cloud-clause).

The second is the summary itself. A model condensing Section L will paraphrase, merge, and occasionally drop requirements, and a matrix that loses one "shall" - a page limit, a format rule, a required representation - can sink an otherwise strong proposal on compliance before anyone scores it. If an agency adds AI disclosure language to a solicitation, asking offerors to identify AI-assisted sections or keep usage records, that sentence is in the document you just asked a model to compress.

The control is a source-traceable matrix: every row cites the section and paragraph it came from, and a human checks each row against the solicitation text rather than against the summary. It is the same front-to-back discipline MacZine laid out for [reading a solicitation's compliance clauses before you bid](/maczine/solicitation-compliance-clause-scan), with the AI output treated as a first pass to audit, never as the record.

None of the three controls costs the speed that made the tool attractive, and all three rest on one principle: AI drafts, a named human decides, and the decision leaves a trail. MacTech builds its own agent tooling on that principle - [IBE](/maczine/ibe-ai-agent-autonomy-gate) settles an AI agent's authority before it acts - and the [Market](/market) lists Proposal Volume Authoring and an AI Assurance Package for firms that want help on either side of the problem, or you can [talk to MacTech](/contact) directly.

When a solicitation on your pipeline does ask offerors to describe their use of generative AI, the firm with a volume owner, a verified claims log, and a traceable matrix will answer it in two sentences. The firm without them will be reading back through chat histories to work out who wrote what, a week before the proposal is due.
