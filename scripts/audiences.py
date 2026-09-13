"""Audience journeys and policy-to-capital research interactions."""
from intelligence import brief_structure


def perspectives():
    return '''<section class="perspectives-section container" id="perspectives"><div class="section-heading"><div><div class="eyebrow">The decision on your desk</div><h2>Different stakes.<br><em>The same need for clarity.</em></h2></div><p>A government affairs team and an investment manager may follow the same event for different reasons. Start with the decision you face.</p></div><div class="perspective-tabs" role="tablist" aria-label="Choose your professional perspective"><button role="tab" id="perspective-government" aria-controls="perspective-panel-government" aria-selected="true" tabindex="0"><span class="perspective-tab-number">01</span><span>Government affairs<small>Oil & gas companies</small></span></button><button role="tab" id="perspective-credit" aria-controls="perspective-panel-credit" aria-selected="false" tabindex="-1"><span class="perspective-tab-number">02</span><span>Distressed debt<small>Hedge funds & special situations</small></span></button></div>
<div class="perspective-panel" role="tabpanel" id="perspective-panel-government" aria-labelledby="perspective-government"><div class="perspective-story"><span class="eyebrow">For the people navigating the policy environment</span><h3>Read the power<br>behind the policy.</h3><p>Connect national decisions to regional authorities, operating assets, and the relationships that determine what happens next.</p><div class="perspective-themes"><span>Stakeholder influence</span><span>Policy milestones</span><span>Asset access</span></div><a class="button" href="government-affairs.html">Explore government affairs </a></div><div class="mandate-brief"><div class="mandate-top"><span>THE RESEARCH MANDATE</span><span>01 / GOVERNMENT AFFAIRS</span></div><h4>“Who can change the conditions<br>around our asset?”</h4><div class="mandate-row"><span>Map the decision</span><p>Formal authority, local influence, and the next institutional milestone.</p></div><div class="mandate-row"><span>Test the position</span><p>Compare official statements with local evidence and implementation.</p></div><div class="mandate-row"><span>Prepare the briefing</span><p>A sourced view of the key people, questions for your next meeting, and a date to revisit the findings.</p></div><div class="mandate-note"><span class="signal-light"></span> Illustrative brief scope · Tailored through a research conversation</div></div></div>
<div class="perspective-panel" role="tabpanel" id="perspective-panel-credit" aria-labelledby="perspective-credit" hidden><div class="perspective-story"><span class="eyebrow">For the people underwriting uncertainty</span><h3>See the politics<br>behind the paper.</h3><p>Examine the political and operational assumptions behind a distressed-debt investment. Follow the actors, documents, and developments that could warrant another look.</p><div class="perspective-themes"><span>Political catalysts</span><span>Counterparty context</span><span>Recovery assumptions</span></div><a class="button" href="distressed-debt.html">Explore distressed-debt research </a></div><div class="mandate-brief mandate-credit"><div class="mandate-top"><span>THE RESEARCH MANDATE</span><span>02 / DISTRESSED DEBT</span></div><h4>“What could change the political<br>assumptions in our thesis?”</h4><div class="mandate-row"><span>Define the catalyst</span><p>A named actor, decision, or documentary milestone with a clear horizon.</p></div><div class="mandate-row"><span>Challenge the narrative</span><p>Test counterparty statements against independent evidence and operating context.</p></div><div class="mandate-row"><span>Bring it to committee</span><p>A thesis-question register, contradictory evidence, and the next verification step.</p></div><div class="mandate-note"><span class="signal-light"></span> Illustrative brief scope · Research scope agreed before commissioning</div></div></div></section>'''


