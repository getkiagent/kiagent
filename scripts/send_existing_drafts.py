#!/usr/bin/env python3
"""
Send Existing Drafts
- Reads all .txt files from outreach/
- Extracts subject from first "Betreff:" line
- Extracts body (everything after preamble/header lines)
- Maps filename -> company email via batch-results JSON files
- Creates Gmail Draft via Gmail API
- --dry-run: log actions without creating drafts

Usage:
    python scripts/send_existing_drafts.py
    python scripts/send_existing_drafts.py --dry-run
"""

import argparse
import base64
import json
import os
import re
import sys
import unicodedata
from email.mime.text import MIMEText
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

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
CREDENTIALS_FILE = PROJECT_ROOT / os.getenv("GMAIL_CREDENTIALS_JSON", "credentials.json")
TOKEN_FILE = PROJECT_ROOT / "token.json"

BATCH_FILES = [
    PROJECT_ROOT / "leads" / "batch-results.json",
    PROJECT_ROOT / "leads" / "batch-results-wave2.json",
    PROJECT_ROOT / "leads" / "batch-results-wave3.json",
]

OUTREACH_DIR = PROJECT_ROOT / "outreach"

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")

BLACKLIST_PREFIXES = ("noreply@", "no-reply@", "mailer-daemon@", "postmaster@")
BLACKLIST_DOMAINS = ("gmail.com", "googlemail.com")

# Lines to strip from body (regex patterns)
HEADER_LINE_RE = re.compile(r"^(Betreff:|An:|Subject:)", re.IGNORECASE)


# --- Normalization -----------------------------------------------------------

def normalize_slug(text: str) -> str:
    """Normalize to lowercase ASCII slug for fuzzy matching."""
    # Expand German umlauts before stripping diacritics
    replacements = {"ä": "ae", "ö": "oe", "ü": "ue", "Ä": "ae", "Ö": "oe", "Ü": "ue", "ß": "ss"}
    for char, rep in replacements.items():
        text = text.replace(char, rep)
    # Decompose remaining accented chars and strip diacritics
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    # Lowercase, keep only alphanumeric + hyphen, collapse separators
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text


# --- Email extraction --------------------------------------------------------

