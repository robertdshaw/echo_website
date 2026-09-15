# EchoFrame website

A static editorial website for geopolitical intelligence, with regional platform coverage and a structured content workflow. The pages are generated statically. A small Flask service serves the build and handles direct contact requests through Resend or authenticated SMTP.

## Preview

Requires Python 3.11 or later.

```powershell
python scripts/build.py
python -m pip install -r requirements.txt
python server.py
```

Open `http://127.0.0.1:4173`. The application redirects the legacy `/site.html` URL to `/` in both preview and deployment. The legacy file is excluded from the public build.

For an internal team URL, see [protected preview setup](docs/PROTECTED-PREVIEW.md). `python scripts/package_preview.py` creates a separate deployment ZIP with the current `public/` build, `preview_server.py`, and a Render configuration that generates a password. Nothing is deployed by the packaging command.

## Edit

- `scripts/build.py`: page templates, navigation, coverage configuration, and the locally generated globe.
- `scripts/programme.py`: Venezuela programme page, fictional evidence brief, and development-aware methodology.
- `scripts/audiences.py`: government affairs and distressed-debt journeys, and illustrative research interactions.
- `scripts/experience.py`: homepage opening, research-question preview, reusable briefing formats, and FAQs.
- `scripts/depth.py`: capability walkthroughs, source directory, trust, engagement formats, and public templates.
- `scripts/samples.py` and `content/samples.json`: complete fictional briefs, generated as HTML and downloadable Markdown.
- `scripts/site_navigation.py`: grouped navigation and a reusable site directory.
- `scripts/testimonials.py`: two attributed expert quotations, with contributor relationships identified.
- `scripts/bureau.py` and `assets/bureau.css`: The Frame Bureau's selective public training overview, linked to a training enquiry preset.
- `content/resources.json`: six primary-source references with use notes, limitations, and review dates.
- `assets/depth.css`: detailed product pages, diagrams, tables, sample documents, and expanded forms.
- `assets/refinements.css`: full logo presentation, scroll effects, claim-led layout, video, and direct contact form.
- `scripts/homepage.py`: three claim-led sections linking to substantive explanations.
- `scripts/intelligence.py`: six analytical layers, five risk dimensions, five scenarios, six decision tests, and an anonymised historical assessment summary.
- `scripts/visuals.py`: the EchoFrame film, presented on About. Historical chart functions remain in source but are no longer published.
- `server.py`: static delivery, contact validation, abuse limits, duplicate prevention, and email transport.
- `docs/CONTACT-DELIVERY.md`: local and deployed email setup, actual limitations, and verification.
- `assets/site.css`: responsive design, typography, illustrations, and print styles.
- `assets/presence.css`: EchoFrame violet and coral palette with reference-inspired spacing and layout; serif typography; responsive audience pages and interactive research previews.
- `assets/site.js`: library search/filtering, keyboard-accessible coverage tabs, evidence-state demonstration, browser-local saved articles, and direct contact submission with an email-link fallback.
- `content/articles.json`: structured articles. Only records with `status: published` are published.
- `docs/CONTENT-PLAYBOOK.md`: formats, workflow, eight-week calendar, source practices, and reusable production prompts.
- `docs/VENEZUELA-CONTENT-STRATEGY.md`: public positioning, plan-to-copy mapping, claim limits, and source-protection requirements.
- `docs/AUDIENCE-CONTENT-PLAN.md`: positioning and commissioning formats for oil and gas government affairs teams and distressed-debt investors.
- `docs/FULL-SITE-CONTENT-MAP.md`: the 33-page architecture, content states, and production workflows for the next layer of research.
- `content/site.json`: public company identification: EchoFrame Intelligence AB, registered in 2026, as confirmed by the owner.

Generated HTML is checked in so the repository can also be previewed directly. Regenerate it after editing source templates or content; do not edit generated pages as the source of truth.

## Add content

