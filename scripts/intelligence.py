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
    ('Social', ''),
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


def brief_structure():
    return '''<section class="section container"><div class="section-heading"><div><div class="eyebrow">A briefing built for the decision</div><h2>Where it is heading, and whether it clears your bar</h2></div><p>Country direction and commercial viability belong alongside one another. Keep the evidence, the interpretation, and the client’s requirements distinct.</p></div><div class="brief-structure"><a href="decision-pathways.html#entry-tests"><strong>06</strong><h3>Decision tests</h3><p>Assess the opportunity against your own requirements.</p><span>Explore the tests </span></a></div></section>'''
