"""What we deliver. An overview, one page per service line, and the projects page.

Copy is docs/services_copy.md. No price, tier or range appears on any of these
pages. Each service line has its own page so a reader arrives at the one thing
they came for rather than a list of everything.
"""

SERVICES = [
    {
        "slug": "asset-watch",
        "name": "Asset Watch",
        "index": "01",
        "kicker": "Subscription / Continuous",
        "lede": "Continuous monitoring of the assets you name. Every development at or near them is recorded "
                "with its date, its place, its type and the sources behind it, and you are told the day one "
                "clears our corroboration rule.",
        "summary": "Continuous monitoring of the assets you name, with an alert the day a development is "
                   "confirmed.",
        "sections": [
            ("What arrives",
             ["An alert on the day a development is confirmed, with the sources and what it affects.",
              "A weekly brief for each asset after an analyst has read it.",
              "Every claim in the brief carries a reference back to the record, so anything can be traced."]),
            ("What does not arrive",
             ["Rumour, unconfirmed chatter, or anything we cannot show you the basis for.",
              "Most weeks are quiet. That is the point of continuous coverage rather than a report."]),
            ("Who it is for",
             ["Operators with people and equipment on the ground, their contractors, and anyone whose "
              "planning depends on whether a specific site keeps running."]),
            ("Where it is available",
             ["Eastern and western Venezuela today.",
              "Colombia, Mexico, Rwanda and Pakistan as collection is built."]),
        ],
        "close": "Talk to us about the assets you need watched.",
        "invitation": "Tell us which assets to watch",
    },
    {
        "slug": "question-book",
        "name": "Question Book",
        "index": "02",
        "kicker": "Subscription / Dated questions",
        "lede": "A written set of questions about your assets, contracts and counterparties, each with a date "
                "by which it will be settled and a rule for how it settles. Each carries a probability that "
                "moves only when evidence clears the same corroboration rule, and each is scored when its "
                "date arrives.",
        "summary": "Written questions with a date and a rule for settling them, each scored when the date "
                   "arrives.",
        "sections": [
            ("What arrives",
             ["The question set, agreed with you and then frozen so it cannot drift.",
              "A probability on each with the developments that moved it, inspectable down to the sources.",
              "An answer and a score on the date, kept as a record over time."]),
            ("Why the scoring matters",
             ["Any firm can give you a probability. Very few will tell you afterwards whether it was any good.",
              "The record of what we got right and wrong is the only honest basis for what our next number "
              "is worth."]),
            ("Who it is for",
             ["Credit and special situations investors, and corporate teams who have to defend an assumption "
              "to a board or an investment committee."]),
        ],
        "close": "Talk to us about the decisions you need answered.",
        "invitation": "Bring us a decision to turn into questions",
    },
    {
        "slug": "ground-truth",
        "name": "Ground Truth",
        "index": "03",
        "kicker": "Subscription / Reporting from the place",
        "lede": "Structured reporting from correspondents in the places we cover, filed as records rather "
                "than articles and joined directly to your asset coverage. It carries more weight than any "
                "media source, because it comes from someone who was there.",
        "summary": "Reporting filed from the place itself, joined to your asset coverage rather than "
                   "published as articles.",
        "sections": [
            ("What arrives",
             ["A record within hours of filing, with what happened, where, who was involved and how the "
              "reporter knows it.",
              "It reaches you before the national press has the story, and often when the national press "
              "never runs it at all."]),
            ("How it works",
             ["We pay local newsrooms for the collection alongside their own reporting.",
              "The correspondents stay inside their newsroom under their own editors.",
              "Their identities stay with them and never reach us or you."]),
            ("Who it is for",
             ["Anyone already taking Asset Watch or Question Book whose assets sit in a covered state.",
              "It is not sold on its own, because on its own it is a stream of reports with nothing to "
              "attach them to."]),
            ("Where it is available",
             ["Only where the correspondent network exists.",
              "We will tell you plainly whether that covers where you are exposed."]),
        ],
        "close": "Talk to us about where you need someone on the ground.",
        "invitation": "Ask where we have people on the ground",
    },
]

