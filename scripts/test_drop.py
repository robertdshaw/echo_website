"""Secure drop tests. Run with: python scripts/test_drop.py"""
import io
import os
import shutil
import sys
import unittest
import uuid
import zipfile
from pathlib import Path
from unittest.mock import patch

from werkzeug.security import generate_password_hash

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import drop_endpoint
from server import app

ORIGIN = {'Origin': 'http://localhost'}


def make_zip(names=None):
    names = names or {'redacted/0001.txt': 'ID: 0001\n\n[Hedge fund 1] asked a question.', 'redacted/0002.txt': 'ID: 0002\n\ntext', 'index.csv': 'id\n0001\n', 'client_labels.csv': 'label\n', 'READ_ME.txt': 'x'}
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, text in names.items():
            archive.writestr(name, text)
    return buffer.getvalue()


class DropTests(unittest.TestCase):
    def setUp(self):
        self.folder = ROOT / '.preview' / ('test-drop-' + uuid.uuid4().hex)
        self.env = patch.dict(os.environ, {
            'DROP_SENDER_USER': 'sender', 'DROP_SENDER_HASH': generate_password_hash('sender-password-1'),
            'DROP_OWNER_USER': 'owner', 'DROP_OWNER_HASH': generate_password_hash('owner-password-1'),
            'DROP_DIR': str(self.folder),
        })
        self.env.start()
        drop_endpoint._failures.clear()
        self.client = app.test_client()

    def tearDown(self):
        self.env.stop()
        shutil.rmtree(self.folder, ignore_errors=True)

    def login(self, client, user, password):
        return client.post('/drop/login', data={'username': user, 'password': password}, headers=ORIGIN)

    def token(self, client):
        return client.get('/drop/api/session').json['token']

    def send(self, client, data=None, token=None):
        headers = dict(ORIGIN, **{'Content-Type': 'application/zip'})
        if token is not False:
            headers['X-Drop-Token'] = token or self.token(client)
        return client.post('/drop/api/upload', data=data if data is not None else make_zip(), headers=headers)

    def test_everything_is_404_until_configured(self):
        with patch.dict(os.environ, {'DROP_OWNER_HASH': ''}):
            for path in ('/drop/', '/drop/login', '/drop/inbox', '/drop/api/list', '/drop/api/session'):
                self.assertEqual(self.client.get(path).status_code, 404, path)
            self.assertEqual(self.client.post('/drop/api/upload', data=make_zip(), headers=ORIGIN).status_code, 404)

    def test_pages_need_a_sign_in(self):
        self.assertEqual(self.client.get('/drop/').status_code, 302)
        self.assertEqual(self.client.get('/drop/tool').status_code, 302)
        self.assertEqual(self.client.get('/drop/inbox').status_code, 302)
        self.assertEqual(self.client.get('/drop/api/list').status_code, 401)
        self.assertEqual(self.client.get('/drop/api/file/20260101-000000-abcdef12').status_code, 401)
        self.assertEqual(self.send(self.client, token='x').status_code, 401)

    def test_the_page_files_are_not_public(self):
        for path in ('/drop_pages/tool.html', '/drop_endpoint.py', '/.drop-inbox/x.zip'):
            self.assertEqual(self.client.get(path).status_code, 404, path)

    def test_wrong_password_and_lockout(self):
        for _ in range(5):
            self.assertIn('failed=1', self.login(self.client, 'sender', 'nope').headers['Location'])
        self.assertIn('wait=1', self.login(self.client, 'sender', 'sender-password-1').headers['Location'])
        self.assertEqual(self.client.get('/drop/api/session').status_code, 401)

    def test_unknown_name_is_refused(self):
        self.assertIn('failed=1', self.login(self.client, 'someone', 'sender-password-1').headers['Location'])

    def test_sender_can_send_but_not_read(self):
        self.assertEqual(self.login(self.client, 'sender', 'sender-password-1').headers['Location'], '/drop/')
        page = self.client.get('/drop/')
        self.assertEqual(page.status_code, 200)
        self.assertIn(b'Redact client names', page.data)
        self.assertIn("frame-ancestors 'none'", page.headers['Content-Security-Policy'])
        self.assertEqual(page.headers['Cache-Control'], 'no-store')
        sent = self.send(self.client)
        self.assertEqual(sent.status_code, 200)
        self.assertEqual(sent.json['documents'], 2)
        self.assertEqual(self.client.get('/drop/api/list').status_code, 403)
        self.assertEqual(self.client.get('/drop/api/file/' + sent.json['reference']).status_code, 403)
        self.assertEqual(self.client.post('/drop/api/delete', json={'all': True}, headers=dict(ORIGIN, **{'X-Drop-Token': self.token(self.client)})).status_code, 403)
        self.assertEqual(self.client.get('/drop/inbox').status_code, 302)
        self.assertEqual(len(list(self.folder.glob('*.zip'))), 1)

    def test_upload_needs_the_page_token_and_same_origin(self):
        self.login(self.client, 'sender', 'sender-password-1')
        self.assertEqual(self.send(self.client, token=False).status_code, 403)
        self.assertEqual(self.send(self.client, token='wrong').status_code, 403)
        token = self.token(self.client)
        cross = self.client.post('/drop/api/upload', data=make_zip(), headers={'Origin': 'https://evil.example', 'X-Drop-Token': token})
        self.assertEqual(cross.status_code, 403)
        self.assertFalse(self.folder.exists() and list(self.folder.glob('*.zip')))

    def test_only_redacted_output_is_accepted(self):
        self.login(self.client, 'sender', 'sender-password-1')
        self.assertEqual(self.send(self.client, data=b'not a zip at all, just bytes').status_code, 400)
        self.assertEqual(self.send(self.client, data=make_zip({'redacted/0001.txt': 'x', 'Client ToR.docx': 'original'})).status_code, 400)
        self.assertEqual(self.send(self.client, data=make_zip({'redacted/../../evil.txt': 'x'})).status_code, 400)
        self.assertEqual(self.send(self.client, data=make_zip({'index.csv': 'id\n'})).status_code, 400)
        self.assertFalse(self.folder.exists() and list(self.folder.glob('*.zip')))

    def test_owner_downloads_and_deletes(self):
        sender = app.test_client()
        self.login(sender, 'sender', 'sender-password-1')
        payload = make_zip()
        first = self.send(sender, data=payload).json['reference']
        self.send(sender, data=payload)
        self.assertEqual(self.login(self.client, 'owner', 'owner-password-1').status_code, 302)
        self.assertEqual(self.client.get('/drop/').headers['Location'], '/drop/inbox')
        self.assertEqual(self.client.get('/drop/inbox').status_code, 200)
        listing = self.client.get('/drop/api/list').json
        self.assertEqual(len(listing['files']), 2)
        self.assertEqual(listing['files'][0]['documents'], 2)
        got = self.client.get('/drop/api/file/' + first)
        self.assertEqual(got.status_code, 200)
        self.assertEqual(got.data, payload)
        self.assertIn('attachment', got.headers['Content-Disposition'])
        self.assertEqual(self.client.get('/drop/api/file/..%2F..%2Fserver.py').status_code, 404)
        self.assertEqual(self.client.get('/drop/api/file/20260101-000000-abcdef12').status_code, 404)
        headers = dict(ORIGIN, **{'X-Drop-Token': listing['token']})
        self.assertEqual(self.client.post('/drop/api/delete', json={'id': first}, headers=ORIGIN).status_code, 403)
        self.assertEqual(self.client.post('/drop/api/delete', json={'id': first}, headers=headers).json['removed'], 1)
        self.assertEqual(len(self.client.get('/drop/api/list').json['files']), 1)
        self.assertEqual(self.client.post('/drop/api/delete', json={'all': True}, headers=headers).json['removed'], 1)
        self.assertEqual(list(self.folder.glob('*')), [])

    def test_changing_a_password_signs_that_person_out(self):
        self.login(self.client, 'sender', 'sender-password-1')
        self.assertEqual(self.client.get('/drop/api/session').status_code, 200)
        with patch.dict(os.environ, {'DROP_SENDER_HASH': generate_password_hash('a-new-password-2')}):
            self.assertEqual(self.client.get('/drop/api/session').status_code, 401)

    def test_single_setting_form(self):
        blank = {'DROP_SENDER_USER': '', 'DROP_SENDER_HASH': '', 'DROP_OWNER_USER': '', 'DROP_OWNER_HASH': ''}
        with patch.dict(os.environ, dict(blank, DROP_USERS='too:short,also:short')):
            self.assertEqual(self.client.get('/drop/login').status_code, 404)
        with patch.dict(os.environ, dict(blank, DROP_USERS='alex:first-long-password, sam:second-long-password')):
            self.assertIn('failed=1', self.login(self.client, 'alex', 'second-long-password').headers['Location'])
            self.assertEqual(self.login(self.client, 'alex', 'first-long-password').headers['Location'], '/drop/')
            self.assertEqual(self.send(self.client).status_code, 200)
            self.assertEqual(self.client.get('/drop/api/list').status_code, 403)
            owner = app.test_client()
            self.login(owner, 'sam', 'second-long-password')
            self.assertEqual(len(owner.get('/drop/api/list').json['files']), 1)

    def test_sign_out(self):
        self.login(self.client, 'owner', 'owner-password-1')
        self.assertEqual(self.client.post('/drop/logout', headers=ORIGIN).status_code, 302)
        self.assertEqual(self.client.get('/drop/api/list').status_code, 401)

    def test_cookie_is_locked_down(self):
        response = self.client.post('/drop/login', data={'username': 'owner', 'password': 'owner-password-1'}, headers={'Origin': 'https://www.echoframe.co'}, base_url='https://www.echoframe.co')
        cookie = response.headers['Set-Cookie']
        for part in ('HttpOnly', 'Secure', 'SameSite=Strict', 'Path=/drop'):
            self.assertIn(part, cookie)

    def test_the_rest_of_the_site_still_answers(self):
        self.assertEqual(self.client.get('/api/contact/status').status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=1)
