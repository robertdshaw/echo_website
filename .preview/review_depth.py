from pathlib import Path
from playwright.sync_api import sync_playwright
import json
paths=['capabilities.html','actor-mapping.html','evidence-workspace.html','decision-pathways.html','sources.html','trust.html','engagement.html','sample-briefs.html','sample-asset-access.html','venezuela-context.html','briefing.html']
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce')
    results=[]
    for width in [1440,390]:
        page.set_viewport_size({'width':width,'height':1000})
        for path in paths:
            page.goto('http://127.0.0.1:4173/'+path,wait_until='networkidle')
            if width==1440 and path in ['capabilities.html','actor-mapping.html','trust.html','briefing.html','sample-asset-access.html']:
                page.screenshot(path='.preview/depth-'+path.replace('.html','')+'.png',full_page=True)
            if width==390 and path in ['capabilities.html','actor-mapping.html','briefing.html']:
                page.screenshot(path='.preview/depth-mobile-'+path.replace('.html','')+'.png',full_page=True)
            page.add_script_tag(path='.preview/axe.min.js')
            violations=page.evaluate('async()=> (await axe.run(document,{runOnly:{type:"tag",values:["wcag2a","wcag2aa","wcag21aa"]}})).violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))}))')
            results.append({'width':width,'path':path,'violations':violations})
    Path('.preview/depth-accessibility.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps([r for r in results if r['violations']]))
    browser.close()
