# EchoFrame editorial playbook

The website now works as a publication and a route into the platforms. Its organizing promise is a clearer view of geopolitical developments through evidence, regional context, and visible reasoning. Following the supplied 9 September 2026 plan, Venezuela is the lead development programme: specific assets, contracts, local actors, and questions that can be resolved.

Read `docs/VENEZUELA-CONTENT-STRATEGY.md` for the programme-specific claim boundaries and production formats. A working component reported in the plan is not evidence that the full client workflow is connected. No proposed correspondent, consultancy, or distribution arrangement should be described publicly as an established partnership.

## What readers should find

Give each piece three levels of depth:

1. **The signal:** a specific headline, a short description, and one central idea. Useful in thirty seconds.
2. **The assessment:** a readable explanation of the evidence, competing interpretations, and implications for the research question. Useful in five minutes.
3. **The evidence:** original sources, dates, limitations, a timeline or relationship table, and a revision record. Useful when a reader needs to challenge the assessment.

The homepage introduces the positioning through three short claims and links to deeper explanations. Keep each major section to a headline, one or two sentences, and one next step. Publish substantive updates on the research and regional pages rather than adding more homepage modules. The library adds topic filtering, search, and shareable filter URLs. Article pages include a contents list, central idea, questions to carry forward, source notes, saved state, print layout, and related reading.

## A sustainable publication mix

Start with one substantial piece per week and one shorter update derived from the same research. Increase frequency only when source verification and review capacity can support it. These are proposed operating targets, not claims about an existing publishing team.

| Format | Reader need | Typical scope | Presentation | Starting cadence |
| --- | --- | --- | --- | --- |
| Signal note | What changed? | 250–400 words; one verified development | Observation → context → next check | One per week when warranted |
| Regional brief | Why might this matter? | 700–1,000 words; bounded question | Central judgment, evidence, timeline, alternatives | Two per month |
| Scenario watch | What paths should we monitor? | 600–900 words | Defined outcomes, triggers, review horizon | Monthly, then event-driven revision |
| Actor notebook | Who can influence the decision? | One question and a small evidence-backed network | Labeled relationships with timestamps | Monthly |
| Methods notebook | How should this be assessed? | 500–900 words | Worked hypothetical example and limitations | Monthly |
| Evidence-led case study | What did the product help someone do? | A documented problem, intervention, and outcome | Before/after workflow, permissioned evidence | Only when evidence is ready |
| Analyst conversation | How does an expert frame the problem? | 15–20 minute interview | Edited transcript, three takeaways, source links | Every six to eight weeks |

The library now contains eight pieces: the revised foundations collection and three additional guides on conflicting accounts, resolvable questions, and Venezuela collection priorities. They should not be relabeled as breaking news or current market assessments. Their date is a preparation date. Remaining dashboard screenshots are archive previews; the legacy Venezuela scoring screenshot has been replaced with an explicitly illustrative question brief.

## Eight-week commissioning plan

| Week | Main commission | Research inputs | Companion content |
| --- | --- | --- | --- |
| 1 | Turn client decisions into an initial question register | Three decisions per client; named subjects, horizons, and resolution rules | Publish a fictional question-design walkthrough |
| 2 | A proposed Oriente zone brief | A bounded asset question, reviewed source access, and place-precision rules | Publish a clearly labeled blank or fictional event brief until verified material is available |
| 3 | Competing accounts of one event | Dated claims, independence assessment, and an analyst review | A side-by-side evidence panel; use a fictional example if public disclosure is not cleared |
| 4 | Documented asset viability | Supporting document identifiers, assessment dates, and six criteria | An unassessed/assessed comparison that makes missing evidence visible |
| 5 | A proposed Occidente brief | An asset question, local event evidence, and source limitations | A source-linked timeline with justified geographic precision |
| 6 | A proposed Guayana brief | A power, industrial, or access question; regional context | An annotated relationship diagram with reviewed public detail |
| 7 | A question-update walkthrough | Prior rationale, versioned event links, and update policy | Screen recording only when the workflow actually runs; otherwise label a design demonstration |
| 8 | A resolution and learning note | A resolved question and predefined evaluation policy | If no question has resolved, publish the evaluation protocol rather than a track record |

Topics become commissions only after a specific question, responsible analyst, and usable source set are identified. Avoid filling a schedule with unsupported urgency.

## The production workflow

**Commission.** Fill in `content/brief-template.md`: reader, decision, geography, horizon, key question, intended format, and what would make the piece worth publishing. For Venezuela, use the question-register and event-brief templates as well. Start with the decision, not a request for an unspecified data feed.

**Collect.** Add original material to `content/source-register-template.csv`. Record the original publisher, date, access time, claim supported, independence, and limitations. Distinguish publication time from event time. Record intended use, rights-review status, and disclosure constraints. Public accessibility alone does not establish permission for every downstream use. Keep copyrighted and sensitive source material in an appropriately controlled research workspace; the public repository needs approved citations and summaries, not licensed archives or raw field reports.

