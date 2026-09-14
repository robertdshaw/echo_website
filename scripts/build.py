"""Build EchoFrame's dependency-free public website from structured editorial content."""
import html
import datetime
import json
import math
import re
import shutil
from pathlib import Path
from programme import venezuela_page
from audiences import perspectives, consequence_section, audience_page
from experience import hero as research_hero, formats, faq
from depth import PAGES, write_downloads
from samples import SAMPLES, sample_library, sample_page, write_sample_downloads
from site_navigation import navigation, home_directory
from chrome import CHROME
from spanish_page import page as spanish_page
from visuals import video_section
from homepage import claims
from how_it_works import page as how_it_works_page
from worked_examples import page as worked_examples_page
from frame_bureau import page as frame_bureau_page
from coverage_page import page as coverage_page
import services
import sectors
from contact import contact_page
from testimonials import testimonials
from page_presentation import enquiry_policy

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT  # Source pages are checked in; Render serves the same generated files.
SITE = json.loads((ROOT / 'content/site.json').read_text(encoding='utf-8'))
E = html.escape
ARROW = ''
GENERATED = []
MARK = '<svg class="echoframe-mark" viewBox="0 0 48 48" fill="none" aria-hidden="true"><g stroke-width="3.8" stroke-linecap="round"><path d="M7 7L29 41M13 7L35 41M19 7L41 41" stroke="#ed704b"/><path d="M41 7L19 41M35 7L13 41M29 7L7 41" stroke="currentColor"/></g></svg>'


def brand(prefix=''):
    return f'<a class="brand" href="{prefix}index.html" aria-label="EchoFrame home">{MARK}<span>echo<span class="brand-light">frame</span><i>®</i></span></a>'


def layout(title, body, page='home', prefix='', description='', lang='en'):
    # Apply the heading punctuation convention to generated pages, not prose.
    def clean_heading(match):
        parts = re.split(r'(<[^>]+>)', match.group(2))
        text = ''.join(part if part.startswith('<') else re.sub(r'\.(?=\s|$|[”’\"])', '', part) for part in parts)
        return match.group(1) + text + match.group(3)
    body = re.sub(r'(<h[1-4]\b[^>]*>)(.*?)(</h[1-4]>)', clean_heading, body, flags=re.DOTALL)
    C = CHROME[lang]
    links = navigation(prefix, lang)
    return f'''<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#f7f6f2">
<title>{E(title)} | EchoFrame</title><meta name="description" content="{E(description or C['description'])}">
<meta property="og:title" content="{E(title)} | EchoFrame"><meta property="og:description" content="{E(description or C['og_description'])}"><meta property="og:type" content="{'article' if page=='article' else 'website'}"><meta property="og:image" content="{prefix}assets/social-card.png">
<link rel="icon" href="{prefix}favicon.png"><link rel="stylesheet" href="{prefix}assets/site.css"><link rel="stylesheet" href="{prefix}assets/presence.css"><link rel="stylesheet" href="{prefix}assets/depth.css"><link rel="stylesheet" href="{prefix}assets/refinements.css"><link rel="stylesheet" href="{prefix}assets/bureau.css"><script defer src="{prefix}assets/site.js"></script></head>
<body class="page-{page}"><a class="skip-link" href="#main">{C['skip']}</a><div class="topline"><div class="container"><span>✳ &nbsp; {C['announce']}</span><a href="{prefix}venezuela.html">{C['announce_link']} </a></div></div>
<header class="site-header"><div class="container nav-shell">{brand(prefix)}<button class="menu-toggle" aria-expanded="false" aria-controls="main-nav">{C['menu']} <span aria-hidden="true">☰</span></button><nav id="main-nav" aria-label="{C['nav_label']}">{links}</nav></div></header>
<main id="main">{body}</main>
<footer class="site-footer"><div class="container"><div class="footer-top"><div>{brand(prefix)}</div><div><h2>{C['connect']}</h2><a href="{prefix}engagement.html">{C['f_engagement']}</a><span>contact@echoframe.co</span><a href="https://ie.linkedin.com/company/echoframing" target="_blank" rel="noopener noreferrer">LinkedIn </a></div><div><h2>{C['company']}</h2><a href="{prefix}about.html">{C['f_about']}</a><a href="{prefix}trust.html">{C['f_trust']}</a></div></div><div class="footer-bottom"><span>© 2026 {E(SITE['legal_name'])}{' · '+E(SITE['registration_line']) if SITE['registration_line'] else ''}</span><span><a href="{prefix}privacy.html">{C['privacy']}</a><span class="meta-dot">/</span>{C['research_mark']}</span><a href="#main">{C['top']} </a></div></div></footer></body></html>'''


