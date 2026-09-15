from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(reduced_motion='reduce')
    results=[]
    for width in [390,1440]:
        page.set_viewport_size({'width':width,'height':1000})
        for path in ['index.html','government-affairs.html','distressed-debt.html','research.html']:
            page.goto('http://127.0.0.1:4173/'+path,wait_until='networkidle')
            page.add_script_tag(path='.preview/axe.min.js')
            violations=page.evaluate('async()=> (await axe.run(document,{runOnly:{type:"tag",values:["wcag2a","wcag2aa","wcag21aa"]}})).violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))}))')
            results.append({'width':width,'path':path,'violations':violations})
    print(json.dumps(results))
    browser.close()
