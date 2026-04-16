#!/usr/bin/env python3
"""
Reset sheet rows with status='outreach_draft' whose Gmail draft no longer exists.
Matches leads by URL (case-insensitive normalized) and by recipient email.
Resets missing-draft rows to status='analysiert'.
"""
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

SHEET_ID = "1OReC3rBa6bMImrw96dbTryW5LlB0SYWnbpn_t7x0-u0"
SHEET_TAB = "Lead Pipeline"
SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/spreadsheets",
]
CREDENTIALS_FILE = PROJECT_ROOT / "credentials.json"
TOKEN_FILE = PROJECT_ROOT / "token.json"


def get_creds():
    creds = None
    if TOKEN_FILE.exists():
        stored_scopes = set(json.loads(TOKEN_FILE.read_text()).get("scopes", []))
        if set(SCOPES).issubset(stored_scopes):
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json())
    return creds


def normalize_url(url: str) -> str:
    u = (url or "").strip().lower()
    if not u:
        return ""
    if not u.startswith("http"):
        u = "https://" + u
    p = urlparse(u)
    host = (p.netloc or p.path).lstrip("/")
    if host.startswith("www."):
        host = host[4:]
    path = p.path.rstrip("/") if p.netloc else ""
    return f"https://{host}{path}"


def extract_email(header_value: str) -> str:
    if not header_value:
        return ""
    v = header_value.strip()
    if "<" in v and ">" in v:
        v = v.split("<", 1)[1].split(">", 1)[0]
    return v.strip().lower() if "@" in v else ""


def load_batch_lookups():
    """url -> company info (from batch-results files); no emails in batch files."""
    lookup = {}
    for name in ["batch-results.json", "batch-results-new.json",
                 "batch-results-wave2.json", "batch-results-wave3.json"]:
        path = PROJECT_ROOT / "leads" / name
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for r in data.get("results", []):
            if r.get("status") == "ok":
                lookup[normalize_url(r.get("url", ""))] = r.get("data", {})
    return lookup


def load_draft_recipients(gmail):
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
            em = extract_email(to)
            if em:
                drafts.append(em)
        page = res.get("nextPageToken")
        if not page:
            break
    return set(drafts)


def a1_col(n: int) -> str:
    s = ""
    while n > 0:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def main():
    creds = get_creds()
    gmail = build("gmail", "v1", credentials=creds)
    sheets = build("sheets", "v4", credentials=creds).spreadsheets()

    print("Lade Batch-Results...")
    batch_lookup = load_batch_lookups()
    print(f"  {len(batch_lookup)} erfolgreich analysierte Leads gelesen.")

    print("Lade Gmail Drafts...")
    draft_emails = load_draft_recipients(gmail)
    print(f"  {len(draft_emails)} Drafts mit Empfänger gefunden.")

    print(f"Lade Sheet '{SHEET_TAB}'...")
    values = sheets.values().get(spreadsheetId=SHEET_ID, range=SHEET_TAB).execute().get("values", [])
    if not values:
        print("  Sheet leer.")
        return
    header = values[0]
    lower = [h.strip().lower() for h in header]

    def find_col(*names):
        for n in names:
            if n in lower:
                return lower.index(n)
        return -1

    url_i = find_col("url", "website")
    status_i = find_col("status")
    email_i = find_col("email", "contact_email", "e-mail")
    if url_i < 0 or status_i < 0:
        print(f"ERROR: url/status Spalten fehlen. Header: {header}")
        sys.exit(1)

    print(f"  Spalten: url={a1_col(url_i+1)}, status={a1_col(status_i+1)}, "
          f"email={a1_col(email_i+1) if email_i>=0 else 'N/A'}")

    rows_to_reset = []
    for r_idx, row in enumerate(values[1:], start=2):
        def cell(i):
            return row[i].strip() if 0 <= i < len(row) else ""
        if cell(status_i).lower() != "outreach_draft":
            continue
        email = cell(email_i).lower() if email_i >= 0 else ""
        if email and email in draft_emails:
            continue
        rows_to_reset.append((r_idx, cell(url_i), email))

    print(f"\n{len(rows_to_reset)} Zeilen mit status='outreach_draft' ohne Gmail-Draft:")
    for r_idx, url, em in rows_to_reset[:50]:
        print(f"  row {r_idx}: {url}  <{em or 'no-email'}>")
    if len(rows_to_reset) > 50:
        print(f"  ... +{len(rows_to_reset)-50} weitere")

    if not rows_to_reset:
        print("\nNichts zu resetten.")
        return

    col_letter = a1_col(status_i + 1)
    data = [{"range": f"'{SHEET_TAB}'!{col_letter}{r}", "values": [["analysiert"]]}
            for r, _, _ in rows_to_reset]
    body = {"valueInputOption": "RAW", "data": data}
    resp = sheets.values().batchUpdate(spreadsheetId=SHEET_ID, body=body).execute()
    print(f"\nReset abgeschlossen: {resp.get('totalUpdatedCells', 0)} Zellen aktualisiert "
          f"(matching key: url, rows={len(rows_to_reset)}).")


if __name__ == "__main__":
    main()
