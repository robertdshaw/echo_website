"""What we deliver. Three subscriptions, three projects, no prices anywhere."""

SERVICES = [
    ('Asset Watch', [
        ('What it is', 'Continuous monitoring of the assets you name. Every development at or near them is recorded '
                       'with its date, its place, its type and the sources behind it, and you are told the day one '
                       'clears our corroboration rule.'),
        ('What arrives', 'An alert on the day a development is confirmed, with the sources and what it affects. A '
                         'weekly brief for each asset after an analyst has read it. Every claim in the brief carries '
                         'a reference back to the record, so anything can be traced.'),
        ('What does not arrive', 'Rumour, unconfirmed chatter, or anything we cannot show you the basis for. Most '
                                 'weeks are quiet. That is the point of continuous coverage rather than a report.'),
        ('Who it is for', 'Operators with people and equipment on the ground, their contractors, and anyone whose '
                          'planning depends on whether a specific site keeps running.'),
        ('Where it is available', 'Eastern and western Venezuela today. Colombia, Mexico, Rwanda and Pakistan as '
                                  'collection is built.'),
    ], 'Talk to us about the assets you need watched.'),
    ('Question Book', [
        ('What it is', 'A written set of questions about your assets, contracts and counterparties, each with a date '
                       'by which it will be settled and a rule for how it settles. Each carries a probability that '
                       'moves only when evidence clears the same corroboration rule, and each is scored when its '
                       'date arrives.'),
        ('What arrives', 'The question set, agreed with you and then frozen so it cannot drift. A probability on each '
                         'with the developments that moved it, inspectable down to the sources. An answer and a score '
                         'on the date, kept as a record over time.'),
        ('Why the scoring matters', 'Any firm can give you a probability. Very few will tell you afterwards whether '
                                    'it was any good. The record of what we got right and wrong is the only honest '
                                    'basis for what our next number is worth.'),
        ('Who it is for', 'Credit and special situations investors, and corporate teams who have to defend an '
                          'assumption to a board or an investment committee.'),
    ], 'Talk to us about the decisions you need answered.'),
    ('Ground Truth', [
        ('What it is', 'Structured reporting from correspondents in the places we cover, filed as records rather than '
                       'articles and joined directly to your asset coverage. It carries more weight than any media '
                       'source, because it comes from someone who was there.'),
        ('What arrives', 'A record within hours of filing, with what happened, where, who was involved and how the '
                         'reporter knows it. It reaches you before the national press has the story, and often when '
                         'the national press never runs it at all.'),
        ('How it works', 'We pay local newsrooms for the collection alongside their own reporting. The correspondents '
                         'stay inside their newsroom under their own editors. Their identities stay with them and '
                         'never reach us or you.'),
        ('Who it is for', 'Anyone already taking Asset Watch or Question Book whose assets sit in a covered state. It '
                          'is not sold on its own, because on its own it is a stream of reports with nothing to '
                          'attach them to.'),
        ('Where it is available', 'Only where the correspondent network exists. We will tell you plainly whether that '
                                  'covers where you are exposed.'),
    ], 'Talk to us about where you need someone on the ground.'),
]

PROJECTS = [
    ('Viability assessment', 'A legal and contractual read of one asset against six criteria, each citing the '
                             'document it rests on. Refreshed for twelve months whenever a development touches that '
                             'asset.'),
    ('Question design', 'Turning a decision you have to make into a set of questions that can actually be settled, '
                        'with the evidence rules written down. Most questions people bring us cannot be answered as '
                        'asked. This is the work of fixing that.'),
    ('Zone brief', 'A single deep read of one state or one cluster of assets, built from the record and ending with '
                   'the questions worth running and what would settle them.'),
    ('Scoping conversation', 'Defining the subject, the decision and the horizon before any mandate. No charge.'),
]


def page(intro):
    services = ''
    for i, (name, rows, invitation) in enumerate(SERVICES, 1):
        body = ''.join(f'<div><span class="eyebrow">{heading}</span><p>{text}</p></div>' for heading, text in rows)
        services += (f'<article class="service-line" id="service-{i}"><div class="eyebrow">{i:02d}</div>'
                     f'<h2>{name}</h2><div class="standards-grid">{body}</div>'
                     f'<p class="service-invitation"><strong>{invitation}</strong></p></article>')
    projects = ''.join(f'<li><h3>{name}</h3><p>{text}</p></li>' for name, text in PROJECTS)
    return intro(
        'What we deliver', 'Three things to subscribe to, three to commission',
        'The subscriptions cover named assets and named questions continuously. The projects are single pieces of '
        'work with a defined scope. Access to the record comes with any subscription and is not sold on its own, '
        'because what you are paying for is coverage rather than logins.'
    ) + f'''<section class="section container services">{services}</section>
<section class="section container" id="projects"><div class="section-heading"><div><div class="eyebrow">Projects</div><h2>Single pieces of work</h2></div><p>Each has a defined scope and an agreed deliverable.</p></div><ul class="project-list">{projects}</ul></section>
<section class="section container" id="what-it-costs"><div class="prose-page"><p>Pricing depends on the number of assets, the number of questions and whether ground reporting is included. We will tell you what your coverage would cost in the first conversation, and what it would not cover.</p></div></section>'''
