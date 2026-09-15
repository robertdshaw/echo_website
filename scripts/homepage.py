"""A short front door: what we collect, how we check it, what a client gets."""


def claims():
    sections = [
        ('01 / The problem', 'Getting information out of remote places',
         'Your exposure sits in the places that are hardest to get information out of. A supply chain runs '
         'from an oilfield in Venezuela to a mine in Rwanda and through a dozen countries in between. '
         'Finding someone reliable in any of them at short notice is slow and expensive. That is the part '
         'we are built for.'),
        ('02 / What we do about it', 'A collection system running down to the municipality',
         'We run collection in the places the wires do not reach, at the level of the municipality and the town. '
         'Local, offline and paywalled material is pulled in continuously, checked against official records, '
         'physical data and markets, and turned into dated events with named actors. Counted over time, those '
         'events are the signals that move ahead of a risk rather than describing it afterwards. The coverage is '
         'running before you need it, so the answer does not begin with a search for someone reliable.'),
        ('03 / What we watch', 'Licensing, labour, security, politics and contract terms',
         'The five things that decide whether an asset keeps running and what it is worth. Who holds the '
         'permit and on what condition. Whether the workforce is about to stop. What is happening around '
         'the site. Which way the politics is turning. What the contract obliges each side to do.'),
        ('04 / Where we work',
         'Collection runs in Venezuela. Colombia, Mexico, Rwanda and Pakistan are being built.',
         'Tell us where you operate and we will tell you plainly whether we cover it.'),
        ('05 / What you get', 'An alert, a brief, a report, or an answer',
         'Continuous coverage of places that are remote, volatile and largely offline, in whatever '
         'form the decision needs. An alert the day a development is confirmed. A short brief when it needs '
         'explaining. A full report when it has to go to a board or an investment committee. A direct answer '
         'when you would rather ask someone who already knows. Everything carries the date it was confirmed '
         'and the sources behind it, so you can check the basis rather than take our word. '
         '<a href="services.html">See the products</a>, or read '
         '<a href="how-it-works.html">how the work is done</a>.'),
    ]
    blocks = ''.join(
        f'<section class="home-claim" aria-labelledby="claim-{i}"><div class="eyebrow">{kicker}</div>'
        f'<div><h2 id="claim-{i}">{title}</h2><p>{copy}</p></div></section>'
        for i, (kicker, title, copy) in enumerate(sections, 1)
    )
    closing = ('<section class="home-claim home-closing"><div><p>If the decision in front of you depends on '
               'somewhere the wires do not cover, start a conversation.</p></div></section>')
    return '<div class="home-claims container">' + blocks + closing + '</div>'