def cta(prefix=''):
    return f'''<section class="briefing-banner"><div class="container"><div><div class="eyebrow">Research enquiries</div><h2>What would better evidence<br>change for you?</h2><p>Tell us your sector, the decision you face, and what a useful first briefing would need to demonstrate.</p></div><a class="button button-light" href="{prefix}briefing.html">See how we can help you {ARROW}</a></div></section>'''


def home():
    return research_hero()+claims()


def intro(kicker, title, description):
    return f'<section class="page-intro container"><div class="eyebrow">{kicker}</div><h1>{title}</h1><p>{description}</p></section>'


def about():
    story = ('<section class="about-story container"><div class="about-visual"><span class="eyebrow">ECHOFRAME</span>'
             + MARK + '<span>Research and assessment</span></div><div>'
             '<h2>The information exists.<br>It is not where people look.</h2>'
             '<p>I spent twenty years as an investigative reporter and risk analyst, most of it in Latin America, '
             'and then a decade building the data systems that try to close the gap between what is known in a '
             'place and what reaches a desk in London or New York.</p>'
             '<p>The people who know what is happening somewhere are the journalists who live there. Very little of '
             'what they know reaches the wires, because nobody is paying for it to. Meanwhile the money goes to '
             'exactly those places. Emerging-market supply chains run through provinces and districts no '
             'correspondent covers, and it is there that a licence, a workforce or a road decides whether an asset '
             'keeps running.</p>'
             '<p>EchoFrame is built on that gap. Find what local reporting already knows, check it against official '
             'records, physical data and markets, and read the meaning out of it, and you can see where something '
             'is going while there is still time to act on it.</p>'
             '<p class="eyebrow">Robert Shaw, founder</p></div></section>')
    return (intro('About EchoFrame', 'Why the company exists',
                  'The people who know what is happening in a place are usually the local journalists. Everything we '
                  'build starts there.')
            + story
            + video_section() + testimonials() + faq() + cta())


def briefing():
    return contact_page()

def privacy():
    return intro('Privacy','How your information is used','What happens when you read this website, save an article, or send EchoFrame a request.')+'''<div class="prose-page container"><section><h2>When you send a request</h2><p>The contact form sends the details you enter to the website’s contact service, which forwards them to EchoFrame through its configured email provider. These details include your name, work email, organisation, sector and decision or question, together with any role, additional details and referral information you provide.</p><p>We use this information to respond to your conversation request. The form does not subscribe you to marketing. Please do not send confidential documents or information that identifies a protected source.</p><p>If the email connection is unavailable, the form tells you that delivery has not been confirmed. Your details remain in the form so you can review them. They are not saved in your browser when you leave.</p></section><section><h2>Delivery records and abuse prevention</h2><p>The website keeps short-lived technical records to limit repeated requests and prevent duplicate email. These contain a random request reference, a keyed digest of the request, its delivery state and a timestamp. They do not contain the text of your message. Request records expire after 24 hours; rate-limit records expire after an hour. Expired records are cleared when new requests are processed.</p><p>A keyed digest of the connection address is used for rate limiting. Hosting and email providers may also process normal service logs and message records. Messages delivered to EchoFrame are held in its email service so the team can respond. Contact us to discuss deletion or retention of correspondence you have sent.</p></section><section><h2>Reading and saved articles</h2><p>Saved article identifiers stay in local storage in this browser. They do not create an account or send your reading list to EchoFrame. Use the save control again to remove an article, or clear the site data on your device.</p><p>This build contains no advertising trackers, analytics scripts, or newsletter database. The presentation video is served from the website without an embedded third-party video player.</p></section><section><h2>External services</h2><p>Google Fonts serves the website’s typography. Your browser connects to Google to retrieve it. The host may process ordinary request information to deliver pages and media.</p><p>Calendar booking opens Cal.com. Regional platform and social links open separate websites with their own data-handling and account arrangements. Email links elsewhere on the website open your chosen email application.</p></section><section><h2>Contact</h2><p>For privacy questions or requests about information you have provided, email <a href="mailto:contact@echoframe.co?subject=Privacy%20request">contact@echoframe.co</a>. This website is operated by EchoFrame Intelligence AB, registered in 2026.</p><p>Last updated: 11 September 2026.</p></section></div>'''


