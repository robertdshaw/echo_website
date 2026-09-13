# September content revision review

Completed locally on `content-fix-sept`. Nothing pushed or deployed. The review build has 28 public pages and four retained articles. The generated `site.html` legacy alias is excluded from publication. The original Markdown snapshot is archived.

## Ordered commits

A baseline commit, `3396756`, preserves the pre-existing website so the requested revisions can be reviewed separately. The eleven approved items then have one local commit each.

| Item | Commit | Result |
| --- | --- | --- |
| 1 | 2530d98 | Home positioning narrowed. Coming-soon countries retained. EU tracker available on request with field guide. |
| 2 | 3a87af4 | Frame Bureau condensed on About; standalone page archived. |
| 3 | eed5847 | Four articles rewritten plainly, unused filters and reading times removed, Robert Shaw bylines and date markers. |
| 4 | 488934e | Three About audience cards, channel wording marker, testimonials unchanged. |
| 5 | 06682f4 | Invented cases removed from pages, data and downloads; real-material placeholders inserted. |
| 6 | 12893f7 | Trust retains engagement handling and links to privacy and editorial standards. |
| 7 | d490ed9 | Eight-field contact form and server delivery to contact@echoframe.co. |
| 8 | fe389dd | One distinct enquiry invitation per page; reference pages have none. |
| 9 | 0512633 | Existing headlines retained pending Rob's replacements. |
| 10 | 2f1360b | Map pages and assets archived intact; Venezuela visualisation placeholders. |
| 11 | This commit | Model facts and style pass, final CTA cleanup, content export and verification report. |

## Headlines and style

Existing headlines remain, including paired headlines, under revised item 9. Headings belonging to removed examples or archived sections leave with those sections. The requested About card names, factual counts, dimension names and placeholder headings are the exceptions. No substitute marketing headlines have been written.

[[ROB: supply revised headlines]]

The public text, scripts, SVG text and downloadable Markdown contain no em dashes. Colons that remain introduce lists, mark fields or form part of preserved headlines and owner markers. Body copy has been revised without reducing the explanatory sections to slogans. Research article claims and existing primary references are retained.

The six dimensions use Rob's supplied names. Prospect theory is removed. Named scenarios are removed and the replacement is stated in one sentence. Rob supplied the name of the Social dimension but no definition, so its explanation remains an owner marker. The existing LinkedIn address and both testimonial quotations remain unchanged.

The final CTA review also removed secondary “Tell me more”, “Learn how” and duplicate article prompts. Navigation, linked article titles, source documents, downloads, privacy requests and reading controls remain usable. They are reference links or interface controls, rather than additional enquiry invitations.

## Owner markers by page and line

Generated HTML is compact, so several markers can share a line. Dates appear in both the article byline and its source note. These are intentionally visible review markers, not confirmed dates or permission claims.

