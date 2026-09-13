# Content rewrite report

Branch `content-rewrite`. Thirteen items, one commit each, in the order given except item 6,
which waited on four lines of copy and was committed after item 7. Nothing has been pushed and
nothing has been deployed.

The site is generated. Every HTML page is written by the Python modules under `scripts/`, so the
copy changes are in those modules and the HTML files are build output committed alongside them.

## Three questions answered before writing

These were asked because the source documents contradicted each other or did not supply something
the item needed. The answers are recorded here because they change what is on the site.

1. **The Venezuela probability.** The live site said 74 per cent, `site_brief.md` and
   `worked_examples.md` said forty per cent, both dated 2 December 2025, and the standing rule says
   no figure from client work appears on the site. Decision: no number, direction only. Both pages
   now say a minority probability. The 74 per cent section is deleted.
2. **The demo link.** No demo URL exists in any of the four documents. Decision: the chat teaser is
   a static exchange and the page's enquiry button leads to the contact form.
3. **The methodology page.** `site_brief.md` says How it works replaces it; the item list did not
   list it for removal. Decision: delete it, repoint the navigation and footer, and add a 301.

A fourth question produced the four one-line reasons for Colombia, Mexico, Rwanda and Pakistan,
which are used verbatim on the coverage page.

## Pages added

| Page | Item |
| --- | --- |
| `how-it-works.html` | 2 |
| `case-study-venezuela.html` | 3 |
| `worked-examples.html` | 4 |
| `frame-bureau.html` | 5 |

`frame-bureau.html` was on the publication exclusion list in `scripts/check_site.py` as an internal
document. It has been taken off it.

## Pages removed

`methodology.html`. `server.py` answers the old URL with a 301 to `/how-it-works.html`.

## Files changed

**New generator modules:** `scripts/how_it_works.py`, `scripts/case_study.py`,
`scripts/worked_examples.py`, `scripts/frame_bureau.py`, `scripts/coverage_page.py`,
`scripts/spanish_page.py`, `scripts/chrome.py`.

**Edited generator modules:** `scripts/build.py`, `scripts/homepage.py`, `scripts/experience.py`,
`scripts/contact.py`, `scripts/depth.py`, `scripts/intelligence.py`, `scripts/programme.py`,
`scripts/audiences.py`, `scripts/samples.py`, `scripts/site_navigation.py`,
`scripts/page_presentation.py`, `scripts/export_content.py`.

**Content data:** `content/articles.json`, `content/samples.json`, `downloads/research-mandate.md`.

**Application:** `server.py` (field table, methodology redirect), `assets/site.js` (payload fields,
confirmation).

**Checks and tests:** `scripts/check_site.py`, `scripts/test_contact.py`, `scripts/depth_check.py`,
`scripts/preview_check.py`.

**Build output:** 34 HTML files at the repository root, including the new pages and the deleted one,
plus the regenerated `EchoFrame-Website-Content.md` snapshot.

**Housekeeping:** `.gitignore` now ignores Python bytecode, and `scripts/__pycache__` is untracked.
It was committed by accident in an earlier item.

## Everything removed, and why

| Removed | Where | Why |
| --- | --- | --- |
| The five analytical layers, including drama theory | `scripts/intelligence.py`, methodology page | The page they served is replaced by the six-step loop. Keeping both would state the same idea twice. |
| The evidence-state explorer | methodology page | Went with that page. The corroboration section on How it works now carries the argument. |
| The selected historical assessment, at 74 per cent | Venezuela page | A figure taken from client work. |
| Individual readings quoted in the reference page | How it works, case study | Same reason. The reference page quotes numbers such as 75.7 and 59.2 from the client series. |
| A claim of collection across more than fifty sources with correspondents in place | How it works, step 1 | The brief says the correspondent agreement is in progress, so the claim overstates it. |
| Module 4 asking trainees to re-weigh five outcomes | Frame Bureau | The five named scenarios are retired. It now says the desk's own questions. |
| A bench line describing anticipatory work | Frame Bureau | Too close to a phrase the brief retires. |
| The Qatar Leadership Centre framing and the embedded chat | Frame Bureau | Client-specific, per item 5. |
| The condensed Frame Bureau section on About | About | Superseded by the page. |
| Nigeria | Coverage | Not in the brief's list of four. Removed on your instruction. |
| Worked example card 1, the succession | Worked examples | The case study is the better version of the same engagement and it carries the chart. A card pointing at another page is a signpost, not content. |
| The role field | Contact form and server | Item 9 names seven fields and role is not one of them. |
| The request reference on the confirmation | Contact form | Meaningless to the visitor. Still generated and still in the email, so duplicate suppression is unaffected. |
| Per-format buttons on engagement, per-card links on the home page | Engagement, home | One invitation per page. |
| The unused region tab widget, `home_directory`, `formats`, `charts`, `programme_teaser` | Generator modules | Dead code that no page rendered. The last three are left in place but unreferenced. |
| Slogan headings built from two clauses | Site-wide | House rules. |
| The stale evidence-state block in the content snapshot exporter | `scripts/export_content.py` | Described a selector that no longer exists. |

### Named in the items but already absent

Four things the items asked me to remove are not in this build. They were taken out before this
rewrite and needed no change.

