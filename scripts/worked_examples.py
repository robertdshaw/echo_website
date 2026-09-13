"""Worked examples. Real engagements, no client named, one shape for every card."""

CARDS = [
    ('The headline number was double the real one',
     'The same desk, six months later.',
     [('The situation',
       'Oil exports were reported at close to double the previous year, and the market read the figure as capacity '
       'to pay.'),
      ('The question', 'How much of that actually reaches the state?'),
      ('What the evidence showed',
       'The export figure is gross. Four deductions come off before any of it is available. The operating majors '
       'recover their costs under the licences they work under. An administration fee applies to sanctioned-channel '
       'sales. Royalties are paid in kind rather than cash. And the largest single operator keeps its dollar revenue '
       'offshore by design. Working each deduction against the licence terms and the reported volumes left roughly '
       'half the headline, and the gap was large enough to change the conclusion rather than refine it.'),
      ('What it changed',
       'Any capacity-to-pay model built on the export print overstated the position by close to half. The number '
       'that mattered had to be built from the licence terms rather than read off the trade data. The two things to '
       'watch are changes to those terms and grid failures that cap output, because both move the real figure '
       'without moving the headline.')]),
    ('The deal that was not yours still moved your position',
     'A US company holding substantial unpaid arbitration awards against a sovereign, with no operations in the '
     'country. April 2026.',
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
    ('Which claim, in what structure, below what price',
     'A distressed credit fund with no existing position. Scoping work, September 2026.',
     [('The situation',
       'A court-run sale of a sovereign US refining subsidiary, with a public queue of creditors waiting to be paid '
       'from the proceeds.'),
      ('The question', 'Should we enter the queue, and if so how?'),
      ('What the evidence showed',
       'The queue is public in the court docket and the arithmetic is unforgiving. Expected proceeds covered the '
       'first nine priorities comfortably and the first thirteen at a stretch. The largest claim sat fourteenth and '
       'needed proceeds far above any plausible sale price to be paid at all, which makes it a call option rather '
       'than a claim. Three routes existed that were not the queue. Buying a senior position from a holder with a '
       'reason to sell. Co-investing in a buyer group. Or waiting for a licence expiry that would improve price '
       'discovery on the deep positions.'),
      ('What it changed',
       'The question the fund brought was whether to enter the queue. The question the scoping produced was which of '
       'four holders would sell, at what price, and which of three structures suited them. That is a four-week '
       'decision and we scoped it as one.')]),
    ('A state that wanted the capability, not the service',
     'A Gulf government. Capability design, 2026.',
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

QUESTION = ('If this government breaks a contract signed under the new hydrocarbons law, what are an investor’s '
            'realistic chances of being paid, and what single event would most improve them within a year?')

ANSWER = ('Low on the current record, and the reason is structural rather than political. Contracts signed under the '
          'new framework have not been tested by an enforcement action, so there is no precedent for what the state '
          'does when challenged. Two things would change that within a year. A first arbitration filing that the '
          'state chooses to answer rather than ignore would establish whether the framework is treated as binding. '
          'And a settlement paid to any existing claimant would be stronger than any statement, because it would '
          'show that clearing claims is worth more to the state than holding them. What would push my estimate down '
          'is a second licensing round issued while existing awards remain unpaid, which would indicate the state '
          'believes it can attract capital without settling.')


def page(intro):
    cards = ''
    for i, (title, context, rows) in enumerate(CARDS, 1):
        body = ''.join(f'<div><span class="eyebrow">{heading}</span><p>{text}</p></div>' for heading, text in rows)
        cards += (f'<article class="worked-example" id="example-{i}"><div class="eyebrow">{i:02d}</div>'
                  f'<h2>{title}</h2><p class="example-context"><em>{context}</em></p>'
                  f'<div class="standards-grid">{body}</div></article>')
    teaser = ('<section class="section container" id="ask-the-desk"><div class="section-heading"><div>'
              '<div class="eyebrow">Put a question to the desk</div>'
              '<h2>It answers from the record, or it tells you it cannot</h2></div>'
              '<p>The desk analyst answers only from the material in front of it. It cites what it used. It does not '
              'hedge. If you ask what would change its mind, it tells you.</p></div><div class="prose-page">'
              f'<p><strong>Question.</strong> {QUESTION}</p>'
              f'<p><strong>Answer, shortened.</strong> {ANSWER}</p></div></section>')
    return intro(
        'Worked examples',
        'Four engagements, described by type',
        'Every one of these is real work. No client is named and no figure from a client document appears. Where a '
        'number carried the argument it has been replaced by the proportion or the direction.'
    ) + '<section class="section container worked-examples">' + cards + '</section>' + teaser
