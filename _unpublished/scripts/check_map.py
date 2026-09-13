"""Check public GIS aggregation, source exclusions and browser behaviour.

Run after scripts/build.py, with server.py listening on port 4173.
No external writes, deployments or contact requests are performed.
"""
import collections
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from map_data import assert_no_text, compact_geometry, EVENT_FIELDS

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'public/assets/gis-demo'
BASE = 'http://127.0.0.1:4173'


def read(name):
    return json.loads((DATA / name).read_text(encoding='utf-8'))


def check_data():
    catalogue = read('catalogue.json')
    boundaries = read('boundaries.json')
    original = json.loads((ROOT / 'docs/gis_demo/events.geojson').read_text(encoding='utf-8'))['features']
    lookup = {f['properties']['event_id']: f for f in original}
    assert len(catalogue['months']) == 24
    assert catalogue['months'][0] == '2024-10' and catalogue['months'][-1] == '2026-09'
    assert len(boundaries['municipalities']['features']) == 34
    assert len({q['question_id'] for q in catalogue['questions']}) == 20
    assert all(q['hindcast'] and q['provisional'] and q['indicative'] for q in catalogue['questions'])
    count = 0
    for i, month in enumerate(catalogue['months']):
        features = read(f'months/{month}.json')['features']
        expected = [f for f in original if f['properties']['first_seen'].startswith(month)]
        assert {f['properties']['event_id'] for f in features} == {f['properties']['event_id'] for f in expected}
        municipal = collections.Counter()
        state = collections.Counter()
        for f in features:
            p = f['properties']
            assert set(p) <= EVENT_FIELDS
            assert p == lookup[p['event_id']]['properties']
            if p['location_precision'] == 'state':
                assert f['geometry'] is None
                assert boundaries['states'][p['state']] == compact_geometry(lookup[p['event_id']]['geometry'])
            else:
                assert f['geometry'] == compact_geometry(lookup[p['event_id']]['geometry'])
                assert f['geometry']['type'] == 'Point'
            if p['corroboration_status'] == 'corroborated':
                state[p['state']] += 1
                if p['boundary_id']:
                    municipal[p['boundary_id']] += 1
        assert all(value == municipal[gid] for gid, value in catalogue['monthly_counts'][month].items())
        assert all(catalogue['state_counts'][s][i] == state[s] for s in catalogue['states'])
        count += len(features)
    assert count == 446
    for file in DATA.rglob('*.json'):
        assert_no_text(json.loads(file.read_text(encoding='utf-8')))
    for field in ['title', 'headline', 'text', 'body', 'reporter', 'actor', 'item_ids']:
        try:
            assert_no_text({'features': [{'properties': {field: 'must never pass'}}]})
        except ValueError:
            pass
        else:
            raise AssertionError(f'Forbidden field passed {field}')
    assets = catalogue['assets']['features']
    assert sum(f['geometry'] is None for f in assets) == 2
    assert all(f['properties']['radius_km'] == 25 for f in assets)
    assert all('backend/' not in (f['properties']['coordinate_source'] or '') for f in assets)
    for page in ['map.html', 'es/map.html']:
        content = (ROOT / 'public' / page).read_text(encoding='utf-8')
        assert '\u2014' not in content
        assert '5.24.0/maplibre-gl.js' in content
    print('Data checks passed for 446 events, 34 municipalities, 24 months and 20 question definitions')


