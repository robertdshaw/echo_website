from pathlib import Path
from bs4 import BeautifulSoup
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT).decode('utf-8')

documents = {p.relative_to(PUBLIC).as_posix(): BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser') for p in PUBLIC.rglob('*.html')}
assert len(documents) == 28
text = '\n'.join(s.get_text(' ', strip=True) for s in documents.values())
for forbidden in [r'\bTerminal A\b', r'\bIssuer B\b', r'prospect theory', r'regime consolidation', r'elite fracture', r'negotiated transition', r'security-force rupture', r'external escalation', r'\d+ min read']:
    assert not re.search(forbidden, text, re.I), forbidden
for p in PUBLIC.rglob('*'):
    if p.is_file() and p.suffix in {'.html', '.js', '.md', '.svg'}:
        assert '\u2014' not in p.read_text(encoding='utf-8'), p

assert (ROOT/'scripts/testimonials.py').read_text(encoding='utf-8') == git('show', '3396756:scripts/testimonials.py')
old_about = BeautifulSoup(git('show', '3396756:about.html'), 'html.parser')
assert [q.get_text() for q in old_about.select('blockquote')] == [q.get_text() for q in documents['about.html'].select('blockquote')]
dimensions = [h.get_text(strip=True) for h in documents['capabilities.html'].select('#risk-dimensions h3')]
assert dimensions == ['Elite Cohesion', 'Political Order', 'Security and Military', 'Economic and Fiscal Stability', 'Geopolitical and External Pressure', 'Social'], dimensions
assert documents['capabilities.html'].select_one('#tracked-questions').get_text(strip=True) == 'The scenario layer has been replaced by dated questions with tracked probabilities.'
for country in ['Colombia', 'Mexico', 'Nigeria', 'Rwanda', 'Pakistan']:
    assert country in documents['coverage.html'].get_text()
assert 'available to clients on request' in documents['coverage.html'].get_text()
assert documents['coverage.html'].select_one('a[href="research/following-european-energy-policy.html"]')
for name in ('index.html', 'es/index.html'):
    assert not re.search(r'Middle East|Mexican energy|Oriente Medio|energético de México', documents[name].get_text())

invitations = []
for name, soup in documents.items():
    contact_links = [a for a in soup.select('a[href]') if 'briefing.html' in a['href']]
    assert len(contact_links) <= 1, name
    if name in {'sources.html', 'privacy.html', 'editorial-standards.html'}:
        assert not contact_links and not soup.select('main a.button'), name
    invitations.extend(a.get_text(strip=True) for a in contact_links)
assert len(invitations) == len(set(invitations))
form = documents['briefing.html'].select_one('#briefing-form')
assert len(form.select('input:not([name=website]), select, textarea')) == 8
assert len(form.select('button')) == 1
assert not form.select('details, #email-draft, #contact-fallback')
articles = json.loads((ROOT/'content/articles.json').read_text(encoding='utf-8'))
assert len(articles) == 4
for article in articles:
    assert article['author'] == 'Robert Shaw'
    assert '[[ROB: confirm dates]]' in documents['research/'+article['slug']+'.html'].get_text()
    baseline = BeautifulSoup(git('show', '3396756:research/'+article['slug']+'.html'), 'html.parser')
    assert baseline.h1.get_text() == documents['research/'+article['slug']+'.html'].h1.get_text()
for a in documents['about.html'].select('footer a[href*="linkedin"]'):
    assert a['href'] in git('show', '3396756:about.html')

manifest = json.loads((ROOT/'_unpublished/map-archive-sha256.json').read_text(encoding='utf-8'))
for name, digest in manifest.items():
    assert hashlib.sha256((ROOT/'_unpublished'/name).read_bytes()).hexdigest() == digest, name

markers = []
for name in sorted(documents):
    for line, value in enumerate((ROOT/name).read_text(encoding='utf-8').splitlines(), 1):
        for marker in re.findall(r'\[\[ROB:.*?\]\]', value):
            markers.append((name, line, marker))

report = '''# September content revision review

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
'''
for name, line, marker in markers:
    report += f'| [{name}:{line}](../{name}#L{line}) | {marker} |\n'
report += '''
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
'''
report += f'- All {len(manifest)} map archive files match their pre-move SHA-256 hashes in `_unpublished/map-archive-sha256.json`.\n'
report += '''- External websites and production email delivery were not exercised. The live service still needs its configured SMTP or Resend credentials; the server reports unavailable or failed delivery honestly.
- `python scripts/export_content.py` refreshes the complete local review text in `EchoFrame-Website-Content.md`. It does not describe these changes as deployed.

## Files changed by the revision

The list below compares against the preserved baseline, excluding pre-existing unrelated `.gitignore` and `render.yaml` edits. The local work also leaves pre-existing untracked deployment notes, README, environment example and preview configuration untouched.

'''
changed = set(git('diff', '--name-only', '3396756').splitlines()) - {'.gitignore', 'render.yaml'}
changed.update({'scripts/export_content.py', '_unpublished/EchoFrame-Website-Content-before-revision.md'})
for name in sorted(changed):
    report += '- `' + name + '`\n'
(ROOT/'docs/CONTENT-FIX-REVIEW.md').write_text(report, encoding='utf-8')
print(json.dumps({'review_checks':'passed', 'public_pages':len(documents), 'map_files_unchanged':len(manifest), 'owner_marker_occurrences':len(markers), 'changed_paths':len(changed)}, indent=2))
