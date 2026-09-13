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

To enable delivery, configure an authorised `CONTACT_FROM` and `RESEND_API_KEY` in the existing Render service, or supported authenticated SMTP settings. Following Rob's subsequent instruction, the application now fixes the recipient to `robert@echoframe.co`. Provider acceptance and inbox arrival still require a real delivery test after configuration. Until then, the form reports sending unavailable and retains the visitor's entries.

Owner markers were included in the initial revision. Rob subsequently requested their removal along with all unfinished-example areas; the cleanup below supersedes that presentation.

Deployment source [82db54b](https://github.com/EchoFrame-Ltd/echoframe-team-preview/commit/82db54b6da5ac7d4ef96f86f4c77c8ec56c25c20). [Render deployment](https://dashboard.render.com/web/srv-dai1fpm1egvs73d1qde0/deploys/dep-daj89b0ae00c73dut0cg).

## Recipient and copy follow-up

Deployment commit `cd3b52b` addresses requests to `robert@echoframe.co`, removes the sentence explaining that details will be emailed to the previous contact address, and keeps the privacy link. The confirmation no longer names the old recipient. The JavaScript-disabled contact address also uses Robert's address. All 14 server tests and the browser submission check passed with stub delivery; no message was sent.

## Unfinished-content cleanup

Deployment `0551ba9` removed the Venezuela rebuild notice and empty visualisation cards. Deployment `060b40c` removes all unfinished worked-example sections, public ROB notes and related promises of material to follow across the site. Unconfirmed article dates are omitted, and the pending About traction area is removed. Testimonials and the six risk-dimension names are retained. The content snapshot and generators reflect these removals.

All 28 pages passed local link and structure checks and browser checks at 1440px and 390px widths, with no JavaScript errors or horizontal overflow. A public-output scan found no remaining unfinished-example sections or ROB markers.