```powershell
python scripts/new_article.py your-article-slug --title "Your article title" --category "Methods"
```

This adds an unpublished draft to `content/articles.json`. Fill in all fields, check sources, and change `status` to `published` when it is ready. Run the build and inspect the article. Each section uses a heading and a list of plain-text paragraphs; sources use `title` and an HTTPS `url`. All article strings are escaped before HTML rendering.

Supported illustrations: `signals`, `maritime`, `policy`, `network`, `scenario`. The current categories are Methods, Venezuela, Europe, and Latin America. For a new category, update the library filter list and draft command choices together. The optional article `collection` field identifies programme notes separately from the foundations collection.

## Deployment

`render.yaml` installs the Python dependencies, builds the pages, and serves `public/` through Gunicorn and Flask. That directory is an explicit publication allowlist: generated pages, the site assets, favicon, the displayed European platform image, the original presentation video, and five public research downloads. The Venezuela preview is now a code-native fictional question brief. Internal administration pages, source documents, draft content, and archive videos are excluded. No deployment is triggered by the build script itself.

The build removes files outside the current allowlist from the dedicated generated publication directory, after validating its workspace location. Removing an article from publication removes its served page on the next build. Do not store hand-authored material in `public/`; it is generated output.

## Integrations and practical limits

- Briefing booking links to the existing `https://cal.eu/robertshaw` calendar.
- `government-affairs.html` and `distressed-debt.html` provide tailored journeys. Briefing URLs with `?audience=government` or `?audience=credit` preselect the corresponding perspective; users can change it.
- The form posts to `/api/contact`. Live delivery requires the mail configuration described in `docs/CONTACT-DELIVERY.md`. It never reports success unless the configured mail service accepts the request.
- Platform links go to their normal entry points. Access is controlled by the respective platforms; platform authentication was not tested or changed.
- The old homepage contained platform auto-login credentials. They have been removed from the rebuilt public code. Rotate those credentials in the platform services before publishing; they may still exist in prior deployments and Git history. This repository does not contain the platform backends needed to rotate them.
- No live intelligence feed, newsletter service, CMS account, or analytics service is connected. The foundations collection consists of evergreen guides and clearly labeled illustrative examples.
- The Venezuela page describes the supplied September 2026 plan. It does not implement collection, field-report intake, GIS, event grouping, a viability backend, inference, or forecast scoring. The sample terminal and its conflicting accounts are fictional. Proposed partners and private commercial terms are not published.
- Saved articles use this browser’s local storage. They are not synchronized between devices.
- Fonts load from Google Fonts with local system fallbacks. The map, diagrams, scripts, styles, and screenshots are local assets.
- The Spanish entry page has been rebuilt as a valid Spanish introduction. It links to the English research collection; full multilingual article publishing is not implemented.

## Verification

```powershell
python scripts/check_site.py
node --check assets/site.js
```

Optional browser verification, after starting the local server:

```powershell
python -m pip install playwright
python -m playwright install chromium
python scripts/preview_check.py
python scripts/depth_check.py
python scripts/test_contact.py
python scripts/refinement_check.py
```

Checks cover library filtering and deep links, empty results, independent audience/region tabs and keyboard behavior, consequence and evidence-state switching, article saving, print layout, audience-specific briefing presets, mobile navigation, image loading, page errors, reduced-motion behavior, and horizontal overflow from 320px mobile to desktop. Screenshots go to `.preview/`.

## Asset provenance

The coverage globe is generated from Natural Earth land geometry bundled by `world-atlas@2`, obtained from `https://cdn.jsdelivr.net/npm/world-atlas@2/land-110m.json`. Natural Earth geographic data is public domain; world-atlas packaging is ISC licensed. See `assets/ATTRIBUTION.md`.

The logo treatment follows the existing EchoFrame mark. Platform screenshots and favicon come from the original repository. Other editorial artwork is implemented directly in SVG/CSS and is illustrative.
