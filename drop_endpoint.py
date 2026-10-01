"""Secure drop: a signed-in page for receiving redacted documents.

The sender opens /drop/, signs in, and drops a folder of documents onto the page.
All reading and redaction happens in the sender's browser. Only the redacted text
is sent here, as one zip file. The original documents are never uploaded.

The owner signs in at the same address, downloads what was sent, and deletes it.

The whole feature is off, and every /drop/ address answers 404, unless one
environment variable is set (in the Render dashboard, never in source control):

    DROP_USERS   sender-name:password,owner-name:password

The first name is the person sending. The second is the person receiving.
Each password needs at least 12 characters and no commas.

Instead of DROP_USERS, password hashes can be used (scripts/drop_password.py):
DROP_SENDER_USER, DROP_SENDER_HASH, DROP_OWNER_USER, DROP_OWNER_HASH.

Optional:

    DROP_FIRM    the sender's own firm, as name,email-domain  (for example
                 Acme Advisory,acme-advisory.com). The page then never treats
                 that firm as a client. Kept here so the name is not in the code.

    DROP_DIR           where received files are kept. Default ./.drop-inbox
                       Render wipes the disk on every deploy and restart unless a
                       persistent disk is attached. Point this at the disk's mount
                       path, or download promptly.

To remove the feature, delete the variable. See docs/SECURE-DROP.md.
"""

import hashlib
import hmac
import io
import os
import re
import secrets
import threading
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from flask import Blueprint, Response, abort, current_app, jsonify, redirect, request, send_file
from itsdangerous import BadSignature, URLSafeTimedSerializer
from werkzeug.security import check_password_hash, generate_password_hash

ROOT = Path(__file__).resolve().parent
PAGES = ROOT / "drop_pages"
drop = Blueprint("drop", __name__, url_prefix="/drop")

COOKIE = "drop_session"
SESSION_SECONDS = 8 * 3600
MAX_UPLOAD = 200 * 1024 * 1024
MAX_UNPACKED = 1024 * 1024 * 1024
MAX_FILES_KEPT = 200
LOGIN_TRIES = 5
LOGIN_WINDOW = 15 * 60
# The redaction page produces exactly these files. Anything else is refused,
# so an original document cannot be sent here by mistake.
ALLOWED_NAME = re.compile(r"^(redacted/\d{4,7}\.txt|index\.csv|client_labels\.csv|READ_ME\.txt)$")
FILE_ID = re.compile(r"^\d{8}-\d{6}-[0-9a-f]{8}$")
# Checked when the sign-in name is unknown, so both cases take the same time.
DUMMY_HASH = generate_password_hash(secrets.token_hex(16))

_failures = {}
_lock = threading.Lock()


def _config():
    c = {
        "sender_user": os.environ.get("DROP_SENDER_USER", "").strip(),
        "sender_hash": os.environ.get("DROP_SENDER_HASH", "").strip(),
        "owner_user": os.environ.get("DROP_OWNER_USER", "").strip(),
        "owner_hash": os.environ.get("DROP_OWNER_HASH", "").strip(),
        "dir": Path(os.environ.get("DROP_DIR") or (ROOT / ".drop-inbox")),
    }
    # The simple form: DROP_USERS = sender-name:password,owner-name:password
    pairs = [p.split(":", 1) for p in os.environ.get("DROP_USERS", "").split(",") if ":" in p]
    if len(pairs) == 2 and all(name.strip() and len(password.strip()) >= 12 for name, password in pairs):
        (sender, sender_password), (owner, owner_password) = pairs
        c.update(
            sender_user=sender.strip(), sender_hash="plain:" + sender_password.strip(),
            owner_user=owner.strip(), owner_hash="plain:" + owner_password.strip(),
        )
    return c


def _password_ok(stored, given):
    if stored.startswith("plain:"):
        return hmac.compare_digest(stored[6:].encode(), given.encode())
    try:
        return check_password_hash(stored, given)
    except ValueError:
        return False


def _enabled(c):
    return bool(
        c["sender_user"] and c["sender_hash"] and c["owner_user"] and c["owner_hash"]
        and c["sender_user"].lower() != c["owner_user"].lower()
    )


def _serializer():
    return URLSafeTimedSerializer(current_app.config["APP_SECRET"], salt="secure-drop")


