"""Verify the team preview protects documents, assets, video, and contact API."""
import base64
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from preview_server import create_preview_app


class PreviewAccessTests(unittest.TestCase):
    def setUp(self):
        self.password = 'test-only-password-32-characters!'
        self.app = create_preview_app({'TESTING': True, 'PREVIEW_USERNAME': 'team', 'PREVIEW_PASSWORD': self.password})
        self.client = self.app.test_client()

    def authorization(self, username='team', password=None):
        value = username + ':' + (self.password if password is None else password)
        return {'Authorization': 'Basic ' + base64.b64encode(value.encode()).decode()}

    def test_every_site_resource_requires_login(self):
        for path in ['/', '/about.html', '/assets/site.css', '/assets/site.js', '/images/EchoFramev3.mp4', '/downloads/evidence-register.csv', '/api/contact/status', '/site.html', '/unknown']:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 401)
                self.assertIn('Basic realm=', response.headers['WWW-Authenticate'])
        self.assertEqual(self.client.post('/api/contact', json={}).status_code, 401)

    def test_wrong_and_malformed_credentials_do_not_pass(self):
        for headers in [self.authorization(password='wrong'), self.authorization(username='other'), {'Authorization': 'Bearer anything'}, {'Authorization': 'Basic !!'}, self.authorization(username='t\u00e9am')]:
            self.assertEqual(self.client.get('/', headers=headers).status_code, 401)

    def test_missing_or_short_password_fails_closed(self):
        for password in ['', 'short']:
            self.app.config['PREVIEW_PASSWORD'] = password
            for path in ['/', '/assets/site.js', '/_health']:
                self.assertEqual(self.client.get(path, headers=self.authorization()).status_code, 503)

    def test_valid_login_serves_page_and_video_ranges(self):
        with self.client.get('/', headers=self.authorization()) as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Power', response.data)
        with self.client.get('/images/EchoFramev3.mp4', headers={**self.authorization(), 'Range': 'bytes=0-99'}) as response:
            self.assertEqual(response.status_code, 206)
            self.assertEqual(len(response.data), 100)
        self.assertEqual(self.client.get('/api/contact/status', headers=self.authorization()).status_code, 200)
        self.assertEqual(self.client.get('/server.py', headers=self.authorization()).status_code, 404)

    def test_all_responses_are_private_and_not_indexed(self):
        for path, headers in [('/', {}), ('/', self.authorization()), ('/_health', {})]:
            with self.client.get(path, headers=headers) as response:
                self.assertIn('no-store', response.headers['Cache-Control'])
                self.assertIn('noindex', response.headers['X-Robots-Tag'])
                self.assertIn('Authorization', response.headers['Vary'])

    def test_health_endpoint_reveals_only_readiness(self):
        self.assertEqual(self.client.get('/_health').json, {'ok': True})
        self.assertEqual(self.client.get('/_health/').status_code, 401)

    def test_rotating_password_revokes_previous_access(self):
        self.app.config['PREVIEW_PASSWORD'] = 'new-test-only-password-32-characters!'
        self.assertEqual(self.client.get('/', headers=self.authorization()).status_code, 401)
        with self.client.get('/', headers=self.authorization(password=self.app.config['PREVIEW_PASSWORD'])) as response:
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)
