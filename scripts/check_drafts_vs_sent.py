#!/usr/bin/env python3
"""
Check Gmail Drafts vs Sent — audit and optional cleanup.
Lists which draft recipients have already been contacted (Sent folder)
and which are new.

Usage:
    python scripts/check_drafts_vs_sent.py              # read-only audit
    python scripts/check_drafts_vs_sent.py --delete-sent # delete drafts already sent + test draft
"""

import argparse
import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv not installed. Run: pip install python-dotenv")
    sys.exit(1)

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("ERROR: Google libraries not installed.")
    print("Run: pip install google-auth-oauthlib google-api-python-client")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

TEST_EMAIL = "p3@x.de"

SCOPES_READONLY = ["https://www.googleapis.com/auth/gmail.readonly"]
SCOPES_MODIFY = ["https://www.googleapis.com/auth/gmail.modify"]
CREDENTIALS_FILE = PROJECT_ROOT / os.getenv("GMAIL_CREDENTIALS_JSON", "credentials.json")
TOKEN_FILE = PROJECT_ROOT / "token.json"


def get_gmail_service(modify=False):
    scopes = SCOPES_MODIFY if modify else SCOPES_READONLY
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), scopes)
        # Re-auth if existing token lacks modify scope
        if modify and creds and "gmail.modify" not in " ".join(creds.scopes or []):
            creds = None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print(f"ERROR: credentials.json nicht gefunden: {CREDENTIALS_FILE}")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), scopes)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def extract_email(header_value: str) -> str | None:
    if not header_value:
        return None
    val = header_value.strip()
    if "<" in val and ">" in val:
        return val.split("<")[1].split(">")[0].strip().lower()
    return val.lower() if "@" in val else None


def get_draft_recipients(service) -> dict[str, dict]:
    """Return {email: {subject, draft_id}} for all drafts with a recipient."""
    drafts = {}
    page_token = None
    while True:
        params = {"userId": "me", "maxResults": 100}
        if page_token:
            params["pageToken"] = page_token
        result = service.users().drafts().list(**params).execute()
        for d in result.get("drafts", []):
            detail = service.users().drafts().get(userId="me", id=d["id"], format="full").execute()
            headers = detail.get("message", {}).get("payload", {}).get("headers", [])
            to = subject = ""
            for h in headers:
                if h["name"].lower() == "to":
                    to = h.get("value", "")
                elif h["name"].lower() == "subject":
                    subject = h.get("value", "")
            email = extract_email(to)
            if email:
                drafts[email] = {"subject": subject, "draft_id": d["id"]}
        page_token = result.get("nextPageToken")
        if not page_token:
            break
    return drafts


def check_sent(service, email: str) -> bool:
    """Check if any message was sent to this email address."""
    query = f"to:{email} in:sent"
    result = service.users().messages().list(userId="me", q=query, maxResults=1).execute()
    return result.get("resultSizeEstimate", 0) > 0


def delete_draft(service, draft_id: str, email: str) -> bool:
    """Delete a single draft. Returns True on success."""
    try:
        service.users().drafts().delete(userId="me", id=draft_id).execute()
        print(f"  GELÖSCHT: {email}")
        return True
    except Exception as e:
        print(f"  FEHLER bei {email}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Gmail Drafts vs Sent Audit")
    parser.add_argument("--delete-sent", action="store_true",
                        help="Delete drafts whose recipient was already contacted + test draft")
    args = parser.parse_args()

    service = get_gmail_service(modify=args.delete_sent)

    print("Lade Drafts...")
    drafts = get_draft_recipients(service)
    print(f"{len(drafts)} Drafts mit Empfänger gefunden.\n")

    if not drafts:
        print("Keine Drafts vorhanden.")
        return

    print("Prüfe Sent-Ordner...")
    new = {}
    already_sent = {}
    test_drafts = {}

    for email, info in sorted(drafts.items()):
        if email == TEST_EMAIL:
            test_drafts[email] = info
        elif check_sent(service, email):
            already_sent[email] = info
        else:
            new[email] = info

    # Display results
    print(f"\n{'=' * 60}")
    print(f"NEU — noch nicht kontaktiert ({len(new)})")
    print("=" * 60)
    for email, info in sorted(new.items()):
        print(f"  {email:40s} | {info['subject']}")

    print(f"\n{'=' * 60}")
    print(f"BEREITS GESENDET — überspringen ({len(already_sent)})")
    print("=" * 60)
    for email, info in sorted(already_sent.items()):
        print(f"  {email:40s} | {info['subject']}")

    if test_drafts:
        print(f"\n{'=' * 60}")
        print(f"TEST-DRAFTS ({len(test_drafts)})")
        print("=" * 60)
        for email, info in test_drafts.items():
            print(f"  {email:40s} | {info['subject']}")

    total_to_delete = len(already_sent) + len(test_drafts)
    print(f"\nGesamt: {len(new)} neu, {len(already_sent)} bereits gesendet, "
          f"{len(test_drafts)} test, {len(drafts)} Drafts total")

    # Delete if flag set
    if args.delete_sent and total_to_delete > 0:
        print(f"\n{'=' * 60}")
        print(f"LÖSCHE {total_to_delete} Drafts (bereits gesendet + test)...")
        print("=" * 60)
        deleted = 0
        to_delete = {**already_sent, **test_drafts}
        for email, info in sorted(to_delete.items()):
            if delete_draft(service, info["draft_id"], email):
                deleted += 1
        print(f"\n{deleted}/{total_to_delete} Drafts gelöscht.")


if __name__ == "__main__":
    main()
