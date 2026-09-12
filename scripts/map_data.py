"""Prepare the approved GIS export for the static demo. No source stores are read."""
import csv
import datetime as dt
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = {'title', 'headline', 'text', 'body', 'reporter', 'actor', 'item_id', 'item_ids', 'actor_names'}
EVENT_FIELDS = {'event_id', 'first_seen', 'last_seen', 'family', 'type', 'severity',
                'corroboration_status', 'freshness', 'source_count', 'source_blocks',
                'physical_verdict', 'facility_id', 'boundary_id', 'state',
                'location_precision', 'point_in_state_polygon', 'source_protection_applied'}


def assert_no_text(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in FORBIDDEN:
                raise ValueError(f'Forbidden export field {key}')
            assert_no_text(child)
    elif isinstance(value, list):
        for child in value:
            assert_no_text(child)


def compact_geometry(value):
    if isinstance(value, float):
        return round(value, 5)
    if isinstance(value, list):
        return [compact_geometry(v) for v in value]
    if isinstance(value, dict):
        return {k: compact_geometry(v) for k, v in value.items()}
    return value


def build_map_data():
    source = ROOT / 'docs/gis_demo'
    dest = ROOT / 'assets/gis-demo'
    dest.mkdir(parents=True, exist_ok=True)
    generated = []

    def write(name, data):
        assert_no_text(data)
        file = dest / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':'), allow_nan=False), encoding='utf-8')
        generated.append(file.relative_to(ROOT).as_posix())

    def read(name):
        data = json.loads((source / name).read_text(encoding='utf-8'))
        assert_no_text(data)
        return data

    def rows(name):
        with (source / name).open(encoding='utf-8-sig', newline='') as file:
            result = list(csv.DictReader(file))
        assert_no_text(result)
        return result

    events = read('events.geojson')['features']
    # This snapshot covers parts of 25 calendar months. Display the latest 24.
    latest = max(r['month'] for r in rows('monthly_counts.csv'))
    end = dt.date.fromisoformat(latest + '-01')
    months = [f'{n // 12:04}-{n % 12 + 1:02}' for n in range(end.year * 12 + end.month - 24, end.year * 12 + end.month)]
    states = sorted({f['properties']['state'] for f in events})
    polygons = {}
    by_month = {month: [] for month in months}
    totals = {state: [0] * 24 for state in states}
    municipal = {month: defaultdict(int) for month in months}
    for row in rows('monthly_counts.csv'):
        if row['month'] in municipal:
            municipal[row['month']][row['boundary_id']] += int(row['status_corroborated'])
    for feature in events:
        p = {k: v for k, v in feature['properties'].items() if k in EVENT_FIELDS}
        precision = p['location_precision']
        if precision not in ('state', 'municipality', 'facility'):
            raise ValueError('Unapproved event precision')
        geometry = compact_geometry(feature['geometry'])
        if precision == 'state':
            if geometry['type'] not in ('Polygon', 'MultiPolygon'):
                raise ValueError('State event must have polygon geometry')
            if p['state'] in polygons and geometry != polygons[p['state']]:
                raise ValueError('Inconsistent state boundaries')
            polygons[p['state']] = geometry
            geometry = None  # Rejoined to shared state geometry in the browser.
        elif geometry['type'] != 'Point':
            raise ValueError('Unexpected point geometry')
        month = p['first_seen'][:7]
        if month in by_month:
            by_month[month].append({'type': 'Feature', 'geometry': geometry, 'properties': p})
            if p['corroboration_status'] == 'corroborated':
                totals[p['state']][months.index(month)] += 1
    for month, features in by_month.items():
        write(f'months/{month}.json', {'type': 'FeatureCollection', 'features': features})
    boundaries = read('municipalities.geojson')
    for f in boundaries['features']:
        f['properties'] = {k: f['properties'][k] for k in ('boundary_id', 'name', 'state')}
        f['geometry'] = compact_geometry(f['geometry'])
    write('boundaries.json', {'municipalities': boundaries, 'states': polygons})
    assets = read('assets.geojson')
    for f in assets['features']:
        p = f['properties']
        # Preserve source attribution without exporting internal paths or research notes.
        p['coordinate_source'] = next(iter(re.findall(r'https://[^\s)\x27]+', p['coordinate_source'] or '')), None)
        f['geometry'] = compact_geometry(f['geometry'])
    series = defaultdict(list)
    for row in rows('asset_series.csv'):
        series[row['asset_id']].append([row['week_start'], int(row['total'])])
    questions = {}
    for row in rows('question_series.csv'):
        if not all(row[k].lower() == 'true' for k in ('hindcast', 'provisional', 'indicative')):
            raise ValueError('Question labels must be preserved')
        key = row['question_id'] + '/' + row['client_profile']
        if key not in questions:
            questions[key] = {k: row[k] for k in ('question_id', 'client_profile', 'wording', 'asset_id', 'family', 'opened_at', 'resolution_date')}
            questions[key].update(hindcast=True, provisional=True, indicative=True, series=[])
        questions[key]['series'].append([row['timestamp'], float(row['probability'])])
    for q in questions.values():
        q['series'].sort()
        if any(not 0 <= value <= 1 for _, value in q['series']):
            raise ValueError('Invalid probability')
    write('catalogue.json', {'months': months, 'states': states, 'state_counts': totals,
                           'monthly_counts': municipal, 'assets': assets,
                           'asset_series': series, 'questions': list(questions.values()),
                           'export_as_of': '2026-09-12',
                           'last_event': max(f['properties']['first_seen'][:10] for f in events),
                           'event_counts': {m: len(v) for m, v in by_month.items()}})
    shutil.copy2(source / 'LICENSE.txt', dest / 'LICENSE.txt')
    generated.append('assets/gis-demo/LICENSE.txt')
    # All 24 months combined, not merely the first month's transfer.
    size = sum((ROOT / path).stat().st_size for path in generated)
    if size > 2_500_000:
        raise ValueError(f'Demo data exceeds its 2.5 MB share of the page budget ({size})')
    print(f'GIS demo data {size:,} bytes, {sum(map(len, by_month.values()))} events across 24 months')
    return generated


if __name__ == '__main__':
    build_map_data()
