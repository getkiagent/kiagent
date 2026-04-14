#!/usr/bin/env python3
"""Find missing business emails for leads.

Pipeline:
  1. Load leads/missing_emails.json (source of truth: company -> email|null).
  2. Resolve each company's URL from leads/batch-results-wave2.json or
     leads/batch-results.json (match on company_name).
  3. For every company with a null email, scrape contact-like pages via
     Firecrawl and regex-extract business emails.
  4. If regex yields nothing, fall back to Claude Haiku on the combined
     scrape text.
  5. Write the updated mapping back to missing_emails.json and log the
     companies that remain NULL.

API keys are read from .env (FIRECRAWL_API_KEY, ANTHROPIC_API_KEY).
Firecrawl scrapes are retried once on timeout/error.
"""

import json
import os
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

FIRECRAWL_KEY = os.getenv("FIRECRAWL_API_KEY")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")

if not FIRECRAWL_KEY:
    sys.exit("ERROR: FIRECRAWL_API_KEY not set in environment")
if not ANTHROPIC_KEY:
    sys.exit("ERROR: ANTHROPIC_API_KEY not set in environment")

from firecrawl import FirecrawlApp
from anthropic import Anthropic

firecrawl = FirecrawlApp(api_key=FIRECRAWL_KEY)
anthropic = Anthropic(api_key=ANTHROPIC_KEY)

HAIKU_MODEL = "claude-haiku-4-5-20251001"

CONTACT_PATHS = [
    "/impressum",
    "/kontakt",
    "/contact",
    "/pages/impressum",
    "/pages/kontakt",
]

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

# Generic / non-business addresses to filter out.
BLACKLIST_PREFIXES = (
    "noreply@",
    "no-reply@",
    "mailer-daemon@",
    "postmaster@",
)
BLACKLIST_DOMAINS = (
    "gmail.com",
    "googlemail.com",
)

PREFERRED_PREFIXES = (
    "info@",
    "kontakt@",
    "contact@",
    "hello@",
    "hallo@",
    "office@",
    "support@",
    "service@",
)

MISSING_FILE = ROOT / "leads" / "missing_emails.json"
WAVE2_FILE = ROOT / "leads" / "batch-results-wave2.json"
WAVE1_FILE = ROOT / "leads" / "batch-results.json"


def load_json(path: Path) -> dict | list | None:
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_url_index() -> dict[str, str]:
    """Map company_name -> website URL from both batch result files."""
    index: dict[str, str] = {}
    for path in (WAVE2_FILE, WAVE1_FILE):
        data = load_json(path)
        if not data:
            continue
        for entry in data.get("results", []):
            d = entry.get("data") or {}
            name = d.get("company_name")
            url = d.get("website") or entry.get("url")
            if name and url and name not in index:
                index[name] = url
    return index


def is_valid_email(email: str) -> bool:
    e = email.lower().strip()
    if any(e.startswith(p) for p in BLACKLIST_PREFIXES):
        return False
    domain = e.split("@", 1)[-1]
    if domain in BLACKLIST_DOMAINS:
        return False
    # Obvious junk captured by greedy regex (image extensions, etc.)
    if any(e.endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif")):
        return False
    return True


def pick_best(emails: list[str]) -> str | None:
    valid = [e for e in emails if is_valid_email(e)]
    if not valid:
        return None
    # Dedupe, preserve order.
    seen: set[str] = set()
    unique: list[str] = []
    for e in valid:
        low = e.lower()
        if low not in seen:
            seen.add(low)
            unique.append(e)
    for prefix in PREFERRED_PREFIXES:
        for e in unique:
            if e.lower().startswith(prefix):
                return e
    return unique[0]


def firecrawl_scrape(url: str) -> str:
    """Scrape a URL via Firecrawl, retry once on error. Returns markdown or ''."""
    for attempt in (1, 2):
        try:
            r = firecrawl.scrape(url, formats=["markdown"])
            content = r.markdown if hasattr(r, "markdown") else r.get("markdown", "")
            return content or ""
        except Exception as exc:
            if attempt == 2:
                print(f"    ! scrape failed ({url}): {exc}")
                return ""
    return ""


def haiku_extract(text: str) -> str | None:
    """Fallback: ask Claude Haiku to pull a business contact email."""
    if not text.strip():
        return None
    snippet = text[:8000]
    try:
        msg = anthropic.messages.create(
            model=HAIKU_MODEL,
            max_tokens=64,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Extrahiere die geschäftliche Kontakt-E-Mail-Adresse "
                        "aus dem folgenden Seiteninhalt. Antworte NUR mit der "
                        "E-Mail oder NULL.\n\n" + snippet
                    ),
                }
            ],
        )
        raw = msg.content[0].text.strip() if msg.content else ""
    except Exception as exc:
        print(f"    ! haiku failed: {exc}")
        return None
    if not raw or raw.upper() == "NULL":
        return None
    match = EMAIL_RE.search(raw)
    if not match:
        return None
    candidate = match.group(0)
    return candidate if is_valid_email(candidate) else None


def find_email(base_url: str) -> str | None:
    base = base_url.rstrip("/")
    collected_text: list[str] = []
    for path in CONTACT_PATHS:
        url = base + path
        print(f"    - scrape {path}")
        content = firecrawl_scrape(url)
        if not content:
            continue
        collected_text.append(content)
        found = pick_best(EMAIL_RE.findall(content))
        if found:
            print(f"      regex -> {found}")
            return found
    # Regex failed on all pages — try Haiku on combined text.
    if collected_text:
        print("    - regex empty, trying Haiku fallback")
        found = haiku_extract("\n\n".join(collected_text))
        if found:
            print(f"      haiku -> {found}")
            return found
    return None


def main() -> int:
    missing = load_json(MISSING_FILE)
    if not isinstance(missing, dict):
        sys.exit(f"ERROR: {MISSING_FILE} not found or invalid")

    url_index = build_url_index()
    targets = [c for c, e in missing.items() if not e]
    if not targets:
        print("Nothing to do — no null emails in missing_emails.json.")
        return 0

    print(f"Processing {len(targets)} companies without email...\n")

    still_missing: list[str] = []
    for company in targets:
        print(f"[{company}]")
        url = url_index.get(company)
        if not url:
            print("    ! no URL found in batch results, skipping")
            still_missing.append(company)
            continue
        email = find_email(url)
        if email:
            missing[company] = email
            print(f"  => {email}\n")
        else:
            still_missing.append(company)
            print("  => NICHT GEFUNDEN\n")

    with open(MISSING_FILE, "w", encoding="utf-8") as f:
        json.dump(missing, f, ensure_ascii=False, indent=2)
    print(f"Updated: {MISSING_FILE}")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    found_count = len(targets) - len(still_missing)
    print(f"Found:   {found_count}/{len(targets)}")
    print(f"Missing: {len(still_missing)}")
    if still_missing:
        print("\nStill NULL:")
        for c in still_missing:
            print(f"  - {c}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
