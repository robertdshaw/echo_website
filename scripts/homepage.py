"""A short front door: what we collect, how we check it, what a client gets."""


def claims():
    sections = [
        ('01 / The problem', 'You hear it once it is already priced in',
         'Your exposure sits in the places that are hardest to get information out of. A supply chain runs '
         'from an oilfield in Venezuela to a mine in Rwanda and through a dozen countries in between. '
         'Finding someone reliable in any of them at short notice is slow and expensive. That is the part '
         'we are built for.'),
        ('02 / What we watch', 'Licensing, labour, security, politics and contract terms',
         'The five things that decide whether an asset keeps running and what it is worth. Who holds the '
         'permit and on what condition. Whether the workforce is about to stop. What is happening around '
         'the site. Which way the politics is turning. What the contract obliges each side to do.'),
        ('03 / Where we work', 'Outside the capitals, and quick to add the next one',
         'Oil states in eastern and western Venezuela today, with Colombia, Mexico, Rwanda and Pakistan '
         'next. The method does not change from one country to the next, so a new desk starts from the '
         'last one rather than from nothing. Tell us where you operate.'),
        ('04 / How we check it', 'Nothing counts on one class of source',
         'News media count as one class however many outlets carry a story. Official records, independent '
         'research, physical data and reporting from the ground are the others. A development is confirmed '
         'when independent classes agree, and it reaches you carrying the date and the sources behind it.'),
        ('05 / What you get', 'An alert, a brief, a report, or an answer',
         'Continuous coverage of places that are hard to reach, volatile and largely offline, in whatever '
         'form the decision needs. An alert the day a development is confirmed. A short brief when it needs '
         'explaining. A full report when it has to go to a board or an investment committee. A direct answer '
         'when you would rather ask someone who already knows. <a href="services.html">See the products</a>.'),
    ]
    blocks = ''.join(
        f'<section class="home-claim" aria-labelledby="claim-{i}"><div class="eyebrow">{kicker}</div>'
        f'<div><h2 id="claim-{i}">{title}</h2><p>{copy}</p></div></section>'
        for i, (kicker, title, copy) in enumerate(sections, 1)
    )
    closing = ('<section class="home-claim home-closing"><div><p>If the decision in front of you depends on '
               'somewhere the wires do not cover, start a conversation.</p></div></section>')
    return '<div class="home-claims container">' + blocks + closing + '</div>'