def _mark(password_hash):
    # Changing a password signs everyone out.
    return hashlib.sha256(password_hash.encode()).hexdigest()[:16]


def _session():
    raw = request.cookies.get(COOKIE, "")
    if not raw:
        return None
    try:
        data = _serializer().loads(raw, max_age=SESSION_SECONDS)
    except BadSignature:
        return None
    c = _config()
    role = data.get("r") if isinstance(data, dict) else None
    if role not in ("sender", "owner"):
        return None
    if not hmac.compare_digest(str(data.get("h", "")), _mark(c[role + "_hash"])):
        return None
    return data


def _local():
    return request.host.split(":")[0] in ("127.0.0.1", "localhost")


def _same_origin():
    origin = request.headers.get("Origin")
    if not origin:
        return request.headers.get("Sec-Fetch-Site") in (None, "same-origin", "none")
    return origin == request.host_url.rstrip("/")


def _token_ok(session):
    sent = request.headers.get("X-Drop-Token", "")
    return bool(sent) and hmac.compare_digest(sent, str(session.get("c", "")))


def _client():
    return request.remote_addr or "unknown"


def _page(name, csp):
    response = Response((PAGES / name).read_bytes(), mimetype="text/html")
    response.headers["Content-Security-Policy"] = csp
    return response


PAGE_CSP = "default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'"
TOOL_CSP = (
    "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data: blob:; "
    "connect-src 'self' https://www.wikidata.org https://en.wikipedia.org; form-action 'none'; "
    "frame-ancestors 'none'; base-uri 'none'"
)


@drop.before_request
def _gate():
    if not _enabled(_config()):
        abort(404)
    if request.endpoint == "drop.upload":
        request.max_content_length = MAX_UPLOAD
    if request.method == "POST" and not _same_origin():
        return jsonify(error="Please use this from the page itself."), 403
    return None


@drop.after_request
def _headers(response):
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Robots-Tag"] = "noindex, nofollow, noarchive"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response


@drop.get("/")
def home():
    session = _session()
    if not session:
        return redirect("/drop/login")
    if session["r"] == "owner":
        return redirect("/drop/inbox")
    return _page("tool.html", TOOL_CSP)


@drop.get("/tool")
def tool():
    if not _session():
        return redirect("/drop/login")
    return _page("tool.html", TOOL_CSP)


@drop.get("/login")
def login_page():
    return _page("login.html", PAGE_CSP)


@drop.post("/login")
def login():
    c = _config()
    who = _client()
    now = time.time()
    with _lock:
        recent = [t for t in _failures.get(who, []) if now - t < LOGIN_WINDOW]
        _failures[who] = recent
        blocked = len(recent) >= LOGIN_TRIES
    if blocked:
        return redirect("/drop/login?wait=1")
    username = (request.form.get("username") or "").strip()[:100]
    password = (request.form.get("password") or "")[:300]
    role = None
    if username and hmac.compare_digest(username.lower().encode(), c["sender_user"].lower().encode()):
        role = "sender"
    elif username and hmac.compare_digest(username.lower().encode(), c["owner_user"].lower().encode()):
        role = "owner"
    good = _password_ok(c[role + "_hash"] if role else DUMMY_HASH, password)
    if not role or not good:
        with _lock:
            _failures.setdefault(who, []).append(now)
        return redirect("/drop/login?failed=1")
    with _lock:
        _failures.pop(who, None)
    token = _serializer().dumps({"r": role, "c": secrets.token_urlsafe(24), "h": _mark(c[role + "_hash"])})
    response = redirect("/drop/")
    response.set_cookie(COOKIE, token, max_age=SESSION_SECONDS, httponly=True, secure=not _local(), samesite="Strict", path="/drop")
    return response


@drop.post("/logout")
def logout():
    response = redirect("/drop/login")
    response.delete_cookie(COOKIE, path="/drop")
    return response


@drop.get("/api/session")
def session_info():
    session = _session()
    if not session:
        return jsonify(error="Sign in first."), 401
    parts = [p.strip() for p in os.environ.get("DROP_FIRM", "").split(",") if p.strip()]
    firm = {"name": parts[0][:80], "domains": [d.lower().lstrip("@")[:120] for d in parts[1:6]]} if parts else None
    return jsonify(role=session["r"], token=session["c"], firm=firm)


