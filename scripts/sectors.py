"""The commodity traders page.

Government affairs and investors keep their own audience pages, so this is the
only one of the three that needs building here.

Coverage claims must stay honest. Collection runs in Venezuela today and the other
four countries are in build, which is what coverage_page.py says. Nothing here may
imply a live desk in a country where there is not one.

The dated regulatory and market facts were checked against primary sources when
the page was written. If you change a date or a figure, check it again.
"""

SECTORS = {
    'commodities': {
        'name': 'Commodity traders',
        'nav': 'Origination and supply, from the growing zone to the port.',
        'title': 'Food and farming, from the<br>growing zone to the port',
        'description': 'Political and regulatory research for the people who originate, trade and finance '
                       'agricultural commodities in the places where the reporting is thinnest.',
        'standfirst': 'A crop is exposed to the same five things an oilfield is. Who holds the export '
                      'licence and on what condition. Whether the labour turns up. Whether the road to the '
                      'port is open. Which way the politics is turning. What the contract with the '
                      'marketing board actually says.',
        'problem_title': 'The decision is made in a district, not a capital',
        'problem': 'A state board sets a farmgate price. An export licence is suspended in one province. A '
                   'quarantine closes a growing zone. A route to the port is taxed by an armed group. None '
                   'of that reaches a price series until it has already moved the price, and by the time it '
                   'is news your counterparty has been trading on it for weeks. Indonesia announced a palm '
                   'oil export ban on 27 April 2022 that took effect the following day. India banned '
                   'non-basmati rice exports on 20 July 2023 and did not lift it until September 2024. '
                   'Neither was a forecast anyone could buy.',
        'watch': [
            ('Licensing and permits', 'Export licences and registration with a marketing board, '
                                      'phytosanitary certificates, quarantine on an infected zone, and the '
                                      'quotas and minimum export prices that appear with a day of notice.'),
            ('Labour', 'Whether the harvest crew turns up, union action at the plantation or the port, and '
                       'findings of forced or child labour, which close a market rather than a farm.'),
            ('Security', 'Roadblocks and informal taxation between the growing zone and the port, crop '
                         'moving across a border to a better price, and conflict that closes a collection '
                         'route.'),
            ('Political change', 'Export bans and taxes, subsidy and fuel decisions, elections that move a '
                                 'farmgate price, and controls on what an exporter may do with its foreign '
                                 'currency.'),
            ('Contract terms', 'What the board sets, what the pre-export finance obliges, and how an '
                               'offtake or a plantation concession is renegotiated when the government '
                               'changes.'),
        ],
        'audiences': [
            ('asset-watch.html', 'Watch a named origin',
             'Continuous coverage of the growing zones, ports and counterparties you depend on.'),
            ('question-book.html', 'Settle a question with a date',
             'Whether an origin keeps supplying, written so it can actually be answered and scored.'),
        ],
    },
}

REGULATION = (
    '<section class="depth-wash"><div class="container split-depth"><div><div class="eyebrow">Why it is '
    'being bought now</div><h2>The rules now require<br>you to know the district</h2><p>Compliance used to '
    'be satisfied by a country score. It is now satisfied by evidence about a place.</p></div><div>'
    '<p>The EU deforestation regulation covers cattle, cocoa, coffee, palm, rubber, soy and wood. It '
    'applies from 30 December 2026 for large and medium operators, and from 30 June 2027 for micro and '
    'small enterprises, after a second delay agreed at the end of 2025. It asks for the location of the '
    'plot and proof that the crop was legal under the producing country’s own law.</p>'
    '<p>The United States forced labour law has been in force since June 2022 and treats cotton as a '
    'priority sector. Withhold release orders have already closed the US market to named palm oil '
    'producers.</p>'
    '<p>Neither obligation is met by a price series or an index. Both require someone to establish what is '
    'true in a specific place, on a date, with the sources attached.</p></div></div></section>')


def page(intro, slug):
    s = SECTORS[slug]
    watch = ''.join(
        f'<article><span class="depth-number">{i:02}</span><h3>{title}</h3><p>{text}</p></article>'
        for i, (title, text) in enumerate(s['watch'], 1))
    audiences = ''.join(
        f'<a href="{url}"><span>{i:02} / Where to start</span><h3>{label}</h3><p>{text}</p><b></b></a>'
        for i, (url, label, text) in enumerate(s['audiences'], 1))
    body = (
        f'<section class="section container"><div class="section-heading"><div><div class="eyebrow">'
        f'The problem</div><h2>{s["problem_title"]}</h2></div><p>{s["problem"]}</p></div></section>'
        f'<section class="section container"><div class="section-heading"><div><div class="eyebrow">'
        f'What we watch</div><h2>Five things that decide<br>whether it keeps running</h2></div></div>'
        f'<div class="depth-cards">{watch}</div></section>')
    body += REGULATION
    body += (
        '<section class="section container"><div class="section-heading"><div><div class="eyebrow">'
        'Where it matters</div><h2>The countries we open next<br>are farming countries</h2></div>'
        '<p>Colombia is coffee and bananas, with a quarantine running in the banana zones since 2019. '
        'Rwanda licenses and prices coffee and tea through a national board whose trading rules changed '
        'as recently as 2023. Pakistan is cotton, rice and wheat, where a provincial decision on '
        'procurement moves a farmgate price faster than any market does. Mexico is fresh produce, where '
        'the labour mechanisms in the trade agreement now reach agriculture.</p></div>'
        '<div class="container prose-page"><p>Collection runs in Venezuela today. The four countries '
        'above are in build. We will tell you plainly whether we cover where you are exposed before you '
        'buy anything, and we would rather lose the sale than imply a desk that does not exist. '
        '<a href="coverage.html">See where collection stands</a>.</p></div></section>')
    body += (
        f'<section class="section container"><div class="section-heading"><div><div class="eyebrow">'
        f'Where to start</div><h2>Two ways in</h2></div></div>'
        f'<div class="depth-link-grid">{audiences}</div>'
        f'<div class="container prose-page"><p>What you actually receive is set out on '
        f'<a href="services.html">products</a>.</p></div></section>')
    return intro(f'Sectors served / {s["name"]}', s['title'], s['standfirst']) + body
