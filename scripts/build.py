"""Build EchoFrame's dependency-free public website from structured editorial content."""
import html
import datetime
import json
import math
import re
import shutil
from pathlib import Path
from programme import programme_teaser, venezuela_page, evidence_methodology, question_preview
from audiences import perspectives, consequence_section, audience_page
from experience import hero as research_hero, formats, faq
from depth import PAGES, write_downloads
from samples import SAMPLES, sample_library, sample_page, write_sample_downloads
from site_navigation import navigation, home_directory
from visuals import video_section
from homepage import claims
from intelligence import six_layers, evidence_flow, hard_questions
from contact import contact_page
from testimonials import testimonials
from map_data import build_map_data
from map_page import map_page

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT  # Source pages are checked in; Render serves the same generated files.
ARTICLES = [a for a in json.loads((ROOT / 'content/articles.json').read_text(encoding='utf-8')) if a.get('status') == 'published']
ARTICLE_BY_SLUG = {a['slug']: a for a in ARTICLES}
SITE = json.loads((ROOT / 'content/site.json').read_text(encoding='utf-8'))
E = html.escape
ARROW = ''
GENERATED = []
MARK = '<svg class="echoframe-mark" viewBox="0 0 48 48" fill="none" aria-hidden="true"><g stroke-width="3.8" stroke-linecap="round"><path d="M7 7L29 41M13 7L35 41M19 7L41 41" stroke="#ed704b"/><path d="M41 7L19 41M35 7L13 41M29 7L7 41" stroke="currentColor"/></g></svg>'


def validate():
    seen = set()
    for a in ARTICLES:
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', a['slug']), 'Invalid slug'
        assert a['slug'] not in seen, 'Duplicate slug'
        seen.add(a['slug'])
        for key in ('title', 'dek', 'category', 'format', 'art', 'date', 'author', 'takeaway', 'sections', 'watch'):
            assert a.get(key), f'Missing {key}: {a["slug"]}'
        for s in a['sources']:
            assert s['url'].startswith('https://'), 'Sources must use HTTPS'
        datetime.date.fromisoformat(a['date'])
        assert a['art'] in ('signals','maritime','policy','network','scenario'), 'Unsupported artwork'
        for section in a['sections']:
            assert section['heading'] and section['paragraphs'] and all(section['paragraphs']), 'Incomplete section'


def brand(prefix=''):
    return f'<a class="brand" href="{prefix}index.html" aria-label="EchoFrame home">{MARK}<span>echo<span class="brand-light">frame</span><i>®</i></span></a>'


def card(a, prefix='', featured=False):
    return f'''<article class="research-card {'featured-card' if featured else ''}" data-slug="{a['slug']}" data-category="{E(a['category'])}" data-search="{E((a['title']+' '+a['dek']+' '+a['category']+' '+a['format']).lower())}">
    <a class="card-art art-{a['art']}" href="{prefix}research/{a['slug']}.html" aria-label="Read {E(a['title'])}"><span class="art-lines" aria-hidden="true"></span><span class="art-number" aria-hidden="true">EF / {ARTICLES.index(a)+1:02}</span><span class="art-label">{E(a['category'])}</span>{ARROW}</a>
    <div class="card-copy"><div class="eyebrow">{E(a['category'])}<span class="meta-dot">·</span>{E(a['format'])}</div><h3><a href="{prefix}research/{a['slug']}.html">{E(a['title'])}</a></h3><p>{E(a['dek'])}</p><div class="card-bottom"><span>{minutes(a)} min read</span><a href="{prefix}research/{a['slug']}.html" aria-label="Read {E(a['title'])}">Read the analysis {ARROW}</a></div></div></article>'''


def minutes(a):
    words = sum(len(p.split()) for s in a['sections'] for p in s['paragraphs'])
    return max(2, round(words / 180))


