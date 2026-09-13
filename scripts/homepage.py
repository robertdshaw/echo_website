"""A short front door: what we collect, how we check it, what a client gets."""


def claims():
    sections = [
        ('01 / Where we collect', 'Outside the capitals',
         'Oil states in eastern and western Venezuela, with Colombia, Mexico, Rwanda and Pakistan next. '
         'We work where the reporting is thinnest and the exposure is largest.'),
        ('02 / How we check it', 'Nothing counts on one class of source',
         'News media count as one class however many outlets carry a story. Official records, independent research, '
         'physical data and reporting from the ground are the others. A development is confirmed when independent classes agree.'),
        ('03 / What you get', 'A record, not a report',
         'A dated record of developments at named assets, a short list of written questions with dates on them, '
         'and a probability on each that moves only when the evidence does.'),
        ('04 / What we deliver', 'Three things to subscribe to, three to commission',
         'Asset Watch covers the assets you name. Question Book answers the questions you have to settle. Ground '
         'Truth files reporting from the places we cover. <a href="services.html">See what we deliver</a>.'),
    ]
    blocks = ''.join(
        f'<section class="home-claim" aria-labelledby="claim-{i}"><div class="eyebrow">{kicker}</div>'
        f'<div><h2 id="claim-{i}">{title}</h2><p>{copy}</p></div></section>'
        for i, (kicker, title, copy) in enumerate(sections, 1)
    )
    closing = ('<section class="home-claim home-closing"><div><p>If the decision in front of you depends on '
               'somewhere the wires do not cover, start a conversation.</p></div></section>')
    return '<div class="home-claims container">' + blocks + closing + '</div>'
