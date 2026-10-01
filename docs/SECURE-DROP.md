# Secure drop

A private page for receiving redacted documents from one named sender.

## What it does

The sender opens `https://www.echoframe.co/drop/`, signs in and drops a folder of
documents onto the page. The page reads and redacts the documents inside the
sender's browser. Client names become a label for the type of company, people
become `[name]`, and email addresses, links and phone numbers are removed. When
the sender presses Send, only the redacted text is sent to this site, as one zip
file. The original documents never leave the sender's computer.

The owner signs in at the same address, downloads the zip and deletes it.

## What protects it

- Every `/drop/` address answers 404 until the sign-in variable is set.
- Two separate sign-ins. The sender can send. Only the owner can list, download
  or delete. The sender cannot read back anything that was sent.
- Passwords live only in the Render dashboard, never in the code. Five wrong
  attempts lock that address out for fifteen minutes.
- The sign-in cookie is HttpOnly, Secure and SameSite=Strict, scoped to `/drop`,
  and lasts eight hours. Changing a password signs that person out.
- The server refuses anything that is not the redaction page's own output. A
  Word or PDF file cannot be sent here by mistake.
- The page can only connect to this site and to Wikipedia's two lookup
  addresses, which it uses to work out what kind of company a client is. Only
  the client's name is sent there.
- Received files are not reachable by link. They are served only to the signed-in
  owner. Nothing is cached and the pages are marked noindex.

## Set it up

1. Deploy the site with `drop_endpoint.py` and the `drop_pages/` folder alongside
   `server.py`. `python scripts/package_update.py` now includes them.
2. In the Render dashboard, open the website service, go to Environment and add
   one variable:

   | Variable | Value |
   | --- | --- |
   | `DROP_USERS` | `sender-name:password,owner-name:password` |

   The first name and password are for the sender. The second are yours. Each
   password needs at least 12 characters and no commas.
3. Give the sender the address, the name and the password by phone or in person.

Password hashes can be used instead of plain passwords. Run
`python scripts/drop_password.py` and set `DROP_SENDER_USER`, `DROP_SENDER_HASH`,
`DROP_OWNER_USER` and `DROP_OWNER_HASH`.

## Where received files are kept

By default they go to `.drop-inbox/` next to `server.py`. Render clears that
folder on every deploy and restart, and a free instance clears it when it goes
to sleep. Either download as soon as the sender has finished, or attach a
persistent disk to the service and set `DROP_DIR` to a folder on it, for example
`/var/data/drop`.

## Take it down when the job is done

1. Sign in as the owner and press Delete everything.
2. Delete the `DROP_USERS` variable in Render. The feature is then off and every
   `/drop/` address answers 404.
3. If a disk was attached only for this, remove it.
4. To remove the code as well, delete `drop_endpoint.py`, `drop_pages/`,
   `scripts/drop_password.py`, `scripts/test_drop.py` and the two lines in
   `server.py` that register the blueprint.

## Check it

```
python scripts/test_drop.py
```
