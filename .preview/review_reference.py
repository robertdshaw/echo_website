from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce')
    page.goto('http://127.0.0.1:4173',wait_until='networkidle')
    page.screenshot(path='.preview/zite-echo-top.png')
    page.screenshot(path='.preview/zite-echo-full.png',full_page=True)
    page.set_viewport_size({'width':390,'height':900})
    page.screenshot(path='.preview/zite-echo-mobile.png')
    print(json.dumps({'font':page.locator('h1').evaluate('(el)=>getComputedStyle(el).fontFamily'),'height':page.evaluate('document.documentElement.scrollHeight')}))
    browser.close()
