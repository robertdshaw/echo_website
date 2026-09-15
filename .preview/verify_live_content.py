from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime
import hashlib
import json
import subprocess
import sys
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://www.echoframe.co/'
PUBLIC = ROOT/'public'
TEXT_TYPES = {'.html', '.css', '.js', '.json', '.svg', '.md', '.csv', '.txt'}
def get(path, extra=None):
    headers={'Cache-Control':'no-cache', 'User-Agent':'EchoFrame-deployment-verification'}
    headers.update(extra or {})
    try:
        with urllib.request.urlopen(urllib.request.Request(BASE+path,headers=headers), timeout=40) as response:
            return response.status, response.read(), dict(response.headers)
    except urllib.error.HTTPError as error:
        return error.code, error.read(), dict(error.headers)
def canonical(body, path):
    return body.replace(b'\r\n', b'\n') if path.suffix in TEXT_TYPES else body
status, home, _ = get('index.html')
matches = status == 200 and canonical(home, Path('index.html')) == canonical((PUBLIC/'index.html').read_bytes(), Path('index.html'))
if not matches:
    print(json.dumps({'live_revision':'previous build still served', 'status':status}))
    sys.exit(2)
if '--probe' in sys.argv:
    print(json.dumps({'live_revision':'approved build now served'}))
    sys.exit(0)
files = sorted(p for p in PUBLIC.rglob('*') if p.is_file())
def check(path):
    relative=path.relative_to(PUBLIC).as_posix()
    if path.suffix == '.mp4':
        code, body, headers=get(relative,{'Range':'bytes=0-1023'})
        with path.open('rb') as file: expected=file.read(1024)
        return relative, code == 206 and body == expected
    code, body, _ = get(relative)
    return relative, code == 200 and canonical(body,path) == canonical(path.read_bytes(),path)
with ThreadPoolExecutor(max_workers=5) as executor:
    results=list(executor.map(check, files))
deleted=subprocess.check_output(['git','diff','HEAD^','HEAD','--diff-filter=D','--name-only'],cwd=ROOT/'.preview/deploy-content-sept').decode().splitlines()
removed=[path.removeprefix('public/') for path in deleted if path.startswith('public/')]
with ThreadPoolExecutor(max_workers=5) as executor:
    exclusions=list(executor.map(lambda path:(path,get(path)[0]),removed))
code, payload, _=get('api/contact/status')
ready=json.loads(payload).get('ready') if code == 200 else None
report={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'site':BASE, 'deployment_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT/'.preview/deploy-content-sept').decode().strip(),
        'public_files_checked':len(results),'public_pages_checked':sum(p.suffix=='.html' for p in files),
        'content_mismatches':[path for path,ok in results if not ok],
        'removed_paths_checked':len(exclusions),'removal_failures':[(path,code) for path,code in exclusions if code!=404],
        'video_range_verified':dict(results).get('images/EchoFramev3.mp4'),
        'contact_ready':ready,'emails_sent':0}
(ROOT/'.preview/live-content-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
assert not report['content_mismatches'] and not report['removal_failures']
