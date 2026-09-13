"""Browser checks for the full-site navigation, research specimens, and workbenches."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
BASE='http://127.0.0.1:4173'
NEW_PAGES=['capabilities.html','actor-mapping.html','evidence-workspace.html','decision-pathways.html','sources.html','venezuela-context.html','trust.html','engagement.html','sample-briefs.html','sample-asset-access.html','sample-thesis-review.html']

with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce')
    errors=[]; page.on('pageerror',lambda error: errors.append(str(error)))
    page.goto(BASE,wait_until='networkidle')
    groups=page.locator('.nav-group')
    groups.nth(0).locator('summary').click()
    assert groups.nth(0).get_attribute('open') is not None
    assert page.get_by_role('link',name='Actor & asset mapping Document').is_visible()
    groups.nth(1).locator('summary').click()
    assert groups.nth(0).get_attribute('open') is None
    groups.nth(1).locator('summary').press('Escape')
    assert groups.nth(1).get_attribute('open') is None
    assert groups.nth(1).locator('summary').evaluate('(el)=>el===document.activeElement')
    page.goto(BASE+'/how-it-works.html',wait_until='networkidle')
    assert page.locator('.analytical-layers article').count()==6
    page.locator('.analytical-layers summary').nth(4).click()
    assert page.locator('.analytical-layers details').nth(4).get_attribute('open') is not None
    assert page.locator('.judgment-stage').count()==3
    page.goto(BASE+'/capabilities.html',wait_until='networkidle')
    assert page.locator('.risk-dimensions article').count()==5
    assert page.locator('.scenario-options details').count()==5
    page.locator('.scenario-options summary').last.click()
    assert page.locator('.scenario-options details').last.get_attribute('open') is not None
    page.goto(BASE+'/decision-pathways.html',wait_until='networkidle')
    assert page.locator('.entry-test-tabs [role=tab]').count()==6
    page.locator('#entry-tab-0').focus()
    page.locator('#entry-tab-0').press('End')
    assert page.locator('#entry-panel-5').is_visible()
    assert page.locator('#entry-panel-0').is_hidden()
    page.locator('#entry-tab-5').press('ArrowRight')
    assert page.locator('#entry-panel-0').is_visible()
    page.locator('#entry-tab-1').click()
    page.locator('#entry-panel-1 a').click()
    assert page.locator('[name=decision_test]').input_value()=='Enforceable contracts'
    assert page.locator('.optional-context').get_attribute('open') is not None
    page.goto(BASE+'/briefing.html?test=unrecognised',wait_until='networkidle')
    assert page.locator('[name=decision_test]').input_value()=='To discuss'
    page.goto(BASE+'/venezuela.html',wait_until='networkidle')
    assert page.locator('.forecast-case').count()==1
    assert page.locator('.forecast-case').inner_text().count('74%')==2
    assert 'private' in page.locator('.forecast-case').inner_text()
    page.goto(BASE+'/actor-mapping.html',wait_until='networkidle')
    page.locator('[data-actor=workers]').click()
    assert page.locator('#actor-title').inner_text()=='Worker representatives'
    assert 'group represented' in page.locator('#actor-evidence').inner_text()
    assert page.locator('[data-actor][aria-pressed=true]').count()==1
    page.goto(BASE+'/evidence-workspace.html',wait_until='networkidle')
    for state,count in [('contradicted',2),('repeated',1),('limited',1),('all',4)]:
        page.locator('[data-ledger-filter='+state+']').click()
        assert page.locator('[data-ledger-state]:visible').count()==count
    page.goto(BASE+'/decision-pathways.html',wait_until='networkidle')
    page.locator('[data-pathway=unresolved]').click()
    assert 'gap visible' in page.locator('#pathway-title').inner_text()
    page.locator('[data-pathway=challenged]').click()
    assert 'restriction' in page.locator('#pathway-title').inner_text()
    page.goto(BASE+'/sources.html?category=Disputes%20%26%20counterparties',wait_until='networkidle')
    assert page.locator('.source-card:visible').count()==2
    page.locator('#source-search').fill('filings')
    assert page.locator('.source-card:visible').count()==1
    page.reload(wait_until='networkidle')
    assert page.locator('.source-card:visible').count()==1
    page.locator('#source-search').fill('no-such-source')
    assert page.locator('#source-empty').is_visible()
    page.locator('#source-reset').click()
    assert page.locator('.source-card:visible').count()==6
    page.goto(BASE+'/briefing.html?audience=credit&format=Focused%20research%20brief',wait_until='networkidle')
    assert page.locator('select[name=format]').input_value()=='Focused research brief'
    assert page.locator('select[name=perspective]').input_value()=='Distressed debt / hedge fund'
    assert page.locator('.optional-context').get_attribute('open') is not None
    assert page.locator('[name=headquarters]').get_attribute('required') is not None
    for sample in ['sample-asset-access','sample-thesis-review']:
        page.goto(BASE+'/'+sample+'.html',wait_until='networkidle')
        assert page.locator('.sample-body>section').count()==8
        assert page.locator('.sample-document').inner_text().count('fictional')>=2
        with page.expect_download() as info:
            page.locator('.sample-toolbar a[download]').click()
        assert info.value.suggested_filename==sample+'.md'
        assert 'FICTIONAL RESEARCH EXERCISE' in (ROOT/'downloads'/info.value.suggested_filename).read_text(encoding='utf-8')
        page.emulate_media(media='print')
        assert page.locator('.sample-toc').is_hidden()
        assert page.locator('.sample-body').is_visible()
        page.emulate_media(media='screen')
    for width in [320,390,768,1440]:
        page.set_viewport_size({'width':width,'height':1000})
        for path in NEW_PAGES+['index.html','government-affairs.html','distressed-debt.html','briefing.html']:
            response=page.goto(BASE+'/'+path,wait_until='networkidle')
            assert response.status==200,path
            assert not page.evaluate('document.documentElement.scrollWidth > innerWidth+1'),f'Overflow: {width} {path}'
        page.goto(BASE,wait_until='networkidle')
        if width<1001:
            page.get_by_role('button',name='Menu').click()
        for group in page.locator('.nav-group').all():
            group.locator('summary').click()
            assert not page.evaluate('document.documentElement.scrollWidth > innerWidth+1'),f'Open navigation overflow: {width}'
            assert group.locator('.nav-panel').is_visible()
    assert not errors,errors
    browser.close()
    print(json.dumps({'result':'passed','new_pages':len(NEW_PAGES),'viewports':[320,390,768,1440],'page_errors':errors}))