def layout(title, body, page='home', prefix='', description='', lang='en'):
    # Apply the heading punctuation convention to generated pages, not prose.
    def clean_heading(match):
        parts = re.split(r'(<[^>]+>)', match.group(2))
        text = ''.join(part if part.startswith('<') else re.sub(r'\.(?=\s|$|[”’\"])', '', part) for part in parts)
        return match.group(1) + text + match.group(3)
    body = re.sub(r'(<h[1-4]\b[^>]*>)(.*?)(</h[1-4]>)', clean_heading, body, flags=re.DOTALL)
    links = navigation(prefix)
    return f'''<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#f7f6f2">
<title>{E(title)} | EchoFrame</title><meta name="description" content="{E(description or 'Political intelligence for oil and gas government affairs teams and distressed-debt investors. Explore asset-level questions, policy context, and the Venezuela programme.')}">
<meta property="og:title" content="{E(title)} | EchoFrame"><meta property="og:description" content="{E(description or 'A clearer view of a complex world. Explore EchoFrame research, coverage, and methodology.')}"><meta property="og:type" content="{'article' if page=='article' else 'website'}"><meta property="og:image" content="{prefix}assets/social-card.png">
<link rel="icon" href="{prefix}favicon.png"><link rel="stylesheet" href="{prefix}assets/site.css"><link rel="stylesheet" href="{prefix}assets/presence.css"><link rel="stylesheet" href="{prefix}assets/depth.css"><link rel="stylesheet" href="{prefix}assets/refinements.css"><link rel="stylesheet" href="{prefix}assets/bureau.css"><script defer src="{prefix}assets/site.js"></script></head>
<body class="page-{page}"><a class="skip-link" href="#main">Skip to content</a><div class="topline"><div class="container"><span>✳ &nbsp; A closer view of Venezuela. Our lead research programme is taking shape.</span><a href="{prefix}venezuela.html">Explore the programme </a></div></div>
<header class="site-header"><div class="container nav-shell">{brand(prefix)}<button class="menu-toggle" aria-expanded="false" aria-controls="main-nav">Menu <span aria-hidden="true">☰</span></button><nav id="main-nav" aria-label="Main navigation">{links}<a class="nav-contact" href="{prefix}briefing.html">Request a demo {ARROW}</a></nav></div></header>
<main id="main">{body}</main>
<footer class="site-footer"><div class="container"><div class="footer-top"><div>{brand(prefix)}<p>A clearer view of a complex world.</p><span class="eyebrow">Evidence. Context. Judgment.</span></div><div><h2>Explore</h2><a href="{prefix}capabilities.html">Research capabilities</a><a href="{prefix}government-affairs.html">Government affairs</a><a href="{prefix}distressed-debt.html">Distressed debt</a><a href="{prefix}venezuela.html">Venezuela programme</a><a href="{prefix}research.html">Intelligence library</a><a href="{prefix}coverage.html">Regional coverage</a><a href="{prefix}methodology.html">Our approach</a></div><div><h2>Connect</h2><a href="{prefix}briefing.html?kind=contact">Contact us</a><a href="{prefix}engagement.html">Working with EchoFrame</a><a href="mailto:contact@echoframe.co">contact@echoframe.co</a><a href="https://ie.linkedin.com/company/echoframing" target="_blank" rel="noopener noreferrer">LinkedIn </a></div><div><h2>Company</h2><a href="{prefix}about.html">About EchoFrame</a><a href="{prefix}trust.html">Trust &amp; privacy</a><a href="{prefix}sample-briefs.html">Sample briefs &amp; templates</a><a href="{prefix}sources.html">Primary-source directory</a><a href="{prefix}editorial-standards.html">Editorial standards</a><a href="{prefix}{'index.html' if lang=='es' else 'es/index.html'}" lang="{'en' if lang=='es' else 'es'}">{'English' if lang=='es' else 'En español'}</a></div></div><div class="footer-bottom"><span>© 2026 {E(SITE['legal_name'])}{' · '+E(SITE['registration_line']) if SITE['registration_line'] else ''}</span><span><a href="{prefix}privacy.html">Privacy</a><span class="meta-dot">/</span>Intelligence with perspective.</span><a href="#main">Back to top </a></div></div></footer></body></html>'''


def cta(prefix=''):
    return f'''<section class="briefing-banner"><div class="container"><div><div class="eyebrow">Put intelligence in context</div><h2>What would better evidence<br>change for you?</h2><p>Tell us your sector, the decision you face, and what a useful first briefing would need to demonstrate.</p></div><a class="button button-light" href="{prefix}briefing.html">See how we can help you {ARROW}</a></div></section>'''


def home():
    return research_hero()+claims()


