"""Prepare an update for the existing Render snapshot repository."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
TARGET = ROOT / '.preview' / 'EchoFrame-website-update.zip'
assert (PUBLIC / 'index.html').is_file(), 'Build the website first.'
TARGET.parent.mkdir(exist_ok=True)

instructions = '''EchoFrame website update

This updates the existing echoframe-team-preview repository.

1. Extract this ZIP into a temporary folder.
2. In GitHub Desktop, select echoframe-team-preview and click Show in Explorer.
3. Copy public/, server.py, and requirements.txt from the extracted folder into
   that repository folder. Replace matching files when prompted.
4. In GitHub Desktop, review Changes, enter a summary, and Commit to main.
5. Click Push origin.
6. In the existing Render service, choose Manual Deploy > Deploy latest commit
   if deployment does not start automatically.
7. Open the Render URL and confirm that the homepage has three claims below
   the opening image. Check that the enquiry form includes Sector and a
   question about what the first briefing should demonstrate.

The package contains generated website files and the updated contact handler.
It does not contain render.yaml, account credentials, or email credentials.
Your existing domain, public/protected access configuration, and environment
variables remain in place. No new Render service is needed.

Email delivery still requires your configured provider. Automated delivery
tests were mocked; this package does not establish that live email is working.

Edit source templates in the main website workspace and rebuild there for
future updates. This package is a deployable snapshot, not the source project.
'''

with ZipFile(TARGET, 'w', compression=ZIP_DEFLATED, compresslevel=6) as archive:
    for path in sorted(PUBLIC.rglob('*')):
        if path.is_file():
            archive.write(path, 'public/' + path.relative_to(PUBLIC).as_posix())
    for name in ['server.py', 'requirements.txt']:
        archive.write(ROOT / name, name)
    archive.writestr('UPDATE-INSTRUCTIONS.txt', instructions)

with ZipFile(TARGET) as archive:
    assert archive.testzip() is None
    assert 'render.yaml' not in archive.namelist()
    assert not any(name.startswith(('.env', '.git/', '.contact-state/')) for name in archive.namelist())
print(TARGET)
print(f'{TARGET.stat().st_size / 1024 / 1024:.1f} MB; existing deployment configuration preserved.')
