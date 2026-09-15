"""Public-facing research experiences and reference-inspired homepage sections."""


def hero():
    """The photograph hero supplied in docs/files.zip, with the image served from assets/."""
    return '''<section class="ef-hero"><div class="container">
  <div class="ef-hero-media">
    <div class="ef-hero-photo" role="img" aria-label="An oil export terminal at night, a tanker moored at a jetty, storage tanks and a refinery lit along the shore, with dark open water filling the rest of the frame"></div>
    <svg class="ef-hero-lights" viewBox="0 0 1598 418" preserveAspectRatio="none" aria-hidden="true">
      <defs><radialGradient id="efFound"><stop offset="0" stop-color="#FFD9A8" stop-opacity="0.95"/><stop offset="0.4" stop-color="#F25120" stop-opacity="0.3"/><stop offset="1" stop-color="#F25120" stop-opacity="0"/></radialGradient></defs>
      <g class="ef-found-1"><circle cx="352" cy="300" r="40" fill="url(#efFound)"/><circle cx="352" cy="300" r="3.2" fill="#FFD9A8"/></g>
      <g class="ef-found-2"><circle cx="210" cy="186" r="36" fill="url(#efFound)"/><circle cx="210" cy="186" r="3" fill="#FFD9A8"/></g>
      <g class="ef-found-3"><circle cx="556" cy="352" r="38" fill="url(#efFound)"/><circle cx="556" cy="352" r="3.2" fill="#FFD9A8"/></g>
      <g class="ef-found-4"><circle cx="424" cy="92" r="34" fill="url(#efFound)"/><circle cx="424" cy="92" r="2.8" fill="#FFD9A8"/></g>
      <g class="ef-found-5"><circle cx="736" cy="266" r="34" fill="url(#efFound)"/><circle cx="736" cy="266" r="2.8" fill="#FFD9A8"/></g>
    </svg>
    <div class="ef-hero-copy">
      <h1><span class="ef-l1"><span class="ef-w" style="--w:0">We</span><span class="ef-w" style="--w:1">watch</span><span class="ef-w" style="--w:2">the</span><span class="ef-w" style="--w:3">places</span></span><span class="ef-l2"><span class="ef-w" style="--w:4">nobody</span><span class="ef-w" style="--w:5">is</span><span class="ef-w" style="--w:6">watching</span></span></h1>
    </div>
    <p class="ef-hero-tag"><span class="ef-dot ef-dot-1">&#8230;</span><span class="ef-dot ef-dot-2">&#8230;</span><span class="ef-tag-words">all the time</span></p>
  </div>
</div></section>
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
        ('Who is EchoFrame for?', 'Oil and gas government affairs teams, funds underwriting a political or '
         'counterparty assumption, and commodity traders and large agribusiness and food-security groups with '
         'origination, farmland or livestock exposure in emerging markets. What they have in common is a decision '
         'that turns on somewhere the wires do not cover. Each engagement starts with a defined policy, actor, '
         'counterparty, or asset question.'),
        ('Which countries do you cover?', 'Collection runs in Venezuela. Colombia, Mexico, Rwanda and Pakistan are '
         'being built. Standing up a new country is not starting again, because the method and the questions '
         'travel. Tell us where you operate and we will tell you plainly whether we cover it.'),
        ('What can a private briefing cover?', 'Bring the decision you face, the assets or contracts involved, and '
         'your time horizon. We can discuss a stakeholder brief, a policy milestone note, a thesis-question '
         'register, or another research format suited to that question.'),
        ('How do you know something is true before you send it?', 'Reporting is checked before it is allowed to '
         'count. Who says this, how would they know, and who else confirms it independently. Four outlets running '
         'the same unnamed official is one piece of unconfirmed information, not four. Everything carries the date '
         'it was confirmed and the sourcing beside the claim, so you can check the basis rather than take our word.'),
        ('Can our own people be trained to run this?', 'Yes. The Frame Bureau is the training division. Five '
         'modules take a group from finding and checking material through to writing the call, and the measure of '
         'success is that they can staff their own desk without us in the room.'),
        ('How do we start?', 'Send us a question through the contact form. Share a bounded research question and '
         'the date that matters. Scope, access, and delivery are discussed directly.'),
    ]
    return '''<section class="faq-section container"><div class="eyebrow">A little more context</div><h2>Frequently asked questions.</h2><div class="faq-list">'''+''.join(f'<details><summary>{question}<span aria-hidden="true">+</span></summary><p>{answer}</p></details>' for question,answer in items[:limit])+'''</div><a class="text-link" href="briefing.html">Have a more specific question? Let’s talk </a></section>'''