| Page and line | Marker |
| --- | --- |
| [about.html:8](../about.html#L8) | [[ROB: confirm wording and whether the channel partner may be named]] |
| [about.html:8](../about.html#L8) | [[ROB: confirm written permission on file for the Luis Matos Azócar quote]] |
| [about.html:8](../about.html#L8) | [[ROB: confirm written permission on file for the Jean-Christophe Loubier quote]] |
| [actor-mapping.html:8](../actor-mapping.html#L8) | [[ROB: supply real redacted material for actor and asset mapping]] |
| [capabilities.html:8](../capabilities.html#L8) | [[ROB: confirm the definition and evidence covered by the Social dimension]] |
| [coverage.html:8](../coverage.html#L8) | [[ROB: supply real redacted material for the coverage overview]] |
| [decision-pathways.html:8](../decision-pathways.html#L8) | [[ROB: supply real redacted material for decision pathways]] |
| [distressed-debt.html:8](../distressed-debt.html#L8) | [[ROB: supply real redacted material for distressed-debt research]] |
| [evidence-workspace.html:8](../evidence-workspace.html#L8) | [[ROB: supply real redacted material for evidence review]] |
| [government-affairs.html:8](../government-affairs.html#L8) | [[ROB: supply real redacted material for government affairs]] |
| [methodology.html:8](../methodology.html#L8) | [[ROB: supply real redacted material for the analytical method]] |
| [research/following-european-energy-policy.html:8](../research/following-european-energy-policy.html#L8) | [[ROB: confirm dates]] |
| [research/following-european-energy-policy.html:8](../research/following-european-energy-policy.html#L8) | [[ROB: supply real redacted material for following-european-energy-policy]] |
| [research/following-european-energy-policy.html:8](../research/following-european-energy-policy.html#L8) | [[ROB: confirm dates]] |
| [research/questions-that-can-resolve.html:8](../research/questions-that-can-resolve.html#L8) | [[ROB: confirm dates]] |
| [research/questions-that-can-resolve.html:8](../research/questions-that-can-resolve.html#L8) | [[ROB: supply real redacted material for questions-that-can-resolve]] |
| [research/questions-that-can-resolve.html:8](../research/questions-that-can-resolve.html#L8) | [[ROB: confirm dates]] |
| [research/venezuela-from-country-to-asset.html:8](../research/venezuela-from-country-to-asset.html#L8) | [[ROB: confirm dates]] |
| [research/venezuela-from-country-to-asset.html:8](../research/venezuela-from-country-to-asset.html#L8) | [[ROB: supply real redacted material for venezuela-from-country-to-asset]] |
| [research/venezuela-from-country-to-asset.html:8](../research/venezuela-from-country-to-asset.html#L8) | [[ROB: confirm dates]] |
| [research/when-sources-disagree.html:8](../research/when-sources-disagree.html#L8) | [[ROB: confirm dates]] |
| [research/when-sources-disagree.html:8](../research/when-sources-disagree.html#L8) | [[ROB: supply real redacted material for when-sources-disagree]] |
| [research/when-sources-disagree.html:8](../research/when-sources-disagree.html#L8) | [[ROB: confirm dates]] |
| [sample-asset-access.html:8](../sample-asset-access.html#L8) | [[ROB: supply real redacted material for Asset-context and stakeholder brief]] |
| [sample-briefs.html:8](../sample-briefs.html#L8) | [[ROB: supply real redacted material for the sample brief collection]] |
| [sample-thesis-review.html:8](../sample-thesis-review.html#L8) | [[ROB: supply real redacted material for Thesis-assumption and catalyst review]] |
| [venezuela.html:8](../venezuela.html#L8) | [[ROB: supply the completed José asset map for public review]] |
| [venezuela.html:8](../venezuela.html#L8) | [[ROB: supply a dated question probability chart for public review]] |
| [venezuela.html:10](../venezuela.html#L10) | [[ROB: supply real redacted material for the Venezuela asset case]] |

## Archived material

All archive paths are inside `_unpublished/` and excluded from the allowlisted publication build. No redirects expose the removed content. Returning these pages requires an explicit later build change.

| Original | Archive | Reason |
| --- | --- | --- |
| frame-bureau.html | _unpublished/frame-bureau.html | Condensed into About |
| scripts/bureau.py | _unpublished/scripts/bureau.py | Standalone generator retired |
| research/from-signal-to-significance.html | _unpublished/research/from-signal-to-significance.html | Outside retained four |
| research/mapping-power-without-false-precision.html | _unpublished/research/mapping-power-without-false-precision.html | Outside retained four |
| research/sanctions-and-operational-reality.html | _unpublished/research/sanctions-and-operational-reality.html | Outside retained four |
| research/scenarios-that-can-be-tested.html | _unpublished/research/scenarios-that-can-be-tested.html | Outside retained four |
| research/reading-maritime-disruption.html | _unpublished/research/reading-maritime-disruption.html | Pre-existing unpublished draft retained in archive |
| Removed and original retained article records | _unpublished/content/articles.json; retained-articles-before-edit.json | Original wording preserved |
| Invented sample records | _unpublished/content/samples.json | Real material pending |
| downloads/sample-asset-access.md | _unpublished/downloads/sample-asset-access.md | Invented brief withdrawn |
| downloads/sample-thesis-review.md | _unpublished/downloads/sample-thesis-review.md | Invented brief withdrawn |
| Invented JavaScript workbenches | _unpublished/assets/fictional-workbenches.js | Examples withdrawn |
| map.html; es/map.html | _unpublished/map.html; _unpublished/es/map.html | Public map withdrawn |
| assets/gis-demo/; assets/map.js; assets/map.css | Same paths under _unpublished/ | Map data and presentation preserved intact |
| scripts/map_data.py; map_page.py; check_map.py | Same paths under _unpublished/scripts/ | Map generation and checks retired |
| EchoFrame-Website-Content.md | _unpublished/EchoFrame-Website-Content-before-revision.md | Previous content snapshot preserved |

The map returns after the real José asset case is ready for public review. No return date is asserted. The map and question-probability chart each have a “To follow” placeholder on Venezuela.

## Verification

- `python scripts/build.py` succeeds. The allowlist publishes 28 pages, four research articles, three blank templates and the retained presentation assets.
- `python scripts/check_site.py` passes local links, fragments, image references, unique IDs, article counts and archive exclusions. No sitemap or separate navigation JSON existed; generated navigation and related links were updated.
- `python scripts/test_contact.py` passes all 14 tests, including fixed recipient, all eight fields, confirmation, failed delivery, idempotency, validation and private-file exclusion.
- `python scripts/preview_check.py` passes all 28 pages at 1440px and 390px, with no JavaScript errors or horizontal overflow. It exercises real browser submission to a local email stub, failure retention, filters and interactive method controls. No email was sent.
- `node --check assets/site.js` passes.
- Additional review checks confirm six exact dimension names, absent prospect theory and named scenarios, no invented Terminal A or Issuer B text, four unchanged article headlines, unchanged testimonials and LinkedIn, retained coming-soon countries, unique enquiry wording and visible owner markers.
- All 34 map archive files match their pre-move SHA-256 hashes in `_unpublished/map-archive-sha256.json`.
- External websites and production email delivery were not exercised. The live service still needs its configured SMTP or Resend credentials; the server reports unavailable or failed delivery honestly.
- `python scripts/export_content.py` refreshes the complete local review text in `EchoFrame-Website-Content.md`. It does not describe these changes as deployed.

## Files changed by the revision

The list below compares against the preserved baseline, excluding pre-existing unrelated `.gitignore` and `render.yaml` edits. The local work also leaves pre-existing untracked deployment notes, README, environment example and preview configuration untouched.

- `404.html`
- `EchoFrame-Website-Content.md`
- `_unpublished/EchoFrame-Website-Content-before-revision.md`
- `_unpublished/README.md`
- `_unpublished/assets/fictional-workbenches.js`
- `_unpublished/assets/gis-demo/LICENSE.txt`
- `_unpublished/assets/gis-demo/boundaries.json`
- `_unpublished/assets/gis-demo/catalogue.json`
- `_unpublished/assets/gis-demo/months/2024-10.json`
- `_unpublished/assets/gis-demo/months/2024-11.json`
- `_unpublished/assets/gis-demo/months/2024-12.json`
- `_unpublished/assets/gis-demo/months/2025-01.json`
- `_unpublished/assets/gis-demo/months/2025-02.json`
- `_unpublished/assets/gis-demo/months/2025-03.json`
- `_unpublished/assets/gis-demo/months/2025-04.json`
- `_unpublished/assets/gis-demo/months/2025-05.json`
- `_unpublished/assets/gis-demo/months/2025-06.json`
- `_unpublished/assets/gis-demo/months/2025-07.json`
- `_unpublished/assets/gis-demo/months/2025-08.json`
- `_unpublished/assets/gis-demo/months/2025-09.json`
- `_unpublished/assets/gis-demo/months/2025-10.json`
- `_unpublished/assets/gis-demo/months/2025-11.json`
- `_unpublished/assets/gis-demo/months/2025-12.json`
- `_unpublished/assets/gis-demo/months/2026-01.json`
- `_unpublished/assets/gis-demo/months/2026-02.json`
- `_unpublished/assets/gis-demo/months/2026-03.json`
- `_unpublished/assets/gis-demo/months/2026-04.json`
- `_unpublished/assets/gis-demo/months/2026-05.json`
- `_unpublished/assets/gis-demo/months/2026-06.json`
- `_unpublished/assets/gis-demo/months/2026-07.json`
- `_unpublished/assets/gis-demo/months/2026-08.json`
- `_unpublished/assets/gis-demo/months/2026-09.json`
- `_unpublished/assets/map.css`
- `_unpublished/assets/map.js`
- `_unpublished/content/articles.json`
- `_unpublished/content/retained-articles-before-edit.json`
- `_unpublished/content/samples.json`
- `_unpublished/downloads/sample-asset-access.md`
- `_unpublished/downloads/sample-thesis-review.md`
- `_unpublished/es/map.html`
- `_unpublished/frame-bureau.html`
- `_unpublished/map-archive-sha256.json`
- `_unpublished/map.html`
- `_unpublished/research/from-signal-to-significance.html`
- `_unpublished/research/mapping-power-without-false-precision.html`
- `_unpublished/research/reading-maritime-disruption.html`
- `_unpublished/research/sanctions-and-operational-reality.html`
- `_unpublished/research/scenarios-that-can-be-tested.html`
- `_unpublished/scripts/bureau.py`
- `_unpublished/scripts/check_map.py`
- `_unpublished/scripts/map_data.py`
- `_unpublished/scripts/map_page.py`
- `about.html`
- `actor-mapping.html`
- `assets/site.js`
- `briefing.html`
- `capabilities.html`
- `content/articles.json`
- `content/samples.json`
- `coverage.html`
- `decision-pathways.html`
- `distressed-debt.html`
- `docs/CONTENT-FIX-REVIEW.md`
- `editorial-standards.html`
- `engagement.html`
- `es/index.html`
- `evidence-workspace.html`
- `government-affairs.html`
- `index.html`
- `methodology.html`
- `privacy.html`
- `research.html`
- `research/following-european-energy-policy.html`
- `research/questions-that-can-resolve.html`
- `research/venezuela-from-country-to-asset.html`
- `research/when-sources-disagree.html`
- `sample-asset-access.html`
- `sample-briefs.html`
- `sample-thesis-review.html`
- `scripts/audiences.py`
- `scripts/build.py`
- `scripts/check_site.py`
- `scripts/contact.py`
- `scripts/depth.py`
- `scripts/experience.py`
- `scripts/export_content.py`
- `scripts/homepage.py`
- `scripts/intelligence.py`
- `scripts/page_presentation.py`
- `scripts/placeholders.py`
- `scripts/preview_check.py`
- `scripts/programme.py`
- `scripts/samples.py`
- `scripts/site_navigation.py`
- `scripts/test_contact.py`
- `server.py`
- `site.html`
- `sources.html`
- `trust.html`
- `venezuela-context.html`
- `venezuela.html`
