#!/usr/bin/env python3
"""
Gmail Draft Cleanup
- Reads all Gmail drafts
- Groups by recipient email
- Keeps 1 random draft per recipient, deletes the rest
- Adds Loom PS line to kept draft if missing
- --dry-run: show actions without executing

Setup:
1. pip install google-auth-oauthlib google-api-python-client
2. Download OAuth2 credentials from Google Cloud Console → credentials.json
3. First run: browser opens for auth, token saved to token.json

Usage:
    python scripts/cleanup_drafts.py
    python scripts/cleanup_drafts.py --dry-run
"""

import argparse
import base64
import os
import random
import sys
from email import message_from_bytes
from pathlib import Path

# Force UTF-8 on Windows
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

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
CREDENTIALS_FILE = PROJECT_ROOT / os.getenv("GMAIL_CREDENTIALS_JSON", "credentials.json")
TOKEN_FILE = PROJECT_ROOT / "token.json"

LOOM_URL = "https://www.loom.com/share/a243a6f8c920487a9db15e9c9816c36e"
LOOM_PS = f"P.S. Hier eine kurze Demo, wie das konkret aussehen kann: {LOOM_URL}"


def get_gmail_service():
    """Authenticate and return Gmail API service."""
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print(f"ERROR: credentials.json nicht gefunden: {CREDENTIALS_FILE}")
                print("Lade OAuth2-Client-Credentials von Google Cloud Console herunter.")
                print(f"Setze GMAIL_CREDENTIALS_JSON in .env oder lege credentials.json im Projektroot ab.")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
        print(f"Token gespeichert: {TOKEN_FILE}")

    return build("gmail", "v1", credentials=creds)


def decode_body(raw: str) -> str:
    """Decode base64url Gmail body to string."""
    padded = raw.replace("-", "+").replace("_", "/")
    padded += "=" * (4 - len(padded) % 4)
    return base64.b64decode(padded).decode("utf-8", errors="replace")


def encode_body(text: str) -> str:
    """Encode string to base64url for Gmail API."""
    return base64.urlsafe_b64encode(text.encode("utf-8")).decode("ascii")


def get_draft_recipient(draft_detail: dict) -> str | None:
    """Extract To: header from draft message."""
    headers = draft_detail.get("message", {}).get("payload", {}).get("headers", [])
    for h in headers:
        if h.get("name", "").lower() == "to":
            val = h.get("value", "").strip()
            # Extract raw email from "Name <email@...>" or plain "email@..."
            if "<" in val and ">" in val:
                return val.split("<")[1].split(">")[0].strip().lower()
            return val.lower()
    return None


def get_draft_body_part(payload: dict) -> tuple[str, str]:
    """
    Extract the text/plain body from a Gmail message payload.
    Returns (body_text, part_path) where part_path identifies which part to update.
    """
    mime_type = payload.get("mimeType", "")

    if mime_type == "text/plain":
        data = payload.get("body", {}).get("data", "")
        return decode_body(data) if data else "", "body"

    if mime_type.startswith("multipart/"):
        for part in payload.get("parts", []):
            body, path = get_draft_body_part(part)
            if body:
                return body, path

    return "", ""


def build_updated_raw(draft_detail: dict, new_body: str) -> str:
    """
    Rebuild the raw RFC 2822 message with updated body.
    Handles simple text/plain messages (covers the generate_outreach.py output format).
    """
    msg = draft_detail.get("message", {})
    payload = msg.get("payload", {})
    headers = payload.get("headers", [])

    lines = []
    for h in headers:
        name = h.get("name", "")
        value = h.get("value", "")
        # Skip content-transfer-encoding, we'll re-add
        if name.lower() in ("content-transfer-encoding", "mime-version"):
            continue
        lines.append(f"{name}: {value}")

    lines.append("MIME-Version: 1.0")
    lines.append("Content-Type: text/plain; charset=utf-8")
    lines.append("Content-Transfer-Encoding: base64")
    lines.append("")
    lines.append(encode_body(new_body))

    raw = "\r\n".join(lines)
    return base64.urlsafe_b64encode(raw.encode("utf-8")).decode("ascii")


def fetch_all_drafts(service) -> list[dict]:
    """Fetch all drafts with full details."""
    drafts = []
    page_token = None

    while True:
        params = {"userId": "me", "maxResults": 100}
        if page_token:
            params["pageToken"] = page_token

        result = service.users().drafts().list(**params).execute()
        batch = result.get("drafts", [])

        for d in batch:
            detail = service.users().drafts().get(
                userId="me", id=d["id"], format="full"
            ).execute()
            drafts.append(detail)

        page_token = result.get("nextPageToken")
        if not page_token:
            break

    return drafts


