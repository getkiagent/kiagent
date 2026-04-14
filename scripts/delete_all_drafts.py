#!/usr/bin/env python3
"""Delete ALL Gmail drafts. No dry-run, no filtering."""

import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def get_gmail_service():
    token_path = PROJECT_ROOT / "token.json"
    creds_path = os.getenv("GMAIL_CREDENTIALS_JSON", PROJECT_ROOT / "credentials.json")
    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
            creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json())
    return build("gmail", "v1", credentials=creds)

def main():
    service = get_gmail_service()
    drafts_api = service.users().drafts()

    # Fetch all draft IDs
    all_ids = []
    page_token = None
    while True:
        resp = drafts_api.list(userId="me", maxResults=500, pageToken=page_token).execute()
        batch = resp.get("drafts", [])
        all_ids.extend(d["id"] for d in batch)
        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    total = len(all_ids)
    if total == 0:
        print("Keine Drafts vorhanden.")
        return

    print(f"{total} Drafts gefunden. Lösche alle...")

    deleted = 0
    errors = 0
    for draft_id in all_ids:
        try:
            drafts_api.delete(userId="me", id=draft_id).execute()
            deleted += 1
        except Exception as e:
            errors += 1
            print(f"  Fehler bei {draft_id}: {e}")

    print(f"\nFertig: {deleted} gelöscht, {errors} Fehler.")

if __name__ == "__main__":
    main()