PROJECTS = [
    ("Viability assessment",
     "A legal and contractual read of one asset against six criteria, each citing the document it rests on. "
     "Refreshed for twelve months whenever a development touches that asset."),
    ("Question design",
     "Turning a decision you have to make into a set of questions that can actually be settled, with the "
     "evidence rules written down. Most questions people bring us cannot be answered as asked. This is the "
     "work of fixing that."),
    ("Zone brief",
     "A single deep read of one state or one cluster of assets, built from the record and ending with the "
     "questions worth running and what would settle them."),
    ("Scoping conversation",
     "Defining the subject, the decision and the horizon before any mandate. No charge."),
]

PRICING = ("Pricing depends on the number of assets, the number of questions and whether ground reporting is "
           "included. We will tell you what your coverage would cost in the first conversation, and what it "
           "would not cover.")


def overview(intro):
    cards = ''.join(
        f'<a href="{s["slug"]}.html"><span>{s["index"]} / SUBSCRIPTION</span><h3>{s["name"]}</h3>'
        f'<p>{s["summary"]}</p><b></b></a>' for s in SERVICES)
    projects = ''.join(f'<li><h3>{name}</h3></li>' for name, _ in PROJECTS)
    return intro(
        'What we deliver', 'Three things to subscribe to, three to commission',
        'The subscriptions cover named assets and named questions continuously. The projects are single '
        'pieces of work with a defined scope.'
    ) + f'''<section class="section container" id="subscriptions"><div class="section-heading"><div><div class="eyebrow">Subscriptions</div><h2>Coverage that keeps running</h2></div><p>Access to the record comes with any subscription and is not sold on its own, because what you are paying for is coverage rather than logins.</p></div><div class="depth-link-grid">{cards}</div></section>
<section class="section container" id="projects"><div class="section-heading"><div><div class="eyebrow">Projects</div><h2>Single pieces of work</h2></div><p>Each has a defined scope and an agreed deliverable. A scoping conversation comes first and carries no charge.</p></div><ul class="project-list project-list-compact">{projects}</ul><p class="service-more"><a href="projects.html">What each project covers</a></p><div class="service-pricing"><span class="eyebrow">What it costs</span><p>{PRICING}</p></div></section>'''


def service_page(intro, slug):
    s = next(x for x in SERVICES if x["slug"] == slug)
    others = [o for o in SERVICES if o["slug"] != slug]
    body = ''
    for heading, points in s["sections"]:
        paragraphs = ''.join(f'<p>{p}</p>' for p in points)
        body += (f'<section class="section container service-section"><div class="section-heading"><div>'
                 f'<h2>{heading}</h2></div></div><div class="prose-page">{paragraphs}</div></section>')
    nav = ''.join(
        f'<a href="{o["slug"]}.html"><span>{o["index"]} / SUBSCRIPTION</span><h3>{o["name"]}</h3>'
        f'<p>{o["summary"]}</p><b></b></a>' for o in others)
    return intro(s["kicker"], s["name"], s["lede"]) + body + (
        '<section class="section container"><div class="section-heading"><div>'
        '<div class="eyebrow">The other subscriptions</div><h2>What else the record carries</h2></div></div>'
        f'<div class="depth-link-grid">{nav}</div></section>')


def projects_page(intro):
    items = ''.join(
        f'<div><span class="eyebrow">{i:02d}</span><h3>{name}</h3><p>{text}</p></div>'
        for i, (name, text) in enumerate(PROJECTS, 1))
    return intro(
        'Projects', 'Single pieces of work',
        'Each project has a defined scope and an agreed deliverable. They stand on their own, and they are '
        'often how a subscription starts.'
    ) + f'''<section class="section container"><div class="standards-grid">{items}</div></section>
<section class="section container"><div class="prose-page"><p>{PRICING}</p></div></section>'''
