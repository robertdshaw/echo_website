"""
Survey endpoint for the GMTL Venezuela regional coverage form.

Paste into server.py, or keep as its own module and register the blueprint:

    from survey_endpoint import survey
    app.register_blueprint(survey)

Environment variables (set these in the Render dashboard):

    SURVEY_STORE       path for the JSONL backup. Default ./data/survey_responses.jsonl
    SURVEY_EXPORT_KEY  secret string needed to download the CSV. No key means export is off.
    SMTP_HOST          e.g. smtp.fastmail.com. Leave unset to skip email.
    SMTP_PORT          default 587
    SMTP_USER
    SMTP_PASS
    SURVEY_TO          where each response is emailed, e.g. robert@echoframe.co
    SURVEY_FROM        defaults to SMTP_USER

Render's disk is wiped on every deploy unless you attach a persistent disk,
so treat email as the real delivery and the JSONL file as a convenience.
"""

import csv
import io
import json
import os
import smtplib
import ssl
import threading
from datetime import datetime, timezone
from email.message import EmailMessage

from flask import Blueprint, Response, abort, jsonify, request

survey = Blueprint("survey", __name__)

STORE = os.environ.get("SURVEY_STORE", "./data/survey_responses.jsonl")
EXPORT_KEY = os.environ.get("SURVEY_EXPORT_KEY", "")
MAX_BYTES = 64 * 1024

Q1_KEYS = [f"q1_{i}" for i in range(1, 7)]
FLAT_COLUMNS = (
    ["submitted_at", "role", "firm", "name", "email"]
    + Q1_KEYS
    + ["q2", "q3", "q4", "q5", "q5_other", "q6", "q7", "q7_comment"]
)


def _clean(value, limit=2000):
    if value is None:
        return ""
    return str(value).replace("\x00", "")[:limit]


def _flatten(row):
    r = row.get("respondent") or {}
    out = {
        "submitted_at": _clean(row.get("submitted_at"), 40),
        "role": _clean(r.get("role"), 200),
        "firm": _clean(r.get("firm"), 200),
        "name": _clean(r.get("name"), 200),
        "email": _clean(r.get("email"), 200),
    }
    q1 = row.get("q1") or {}
    for key in Q1_KEYS:
        entry = q1.get(key) or {}
        out[key] = _clean(entry.get("answer"), 10)
    out["q2"] = " | ".join(_clean(v, 300) for v in (row.get("q2") or []))
    out["q3"] = ", ".join(_clean(v, 60) for v in (row.get("q3") or []))
    out["q4"] = _clean(row.get("q4"))
    out["q5"] = ", ".join(_clean(v, 60) for v in (row.get("q5") or []))
    out["q5_other"] = _clean(row.get("q5_other"), 300)
    out["q6"] = _clean(row.get("q6"))
    out["q7"] = _clean(row.get("q7"), 20)
    out["q7_comment"] = _clean(row.get("q7_comment"))
    return out


def _as_text(flat):
    lines = ["GMTL Venezuela regional coverage survey", ""]
    lines.append(f"Received: {flat['submitted_at']}")
    lines.append(f"Role: {flat['role'] or 'not given'}")
    lines.append(f"Firm: {flat['firm'] or 'not given'}")
    if flat["name"] or flat["email"]:
        lines.append(f"Contact: {flat['name']} {flat['email']}".strip())
    lines += ["", "1. Would pay to have answered"]
    labels = [
        "Contract, licence or JV terms change",
        "Operates without a stoppage over 48 hours",
        "Security allows normal work",
        "Communities block or disrupt",
        "Governor, mayor or regional PDVSA management changes",
        "Workers and contractors are paid",
    ]
    for key, label in zip(Q1_KEYS, labels):
        lines.append(f"   {flat[key] or '-':<6} {label}")
    lines += [
        "",
        f"2. Assets or areas: {flat['q2'] or 'none given'}",
        f"3. Wants first: {flat['q3'] or 'none'}",
        "",
        "4. Decision in the next twelve months",
        f"   {flat['q4'] or 'none given'}",
        "",
        f"5. Information comes from: {flat['q5'] or 'none'}"
        + (f" ({flat['q5_other']})" if flat["q5_other"] else ""),
        "",
        "6. Missed in the last two years",
        f"   {flat['q6'] or 'none given'}",
        "",
        f"7. Probability would: {flat['q7'] or 'no answer'}",
    ]
    if flat["q7_comment"]:
        lines += ["", "Anything else", f"   {flat['q7_comment']}"]
    return "\n".join(lines)


def _email(flat):
    host = os.environ.get("SMTP_HOST")
    to = os.environ.get("SURVEY_TO")
    if not host or not to:
        return
    user = os.environ.get("SMTP_USER", "")
    msg = EmailMessage()
    who = flat["firm"] or flat["role"] or "anonymous"
    msg["Subject"] = f"Venezuela survey response: {who}"
    msg["From"] = os.environ.get("SURVEY_FROM", user)
    msg["To"] = to
    msg.set_content(_as_text(flat))
    try:
        with smtplib.SMTP(host, int(os.environ.get("SMTP_PORT", 587)), timeout=20) as s:
            s.starttls(context=ssl.create_default_context())
            if user:
                s.login(user, os.environ.get("SMTP_PASS", ""))
            s.send_message(msg)
    except Exception as exc:  # never fail the respondent's submission
        print(f"[survey] email failed: {exc}", flush=True)


ALLOWED_ORIGINS = {
    "https://survey.echoframe.co",
    "https://www.echoframe.co",
    "https://echoframe.co",
}


@survey.after_request
def _cors(resp):
    origin = request.headers.get("Origin", "")
    if origin in ALLOWED_ORIGINS:
        resp.headers["Access-Control-Allow-Origin"] = origin
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
        resp.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return resp


@survey.route("/api/survey", methods=["OPTIONS"])
def preflight():
    return ("", 204)


@survey.post("/api/survey")
def receive():
    raw = request.get_data(cache=False, as_text=False)
    if len(raw) > MAX_BYTES:
        abort(413)
    try:
        row = json.loads(raw.decode("utf-8"))
    except Exception:
        return jsonify({"ok": False, "error": "bad payload"}), 400
    if not isinstance(row, dict):
        return jsonify({"ok": False, "error": "bad payload"}), 400

    row["submitted_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    row["_ip"] = (request.headers.get("X-Forwarded-For", "") or "").split(",")[0].strip()
    flat = _flatten(row)

    try:
        os.makedirs(os.path.dirname(STORE) or ".", exist_ok=True)
        with open(STORE, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    except Exception as exc:
        print(f"[survey] write failed: {exc}", flush=True)

    threading.Thread(target=_email, args=(flat,), daemon=True).start()
    return jsonify({"ok": True})


@survey.get("/api/survey/export")
def export():
    if not EXPORT_KEY or request.args.get("key") != EXPORT_KEY:
        abort(404)
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=FLAT_COLUMNS, extrasaction="ignore")
    writer.writeheader()
    try:
        with open(STORE, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    writer.writerow(_flatten(json.loads(line)))
    except FileNotFoundError:
        pass
    return Response(
        buf.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=venezuela_survey.csv"},
    )
