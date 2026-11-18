"""Where we work. Coverage follows the client's exposure, not a fixed list of countries.

Coverage claims must stay honest. Venezuela is the one running programme. Nothing here
may imply a live desk anywhere else, and the defence work is described as in development
until it is in use.
"""


def page(intro):
    jump = ('<div class="container region-jump"><a href="#how">How coverage is built</a>'
            '<a href="#venezuela">Venezuela</a><a href="#brussels">Brussels</a>'
            '<a href="#defence">Defence and security</a></div>')
    how = ('<section id="how" class="region-detail container"><div>'
           '<div class="eyebrow">How coverage is built</div><h2>Around your question.</h2>'
           '<p>Exposure usually sits far from the capital, in places where reporting is thin and nobody is watching '
           'between one commissioned report and the next. We find the local newsrooms that already know the ground, '
           'license their archive, and set up collection for the places that matter to you.</p>'
           '<p>We work across Latin America, Africa and South Asia, for clients in energy, life sciences and '
           'finance. Tell us where you operate and we will tell you plainly whether we cover it, and what it would '
           'take if we do not yet.</p>'
           '</div></section>')
    venezuela = ('<section id="venezuela" class="region-detail container"><div>'
                 '<div class="eyebrow"><span class="status-dot orange"></span> Longest-running programme</div>'
                 '<h2>Venezuela.</h2>'
                 '<p>Venezuela is the working programme. Two years of archive, a structured event record for the '
                 'eastern oil states, and a correspondent agreement in progress.</p>'
                 '<p>Collection sits in the oil states of the east and the west, outside the capital, where the '
                 'exposure is largest and the reporting is thinnest. Scope, delivery and access are agreed for each '
                 'engagement.</p>'
                 '</div></section>')
    brussels = ('<section id="brussels" class="region-detail container"><div>'
                '<div class="eyebrow">The same method on a different record</div>'
                '<h2>European energy and regulatory policy.</h2>'
                '<p>It looks like a different business and it is not. In Venezuela the problem is that almost nothing '
                'is written down. In Brussels the problem is that everything is, continuously, in volumes no team can '
                'read. Both are the same failure, which is a public record that exists but cannot be used as a '
                'record. One is scarcity and one is volume.</p>'
                '<p>The tracker is available to clients on request.</p>'
                '</div></section>')
    defence = ('<section id="defence" class="region-detail container"><div>'
               '<div class="eyebrow">Defence and security</div><h2>Decision support for planners.</h2>'
               '<p>For defence and security institutions we are developing decision support for planning around '
               'energy and critical infrastructure in contested environments. A person stays in command of every '
               'decision, and each prediction and suggested option can be traced back to the sources behind it.</p>'
               '<p>We are developing it with TALISMAN, a Paris crisis-communications and strategic-advisory firm '
               'active in defence and security. TALISMAN will co-design the operational scenario the system is tested '
               'on, and will run the table-top exercise that shows whether planners find its output useful and '
               'trustworthy.</p>'
               '<p>This work is in development. We will say so here until it is in use.</p>'
               '</div></section>')
    return intro(
        'Where we work', 'We work where our clients are exposed',
        'Coverage is built around your question, not around a fixed list of countries.'
    ) + jump + how + venezuela + brussels + defence
