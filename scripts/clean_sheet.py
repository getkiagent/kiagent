"""
GetKiAgent — Sheet Cleaner

Reads "Lead Pipeline" sheet, normalizes URLs, removes test/empty rows,
deduplicates by normalized URL (keeps higher score), writes back.

Usage:
    python scripts/clean_sheet.py --dry-run   # preview only
    python scripts/clean_sheet.py             # apply changes

Requirements:
    pip install gspread google-auth python-dotenv

.env vars needed:
    GOOGLE_SERVICE_ACCOUNT_JSON=/path/to/service_account.json
    GOOGLE_SHEET_ID=1OReC3rBa6bMImrw96dbTryW5LlB0SYWnbpn_t7x0-u0  (default hardcoded)
"""

import sys
import os
import json
from pathlib import Path
from urllib.parse import urlparse

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv not installed. Run: pip install python-dotenv")
    sys.exit(1)

try:
    import gspread
    from google.oauth2.service_account import Credentials
except ImportError:
    print("ERROR: gspread or google-auth not installed. Run: pip install gspread google-auth")
    sys.exit(1)

# Load .env from project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "1OReC3rBa6bMImrw96dbTryW5LlB0SYWnbpn_t7x0-u0")
SHEET_TAB = "Lead Pipeline"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Rows that are test data — deleted regardless of URL
TEST_COMPANY_NAMES = {"PROBE WRITE 3"}
TEST_CATEGORIES = {"test"}


# ── URL normalization ──────────────────────────────────────────────────────────

def normalize_url(url: str) -> str:
    """
    Normalize a URL to canonical form:
    - lowercase
    - strip trailing slashes
    - ensure https:// prefix
    - strip www.
    """
    url = url.strip().lower()
    if not url:
        return ""

    # Add scheme if missing
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    # Parse and rebuild
    parsed = urlparse(url)
    host = parsed.netloc or parsed.path

    # Strip www.
    if host.startswith("www."):
        host = host[4:]

    # Rebuild: scheme + host + path (strip trailing slash from path)
    path = parsed.path.rstrip("/") if parsed.netloc else ""
    normalized = f"https://{host}{path}"

    return normalized


# ── Google Sheets client ───────────────────────────────────────────────────────

def get_sheet():
    creds_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not creds_path:
        print("ERROR: GOOGLE_SERVICE_ACCOUNT_JSON not set in .env")
        print("  Set it to the path of your service account JSON file.")
        sys.exit(1)

    creds_file = Path(creds_path)
    if not creds_file.exists():
        print(f"ERROR: Service account file not found: {creds_file}")
        sys.exit(1)

    creds = Credentials.from_service_account_file(str(creds_file), scopes=SCOPES)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(SHEET_ID)
    return spreadsheet.worksheet(SHEET_TAB)


# ── Main logic ─────────────────────────────────────────────────────────────────

