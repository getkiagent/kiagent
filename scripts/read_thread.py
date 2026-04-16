#!/usr/bin/env python3
"""Dump plaintext body of a Gmail thread for quick triage."""
import base64
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_FILE = Path(__file__).resolve().parent.parent / "token.json"


def decode(part):
    data = part.get("body", {}).get("data")
    if data:
        return base64.urlsafe_b64decode(data.encode("utf-8")).decode("utf-8", errors="replace")
    return ""


def extract_text(payload):
    mime = payload.get("mimeType", "")
    if mime == "text/plain":
        return decode(payload)
    for p in payload.get("parts", []) or []:
        t = extract_text(p)
        if t:
            return t
    return ""


def main():
    if len(sys.argv) < 2:
        print("usage: read_thread.py <thread_id>")
        sys.exit(1)
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE))
    svc = build("gmail", "v1", credentials=creds)
    thread = svc.users().threads().get(userId="me", id=sys.argv[1], format="full").execute()

    for i, msg in enumerate(thread["messages"]):
        headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        print("=" * 70)
        print(f"MSG {i+1}  From: {headers.get('From','')}")
        print(f"        To:   {headers.get('To','')}")
        print(f"        Date: {headers.get('Date','')}")
        print(f"        Subj: {headers.get('Subject','')}")
        print("-" * 70)
        body = extract_text(msg["payload"])
        print(body[:3000])
        print()


if __name__ == "__main__":
    main()