**Assess.** Write the observed facts first. Then write the interpretation, the strongest alternative, and the observable evidence that would change the judgment. Keep unresolved questions visible.

**Draft.** Use the structured article format in `content/articles.json`. Write a descriptive title and a plain-language central idea. Use short paragraphs, informative section headings, and references that support the specific claims being made.

**Review.** The editor checks the claim-to-source mapping, uncertainty, dates, naming, and commercial relevance. A regional specialist checks substantive interpretations where needed. Sanctions and regulatory conclusions need appropriate specialist review before being presented as guidance. Do not assert that a review occurred unless it did.

**Package.** Prepare the article, a map or diagram if useful, a chart with a source and defined period, a short excerpt, and a discussion question. Show a timestamp on data graphics. Preserve accessible alternatives and explain the chart's main point in text.

**Publish.** Set the article's status to `published`, run `python scripts/build.py`, and review the generated page. Check the mobile view, sources, title, metadata, and booking route. Deploy through the existing hosting workflow when ready.

**Revisit.** Give current assessments a next review date and a trigger for early review. A revision should state what changed and why. Keep corrections in the source record and visible article notes.

## Use AI for bounded production tasks

These prompts are templates for the team's chosen writing tools. They do not configure a paid service or send any material automatically. Provide the verified source packet with each prompt and review the output.

### 1. Organize evidence

> Using only the supplied source packet, create a claim register. For each claim include the original source identifier, relevant date, exact supporting passage or location, whether it is direct observation or reported information, and limitations. Group reports that trace back to the same original source. Mark unsupported claims UNVERIFIED. Do not infer missing facts.

### 2. Challenge the interpretation

> The research question is [question] for [reader] over [horizon]. The proposed assessment is [assessment]. Using only the supplied evidence register, identify the strongest competing explanation, the assumptions each explanation requires, and the next observation that could distinguish them. Separate criticism of evidence from disagreement about interpretation. Do not invent probabilities.

### 3. Produce a layered first draft

> Draft a [format] for [reader] from the approved evidence register and analyst assessment. Include a descriptive title, a 35-word description, a 50-word central idea, four informative sections, three watchpoints, and source notes. Keep observed facts, analytical judgments, and hypotheses distinguishable. Place each source identifier beside the supported claim. If the evidence does not support a claim, leave an explicit editorial query instead of filling the gap.

### 4. Repurpose an approved article

> Use only this approved article to produce: a 120-word email excerpt, a 180-word professional social post, a six-slide outline with one idea per slide, and a 90-second narration script. Preserve uncertainty and scope. Do not add facts, forecasts, client names, urgency, or performance claims. Link every version back to the full article. Label excerpts so they cannot be mistaken for an updated assessment.

### 5. Audit before publication

> Compare the draft against the source register. Return a table of claims that are unsupported, stronger than their sources, stale, temporally ambiguous, or inconsistent across the draft. Check whether a map or chart caption could imply live data. Identify conclusions that need specialist review. Do not rewrite around evidence gaps; report them.

## Visual production rules

- **Maps:** use real geography, meaningful annotations, a geographic scope, and a source/date caption. An illustrative coverage map should say so. A geographic graphic cannot establish causality.
- **Actor networks:** every connection needs a relationship type and evidence. Color represents a defined category, not an unexplained score.
- **Timelines:** distinguish event dates from publication dates; show formal status and next milestone.
- **Scenarios:** use a comparison matrix or interactive selector. Percentages require a documented estimation method; decorative percentages undermine credibility.
- **Screenshots:** refresh from the actual platform after checking permissions. Identify screenshots as previews and state the captured date where known. Remove confidential data before publication.
- **Photography:** use owned or appropriately licensed work with a caption. Generated illustrations must not be represented as evidence or photos of actual events.
- **Video:** use a specific question, an actual workflow, captions, a transcript, and a clear next step. Load on demand; do not ship all archive videos with every site build.

## One piece, six useful outputs

An approved regional brief can become: the full article, a one-page printable version, a source-linked diagram, a short email excerpt, a narrated walkthrough, and an analyst Q&A. Each version should add a useful way to understand the same work. Recheck the original if a derivative is published much later.

Do not advertise a newsletter subscription until an email provider, consent capture, confirmation flow, unsubscribe handling, and delivery ownership are actually configured. The present site uses an explicit email-draft request and the existing calendar.

## What to measure

Begin with editorial quality: source completeness, correction frequency, review timeliness, and reader questions answered. Then assess which topics lead to substantive briefing inquiries and whether the inquiry describes a relevant research need.

If analytics are introduced later, define necessary events and privacy handling first. Useful questions include whether readers move from an article to its regional coverage page, return to updated research, or book a relevant conversation. No analytics integration is included in this rebuild.

## Evidence still needed for richer commercial content

Prepare permissioned analyst biographies, named subject expertise, current product screenshots, a documented client workflow, and any support for performance claims. Publish a case study only when the outcome can be substantiated and the client has approved its use. The rebuild intentionally uses methodology and inspectable research as the public evidence of depth.
