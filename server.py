"""Serve the public build and deliver visitor requests through configured email.

No contact details are written to the website's state database. Delivery receipts
contain only a random request identifier, keyed payload digest, and status.
"""
import hashlib
import hmac
import json
import os
import re
import secrets
import smtplib
import sqlite3
import ssl
import time
import urllib.error
import urllib.request
from contextlib import contextmanager
from email.message import EmailMessage
from pathlib import Path
from urllib.parse import urlsplit
from flask import Flask, jsonify, request, send_from_directory, redirect
from werkzeug.middleware.proxy_fix import ProxyFix

ROOT=Path(__file__).resolve().parent


def load_local_environment():
    path=ROOT/'.env.local'
    if path.exists():
        for line in path.read_text(encoding='utf-8').splitlines():
            if not line.strip() or line.lstrip().startswith('#') or '=' not in line:
                continue
            key,value=line.split('=',1); key=key.strip(); value=value.strip()
            if len(value)>1 and value[0]==value[-1] and value[0] in "\"'":
                value=value[1:-1]
            if re.fullmatch(r'[A-Z][A-Z0-9_]*',key) and value:
                os.environ.setdefault(key,value)


FIELDS={
    'name':('Full name',120,True), 'email':('Work email',200,True),
    'organization':('Organisation',160,True),
    'sector':('Sector',100,True), 'question':('Decision or question',3000,True),
    'details':('Additional details',3000,False), 'referral':('How they found EchoFrame',80,False),
}


def valid_email(value):
    return bool(re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?\.[A-Za-z]{2,63}",value)) and '..' not in value


def mail_configured(config):
    if not valid_email(config.get('CONTACT_FROM','')) or not valid_email(config.get('CONTACT_TO','')):
        return False
    return bool(config.get('RESEND_API_KEY') or config.get('SENDGRID_API_KEY') or (config.get('SMTP_HOST') and config.get('SMTP_USERNAME') and config.get('SMTP_PASSWORD') and config.get('SMTP_SECURITY') in ('ssl','starttls')))


def send_contact(config, values, request_id):
    subject=f"EchoFrame conversation request from {values['organization']}"
    body='New EchoFrame website request\n\n'+'\n'.join(f'{label}: {values[key] or "Not specified"}' for key,(label,_,_) in FIELDS.items())
    body+=f'\n\nRequest reference: {request_id}\nSubmitted: {time.strftime("%Y-%m-%d %H:%M:%S UTC",time.gmtime())}\n\nReply to this email to contact the visitor.\n'
    if config.get('RESEND_API_KEY'):
        payload={'from':config['CONTACT_FROM'],'to':[config['CONTACT_TO']], 'reply_to':values['email'],'subject':subject,'text':body}
        req=urllib.request.Request('https://api.resend.com/emails',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+config['RESEND_API_KEY'],'Content-Type':'application/json','Idempotency-Key':'contact-'+request_id},method='POST')
        with urllib.request.urlopen(req,timeout=20) as response:
            receipt=json.loads(response.read())
            if not receipt.get('id'):
                raise RuntimeError('Missing delivery acceptance receipt')
        return
    if config.get('SENDGRID_API_KEY'):
        # SendGrid's v3 send endpoint answers 202 with an empty body; the
        # accepted message identifier arrives in the X-Message-Id header.
        payload={'personalizations':[{'to':[{'email':config['CONTACT_TO']}]}],
                 'from':{'email':config['CONTACT_FROM']},
                 'reply_to':{'email':values['email']},
                 'subject':subject,
                 'custom_args':{'request_id':request_id},
                 'content':[{'type':'text/plain','value':body}]}
        req=urllib.request.Request('https://api.sendgrid.com/v3/mail/send',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+config['SENDGRID_API_KEY'],'Content-Type':'application/json'},method='POST')
        with urllib.request.urlopen(req,timeout=20) as response:
            if response.status!=202 or not response.headers.get('X-Message-Id'):
                raise RuntimeError('Missing delivery acceptance receipt')
        return
    message=EmailMessage()
    message['From']=config['CONTACT_FROM']; message['To']=config['CONTACT_TO']
    message['Reply-To']=values['email']; message['Subject']=subject
    message['Message-ID']=f'<{request_id}@{config["CONTACT_FROM"].split("@")[1]}>'
    message.set_content(body)
    context=ssl.create_default_context()
    port=int(config.get('SMTP_PORT',587))
    connection=smtplib.SMTP_SSL(config['SMTP_HOST'],port,timeout=20,context=context) if config.get('SMTP_SECURITY')=='ssl' else smtplib.SMTP(config['SMTP_HOST'],port,timeout=20)
    with connection as smtp:
        if config.get('SMTP_SECURITY')=='starttls':
            smtp.ehlo(); smtp.starttls(context=context); smtp.ehlo()
        smtp.login(config['SMTP_USERNAME'],config['SMTP_PASSWORD'])
        refused=smtp.send_message(message)
        if refused:
            raise RuntimeError('Recipient not accepted')


