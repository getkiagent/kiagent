#!/usr/bin/env python3
"""
Delete ALL Gmail drafts. Destructive — requires confirmation.

WARNING: this deletes EVERY draft in the connected Gmail account,
including drafts unrelated to GetKiAgent outreach. Use cleanup_drafts.py
for scoped cleanup.

Usage:
    python scripts/delete_all_drafts.py           # interactive confirmation
    python scripts/delete_all_drafts.py --yes     # skip confirmation (scripts)
"""

import argparse
import os
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def get_gmail_service():
    token_path = PROJECT_ROOT / "token.json"
    creds_env = os.getenv("GMAIL_CREDENTIALS_JSON")
    creds_path = PROJECT_ROOT / creds_env if creds_env else PROJECT_ROOT / "credentials.json"
    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError as e:
                print(f"ERROR: Gmail auth expired — refresh token.json manually. Details: {e}")
                sys.exit(1)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
            creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def delete_with_retry(drafts_api, draft_id: str, max_retries: int = 3) -> None:
    for attempt in range(max_retries):
        try:
            drafts_api.delete(userId="me", id=draft_id).execute()
            return
        except HttpError as e:
            if e.resp.status in (429, 500, 502, 503, 504) and attempt < max_retries - 1:
                time.sleep(2 ** (attempt + 1))
                continue
            raise


def main():
    parser = argparse.ArgumentParser(description="Delete ALL Gmail drafts (destructive)")
    parser.add_argument("--yes", action="store_true", help="Skip interactive confirmation")
    args = parser.parse_args()

    service = get_gmail_service()
    drafts_api = service.users().drafts()

    all_ids = []
    page_token = None
    while True:
        resp = drafts_api.list(userId="me", maxResults=500, pageToken=page_token).execute()
        all_ids.extend(d["id"] for d in resp.get("drafts", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    total = len(all_ids)
    if total == 0:
        print("Keine Drafts vorhanden.")
        return

    print("=" * 60)
    print(f"WARNUNG: Löscht ALLE {total} Gmail-Drafts im Account.")
    print("Das umfasst auch Drafts die NICHTS mit GetKiAgent zu tun haben.")
    print("=" * 60)

    if not args.yes:
        confirm = input("Tippe 'DELETE' zur Bestätigung: ").strip()
        if confirm != "DELETE":
            print("Abgebrochen.")
            sys.exit(0)

    deleted = 0
    errors = 0
    for draft_id in all_ids:
        try:
            delete_with_retry(drafts_api, draft_id)
            deleted += 1
        except HttpError as e:
            errors += 1
            print(f"  Fehler bei {draft_id}: {e}")

    print(f"\nFertig: {deleted} gelöscht, {errors} Fehler.")

if __name__ == "__main__":
    main()