def clean(dry_run: bool):
    print(f"{'[DRY-RUN] ' if dry_run else ''}Connecting to sheet: {SHEET_TAB} ({SHEET_ID})")

    sheet = get_sheet()
    all_values = sheet.get_all_values()

    if not all_values:
        print("Sheet is empty.")
        return

    header = all_values[0]
    data_rows = all_values[1:]  # exclude header
    rows_before = len(data_rows)

    print(f"  Rows read: {rows_before} (+ 1 header)")

    # Identify column indices
    def col(name: str) -> int:
        try:
            return header.index(name)
        except ValueError:
            return -1

    url_col = col("url")
    company_col = col("company_name")
    category_col = col("category")
    score_col = col("score")
    status_col = col("status")

    if url_col == -1:
        print("ERROR: 'url' column not found in header row.")
        print(f"  Header: {header}")
        sys.exit(1)

    def get_cell(row: list, idx: int) -> str:
        return row[idx].strip() if idx >= 0 and idx < len(row) else ""

    def get_score(row: list) -> float:
        raw = get_cell(row, score_col)
        try:
            return float(raw)
        except (ValueError, TypeError):
            return 0.0

    # ── Step 1: Normalize URLs ─────────────────────────────────────────────────
    url_changes = []  # (row_index_in_data, old_url, new_url)
    for i, row in enumerate(data_rows):
        raw_url = get_cell(row, url_col)
        if not raw_url:
            continue
        normed = normalize_url(raw_url)
        if normed != raw_url:
            url_changes.append((i, raw_url, normed))
            # Mutate in place (we work on data_rows throughout)
            while len(data_rows[i]) <= url_col:
                data_rows[i].append("")
            data_rows[i] = list(data_rows[i])
            data_rows[i][url_col] = normed

    print(f"\n  URL normalization: {len(url_changes)} changes")
    for _, old, new in url_changes[:10]:
        print(f"    {old!r} → {new!r}")
    if len(url_changes) > 10:
        print(f"    ... and {len(url_changes) - 10} more")

    # ── Step 2: Remove rows with empty URL ────────────────────────────────────
    before_empty = len(data_rows)
    data_rows = [r for r in data_rows if get_cell(r, url_col)]
    removed_empty = before_empty - len(data_rows)
    print(f"\n  Empty URL rows removed: {removed_empty}")

    # ── Step 3: Remove test rows ───────────────────────────────────────────────
    def is_test_row(row: list) -> bool:
        company = get_cell(row, company_col).upper()
        category = get_cell(row, category_col).lower()
        return company in {n.upper() for n in TEST_COMPANY_NAMES} or category in TEST_CATEGORIES

    before_test = len(data_rows)
    test_removed = [r for r in data_rows if is_test_row(r)]
    data_rows = [r for r in data_rows if not is_test_row(r)]
    removed_test = before_test - len(data_rows)
    print(f"\n  Test rows removed: {removed_test}")
    for r in test_removed:
        print(f"    company={get_cell(r, company_col)!r}  category={get_cell(r, category_col)!r}")

    # ── Step 4: Deduplicate by normalized URL ──────────────────────────────────
    seen: dict[str, int] = {}  # normalized_url → index in data_rows
    duplicates_removed = 0

    deduped: list[list] = []
    for row in data_rows:
        url = get_cell(row, url_col)
        if not url:
            deduped.append(row)
            continue
        key = url  # already normalized above

        if key not in seen:
            seen[key] = len(deduped)
            deduped.append(row)
        else:
            existing_idx = seen[key]
            existing = deduped[existing_idx]
            existing_score = get_score(existing)
            new_score = get_score(row)

            if new_score > existing_score:
                # Replace with higher-scored duplicate
                print(f"    DEDUP keep newer: {key}  ({existing_score} → {new_score})")
                deduped[existing_idx] = row
            else:
                print(f"    DEDUP drop: {key}  (score {new_score} ≤ {existing_score})")
            duplicates_removed += 1

    data_rows = deduped
    print(f"\n  Duplicates removed: {duplicates_removed}")

    # ── Step 5: Remove trailing empty rows ────────────────────────────────────
    while data_rows and all(c == "" for c in data_rows[-1]):
        data_rows.pop()

    # ── Summary ────────────────────────────────────────────────────────────────
    rows_after = len(data_rows)
    total_removed = rows_before - rows_after

    print(f"\n{'=' * 50}")
    print(f"  Rows before : {rows_before}")
    print(f"  Rows after  : {rows_after}")
    print(f"  Total removed: {total_removed}")
    print(f"    – empty URL : {removed_empty}")
    print(f"    – test rows : {removed_test}")
    print(f"    – duplicates: {duplicates_removed}")
    print(f"{'=' * 50}")

    if dry_run:
        print("\n[DRY-RUN] No changes written. Run without --dry-run to apply.")
        return

    # ── Write back ─────────────────────────────────────────────────────────────
    print("\nWriting cleaned data back to sheet...")

    new_data = [header] + data_rows

    # Clear sheet and rewrite
    sheet.clear()
    if new_data:
        sheet.update(range_name="A1", values=new_data)

    print(f"Done. {rows_after} data rows written.")


def main():
    dry_run = "--dry-run" in sys.argv
    clean(dry_run=dry_run)


if __name__ == "__main__":
    main()
