"""Regional coverage. One programme live, one in build, four countries next."""
from html import escape as E

NEXT_COUNTRIES = [
    ('Colombia',
     'Ten years of work on the country and contacts across energy, infrastructure, finance and media, with coca, '
     'mining and pipeline exposure concentrated in departments the national press barely covers.'),
    ('Mexico',
     'Energy and industrial investment spread across states where security and local politics decide whether a '
     'project runs, and where reporting outside Mexico City is thin and often dangerous.'),
    ('Rwanda',
     'A regional hub for mining and logistics into eastern Congo, where the questions that matter to an investor sit '
     'on the other side of a border and almost nothing is reported in either country.'),
    ('Pakistan',
     'Infrastructure and energy corridors running through provinces where the security picture changes by district '
     'and national coverage stops at the provincial capital.'),
]


def page(intro):
    countries = ''.join(f'<li><h3>{E(name)}</h3><p>{E(reason)}</p></li>' for name, reason in NEXT_COUNTRIES)
    jump = ('<div class="container region-jump"><a href="#live">Live</a>'
            '<a href="#in-build">In build</a><a href="#next">Next</a></div>')
    live = ('<section id="live" class="region-detail container"><div>'
            '<div class="eyebrow"><span class="status-dot orange"></span> Live</div><h2>Venezuela.</h2>'
            '<p>Venezuela is the working programme. Two years of archive, a structured event record for the eastern '
            'oil states, and a correspondent agreement in progress.</p>'
            '<p>Collection sits in the oil states of the east and the west, outside the capital, where the exposure '
            'is largest and the reporting is thinnest. Scope, delivery and access are agreed for each engagement.</p>'
            '</div></section>')
    in_build = ('<section id="in-build" class="region-detail container"><div><div class="eyebrow">In build</div>'
                '<h2>European energy and regulatory policy.</h2>'
                '<p>It looks like a different business and it is not. In Venezuela the problem is that almost nothing '
                'is written down. In Brussels the problem is that everything is, continuously, in volumes no team can '
                'read. Both are the same failure, which is a public record that exists but cannot be used as a '
                'record. One is scarcity and one is volume.</p>'
                '<p>The tracker is available to clients on request.</p>'
                '</div></section>')
    nxt = ('<section id="next" class="region-detail container"><div><div class="eyebrow">Next</div>'
           '<h2>Four countries.</h2>'
           '<p>Each is chosen for the same three reasons. Real capital exposure outside the capital, thin local '
           'reporting, and a standing relationship we can build the collection on.</p></div>'
           '</section><div class="container"><section class="coverage-coming" aria-labelledby="coming-coverage-title">'
           '<h2 id="coming-coverage-title" class="visually-hidden">The countries next in the programme</h2>'
           f'<ul>{countries}</ul></section></div>')
    return intro(
        'Regional coverage', 'Where we collect, and where we go next',
        'One programme is running, one is being built, and four countries follow. Each is chosen for where the '
        'exposure sits rather than for where the reporting is already easy.'
    ) + jump + live + in_build + nxt
