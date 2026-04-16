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
from email.header import Header
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv not installed. Run: pip install python-dotenv")
    sys.exit(1)

try:
    import time
    from google.auth.exceptions import RefreshError
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
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
    PROJECT_ROOT / "leads" / "qualified-leads.json",
    PROJECT_ROOT / "leads" / "beauty" / "qualified-tierA-enriched.json",
]

OUTREACH_DIR = PROJECT_ROOT / "outreach"

SEND_LOG_FILE = PROJECT_ROOT / "tasks" / "send-log.json"
MAX_DRAFTS_PER_DAY = 40

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
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        except ValueError as e:
            print(f"ERROR: token.json nicht lesbar ({e}). Lösche die Datei und führe erneut aus.")
            sys.exit(1)
        if creds and creds.scopes and set(SCOPES) - set(creds.scopes):
            print("WARN: token.json hat nicht alle benötigten Scopes — lösche Token und re-authentifiziere.")
            creds = None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError as e:
                print(f"ERROR: Gmail auth expired — refresh token.json manually. Details: {e}")
                sys.exit(1)
        else:
            if not CREDENTIALS_FILE.exists():
                print(f"ERROR: credentials.json nicht gefunden unter {CREDENTIALS_FILE}")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def fetch_existing_draft_recipients(service) -> set[str]:
    """Return lowercased set of 'to' addresses for all existing drafts (for --keep-existing)."""
    recipients: set[str] = set()
    page_token = None
    while True:
        resp = service.users().drafts().list(userId="me", maxResults=500, pageToken=page_token).execute()
        for d in resp.get("drafts", []):
            try:
                full = service.users().drafts().get(userId="me", id=d["id"], format="metadata").execute()
                headers = full.get("message", {}).get("payload", {}).get("headers", [])
                for h in headers:
                    if h.get("name", "").lower() == "to":
                        for m in EMAIL_RE.findall(h.get("value", "")):
                            recipients.add(m.lower())
            except HttpError as e:
                print(f"  WARN: konnte Draft {d['id']} nicht lesen: {e}")
                continue
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return recipients


def create_draft(service, to: str, subject: str, body: str, max_retries: int = 3) -> str:
    """Creates a Gmail draft with exponential backoff on transient errors."""
    msg = MIMEText(body, "plain", "utf-8")
    msg["to"] = to
    msg["subject"] = Header(subject, "utf-8")
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    for attempt in range(max_retries):
        try:
            draft = service.users().drafts().create(
                userId="me",
                body={"message": {"raw": raw}},
            ).execute()
            return draft["id"]
        except HttpError as e:
            if e.resp.status in (429, 500, 502, 503, 504) and attempt < max_retries - 1:
                wait = 2 ** (attempt + 1)
                print(f"  WARN: Gmail HTTP {e.resp.status}, retry in {wait}s (attempt {attempt+1}/{max_retries})")
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("create_draft: all retries exhausted")


# --- Send-Cap ----------------------------------------------------------------

def _today_str() -> str:
    from datetime import date
    return date.today().isoformat()


def load_send_log() -> dict:
    """Return today's draft-count log. Resets automatically on new day."""
    today = _today_str()
    if not SEND_LOG_FILE.exists():
        return {"date": today, "count": 0}
    try:
        with open(SEND_LOG_FILE, encoding="utf-8") as f:
            log = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"date": today, "count": 0}
    if log.get("date") != today:
        return {"date": today, "count": 0}
    return log


def save_send_log(log: dict) -> None:
    SEND_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SEND_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