REGIONS = [
    {'id':'europe','name':'Europe','subtitle':'Understand policy as it takes shape.','description':'Follow energy policy through institutions, negotiations, and implementation. Connect the documentary record to the technologies, projects, and markets within your research scope.','tags':['Energy policy','Regulatory process','Institutional influence'],'image':'eu-regulatory-map.png','platform':'EU Energy Tracker','url':'https://eu-regulatory-monitor.onrender.com/','article':'following-european-energy-policy'},
    {'id':'latin-america','name':'Venezuela','subtitle':'Venezuela, at the level of the asset.','description':'Our lead development programme connects local events, conflicting accounts, and documented viability to specific asset-level questions. Explore the proposed workflow and collection priorities for Venezuela.','tags':['Venezuela programme','Asset-level questions','In development'],'image':'venezuela-predictive.png','platform':'Venezuela research platform','url':'https://vz.echoframe.co','article':'venezuela-from-country-to-asset'},
]
REGIONS = [REGIONS[1], REGIONS[0]]
COMING_REGIONS = ['Colombia', 'Mexico', 'Nigeria', 'Rwanda', 'Pakistan']


def coming_coverage():
    countries = ''.join(f'<li><h3>{E(country)}</h3><span>Coming soon</span></li>' for country in COMING_REGIONS)
    return f'<section class="coverage-coming" aria-labelledby="coming-coverage-title"><div class="eyebrow">On the horizon</div><h2 id="coming-coverage-title">Next in our frame.</h2><p>Our regional coverage is expanding. These five countries are coming soon.</p><ul class="coming-countries">{countries}</ul></section>'


def coverage_widget():
    buttons = ''.join(f'<button role="tab" id="tab-{r["id"]}" aria-controls="panel-{r["id"]}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}">{r["name"]} <span>0{i+1}</span></button>' for i,r in enumerate(REGIONS))
    panels = ''
    for i,r in enumerate(REGIONS):
        panels += f'''<div class="coverage-panel" role="tabpanel" id="panel-{r['id']}" aria-labelledby="tab-{r['id']}" {'' if i==0 else 'hidden'}><div class="coverage-copy"><div class="eyebrow">Regional focus / 0{i+1}</div><h3>{r['subtitle']}</h3><p>{r['description']}</p><div class="tags">{''.join(f'<span>{t}</span>' for t in r['tags'])}</div><a class="text-link" href="coverage.html#{r['id']}">Explore {r['name']} {ARROW}</a></div><div class="platform-preview"><div class="preview-bar"><span><i></i><i></i><i></i></span><span>PLATFORM PREVIEW</span></div><img src="images/{r['image']}" alt="Existing {r['platform']} interface screenshot; historical preview, not live data" loading="lazy" width="900" height="550"><span class="preview-label">{r['platform']} <span>ARCHIVE SCREENSHOT</span></span></div></div>'''
    # Replace the legacy Venezuela scoring screenshot with an explicitly
    # illustrative brief; it must not imply validated forecast performance.
    start = panels.index('<div class="platform-preview">', panels.index('id="panel-latin-america"'))
    end = panels.index('</div></div>', start) + len('</div>')
    panels = panels[:start] + question_preview() + panels[end:]
    return f'<div class="coverage-tabs" role="tablist" aria-label="Explore coverage regions">{buttons}</div>{panels}'+coming_coverage()


def intro(kicker, title, description):
    return f'<section class="page-intro container"><div class="eyebrow">{kicker}</div><h1>{title}</h1><p>{description}</p></section>'


def library():
    return intro('The intelligence library','A wider frame.<br><em>A clearer perspective.</em>','Asset-level questions, evidence guides, and regional context. Explore the Venezuela programme alongside the wider research collection.')+'''<section class="container library-section"><div class="library-controls"><div class="filter-buttons" role="group" aria-label="Filter intelligence by region or subject">'''+''.join(f'<button class="filter-button" data-filter="{c}" aria-pressed="{str(i==0).lower()}">{c}</button>' for i,c in enumerate(['All intelligence','Venezuela','Europe','Latin America','Methods']))+'''</div><label class="search-box"><span aria-hidden="true">⌕</span><input type="search" id="research-search" placeholder="Search the library" aria-label="Search intelligence"></label></div><div class="library-meta"><span id="result-count" role="status" aria-live="polite">'''+str(len(ARTICLES))+''' perspectives</span><label class="saved-filter"><input id="saved-only" type="checkbox"> Saved on this device</label><span>RESEARCH & PROGRAMME NOTES / SEPTEMBER 2026</span></div><div class="card-grid library-grid">'''+''.join(card(a) for a in ARTICLES)+'''</div><div id="no-results" class="empty-state" hidden><h2>A different angle?</h2><p>No articles match this search. Try another topic or reset the filters.</p><button class="button" id="reset-search">Show all intelligence </button></div><p class="collection-note">This library contains evergreen research guides and programme-design notes. Venezuela collection priorities and sample briefs describe work in development, not live coverage or current forecasts.</p></section>'''+cta()


