"""Shared navigation for the full research website."""
from html import escape as E

GROUPS = [
    ('Capabilities', [
        ('capabilities.html','Research system','Explore the full analytical workflow.'),
        ('actor-mapping.html','Actor & asset mapping','Document the relationships behind a decision.'),
        ('evidence-workspace.html','Evidence workspace','Inspect sources, contradictions, and limits.'),
        ('decision-pathways.html','Decision pathways','Define milestones and review triggers.')]),
    ('Who we help', [
        ('government-affairs.html','Government affairs','Policy, stakeholders, and operating assets.'),
        ('distressed-debt.html','Distressed debt','Political assumptions and counterparty research.'),
        ('engagement.html','Working with EchoFrame','Research formats, scope, and delivery.')]),
    ('Research', [
        ('research.html','Intelligence library','Essays, field guides, and programme notes.'),
        ('sample-briefs.html','Sample briefs & templates','Complete fictional examples and downloads.'),
        ('sources.html','Primary-source directory','Official records and how to use them.'),
        ('coverage.html','Regional perspective','Explore the wider research frame.')]),
    ('Company', [
        ('about.html','About EchoFrame','The purpose and approach behind the research.'),
        ('methodology.html','Our methodology','From collection to an inspectable judgment.'),
        ('trust.html','Trust & privacy','Evidence, information handling, and boundaries.'),
        ('editorial-standards.html','Editorial standards','Attribution, uncertainty, and corrections.')])
]


def navigation(prefix=''):
    result=''
    for title,items in GROUPS:
        result+=f'<details class="nav-group"><summary>{title}</summary><div class="nav-panel"><div class="nav-panel-label">{title}</div>'
        result+=''.join(f'<a href="{prefix}{url}"><strong>{E(label)}</strong><small>{E(desc)}</small></a>' for url,label,desc in items)
        result+='</div></details>'
    return result+f'<a href="{prefix}venezuela.html">Venezuela</a>'


def home_directory():
    return '''<section class="section container site-directory"><div class="section-heading"><div><div class="eyebrow">Inside EchoFrame</div><h2>More to explore.<br>More to work with.</h2></div><p>Go from the overview to the method, the evidence, and the output. Choose the level of detail you need.</p></div><div class="depth-link-grid"><a href="capabilities.html"><span>01 / THE RESEARCH SYSTEM</span><h3>Explore the capabilities.</h3><p>Interactive actor maps, evidence review, and decision pathways.</p><b></b></a><a href="sample-briefs.html"><span>02 / THE FINISHED FORMAT</span><h3>Read a complete brief.</h3><p>Two fictional research examples with downloadable copies and blank templates.</p><b></b></a><a href="sources.html"><span>03 / THE SOURCE RECORD</span><h3>Start with primary sources.</h3><p>Official research references, use notes, and the limits to keep in view.</p><b></b></a></div><div class="directory-bottom"><a href="trust.html">Trust, privacy & source handling </a><a href="engagement.html">How a research engagement works </a></div></section>'''