def create_app(overrides=None, sender=None):
    load_local_environment()
    app=Flask(__name__,static_folder=None)
    app.config.update(MAX_CONTENT_LENGTH=16000,CONTACT_TO='robert@echoframe.co',CONTACT_FROM=os.getenv('CONTACT_FROM',''),APP_SECRET=os.getenv('APP_SECRET') or secrets.token_hex(32),PUBLIC_ORIGIN=os.getenv('PUBLIC_ORIGIN',''),STATE_PATH=ROOT/'.contact-state'/'requests.sqlite3',RESEND_API_KEY=os.getenv('RESEND_API_KEY',''),SENDGRID_API_KEY=os.getenv('SENDGRID_API_KEY',''),SMTP_HOST=os.getenv('SMTP_HOST',''),SMTP_PORT=os.getenv('SMTP_PORT','587'),SMTP_USERNAME=os.getenv('SMTP_USERNAME',''),SMTP_PASSWORD=os.getenv('SMTP_PASSWORD',''),SMTP_SECURITY=os.getenv('SMTP_SECURITY','starttls'))
    if overrides:
        app.config.update(overrides)
    if os.getenv('TRUST_PROXY')=='true':
        app.wsgi_app=ProxyFix(app.wsgi_app,x_for=1,x_proto=1)
    deliver=sender or send_contact

    def digest(text):
        return hmac.new(app.config['APP_SECRET'].encode(),text.encode(),hashlib.sha256).hexdigest()

    @contextmanager
    def db():
        path=Path(app.config['STATE_PATH']); path.parent.mkdir(parents=True,exist_ok=True)
        conn=sqlite3.connect(path,timeout=5)
        conn.execute('CREATE TABLE IF NOT EXISTS requests (id TEXT PRIMARY KEY, digest TEXT, state TEXT, created REAL)')
        conn.execute('CREATE TABLE IF NOT EXISTS rate (fingerprint TEXT, created REAL)')
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    @app.after_request
    def headers(response):
        response.headers['X-Content-Type-Options']='nosniff'
        response.headers['Referrer-Policy']='strict-origin-when-cross-origin'
        if request.path.startswith('/api/'):
            response.headers['Cache-Control']='no-store'
        return response

    @app.get('/api/contact/status')
    def status():
        stamp=f'{int(time.time())}.{secrets.token_hex(12)}'
        token=stamp+'.'+digest(stamp)
        return jsonify(ready=mail_configured(app.config),token=token)

    @app.post('/api/contact')
    def contact():
        origin=request.headers.get('Origin','')
        allowed_origin=app.config['PUBLIC_ORIGIN'] or request.host_url.rstrip('/')
        # Reverse proxies terminate HTTPS; an explicit PUBLIC_ORIGIN should be
        # configured on deployment. Local development uses the request origin.
        if origin!=allowed_origin or request.headers.get('Sec-Fetch-Site')=='cross-site':
            return jsonify(error='Please send your request from this website.'),403
        if not request.is_json:
            return jsonify(error='The request format was not recognised.'),415
        data=request.get_json(silent=True)
        if not isinstance(data,dict):
            return jsonify(error='Please check your request and try again.'),400
        token=data.get('token','')
        try:
            stamp,nonce,signature=token.split('.')
            age=time.time()-int(stamp)
            valid=0<=age<7200 and hmac.compare_digest(signature,digest(stamp+'.'+nonce))
        except (AttributeError,ValueError,TypeError):
            valid=False
        if not valid:
            return jsonify(error='This form has expired. Reload the page; your request has not been sent.',refresh=True),403
        if data.get('website'):
            return jsonify(error='The request could not be accepted.'),400
        values={}; errors={}
        for key,(label,limit,required) in FIELDS.items():
            value=data.get(key,'')
            if not isinstance(value,str):
                errors[key]=f'Please check {label.lower()}.'; continue
            value=value.strip()
            if (required and not value) or len(value)>limit or ('\n' in value or '\r' in value) and key not in ('question','details') or '\x00' in value:
                errors[key]=f'Please enter {label.lower()} (up to {limit} characters).'
            values[key]=value
        if not valid_email(values.get('email','')):
            errors['email']='Please enter a valid work email address.'
        if errors:
            return jsonify(error='Please check the highlighted details.',fields=errors),400
        request_id=data.get('request_id','')
        if not isinstance(request_id,str) or not re.fullmatch(r'[a-f0-9-]{36}',request_id):
            return jsonify(error='Please reload the form and try again.'),400
        if not mail_configured(app.config):
            return jsonify(error='Sending is temporarily unavailable. Your request has not been sent. Please try again later.'),503
        payload_digest=digest(json.dumps(values,sort_keys=True))
        fingerprint=digest(request.remote_addr or 'unknown')
        with db() as conn:
            conn.execute('BEGIN IMMEDIATE')
            conn.execute('DELETE FROM rate WHERE created < ?', (time.time()-3600,))
            conn.execute('DELETE FROM requests WHERE created < ?', (time.time()-86400,))
            previous=conn.execute('SELECT digest,state FROM requests WHERE id=?',(request_id,)).fetchone()
            if previous:
                if previous[0]!=payload_digest:
                    return jsonify(error='This request has changed. Please start a new request.'),409
                if previous[1]=='accepted':
                    return jsonify(ok=True,reference=request_id,duplicate=True)
                return jsonify(error='This request is already being processed or delivery could not be confirmed. Please contact us before sending it again.'),409
            attempts=conn.execute('SELECT count(*) FROM rate WHERE fingerprint=?',(fingerprint,)).fetchone()[0]
            if attempts>=5:
                return jsonify(error='Too many requests. Please try again in an hour or use the contact email.'),429
            conn.execute('INSERT INTO rate VALUES (?,?)',(fingerprint,time.time()))
            conn.execute('INSERT INTO requests VALUES (?,?,?,?)',(request_id,payload_digest,'processing',time.time()))
        try:
            deliver(app.config,values,request_id)
        except Exception:
            # Never expose provider errors, credentials, or the visitor's data.
            with db() as conn:
                conn.execute('UPDATE requests SET state=? WHERE id=?',('unconfirmed',request_id))
            return jsonify(error='We could not confirm delivery. Your details are still here. Please contact us directly before trying again.'),502
        with db() as conn:
            conn.execute('UPDATE requests SET state=? WHERE id=?',('accepted',request_id))
        return jsonify(ok=True,reference=request_id)

    @app.errorhandler(413)
    def oversized(error):
        return jsonify(error='Your message is too long. Please shorten it and try again.'),413

    @app.get('/site.html')
    def legacy():
        return redirect('/',code=301)

    @app.get('/methodology.html')
    def retired_methodology():
        # The methodology page was replaced by How it works; keep the old link alive.
        return redirect('/how-it-works.html',code=301)

    @app.get('/es/')
    @app.get('/es/index.html')
    def suspended_spanish():
        # The Spanish mirror is suspended. Send its links to the English home
        # page rather than answering 404 while the decision is open.
        return redirect('/',code=302)

    @app.get('/')
    @app.get('/<path:path>')
    def website(path='index.html'):
        if path.startswith('api/'):
            return jsonify(error='Endpoint not found'),404
        return send_from_directory(ROOT/'public',path,conditional=True)

    return app


app=create_app()

if __name__=='__main__':
    app.run(host='127.0.0.1',port=int(os.getenv('PORT','4173')),debug=False)