def article_page(a):
    date_label = datetime.date.fromisoformat(a['date']).strftime('%d %B %Y').lstrip('0')
    toc = ''.join(f'<a href="#section-{i}"><span>0{i}</span>{E(s["heading"])}</a>' for i,s in enumerate(a['sections'],1))
    sections = ''.join(f'<section id="section-{i}"><h2>{E(s["heading"])}</h2>'+''.join(f'<p>{E(p)}</p>' for p in s['paragraphs'])+'</section>' for i,s in enumerate(a['sections'],1))
    sources = ''.join(f'<li><a href="{E(s["url"])}" target="_blank" rel="noopener noreferrer">{E(s["title"])} </a></li>' for s in a['sources'])
    related = [r for r in ARTICLES if r['slug']!=a['slug']][:3]
    return f'''<div class="reading-progress" aria-hidden="true"></div><article><header class="article-header container"><a class="back-link" href="../research.html"> Intelligence library</a><div class="eyebrow">{E(a['category'])} / {E(a['format'])}</div><h1>{E(a['title'])}</h1><p class="article-dek">{E(a['dek'])}</p><div class="article-byline"><span class="author-mark">{MARK}</span><span>{E(a['author'])}<small><time datetime="{a['date']}">{date_label}</time> · {minutes(a)} min read · {E(a.get('collection','Foundations collection'))}</small></span><div class="reader-actions"><button class="save-article" data-slug="{a['slug']}" aria-pressed="false">Save article +</button><button class="copy-link">Copy link </button><button class="print-article">Print </button></div></div><span class="reader-status" role="status" aria-live="polite"></span></header><div class="article-layout container"><aside class="article-toc"><div class="eyebrow">In this perspective</div>{toc}<a href="#source-notes"><span></span>Sources & notes</a></aside><div class="article-body"><div class="takeaway"><div class="eyebrow">The central idea</div><p>{E(a['takeaway'])}</p></div>{sections}<section class="watch-box"><div class="eyebrow">Questions to carry forward</div><h2>What to watch.</h2><ul>{''.join(f'<li>{E(w)}</li>' for w in a['watch'])}</ul></section><section id="source-notes" class="source-notes"><h2>Sources & editorial notes</h2><p>{E(a['sourceNote'])}</p>{'<ol>'+sources+'</ol>' if sources else ''}<p>Prepared {date_label}. Read our <a href="../editorial-standards.html">editorial standards</a>. To suggest a correction, <a href="mailto:contact@echoframe.co?subject=Editorial%20correction%3A%20{a['slug']}">contact the editorial desk</a>.</p></section></div></div></article><section class="section container"><div class="section-heading"><div><div class="eyebrow">Continue exploring</div><h2>Connect another perspective.</h2></div></div><div class="card-grid">{''.join(card(r,'../') for r in related)}</div></section>'''+cta('../')


def coverage():
    result = intro('Regional coverage','The world is connected.<br><em>The details are local.</em>','Explore our Venezuela programme and European energy policy research. Connect regional context with evidence you can inspect.')
    result += '<div class="container region-jump">'+''.join(f'<a href="#{r["id"]}">{r["name"]} </a>' for r in REGIONS)+'</div>'
    for i,r in enumerate(REGIONS):
        link = f'<a class="button" href="{r["url"]}" target="_blank" rel="noopener noreferrer">Open platform {ARROW}</a>'
        if r["id"] == "europe":
            link = "<p>The European energy policy tracker is available to clients on request.</p>"
        result += f'''<section id="{r['id']}" class="region-detail container"><div><div class="eyebrow">0{i+1} / {r['name']}</div><h2>{r['subtitle']}</h2><p>{r['description']}</p><div class="tags">{''.join(f'<span>{t}</span>' for t in r['tags'])}</div><h3>{r['platform']}</h3><div class="region-actions">{link}<a class="text-link" href="research/{r['article']}.html">Read a related guide </a></div><p class="fine-print">{'Platform access is managed by the platform. Contact us if you need an account.' if r['url'] else 'Contact the team to discuss current research scope and access.'}</p></div><figure class="coverage-figure"><img src="images/{r['image']}" alt="Historical {r['platform']} interface preview" loading="lazy"><figcaption>Archive platform screenshot · Illustrates the interface, not current conditions.</figcaption></figure></section>'''
    result = re.sub(r'<figure class="coverage-figure"><img src="images/eu-regulatory-map.png".*?</figure>', "", result)
    old_figure = '<figure class="coverage-figure"><img src="images/venezuela-predictive.png" alt="Historical Venezuela research platform interface preview" loading="lazy"><figcaption>Archive platform screenshot · Illustrates the interface, not current conditions.</figcaption></figure>'
    result = result.replace(old_figure, question_preview())
    return result+'<div class="container">'+coming_coverage()+'</div>'+cta()


