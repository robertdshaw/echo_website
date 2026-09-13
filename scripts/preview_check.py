"""Local browser checks with an in-process email stub. No messages leave the test."""
import json
import sys
import threading
import uuid
from pathlib import Path
from werkzeug.serving import make_server, WSGIRequestHandler
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from server import create_app

class QuietHandler(WSGIRequestHandler):
    def log_request(self, *args, **kwargs): pass

sent = []
state = ROOT/'.preview'/('browser-contact-'+uuid.uuid4().hex+'.sqlite3')
app = create_app({'TESTING': True, 'STATE_PATH': state, 'APP_SECRET': 'browser-test-only',
                  'CONTACT_FROM': 'site@example.com', 'RESEND_API_KEY': 'stub-only'},
                 sender=lambda config, values, rid: sent.append((config['CONTACT_TO'], values, rid)))
http = make_server('127.0.0.1', 0, app, request_handler=QuietHandler)
base = f'http://127.0.0.1:{http.server_port}'
app.config['PUBLIC_ORIGIN'] = base
threading.Thread(target=http.serve_forever, daemon=True).start()
errors = []
overflow = []
try:
    with sync_playwright() as driver:
        browser = driver.chromium.launch()
        page = browser.new_page(viewport={'width':1440,'height':1000})
        page.emulate_media(reduced_motion='reduce')
        page.on('pageerror', lambda error: errors.append(str(error)))
        # Keep the browser check local. External sources and delivery are not exercised.
        page.route('**/*', lambda route: route.continue_() if route.request.url.startswith(base) else route.abort())
        paths = sorted(p.relative_to(ROOT/'public').as_posix() for p in (ROOT/'public').rglob('*.html'))
        for width in (1440,390):
            page.set_viewport_size({'width':width,'height':900})
            for path in paths:
                response=page.goto(base+'/'+path, wait_until='load')
                assert response.status==200, path
                assert page.locator('main h1').count()==1, path
                if page.evaluate('document.documentElement.scrollWidth > innerWidth + 2'): overflow.append((path,width))
            page.goto(base+'/index.html',wait_until='load')
            page.screenshot(path=str(ROOT/'.preview'/f'content-home-{width}.png'),full_page=True)
        page.set_viewport_size({'width':1100,'height':900})
        page.goto(base+'/briefing.html',wait_until='load')
        assert page.locator('#briefing-form input:not([name=website]), #briefing-form select, #briefing-form textarea').count()==8
        assert page.locator('#briefing-form button').count()==1
        assert page.locator('#email-draft, #contact-fallback, .optional-context').count()==0
        for name,value in {'name':'Browser Test','email':'reader@example.com','organization':'Test Organisation','role':'Research','question':'Please discuss our research scope.','details':'Additional background.\nA second paragraph.'}.items():
            page.locator(f'[name="{name}"]').fill(value)
        page.locator('[name=sector]').select_option(label='Oil & gas')
        page.locator('[name=referral]').select_option(label='Search')
        page.locator('.send-request').click()
        expect(page.locator('#contact-success')).to_be_visible()
        assert len(sent)==1
        assert sent[0][0]=='robert@echoframe.co'
        assert sent[0][1]['details']=='Additional background.\nA second paragraph.'
        assert page.locator('.send-request').is_hidden()
        page.screenshot(path=str(ROOT/'.preview'/'content-form-confirmation.png'),full_page=True)
        # Failed sending must retain the form and never display a success state.
        app.config['RESEND_API_KEY']=''
        app.config.update(SMTP_HOST='', SMTP_USERNAME='', SMTP_PASSWORD='')
        page.reload(wait_until='load')
        for name,value in {'name':'Browser Test','email':'reader@example.com','organization':'Test Organisation','question':'A delivery failure check.'}.items():
            page.locator(f'[name="{name}"]').fill(value)
        page.locator('[name=sector]').select_option(label='Other')
        page.locator('.send-request').click()
        expect(page.locator('#form-status')).to_contain_text('has not been sent')
        assert page.locator('#contact-success').is_hidden()
        assert page.locator('[name=question]').input_value()=='A delivery failure check.'
        assert len(sent)==1
        # Library controls remain useful after the article reduction.
        page.goto(base+'/research.html',wait_until='load')
        assert page.locator('.library-grid .research-card').count()==4
        page.locator('[data-filter="Europe"]').click()
        assert page.locator('.library-grid .research-card:visible').count()==1
        page.locator('[data-filter="All intelligence"]').click()
        page.locator('#research-search').fill('zz-no-match')
        expect(page.locator('#no-results')).to_be_visible()
        page.locator('#reset-search').click()
        assert page.locator('.library-grid .research-card:visible').count()==4
        # Keyboard-controlled navigation and methodology panels still work.
        page.goto(base+'/methodology.html',wait_until='load')
        page.locator('[data-evidence-state="corroborated"]').click()
        expect(page.locator('#evidence-title')).to_contain_text('Independent evidence')
        page.goto(base+'/decision-pathways.html',wait_until='load')
        page.locator('#entry-tab-1').click()
        expect(page.locator('#entry-panel-1')).to_be_visible()
        browser.close()
    result={'pages':len(paths),'viewports':[1440,390],'javascript_errors':errors,'horizontal_overflow':overflow,
            'form':'eight fields, confirmation, failure retention and fixed recipient passed with stub delivery',
            'research_filters':'passed','evidence_and_decision_controls':'passed','emails_sent':0}
    (ROOT/'.preview'/'content-browser-check.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
    assert not errors and not overflow
finally:
    http.shutdown()
    if state.exists(): state.unlink()