def _check_zip(data):
    """Return the number of redacted text files, or None if this is not what the page produces."""
    if len(data) < 22 or data[:2] != b"PK":
        return None
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            infos = archive.infolist()
            if not infos or len(infos) > 200000:
                return None
            total = 0
            documents = 0
            for info in infos:
                if info.is_dir():
                    continue
                if not ALLOWED_NAME.fullmatch(info.filename):
                    return None
                total += info.file_size
                if total > MAX_UNPACKED:
                    return None
                if info.filename.startswith("redacted/"):
                    documents += 1
            if documents == 0 or archive.testzip() is not None:
                return None
            return documents
    except (zipfile.BadZipFile, ValueError, RuntimeError, OSError):
        return None


@drop.post("/api/upload")
def upload():
    session = _session()
    if not session:
        return jsonify(error="Sign in first."), 401
    if not _token_ok(session):
        return jsonify(error="Please reload the page and try again."), 403
    data = request.get_data(cache=False)
    documents = _check_zip(data)
    if documents is None:
        return jsonify(error="Only the redacted copies made by this page can be sent."), 400
    folder = _config()["dir"]
    folder.mkdir(parents=True, exist_ok=True)
    if len(list(folder.glob("*.zip"))) >= MAX_FILES_KEPT:
        return jsonify(error="The inbox is full. Ask the recipient to clear it."), 507
    file_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + "-" + secrets.token_hex(4)
    temporary = folder / (file_id + ".part")
    temporary.write_bytes(data)
    try:
        os.chmod(temporary, 0o600)
    except OSError:
        pass
    os.replace(temporary, folder / (file_id + ".zip"))
    print(f"[drop] received {file_id}: {documents} documents, {len(data)} bytes", flush=True)
    return jsonify(ok=True, documents=documents, reference=file_id)


def _owner():
    session = _session()
    if not session:
        return None, (jsonify(error="Sign in first."), 401)
    if session["r"] != "owner":
        return None, (jsonify(error="Not available."), 403)
    return session, None


@drop.get("/inbox")
def inbox():
    session = _session()
    if not session:
        return redirect("/drop/login")
    if session["r"] != "owner":
        return redirect("/drop/")
    return _page("inbox.html", PAGE_CSP)


@drop.get("/api/list")
def list_files():
    session, error = _owner()
    if error:
        return error
    folder = _config()["dir"]
    rows = []
    for path in sorted(folder.glob("*.zip"), reverse=True) if folder.exists() else []:
        if not FILE_ID.fullmatch(path.stem):
            continue
        documents = 0
        try:
            with zipfile.ZipFile(path) as archive:
                documents = sum(1 for n in archive.namelist() if n.startswith("redacted/") and n.endswith(".txt"))
        except (zipfile.BadZipFile, OSError):
            pass
        stat = path.stat()
        rows.append({
            "id": path.stem,
            "received": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(timespec="seconds"),
            "bytes": stat.st_size,
            "documents": documents,
        })
    return jsonify(files=rows, token=session["c"])


@drop.get("/api/file/<file_id>")
def get_file(file_id):
    session, error = _owner()
    if error:
        return error
    if not FILE_ID.fullmatch(file_id):
        abort(404)
    path = _config()["dir"] / (file_id + ".zip")
    if not path.is_file():
        abort(404)
    return send_file(path, mimetype="application/zip", as_attachment=True, download_name=f"redacted-{file_id}.zip", max_age=0)


@drop.post("/api/delete")
def delete_files():
    session, error = _owner()
    if error:
        return error
    if not _token_ok(session):
        return jsonify(error="Please reload the page and try again."), 403
    body = request.get_json(silent=True) or {}
    folder = _config()["dir"]
    removed = 0
    if body.get("all") is True:
        targets = [p for p in folder.glob("*.zip")] + [p for p in folder.glob("*.part")] if folder.exists() else []
    else:
        file_id = str(body.get("id", ""))
        if not FILE_ID.fullmatch(file_id):
            return jsonify(error="Unknown file."), 400
        targets = [folder / (file_id + ".zip")]
    for path in targets:
        try:
            path.unlink()
            removed += 1
        except FileNotFoundError:
            pass
    print(f"[drop] deleted {removed} file(s)", flush=True)
    return jsonify(ok=True, removed=removed)
