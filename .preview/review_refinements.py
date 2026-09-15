from pathlib import Path
from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce')
    errors=[]; page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto('http://127.0.0.1:4173',wait_until='networkidle')
    page.screenshot(path='.preview/refined-home.png',full_page=True)
    page.locator('.landscape-wrap').screenshot(path='.preview/refined-scene.png')
    page.locator('#energy-charts').screenshot(path='.preview/refined-charts.png')
    video=page.locator('video')
    video.scroll_into_view_if_needed()
    page.wait_for_function('document.querySelector("video").readyState>=1')
    print(json.dumps(video.evaluate('(v)=>({duration:v.duration,width:v.videoWidth,height:v.videoHeight,ready:v.readyState})')))
    video.evaluate('(v)=>v.currentTime=12')
    page.wait_for_function('document.querySelector("video").readyState>=2')
    video.screenshot(path='.preview/original-video-frame.png')
    page.goto('http://127.0.0.1:4173/briefing.html',wait_until='networkidle')
    page.screenshot(path='.preview/refined-contact.png',full_page=True)
    results=[]
    for width in [1440,390]:
        page.set_viewport_size({'width':width,'height':1000})
        for path in ['index.html','briefing.html','about.html','research/from-signal-to-significance.html','trust.html','sample-asset-access.html']:
            page.goto('http://127.0.0.1:4173/'+path,wait_until='networkidle')
            page.add_script_tag(path='.preview/axe.min.js')
            v=page.evaluate('async()=> (await axe.run(document,{runOnly:{type:"tag",values:["wcag2a","wcag2aa","wcag21aa"]}})).violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))}))')
            if v: results.append({'width':width,'page':path,'violations':v})
    print(json.dumps({'violations':results,'errors':errors}))
    Path('.preview/refinement-a11y.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    browser.close()
