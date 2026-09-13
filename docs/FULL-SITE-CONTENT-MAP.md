# EchoFrame: full-site content and production map

The public build now contains 33 pages. The reference informs spacing, hierarchy, feature sections, and navigation depth. EchoFrame retains its own violet/coral identity, audience strategy, writing, and illustrations.

The homepage is a short front door: an animated four-word headline, a single introductory paragraph, a restrained scrolling image, and three claims. Each claim has one explanation and one link to a substantive page (government affairs, distressed debt, methodology). The opening link leads to capabilities. The homepage no longer includes historical EIA charts, dashboards, research-card grids, regional tabs, FAQs, video, or testimonials. Video, contributor quotations, and FAQs are on About; regional coverage and the five Coming soon countries are on Coverage. Deeper pages close with a clear invitation to see how EchoFrame can help. Intake asks for sector, decision, and what the first briefing should demonstrate, with audience presets and full details included in both direct delivery and the email fallback.

## Reader journeys

| Reader | Start | Explore | Inspect | Act |
| --- | --- | --- | --- | --- |
| Oil and gas government affairs | Government affairs | Actor mapping and evidence workspace | Asset-access sample | Briefing form with audience preset |
| Distressed debt | Distressed debt | Decision pathways and sources | Thesis-review sample | Briefing form with audience preset |
| Product evaluation | Capabilities | Three interactive capability pages | Samples, templates, maturity table | Engagement formats |
| Research diligence | Sources | Official records and usage limits | Venezuela context notebook | Define a source plan |
| Trust and procurement | Trust | Privacy and editorial standards | Actual website behavior and scoping requirements | Agree handling before sharing private material |
| Training | The Frame Bureau | Evidence, judgment, and review | Practical learning outcomes | Contact form with training programme selected |

## Content families

| Pages | Content | Source of truth |
| --- | --- | --- |
| Capabilities, actor mapping, evidence workspace, decision pathways | Linked workflow, interactive illustrations, evidence requirements, delivery formats, and development status | `scripts/depth.py`, `assets/site.js` |
| Sample library and two complete specimens | Executive assessment, six analytical sections per brief, evidence register, downloadable copies | `scripts/samples.py`, `content/samples.json` |
| Sources | Six official references, uses, limitations, search and category filters | `content/resources.json` |
| Venezuela context | Dated historical EIA background and original research framework | `scripts/depth.py` |
| Trust and engagement | Actual website behavior, handling requirements, three engagement formats, and preparation checklist | `scripts/depth.py` |
| Audience pages | Research problems, fit criteria, fictional before/after workflow, and deeper reading | `scripts/audiences.py`, `scripts/depth.py` |
| The Frame Bureau | Selective introduction to EchoFrame's training division and practical learning outcomes | `scripts/bureau.py`, `assets/bureau.css` |
| Enquiry form | Decision and asset context, role, phone, headquarters, research format, and referral | `scripts/contact.py`, `assets/site.js`, `server.py` |

Navigation is defined in `scripts/site_navigation.py`. The original library retains its eight complete essays, guides, and programme notes. Existing coverage, methodology, company, privacy, and Spanish overview pages remain available.

The Frame Bureau replaces the former collective naming. Its public introduction draws selectively on the owner-provided private training brief. Do not publish the private access link, recipient or company names, faculty biographies, client case-study claims, performance figures, detailed curriculum, scoring logic, or delivery commitments from that brief. The public page describes the training approach without reproducing the proposal.

## Four publication states

1. **Sourced background:** cite the primary page, identify observation and publication periods, and record review dates. A recent access date is not a recent measurement.
2. **Original research framework:** identify EchoFrame's interpretation and method. Do not imply a source endorses the analysis.
3. **Fictional specimen:** label the cover, document, and download. Keep source IDs and entity names synthetic. It becomes a real case study only when supported by an approved record, not when its label is removed.
4. **Programme design:** distinguish existing foundations, disconnected components, and development requirements. Security controls, performance, partnerships, and delivery commitments need supporting evidence.

## Producing the next layer

### Verified asset brief

Use the mandate template to define the asset, question, observation window, intended reader, and resolution rule. Build the source ledger before drafting the conclusion. Compare an authority record, a local account, and a discriminating observation where available. Record source independence and publication permissions. Have a reviewer challenge the strongest alternative explanation. Publish a dated, appropriately redacted output only when the record supports it.

