#!/usr/bin/env python3
"""
GetKiAgent Outreach Engine v3
Generates personalized outreach emails from batch-results JSON.

Usage:
    python scripts/generate_outreach.py leads/batch-results.json
    python scripts/generate_outreach.py leads/batch-results.json --draft
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# Force UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv not installed. Run: pip install python-dotenv")
    sys.exit(1)

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic not installed. Run: pip install anthropic")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests")
    sys.exit(1)

try:
    from firecrawl import FirecrawlApp
    FIRECRAWL_AVAILABLE = True
except ImportError:
    FIRECRAWL_AVAILABLE = False

# Load .env from project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("ERROR: ANTHROPIC_API_KEY not set. Add it to .env or environment.")
    sys.exit(1)

MODEL = "claude-sonnet-4-6"
PROMPT_FILE = PROJECT_ROOT / "prompts" / "outreach_mail_v1.md"
OUTREACH_DIR = PROJECT_ROOT / "outreach"

CTA = "Habt ihr diese Woche 15 Minuten für einen kurzen Walkthrough?"


def load_leads(path: Path) -> list[dict]:
    """Load leads from batch-results JSON."""
    if not path.exists():
        print(f"ERROR: Leads file not found at {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [r for r in data.get("results", []) if r.get("status") == "ok"]


def load_prompt() -> str:
    """Load system prompt for mail generation."""
    if not PROMPT_FILE.exists():
        print(f"ERROR: Prompt file not found at {PROMPT_FILE}")
        sys.exit(1)
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read()


def filter_leads_by_score(leads: list[dict], min_score: int, max_score: int) -> list[dict]:
    """Return leads within score range (inclusive)."""
    result = []
    for lead in leads:
        d = lead.get("data", {})
        score = d.get("score_1_to_10", 0)
        if isinstance(score, (int, float)) and min_score <= score <= max_score:
            result.append(lead)
    return result


EMAIL_RE = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')
# Emails to ignore (generic, not useful for outreach)
EMAIL_BLACKLIST = {"noreply@", "no-reply@", "mailer-daemon@", "postmaster@"}


def _is_valid_email(email: str) -> bool:
    """Filter out noreply and other junk emails."""
    lower = email.lower()
    return not any(lower.startswith(bl) for bl in EMAIL_BLACKLIST)


def extract_email_from_json(lead_data: dict) -> str | None:
    """Extract email from all text fields in lead data via regex."""
    # 1. visible_contact_options — most likely to contain real addresses
    for opt in lead_data.get("visible_contact_options", []):
        match = EMAIL_RE.search(str(opt))
        if match and _is_valid_email(match.group(0)):
            return match.group(0)

    # 2. support_pain_signals
    for signal in lead_data.get("support_pain_signals", []):
        match = EMAIL_RE.search(str(signal))
        if match and _is_valid_email(match.group(0)):
            return match.group(0)

    # 3. Freetext fields (lower confidence — Claude may mention emails as suggestions)
    for field in ["recommended_next_action", "uncertainty_notes"]:
        text = lead_data.get(field, "")
        if text:
            match = EMAIL_RE.search(text)
            if match and _is_valid_email(match.group(0)):
                return match.group(0)

    return None


def extract_email_via_firecrawl(website: str) -> str | None:
    """Scrape contact/impressum pages via Firecrawl to find an email."""
    if not FIRECRAWL_AVAILABLE:
        print("  -> Firecrawl nicht installiert, ueberspringe Scraping")
        return None

    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        print("  -> FIRECRAWL_API_KEY fehlt, ueberspringe Scraping")
        return None

    app = FirecrawlApp(api_key=api_key)
    base = website.rstrip("/")

    # Try these paths in order
    paths = ["/pages/kontakt", "/kontakt", "/contact", "/impressum", "/pages/impressum"]

    for path in paths:
        url = base + path
        try:
            print(f"  -> Firecrawl: scrape {url}")
            result = app.scrape(url, formats=["markdown"])
            content = ""
            if isinstance(result, dict):
                content = result.get("markdown", "") or result.get("content", "")
            elif hasattr(result, "markdown"):
                content = result.markdown or ""

            if not content:
                continue

            # Find all emails, return the best one
            emails = EMAIL_RE.findall(content)
            valid = [e for e in emails if _is_valid_email(e)]
            if valid:
                # Prefer info@, kontakt@, hello@, office@ over random addresses
                preferred_prefixes = ["info@", "kontakt@", "contact@", "hello@", "office@", "support@"]
                for prefix in preferred_prefixes:
                    for e in valid:
                        if e.lower().startswith(prefix):
                            return e
                return valid[0]
        except Exception as e:
            err_str = str(e)[:100]
            print(f"  -> Firecrawl-Fehler bei {url}: {err_str}")
            continue

    return None


def extract_email(lead_data: dict) -> str | None:
    """Extract email: first from JSON fields, then via Firecrawl fallback."""
    # Step 1: Try JSON extraction
    email = extract_email_from_json(lead_data)
    if email:
        return email

    # Step 2: Firecrawl fallback
    website = lead_data.get("website", "")
    if website:
        print(f"  -> Keine Email im JSON, versuche Firecrawl...")
        email = extract_email_via_firecrawl(website)
        if email:
            print(f"  -> Email via Firecrawl gefunden: {email}")
            return email

    return None


def slugify(name: str) -> str:
    """Convert company name to filename-safe slug."""
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9äöüß]+", "-", slug)
    slug = slug.strip("-")
    return slug


def generate_mail(lead: dict, system_prompt: str, cta_index: int, previous_mails: list[str]) -> str:
    """Call Claude API to generate outreach mail. Passes previous mails for uniqueness."""
    lead_data = lead.get("data", {})
    company = lead_data.get("company_name", "Unknown")
    cta = CTA

    # Build context about previous mails to enforce uniqueness
    uniqueness_block = ""
    if previous_mails:
        uniqueness_block = (
            "\n\nWICHTIG — EINZIGARTIGKEIT:\n"
            "Die folgenden Mails wurden bereits generiert. "
            "Dein Mittelteil (Pain-Hook, Brücke, Vorschlag) MUSS sich komplett von diesen unterscheiden. "
            "Andere Satzstrukturen, anderer Einstieg, andere Formulierungen. "
            "KEIN Satz darf sich wörtlich oder sinngemäß wiederholen.\n\n"
        )
        for i, prev in enumerate(previous_mails):
            uniqueness_block += f"--- BEREITS GENERIERTE MAIL {i+1} ---\n{prev}\n\n"

    user_message = (
        f"Generiere eine Outreach-Mail für diesen Lead.\n\n"
        f"PFLICHT-CTA (verwende genau diesen CTA, angepasst an den Brand-Namen): {cta}\n\n"
        f"Lead-Daten:\n```json\n{json.dumps(lead_data, indent=2, ensure_ascii=False)}\n```"
        f"{uniqueness_block}"
    )

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = client.messages.create(
        model=MODEL,
        max_tokens=600,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    return response.content[0].text


def save_mail(company_name: str, mail_text: str) -> Path:
    """Save generated mail to outreach directory."""
    OUTREACH_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{slugify(company_name)}.txt"
    filepath = OUTREACH_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(mail_text)
    return filepath


def send_draft(webhook_url: str, to: str, subject: str, body: str, company: str):
    """Send mail as Gmail draft via n8n webhook."""
    payload = {"to": to, "subject": subject, "body": body}
    try:
        resp = requests.post(webhook_url, json=payload, timeout=15)
        if resp.ok:
            print(f"  -> Gmail-Entwurf erstellt für {company}")
        else:
            print(f"  -> WARNUNG: Webhook-Fehler für {company}: {resp.status_code} {resp.text[:200]}")
    except requests.RequestException as e:
        print(f"  -> WARNUNG: Webhook fehlgeschlagen für {company}: {e}")


def parse_subject(mail_text: str) -> str:
    """Extract subject line from generated mail."""
    for line in mail_text.splitlines():
        if line.strip().lower().startswith("betreff:"):
            return line.split(":", 1)[1].strip()
    return "Kurze Frage"


def parse_body(mail_text: str) -> str:
    """Extract body (everything after Betreff line)."""
    lines = mail_text.splitlines()
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("betreff:"):
            # Skip betreff line and any blank lines after it
            body_lines = lines[i+1:]
            # Strip leading blank lines
            while body_lines and not body_lines[0].strip():
                body_lines.pop(0)
            return "\n".join(body_lines)
    return mail_text


def main():
    parser = argparse.ArgumentParser(description="GetKiAgent Outreach Mail Generator v3")
    parser.add_argument("batch_file", help="Path to batch-results JSON file")
    parser.add_argument("--draft", action="store_true", help="Send mails as Gmail drafts via n8n webhook")
    parser.add_argument("--only", nargs="+", help="Only process leads whose website contains one of these strings")
    parser.add_argument("--force", action="store_true", help="Skip score filter, process all leads regardless of score")
    parser.add_argument("--min-score", type=int, default=8, help="Minimum score to include (default: 8)")
    parser.add_argument("--max-score", type=int, default=10, help="Maximum score to include (default: 10)")
    args = parser.parse_args()

    batch_path = Path(args.batch_file)
    leads = load_leads(batch_path)
    system_prompt = load_prompt()

    # Filter by score range unless --force
    if args.force:
        tier_a = leads
        print("--force aktiv: Score-Filter übersprungen")
    else:
        tier_a = filter_leads_by_score(leads, args.min_score, args.max_score)
    if not tier_a:
        print(f"Keine Leads mit Score {args.min_score}–{args.max_score} gefunden.")
        sys.exit(0)

    # Optional: filter to specific leads
    if args.only:
        tier_a = [
            l for l in tier_a
            if any(
                filt.lower() in l.get("data", {}).get("website", "").lower()
                or filt.lower() in l.get("data", {}).get("company_name", "").lower()
                for filt in args.only
            )
        ]
        if not tier_a:
            print(f"Keine Leads gefunden die zu --only {args.only} passen.")
            sys.exit(0)

    print(f"Gefunden: {len(tier_a)} Tier-A-Leads (Score 8+)")

    # Check webhook URL if --draft
    webhook_url = None
    if args.draft:
        webhook_url = os.getenv("N8N_WEBHOOK_URL")
        if not webhook_url:
            print("ERROR: --draft gesetzt, aber N8N_WEBHOOK_URL fehlt in .env")
            sys.exit(1)
        print(f"Draft-Modus aktiv — Webhook: {webhook_url[:50]}...")

    previous_mails: list[str] = []
    stats = {"generated": 0, "drafted": 0, "no_email": 0}

    for i, lead in enumerate(tier_a):
        lead_data = lead.get("data", {})
        company = lead_data.get("company_name", "Unknown")
        score = lead_data.get("score_1_to_10", "?")
        email = extract_email(lead_data)

        print(f"\n{'='*60}")
        print(f"[{i+1}/{len(tier_a)}] {company} — Score {score}/10")
        if email:
            print(f"  Email: {email}")
        else:
            print(f"  Email: NICHT GEFUNDEN — wird manuell eingetragen")

        # Generate mail
        mail_text = generate_mail(lead, system_prompt, cta_index=i, previous_mails=previous_mails)
        previous_mails.append(mail_text)

        # If no email, add placeholder
        if not email:
            mail_text = mail_text.replace("Hi,", "An: [EMAIL MANUELL EINTRAGEN]\n\nHi,", 1)
            stats["no_email"] += 1

        # Save locally
        filepath = save_mail(company, mail_text)
        print(f"  -> Gespeichert: {filepath}")
        stats["generated"] += 1

        # Print mail
        print(f"{'-'*40}")
        print(mail_text)
        print(f"{'-'*40}")

        # Send draft if --draft and email exists
        if args.draft and email:
            subject = parse_subject(mail_text)
            body = parse_body(mail_text)
            send_draft(webhook_url, email, subject, body, company)
            stats["drafted"] += 1
        elif args.draft and not email:
            print(f"  -> KEIN Webhook — keine Email-Adresse für {company}")

    # Summary
    print(f"\n{'='*60}")
    print(f"FERTIG")
    print(f"  Generiert: {stats['generated']} Mails")
    print(f"  Ohne Email: {stats['no_email']} (manuell nachtragen)")
    if args.draft:
        print(f"  Gmail-Entwürfe: {stats['drafted']}")
    print(f"  Ausgabeverzeichnis: {OUTREACH_DIR}/")


if __name__ == "__main__":
    main()
