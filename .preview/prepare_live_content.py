"""Synchronise the approved allowlisted build into the isolated deployment checkout."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'public'
DEPLOY = ROOT / '.preview/deploy-content-sept'
TARGET = DEPLOY / 'public'
assert DEPLOY.resolve().is_relative_to(ROOT.resolve())
assert TARGET.resolve().parent == DEPLOY.resolve()
assert (DEPLOY / '.git').is_dir()
config_before = (DEPLOY / 'render.yaml').read_bytes()
files = {p.relative_to(SOURCE) for p in SOURCE.rglob('*') if p.is_file()}
removed = []
for path in TARGET.rglob('*'):
    if path.is_file() and path.relative_to(TARGET) not in files:
        assert path.resolve().is_relative_to(TARGET.resolve())
        removed.append(path.relative_to(TARGET).as_posix())
        path.unlink()
for relative in files:
    target = TARGET / relative
    assert target.resolve().is_relative_to(TARGET.resolve())
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE / relative, target)
for name in ('server.py', 'requirements.txt'):
    shutil.copy2(ROOT / name, DEPLOY / name)
assert config_before == (DEPLOY / 'render.yaml').read_bytes()
assert files == {p.relative_to(TARGET) for p in TARGET.rglob('*') if p.is_file()}
assert all((SOURCE / p).read_bytes() == (TARGET / p).read_bytes() for p in files)
print(json.dumps({'copied_public_files': len(files), 'removed_obsolete_files': len(removed), 'hosting_configuration': 'unchanged'}, indent=2))
