"""Password-protected team preview. Missing credentials never expose the site."""
import hmac
import os
from flask import request
from server import create_app


def create_preview_app(overrides=None):
    app = create_app(overrides)
    app.config.update(
        PREVIEW_USERNAME=os.getenv('PREVIEW_USERNAME', 'team'),
        PREVIEW_PASSWORD=os.getenv('PREVIEW_PASSWORD', ''),
    )
    if overrides:
        app.config.update(overrides)

    def configured():
        return bool(app.config['PREVIEW_USERNAME']) and len(app.config['PREVIEW_PASSWORD']) >= 16

    @app.before_request
    def require_preview_login():
        if not configured():
            return 'Preview access is not configured.', 503
        if request.path == '/_health':
            return None
        auth = request.authorization
        username = auth.username or '' if auth and auth.type == 'basic' else ''
        password = auth.password or '' if auth and auth.type == 'basic' else ''
        username_ok = hmac.compare_digest(username.encode(), app.config['PREVIEW_USERNAME'].encode())
        password_ok = hmac.compare_digest(password.encode(), app.config['PREVIEW_PASSWORD'].encode())
        if not (username_ok and password_ok):
            return 'Preview sign-in required.', 401, {
                'WWW-Authenticate': 'Basic realm="EchoFrame team preview", charset="UTF-8"',
            }

    @app.after_request
    def prevent_preview_caching(response):
        response.headers['X-Robots-Tag'] = 'noindex, nofollow, noarchive'
        response.headers['Cache-Control'] = 'private, no-store'
        response.vary.add('Authorization')
        return response

    @app.get('/_health')
    def health():
        return {'ok': True}

    return app


app = create_preview_app()