def methodology():
    legacy = evidence_methodology(intro, cta)
    # Retain the working evidence-state explorer; replace the dated status tour.
    start = legacy.index('<section class="scenario-section">')
    end = legacy.index('<section class="section container">', start)
    evidence_demo = legacy[start:end]
    return intro('Our method / Evidence to judgment', 'Political science,<br><em>run as data science</em>', 'Six analytical layers connect reporting to events, actors, incentives, and possible outcomes. The reasoning should be visible enough to challenge, and clear enough to use in a decision.')+six_layers()+evidence_flow()+evidence_demo+hard_questions()+cta()


def frame_bureau_summary():
    return '<section class="section container" id="frame-bureau"><h2>The Frame Bureau</h2><p>The Frame Bureau is EchoFrame’s training division. It brings investigative journalism, data science and political risk analysis into practical work on research questions. Participants check sources, distinguish evidence from assumptions, write assessments and review them when the evidence changes.</p><p>Training is available on request through <a href="mailto:contact@echoframe.co">contact@echoframe.co</a>.</p></section>'


def about():
    return intro('About EchoFrame','Independent thinking.<br><em>Connected intelligence.</em>','EchoFrame develops political risk research around specific assets, contracts, and local actors. Our Venezuela programme is being shaped around the decisions operators, entrants, creditors, and suppliers need to make.')+'''<section class="about-story container"><div class="about-visual"><span class="eyebrow">THE WIDER FRAME</span>'''+MARK+'''<span>Evidence  Context  Perspective</span></div><div><div class="eyebrow">Why we exist</div><h2>The event is only part of the story.</h2><p>The value of an observation depends on its context: the actors involved, the incentives at work, the history behind it, and the plausible paths ahead.</p><p>Our Venezuela programme brings that question into focus: how can national context, local reporting, official records, and physical observations inform a decision about a particular asset? The connected event and forecasting workflow remains in development. Our regional focus is Venezuela and European energy policy.</p><a class="text-link" href="methodology.html">Explore the approach </a></div></section><section class="section container"><div class="section-heading"><div><div class="eyebrow">Designed around the question</div><h2>Different decisions. Shared context.</h2></div></div><div class="standards-grid"><div><span class="eyebrow">01 / Energy</span><h3>Understand your operating environment.</h3><p>Frame questions around institutions, infrastructure, and the policy processes relevant to your regional footprint.</p></div><div><span class="eyebrow">02 / Commodities</span><h3>Follow the chain of implications.</h3><p>Connect geopolitical developments to research on maritime routes, energy systems, and operational constraints.</p></div><div><span class="eyebrow">03 / Research & strategy</span><h3>Make the reasoning visible.</h3><p>Explore actor networks, competing scenarios, and the source record behind an analytical judgment.</p></div></div></section>'''+frame_bureau_summary()+video_section()+testimonials()+faq()+cta()


def briefing():
    return contact_page()

