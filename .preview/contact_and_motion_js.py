from pathlib import Path
p=Path('assets/site.js'); s=p.read_text(encoding='utf-8')
start=s.index("const briefingForm = document.querySelector('#briefing-form');")
end=s.index('// The interactive workbenches',start)
replacement=r'''const briefingForm = document.querySelector('#briefing-form');
if (briefingForm) {
  const params = new URLSearchParams(location.search);
  const status = document.querySelector('#form-status');
  const submit = briefingForm.querySelector('.send-request');
  const fallback = document.querySelector('#contact-fallback');
  const draft = document.querySelector('#email-draft');
  const success = document.querySelector('#contact-success');
  let token = '';
  let submitting = false;
  let previousPayload = '';
  let requestId = '';
  function newId() { return crypto.randomUUID(); }
  for (const name of ['region','format']) {
    if ([...briefingForm.elements[name].options].some(option => option.value === params.get(name))) briefingForm.elements[name].value = params.get(name);
  }
  const audiencePresets = {
    government: ['Oil & gas government affairs','Your government affairs brief.','Tell us about the policy decision, stakeholder meeting, or operating asset you are working on.'],
    credit: ['Distressed debt / hedge fund','Your distressed-debt research brief.','Tell us which political or operating assumption you want to examine, and when it matters to your investment decision.']
  };
  const preset = audiencePresets[params.get('audience')];
  if (preset) {
    briefingForm.elements.perspective.value = preset[0];
    document.querySelector('#briefing-form-title').textContent = preset[1];
    document.querySelector('#audience-context').textContent = preset[2];
    document.querySelector('#audience-context').hidden = false;
  }
  if (params.has('audience') || params.has('format') || params.has('region')) briefingForm.querySelector('.optional-context').open = true;
  if (params.get('kind') === 'contact') briefingForm.elements.request_type.value = 'Contact request';
  const labels = {request_type:'Request type',name:'Full name',email:'Work email',organization:'Organisation',role:'Role / team',headquarters:'Location',phone:'Phone',question:'Message',region:'Region',perspective:'Perspective',subject:'Asset, contract, or place',deadline:'Deadline',format:'Research format',referral:'How I found EchoFrame'};
  function readFields() {
    const data = Object.fromEntries(new FormData(briefingForm));
    return Object.fromEntries(Object.entries(data).map(([key,value]) => [key,String(value).trim()]));
  }
  function updateDraft() {
    const values = readFields();
    const text = 'Hello EchoFrame,\n\n'+Object.entries(labels).map(([key,label]) => `${label}: ${values[key] || 'Not specified'}`).join('\n')+'\n';
    draft.href = `mailto:contact@echoframe.co?subject=${encodeURIComponent('EchoFrame '+values.request_type)}&body=${encodeURIComponent(text)}`;
  }
  function buttonLabel() { submit.innerHTML = (briefingForm.elements.request_type.value === 'Demo request' ? 'Send demo request' : 'Send contact request')+' <span aria-hidden="true">↗</span>'; }
  briefingForm.addEventListener('input', event => { event.target.removeAttribute('aria-invalid'); updateDraft(); });
  briefingForm.addEventListener('change', () => { if (!submitting) buttonLabel(); updateDraft(); });
  async function initialise() {
    try {
      const response = await fetch('/api/contact/status',{cache:'no-store',credentials:'same-origin'});
      if (!response.ok) throw new Error('Unavailable');
      const info = await response.json(); token = info.token || '';
      if (!info.ready) {
        status.textContent = 'Direct sending is being connected. You can fill in your details and use the email link below in the meantime.';
        fallback.hidden = false;
      }
    } catch {
      status.textContent = 'Direct sending is temporarily unavailable. You can use the email link below with your details.';
      fallback.hidden = false;
    }
  }
  briefingForm.addEventListener('submit', async event => {
    event.preventDefault();
    if (submitting || !briefingForm.reportValidity()) return;
    const fields = readFields();
    const payload = JSON.stringify(fields);
    if (payload !== previousPayload) { requestId = newId(); previousPayload = payload; }
    submitting = true; submit.disabled = true; submit.textContent = 'Sending your request…';
    status.textContent = 'Sending securely to EchoFrame…'; fallback.hidden = true;
    briefingForm.querySelectorAll('[aria-invalid]').forEach(field => field.removeAttribute('aria-invalid'));
    try {
      if (!token) await initialise();
      const response = await fetch('/api/contact',{method:'POST',headers:{'Content-Type':'application/json'},credentials:'same-origin',body:JSON.stringify({...fields,token,request_id:requestId}),signal:AbortSignal.timeout(30000)});
      const result = await response.json();
      if (!response.ok || !result.ok) {
        if (result.fields) {
          const invalid = Object.keys(result.fields);
          invalid.forEach(name => briefingForm.elements[name]?.setAttribute('aria-invalid','true'));
          briefingForm.elements[invalid[0]]?.focus();
        }
        if (result.refresh) await initialise();
        throw new Error(result.error || 'We could not confirm that your request was sent. Please contact us directly.');
      }
      status.textContent = 'Request accepted by our email service.';
      document.querySelector('#contact-reference').textContent = 'Reference: '+result.reference;
      success.hidden = false; submit.hidden = true;
      briefingForm.querySelectorAll('input,select,textarea').forEach(field => { field.disabled = true; });
      success.focus();
    } catch (error) {
      status.textContent = error.name === 'TimeoutError' || error instanceof TypeError ? 'We could not confirm delivery. Your details are still here. Please contact us directly before trying again.' : error.message;
      fallback.hidden = false; updateDraft();
    } finally { submitting = false; submit.disabled = false; buttonLabel(); }
  });
  document.querySelector('#new-request').addEventListener('click', () => {
    briefingForm.reset(); briefingForm.querySelectorAll('input,select,textarea').forEach(field => { field.disabled = false; });
    success.hidden = true; submit.hidden = false; status.textContent = ''; fallback.hidden = true;
    previousPayload = ''; requestId = ''; buttonLabel(); updateDraft(); initialise(); briefingForm.elements.name.focus();
  });
  buttonLabel(); updateDraft(); initialise();
}

// A reversible scroll treatment. With reduced motion or no JS, all text is visible.
const scene = document.querySelector('.research-landscape');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
if (scene) {
  let queued = false;
  function paintScene() {
    queued = false;
    if (reducedMotion.matches) {
      scene.classList.remove('scene-active'); scene.style.removeProperty('--scene-scale');
      scene.querySelectorAll('.story-line').forEach(line => { line.style.removeProperty('--line-opacity'); line.style.removeProperty('--line-offset'); });
      return;
    }
    scene.classList.add('scene-active');
    const box = scene.parentElement.getBoundingClientRect();
    const progress = Math.max(0,Math.min(1,(innerHeight*.9-box.top)/(innerHeight*.85)));
    scene.style.setProperty('--scene-scale',(0.92+0.08*progress).toFixed(4));
    scene.querySelectorAll('.story-line').forEach((line,index) => {
      const amount = Math.max(0,Math.min(1,(progress-index*.22)/.24));
      line.style.setProperty('--line-opacity',amount.toFixed(3));
      line.style.setProperty('--line-offset',`${(1-amount)*18}px`);
    });
  }
  function queueScene() { if (!queued) { queued=true; requestAnimationFrame(paintScene); } }
  addEventListener('scroll',queueScene,{passive:true}); addEventListener('resize',queueScene); reducedMotion.addEventListener('change',queueScene); paintScene();
}
const exportValues = {'2021':'263,000','2022':'442,000','2023':'an estimated 621,000'};
document.querySelectorAll('[data-export-year]').forEach(button => button.addEventListener('click', () => {
  const year=button.dataset.exportYear;
  document.querySelector('#export-insight').textContent = `${year}: ${exportValues[year]} barrels a day. The series describes historical exports, not current capacity.`;
  document.querySelectorAll('[data-export-year]').forEach(other => other.setAttribute('aria-pressed',String(other===button)));
  document.querySelectorAll('[data-export-point]').forEach(point => { point.setAttribute('r',point.dataset.exportPoint===year?'9':'5'); });
}));
const generationMix = {hydro:['64%','Hydropower','Hydropower supplied almost two-thirds of generation in 2021. For an asset-level inquiry, the next question is how the site gets its power.'],gas:['25%','Natural gas','Natural gas supplied a quarter of electricity in 2021. A site-level inquiry should examine its power source and any backup arrangements.'],oil:['11%','Petroleum','Petroleum supplied 11% of electricity in 2021. This national share does not establish the fuel supply or resilience of a particular site.']};
document.querySelectorAll('[data-energy-mix]').forEach(button => button.addEventListener('click', () => {
  const [value,label,note]=generationMix[button.dataset.energyMix];
  document.querySelector('#mix-value').textContent=value; document.querySelector('#mix-label').textContent=label; document.querySelector('#mix-insight').textContent=note;
  document.querySelectorAll('[data-energy-mix]').forEach(other => other.setAttribute('aria-pressed',String(other===button)));
}));

'''
s=s[:start]+replacement+s[end:]
p.write_text(s,encoding='utf-8')