Produce a homepage teaser, complete brief, dated timeline, actor diagram, and one-page meeting note from that same evidence. Preserve the most consequential limitation in every derivative.

### Political catalyst review

Name the counterparty, thesis assumption, expected milestone, and document that could establish it. Separate intention, authority, implementation, and economic outcome. Build a supporting/challenging/unresolved register. Keep legal and valuation conclusions with the appropriate specialists. End with committee questions and a review trigger.

Produce an assumption card, full note, document timeline, qualitative pathway graphic, and a revision note when the assessment changes.

### Source-directory maintenance

Edit the JSON entry, check the primary link, and record the actual review date. Explain what to capture and what the source cannot prove. Re-check time-sensitive material at the point of use. Flag or replace a reference when its location or access changes.

### Company and trust content

Use confirmed information for company identification. Publish biographies, credentials, testimonials, affiliations, and client outcomes only from an approved supporting record. For a security statement, identify the actual service, implemented control, and evidence of its operation. No fictional people or certifications are needed to complete the design.

## Build and review

Run `python scripts/build.py`, `python scripts/check_site.py`, and `node --check assets/site.js`. With the preview server running, use `python scripts/preview_check.py` and `python scripts/depth_check.py` for browser checks after relevant changes. Inspect mobile and desktop output after structural edits.

The sample HTML and Markdown share the same content records. The build publishes five explicitly authored downloads; private plans and source documents stay outside the allowlist.

The enquiry form now sends details through the configured email service; setup is documented in CONTACT-DELIVERY.md. It does not create a CRM entry. No analytics, newsletter database, or external data integration was added.

The public regional coverage is Venezuela and Europe. Mexico and Middle East coverage, platform previews, and enquiry options have been removed. The former Middle East field guide is retained as an unpublished draft in the editorial source.

Colombia, Mexico, Nigeria, Rwanda, and Pakistan now appear in a shared Coming soon section on the coverage page. They are not active coverage tabs or connected platforms; no launch dates are stated.

The opening headline is Power shifts / Exposure follows, with four staggered word animations. Introductory CTA and audience links omit decorative arrows. The oil image begins within the opening viewport, changes corner curvature and scale with scroll position, and carries no repeated headline overlay. Reduced-motion preferences show a static headline and image. Generated major headings omit sentence-ending full stops; paragraph and testimonial punctuation is preserved.


## Product-brief structure added 11 September 2026

The short homepage now leads with board-defensible judgment, opportunities tested against the client's own bar, and political science run as data science. The three linked pages retain their audience/method routes.

- Capabilities: five risk dimensions and five qualitative Venezuela scenario pathways, with expand-to-read evidence questions.
- Methodology: six analytical layers (NLP/entity recognition, network analysis, drama theory, prospect theory, Bayesian inference, revealed preference), an evidence-to-judgment diagram, the evidence-state explorer, and hard questions.
- Decision pathways: six interactive commercial tests (rule of law, enforceable contracts, predictable rules, infrastructure, credible institutions, policy continuity), followed by the existing fictional question register.
- Audience pages and Venezuela: a 5 / 5 / 6 navigation structure connecting country direction, scenarios, and commercial criteria.
- Contact: a selected decision test carries through to intake and both email delivery paths.
- Venezuela: an anonymised historical assessment summary attributes the reported 74% combined coercive-outcome probability to EchoFrame's private record. The 3 January 2026 event has a separate official reference. The publication does not imply 74% for the specific capture, a complete evaluation, or audited calibration.

The owner confirmed that the underlying assessment is a private client document. No recipient identity, access code, private URL, quoted client material, individual thresholds, event counts, or purported live scores are published. The public site explains the structure; the proprietary brief's displayed August readings are not repackaged as September live data. The older detailed engineering-status table is replaced with reader-facing method explanations, rather than treating an earlier working plan as a present deployment audit.


## Visual cleanup

Removed the visible caption beneath the homepage oil image and decorative directional symbols from shared navigation, links, buttons, diagrams, and JavaScript-generated labels. Native disclosure markers and select arrows are suppressed while controls retain their normal behaviour. The origin of the illustrative image remains documented in the asset attribution file.
