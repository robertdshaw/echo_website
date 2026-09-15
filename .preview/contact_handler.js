const briefingForm = document.querySelector('#briefing-form');
if (briefingForm) {
  const status = document.querySelector('#form-status');
  const submit = briefingForm.querySelector('.send-request');
  const success = document.querySelector('#contact-success');
  const fieldsToSend = ['name', 'email', 'organization', 'role', 'sector', 'question', 'details', 'referral', 'website'];
  let token = '';
  let submitting = false;
  let previousPayload = '';
  let requestId = '';
  let accepted = false;
  const audience = new URLSearchParams(location.search).get('audience');
  if (audience === 'government') briefingForm.elements.sector.value = 'Oil & gas';
  if (audience === 'credit') briefingForm.elements.sector.value = 'Distressed debt & special situations';
  async function initialise() {
    const response = await fetch('/api/contact/status', {cache: 'no-store', credentials: 'same-origin', signal: AbortSignal.timeout(15000)});
    if (!response.ok) throw new Error('Sending is temporarily unavailable. Your request has not been sent. Please try again later.');
    const info = await response.json();
    token = info.token || '';
    if (!info.ready || !token) throw new Error('Sending is temporarily unavailable. Your request has not been sent. Please try again later.');
  }
  briefingForm.addEventListener('input', event => event.target.removeAttribute('aria-invalid'));
  briefingForm.addEventListener('submit', async event => {
    event.preventDefault();
    if (submitting || accepted || !briefingForm.reportValidity()) return;
    const fields = Object.fromEntries(fieldsToSend.map(name => [name, briefingForm.elements[name].value.trim()]));
    const payload = JSON.stringify(fields);
    if (payload !== previousPayload) { requestId = crypto.randomUUID(); previousPayload = payload; }
    submitting = true; submit.disabled = true; submit.textContent = 'Sending your request';
    status.textContent = 'Sending your request to EchoFrame.';
    briefingForm.querySelectorAll('[aria-invalid]').forEach(field => field.removeAttribute('aria-invalid'));
    try {
      if (!token) await initialise();
      const response = await fetch('/api/contact', {
        method: 'POST', headers: {'Content-Type': 'application/json'}, credentials: 'same-origin',
        body: JSON.stringify({...fields, token, request_id: requestId}), signal: AbortSignal.timeout(30000)
      });
      const result = await response.json();
      if (!response.ok || !result.ok) {
        if (result.refresh) token = '';
        if (result.fields) {
          const invalid = Object.keys(result.fields);
          invalid.forEach(name => briefingForm.elements[name]?.setAttribute('aria-invalid', 'true'));
          briefingForm.elements[invalid[0]]?.focus();
        }
        throw new Error(result.error || 'We could not confirm delivery. Your details remain in the form.');
      }
      accepted = true; status.textContent = '';
      document.querySelector('#contact-reference').textContent = 'Request reference ' + result.reference;
      success.hidden = false; submit.hidden = true;
      briefingForm.querySelectorAll('input,select,textarea').forEach(field => { field.disabled = true; });
      success.focus();
    } catch (error) {
      status.textContent = error.name === 'TimeoutError' || error instanceof TypeError
        ? 'We could not confirm delivery. Your details remain in the form. Please contact contact@echoframe.co before sending again.'
        : error.message;
    } finally { submitting = false; submit.disabled = accepted; submit.textContent = 'Book a conversation'; }
  });
}
