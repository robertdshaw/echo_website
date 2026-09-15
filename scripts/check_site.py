"""Check the actual publication output: local links, fragments, images, and exclusions."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT=Path(__file__).resolve().parents[1]
PUBLIC=ROOT/'public'
errors=[]

class Document(HTMLParser):
    def __init__(self,text):
        super().__init__(); self.links=[]; self.ids=set(); self.duplicate_ids=[]; self.h1=0; self.lang=False
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='html': self.lang=bool(attrs.get('lang'))
        if tag=='h1': self.h1+=1
        if 'id' in attrs:
            if attrs['id'] in self.ids: self.duplicate_ids.append(attrs['id'])
            self.ids.add(attrs['id'])
        for attr in ('href','src'):
            if attrs.get(attr): self.links.append(attrs[attr])
        if tag=='img' and 'alt' not in attrs: errors.append('Image is missing alt text (use an empty alt for decorative imagery)')

documents={p:Document(p.read_text(encoding='utf-8')) for p in PUBLIC.rglob('*.html')}
for path,doc in documents.items():
    if not doc.lang: errors.append(f'{path.name}: missing language')
    if doc.h1!=1: errors.append(f'{path.name}: expected one h1, found {doc.h1}')
    if doc.duplicate_ids: errors.append(f'{path.name}: duplicate IDs {doc.duplicate_ids}')
    for link in doc.links:
        parts=urlsplit(link)
        if parts.scheme or parts.netloc: continue
        target=(path.parent/unquote(parts.path)).resolve() if parts.path else path.resolve()
        if target.is_dir(): target=target/'index.html'
        # A private page is served by the app from private/, never from public/.
        if not target.exists() and not (ROOT/'private'/link).exists():
            errors.append(f'{path.relative_to(PUBLIC)}: missing {link}')
        elif not target.exists():
            pass
        elif parts.fragment and target in documents and unquote(parts.fragment) not in documents[target].ids:
            errors.append(f'{path.relative_to(PUBLIC)}: missing fragment {link}')

for forbidden in ['admin.html','all-in-one-auth-system.html','gmtl-data-collection.html','latinnews-data-collection.html','content','docs',
                  '_unpublished','map.html','es/map.html','assets/gis-demo','assets/map.js','assets/map.css',
                  'downloads/sample-asset-access.md','downloads/sample-thesis-review.md']:
    target = PUBLIC / forbidden
    if target.is_file() or target.is_dir() and any(p.is_file() for p in target.rglob('*')):
        errors.append(f'Internal file published: {forbidden}')
for path in PUBLIC.rglob('*'):
    if path.is_file() and path.suffix in ('.html','.js'):
        content=path.read_text(encoding='utf-8')
        if '/auto-login?key=' in content or 'SUPABASE_KEY' in content: errors.append(f'Legacy credential flow in {path}')
        for private_plan_detail in ['El Pitazo','Ecoanalítica','Síntesis Financiera','772,000','763,000','scenario_bayes.py']:
            if private_plan_detail in content: errors.append(f'Internal plan detail published in {path.name}: {private_plan_detail}')
if errors: raise SystemExit('\n'.join(errors))
print(f'Passed: {len(documents)} HTML pages, local assets, fragment links, unique IDs, and publication exclusions.')
