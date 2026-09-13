"""A single enquiry form with seven visitor fields and direct email delivery."""


def contact_page():
    return '''<section class="depth-hero contact-intro"><div class="container"><div class="eyebrow">Talk to EchoFrame</div><h1>Tell us what you need to understand.</h1><p>Tell us the decision you face and the evidence you need. We will read it and reply to your work email.</p></div></section>
<section class="contact-layout container"><aside class="contact-aside"><div class="eyebrow">A useful first conversation</div><h2>Your question is our starting point.</h2><p>Describe the policy issue, the asset or the investment question you are working on. Include the deadline and any background that would help us understand what matters to your team.</p><p>We use the first conversation to establish whether the question fits what we collect, what sources it would need and what a useful output would contain.</p><p>Please leave out confidential documents and anything that could identify a protected source.</p></aside>
<form id="briefing-form" class="briefing-form direct-contact-form"><h2 id="briefing-form-title">How can we help?</h2><p class="required-note">Fields marked * are required.</p><div class="enquiry-grid">
<label>Your name *<input name="name" autocomplete="name" required maxlength="120" placeholder="Full name"></label>
<label>Work email *<input name="email" type="email" autocomplete="email" required maxlength="200" placeholder="you@company.com"></label>
<label>Organisation *<input name="organization" autocomplete="organization" required maxlength="160" placeholder="Company or institution"></label>
<label>Your sector *<select name="sector" required><option value="">Select your sector</option><option>Oil &amp; gas</option><option>Distressed debt &amp; special situations</option><option>Energy &amp; infrastructure</option><option>Advisory &amp; research</option><option>Government or public institution</option><option>Other</option></select></label></div>
<label>What decision or question are you working on? *<textarea name="question" rows="3" required maxlength="3000" placeholder="Describe the decision or question you need to understand."></textarea></label>
<label>Anything else that would help<textarea name="details" rows="4" maxlength="3000" placeholder="The asset or market, your deadline, and any non-confidential background."></textarea></label>
<label>How did you find us?<select name="referral"><option>Prefer not to say</option><option>Colleague or professional referral</option><option>LinkedIn</option><option>Search</option><option>Event or publication</option></select></label>
<div class="contact-honeypot" aria-hidden="true"><label>Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label></div>
<p class="contact-privacy"><a href="privacy.html">Read our privacy notice</a>.</p>
<button class="button button-coral send-request" type="submit">Send</button><p id="form-status" role="status" aria-live="polite"></p>
<div id="contact-success" class="contact-success" hidden tabindex="-1"><h3>Your request has been sent</h3><p>We will reply as soon as possible.</p></div>
<noscript><p>This form needs JavaScript. Write to contact@echoframe.co instead.</p></noscript></form></section>'''