def standards():
    return intro('Editorial standards','Show the work.<br><em>Keep the context.</em>','Our public editorial standard: a reader should be able to identify the evidence, understand the interpretation, and see where uncertainty remains.')+'''<div class="prose-page container"><section><h2>Different formats, clearly labeled</h2><p>Research essays develop an argument. Field guides explain a research process. Methods notebooks examine an analytical technique. The foundations collection is evergreen educational material. Programme notes explain work in development. Neither format should be mistaken for current alerts, verified field coverage, or a forecast track record.</p></section><section><h2>Evidence and attribution</h2><p>Factual claims should link to the primary material that supports them. Sources should be recorded with publication and access dates where relevant. Multiple reports derived from one source should not be represented as independent confirmation.</p><p>Original editorial frameworks are labeled as such. Illustrative examples and archived interface screenshots are identified where they appear. They do not represent live monitoring.</p></section><section><h2>Rights, precision, and source protection</h2><p>The intended Venezuela workflow requires review of permitted source use before client publication. A publicly accessible source is not a blanket permission to reproduce its text. Public outputs should use approved summaries and references.</p><p>Source-protecting material must not expose identities, identifying narrative, or unsafe geographic detail. A state-level observation should not appear as a precise facility pin. These are design and editorial requirements; this public website is not a field-report intake or protection system.</p></section><section><h2>Assessment and uncertainty</h2><p>An analytical judgment should make its assumptions visible, consider credible alternatives, and state what could change the assessment. Confidence in evidence is distinct from the estimated likelihood of an outcome. Numerical forecasts require an explained basis and review horizon.</p></section><section><h2>Technology and editorial responsibility</h2><p>Automated tools can assist with organization, transcription, comparison, and drafting. A proposed finding still needs source verification and an accountable editorial review. Generated imagery must not be presented as documentary evidence, and synthetic examples must be labeled.</p></section><section><h2>Corrections and review</h2><p>Material corrections should identify what changed and why. Publication and substantive revision dates should remain visible. Send a correction request with the article link, disputed claim, and supporting evidence to <a href="mailto:contact@echoframe.co?subject=Editorial%20correction">contact@echoframe.co</a>.</p></section><section><h2>Commercial claims</h2><p>Case studies, client outcomes, and testimonials require a supporting record and permission for publication. This website does not claim independently audited forecast accuracy or guaranteed commercial outcomes.</p></section></div>'''


def privacy():
    return intro('Privacy','Your information.<br><em>A clear account of how it is used.</em>','What happens when you read this website, save an article, or send EchoFrame a request.')+'''<div class="prose-page container"><section><h2>When you send a request</h2><p>The contact form sends the details you enter to the website’s contact service, which forwards them to EchoFrame through its configured email provider. These details include your name, work email, organisation, role, location, message, and any optional phone or research information you supply.</p><p>We use this information to respond to your demo or contact request. The form does not subscribe you to marketing. Please do not send confidential documents or information that identifies a protected source.</p><p>If the email connection is unavailable, the form tells you that delivery has not been confirmed. Your details remain in the page so you can use the direct email link. They are not saved in your browser when you leave.</p></section><section><h2>Delivery records and abuse prevention</h2><p>The website keeps short-lived technical records to limit repeated requests and prevent duplicate email. These contain a random request reference, a keyed digest of the request, its delivery state, and a timestamp—not the text of your message. Request records expire after 24 hours; rate-limit records expire after an hour. Expired records are cleared when new requests are processed.</p><p>A keyed digest of the connection address is used for rate limiting. Hosting and email providers may also process normal service logs and message records. Messages delivered to EchoFrame are held in its email service so the team can respond. Contact us to discuss deletion or retention of correspondence you have sent.</p></section><section><h2>Reading and saved articles</h2><p>Saved article identifiers stay in local storage in this browser. They do not create an account or send your reading list to EchoFrame. Use the save control again to remove an article, or clear the site data on your device.</p><p>This build contains no advertising trackers, analytics scripts, or newsletter database. The presentation video is served from the website without an embedded third-party video player.</p></section><section><h2>External services</h2><p>Google Fonts serves the website’s typography. Your browser connects to Google to retrieve it. The host may process ordinary request information to deliver pages and media.</p><p>Calendar booking opens Cal.com. Regional platform and social links open separate websites with their own data-handling and account arrangements. The fallback email link opens your chosen email application.</p></section><section><h2>Contact</h2><p>For privacy questions or requests about information you have provided, email <a href="mailto:contact@echoframe.co?subject=Privacy%20request">contact@echoframe.co</a>. This website is operated by EchoFrame Intelligence AB, registered in 2026.</p><p>Last updated: 11 September 2026.</p></section></div>'''


