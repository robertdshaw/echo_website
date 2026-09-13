"""Public explanations adapted from the owner's Venezuela product brief.

No recipient details, access links, client thresholds, or live-looking scores.
"""
import html

E = html.escape

LAYERS = [
    ('NLP & entity recognition', 'Turn reporting into events you can examine',
     'Identify the people, organisations, places, and actions in a report. Keep the original source beside the extracted event, so an analyst can check what the text actually establishes.',
     'A statement that a terminal is open becomes a claim about a named place, activity, and time. It does not become proof that operations are normal.'),
    ('Network analysis', 'Follow the relationships behind the decision',
     'Connect documented authority, ownership, sanctions, and operating relationships. A useful graph shows the evidence for a connection and distinguishes a formal role from inferred influence.',
     'An approval may involve a national ministry, a local authority, and a service provider. Map the dependencies before deciding which relationship matters most.'),
    ('Drama theory', 'Ask whether a threat or promise is credible',
     'Examine what each actor wants, what they threaten and what would make another actor comply. Compare the declared position with the options actually available.',
     'A threatened withdrawal matters differently when the actor has an alternative buyer, a financial constraint, or allies unwilling to follow.'),
    ('Bayesian inference', 'Let evidence change the probability assessment',
     'Start with a clearly defined question and an initial probability. Assess how the new evidence changes the likelihood of its outcome, then record the reason for any revision.',
     'Several reports repeating one announcement are one evidentiary chain. Treating them as independent updates would create false confidence.'),
    ('Revealed preference', 'Identify the criteria behind previous decisions',
     'With the client, examine previous entries, declines, and stated constraints. Use that record to propose decision criteria, then confirm which requirements apply to the opportunity at hand.',
     'Past decisions may suggest a minimum requirement for contract protection or access. They do not establish a universal threshold, or replace the client’s current mandate.'),
]

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


def analytical_layers():
    items = ''.join(f'<article><span class="eyebrow">Layer {i:02}</span><h3>{E(name)}</h3><p class="layer-claim">{E(claim)}</p><p>{E(copy)}</p></article>' for i, (name, claim, copy, example) in enumerate(LAYERS, 1))
    return '<section class="section container" id="analytical-layers"><div class="section-heading"><div><div class="eyebrow">Five analytical layers</div><h2>Different lenses<br>One evidence record</h2></div><p>Each layer asks a different question of the same material. The value lies in seeing how the interpretation was reached and where it could be wrong.</p></div><div class="analytical-layers">'+items+'</div></section>'


def evidence_flow():
    return '''<section class="section container evidence-flow-section"><div class="eyebrow">The assessment process</div><h2>How evidence moves the assessment</h2><figure class="judgment-flow"><div class="judgment-stage"><span>01 / Observe</span><strong>Reports are organised<br>into event records</strong><p>Source, actor, place, time, and competing accounts.</p></div><div class="judgment-stage"><span>02 / Interpret</span><strong>Relationships and<br>behaviour add context</strong><p>Authority, incentives, dependencies, and alternatives.</p></div><div class="judgment-stage"><span>03 / Reassess</span><strong>Assessments are compared<br>with the client’s criteria</strong><p>What changed, what it means, and what needs review.</p></div><figcaption>Analytical workflow illustration. Arrows describe the reasoning sequence; they do not represent data volumes or live feeds.</figcaption></figure></section>'''


def risk_dimensions():
    rows = ''.join(f'<article><span aria-hidden="true">{i:02}</span><div><h3>{E(name)}</h3><p>{E(copy)}</p></div></article>' for i, (name, copy) in enumerate(RISKS, 1))
    return '''<section class="section container" id="risk-dimensions"><div class="section-heading"><div><div class="eyebrow">The country assessment</div><h2>Six dimensions<br>A more useful risk picture</h2></div><p>A single country score can hide the change that matters to your business. Read these six dimensions separately, then examine their connections.</p></div><div class="risk-dimensions">'''+rows+'''</div><p class="visual-caption">A risk score, a question probability, and a commercial threshold answer different questions. Any numerical reading needs its date, evidence, scale, and uncertainty attached.</p></section>'''


def scenario_framework():
    return '<section class="section container" id="tracked-questions"><p>The scenario layer has been replaced by dated questions with tracked probabilities.</p></section>'


