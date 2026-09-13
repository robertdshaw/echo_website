"""Public-facing research experiences and reference-inspired homepage sections."""


def hero():
    return '''<section class="power-hero" aria-labelledby="power-title"><div class="container power-hero-inner"><div class="power-copy"><div class="eyebrow">Political intelligence / Material exposure</div><h1 id="power-title" aria-label="Power shifts Exposure follows"><span class="hero-line"><span class="hero-word" style="--word-order:0">Power</span> <span class="hero-word" style="--word-order:1">shifts</span></span><em class="hero-line"><span class="hero-word" style="--word-order:2">Exposure</span> <span class="hero-word" style="--word-order:3">follows</span></em></h1><p>EchoFrame serves oil and gas government affairs teams and distressed-debt and special-situations investors. Venezuela is our lead programme. Our second area is European energy policy.</p><div class="power-actions"><a class="text-link" href="capabilities.html">Tell me more</a></div></div></div>
<div class="container landscape-wrap" id="research-preview"><div class="research-landscape"><img class="power-hero-image" src="assets/energy-horizon.png" alt="" width="1774" height="887" fetchpriority="high"><div class="landscape-caption"><span>THE BIG PICTURE / THE LOCAL DETAIL</span><span>VENEZUELA / LEAD DEVELOPMENT PROGRAMME</span></div></div></div></section>
'''


def formats():
    items = [
        ('☼', 'The stakeholder brief', 'Understand formal authority, documented influence, and the relationships around a decision.', 'government-affairs.html'),
        ('⌁', 'The policy milestone', 'Follow a proposal through the institutions, documents, and decision points that matter.', 'research/following-european-energy-policy.html'),
        ('◎', 'The asset question', 'Bring a country-level narrative down to a specific contract, facility, or operating context.', 'venezuela.html'),
        ('≋', 'The evidence note', 'Keep competing accounts visible. Distinguish repeated reporting from independent confirmation.', 'research/when-sources-disagree.html'),
        ('◇', 'The thesis review', 'Identify the political and operational assumptions that deserve another look.', 'distressed-debt.html'),
        ('', 'The resolution register', 'Give each research question a time horizon, an observable outcome, and an evidence rule.', 'research/questions-that-can-resolve.html'),
    ]
    return '''<section class="formats-section section container"><div class="section-heading"><div><div class="eyebrow">04 / Research with a purpose</div><h2>Research that earns<br>its place in the conversation.</h2></div><p>Six ways to turn a broad concern into useful research. We agree the question, sources, and scope with you.</p></div><div class="format-grid">'''+''.join(f'<a href="{url}" class="format-card"><span class="format-icon" aria-hidden="true">{icon}</span><h3>{title}</h3><p>{text}</p></a>' for icon,title,text,url in items)+'''</div></section>'''


def faq(limit=None):
    items = [
        ('Who is EchoFrame for?', 'Our primary audience is oil and gas government affairs teams and fund managers researching distressed debt and special situations. Each engagement starts with a defined policy, actor, counterparty, or asset question.'),
        ('What can a private briefing cover?', 'Bring the decision you face, the assets or contracts involved, and your time horizon. We can discuss a stakeholder brief, a policy milestone note, a thesis-question register, or another research format suited to that question.'),
        ('What is the status of the Venezuela programme?', 'Venezuela is our lead development programme. Collection and indexing form part of the foundation. The connected event, corroboration, spatial-analysis, and forecasting workflow remains in development. Real, redacted material will be added when it is ready for publication.'),
        ('Can I explore the research before getting in touch?', 'Yes. The intelligence library includes complete research essays, field guides, and programme notes. These explain our reasoning and methods. They are not a live feed or a record of validated forecasts.'),
        ('How do you handle conflicting sources?', 'Our editorial approach keeps the original claim, source, timing, and uncertainty visible. Repeated reporting is not counted as independent confirmation. A disagreement can become a research question rather than being averaged away.'),
        ('How do we start?', 'Request a demo or send us a question through the contact form. Share a bounded research question and the date that matters. Scope, access, and delivery are discussed directly.'),
    ]
    return '''<section class="faq-section container"><div class="eyebrow">A little more context</div><h2>Frequently asked questions.</h2><div class="faq-list">'''+''.join(f'<details><summary>{question}<span aria-hidden="true">+</span></summary><p>{answer}</p></details>' for question,answer in items[:limit])+'''</div><a class="text-link" href="briefing.html">Have a more specific question? Let’s talk </a></section>'''
