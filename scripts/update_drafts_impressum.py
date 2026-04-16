#!/usr/bin/env python3
"""
Update existing Gmail drafts — append canonical Impressum line in-place.

Non-destructive: only drafts missing the impressum_line get patched.
Drafts already compliant are skipped. Drafts unrelated to GetKiAgent
(no signature match) are skipped too.

Usage:
    python scripts/update_drafts_impressum.py --niche ecommerce-beauty
    python scripts/update_drafts_impressum.py --niche ecommerce-beauty --dry-run
"""
from __future__ import annotations

import argparse
import base64
import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from generate_outreach import SIGNATURE_REQUIRED, IMPRESSUM_SEPARATOR, _impressum_from_config
from niche_config import load_niche_config

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
CREDENTIALS_FILE = PROJECT_ROOT / os.getenv("GMAIL_CREDENTIALS_JSON", "credentials.json")
TOKEN_FILE = PROJECT_ROOT / "token.json"


def get_service():
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
                creds = flow.run_local_server(port=0)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
    return build("gmail", "v1", credentials=creds)


def _extract_body(payload: dict) -> tuple[str | None, dict | None]:
    """Return (decoded_body, body_part_ref) for plain-text body."""
    if payload.get("body", {}).get("data"):
        data = payload["body"]["data"]
        return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace"), payload["body"]
    for part in payload.get("parts", []):
        if part.get("mimeType") == "text/plain" and part.get("body", {}).get("data"):
            data = part["body"]["data"]
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace"), part["body"]
    return None, None


def _rebuild_raw(msg: dict, new_body: str) -> str:
    """Reconstruct raw RFC822 message from headers + new body."""
    headers = msg["payload"].get("headers", [])
    keep = {"to", "cc", "bcc", "subject", "from", "reply-to", "content-type", "mime-version"}
    lines: list[str] = []
    have_ct = have_mv = False
    for h in headers:
        name = h["name"].lower()
        if name not in keep:
            continue
        if name == "content-type":
            have_ct = True
        if name == "mime-version":
            have_mv = True
        lines.append(f"{h['name']}: {h['value']}")
    if not have_ct:
        lines.append("Content-Type: text/plain; charset=utf-8")
    if not have_mv:
        lines.append("MIME-Version: 1.0")
    lines.append("")
    lines.append(new_body)
    return "\r\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Append canonical Impressum to existing Gmail drafts (non-destructive).")
    parser.add_argument("--niche", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    config = load_niche_config(args.niche)
    imp = _impressum_from_config(config)
    if not imp:
        print(f"ERROR: impressum_line fehlt in configs/{args.niche}.yaml")
        return 1

    service = get_service()
    print("Lade alle Drafts…")
    drafts = []
    page_token = None
    while True:
        resp = service.users().drafts().list(userId="me", pageToken=page_token, maxResults=500).execute()
        drafts.extend(resp.get("drafts", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    print(f"  -> {len(drafts)} Drafts gefunden\n")

    stats = {"patched": 0, "already_ok": 0, "not_getkiagent": 0, "no_body": 0, "errors": 0}

    for d in drafts:
        try:
            draft = service.users().drafts().get(userId="me", id=d["id"], format="full").execute()
        except HttpError as exc:
            print(f"  ERROR get draft {d['id']}: {exc}")
            stats["errors"] += 1
            continue

        msg = draft["message"]
        body, _body_ref = _extract_body(msg.get("payload", {}))
        if not body:
            stats["no_body"] += 1
            continue

        # Scope: only touch GetKiAgent drafts (signature match)
        if SIGNATURE_REQUIRED not in body:
            stats["not_getkiagent"] += 1
            continue

        if imp in body:
            stats["already_ok"] += 1
            continue

        new_body = body.rstrip() + IMPRESSUM_SEPARATOR + imp + "\n"
        to_header = next((h["value"] for h in msg["payload"].get("headers", []) if h["name"].lower() == "to"), "?")

        if args.dry_run:
            print(f"  [dry] würde patchen: {to_header}")
            stats["patched"] += 1
            continue

        raw = _rebuild_raw(msg, new_body)
        encoded = base64.urlsafe_b64encode(raw.encode("utf-8")).decode("ascii")
        try:
            service.users().drafts().update(
                userId="me", id=d["id"],
                body={"message": {"raw": encoded}},
            ).execute()
            print(f"  patched: {to_header}")
            stats["patched"] += 1
        except HttpError as exc:
            print(f"  ERROR update {to_header}: {exc}")
            stats["errors"] += 1

    print(f"\nFertig.")
    print(f"  Patched       : {stats['patched']}")
    print(f"  Already ok    : {stats['already_ok']}")
    print(f"  Nicht GetKi   : {stats['not_getkiagent']}")
    print(f"  Kein Body     : {stats['no_body']}")
    print(f"  Errors        : {stats['errors']}")
    if args.dry_run:
        print("(dry-run: keine Drafts geändert)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
