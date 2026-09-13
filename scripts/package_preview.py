"""Package only the built site and protected runtime for a new private repo."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
TARGET = ROOT / '.preview' / 'EchoFrame-protected-preview.zip'

assert (PUBLIC / 'index.html').exists(), 'Run python scripts/build.py first.'
assert TARGET.resolve().is_relative_to(ROOT / '.preview')
TARGET.parent.mkdir(exist_ok=True)

with ZipFile(TARGET, 'w', compression=ZIP_DEFLATED, compresslevel=6) as archive:
    for path in sorted(PUBLIC.rglob('*')):
        if path.is_file():
            archive.write(path, 'public/' + path.relative_to(PUBLIC).as_posix())
    for name in ['server.py', 'preview_server.py', 'requirements.txt']:
        archive.write(ROOT / name, name)
    archive.write(ROOT / 'render.preview.yaml', 'render.yaml')
    archive.write(ROOT / 'docs' / 'PROTECTED-PREVIEW.md', 'README.md')
    archive.writestr('.gitignore', '.env\n.env.*\n.contact-state/\n__pycache__/\n')

with ZipFile(TARGET) as archive:
    assert archive.testzip() is None, 'Archive integrity check failed.'
    assert not any(name.startswith(('.env', '.git/', '.contact-state/')) for name in archive.namelist())

print(TARGET)
print(f'{TARGET.stat().st_size / 1024 / 1024:.1f} MB; website and protected runtime only.')