def check_browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context(viewport={'width': 1440, 'height': 1000})
        page = context.new_page()
        errors, requests, resources = [], collections.Counter(), {}
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('request', lambda req: requests.update([req.url]))
        def measure(response):
            if response.ok:
                try:
                    resources[response.url] = len(response.body())
                except Exception:
                    pass
        page.on('response', measure)
        page.goto(BASE + '/map.html', wait_until='networkidle')
        page.wait_for_function("document.querySelector('[data-gis-demo]').dataset.loadedMonth === '2026-09'")
        page.wait_for_function("window.EchoFrameGIS.map && window.EchoFrameGIS.map.getLayer('event-points')")
        assert page.locator('#gis-event option').count() == 4
        assert page.evaluate("async () => (await EchoFrameGIS.map.getSource('points').getData()).features.every(f => f.geometry.type === 'Point' && f.properties.location_precision !== 'state')")
        assert page.evaluate("async () => (await EchoFrameGIS.map.getSource('states').getData()).features.every(f => ['Polygon','MultiPolygon'].includes(f.geometry.type))")
        assert page.evaluate("async () => (await EchoFrameGIS.map.getSource('states').getData()).features.length") == 1
        # Actual map click opens a state record. No state pin is involved.
        page.wait_for_function("EchoFrameGIS.map.isSourceLoaded('states')")
        target = page.evaluate("EchoFrameGIS.map.project([-64.4,9.3])")
        page.locator('#gis-map').click(position={'x': target['x'], 'y': target['y']})
        assert page.locator('#gis-detail h2').inner_text() == 'Event record'
        assert 'State' in page.locator('#gis-detail').inner_text()
        # Geodesic circle is 25 km in every direction.
        result = page.evaluate("""() => {
          const coords = EchoFrameGIS.circle({geometry:{coordinates:[-63,9]}}).geometry.coordinates[0];
          const r = x => x * Math.PI / 180;
          return coords.map(([lon,lat]) => 6371.0088 * 2 * Math.asin(Math.sqrt(Math.sin(r(lat-9)/2)**2 + Math.cos(r(lat))*Math.cos(r(9))*Math.sin(r(lon+63)/2)**2)));
        }""")
        assert all(abs(n - 25) < 0.00001 for n in result)
        # Unknown severity stays hollow. Contradiction never receives a solid fill.
        assert page.evaluate("EchoFrameGIS.eventPaint({severity:null,corroboration_status:'corroborated'}).fill") == 0
        assert page.evaluate("EchoFrameGIS.eventPaint({severity:'high',corroboration_status:'contradicted'}).fill") == 0
        assert page.evaluate("EchoFrameGIS.eventPaint({severity:'low',corroboration_status:'single_source'}).opacity") == .45
        assert page.evaluate("['low','medium','high'].map(severity => EchoFrameGIS.eventPaint({severity}).radius)") == [4, 7, 10]
        def select(index, month):
            page.locator('#gis-month').evaluate('(node, value) => {node.value=value; node.dispatchEvent(new Event("input"));}', index)
            page.wait_for_function('(month) => document.querySelector("[data-gis-demo]").dataset.loadedMonth === month', arg=month)
        select(0, '2024-10')
        assert page.locator('#gis-event option').count() == 10
        page.locator('#gis-asset').select_option('petropiar')
        assert page.locator('.gis-question').count() == 3
        assert 'Provisional' in page.locator('#gis-detail').inner_text()
        select(23, '2026-09')
        assert page.locator('.gis-question').count() == 0
        page.locator('#gis-asset').select_option('bloque_carabobo')
        assert 'Coordinates unresolved' in page.locator('#gis-detail').inner_text()
        select(0, '2024-10')
        assert 'No open questions' not in page.locator('#gis-detail').inner_text()
        # Explicit temporal fixture excludes future snapshots and expired questions.
        temporal = page.evaluate("""() => {
          const q={asset_id:'a',opened_at:'2024-01-01',resolution_date:'2024-03-31',series:[['2024-01-01',.2],['2024-03-01',.8]]};
          return [EchoFrameGIS.openQuestions([q],'a','2024-02-29')[0].snapshot[1], EchoFrameGIS.openQuestions([q],'a','2024-04-01').length,
            EchoFrameGIS.completedWeeks([['2024-02-26',4]],'2024-02-29').length];
        }""")
        assert temporal == [.2, 0, 0]
        # Play advances once loaded and can be paused without background advancement.
        page.locator('#gis-play').click()
        page.wait_for_function("document.querySelector('[data-gis-demo]').dataset.loadedMonth === '2024-11'")
        page.locator('#gis-play').click()
        assert page.locator('#gis-play').get_attribute('aria-pressed') == 'false'
        # Rapid changes must not let the previous request replace the final month.
        page.locator('#gis-month').evaluate('(node)=>{for(const n of [8,9,10,11,12]){node.value=n;node.dispatchEvent(new Event("input"));}}')
        page.wait_for_function("document.querySelector('[data-gis-demo]').dataset.loadedMonth === '2025-10'")
        page.wait_for_timeout(300)
        assert page.locator('#gis-month').input_value() == '12'
        assert 'October 2025' in page.locator('#gis-status').inner_text()
        # Cache keeps successful monthly files and shared geometry to one request each.
        assert requests[BASE + '/assets/gis-demo/months/2024-10.json'] == 1
        assert requests[BASE + '/assets/gis-demo/boundaries.json'] == 1
        assert requests[BASE + '/assets/gis-demo/catalogue.json'] == 1
        # Failed monthly data must not become a false zero or retain old points.
        page.route('**/months/2025-12.json', lambda route: route.fulfill(status=503, body='unavailable'))
        page.locator('#gis-month').evaluate('(node)=>{node.value=14;node.dispatchEvent(new Event("input"));}')
        page.wait_for_function("!document.querySelector('#gis-retry').hidden")
        assert 'No event count' in page.locator('#gis-status').inner_text()
        assert page.evaluate("async () => (await EchoFrameGIS.map.getSource('points').getData()).features.length") == 0
        page.unroute('**/months/2025-12.json')
        page.locator('#gis-retry').click()
        page.wait_for_function("document.querySelector('[data-gis-demo]').dataset.loadedMonth === '2025-12'")
        select(15, '2026-01')
        page.locator('#gis-asset').select_option('jose_complex')
        page.screenshot(path=str(ROOT / '.preview/map-desktop-checked.png'), full_page=True)
        # Budget covers all monthly files plus the measured page, fonts, library and basemap.
        page.wait_for_load_state('networkidle')
        local_data = sum(f.stat().st_size for f in DATA.rglob('*') if f.is_file())
        non_data = sum(size for url, size in resources.items() if '/assets/gis-demo/' not in url and '/months/' not in url)
        full_budget = local_data + non_data
        assert full_budget < 5_000_000, full_budget
        print(f'Complete data plus measured page resources {full_budget:,} bytes')
        (ROOT / '.preview/map-resource-sizes.json').write_text(json.dumps({'full_budget': full_budget, 'resources': resources}, indent=2), encoding='utf-8')
        # Both languages, minimum mobile widths, desktop and accessibility.
        for language in ['', 'es/']:
            page.goto(BASE + '/' + language + 'map.html', wait_until='networkidle')
            page.wait_for_function("document.querySelector('[data-gis-demo]').dataset.loadedMonth === '2026-09'")
            for width in [320, 390, 768, 1440]:
                page.set_viewport_size({'width': width, 'height': 900})
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth'), (language, width)
            if (ROOT / '.preview/axe.min.js').exists():
                page.add_script_tag(path=str(ROOT / '.preview/axe.min.js'))
                violations = page.evaluate("async()=> (await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})).violations.map(v=>v.id)")
                assert not violations, violations
        select(0, '2024-10')
        page.locator('#gis-asset').select_option('petropiar')
        assert page.locator('.gis-question p').first.inner_text().startswith('\u00bfOFAC')
        page.set_viewport_size({'width': 390, 'height': 844})
        page.screenshot(path=str(ROOT / '.preview/map-spanish-checked.png'), full_page=True)
        assert not errors, errors
        context.close()
        # Basemap outage falls back without losing WebGL map or record controls.
        context = browser.new_context()
        context.route('https://tiles.openfreemap.org/**', lambda route: route.abort())
        page = context.new_page(); page.goto(BASE + '/map.html', wait_until='networkidle')
        page.wait_for_function("document.querySelector('#gis-basemap').textContent.startsWith('No basemap')")
        assert page.evaluate("!!EchoFrameGIS.map.getLayer('event-points')")
        context.close()
        # CDN/WebGL failure still leaves a visible boundary map and usable details.
        context = browser.new_context()
        context.route('**/maplibre-gl.js', lambda route: route.abort())
        page = context.new_page(); page.goto(BASE + '/map.html', wait_until='networkidle')
        page.wait_for_selector('#gis-map.gis-map-fallback svg')
        page.locator('#gis-event').select_option(index=1)
        assert page.locator('#gis-detail h2').inner_text() == 'Event record'
        context.close(); browser.close()
        print('Browser checks passed for filtering, state polygons, details, probabilities, playback, caching, failures, layout and accessibility')


if __name__ == '__main__':
    check_data()
    check_browser()
