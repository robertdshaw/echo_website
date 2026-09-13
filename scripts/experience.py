"""Public-facing research experiences and reference-inspired homepage sections."""


def hero():
    return '''<section class="power-hero" aria-labelledby="power-title"><div class="container power-hero-inner"><div class="power-copy"><div class="eyebrow">Emerging markets / Continuous collection</div><h1 id="power-title" aria-label="Continuous intelligence from places that only produce snapshots"><span class="hero-line"><span class="hero-word" style="--word-order:0">Continuous</span> <span class="hero-word" style="--word-order:1">intelligence</span> <span class="hero-word" style="--word-order:2">from</span> <span class="hero-word" style="--word-order:3">places</span></span><em class="hero-line"><span class="hero-word" style="--word-order:4">that</span> <span class="hero-word" style="--word-order:5">only</span> <span class="hero-word" style="--word-order:6">produce</span> <span class="hero-word" style="--word-order:7">snapshots</span></em></h1><p>EchoFrame builds a dated, sourced record of what is happening in the parts of emerging markets where information is thin. We pay local newsrooms for the reporting and archives they already have, and check what they report against official records, physical data and markets. Companies and investors use the record to answer questions a one-off report cannot.</p></div></div>
<div class="container landscape-wrap" id="research-preview"><div class="research-landscape"><img class="power-hero-image" src="assets/energy-horizon.png" alt="" width="1774" height="887" fetchpriority="high"><div class="landscape-caption"><span>WHERE THE REPORTING IS THINNEST</span><span>VENEZUELA / THE WORKING PROGRAMME</span></div></div></div></section>
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
        ('What is the status of the Venezuela programme?', 'Venezuela is the working programme. There are two years of archive, a structured event record for the eastern oil states, and a correspondent agreement in progress. Scope and delivery are agreed for each engagement.'),
        ('Can I explore the research before getting in touch?', 'Yes. The four library articles explain source comparison, question design, Venezuela collection priorities and European energy policy research. They do not present a live feed or a validated forecast record.'),
        ('How do you handle conflicting sources?', 'A disagreement becomes a research question rather than being averaged away. We keep both accounts, record what each source was able to observe, and say what evidence would settle it.'),
        ('How do we start?', 'Send us a question through the contact form. Share a bounded research question and the date that matters. Scope, access, and delivery are discussed directly.'),
    ]
    return '''<section class="faq-section container"><div class="eyebrow">A little more context</div><h2>Frequently asked questions.</h2><div class="faq-list">'''+''.join(f'<details><summary>{question}<span aria-hidden="true">+</span></summary><p>{answer}</p></details>' for question,answer in items[:limit])+'''</div><a class="text-link" href="briefing.html">Have a more specific question? Let’s talk </a></section>'''
