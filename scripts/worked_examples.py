"""Worked examples. Real engagements, no client named, one shape for every card."""

CARDS = [
    ('The regulation you did not see coming',
     'The EU government affairs team of a major US oil and gas producer. Proposal, February 2026.',
     'assets/example-evidence.jpg',
     'The record is public and scattered. Legislation, votes, consultations and committee activity are published '
     'by different institutions on different days and never in one place.',
     [('The situation',
       'A government affairs team was tracking European regulation by hand, across institutions that publish '
       'continuously and never in the same place.'),
      ('The question',
       'Which of the things moving in Brussels actually touches our assets, and how early can we see one coming?'),
      ('What the evidence showed',
       'Almost all of it is public and almost none of it is usable as a record. Adopted law sits in EUR-Lex and the '
       'Official Journal, positions show up in committee activity and roll-call votes, direction comes from Council '
       'outcomes and Commission press, and the detail arrives in consultations run by the climate, energy and '
       'environment directorates. Reading them is not the hard part. Knowing which document touches your own '
       'exposure is. We mapped the team’s assets onto the policy domains that could move them, which were '
       'methane, the carbon border mechanism, emissions trading, hydrogen classification, gas and LNG policy, '
       'sustainability reporting and refining standards, and scored each document against those rather than '
       'against general interest.'),
      ('What it changed',
       'The proposal replaced manual monitoring with a pipeline that reads those sources continuously, scores each '
       'document against the team’s own exposure, and flags a domain when its volume breaks from its own '
       'baseline. One regulatory change landing unseen costs more than watching for it does, and that was the '
       'argument the team needed to make internally.')]),
    ('The deal that was not yours still moved your position',
     'A US company holding substantial unpaid arbitration awards against a sovereign, with no operations in the '
     'country. April 2026.',
     None, None,
     [('The situation',
       'Two competitors announced an asset swap, one consolidating heavy crude, the other consolidating cross-border '
       'gas.'),
      ('The question', 'Does a transaction we are not part of change what our claims are worth?'),
      ('What the evidence showed',
       'Three ways. The crude consolidation raised the barrier to any operational return to the former acreage, '
       'which made a negotiated settlement more likely than re-entry. The transition government had a structural '
       'reason to clear legacy claims, because unresolved awards create legal risk over the state company cargoes '
       'and receivables and deter the investment it was courting. That made the claims leverage rather than history. '
       'And the gas consolidation improved the long-run feed outlook for a liquefaction plant in which the client '
       'holds equity, which is second order but real.'),
      ('What it changed',
       'The client moved from enforcement to structured settlement, timed to the government licensing window rather '
       'than to the arbitration calendar. What would close that window is resistance to the licensing framework from '
       'the hardliners and the military, and that is what we watch.')]),
    ('A state that wanted the capability, not the service',
     'A Gulf government. Capability design, 2026.',
     None, None,
     [('The situation',
       'Ministries were commissioning the same country and sector analysis repeatedly from outside firms, with '
       'nothing accumulating between engagements.'),
      ('The question', 'What would it take to build this inside the state instead of renting it?'),
      ('What the evidence showed',
       'Three things had to be built together rather than in sequence. A collection and data layer, so there is a '
       'record instead of a series of reports. An actor and behaviour layer, because most questions a government '
       'asks are about what specific people will do. And a way of testing a move before making it, so a decision can '
       'be pressure-tested rather than defended after the fact. We proposed an eighteen-month build in six stages, '
       'each with named staff and a defined handover, moving from our people leading to joint delivery to their '
       'people leading. The point of the sequence is that capability stays when we leave.'),
      ('What it changed',
       'The conversation moved from what a report would cost to what an internal function would cost to run, which '
       'is a different and more useful question.')]),
]

def page(intro):
    cards = ''
    for i, (title, context, image, caption, rows) in enumerate(CARDS, 1):
        lead = dict(rows)
        head = ''.join(
            f'<div class="we-line"><span class="eyebrow">{h}</span><p>{lead[h]}</p></div>'
            for h in ('The situation', 'The question') if h in lead)
        rest = ''.join(
            f'<div class="we-block"><span class="eyebrow">{h}</span><p>{text}</p></div>'
            for h, text in rows if h not in ('The situation', 'The question'))
        cards += (f'<article class="worked-example" id="example-{i}">'
                  f'<header class="we-head"><span class="we-number">{i:02d}</span>'
                  f'<div><h2>{title}</h2><p class="we-meta">{context}</p></div></header>'
                  + (f'<figure class="we-figure"><img src="{image}" alt="" width="1200" height="675" loading="lazy">'
                     f'<figcaption>{caption}</figcaption></figure>' if image else '')
                  + f'<div class="we-frame">{head}</div>'
                  f'<div class="we-body">{rest}</div></article>')
    return intro(
        'Worked examples',
        'Three pieces of work, and what each one changed',
        'Every one of these is real. No client is named and no figure from a client document appears. Where a '
        'number carried the argument it has been replaced by the proportion or the direction.'
    ) + '<section class="section container worked-examples">' + cards + '</section>'
