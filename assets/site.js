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
    title: 'Who has authority and what happens next?',
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
  const status = document.querySelector('#form-status');
  const submit = briefingForm.querySelector('.send-request');
  const success = document.querySelector('#contact-success');
  const fieldsToSend = ['name', 'email', 'organization', 'sector', 'question', 'details', 'referral', 'website'];
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
// The hero photograph widens as the hero enters view and eases back as it
// leaves. Only the image inside the frame moves, so layout never shifts.
const heroPhoto = document.querySelector('.ef-hero-photo');
const heroFrame = document.querySelector('.ef-hero-media');
if (heroPhoto && heroFrame) {
  const heroMotion = matchMedia('(prefers-reduced-motion: reduce)');
  let heroQueued = false;
  function paintHero() {
    heroQueued = false;
    if (heroMotion.matches) { heroPhoto.style.removeProperty('--ef-zoom'); return; }
    const box = heroFrame.getBoundingClientRect();
    const top = box.top + scrollY;
    // Measured from where the hero sits, not from the viewport, because the hero
    // is already fully in view when the page loads.
    const progress = Math.max(0, Math.min(1, (scrollY - top) / Math.max(1, box.height)));
    // One rise and one fall. At rest on load, widest halfway out, back at rest after.
    heroPhoto.style.setProperty('--ef-zoom', (1 + 0.06 * Math.sin(Math.PI * progress)).toFixed(4));
  }
  function queueHero() { if (!heroQueued) { heroQueued = true; requestAnimationFrame(paintHero); } }
  addEventListener('scroll', queueHero, { passive: true });
  addEventListener('resize', queueHero);
  heroMotion.addEventListener('change', queueHero);
  paintHero();
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
