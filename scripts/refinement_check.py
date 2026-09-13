"""Browser checks for the logo, scroll scene, claim journeys, video, and contact flow.

All contact responses are intercepted; no email is sent by this check.
"""
import json
import re
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parents[1]
BASE='http://127.0.0.1:4173'
ARTIFACTS=ROOT/'.preview'
ARTIFACTS.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':1440,'height':1000})
    errors=[]
    page.on('pageerror',lambda error: errors.append(str(error)))
    page.goto(BASE,wait_until='networkidle')
    page.evaluate("document.documentElement.style.scrollBehavior='auto'")
    scene=page.locator('.research-landscape')
    top=scene.evaluate('(el)=>el.parentElement.getBoundingClientRect().top+scrollY')
    assert top<750, 'Oil image should begin within the opening viewport'
    assert page.locator('.hero-word').all_text_contents()==['Power','shifts','Exposure','follows']
    assert page.locator('.hero-word').evaluate_all("els=>els.every(el=>getComputedStyle(el).animationName==='word-flutter')")
    assert page.locator('.hero-word').evaluate_all("els=>els.map(el=>getComputedStyle(el).animationDelay)")==['0s','0.13s','0.26s','0.39s']
    assert page.locator('.landscape-story').count()==0
    page.wait_for_function("document.querySelector('.research-landscape').style.getPropertyValue('--scene-scale')!==''")
    initial=scene.evaluate("el=>Number(el.style.getPropertyValue('--scene-scale'))")
    curve=scene.evaluate("el=>parseFloat(el.style.getPropertyValue('--scene-curve'))")
    page.evaluate('(y)=>scrollTo(0,y)',top-70)
    page.wait_for_function("Number(document.querySelector('.research-landscape').style.getPropertyValue('--scene-scale'))>.995")
    assert scene.evaluate("el=>Number(el.style.getPropertyValue('--scene-scale'))")>initial
    assert scene.evaluate("el=>parseFloat(el.style.getPropertyValue('--scene-curve'))")<curve
    page.evaluate('scrollTo(0,0)')
    page.wait_for_function("initial=>Math.abs(Number(document.querySelector('.research-landscape').style.getPropertyValue('--scene-scale'))-initial)<.0001",arg=initial)
    assert abs(scene.evaluate("el=>parseFloat(el.style.getPropertyValue('--scene-curve'))")-curve)<.1
    page.emulate_media(reduced_motion='reduce')
    page.wait_for_function("!document.querySelector('.research-landscape').classList.contains('scene-active')")
    assert page.locator('.hero-word').evaluate_all("els=>els.every(el=>getComputedStyle(el).animationName==='none')")
    assert page.locator('.image-disclosure').count()==0
    assert page.locator('.home-claim').count()==3
    assert page.locator('.chart-data, .research-console, .faq-list, video').count()==0
    assert '2021' not in page.locator('main').inner_text()
    assert '2023' not in page.locator('main').inner_text()
    page.goto(BASE+'/about.html',wait_until='networkidle')
    assert page.locator('.expert-quotes figure').count()==2
    video=page.locator('video')
    page.wait_for_function('document.querySelector("video").readyState>=2')
    assert video.evaluate('el=>el.duration')>80
    assert video.evaluate('el=>el.videoWidth')==1920
    video.evaluate('el=>{el.muted=true;el.currentTime=12;return el.play()}')
    page.wait_for_function('document.querySelector("video").currentTime>12.3')
    video.evaluate('el=>el.pause()')

    # Exercise complete outgoing fields and both requested journeys.
    delivered=[]
    response_mode={'error':False}
    page.route('**/api/contact/status',lambda route: route.fulfill(json={'ready':True,'token':'browser-test-token'}))
    def capture(route):
        values=route.request.post_data_json
        delivered.append(values)
        if response_mode['error']:
            route.fulfill(status=502,json={'error':'We could not confirm delivery. Your details are still here.'})
        else:
            route.fulfill(json={'ok':True,'reference':values['request_id']})
    page.route('**/api/contact',capture)
    fields={'name':'Example Reader','email':'reader@example.com','organization':'Example Research','role':'Research director','question':'Policy changes & access.\nA second paragraph.','details':'Our deadline is approaching.\nPlease explain the scope.'}
    page.goto(BASE+'/briefing.html?audience=credit',wait_until='networkidle')
    # The audience parameter preselects the sector for the visitor.
    assert page.locator('[name=sector]').input_value()=='Distressed debt & special situations'
    for name,value in fields.items():
        page.locator('[name="'+name+'"]').fill(value)
    page.locator('[name=referral]').select_option('LinkedIn')
    page.locator('.send-request').click()
    expect(page.locator('#contact-success')).to_be_visible()
    assert page.locator('[name=name]').is_disabled()
    values=delivered[-1]
    assert all(values[key]==value for key,value in fields.items()),'A submitted field was not delivered'
    assert values['sector']=='Distressed debt & special situations'
    assert values['referral']=='LinkedIn' and values['website']==''
    assert values['token']=='browser-test-token'
    assert values['request_id'] in page.locator('#contact-reference').inner_text()

    # A refused delivery keeps the details in the form and reuses the reference.
    response_mode['error']=True
    page.goto(BASE+'/briefing.html',wait_until='networkidle')
    for name,value in fields.items():
        page.locator('[name="'+name+'"]').fill(value)
    page.locator('[name=sector]').select_option('Oil & gas')
    page.locator('.send-request').click()
    expect(page.locator('#form-status')).to_contain_text('could not confirm delivery')
    expect(page.locator('#contact-success')).to_be_hidden()
    assert page.locator('[name=name]').input_value()==fields['name']
    failed_id=delivered[-1]['request_id']
    page.locator('.send-request').click()
    expect(page.locator('#form-status')).to_contain_text('could not confirm delivery')
    assert delivered[-1]['request_id']==failed_id,'An unchanged retry must reuse the request reference'
    response_mode['error']=False

    paths=[path.relative_to(ROOT/'public').as_posix() for path in (ROOT/'public').rglob('*.html')]
    for width in [320,390,768,1440]:
        page.set_viewport_size({'width':width,'height':1000})
        for path in paths:
            page.goto(BASE+'/'+path,wait_until='domcontentloaded')
            page.evaluate('document.fonts.ready')
            assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),f'Overflow: {width} {path}'
            assert not re.search('[\u2190-\u21ff\u2303\u2304\u27f0-\u27ff]',page.locator('body').inner_text()),f'Arrow remains: {path}'
            assert page.locator('.echoframe-mark').evaluate_all('''els=>els.every(el=>{
                const b=el.getBBox(),v=el.viewBox.baseVal;
                return b.x>=v.x+2 && b.y>=v.y+2 && b.x+b.width<=v.width-2 && b.y+b.height<=v.height-2;
            })'''),f'Clipped mark: {width} {path}'
        print(f'All {len(paths)} pages passed at {width}px',flush=True)
    page.set_viewport_size({'width':1440,'height':1000})
    page.goto(BASE,wait_until='networkidle')
    page.screenshot(path=str(ARTIFACTS/'refined-viewport.png'))
    page.locator('.research-landscape').screenshot(path=str(ARTIFACTS/'refined-scene-final.png'))
    assert not errors,errors
    browser.close()
    print(json.dumps({'result':'passed','pages':len(paths),'mail':'mocked only','page_errors':errors}))
