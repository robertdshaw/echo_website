from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':1200,'height':630},reduced_motion='reduce')
    page.goto('http://127.0.0.1:4173/assets/social-card.svg',wait_until='networkidle')
    page.screenshot(path='assets/social-card.png')
    page.set_viewport_size({'width':1440,'height':1000})
    page.goto('http://127.0.0.1:4173',wait_until='networkidle')
    page.locator('#intelligence').screenshot(path='.preview/reference-desk.png')
    print(json.dumps(page.locator('.dispatch,.dispatch h3,.dispatches,.desk-grid').evaluate_all('(els)=>els.map(e=>({class:e.className,width:e.clientWidth,scroll:e.scrollWidth,overflow:getComputedStyle(e).overflow,whiteSpace:getComputedStyle(e).whiteSpace}))')))
    page.screenshot(path='.preview/reference-final-home.png',full_page=True)
    page.goto('http://127.0.0.1:4173/government-affairs.html',wait_until='networkidle')
    page.screenshot(path='.preview/reference-final-government.png',full_page=True)
    browser.close()