def spanish():
    return intro('Inteligencia geopolítica','Entienda las señales.<br><em>Amplíe la perspectiva.</em>','Investigación de fuentes abiertas, contexto regional y análisis estructurado para comprender un mundo conectado.')+'''<section class="prose-page container"><h2>Del acontecimiento al contexto.</h2><p>EchoFrame trabaja para equipos de asuntos gubernamentales del sector del petróleo y el gas e inversores en deuda en dificultades y situaciones especiales.</p><p>Venezuela es nuestro programa principal. Nuestra segunda área es la política energética europea. El programa de Venezuela se está desarrollando en torno a activos concretos, hechos locales, fuentes que discrepan y preguntas con una fecha y una regla de resolución. La integración de eventos y pronósticos sigue en desarrollo.</p><p><a href="../venezuela.html">Conozca el programa de Venezuela (en inglés) </a></p><h2>Explore nuestra investigación.</h2><p>La biblioteca en inglés incluye ensayos, guías regionales y cuadernos de metodología. La colección inicial explica cómo evaluar fuentes, interpretar señales y formular preguntas de investigación. No presenta pronósticos de mercado en tiempo real.</p><div class="hero-actions"><a class="button" href="../research.html">Explorar la biblioteca en inglés </a><a class="text-link" href="../coverage.html">Ver cobertura </a></div><h2>Conversemos sobre sus prioridades.</h2><p>Escríbanos con la región y las preguntas que le interesan. Podemos comentar el alcance de la investigación y las opciones de acceso.</p><a class="button" href="mailto:contact@echoframe.co?subject=Consulta%20sobre%20EchoFrame">Contactar con EchoFrame </a></section>'''


def globe():
    """Project bundled Natural Earth land polygons; no runtime map dependency."""
    data=json.loads((ROOT/'assets/land-110m.json').read_text())
    scale,translate=data['transform']['scale'],data['transform']['translate']
    arcs=[]
    for arc in data['arcs']:
        x=y=0; points=[]
        for dx,dy in arc:
            x+=dx; y+=dy; points.append((x*scale[0]+translate[0],y*scale[1]+translate[1]))
        arcs.append(points)
    def project(lon,lat):
        lon=math.radians(lon-5); lat=math.radians(lat); center=math.radians(12)
        depth=math.sin(center)*math.sin(lat)+math.cos(center)*math.cos(lat)*math.cos(lon)
        x=math.cos(lat)*math.sin(lon); y=math.cos(center)*math.sin(lat)-math.sin(center)*math.cos(lat)*math.cos(lon)
        if depth<0:
            length=math.hypot(x,y); x/=length; y/=length
        return 325+268*x,325-268*y,depth
    paths=[]
    for polygon in data['objects']['land']['geometries'][0]['arcs']:
        for ring in polygon:
            points=[]
            for index in ring:
                points.extend(arcs[index] if index>=0 else reversed(arcs[~index]))
            projected=[project(*p) for p in points]
            if not any(p[2]>0 for p in projected): continue
            paths.append('M'+'L'.join(f'{x:.1f},{y:.1f}' for x,y,_ in projected)+'Z')
    graticule=[]
    for axis in ('lat','lon'):
        for fixed in range(-75,180 if axis=='lon' else 90,15):
            line=''; started=False
            for varying in range(-180 if axis=='lat' else -90,181 if axis=='lat' else 91,2):
                x,y,z=project(varying,fixed) if axis=='lat' else project(fixed,varying)
                if z>=0: line+=('L' if started else 'M')+f'{x:.1f},{y:.1f}'; started=True
                else: started=False
            graticule.append(f'<path d="{line}"/>')
    markers=''
    coords=[(-66,10),(12,50)]
    for lon,lat in coords:
        x,y,_=project(lon,lat)
        markers+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="#ed704b" opacity=".13"/><circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#d36c49"/>'
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 650 650"><defs><radialGradient id="ocean" cx="35%" cy="30%" r="75%"><stop stop-color="#f7f6f2"/><stop offset="1" stop-color="#dfdbe8"/></radialGradient><pattern id="dots" width="5" height="5" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".7" fill="#78668c" opacity=".36"/></pattern><clipPath id="sphere"><circle cx="325" cy="325" r="268"/></clipPath></defs><g fill="none" stroke="#bcb2c9" stroke-width=".7"><circle cx="325" cy="325" r="290" stroke-dasharray="2 7"/><ellipse cx="325" cy="325" rx="322" ry="122" transform="rotate(-29 325 325)"/></g><circle cx="325" cy="325" r="268" fill="url(#ocean)" stroke="#b6abc5"/><g clip-path="url(#sphere)"><g fill="#c6bcd1" stroke="#a99ab9" stroke-width=".6">{''.join(f'<path d="{p}"/>' for p in paths)}</g><g fill="none" stroke="#a897ba" stroke-width=".5" opacity=".38">{''.join(graticule)}</g><circle cx="325" cy="325" r="268" fill="url(#dots)" opacity=".3"/><g fill="none" stroke="#795797" stroke-width="1.2" stroke-dasharray="4 5"><path d="M81 298Q246 106 347 128"/></g>{markers}</g></svg>'''
    (ROOT/'assets/globe.svg').write_text(svg,encoding='utf-8')


