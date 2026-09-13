"""Browser smoke checks. Run a local server on port 4173 before running this file."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
ARTIFACTS=ROOT/'.preview'
ARTIFACTS.mkdir(exist_ok=True)
BASE='http://127.0.0.1:4173'

with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
    errors=[]
    page.on('pageerror',lambda error: errors.append(str(error)))
    page.goto(BASE,wait_until='networkidle')
    page.screenshot(path=str(ARTIFACTS/'homepage-desktop.png'),full_page=True)
    assert page.locator('h1').count()==1
    # Each homepage claim explains itself one click deeper, then leads to intake.
    destinations=['government-affairs.html','distressed-debt.html','methodology.html']
    assert page.locator('.home-claim a').evaluate_all('(els)=>els.map(el=>el.getAttribute("href"))')==destinations
    for i,destination in enumerate(destinations):
        page.goto(BASE,wait_until='networkidle')
        page.locator('.home-claim a').nth(i).click()
        assert page.url.endswith('/'+destination)
        link=page.get_by_role('link',name='See how we can help you').last
        link.click()
        assert '/briefing.html' in page.url
        expected=['Oil & gas','Distressed debt & special situations',''][i]
        assert page.locator('[name=sector]').input_value()==expected
        assert page.locator('[name=proof]').is_visible()
    page.goto(BASE+'/about.html',wait_until='networkidle')
    question=page.locator('.faq-list summary').first
    question.focus()
    question.press('Enter')
    assert page.locator('.faq-list details').first.get_attribute('open') is not None
    question.press('Enter')
    assert page.locator('.faq-list details').first.get_attribute('open') is None
    page.goto(BASE+'/research.html',wait_until='networkidle')
    page.get_by_role('button',name='Methods',exact=True).click()
    assert page.locator('.research-card:visible').count()==4
    page.get_by_role('searchbox').fill('actor')
    assert page.locator('.research-card:visible').count()==1
    page.reload()
    assert page.locator('.research-card:visible').count()==1
    page.get_by_role('searchbox').fill('nothing-matches-this')
    assert page.locator('#no-results').is_visible()
    page.locator('#reset-search').click()
    assert page.locator('.research-card:visible').count()==8
    page.get_by_role('button',name='Venezuela',exact=True).click()
    assert page.locator('.research-card:visible').count()==2
    page.get_by_role('button',name='All intelligence',exact=True).click()
    page.screenshot(path=str(ARTIFACTS/'library-desktop.png'),full_page=True)
    page.goto(BASE+'/methodology.html',wait_until='networkidle')
    page.locator('[data-evidence-state=contradicted]').click()
    assert 'disagreement' in page.locator('#evidence-title').inner_text()
    assert page.locator('[data-evidence-state=single]').get_attribute('aria-pressed')=='false'
    page.goto(BASE+'/venezuela.html',wait_until='networkidle')
    assert page.locator('.evidence-grid article').count()==3
    assert 'FICTIONAL ASSET' in page.locator('.question-card').inner_text()
    page.screenshot(path=str(ARTIFACTS/'venezuela-desktop.png'),full_page=True)
    page.goto(BASE+'/research/from-signal-to-significance.html',wait_until='networkidle')
    page.locator('.save-article').click()
    assert page.locator('.save-article').get_attribute('aria-pressed')=='true'
    page.reload()
    assert page.locator('.save-article').get_attribute('aria-pressed')=='true'
    page.goto(BASE+'/research.html?saved=1',wait_until='networkidle')
    assert page.locator('.research-card:visible').count()==1
    page.goto(BASE+'/research/from-signal-to-significance.html',wait_until='networkidle')
    page.locator('.save-article').click()
    assert page.locator('.save-article').get_attribute('aria-pressed')=='false'
    page.screenshot(path=str(ARTIFACTS/'article-desktop.png'),full_page=True)
    page.emulate_media(media='print')
    assert page.locator('.site-header').is_hidden()
    assert page.locator('.article-body').is_visible()
    page.emulate_media(media='screen')
    page.goto(BASE+'/briefing.html?region=Venezuela',wait_until='networkidle')
    assert page.locator('select[name=region]').input_value()=='Venezuela'
    assert page.locator('.send-request').inner_text().startswith('Send demo request')
    assert page.locator('[name=organization]').get_attribute('required') is not None
    for audience,expected in [('government','Oil & gas government affairs'),('credit','Distressed debt / hedge fund')]:
        page.goto(BASE+'/briefing.html?audience='+audience,wait_until='networkidle')
        assert page.get_by_label('Your perspective').input_value()==expected
        assert page.locator('#audience-context').is_visible()
    page.goto(BASE+'/briefing.html?audience=unknown',wait_until='networkidle')
    assert page.get_by_label('Your perspective').input_value()=='Not specified'
    assert page.locator('#audience-context').is_hidden()
    for width in [320,390,768,1440]:
        page.set_viewport_size({'width':width,'height':900})
        for path in ['index.html','government-affairs.html','distressed-debt.html','venezuela.html','research.html','coverage.html','methodology.html','about.html','briefing.html','editorial-standards.html','privacy.html','es/index.html','research/following-european-energy-policy.html','research/when-sources-disagree.html']:
            response=page.goto(BASE+'/'+path,wait_until='networkidle')
            assert response.status==200,path
            assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1'),f'Horizontal overflow: {width} {path}'
            page.locator('img').evaluate_all('(images)=>images.forEach(i=>i.loading="eager")')
            page.wait_for_function('Array.from(document.images).every(i=>i.complete && i.naturalWidth>0)')
            broken=page.locator('img').evaluate_all('(images)=>images.filter(i=>!i.complete || i.naturalWidth===0).map(i=>i.src)')
            assert not broken,f'Broken images: {path}: {broken}'
        if width==390:
            page.goto(BASE,wait_until='networkidle')
            page.screenshot(path=str(ARTIFACTS/'homepage-mobile.png'),full_page=True)
            page.get_by_role('button',name='Menu').click()
            assert page.locator('#main-nav').is_visible()
            page.get_by_role('button',name='Menu').press('Escape')
            assert page.locator('#main-nav').is_hidden()
    page.emulate_media(reduced_motion='reduce')
    page.goto(BASE,wait_until='networkidle')
    assert page.locator('.power-copy').evaluate('(el)=>getComputedStyle(el).animationName')=='none'
    assert not errors,errors
    browser.close()
    print(json.dumps({'result':'passed','viewports':[320,390,768,1440],'page_errors':errors,'screenshots':str(ARTIFACTS)},indent=2))
