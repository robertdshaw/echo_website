"""Verify deployed bytes and the actual public map pages. Read-only requests."""
import hashlib
import json
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
LIVE = Path('C:/Users/rshaw/OneDrive/Documents/GitHub/echoframe-team-previe')
MANIFEST = json.loads((ROOT / '.preview/map-publish-manifest.json').read_text())
BASE = 'https://www.echoframe.co/'
expected = {}
for path in MANIFEST:
    data = subprocess.check_output(['git', 'show', f'HEAD:{path}'], cwd=LIVE)
    expected[path.removeprefix('public/')] = {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}

report = {'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=LIVE, text=True).strip(), 'pages': []}
with sync_playwright() as p:
    browser = p.chromium.launch()
    for relative in ['map.html', 'es/map.html']:
        context = browser.new_context(viewport={'width': 1440, 'height': 1000})
        page = context.new_page()
        resources, errors = {}, []
        def measure(response):
            if response.ok:
                try:
                    resources[response.url] = len(response.body())
                except Exception:
                    pass
        page.on('response', measure)
        page.on('pageerror', lambda error: errors.append(str(error)))
        response = page.goto('https://echoframe.co/' + relative, wait_until='networkidle', timeout=60000)
        assert response.status == 200, (response.status, page.url)
        page.wait_for_function("document.querySelector('[data-gis-demo]')?.dataset.loadedMonth === '2026-09'", timeout=30000)
        page.wait_for_function("window.EchoFrameGIS.map && window.EchoFrameGIS.map.getLayer('event-points')", timeout=30000)
        page.wait_for_function("document.querySelector('#gis-basemap').textContent.includes('OpenFreeMap')", timeout=30000)
        page.wait_for_function("document.querySelector('#gis-basemap').querySelector('a[href=\"https://www.openstreetmap.org/copyright\"]')")
        assert page.locator('#map-notes a[href="https://www.openstreetmap.org/copyright"]').count() == 1
        assert page.locator('#map-notes a[href$="gis-demo/LICENSE.txt"]').inner_text() == 'ODbL 1.0'
        assert page.locator('#gis-event option').count() == 4
        assert page.locator('#gis-asset option').count() == 15
        page.locator('#gis-month').evaluate('(el)=>{el.value=0;el.dispatchEvent(new Event("input"))}')
        page.wait_for_function("document.querySelector('[data-gis-demo]').dataset.loadedMonth === '2024-10'")
        page.locator('#gis-asset').select_option('petropiar')
        assert page.locator('.gis-question').count() == 3
        assert 'Provisional' in page.locator('#gis-detail').inner_text()
        page.wait_for_load_state('networkidle')
        data_size = sum(item['bytes'] for path, item in expected.items() if path.startswith('assets/gis-demo/'))
        other_size = sum(size for url, size in resources.items() if '/assets/gis-demo/' not in url)
        size = data_size + other_size
        assert size < 5_000_000, (relative, size)
        for width in [390, 1440]:
            page.set_viewport_size({'width': width, 'height': 1000})
            assert not page.evaluate('document.documentElement.scrollWidth > innerWidth')
        page.screenshot(path=str(ROOT / '.preview' / ('live-map-es.png' if relative.startswith('es') else 'live-map-en.png')), full_page=True)
        assert not errors, errors
        report['pages'].append({'url': page.url, 'status': response.status, 'complete_payload_bytes': size,
                                'all_gis_data_bytes': data_size, 'osm_attribution': True, 'odbl_link': True,
                                'basemap_credit': page.locator('#gis-basemap').inner_text(), 'resources': resources})
        context.close()
    context = browser.new_context()
    page = context.new_page()
    page.goto(BASE + 'venezuela.html', wait_until='domcontentloaded')
    link = page.get_by_role('link', name='See the map', exact=True)
    assert link.get_attribute('href') == 'map.html'
    report['venezuela_link'] = True
    # Read every deployed file, calculate its digest in the browser and compare
    # with the exact Git blob pushed to Render, including all 24 event months.
    hashes = page.evaluate('''async (paths) => {
      const results = [];
      for (let start = 0; start < paths.length; start += 4) {
        const batch = await Promise.all(paths.slice(start, start + 4).map(async path => {
          const response = await fetch('/' + path, {cache:'no-store'});
          const bytes = await response.arrayBuffer();
          const digest = await crypto.subtle.digest('SHA-256', bytes);
          return {path, status:response.status, bytes:bytes.byteLength,
            sha256:Array.from(new Uint8Array(digest)).map(n=>n.toString(16).padStart(2,'0')).join('')};
        }));
        results.push(...batch);
      }
      return results;
    }''', list(expected))
    for result in hashes:
        assert result['status'] == 200, result
        assert result['sha256'] == expected[result['path']]['sha256'], result['path']
    report['verified_files'] = hashes
    report['checked_at_utc'] = page.evaluate('new Date().toISOString()')
    context.close(); browser.close()
(ROOT / '.preview/map-live-verification.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('pages', 'verified_files')}))
for page in report['pages']:
    print(page['url'], page['status'], page['complete_payload_bytes'], 'bytes', 'OSM and ODbL verified')
print(len(report['verified_files']), 'live files match the published Git commit')
