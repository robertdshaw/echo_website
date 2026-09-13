"""A single enquiry form with eight visitor fields and direct email delivery."""


def contact_page():
    return '''<section class="depth-hero contact-intro"><div class="container"><div class="eyebrow">Talk to EchoFrame</div><h1>Tell us what you need<br>to understand.</h1><p>Tell us the decision you face and the evidence you need. We will review your request and reply using your work email.</p></div></section>
<section class="contact-layout container"><aside class="contact-aside"><div class="eyebrow">A useful first conversation</div><h2>Your question.<br>Our starting point.</h2><p>Describe the policy issue, asset or investment question you are working on. Include the deadline and any background that would help us understand what matters to your team.</p><p>We use the first conversation to establish whether the question fits our research, what sources it needs and what a useful output would contain.</p><p>Please leave out confidential documents and information that could identify a protected source.</p></aside>
<form id="briefing-form" class="briefing-form direct-contact-form"><h2 id="briefing-form-title">How can we help?</h2><p class="required-note">Fields marked * are required.</p><div class="enquiry-grid">
<label>Your name *<input name="name" autocomplete="name" required maxlength="120" placeholder="Full name"></label>
<label>Work email *<input name="email" type="email" autocomplete="email" required maxlength="200" placeholder="you@company.com"></label>
<label>Organisation *<input name="organization" autocomplete="organization" required maxlength="160" placeholder="Company or institution"></label>
<label>Your role<input name="role" autocomplete="organization-title" maxlength="160" placeholder="Role or team"></label></div>
<label>Your sector *<select name="sector" required><option value="">Select your sector</option><option>Oil &amp; gas</option><option>Distressed debt &amp; special situations</option><option>Energy &amp; infrastructure</option><option>Advisory &amp; research</option><option>Other</option></select></label>
<label>What decision or question are you working on? *<textarea name="question" rows="3" required maxlength="3000" placeholder="Describe the decision or question you need to understand."></textarea></label>
<label>Additional details<textarea name="details" rows="4" maxlength="3000" placeholder="Include the asset or market, your deadline and any non-confidential background."></textarea></label>
<label>How did you find us?<select name="referral"><option>Prefer not to say</option><option>Colleague or professional referral</option><option>LinkedIn</option><option>Search</option><option>Event or publication</option></select></label>
<div class="contact-honeypot" aria-hidden="true"><label>Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label></div>
<p class="contact-privacy">Your request and the details you provide will be emailed to contact@echoframe.co so we can respond. <a href="privacy.html">Read our privacy notice</a>.</p>
<button class="button button-coral send-request" type="submit">Book a conversation</button><p id="form-status" role="status" aria-live="polite"></p>
<div id="contact-success" class="contact-success" hidden tabindex="-1"><h3>Your request is on its way</h3><p>Our email service has accepted your request for contact@echoframe.co. We will reply using the work email you provided.</p><p id="contact-reference"></p></div>
<noscript><p>JavaScript is needed to submit this form. You can reach us at contact@echoframe.co.</p></noscript></form></section>'''