def consequence_section():
    return '''<section class="consequence-section"><div class="container"><div class="section-heading"><div><div class="eyebrow">The chain of consequence</div><h2>One development.<br><em>More than one exposure.</em></h2></div><p>Explore the same fictional situation through three research questions. Each connection needs evidence.</p></div><div class="consequence-flow" role="group" aria-label="Explore an illustrative chain of consequence"><button data-consequence="policy" aria-pressed="true"><span>01 / THE DECISION</span><strong>A policy process<br>changes direction.</strong><i aria-hidden="true"></i></button><button data-consequence="asset" aria-pressed="false"><span>02 / THE ASSET</span><strong>Operating assumptions<br>come under review.</strong><i aria-hidden="true"></i></button><button data-consequence="capital" aria-pressed="false"><span>03 / THE THESIS</span><strong>Capital assumptions<br>need a fresh test.</strong><i aria-hidden="true"></i></button></div><div class="consequence-detail" aria-live="polite"><span class="eyebrow" id="consequence-kicker">Government affairs / The decision pathway</span><div><h3 id="consequence-title">Who has authority—and what happens next?</h3><p id="consequence-text">Identify the issuing institution, the formal status of its proposal, and the next decision point. Separate a public position from an implemented measure.</p><a id="consequence-link" class="text-link" href="government-affairs.html">Explore this research perspective </a></div></div><div class="consequence-footnote"><span>ILLUSTRATIVE RESEARCH FRAMEWORK</span><span>No real policy event, issuer, security, or forecast is represented.</span></div></div></section>'''


AUDIENCES = {
    'government': {
        'slug': 'government-affairs',
        'label': 'Oil & gas / Government affairs',
        'title': 'Judgment you can<br><em>defend to a board</em>',
        'description': 'Political intelligence for government affairs teams navigating the connections between policy, stakeholders, and operating assets.',
        'question': 'Which decisions and relationships could change the conditions around our asset?',
        'lead': 'Permission on paper is only half the story',
        'lead_text': 'An announcement tells you what an institution intends. To understand what it means for your asset, trace who must act, which conditions remain, and what evidence would show that implementation has begun.',
        'themes': [('The decision pathway', 'Who has formal authority, who can influence implementation, and which institutional milestone comes next?'), ('The stakeholder landscape', 'Which documented roles, public positions, and local relationships matter to the question?'), ('The operating context', 'How do official statements compare with evidence about access, labour, community concerns, or implementation?')],
        'outputs': [('Stakeholder brief', 'A map of documented roles and positions, with source dates and unresolved relationships.'), ('Policy milestone note', 'The relevant documents, formal status, next decision point, and questions requiring specialist review.'), ('Asset-context brief', 'Local observations, competing accounts, and the implications to investigate for the operating footprint.')],
        'prompt': 'What are the three decisions over the next twelve months that depend on the policy environment around your assets?',
        'cta': 'Discuss a government affairs brief',
        'reading': [('mapping-power-without-false-precision', 'A better map of who matters.'), ('following-european-energy-policy', 'Policy is a process. Track the whole chain.'), ('when-sources-disagree', 'When the accounts do not add up.')]
    },
    'credit': {
        'slug': 'distressed-debt',
        'label': 'Hedge funds / Distressed debt & special situations',
        'title': 'The opportunity has to<br><em>clear your bar</em>',
        'description': 'Research for fund managers examining the political, counterparty, and operational assumptions behind a distressed-debt thesis.',
        'question': 'Which observable developments would make us revisit the political assumptions in this thesis?',
        'lead': 'Find the political assumption in your thesis',
        'lead_text': 'Take one expectation from the investment case: access will improve, a counterparty will perform, or a political decision will arrive on time. Define the observable event behind it, then seek evidence that could challenge it as well as support it.',
        'themes': [('The political catalyst', 'Which named decision, actor, or institutional milestone matters, and over what horizon?'), ('The counterparty narrative', 'Which statements are supported by documents and independent observations—and where do accounts diverge?'), ('The recovery assumptions', 'Which political or operational assumptions need evidence, and which questions belong with legal or valuation specialists?')],
        'outputs': [('Thesis-question register', 'Clear questions, deadlines, and the evidence needed to answer them—with unresolved assumptions kept in view.'), ('Catalyst and counterparty brief', 'Relevant actors, documentary milestones, competing accounts, and a record of what has changed.'), ('Asset viability note', 'Documented criteria and missing evidence, kept separate from security valuation or legal conclusions.')],
        'prompt': 'Which political or operational assumption in your thesis would be most costly to leave untested?',
        'cta': 'Discuss a distressed-debt brief',
        'reading': [('questions-that-can-resolve', 'Give the question a deadline.'), ('sanctions-and-operational-reality', 'A sanctions headline is only the starting point.'), ('venezuela-from-country-to-asset', 'Venezuela, at the level of the asset.')]
    }
}


