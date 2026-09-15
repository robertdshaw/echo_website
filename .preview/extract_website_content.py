import csv
import io
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Comment, NavigableString

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
OUT = ROOT / 'EchoFrame-Website-Content.md'
BASE = 'https://www.echoframe.co/'

def clean(s):
    return re.sub(r'\s+', ' ', s).strip()

def tidy(s):
    s = re.sub(r'[ \t]+\n', '\n', s)
    return re.sub(r'\n{3,}', '\n\n', s).strip()

def render(node, url, depth=0):
    if isinstance(node, Comment):
        return ''
    if isinstance(node, NavigableString):
        return re.sub(r'\s+', ' ', str(node))
    tag = node.name
    classes = node.get('class', [])
    if tag in ('script', 'style', 'template') or 'contact-honeypot' in classes:
        return ''
    if node.get('aria-hidden') == 'true' and tag != 'svg':
        return ''
    if tag == 'svg':
        words = [clean(t.get_text(' ', strip=True)) for t in node.select('title, desc, text')]
        return '\n\n' + ' / '.join(words) + '\n\n' if words else ''
    if tag == 'img':
        src = node.get('src')
        return '\n\n[Image' + (': ' + node['alt'] if node.get('alt') else '') + '](' + urljoin(url, src) + ')\n\n' if src else ''
    if tag in ('video', 'audio'):
        sources = [node.get('src')] + [s.get('src') for s in node.find_all('source')]
        return '\n\n' + '\n\n'.join(f'[{tag.capitalize()}]({urljoin(url, s)})' for s in dict.fromkeys(sources) if s) + '\n\n'
    if tag == 'iframe':
        return '\n\n[' + node.get('title', 'Embedded media') + '](' + urljoin(url, node.get('src', '')) + ')\n\n'
    if tag == 'br':
        return ' '
    if tag == 'hr':
        return '\n\n---\n\n'
    if tag == 'input':
        if node.get('type') == 'hidden':
            return ''
        placeholder = node.get('placeholder', '')
        return ' (' + placeholder + ')' if placeholder else ''
    if tag == 'textarea':
        return ' (' + node.get('placeholder', '') + ')' if node.get('placeholder') else ''
    if tag == 'select':
        options = node.find_all('option')
        return '\n\nOptions: ' + '; '.join(clean(o.get_text()) for o in options) + '\n\n' if options else ''
    if tag == 'table':
        rows = [[clean(render(c, url)) for c in r.find_all(['th', 'td'], recursive=False)] for r in node.find_all('tr')]
        rows = [r for r in rows if r]
        if not rows:
            return ''
        width = max(map(len, rows))
        rows = [[v.replace('|', '\\|') for v in r] + [''] * (width - len(r)) for r in rows]
        rows.insert(1, ['---'] * width)
        return '\n\n' + '\n'.join('| ' + ' | '.join(r) + ' |' for r in rows) + '\n\n'
    if tag in ('ul', 'ol'):
        lines = []
        for i, li in enumerate(node.find_all('li', recursive=False), 1):
            text = tidy(''.join(render(c, url, depth+1) for c in li.children))
            marker = str(i) + '. ' if tag == 'ol' else '- '
            lines.append(marker + text.replace('\n', '\n  '))
        return '\n\n' + '\n'.join(lines) + '\n\n'
    text = ''.join(render(c, url, depth) for c in node.children)
    if re.fullmatch(r'h[1-6]', tag or ''):
        return '\n\n' + '#' * min(6, int(tag[1]) + 2) + ' ' + clean(text) + '\n\n'
    if tag == 'a':
        if 'brand' in classes:
            return '[EchoFrame](' + urljoin(url, node.get('href', '')) + ') '
        label = clean(text) or node.get('aria-label', '')
        if not label:
            return ''
        return '[' + label + '](' + urljoin(url, node.get('href', '')) + ') '
    if tag in ('strong', 'b'):
        return '**' + clean(text) + '** ' if clean(text) else ''
    if tag in ('em', 'i'):
        return '*' + clean(text) + '*' if clean(text) else ''
    if tag == 'summary':
        return '\n\n**' + clean(text) + '**\n\n'
    if tag == 'blockquote':
        return '\n\n' + '\n'.join('> ' + line for line in tidy(text).splitlines()) + '\n\n'
    if tag in ('p', 'div', 'section', 'article', 'aside', 'header', 'footer', 'nav', 'form', 'fieldset', 'figure', 'figcaption', 'details', 'label', 'legend', 'dt', 'dd', 'button', 'noscript'):
        return '\n\n' + text.strip() + '\n\n' if text.strip() else ''
    if 'hero-line' in classes:
        return clean(text) + ' '
    if tag in ('span', 'small', 'time', 'output'):
        return text + ' ' if text else ''
    return text

def js_object(source, name):
    start = re.search(r'\bconst\s+' + name + r'\s*=\s*', source).end()
    quote = None
    escaped = False
    level = 0
    for pos in range(start, len(source)):
        ch = source[pos]
        if quote:
            if escaped:
                escaped = False
            elif ch == '\\':
                escaped = True
            elif ch == quote:
                quote = None
        elif ch in "'\"`":
            quote = ch
        elif ch in '{[':
            level += 1
        elif ch in '}]':
            level -= 1
            if level == 0:
                expr = source[start:pos+1]
                code = 'const vm=require("vm");process.stdout.write(JSON.stringify(vm.runInNewContext(' + json.dumps('(' + expr + ')') + ')));'
                result = subprocess.run(['node', '-e', code], capture_output=True, encoding='utf-8', check=True)
                return json.loads(result.stdout)
    raise ValueError(name)