def is_valid_email(email: str) -> bool:
    e = email.lower()
    if any(e.startswith(p) for p in BLACKLIST_PREFIXES):
        return False
    domain = e.split("@", 1)[-1]
    if domain in BLACKLIST_DOMAINS:
        return False
    if any(e.endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif")):
        return False
    return True


def extract_email_from_data(data: dict) -> str | None:
    """Regex-search all text in a result's data dict for a business email."""
    text = json.dumps(data, ensure_ascii=False)
    found = [e for e in EMAIL_RE.findall(text) if is_valid_email(e)]
    return found[0] if found else None


def load_email_index() -> dict[str, tuple[str, str]]:
    """
    Returns {normalized_slug: (company_name, email)} for every company
    that has an extractable email across all batch files.
    """
    index: dict[str, tuple[str, str]] = {}
    for path in BATCH_FILES:
        if not path.exists():
            continue
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for result in data.get("results", []):
            entry = result.get("data")
            if not entry:
                continue
            company = entry.get("company_name", "").strip()
            email = extract_email_from_data(entry)
            if not company or not email:
                continue
            slug = normalize_slug(company)
            if slug not in index:
                index[slug] = (company, email)
    return index


# --- .txt parsing ------------------------------------------------------------

def parse_txt(path: Path) -> tuple[str | None, str]:
    """
    Returns (subject, body).
    subject: text after "Betreff: " on the first matching line, or None.
    body: everything after header lines (Betreff/An) and preamble, trimmed.
    """
    raw = path.read_text(encoding="utf-8", errors="replace")
    lines = raw.splitlines()

    subject: str | None = None
    betreff_index: int | None = None

    # Find first Betreff: line
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.lower().startswith("betreff:"):
            subject = stripped[len("betreff:"):].strip()
            betreff_index = i
            break

    # Build body: lines after the Betreff: line, skipping header lines and leading blanks
    if betreff_index is not None:
        body_lines = lines[betreff_index + 1:]
    else:
        body_lines = lines  # no Betreff found, use all

    # Skip "An:" lines
    body_lines = [l for l in body_lines if not HEADER_LINE_RE.match(l.strip())]

    # Strip leading blank lines
    while body_lines and not body_lines[0].strip():
        body_lines.pop(0)

    body = "\n".join(body_lines).strip()
    return subject, body


# --- Filename -> email lookup -------------------------------------------------

def resolve_email(
    filename_stem: str,
    email_index: dict[str, tuple[str, str]],
) -> tuple[str | None, str | None]:
    """
    Returns (company_name, email) or (None, None) if no match.
    Strategy: exact slug match, then longest-prefix match.
    """
    slug = normalize_slug(filename_stem)

    # Exact match
    if slug in email_index:
        return email_index[slug]

    # Substring match: filename slug is contained in company slug or vice versa
    best_match: tuple[str, str] | None = None
    best_len = 0
    for company_slug, (company_name, email) in email_index.items():
        # Check if one is a substring of the other
        if slug in company_slug or company_slug in slug:
            match_len = min(len(slug), len(company_slug))
            if match_len > best_len:
                best_len = match_len
                best_match = (company_name, email)

    if best_match:
        return best_match

    return None, None


# --- Gmail -------------------------------------------------------------------

def get_gmail_service():
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def create_draft(service, to: str, subject: str, body: str) -> str:
    """Creates a Gmail draft and returns its draft ID."""
    msg = MIMEText(body, "plain", "utf-8")
    msg["to"] = to
    msg["subject"] = subject
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    draft = service.users().drafts().create(
        userId="me",
        body={"message": {"raw": raw}},
    ).execute()
    return draft["id"]


# --- Main --------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Create Gmail drafts from outreach .txt files")
    parser.add_argument("--dry-run", action="store_true", help="Log actions without creating drafts")
    args = parser.parse_args()

    dry_run = args.dry_run
    if dry_run:
        print("[DRY RUN] No drafts will be created.\n")

    # Load email index
    email_index = load_email_index()
    print(f"Loaded {len(email_index)} companies with emails from batch files.\n")

    # Collect .txt files
    txt_files = sorted(OUTREACH_DIR.glob("*.txt"))
    print(f"Found {len(txt_files)} .txt files in outreach/\n")
    print("-" * 60)

    # Init Gmail service only if not dry run
    service = None
    if not dry_run:
        service = get_gmail_service()

    results = {"created": 0, "skipped": 0, "errors": 0}

    for txt_path in txt_files:
        stem = txt_path.stem
        company_name, email = resolve_email(stem, email_index)

        if not email:
            print(f"[SKIP]  {stem}")
            print(f"        Reason: no matching email found")
            print()
            results["skipped"] += 1
            continue

        subject, body = parse_txt(txt_path)

        if not subject:
            subject = f"Kurze Frage an {company_name}"

        if not body:
            print(f"[SKIP]  {stem}")
            print(f"        Reason: body is empty after parsing")
            print()
            results["skipped"] += 1
            continue

        status = "DRY RUN" if dry_run else "DRAFT"

        if not dry_run:
            try:
                draft_id = create_draft(service, email, subject, body)
                status = f"created (id={draft_id})"
                results["created"] += 1
            except Exception as exc:
                status = f"ERROR: {exc}"
                results["errors"] += 1
        else:
            results["created"] += 1

        print(f"[{status.upper()[:6]}] {company_name}")
        print(f"        File:    {txt_path.name}")
        print(f"        Email:   {email}")
        print(f"        Subject: {subject}")
        print(f"        Body:    {len(body)} chars, first line: {body.splitlines()[0][:60]}")
        print()

    print("=" * 60)
    print(f"Created: {results['created']}  |  Skipped: {results['skipped']}  |  Errors: {results['errors']}")
    return 0 if results["errors"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
