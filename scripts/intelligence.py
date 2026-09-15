"""Public explanations adapted from the owner's Venezuela product brief.

No recipient details, access links, client thresholds, or live-looking scores.
"""
import html

E = html.escape

RISKS = [
    ('Elite Cohesion', 'Changes in alignment among decision-makers, and what those changes could mean for authority and implementation.'),
    ('Political Order', 'The institutions, rules and policy decisions that shape the operating and contractual environment.'),
    ('Security and Military', 'The use or threat of force, security constraints and their implications for people, access and continuity.'),
    ('Economic and Fiscal Stability', 'Pressure on public finances, payment capacity and the services or infrastructure an asset depends on.'),
    ('Geopolitical and External Pressure', 'External alignments, sanctions decisions and international actions that could change the available options.'),
    ('Social Pressure and Labour', 'Protest, strikes and the living conditions behind them, and whether they are likely to interrupt the workforce, access to a site or the route to port.'),
]


TESTS = [
    ('Rule of law', 'Which protections must work in practice?', 'Relevant rules, enforcement history, procedural access, and the limits identified by qualified advisers.', 'A documented change in enforcement or access to a remedy.'),
    ('Enforceable contracts', 'What protection must the agreement provide?', 'The contract, governing law, dispute process, security arrangements, and specialist assessment of enforceability.', 'A material change in the agreement, its implementation, or the available remedy.'),
    ('Predictable rules', 'How much regulatory uncertainty can the mandate accept?', 'The applicable instruments, decision process, implementation record, and any stated review or expiry dates.', 'A new instrument, an implementation decision, or evidence that practice differs from the published rule.'),
    ('Infrastructure', 'What must be available for the asset to work?', 'Dated evidence on power, transport, inputs, maintenance, and the dependencies specific to the facility.', 'A verified change in a critical service or access route.'),
    ('Credible institutions', 'Which institutions must be able to deliver?', 'Documented authority, resources, counterparties, implementation capacity, and evidence of past performance.', 'A change in authority, capacity, or compliance that affects the decision.'),
    ('Policy continuity', 'How long must the policy position hold?', 'The decision horizon, formal commitments, implementation milestones, and credible routes by which policy could change.', 'A decision or actor change that alters the expected policy path.'),
]


def risk_dimensions():
    rows = ''.join(f'<article><span aria-hidden="true">{i:02}</span><div><h3>{E(name)}</h3><p>{E(copy)}</p></div></article>' for i, (name, copy) in enumerate(RISKS, 1))
    return '''<section class="section container" id="risk-dimensions"><div class="section-heading"><div><div class="eyebrow">The country assessment</div><h2>Six dimensions of the country picture</h2></div><p>A single country score can hide the change that matters to your business. Read these six dimensions separately, then examine their connections.</p></div><div class="risk-dimensions">'''+rows+'''</div><p class="visual-caption">A risk score, a question probability, and a commercial threshold answer different questions. Any numerical reading needs its date, evidence, scale, and uncertainty attached.</p></section>'''


def scenario_framework():
    return '<section class="section container" id="tracked-questions"><p>The scenario layer has been replaced by dated questions with tracked probabilities.</p></section>'


def entry_tests():
    tabs, panels = [], []
    for i, (name, bar, evidence, change) in enumerate(TESTS):
        tabs.append(f'<button role="tab" id="entry-tab-{i}" aria-controls="entry-panel-{i}" aria-selected="{str(i == 0).lower()}" tabindex="{0 if i == 0 else -1}"><span>{i+1:02}</span>{E(name)}</button>')
        panels.append(f'<div class="entry-test-panel" id="entry-panel-{i}" role="tabpanel" aria-labelledby="entry-tab-{i}" {"hidden" if i else ""}><h3>{E(name)}</h3><dl><div><dt>Your requirement</dt><dd>{E(bar)} Agree the threshold with your team.</dd></div><div><dt>The evidence to inspect</dt><dd>{E(evidence)}</dd></div><div><dt>What would trigger a review</dt><dd>{E(change)}</dd></div></dl><a class="text-link" href="briefing.html?test={E(name)}">Discuss this requirement </a></div>')
    return '''<section class="section container" id="entry-tests"><div class="section-heading"><div><div class="eyebrow">The commercial decision</div><h2>Six tests, and your bar for each one</h2></div><p>A country can become more attractive while a particular opportunity still fails your requirements. Set the bar before deciding whether the evidence clears it.</p></div><div class="entry-test-workbench"><div class="entry-test-tabs" role="tablist" aria-label="Explore the six decision tests">'''+''.join(tabs)+'''</div>'''+''.join(panels)+'''</div><p class="visual-caption">This walkthrough explains the questions to ask. It does not disclose a client’s thresholds or assign scores to an actual opportunity.</p></section>'''


def question_families():
    """The six operational families for an energy asset.

    Deliberately not thresholded here. Twenty four hours without power matters
    to one operator and not to another, so the number is set with the client.
    What does not move is that each family resolves on a date against a rule
    agreed before the work starts.
    """
    return ('<section class="section container" id="question-families"><div class="section-heading"><div><div class="eyebrow">The question set</div><h2>Six families of question,<br>written so a date settles them</h2></div><p>These are the operational families for an energy asset. The threshold and the window are set with you, because a day without power matters to one operator and not to another. What does not change is that each one resolves against a rule agreed before the work starts.</p></div><div class="standards-grid"><div><span class="eyebrow">F1</span><h3>Compliance</h3><p>Will the licence, permit or sanctions authorisation the operator works under be amended, revoked, suspended or allowed to lapse?</p></div><div><span class="eyebrow">F2</span><h3>Operations</h3><p>Will the plant lose power, feedstock or a process unit for long enough to interrupt loading?</p></div><div><span class="eyebrow">F3</span><h3>Security</h3><p>Will armed actors, whether state forces or an armed group, deploy at the site, take control of who enters it, or attack the infrastructure and transport it depends on?</p></div><div><span class="eyebrow">F4</span><h3>Community</h3><p>Will access to the site or the route to port be blocked for long enough to hold a shipment?</p></div><div><span class="eyebrow">F5</span><h3>Local politics</h3><p>Will the regional management of the state operator, or the governor of the state, be replaced?</p></div><div><span class="eyebrow">F6</span><h3>Payment</h3><p>Will the operator or its state counterparty fall behind on wages, contractor invoices or supplier payments for long enough that the arrears are sustained and visible?</p></div></div></section>')


def brief_structure():
    return '''<section class="section container"><div class="section-heading"><div><div class="eyebrow">A briefing built for the decision</div><h2>Where it is heading, and whether it clears your bar</h2></div><p>Country direction and commercial viability belong alongside one another. Keep the evidence, the interpretation, and the client’s requirements distinct.</p></div><div class="brief-structure"><a href="venezuela.html#risk-dimensions"><h3>Risk dimensions</h3><p>See which part of the country picture is changing.</p><span>Explore the dimensions </span></a><a href="decision-pathways.html#entry-tests"><h3>Decision tests</h3><p>Assess the opportunity against your own requirements.</p><span>Explore the tests </span></a></div></section>'''
