function headingCopy(value) { return value.replace(/\.(?=\s|$)/g, ''); }
'use strict';

// A transparent, local preview of three research mandates.
const previewTopics = {
  policy: ['Who can change the conditions around an operating asset?', 'Trace formal authority, documented positions, and the next policy milestone. Compare the official account with local evidence.', 'government-affairs.html', 'Explore the government affairs perspective'],
  asset: ['What would establish that access to an asset has changed?', 'Define the asset, the observation window, and the evidence needed. Keep official statements, local accounts, and physical observations distinct.', 'venezuela.html', 'Explore the Venezuela programme'],
  credit: ['Which political assumption in the thesis needs another look?', 'Identify a named decision or counterparty milestone. Record the evidence that could support, challenge, or leave the assumption unresolved.', 'distressed-debt.html', 'Explore the distressed-debt perspective']
};
document.querySelectorAll('[data-preview-topic]').forEach(button => {
  button.addEventListener('click', () => {
    const [question, answer, href, label] = previewTopics[button.dataset.previewTopic];
    document.querySelector('#preview-question').textContent = headingCopy(question);
    document.querySelector('#preview-answer').textContent = answer;
    const link = document.querySelector('#preview-link');
    link.href = href;
    link.firstChild.textContent = label + ' ';
    document.querySelectorAll('[data-preview-topic]').forEach(option => option.setAttribute('aria-pressed', String(option === button)));
  });
});

const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('#main-nav');
const navGroups = [...document.querySelectorAll('.nav-group')];
navGroups.forEach(group => group.querySelector('summary').addEventListener('click', () => {
  navGroups.forEach(other => { if (other !== group) other.open = false; });
}));
navGroups.forEach(group => group.addEventListener('toggle', () => {
  if (group.open) navGroups.forEach(other => { if (other !== group) other.open = false; });
}));
navGroups.forEach(group => group.querySelectorAll('a').forEach(link => link.addEventListener('click', () => { group.open = false; })));
document.addEventListener('click', event => {
  if (!event.target.closest('.nav-group')) navGroups.forEach(group => { group.open = false; });
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape') {
    const openGroup = navGroups.find(group => group.open);
    if (openGroup) { openGroup.open = false; openGroup.querySelector('summary').focus(); }
  }
});
function closeMenu(returnFocus = false) {
  navGroups.forEach(group => { group.open = false; });
  nav?.classList.remove('is-open');
  menuButton?.setAttribute('aria-expanded', 'false');
  if (returnFocus) menuButton?.focus();
}
menuButton?.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  nav.classList.toggle('is-open', open);
});
nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => closeMenu()));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menuButton?.getAttribute('aria-expanded') === 'true') closeMenu(true);
});
document.addEventListener('click', event => {
  if (!event.target.closest('.site-header')) closeMenu();
});

// The full library is rendered in HTML; filtering is a progressive enhancement.
const search = document.querySelector('#research-search');
if (search) {
  const filters = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('.library-grid .research-card')];
  const params = new URLSearchParams(location.search);
  const savedOnly = document.querySelector('#saved-only');
  savedOnly.checked = params.get('saved') === '1';
  function savedSlugs() {
    try {
      const value = JSON.parse(localStorage.getItem('echoframe-saved-articles') || '[]');
      return Array.isArray(value) ? value : [];
    } catch { return []; }
  }
  let category = filters.some(button => button.dataset.filter === params.get('category')) ? params.get('category') : 'All intelligence';
  search.value = params.get('q') || '';
  function filterLibrary(updateUrl = true) {
    const query = search.value.trim().toLowerCase();
    let count = 0;
    const saved = savedSlugs();
    cards.forEach(card => {
      card.hidden = !((category === 'All intelligence' || category === card.dataset.category) && card.dataset.search.includes(query) && (!savedOnly.checked || saved.includes(card.dataset.slug)));
      if (!card.hidden) count++;
    });
    filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
    document.querySelector('#result-count').textContent = `${count} perspective${count === 1 ? '' : 's'}`;
    document.querySelector('#no-results').hidden = count !== 0;
    if (updateUrl) {
      const url = new URL(location.href);
      category === 'All intelligence' ? url.searchParams.delete('category') : url.searchParams.set('category', category);
      query ? url.searchParams.set('q', search.value.trim()) : url.searchParams.delete('q');
      savedOnly.checked ? url.searchParams.set('saved', '1') : url.searchParams.delete('saved');
      history.replaceState(null, '', url);
    }
  }
  filters.forEach(button => button.addEventListener('click', () => { category = button.dataset.filter; filterLibrary(); }));
  search.addEventListener('input', () => filterLibrary());
  savedOnly.addEventListener('change', () => filterLibrary());
  addEventListener('storage', () => filterLibrary(false));
  document.querySelector('#reset-search').addEventListener('click', () => { category = 'All intelligence'; search.value = ''; savedOnly.checked = false; filterLibrary(); search.focus(); });
  filterLibrary(false);
}

