#!/usr/bin/env python3
"""Fix signature in Gmail drafts: 'Ilias\n' → 'Ilias Tebque\n'"""

import os
import base64
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
TOKEN = os.path.expanduser("~/Desktop/getkiagent/token.pickle")
CREDS = os.path.expanduser("~/Desktop/getkiagent/credentials.json")

OLD_SIG = "Ilias\nGetKiAgent"
NEW_SIG = "Ilias Tebque\nGetKiAgent"


def get_service():
    creds = None
    if os.path.exists(TOKEN):
        with open(TOKEN, "rb") as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN, "wb") as f:
            pickle.dump(creds, f)
    return build("gmail", "v1", credentials=creds)


def main():
    service = get_service()
    drafts = []
    page_token = None
    while True:
        resp = service.users().drafts().list(userId="me", pageToken=page_token).execute()
        drafts.extend(resp.get("drafts", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    print(f"Gefunden: {len(drafts)} Drafts")
    fixed = 0
    skipped = 0

    for d in drafts:
        draft = service.users().drafts().get(userId="me", id=d["id"], format="full").execute()
        msg = draft["message"]
        payload = msg.get("payload", {})

        # Get body
        body_data = None
        if payload.get("body", {}).get("data"):
            body_data = payload["body"]["data"]
        elif payload.get("parts"):
            for part in payload["parts"]:
                if part.get("mimeType") == "text/plain" and part.get("body", {}).get("data"):
                    body_data = part["body"]["data"]
                    break

        if not body_data:
            skipped += 1
            continue

        decoded = base64.urlsafe_b64decode(body_data).decode("utf-8")

        if OLD_SIG in decoded and NEW_SIG not in decoded:
            new_body = decoded.replace(OLD_SIG, NEW_SIG)
            encoded = base64.urlsafe_b64encode(new_body.encode("utf-8")).decode("ascii")

            # Rebuild
            if payload.get("body", {}).get("data"):
                payload["body"]["data"] = encoded
            elif payload.get("parts"):
                for part in payload["parts"]:
                    if part.get("mimeType") == "text/plain" and part.get("body", {}).get("data"):
                        part["body"]["data"] = encoded
                        break

            service.users().drafts().update(
                userId="me", id=d["id"],
                body={"message": {"raw": base64.urlsafe_b64encode(
                    _build_raw(msg, new_body).encode("utf-8")
                ).decode("ascii")}}
            ).execute()
            fixed += 1
        else:
            skipped += 1

    print(f"Fixed: {fixed} | Skipped: {skipped}")


def _build_raw(msg, new_body):
    """Build raw email string from message headers + new body."""
    headers = msg["payload"].get("headers", [])
    lines = []
    for h in headers:
        name = h["name"]
        if name.lower() in ("to", "subject", "from", "content-type", "mime-version"):
            lines.append(f"{name}: {h['value']}")
    if not any(h["name"].lower() == "content-type" for h in headers):
        lines.append("Content-Type: text/plain; charset=utf-8")
    if not any(h["name"].lower() == "mime-version" for h in headers):
        lines.append("MIME-Version: 1.0")
    lines.append("")
    lines.append(new_body)
    return "\r\n".join(lines)


if __name__ == "__main__":
    main()