def add_loom_ps(body: str) -> str:
    """Append Loom PS line to body if not already present."""
    if LOOM_URL in body:
        return body
    stripped = body.rstrip()
    return stripped + "\n\n" + LOOM_PS + "\n"


def main():
    parser = argparse.ArgumentParser(description="Gmail Draft Cleanup")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Zeige was gelöscht würde ohne zu löschen",
    )
    parser.add_argument(
        "--delete-empty",
        action="store_true",
        help="Lösche alle Drafts ohne Empfänger (no_recipient Liste)",
    )
    args = parser.parse_args()

    if args.dry_run:
        print("[DRY-RUN] Keine Änderungen werden vorgenommen.\n")

    service = get_gmail_service()

    print("Lade alle Drafts...")
    all_drafts = fetch_all_drafts(service)
    print(f"Gefunden: {len(all_drafts)} Drafts total\n")

    if not all_drafts:
        print("Keine Drafts vorhanden.")
        return

    # Group by recipient
    groups: dict[str, list[dict]] = {}
    no_recipient = []

    for draft in all_drafts:
        recipient = get_draft_recipient(draft)
        if not recipient:
            no_recipient.append(draft)
            continue
        groups.setdefault(recipient, []).append(draft)

    stats = {"kept": 0, "deleted": 0, "deleted_empty": 0, "loom_added": 0, "loom_already": 0}

    if no_recipient:
        if args.delete_empty:
            print(f"LÖSCHE {len(no_recipient)} Drafts ohne Empfänger-Email:\n")
        else:
            print(f"WARNUNG: {len(no_recipient)} Drafts ohne Empfänger-Email (werden nicht angefasst):\n")
        for d in no_recipient:
            subject = ""
            for h in d.get("message", {}).get("payload", {}).get("headers", []):
                if h.get("name", "").lower() == "subject":
                    subject = h.get("value", "")
            print(f"  - ID {d['id']} | Betreff: {subject or '(kein Betreff)'}")
            if args.delete_empty and not args.dry_run:
                service.users().drafts().delete(userId="me", id=d["id"]).execute()
        if args.delete_empty:
            stats["deleted_empty"] = len(no_recipient)
        print()

    print("=" * 60)

    for recipient, drafts in sorted(groups.items()):
        print(f"\nEmpfänger: {recipient} ({len(drafts)} Drafts)")

        # Pick 1 random draft to keep
        kept = random.choice(drafts)
        to_delete = [d for d in drafts if d["id"] != kept["id"]]

        # Extract subject of kept draft
        kept_subject = ""
        for h in kept.get("message", {}).get("payload", {}).get("headers", []):
            if h.get("name", "").lower() == "subject":
                kept_subject = h.get("value", "")

        print(f"  BEHALTEN: ID {kept['id']} | {kept_subject or '(kein Betreff)'}")

        # Check/add Loom PS to kept draft
        payload = kept.get("message", {}).get("payload", {})
        body_text, _ = get_draft_body_part(payload)

        if LOOM_URL in body_text:
            print(f"  LOOM:    Bereits vorhanden — kein Update nötig")
            stats["loom_already"] += 1
        else:
            print(f"  LOOM:    PS-Zeile wird eingefügt")
            if not args.dry_run:
                new_body = add_loom_ps(body_text)
                raw = build_updated_raw(kept, new_body)
                service.users().drafts().update(
                    userId="me",
                    id=kept["id"],
                    body={"message": {"raw": raw}},
                ).execute()
            stats["loom_added"] += 1

        stats["kept"] += 1

        # Delete the rest
        for d in to_delete:
            subj = ""
            for h in d.get("message", {}).get("payload", {}).get("headers", []):
                if h.get("name", "").lower() == "subject":
                    subj = h.get("value", "")
            print(f"  LÖSCHEN: ID {d['id']} | {subj or '(kein Betreff)'}")
            if not args.dry_run:
                service.users().drafts().delete(userId="me", id=d["id"]).execute()
            stats["deleted"] += 1

    print(f"\n{'=' * 60}")
    print("ZUSAMMENFASSUNG" + (" [DRY-RUN]" if args.dry_run else ""))
    print(f"  Behalten:    {stats['kept']} Drafts")
    print(f"  Gelöscht:    {stats['deleted']} Drafts")
    print(f"  Loom neu:    {stats['loom_added']} Drafts aktualisiert")
    print(f"  Loom vorhanden: {stats['loom_already']} Drafts (kein Update)")
    if stats["deleted_empty"]:
        print(f"  Ohne Empfänger gelöscht: {stats['deleted_empty']} Drafts")


if __name__ == "__main__":
    main()