# --- Main --------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Create Gmail drafts from outreach .txt files")
    parser.add_argument("--dry-run", action="store_true", help="Log actions without creating drafts")
    parser.add_argument("--keep-existing", action="store_true", help="Skip recipients that already have a Gmail draft (PLAN.md Stage 5)")
    parser.add_argument("--niche", default=None, help="Niche name — read from outreach/{niche}/ instead of outreach/")
    parser.add_argument("--folder", default=None, help="Path to folder with .txt drafts (overrides --niche). Relative to project root or absolute.")
    parser.add_argument("--limit", type=int, default=None, help="Stop after N successful draft creations")
    parser.add_argument("--no-cap", action="store_true", help="Ignore daily draft cap (use for one-off bulk imports, not for Send)")
    args = parser.parse_args()

    dry_run = args.dry_run
    if dry_run:
        print("[DRY RUN] No drafts will be created.\n")

    # Load email index
    email_index = load_email_index()
    print(f"Loaded {len(email_index)} companies with emails from batch files.\n")

    # Collect .txt files (folder > niche > default)
    if args.folder:
        folder_path = Path(args.folder)
        outreach_base = folder_path if folder_path.is_absolute() else PROJECT_ROOT / folder_path
    elif args.niche:
        outreach_base = OUTREACH_DIR / args.niche
    else:
        outreach_base = OUTREACH_DIR
    if not outreach_base.exists():
        print(f"ERROR: Outreach-Verzeichnis nicht gefunden: {outreach_base}")
        return 1
    txt_files = sorted(outreach_base.glob("*.txt"))
    print(f"Found {len(txt_files)} .txt files in {outreach_base.relative_to(PROJECT_ROOT)}/\n")

    # Optional folder-local recipients.json override (checked before batch-results lookup)
    folder_recipients: dict[str, str] = {}
    if args.folder:
        recipients_file = outreach_base / "recipients.json"
        if recipients_file.exists():
            try:
                raw = json.loads(recipients_file.read_text(encoding="utf-8"))
                folder_recipients = {k: v for k, v in raw.items() if isinstance(v, str) and v.strip()}
                print(f"Loaded {len(folder_recipients)} recipient override(s) from {recipients_file.relative_to(PROJECT_ROOT)}\n")
            except (OSError, json.JSONDecodeError) as exc:
                print(f"WARN: recipients.json konnte nicht geladen werden: {exc}\n")
    print("-" * 60)

    if not txt_files:
        return 0

    # Init Gmail service only if not dry run
    service = None
    existing_recipients: set[str] = set()
    if not dry_run:
        service = get_gmail_service()
        if args.keep_existing:
            print("Scanning existing Gmail drafts...")
            existing_recipients = fetch_existing_draft_recipients(service)
            print(f"  -> {len(existing_recipients)} existing recipients found\n")

    results = {"created": 0, "skipped": 0, "errors": 0, "kept_existing": 0}

    send_log = load_send_log()
    if not dry_run:
        remaining = MAX_DRAFTS_PER_DAY - send_log["count"]
        print(f"[CAP] Tages-Draft-Cap: {send_log['count']}/{MAX_DRAFTS_PER_DAY} verbraucht, {max(remaining, 0)} verbleibend.\n")

    for txt_path in txt_files:
        stem = txt_path.stem
        override_email = folder_recipients.get(stem, "").strip()
        if override_email and is_valid_email(override_email):
            company_name, email = stem, override_email
        else:
            company_name, email = resolve_email(stem, email_index)

        if not email:
            print(f"[SKIP]  {stem}")
            print(f"        Reason: no matching email found")
            print()
            results["skipped"] += 1
            continue

        if args.keep_existing and email.lower() in existing_recipients:
            print(f"[KEEP]  {company_name} ({email}) — draft already exists")
            print()
            results["kept_existing"] += 1
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

        if not dry_run and not args.no_cap and send_log["count"] >= MAX_DRAFTS_PER_DAY:
            print(f"[CAP] Tages-Draft-Cap ({MAX_DRAFTS_PER_DAY}) erreicht — Rest-Queue: {len(txt_files) - (results['created'] + results['skipped'] + results['kept_existing'] + results['errors'])} Mails. Morgen fortsetzen.")
            break

        status = "DRY RUN" if dry_run else "DRAFT"

        if not dry_run:
            try:
                draft_id = create_draft(service, email, subject, body)
                status = f"created (id={draft_id})"
                results["created"] += 1
                send_log["count"] += 1
                save_send_log(send_log)
            except HttpError as exc:
                status = f"ERROR: {exc}"
                results["errors"] += 1
            except RuntimeError as exc:
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

        if args.limit and results["created"] >= args.limit:
            print(f"[LIMIT] Reached --limit {args.limit}, stopping.")
            break

    print("=" * 60)
    print(f"Created: {results['created']}  |  Kept: {results['kept_existing']}  |  Skipped: {results['skipped']}  |  Errors: {results['errors']}")
    return 0 if results["errors"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
