# Live website deployment

The public domain is https://www.echoframe.co (echoframe.co redirects there).

Authoring workspace: this project, echo_website. Its origin remote is
robertdshaw/echo_website and is not the repository currently serving the new site.

Live deployment repository: EchoFrame-Ltd/echoframe-team-preview.
Local checkout: C:/Users/rshaw/OneDrive/Documents/GitHub/echoframe-team-previe
(the local directory name lacks the final w).

The live repository contains a prebuilt public/ directory, server.py,
requirements.txt, and its own render.yaml. Rebuild here, compare against that
checkout, and copy the intended publication changes there before committing and
pushing a live update. Preserve unrelated changes and deployment configuration.
A local build or ZIP alone does not publish to the public domain.

On 12 September 2026, the live repository already matched the arrow-free build,
but Render was serving an earlier commit. Commit 7319012 changes the live
Blueprint autoDeployTrigger from off to commit. At the last check, Render had
not yet started a deployment of that commit; a dashboard deployment was requested.
Confirm that the Blueprint is synced and Auto-Deploy is On Commit in Render.

Always verify the public URL and the served assets after deployment. Do not
report a local build, GitHub push, or configuration change as a completed live
deployment without checking the actual served site.