def entry_tests():
    tabs, panels = [], []
    for i, (name, bar, evidence, change) in enumerate(TESTS):
        tabs.append(f'<button role="tab" id="entry-tab-{i}" aria-controls="entry-panel-{i}" aria-selected="{str(i == 0).lower()}" tabindex="{0 if i == 0 else -1}"><span>{i+1:02}</span>{E(name)}</button>')
        panels.append(f'<div class="entry-test-panel" id="entry-panel-{i}" role="tabpanel" aria-labelledby="entry-tab-{i}" {"hidden" if i else ""}><h3>{E(name)}</h3><dl><div><dt>Your requirement</dt><dd>{E(bar)} Agree the threshold with your team.</dd></div><div><dt>The evidence to inspect</dt><dd>{E(evidence)}</dd></div><div><dt>What would trigger a review</dt><dd>{E(change)}</dd></div></dl><a class="text-link" href="briefing.html?test={E(name)}">Discuss this requirement </a></div>')
    return '''<section class="section container" id="entry-tests"><div class="section-heading"><div><div class="eyebrow">The commercial decision</div><h2>Six tests<br>Your bar for each one</h2></div><p>A country can become more attractive while a particular opportunity still fails your requirements. Set the bar before deciding whether the evidence clears it.</p></div><div class="entry-test-workbench"><div class="entry-test-tabs" role="tablist" aria-label="Explore the six decision tests">'''+''.join(tabs)+'''</div>'''+''.join(panels)+'''</div><p class="visual-caption">This walkthrough explains the questions to ask. It does not disclose a client’s thresholds or assign scores to an actual opportunity.</p></section>'''


def hard_questions():
    return '''<section class="section container hard-questions"><div class="eyebrow">Reviewing an assessment</div><h2>No soft answers</h2><p class="depth-lead">Ask what supports the judgment, what challenges it, and what would change the answer. A useful briefing should be able to show its reasoning.</p><div class="faq-list"><details><summary>What would make you change your mind?<span aria-hidden="true">+</span></summary><p>Name the observation, the relevant question, and the reason it would change the assessment. Set a review date. If the evidence is insufficient, say what is missing.</p></details><details><summary>Does lower country risk mean the opportunity is viable?<span aria-hidden="true">+</span></summary><p>Not necessarily. Country direction and commercial readiness are separate judgments. Test the particular contract, operating dependencies, and institutional requirements against the client’s criteria.</p></details><details><summary>How do we know the method adds value?<span aria-hidden="true">+</span></summary><p>Agree what a first briefing must demonstrate. For forecast performance, inspect dated forecasts, revisions, outcomes, and a consistent benchmark across the record, including unsuccessful calls.</p></details></div></section>'''


def brief_structure():
    return '''<section class="section container"><div class="section-heading"><div><div class="eyebrow">A briefing built for the decision</div><h2>Where it is heading<br>Whether it clears your bar</h2></div><p>Country direction and commercial viability belong alongside one another. Keep the evidence, the interpretation, and the client’s requirements distinct.</p></div><div class="brief-structure"><a href="capabilities.html#risk-dimensions"><strong>06</strong><h3>Risk dimensions</h3><p>See which part of the country picture is changing.</p><span>Explore the dimensions </span></a><a href="decision-pathways.html#entry-tests"><strong>06</strong><h3>Decision tests</h3><p>Assess the opportunity against your own requirements.</p><span>Explore the tests </span></a></div></section>'''


def forecast_case():
    return '''<section class="section container forecast-case" id="forecast-case"><div class="section-heading"><div><div class="eyebrow">Selected historical assessment / EchoFrame’s account</div><h2>A view formed<br>before the outcome</h2></div><p>A short summary of a private client assessment. The client and the underlying document remain confidential.</p></div><div class="forecast-record"><article><div class="eyebrow">The assessment / 2 December 2025</div><strong class="forecast-number">74%</strong><h3>Combined probability of coercive outcomes</h3><p>EchoFrame reports that its assessment assigned this combined probability to coercive outcomes. This was an aggregate across outcome categories, not a 74% probability assigned specifically to Maduro’s capture.</p></article><article><div class="eyebrow">The subsequent event / 3 January 2026</div><strong class="forecast-number">32 days</strong><h3>From assessment to capture</h3><p>U.S. forces captured Nicolás Maduro on 3 January 2026. The dates place that event 32 days after the assessment described by EchoFrame.</p><a class="text-link" href="https://www.govinfo.gov/content/pkg/CDOC-119hdoc124/pdf/CDOC-119hdoc124.pdf" target="_blank" rel="noopener noreferrer">Read the official account of the operation </a></article></div><div class="forecast-meaning"><h3>What this asks of your next briefing</h3><p>Look beyond a single expected outcome. Ask which alternative paths deserve attention, which actors could change the balance, and which observations would require a new assessment. That is the method to examine before your next decision.</p><p class="visual-caption">The probability is drawn from EchoFrame’s account of its private assessment; the original record is not published here. The official source supports the subsequent event, not the forecast claim. One selected case does not establish calibration or a complete performance record.</p><a class="text-link" href="briefing.html?region=Venezuela&amp;format=Scoping%20conversation">Discuss the reasoning behind the assessment </a></div></section>'''