// Each tablist owns its own panels, so audience and coverage controls coexist.
document.querySelectorAll('[role="tablist"]').forEach(tablist => {
  const tabs = [...tablist.querySelectorAll('[role="tab"]')];
  function selectTab(tab, focus = false) {
    tabs.forEach(item => {
      const active = item === tab;
      item.setAttribute('aria-selected', String(active));
      item.tabIndex = active ? 0 : -1;
      document.getElementById(item.getAttribute('aria-controls')).hidden = !active;
    });
    if (focus) tab.focus();
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => selectTab(tab));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next !== undefined) { event.preventDefault(); selectTab(tabs[next], true); }
    });
  });
});
document.querySelectorAll('[data-select-perspective]').forEach(link => link.addEventListener('click', () => {
  document.getElementById(`perspective-${link.dataset.selectPerspective}`)?.click();
}));

const consequences = {
  policy: {
    kicker: 'Government affairs / The decision pathway',
    title: 'Who has authority—and what happens next?',
    text: 'Identify the issuing institution, the formal status of its proposal, and the next decision point. Separate a public position from an implemented measure.',
    url: 'government-affairs.html'
  },
  asset: {
    kicker: 'Asset-level research / The operating context',
    title: 'What changed at the asset, and what is still a claim?',
    text: 'Compare the documentary position with dated observations about activity, access, or counterparties. Keep disagreements visible and identify the evidence that could resolve them.',
    url: 'venezuela.html'
  },
  capital: {
    kicker: 'Distressed debt / The thesis assumption',
    title: 'Which assumption now needs fresh evidence?',
    text: 'Connect the verified development to a bounded research question about the thesis. Identify which political or operational assumptions require review, while leaving valuation and legal determinations to the appropriate specialists.',
    url: 'distressed-debt.html'
  }
};
document.querySelectorAll('[data-consequence]').forEach(button => button.addEventListener('click', () => {
  const data = consequences[button.dataset.consequence];
  ['kicker', 'title', 'text'].forEach(key => { document.getElementById(`consequence-${key}`).textContent = key === "title" ? headingCopy(data[key]) : data[key]; });
  document.getElementById('consequence-link').href = data.url;
  document.querySelectorAll('[data-consequence]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
}));

const evidenceStates = {
  single: {
    title: 'One evidentiary chain, however many headlines.',
    description: 'Reports trace back to one source or source family. Repetition does not make the underlying account independently confirmed.',
    check: 'Identify the original account, its time and place, and how the source knows.',
    next: 'Seek an independently obtained account or a different collection method.'
  },
  corroborated: {
    title: 'Independent evidence supports the same event.',
    description: 'Independent accounts or collection methods support a comparable claim about the same time, place, and activity. The label does not remove the need to state limitations.',
    check: 'Trace the underlying accounts. Different ownership and home cities are screening clues, not proof of independent reporting.',
    next: 'Record exactly which parts of the event are supported and which remain uncertain.'
  },
  contradicted: {
    title: 'Keep both accounts. The disagreement stays visible.',
    description: 'Credible accounts assert incompatible claims about the same event. Retain the supporting and opposing evidence and route the conflict to an analyst.',
    check: 'Establish that the apparent contradiction is not a difference in timing, location, or the activity being described.',
    next: 'Seek a discriminating observation. Do not silently resolve the conflict or turn a denial into another positive signal.'
  }
};
document.querySelectorAll('[data-evidence-state]').forEach(button => button.addEventListener('click', () => {
  const selected = evidenceStates[button.dataset.evidenceState];
  for (const [key, value] of Object.entries(selected)) document.getElementById(`evidence-${key}`).textContent = key === "title" ? headingCopy(value) : value;
  document.querySelectorAll('[data-evidence-state]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
}));

async function copyText(text, status) {
  try {
    if (!navigator.clipboard) throw new Error('Clipboard unavailable');
    await navigator.clipboard.writeText(text);
    status.textContent = 'Copied to clipboard.';
  } catch {
    status.textContent = 'Clipboard access is unavailable. Select and copy the text manually.';
  }
}
const saveButton = document.querySelector('.save-article');
if (saveButton) {
  const status = document.querySelector('.reader-status');
  const storageKey = 'echoframe-saved-articles';
  let saved = [];
  try {
    const stored = JSON.parse(localStorage.getItem(storageKey) || '[]');
    if (Array.isArray(stored)) saved = stored.filter(value => typeof value === 'string');
  } catch { /* Reading remains available if storage is disabled. */ }
  function renderSaved() {
    const isSaved = saved.includes(saveButton.dataset.slug);
    saveButton.setAttribute('aria-pressed', String(isSaved));
    saveButton.textContent = isSaved ? 'Saved ✓' : 'Save article +';
  }
  saveButton.addEventListener('click', () => {
    const slug = saveButton.dataset.slug;
    const next = saved.includes(slug) ? saved.filter(item => item !== slug) : [...saved, slug];
    try {
      localStorage.setItem(storageKey, JSON.stringify(next)); saved = next; renderSaved();
      status.textContent = saved.includes(slug) ? 'Article saved in this browser on this device.' : 'Article removed from your saved list.';
    } catch { status.textContent = 'This browser cannot save articles. You can bookmark the page instead.'; }
  });
  renderSaved();
  document.querySelector('.copy-link').addEventListener('click', async () => {
    await copyText(location.href, status);
    if (status.textContent.startsWith('Clipboard access')) status.textContent = 'Copy this page’s address from your browser to share it.';
  });
  document.querySelector('.print-article').addEventListener('click', () => window.print());
  let queued = false;
  function updateProgress() {
    const article = document.querySelector('main > article');
    const bottom = article.offsetTop + article.offsetHeight - innerHeight;
    document.querySelector('.reading-progress').style.width = `${Math.min(100, Math.max(0, scrollY / Math.max(1, bottom) * 100))}%`;
    queued = false;
  }
  addEventListener('scroll', () => { if (!queued) { requestAnimationFrame(updateProgress); queued = true; } }, { passive: true });
  addEventListener('resize', updateProgress);
  updateProgress();
}

const briefingForm = document.querySelector('#briefing-form');
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
  const decisionTest = briefingForm.elements.decision_test;
  if ([...decisionTest.options].some(option => option.value === params.get('test'))) {
    decisionTest.value = params.get('test');
    briefingForm.querySelector('.optional-context').open = true;
  }
  if (preset) {
    briefingForm.elements.perspective.value = preset[0];
    briefingForm.elements.sector.value = params.get('audience') === 'government' ? 'Oil & gas' : 'Distressed debt & special situations';
    document.querySelector('#briefing-form-title').textContent = headingCopy(preset[1]);
    document.querySelector('#audience-context').textContent = preset[2];
    document.querySelector('#audience-context').hidden = false;
  }
  if (params.has('audience') || params.has('format') || params.has('region')) briefingForm.querySelector('.optional-context').open = true;
  if (params.get('kind') === 'contact') briefingForm.elements.request_type.value = 'Contact request';
  const sectorGuidance = {
    'Oil & gas': 'A useful starting point: one asset, the authority that affects it, and the evidence you need before your next stakeholder meeting.',
    'Distressed debt & special situations': 'A useful starting point: one political assumption in the thesis, its time horizon, and the evidence that would make you revisit it.',
    'Energy & infrastructure': 'A useful starting point: one project dependency, the decision-maker involved, and the next milestone you need to understand.',
    'Advisory & research': 'A useful starting point: the question your team must answer and a source or method you would like us to walk through.',
    'Other': 'Tell us your sector and the decision in your message. We will assess whether the question fits our research scope.'
  };
  function updateSectorGuidance() {
    document.querySelector('#sector-guidance').textContent = sectorGuidance[briefingForm.elements.sector.value] || 'Choose a sector so we can suggest a starting point. Please use non-confidential examples.';
  }
  briefingForm.elements.sector.addEventListener('change', updateSectorGuidance);
  updateSectorGuidance();
  const labels = {request_type:'Request type',name:'Full name',email:'Work email',organization:'Organisation',role:'Role / team',headquarters:'Location',phone:'Phone',sector:'Sector',question:'Decision / research question',proof:'What the first briefing should demonstrate',region:'Region',perspective:'Perspective',decision_test:'Requirement to explore',subject:'Asset, contract, or place',deadline:'Deadline',format:'Research format',referral:'How I found EchoFrame'};
  function readFields() {
    const data = Object.fromEntries(new FormData(briefingForm));
    return Object.fromEntries(Object.entries(data).map(([key,value]) => [key,String(value).trim()]));
  }
  function updateDraft() {
    const values = readFields();
    const text = 'Hello EchoFrame,\n\n'+Object.entries(labels).map(([key,label]) => `${label}: ${values[key] || 'Not specified'}`).join('\n')+'\n';
    draft.href = `mailto:contact@echoframe.co?subject=${encodeURIComponent('EchoFrame '+values.request_type)}&body=${encodeURIComponent(text)}`;
  }
  function buttonLabel() { submit.innerHTML = (briefingForm.elements.request_type.value === 'Demo request' ? 'Send demo request' : 'Send contact request')+' '; }
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

// The image opens from a curved frame into a wider rectangle as it enters view.
const scene = document.querySelector('.research-landscape');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
if (scene) {
  let queued = false;
  function paintScene() {
    queued = false;
    if (reducedMotion.matches) {
      scene.classList.remove('scene-active');
      ['--scene-scale','--scene-curve','--scene-corner'].forEach(key=>scene.style.removeProperty(key));
      return;
    }
    scene.classList.add('scene-active');
    const box = scene.parentElement.getBoundingClientRect();
    const progress = Math.max(0,Math.min(1,(innerHeight*.9-box.top)/(innerHeight*.85)));
    scene.style.setProperty('--scene-scale',(0.92+0.08*progress).toFixed(4));
    scene.style.setProperty('--scene-curve',`${(110-104*progress).toFixed(1)}px`);
    scene.style.setProperty('--scene-corner',`${(35-29*progress).toFixed(1)}px`);
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

document.querySelectorAll('.print-sample').forEach(button => button.addEventListener('click', () => window.print()));
const sourceSearch = document.querySelector('#source-search');
if (sourceSearch) {
  const category = document.querySelector('#source-category');
  const records = [...document.querySelectorAll('.source-card')];
  const parameters = new URLSearchParams(location.search);
  sourceSearch.value = parameters.get('q') || '';
  if ([...category.options].some(option => option.value === parameters.get('category'))) category.value = parameters.get('category');
  function filterSources() {
    let count = 0;
    const query = sourceSearch.value.trim().toLowerCase();
    records.forEach(record => {
      record.hidden = !((category.value === 'All sources' || category.value === record.dataset.sourceCategory) && record.dataset.sourceSearch.includes(query));
      if (!record.hidden) count++;
    });
    document.querySelector('#source-count').textContent = `${count} source${count === 1 ? '' : 's'}`;
    document.querySelector('#source-empty').hidden = count !== 0;
    const url = new URL(location.href);
    query ? url.searchParams.set('q',sourceSearch.value.trim()) : url.searchParams.delete('q');
    category.value === 'All sources' ? url.searchParams.delete('category') : url.searchParams.set('category',category.value);
    history.replaceState(null,'',url);
  }
  sourceSearch.addEventListener('input',filterSources);
  category.addEventListener('change',filterSources);
  document.querySelector('#source-reset').addEventListener('click', () => { category.value='All sources'; sourceSearch.value=''; filterSources(); sourceSearch.focus(); });
  filterSources();
}
