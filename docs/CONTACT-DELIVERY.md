# Contact email delivery

The demo/contact form submits every field to `/api/contact`. The server sends one email to the fixed `CONTACT_TO` address and sets Reply-To to the visitor's work email. Success means the email service accepted the message; it does not guarantee inbox placement. No visitor acknowledgement or calendar booking is sent automatically.

## Connect a provider

Copy `.env.example` to `.env.local`, which is ignored by Git and excluded from the public build. Enter secrets locally, never in browser JavaScript or shared screenshots.

- Set `CONTACT_TO` to the receiving inbox (currently `contact@echoframe.co`).
- Set `CONTACT_FROM` to a plain email address authorised by your sending service.
- Set `APP_SECRET` to a stable random secret of at least 32 bytes.
- For Resend, verify your sending domain and set `RESEND_API_KEY` to a sending API key. Its [official send API](https://resend.com/docs/api-reference/emails/send-email) describes sender and domain requirements.
- For SendGrid, verify a single sender or authenticate your sending domain, then set `SENDGRID_API_KEY` to an API key with Mail Send permission. The server posts to SendGrid's [v3 mail send endpoint](https://www.twilio.com/docs/sendgrid/api-reference/mail-send/mail-send) over HTTPS, so it works on hosting plans that block SMTP ports. `CONTACT_FROM` must match the verified sender or authenticated domain, or SendGrid rejects the message.
- For SMTP, leave `RESEND_API_KEY` and `SENDGRID_API_KEY` empty and set `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, and `SMTP_SECURITY` (`starttls`, normally port 587; or `ssl`, normally port 465). Use your provider's application credentials where required. Plaintext SMTP is unsupported.

Run `python scripts/build.py`, install `requirements.txt`, and run `python server.py`. Restart the server after changing environment values. Open `http://127.0.0.1:4173/briefing.html`. `/api/contact/status` reports `ready: true` when the required settings are present; this is a configuration check, not a test of credentials or domain verification.

With no provider connected, the page explains that sending is being connected and offers a populated email link. Clicking the main button cannot produce a false success message.

## Deployment

The Render blueprint now describes a Python web service, because a static host cannot deliver this form by itself. Deployment has not been performed. Set the same variables in Render's secret environment settings. The blueprint offers Resend and SendGrid; to use SMTP, remove both key entries and add the SMTP settings instead.

Render's [Free web services](https://render.com/docs/free) block common SMTP ports. Use an HTTPS sending API, either SendGrid or Resend, for the free protected preview, or a hosting plan that supports your SMTP provider's connection. SendGrid's own SMTP relay on port 587 is subject to that block; its HTTPS API is not.

When more than one provider is configured the server uses Resend first, then SendGrid, then SMTP. Set only the key for the provider you intend to use.

Set `PUBLIC_ORIGIN` to the exact public origin, such as `https://echoframe.co`, without a trailing slash. Redirect alternate domains to that origin. `TRUST_PROXY=true` is for the deployment's single trusted reverse proxy; omit it when running directly. Gunicorn runs one worker with four threads.

After connection, submit a real test using an inbox you control. Confirm the message arrives, includes all supplied details, identifies demo versus contact, and replying addresses the visitor. This live check has not yet been performed. Automated checks use mocked transports and send no email.

## Storage and practical limits

The website does not store raw form details. SQLite stores random request IDs, keyed payload digests, delivery states, timestamps, and keyed IP fingerprints for duplicate prevention and rate limits. Request records older than 24 hours and rate records older than one hour are pruned during submissions. Provider-held email copies are separate from website state.

This is a synchronous delivery service with a limit of five attempts per IP per hour. Shared corporate networks share that limit. State is local to the service instance; an ephemeral filesystem loses it on redeployment. A persistent disk or shared database is needed if these protections must survive instance replacement or scale across instances. Keep the application secret stable across restarts.

A timeout may occur after the provider has accepted a message. Such requests are marked unconfirmed and repeated delivery is blocked to avoid duplicates. The page preserves entered details and offers email as a fallback. There is no delivery queue, bounce webhook, automated newsletter subscription, or CRM integration.

## Verification

```powershell
python scripts/test_contact.py
python scripts/refinement_check.py
```

The browser check requires the local preview on port 4173 and Playwright Chromium. It mocks delivery responses. The backend checks validate all three mail transports, complete field forwarding, errors, duplicate requests, limits, origin checks, and private-file exclusion.
