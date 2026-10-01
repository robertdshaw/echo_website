"""Make a password hash for the secure drop sign-in.

Run it on your own machine:

    python scripts/drop_password.py

Type the password when asked. Nothing is saved. Copy the printed line into the
Render dashboard as DROP_SENDER_HASH or DROP_OWNER_HASH. Only the hash goes into
Render. Give the password itself to the person by phone or in person.
"""
import getpass
import sys

from werkzeug.security import generate_password_hash


def main():
    first = getpass.getpass("Password: ")
    if len(first) < 12:
        sys.exit("Use at least 12 characters.")
    if first != getpass.getpass("Again: "):
        sys.exit("The two entries did not match.")
    print(generate_password_hash(first))


if __name__ == "__main__":
    main()