def write(path, title, body, page='home', prefix='', lang='en', description=''):
    dest=OUT/path; dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(layout(title,body,page,prefix,description,lang),encoding='utf-8')
    GENERATED.append(path)


def main():
    validate(); globe()
    downloads = write_downloads() + write_sample_downloads()
    map_files = build_map_data()
    for lang, path in [('en', 'map.html'), ('es', 'es/map.html')]:
        dest = OUT / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(map_page(layout, brand, lang), encoding='utf-8')
        GENERATED.append(path)
    for path, title, render, key in PAGES:
        write(path, title, render(), key)
    write('sample-briefs.html','Sample briefs & templates',sample_library(),'samples')
    for sample in SAMPLES:
        write(sample['slug']+'.html',sample['title'],sample_page(sample),'sample')
    write('index.html','A clearer view of a complex world',home())
    write('site.html','A clearer view of a complex world',home())
    write('government-affairs.html','Oil & gas government affairs',audience_page('government'),'government',description='Political intelligence for oil and gas government affairs teams. Scope research on stakeholders, policy milestones, and the evidence around operating assets.')
    write('distressed-debt.html','Distressed debt & special situations',audience_page('credit'),'credit',description='Political and asset-level research for distressed-debt investors. Frame thesis questions, inspect counterparty narratives, and identify evidence worth reviewing.')
    write('research.html','Intelligence library',library(),'research')
    write('coverage.html','Regional coverage',coverage(),'coverage')
    write('venezuela.html','Venezuela · Asset-level intelligence',venezuela_page(intro,cta),'venezuela')
    write('methodology.html','Our approach',methodology(),'methodology')
    write('about.html','About',about(),'about')
    write('briefing.html','Book a briefing',briefing(),'briefing')
    write('editorial-standards.html','Editorial standards',standards(),'standards')
    write('privacy.html','Privacy',privacy(),'privacy')
    write('es/index.html','Inteligencia geopolítica',spanish(),'home','../','es')
    for a in ARTICLES:
        write(f'research/{a["slug"]}.html',a['title'],article_page(a),'article','../',description=a['dek'])
    write('404.html','Page not found',intro('404 / Outside the frame','Let’s find<br><em>a better direction.</em>','The page you requested could not be found.')+'<div class="container section"><a class="button" href="index.html">Return to the homepage </a></div>')
    # Publish an explicit allowlist, excluding internal tools and source documents.
    public = ROOT / 'public'
    public.mkdir(exist_ok=True)
    publication_root = public.resolve()
    assert publication_root.parent == ROOT.resolve(), 'Publication directory must remain inside the workspace'
    # Render serves existing files before redirect rules. Keep the legacy alias
    # in the checkout, but let Render redirect /site.html to the canonical home.
    published_pages = [path for path in GENERATED if path != 'site.html']
    for obsolete in public.rglob('*.html'):
        if obsolete.relative_to(public).as_posix() not in published_pages:
            assert obsolete.resolve().is_relative_to(publication_root), 'Refusing to remove a page outside public/'
            obsolete.unlink()
    files = published_pages + ['favicon.png', 'assets/site.css', 'assets/presence.css', 'assets/depth.css', 'assets/refinements.css', 'assets/bureau.css', 'assets/site.js', 'assets/globe.svg', 'assets/energy-horizon.png', 'assets/social-card.svg', 'assets/social-card.png', 'assets/ATTRIBUTION.md']
    files += downloads + ['images/EchoFramev3.mp4']
    files += map_files + ['assets/map.css', 'assets/map.js']
    # Archive interface screenshots are not part of the publication output.
    for obsolete in public.rglob('*'):
        if obsolete.is_file() and obsolete.relative_to(public).as_posix() not in files:
            assert obsolete.resolve().is_relative_to(publication_root), 'Refusing to remove a file outside public/'
            obsolete.unlink()
    for path in files:
        source = ROOT / path
        if not source.exists():
            raise FileNotFoundError(f'Missing publication asset: {path}')
        target = public / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    print(f'Built {len(GENERATED)} pages; {len(published_pages)} published plus the legacy redirect. Includes {len(ARTICLES)} research articles. Deployment directory: public/')


if __name__=='__main__': main()