pages = sorted(PUBLIC.rglob('*.html'), key=lambda p: (p.relative_to(PUBLIC).as_posix() != 'index.html', p.relative_to(PUBLIC).as_posix()))
parts = ['# EchoFrame website content', 'Content snapshot from the published-site files, 13 September 2026. Includes all 35 HTML pages in English and Spanish, interactive explanatory copy and downloadable text templates. Shared navigation and footer content appear once per variant. Original wording is preserved. Images and video are linked; no video transcript is available. Map geometry and individual event-data rows are linked rather than expanded into prose.']
parts.append('## Contents\n\n' + '\n'.join(f'- [{p.relative_to(PUBLIC).as_posix()}](#page-{i:02d})' for i, p in enumerate(pages, 1)))
shared = {}
soups = {}
for i, path in enumerate(pages, 1):
    rel = path.relative_to(PUBLIC).as_posix()
    url = urljoin(BASE, rel)
    soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    soups[rel] = soup
    title = soup.title.get_text().removesuffix(' | EchoFrame').strip()
    parts += [f'<a id="page-{i:02d}"></a>\n\n## {title}', f'Page: [{rel}]({url})', tidy(render(soup.find('main') or soup.body, url))]
    for selector, label in [('.topline', 'Announcement'), ('header.site-header', 'Navigation'), ('footer', 'Footer')]:
        node = soup.select_one(selector)
        if node:
            content = tidy(render(node, url))
            # Relative links differ by page; deduplicate by original rendered text.
            key = (label, clean(node.get_text(' ', strip=True)))
            if key not in shared:
                shared[key] = (label, rel, content)

parts.append('## Shared navigation and footer content')
for label, rel, content in shared.values():
    parts += [f'### {label}\n\nVariant shown on {rel}.', content]

source = (PUBLIC / 'assets/site.js').read_text(encoding='utf-8')
parts += ['## Interactive explanations', 'These alternatives appear when a visitor changes a selector or opens a tailored briefing form.']
objects = [('previewTopics', 'Research mandate previews'), ('consequences', 'Decision context'), ('evidenceStates', 'Evidence status'), ('audiencePresets', 'Briefing forms by audience'), ('sectorGuidance', 'Briefing guidance by sector'), ('generationMix', 'Electricity generation chart'), ('actorRecords', 'Fictional actor mapping'), ('pathwayRecords', 'Fictional decision pathways')]
for name, label in objects:
    values = js_object(source, name)
    parts.append('### ' + label)
    for key, value in values.items():
        parts.append('#### ' + key.replace('_', ' ').capitalize())
        strings = value.values() if isinstance(value, dict) else value if isinstance(value, list) else [value]
        for text in strings:
            if text.endswith('.html'):
                parts.append(f'[Related page]({urljoin(BASE, text)})')
            else:
                parts.append(text)
parts.append('### Historical exports chart')
for year, value in js_object(source, 'exportValues').items():
    parts.append(f'{year}: {value} barrels a day. The series describes historical exports, not current capacity.')

parts.append('## Map question wording')
parts.append('The map labels these probability series as hindcast, provisional and indicative. Probabilities are not a track record. The following wording is taken from the published catalogue.')
catalogue = json.loads((PUBLIC / 'assets/gis-demo/catalogue.json').read_text(encoding='utf-8'))
seen = set()
for q in catalogue['questions']:
    if q['question_id'] in seen:
        continue
    seen.add(q['question_id'])
    parts += ['### ' + q['question_id'], q['wording']]
mapjs = (PUBLIC / 'assets/map.js').read_text(encoding='utf-8')
parts.append('### Preguntas en espa\u00f1ol')
for number, text in js_object(mapjs, 'questionES').items():
    parts.append(f'{number}. {text}')
parts.append('### Map interface copy / Texto de la interfaz')
pattern = r'''\bt\(('(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*"),\s*('(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*")\)'''
pairs = list(dict.fromkeys(re.findall(pattern, mapjs)))
for en, es in pairs:
    parts.append('- ' + en[1:-1].replace("\\'", "'") + ' / ' + es[1:-1].replace("\\'", "'"))
parts.append('### Map data downloads\n\n[Published map catalogue](https://www.echoframe.co/assets/gis-demo/catalogue.json)\n\n[Map data licence](https://www.echoframe.co/assets/gis-demo/LICENSE.txt)')

parts.append('## Downloadable text and templates')
for path in sorted((PUBLIC / 'downloads').iterdir()):
    if path.suffix not in ('.csv', '.md'):
        continue
    parts += ['### ' + path.name, f'[Download original]({urljoin(BASE, "downloads/" + path.name)})']
    text = path.read_text(encoding='utf-8-sig')
    if path.suffix == '.md':
        text = re.sub(r'(?m)^(#{1,6}) ', lambda m: '#' * min(6, len(m[1]) + 3) + ' ', text)
        parts.append(text.strip())
    else:
        rows = list(csv.reader(io.StringIO(text)))
        parts.append('Template fields\n\n' + '\n'.join('- ' + field for field in rows[0]))
        for row in rows[1:]:
            if row:
                parts.append(' | '.join(row))

OUT.write_text('\n\n---\n\n'.join(parts[:1]) + '\n\n' + tidy('\n\n'.join(parts[1:])) + '\n', encoding='utf-8')
print(json.dumps({'file': str(OUT), 'pages': len(pages), 'bytes': OUT.stat().st_size, 'words': len(OUT.read_text(encoding='utf-8').split()), 'questions': len(seen)}, indent=2))