from depth import audience_depth


def proof_scope(key):
    if key == 'government':
        title = 'Bring one asset, not your entire agenda'
        copy = 'We can scope a first briefing around the decision that matters most: who holds authority, what still has to happen, and which local evidence would establish a change.'
        test = 'Judge the proposed work by whether it gives your team a sourced view of the decision, clear gaps to investigate, and sharper questions for the next meeting.'
        url, label = 'sample-asset-access.html', 'Inspect the fictional asset-access brief'
    else:
        title = 'Put one assumption under scrutiny'
        copy = 'We can scope a first briefing around a political or operational expectation in your thesis. Agree the time horizon, the competing explanations, and the evidence that would warrant a review.'
        test = 'Judge the proposed work by whether it makes that assumption testable and the reasoning traceable. Valuation, legal conclusions, and investment decisions remain with your team and advisers.'
        url, label = 'sample-thesis-review.html', 'Inspect the fictional thesis-review brief'
    return f'<section class="section container proof-scope"><div class="eyebrow">How to assess the fit</div><h2>{title}</h2><p>{copy}</p><p>{test}</p><a class="text-link" href="{url}">{label} </a></section>'


def audience_page(key):
    a=AUDIENCES[key]
    themes=''.join(f'<article><span class="eyebrow">0{i} / Research question</span><h3>{title}</h3><p>{text}</p></article>' for i,(title,text) in enumerate(a['themes'],1))
    outputs=''.join(f'<article><span class="output-index">0{i}</span><div><h3>{title}</h3><p>{text}</p></div></article>' for i,(title,text) in enumerate(a['outputs'],1))
    reading=''.join(f'<a href="research/{slug}.html"><span>{title}</span></a>' for slug,title in a['reading'])
    return f'''<section class="audience-hero audience-{key}"><div class="container"><div class="eyebrow">{a['label']}</div><h1>{a['title']}</h1><p>{a['description']}</p><a class="button button-coral" href="briefing.html?audience={key}">{a['cta']} </a><div class="audience-hero-caption"><span>POLICY  ACTORS  ASSETS  EXPOSURE</span><span>RESEARCH WITH A DEFINED MANDATE</span></div></div><div class="audience-hero-orbits" aria-hidden="true"><i></i><i></i><i></i></div></section><section class="section container"><div class="audience-opening"><div><div class="eyebrow">Your question, in focus</div><h2>{a['lead']}</h2><p>{a['lead_text']}</p></div><blockquote>{a['question']}<cite>AN ILLUSTRATIVE RESEARCH MANDATE</cite></blockquote></div><div class="audience-themes">{themes}</div></section><section class="audience-outputs"><div class="container"><div><div class="eyebrow">A briefing with substance</div><h2>What a focused<br><em>mandate can cover.</em></h2><p>These are possible research formats. Scope, source access, and delivery are agreed in a briefing conversation.</p></div><div class="outputs-list">{outputs}</div></div></section><section class="section container audience-programme"><div><div class="eyebrow">Lead development programme</div><h2>Venezuela.<br><em>Closer to the asset.</em></h2><p>Explore the five risk dimensions, scenario framework, and six decision tests alongside an anonymised historical assessment and fictional asset-level examples.</p><a class="text-link" href="venezuela.html">Inside the Venezuela programme </a></div><div class="audience-reading"><span class="eyebrow">Start with the research</span>{reading}</div></section>{brief_structure()}{audience_depth(key)}{proof_scope(key)}<section class="audience-close"><div class="container"><div class="eyebrow">Start with the question that matters</div><h2>{a['prompt']}</h2><a class="button button-coral" href="briefing.html?audience={key}">See how we can help you </a><p>Tell us your decision and what you would need to see to judge whether our research is useful.</p></div></section>'''