- Prospect theory. It appears nowhere.
- The five named scenarios. Already replaced by dated questions.
- The platform assurance paragraph on the trust page.
- The Terminal A material and every other invented example, including on the sample pages.
- The Middle East and Mexican energy positioning on the home page and the Spanish page.
- On the contact form, the copy-this-text fallback, the request-type selector, the extra proof
  question, and the location, phone and research expander fields.

Both sample pages lost their examples in that earlier cleanup, so each now carries a section headed
"Worked example" linking to the worked examples page, as item 11 requires.

## Where the brief and the existing content contradicted each other

1. **The probability.** Covered above. Three-way conflict, resolved by decision.
2. **The case study and worked example card 1 were the same engagement.** Settled. Card 1 is cut.
   The case study is the only place that story appears, and it has the chart. The worked examples
   page runs cards 2, 3 and 4 plus card 6, the capability build.
3. **Corroboration appears on the home page and on How it works.** The brief specifies home block 2
   and separately requires a corroboration section on How it works. Home states it in one line and
   How it works carries the mechanism and the mastheads argument.
4. **The loop and the five operations appear on How it works and on the Frame Bureau page.** Item 5
   says keep them on the Frame Bureau page. They are named there as the curriculum and explained
   only on How it works.
5. **Nigeria.** "Keep the coming-soon countries" against a brief list of four. Resolved by decision.
6. **Per-country reasons.** Item 6 says each reason comes from the brief; the brief gives one shared
   reason for all four. You supplied the four lines.
7. **The reference file path.** The items point to `docs/reference/frame_bureau_qlc.html`. The file
   is at `docs/frame_bureau_qlc.html`.
8. **The five module names** are not in the prose of the reference page. They are in a JavaScript
   array inside it, and in card 5 of `worked_examples.md`. Both agree, and that wording is used.

## Sentences I was unsure of

**English.**

1. How it works, step 4: "The readings move separately rather than collapsing into one number, so
   pressure from outside stays visible next to the cohesion of the people in power." The reference
   made this point with client figures. This keeps the point and drops the numbers, but it is my
   sentence rather than yours.
2. Case study: "A minority probability on a major political rupture within thirty days." This is the
   agreed replacement for forty per cent. Check that "minority probability" is how you want the call
   described.
3. Withdrawn. The sentence was in worked example card 1, which is cut.
4. Engagement, scoping conversation: "Most engagements start here, and some stop here, because the
   honest answer is sometimes that the record cannot carry the question." Settled. Kept.
5. About: the first-person paragraph is attributed to "Robert Shaw, founder". First person needs a
   speaker. Remove the attribution if you would rather it read unsigned.
6. The two testimonials keep the American spellings "modeling" and "rigor". They are quoted and item
   7 says to keep them exactly, so British spelling was not applied to them.
7. "Judgement" is used throughout, including in "structured judgement". Settled. British spelling
   is the rule and it is not a fixed term. American spelling survives only where a document is
   quoted verbatim, which on this site means the two testimonials.

**Spanish.** The mirror is one page. These are the sentences where I am least sure of the register.

8. "Inteligencia continua. Desde lugares que solo producen instantáneas." The headline. "Instantánea"
   for snapshot is literal and reads well to me, but a native reader should confirm it does not
   sound photographic.
9. "Un registro fechado y documentado de lo que ocurre." "Documentado" is doing the work of
   "sourced", for which there is no clean single word.
10. "Los medios de comunicación cuentan como una sola clase, por muchos que publiquen la misma
    noticia." The subjunctive "por muchos que" is correct but formal.
11. "Un acuerdo con corresponsales en preparación." For "a correspondent agreement in progress".
12. Settled. "Mesa" was wrong for an intelligence desk. The navigation now reads
    "Formar a una institución para que lleve su propia unidad de análisis."
13. The navigation panels say "(en inglés)" because the Spanish labels link to English pages. The
    alternative was leaving the navigation in English, which item 12 forbids.

## Checks

- `python scripts/build.py` builds 32 pages, 31 published plus the legacy redirect.
- `python scripts/check_site.py` passes. See below.
- `python scripts/test_contact.py` passes, 17 tests.
- No page contains a placeholder or an editor's marker.
- The two empty divs the items require are present and empty: `loop-diagram` on How it works and
  `venezuela-series` on the case study.
- Every content page carries exactly one enquiry invitation, no two pages use the same wording, and
  sources, privacy and editorial standards carry none.
- No em dash, no colon joining two clauses, and no sentence beginning with "Also" anywhere.
- The retired vocabulary does not appear as a selling point on any page in either language.

### Link checker

```
Passed: 31 HTML pages, local assets, fragment links, unique IDs, article count,
and publication exclusions.
```

## Not done, and why

- **The loop diagram and the four-line chart.** Placeholder divs only, as instructed.
- **The reworded "How the machine moves the odds" graphic** in Part 3 of the brief. Not in the
  numbered items, and it needs the live questions and their current probabilities, which are not in
  the source documents.
- **A full Spanish mirror of the site.** The mirror is one page. Item 12 says translate every
  changed page; the only Spanish page is the home page.
- **Capability build as a sales line.** `positioning.md` describes it. No item places it on a page,
  and worked example card 6 covers the same ground, so it has no page of its own.
