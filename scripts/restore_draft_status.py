#!/usr/bin/env python3
"""
Match Gmail draft recipients by domain against sheet URLs.
For sheet rows whose URL domain matches an existing draft's recipient domain,
restore status to 'outreach_draft'.
"""
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

SHEET_ID = "1OReC3rBa6bMImrw96dbTryW5LlB0SYWnbpn_t7x0-u0"
SHEET_TAB = "Lead Pipeline"
SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/spreadsheets",
]
TOKEN_FILE = PROJECT_ROOT / "token.json"


def url_host(url: str) -> str:
    u = (url or "").strip().lower()
    if not u:
        return ""
    if not u.startswith("http"):
        u = "https://" + u
    p = urlparse(u)
    host = (p.netloc or p.path).split("/")[0]
    if host.startswith("www."):
        host = host[4:]
    return host


def email_domain(e: str) -> str:
    e = (e or "").strip().lower()
    return e.split("@", 1)[1] if "@" in e else ""


def extract_to(header_value: str) -> str:
    v = (header_value or "").strip()
    if "<" in v and ">" in v:
        v = v.split("<", 1)[1].split(">", 1)[0]
    return v.strip().lower() if "@" in v else ""


def a1_col(n: int) -> str:
    s = ""
    while n > 0:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def main():
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    gmail = build("gmail", "v1", credentials=creds)
    sheets = build("sheets", "v4", credentials=creds).spreadsheets()

    print("Lade Gmail Drafts...")
    drafts = []
    page = None
    while True:
        params = {"userId": "me", "maxResults": 100}
        if page:
            params["pageToken"] = page
        res = gmail.users().drafts().list(**params).execute()
        for d in res.get("drafts", []):
            detail = gmail.users().drafts().get(userId="me", id=d["id"], format="metadata").execute()
            headers = detail.get("message", {}).get("payload", {}).get("headers", [])
            to = next((h["value"] for h in headers if h["name"].lower() == "to"), "")
            em = extract_to(to)
            if em:
                drafts.append(em)
        page = res.get("nextPageToken")
        if not page:
            break
    draft_domains = {email_domain(e) for e in drafts if email_domain(e)}
    print(f"  {len(drafts)} Drafts, {len(draft_domains)} unique Domains")

    print(f"Lade Sheet '{SHEET_TAB}'...")
    values = sheets.values().get(spreadsheetId=SHEET_ID, range=SHEET_TAB).execute().get("values", [])
    header = values[0]
    lower = [h.strip().lower() for h in header]
    url_i = lower.index("url")
    status_i = lower.index("status")

    rows_to_restore = []
    for r_idx, row in enumerate(values[1:], start=2):
        def cell(i):
            return row[i].strip() if 0 <= i < len(row) else ""
        if cell(status_i).lower() != "analysiert":
            continue
        host = url_host(cell(url_i))
        if not host:
            continue
        # Match: draft-domain equals host, or host ends with draft-domain, or vice versa
        for dd in draft_domains:
            if dd == host or host.endswith("." + dd) or dd.endswith("." + host):
                rows_to_restore.append((r_idx, cell(url_i), dd))
                break

    print(f"\n{len(rows_to_restore)} Zeilen werden auf 'outreach_draft' zurückgesetzt:")
    for r, u, dd in rows_to_restore:
        print(f"  row {r}: {u}  <- draft@{dd}")

    if not rows_to_restore:
        print("\nNichts wiederherzustellen.")
        return

    col = a1_col(status_i + 1)
    data = [{"range": f"'{SHEET_TAB}'!{col}{r}", "values": [["outreach_draft"]]}
            for r, _, _ in rows_to_restore]
    resp = sheets.values().batchUpdate(
        spreadsheetId=SHEET_ID,
        body={"valueInputOption": "RAW", "data": data},
    ).execute()
    print(f"\nRestore abgeschlossen: {resp.get('totalUpdatedCells', 0)} Zellen "
          f"(matching key: url, rows={len(rows_to_restore)}).")


if __name__ == "__main__":
    main()
