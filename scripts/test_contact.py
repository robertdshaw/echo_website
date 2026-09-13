"""Contact API and email-transport tests. No email leaves the test process."""
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch, MagicMock
import uuid

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from server import create_app, send_contact


class ContactTests(unittest.TestCase):
    def setUp(self):
        self.state=ROOT/'.preview'/('test-contact-'+uuid.uuid4().hex+'.sqlite3')
        self.sent=[]
        self.app=create_app({'TESTING':True,'STATE_PATH':self.state,'APP_SECRET':'test-secret-only','CONTACT_FROM':'website@example.com','CONTACT_TO':'desk@example.com','RESEND_API_KEY':'test-key','PUBLIC_ORIGIN':'http://localhost'},sender=lambda config,values,rid:self.sent.append((values,rid)))
        self.client=self.app.test_client()
        self.token=self.client.get('/api/contact/status').json['token']
        self.payload={'request_id':str(uuid.uuid4()),'token':self.token,'request_type':'Demo request','name':'Test Reader','email':'reader@example.com','organization':'Example Company','role':'Research director','headquarters':'London','phone':'+44 000 000','decision_test':'Enforceable contracts','sector':'Distressed debt & special situations','proof':'Test the political catalyst.\nShow contrary evidence.','question':'Please demonstrate the research workflow.\nSecond paragraph.','region':'Venezuela','perspective':'Distressed debt / hedge fund','subject':'Terminal A','deadline':'2027-06-30','format':'Focused research brief','referral':'Search','website':''}

    def tearDown(self):
        if self.state.exists(): self.state.unlink()

    def post(self,payload=None,origin='http://localhost'):
        return self.client.post('/api/contact',json=payload or self.payload,headers={'Origin':origin})

    def test_sends_every_detail_and_reply_is_successful(self):
        response=self.post()
        self.assertEqual(response.status_code,200)
        self.assertTrue(response.json['ok'])
        for key in ['name','email','organization','role','phone','headquarters','question','request_type','region','perspective','format','referral','deadline','subject','sector','proof','decision_test']:
            self.assertEqual(self.sent[0][0][key],self.payload[key])

    def test_contact_type_is_also_supported(self):
        self.payload['request_type']='Contact request'
        self.assertEqual(self.post().status_code,200)
        self.assertEqual(self.sent[0][0]['request_type'],'Contact request')

    def test_duplicate_is_not_sent_twice(self):
        self.assertEqual(self.post().status_code,200)
        response=self.post()
        self.assertTrue(response.json['duplicate'])
        self.assertEqual(len(self.sent),1)

    def test_changed_payload_cannot_reuse_receipt(self):
        self.post(); self.payload['name']='Changed Reader'
        self.assertEqual(self.post().status_code,409)
        self.assertEqual(len(self.sent),1)

    def test_missing_provider_never_reports_success(self):
        self.app.config.update(RESEND_API_KEY='',SMTP_HOST='',SMTP_USERNAME='',SMTP_PASSWORD='')
        self.assertFalse(self.client.get('/api/contact/status').json['ready'])
        self.assertEqual(self.post().status_code,503)
        self.assertFalse(self.sent)

    def test_cross_origin_and_forged_token_rejected(self):
        self.assertEqual(self.post(origin='https://unrelated.example').status_code,403)
        self.payload['token']='0.fake.invalid'
        self.assertEqual(self.post().status_code,403)
        self.assertFalse(self.sent)

    def test_required_fields_and_header_injection(self):
        self.payload['role']=''
        self.payload['sector']=''
        self.payload['email']='reader@example.com\r\nBcc: stranger@example.com'
        result=self.post()
        self.assertEqual(result.status_code,400)
        self.assertIn('role',result.json['fields'])
        self.assertIn('sector',result.json['fields'])
        self.assertIn('email',result.json['fields'])
        self.assertFalse(self.sent)

    def test_honeypot_and_oversized_requests(self):
        self.payload['website']='spam.example'
        self.assertEqual(self.post().status_code,400)
        self.payload['question']='x'*20000
        self.assertEqual(self.post().status_code,413)
        self.assertFalse(self.sent)

    def test_rate_limit_counts_requests_not_retries(self):
        for _ in range(5):
            self.payload['request_id']=str(uuid.uuid4())
            self.assertEqual(self.post().status_code,200)
        self.payload['request_id']=str(uuid.uuid4())
        self.assertEqual(self.post().status_code,429)
        self.assertEqual(len(self.sent),5)

    def test_state_database_contains_no_contact_details(self):
        self.post(); raw=self.state.read_bytes()
        self.assertNotIn(b'reader@example.com',raw)
        self.assertNotIn(b'Example Company',raw)
        self.assertNotIn(b'Test Reader',raw)

    def test_failed_transport_retains_unconfirmed_state(self):
        def failing(*args): raise RuntimeError('Sensitive provider error')
        app=create_app(dict(self.app.config),sender=failing)
        client=app.test_client()
        result=client.post('/api/contact',json=self.payload,headers={'Origin':'http://localhost'})
        self.assertEqual(result.status_code,502)
        self.assertNotIn('Sensitive',result.json['error'])
        self.assertEqual(client.post('/api/contact',json=self.payload,headers={'Origin':'http://localhost'}).status_code,409)

    def test_smtp_fixed_recipient_tls_and_reply_to(self):
        config=dict(self.app.config,RESEND_API_KEY='',SMTP_HOST='smtp.example.com',SMTP_PORT='587',SMTP_USERNAME='user',SMTP_PASSWORD='secret',SMTP_SECURITY='starttls')
        with patch('server.smtplib.SMTP') as smtp:
            connection=smtp.return_value.__enter__.return_value
            connection.send_message.return_value={}
            send_contact(config,self.payload,self.payload['request_id'])
            connection.starttls.assert_called_once()
            connection.login.assert_called_once_with('user','secret')
            message=connection.send_message.call_args.args[0]
            self.assertEqual(message['To'],'desk@example.com')
            self.assertEqual(message['Reply-To'],'reader@example.com')
            self.assertIn('Research director',message.get_content())
            self.assertIn('Sector: Distressed debt & special situations',message.get_content())
            self.assertIn(self.payload['proof'],message.get_content())
            self.assertIn('Requirement to explore: Enforceable contracts',message.get_content())
            self.assertIn('Phone: +44 000 000',message.get_content())

    def test_resend_request_contains_idempotency_and_reply_to(self):
        with patch('server.urllib.request.urlopen') as call:
            call.return_value.__enter__.return_value.read.return_value=b'{"id":"accepted-test"}'
            send_contact(self.app.config,self.payload,self.payload['request_id'])
            req=call.call_args.args[0]
            data=json.loads(req.data)
            self.assertEqual(data['to'],['desk@example.com'])
            self.assertEqual(data['reply_to'],'reader@example.com')
            self.assertIn('Role / team: Research director',data['text'])
            self.assertIn('Idempotency-key',req.headers)
            self.assertIn('Sector: Distressed debt & special situations',data['text'])
            self.assertIn(self.payload['proof'],data['text'])
            self.assertIn('Requirement to explore: Enforceable contracts',data['text'])

    def test_private_files_are_not_served_and_video_supports_range(self):
        self.assertEqual(self.client.get('/.env.local').status_code,404)
        self.assertEqual(self.client.get('/server.py').status_code,404)
        response=self.client.get('/images/EchoFramev3.mp4',headers={'Range':'bytes=0-99'})
        self.assertEqual(response.status_code,206)
        self.assertEqual(len(response.data),100)
        response.close()


if __name__=='__main__': unittest.main(verbosity=2)