def spanish():
    return spanish_page(intro)


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
    dest.write_text(layout(title,enquiry_policy(body,path),page,prefix,description,lang),encoding='utf-8')
    GENERATED.append(path)


def main():
    globe()
    downloads = write_downloads() + write_sample_downloads()
    for path, title, render, key in PAGES:
        write(path, title, render(), key)
    write('sample-briefs.html','Sample briefs & templates',sample_library(),'samples')
    for sample in SAMPLES:
        write(sample['slug']+'.html',sample['title'],sample_page(sample),'sample')
    write('index.html','A clearer view of a complex world',home())
    write('site.html','A clearer view of a complex world',home())
    write('government-affairs.html','Oil & gas government affairs',audience_page('government'),'government',description='Political intelligence for oil and gas government affairs teams. Scope research on stakeholders, policy milestones, and the evidence around operating assets.')
    write('distressed-debt.html','Distressed debt & special situations',audience_page('credit'),'credit',description='Political and asset-level research for distressed-debt investors. Frame thesis questions, inspect counterparty narratives, and identify evidence worth reviewing.')
    write('services.html','Products',services.overview(intro),'services')
    for line in services.SERVICES:
        write(line['slug']+'.html', line['name'], services.service_page(intro, line['slug']), 'services')
    write('projects.html','Bespoke projects',services.projects_page(intro),'services')
    write('commodities.html', sectors.SECTORS['commodities']['name'],
          sectors.page(intro, 'commodities'), 'sector',
          description=sectors.SECTORS['commodities']['description'])
    write('coverage.html','Regional coverage',coverage_page(intro),'coverage')
    write('venezuela.html','Venezuela · Asset-level intelligence',venezuela_page(intro,cta),'venezuela')
    write('how-it-works.html','How it works',how_it_works_page(intro),'how-it-works')
    write('worked-examples.html','Worked examples',worked_examples_page(intro),'worked-examples')
    write('frame-bureau.html','The Frame Bureau',frame_bureau_page(intro),'frame-bureau')
    write('about.html','About',about(),'about')
    write('briefing.html','Book a briefing',briefing(),'briefing')
    write('privacy.html','Privacy',privacy(),'privacy')
    # The Spanish mirror is suspended. spanish() and the 'es' chrome stay in the
    # repository so the page can be restored without rebuilding it.
    write('404.html','Page not found',intro('404','That page is not here','The page you requested could not be found.')+'<div class="container section"><a class="button" href="index.html">Return to the homepage </a></div>')
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
    files = published_pages + ['favicon.png', 'assets/site.css', 'assets/presence.css', 'assets/depth.css', 'assets/refinements.css', 'assets/bureau.css', 'assets/site.js', 'assets/globe.svg', 'assets/energy-horizon.png', 'assets/hero-terminal.jpg', 'assets/example-evidence.jpg', 'assets/case_upgrader.jpg', 'assets/case_terminal.jpg', 'assets/case_docket.jpg', 'assets/case_gasplant.jpg', 'assets/social-card.svg', 'assets/social-card.png', 'assets/ATTRIBUTION.md']
    files += downloads + ['images/EchoFramev3.mp4']
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
    print(f'Built {len(GENERATED)} pages; {len(published_pages)} published plus the legacy redirect. Deployment directory: public/')


if __name__=='__main__': main()
