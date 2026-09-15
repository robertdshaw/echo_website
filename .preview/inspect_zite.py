from playwright.sync_api import sync_playwright
import json
from pathlib import Path
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':1440,'height':1000}, device_scale_factor=1)
    page.goto('https://zite.co',wait_until='networkidle',timeout=60000)
    page.screenshot(path='.preview/zite-top.png')
    for y in range(0,12000,800):
        page.evaluate('(y)=>window.scrollTo(0,y)',y)
        page.wait_for_timeout(150)
    page.screenshot(path='.preview/zite-full.png',full_page=True)
    print(json.dumps(page.locator('h1,h2,body,nav').evaluate_all('(els)=>els.slice(0,16).map(e=>({tag:e.tagName,text:e.innerText.slice(0,130),font:getComputedStyle(e).fontFamily,size:getComputedStyle(e).fontSize,color:getComputedStyle(e).color,background:getComputedStyle(e).backgroundColor}))'),ensure_ascii=True))
    browser.close()
