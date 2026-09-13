"""Shared navigation for the full research website."""
from html import escape as E
from chrome import GROUPS_ES, ITEMS_ES

GROUPS = [
    ('Services', [
        ('services.html','What we deliver','The subscriptions and the projects, in one view.'),
        ('asset-watch.html','Asset Watch','Continuous coverage of the assets you name.'),
        ('question-book.html','Question Book','Dated questions, scored when the date arrives.'),
        ('ground-truth.html','Ground Truth','Reporting filed from the place itself.'),
        ('projects.html','Projects','Single pieces of work with a defined scope.')]),
    ('Our work', [
        ('government-affairs.html','Government affairs','Policy, stakeholders, and operating assets.'),
        ('distressed-debt.html','Distressed debt','Political assumptions and counterparty research.'),
        ('engagement.html','Working with EchoFrame','Formats, scope, and delivery.')]),
    ('Cases', [
        ('case-study-venezuela.html','Case study, Venezuela','A call made before the outcome.'),
        ('worked-examples.html','Worked examples','Three pieces of work, and what each changed.'),
        ]),
    ('Training', 'frame-bureau.html'),
    ('About', [
        ('about.html','About EchoFrame','The purpose and approach behind the research.'),
        ('how-it-works.html','How it works','The six steps, and how a development is confirmed.'),
        ('trust.html','Trust & privacy','Evidence, information handling, and boundaries.'),
        ('editorial-standards.html','Editorial standards','Attribution, uncertainty, and corrections.')])
]


def navigation(prefix='', lang='en'):
    result=''
    for title,items in GROUPS:
        label = GROUPS_ES[title] if lang=='es' else title
        if isinstance(items, str):
            # A group of one is a link, not a menu to open.
            result += f'<a class="nav-direct" href="{prefix}{items}">{E(label)}</a>'
            continue
        panel_label = f'{label} (en inglés)' if lang=='es' else label
        result+=f'<details class="nav-group"><summary>{E(label)}</summary><div class="nav-panel"><div class="nav-panel-label">{E(panel_label)}</div>'
        for url,item_label,desc in items:
            if lang=='es':
                item_label,desc = ITEMS_ES.get(url,(item_label,desc))
            result+=f'<a href="{prefix}{url}"><strong>{E(item_label)}</strong><small>{E(desc)}</small></a>'
        result+='</div></details>'
    return result


def home_directory():
    return '''<section class="section container site-directory"><div class="section-heading"><div><div class="eyebrow">Inside EchoFrame</div><h2>More to explore.<br>More to work with.</h2></div><p>Go from the overview to the method, the evidence, and the output. Choose the level of detail you need.</p></div><div class="depth-link-grid"><a href="capabilities.html"><span>01 / THE RESEARCH SYSTEM</span><h3>Explore the capabilities.</h3><p>Interactive actor maps, evidence review, and decision pathways.</p><b></b></a><a href="sample-briefs.html"><span>02 / THE FINISHED FORMAT</span><h3>Forthcoming research briefs</h3><p>Blank templates and space for real, redacted research material.</p><b></b></a><a href="sources.html"><span>03 / THE SOURCE RECORD</span><h3>Start with primary sources.</h3><p>Official research references, use notes, and the limits to keep in view.</p><b></b></a></div><div class="directory-bottom"><a href="trust.html">Trust, privacy & source handling </a><a href="engagement.html">How a research engagement works </a></div></section>'''
