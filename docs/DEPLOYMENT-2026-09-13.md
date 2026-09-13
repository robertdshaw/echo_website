# September content deployment

The approved revision is live at [www.echoframe.co](https://www.echoframe.co/). Rob authorised the push and deployment after the local content review.

- Authoring repository `robertdshaw/echo_website`, branch `content-fix-sept`, revision `49f24dc`. All eleven ordered content commits were pushed.
- Live repository `EchoFrame-Ltd/echoframe-team-preview`, branch `main`, deployment commit `82db54b6da5ac7d4ef96f86f4c77c8ec56c25c20`.
- Render deployment `dep-daj89b0ae00c73dut0cg` reported success at 11:11:26 UTC on 13 September 2026.
- Public-domain verification completed at 11:12:39 UTC. All 28 HTML pages and all 44 published files matched the approved local build, allowing only text line-ending differences. Video verification checked an HTTP range response against the original bytes.
- All 39 removed public paths returned HTTP 404, including both map pages, the map data and scripts, retired articles, Frame Bureau and invented sample downloads.
- The live repository's existing Render configuration was preserved. Deployment used an isolated checkout; unrelated authoring changes and the existing live checkout were left untouched.

## Contact delivery still requires configuration

The eight-field form and matching server are deployed. The production `/api/contact/status` endpoint returns `ready: false`, as it did before deployment. No email provider credentials were available in the local configuration or current environment. No email was sent during verification.

To enable delivery, configure an authorised `CONTACT_FROM` and `RESEND_API_KEY` in the existing Render service, or supported authenticated SMTP settings. The application fixes the recipient to `contact@echoframe.co`. Provider acceptance and inbox arrival still require a real delivery test after configuration. Until then, the form reports sending unavailable and retains the visitor's entries.

The owner markers for dates, quote permissions, channel naming, real redacted examples, visualisations and the Social dimension remain in the deployed content as approved.

Deployment source [82db54b](https://github.com/EchoFrame-Ltd/echoframe-team-preview/commit/82db54b6da5ac7d4ef96f86f4c77c8ec56c25c20). [Render deployment](https://dashboard.render.com/web/srv-dai1fpm1egvs73d1qde0/deploys/dep-daj89b0ae00c73dut0cg).
