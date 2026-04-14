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


# Load .env from project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("ERROR: ANTHROPIC_API_KEY not set. Add it to .env or environment.")
    sys.exit(1)

MODEL = "claude-sonnet-4-6"
PROMPT_FILE = PROJECT_ROOT / "prompts" / "outreach_mail_v1.md"
PROMPT_TIER_B_FILE = PROJECT_ROOT / "prompts" / "outreach_mail_tier_b_v1.md"
FOLLOWUP_PROMPT_FILE = PROJECT_ROOT / "prompts" / "followup_v1.md"
OUTREACH_DIR = PROJECT_ROOT / "outreach"
FOLLOWUP_DIR = PROJECT_ROOT / "outreach" / "followup"

CTA = "Habt ihr diese Woche 15 Minuten für einen kurzen Walkthrough?"


def load_leads(path: Path) -> list[dict]:
    """Load leads from batch-results JSON."""
    if not path.exists():
        print(f"ERROR: Leads file not found at {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Support both {"results": [...]} and direct list format
    if isinstance(data, list):
        results = data
    else:
        results = data.get("results", [])
    return [r for r in results if r.get("status") == "ok"]


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
    """Extract email from freetext JSON fields via regex (fallback only)."""
    for signal in lead_data.get("support_pain_signals", []):
        match = EMAIL_RE.search(str(signal))
        if match and _is_valid_email(match.group(0)):
            return match.group(0)

    for field in ["recommended_next_action", "uncertainty_notes"]:
        text = lead_data.get(field, "")
        if text:
            match = EMAIL_RE.search(text)
            if match and _is_valid_email(match.group(0)):
                return match.group(0)

    return None


JINA_BASE = "https://r.jina.ai/"
JINA_HEADERS = {"Accept": "text/markdown", "X-Return-Format": "markdown"}


def extract_email_via_jina(website: str) -> str | None:
    """Scrape contact/impressum pages via Jina reader (free) to find an email."""
    base = website.rstrip("/")
    paths = ["/pages/kontakt", "/kontakt", "/contact", "/impressum", "/pages/impressum"]

    for path in paths:
        url = base + path
        try:
            print(f"  -> Jina: scrape {url}")
            r = requests.get(f"{JINA_BASE}{url}", headers=JINA_HEADERS, timeout=20)
            content = r.text if r.status_code == 200 else ""
            if not content:
                continue

            emails = EMAIL_RE.findall(content)
            valid = [e for e in emails if _is_valid_email(e)]
            if valid:
                preferred_prefixes = ["info@", "kontakt@", "contact@", "hello@", "office@", "support@"]
                for prefix in preferred_prefixes:
                    for e in valid:
                        if e.lower().startswith(prefix):
                            return e
                return valid[0]
        except Exception as e:
            print(f"  -> Jina-Fehler bei {url}: {str(e)[:200]}")
            continue

    return None


def extract_email(lead_data: dict) -> str | None:
    """Extract email: contact_email field → regex fallback → Firecrawl."""
    # Step 1: contact_email set by Claude during lead analysis
    contact_email = lead_data.get("contact_email")
    if contact_email:
        match = EMAIL_RE.fullmatch(str(contact_email).strip())
        if match and _is_valid_email(match.group(0)):
            return match.group(0)

    # Step 2: regex on freetext fields
    email = extract_email_from_json(lead_data)
    if email:
        return email

    # Step 3: Firecrawl fallback
    website = lead_data.get("website", "")
    if website:
        print(f"  -> Keine Email im JSON, versuche Firecrawl...")
        email = extract_email_via_jina(website)
        if email:
            print(f"  -> Email via Firecrawl gefunden: {email}")
            return email

    return None


def slugify(name: str) -> str:
    """Convert company name to filename-safe slug."""
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9äöüß]+", "-", slug)
    slug = slug.strip("-")
    return slug or "unbekannt"


def find_original_mail(company_name: str) -> str | None:
    """Find the original outreach file for a company."""
    slug = slugify(company_name)
    path = OUTREACH_DIR / f"{slug}.txt"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return None


META_PROMPT_MODEL = "claude-haiku-4-5-20251001"

META_PROMPT_SYSTEM = """Du bist ein B2B-Sales-Stratege für KI-Kundenservice-Automatisierung im DACH-E-Commerce.

Deine Aufgabe: Analysiere die Lead-Daten und erstelle einen präzisen, lead-spezifischen Briefing-Prompt für den Copywriter, der die Outreach-Mail schreibt.

Dein Output ist NUR der Briefing-Prompt (kein Kommentar, keine Mail). Der Prompt muss enthalten:
1. HOOK-STRATEGIE: Welcher konkrete Pain Point dieses Leads am stärksten ist und wie der Einstieg ihn adressieren soll (mit Begründung aus den Daten)
2. TONALITÄT: Wie formell/locker basierend auf Brand-Auftritt (z.B. Premium-Brand → professionell, junges DTC → locker-direkt)
3. BRÜCKE: Welches spezifische Automatisierungs-Szenario für diesen Lead am relevantesten ist (WISMO, Retouren, Produktberatung, FAQ) — mit Bezug auf deren aktuelle Support-Schwächen
4. VERMEIDEN: Was bei diesem Lead NICHT funktioniert (z.B. keine Preise nennen wenn Premium-Brand, keine Tech-Details wenn Lifestyle-Marke)

Halte den Prompt unter 200 Wörter. Sei konkret, nicht generisch."""


def generate_meta_prompt(lead_data: dict, client: anthropic.Anthropic) -> str:
    """Step 1: Generate a lead-specific briefing prompt via Haiku."""
    try:
        response = client.messages.create(
            model=META_PROMPT_MODEL,
            max_tokens=400,
            system=META_PROMPT_SYSTEM,
            messages=[{"role": "user", "content": json.dumps(lead_data, ensure_ascii=False)}],
        )
    except anthropic.APIError as e:
        raise RuntimeError(f"Claude API-Fehler (Haiku): {e}") from e
    if not response.content:
        raise RuntimeError("Claude (Haiku) hat leeren Content zurückgegeben")
    return response.content[0].text


def generate_mail(lead: dict, system_prompt: str, cta_index: int, previous_mails: list[str], original_mail: str | None = None, inject_cta: bool = True) -> str:
    """Call Claude API to generate outreach or follow-up mail (with meta-prompting)."""
    lead_data = lead.get("data", {})
    company = lead_data.get("company_name", "Unknown")
    cta = CTA

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # Step 1: Meta-prompt — Haiku generates a lead-specific briefing
    print(f"  -> Meta-Prompt: Haiku analysiert {company}...")
    meta_briefing = generate_meta_prompt(lead_data, client)
    print(f"  -> Briefing generiert ({len(meta_briefing)} Zeichen)")

    # Merge: base system prompt + dynamic briefing
    enhanced_prompt = (
        f"{system_prompt}\n\n"
        f"## LEAD-SPEZIFISCHES BRIEFING (von Sales-Stratege erstellt)\n\n"
        f"{meta_briefing}"
    )

    # Build context about previous mails to enforce uniqueness (max 3 to avoid token bloat)
    uniqueness_block = ""
    recent_mails = previous_mails[-3:]
    if recent_mails:
        uniqueness_block = (
            "\n\nWICHTIG — EINZIGARTIGKEIT:\n"
            "Die folgenden Mails wurden bereits generiert. "
            "Dein Mittelteil (Pain-Hook, Brücke, Vorschlag) MUSS sich komplett von diesen unterscheiden. "
            "Andere Satzstrukturen, anderer Einstieg, andere Formulierungen. "
            "KEIN Satz darf sich wörtlich oder sinngemäß wiederholen.\n\n"
        )
        for i, prev in enumerate(recent_mails):
            uniqueness_block += f"--- BEREITS GENERIERTE MAIL {i+1} ---\n{prev}\n\n"

    if original_mail:
        user_message = (
            f"Generiere eine Follow-Up Mail für diesen Lead.\n\n"
            f"ERSTMAIL (Betreff und Inhalt — für Bezug und Neuwert-Differenzierung):\n{original_mail}\n\n"
            f"Lead-Daten:\n```json\n{json.dumps(lead_data, ensure_ascii=False)}\n```"
            f"{uniqueness_block}"
        )
    else:
        if inject_cta:
            user_message = (
                f"Generiere eine Outreach-Mail für diesen Lead.\n\n"
                f"PFLICHT-CTA (verwende genau diesen CTA, angepasst an den Brand-Namen): {cta}\n\n"
                f"Lead-Daten:\n```json\n{json.dumps(lead_data, ensure_ascii=False)}\n```"
                f"{uniqueness_block}"
            )
        else:
            user_message = (
                f"Generiere eine Outreach-Mail für diesen Lead.\n\n"
                f"Lead-Daten:\n```json\n{json.dumps(lead_data, ensure_ascii=False)}\n```"
                f"{uniqueness_block}"
            )

    # Step 2: Sonnet generates mail using enhanced prompt
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=600,
            system=enhanced_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
    except anthropic.APIError as e:
        raise RuntimeError(f"Claude API-Fehler (Sonnet): {e}") from e
    if not response.content:
        raise RuntimeError("Claude (Sonnet) hat leeren Content zurückgegeben")
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


def validate_quality_gates(mail_text: str, config: dict) -> list[str]:
    """Validate mail against niche config quality gates. Returns list of failures."""
    gates = config.get("outreach", {}).get("quality_gates", {})
    if not gates:
        return []

    failures = []
    # Word count (body only — exclude Betreff, P.S., Signatur)
    body = parse_body(mail_text)
    body_lines = [l for l in body.splitlines() if not l.strip().startswith("P.S.") and l.strip() not in ("Ilias", "GetKiAgent — KI-Support für E-Commerce", "")]
    word_count = sum(len(l.split()) for l in body_lines)
    max_words = gates.get("max_main_body_words_tier_a", 120)
    if word_count > max_words:
        failures.append(f"Body {word_count} Wörter (max {max_words})")

    # Forbidden phrases
    for phrase in gates.get("forbidden_phrases", []):
        if phrase.lower() in mail_text.lower():
            failures.append(f"Verbotene Phrase: '{phrase}'")

    # Company name in subject
    if gates.get("require_company_name_in_subject"):
        subject = parse_subject(mail_text)
        # Can't validate without knowing company name — skip here

    # P.S. with demo
    if gates.get("require_ps_with_demo"):
        if "P.S." not in mail_text:
            failures.append("P.S.-Zeile fehlt")

    return failures


def main():
    sys.path.insert(0, str(Path(__file__).parent))
    from niche_config import load_niche_config, niche_outreach_dir

    parser = argparse.ArgumentParser(description="GetKiAgent Outreach Mail Generator v3")
    parser.add_argument("batch_file", help="Path to batch-results JSON file")
    parser.add_argument("--draft", action="store_true", help="Send mails as Gmail drafts via n8n webhook")
    parser.add_argument("--followup", action="store_true", help="Generate follow-up mails using followup_v1.md prompt")
    parser.add_argument("--only", nargs="+", help="Only process leads whose website contains one of these strings")
    parser.add_argument("--force", action="store_true", help="Skip score filter, process all leads regardless of score")
    parser.add_argument("--min-score", type=int, default=7, help="Minimum score to include (default: 7)")
    parser.add_argument("--max-score", type=int, default=10, help="Maximum score to include (default: 10)")
    parser.add_argument("--prompt", type=str, default=None, help="Path to custom system prompt file (overrides default)")
    parser.add_argument("--niche", default=None, help="Niche name — loads config from configs/{niche}.yaml")
    args = parser.parse_args()

    niche_config = load_niche_config(args.niche)
    batch_path = Path(args.batch_file)
    leads = load_leads(batch_path)

    # Determine output dir and prompt based on niche config
    if niche_config and not args.followup and not args.prompt:
        output_dir = niche_outreach_dir(args.niche)

        # Check Guard Rail 5: demo_url required
        demo_url = niche_config.get("niche", {}).get("demo_url")
        if not demo_url:
            print(f"ERROR: demo_url nicht gesetzt in configs/{args.niche}.yaml — Outreach blockiert.")
            sys.exit(1)

        # Load prompt from config paths
        outreach_cfg = niche_config.get("outreach", {})
        tier_a_path = PROJECT_ROOT / outreach_cfg.get("tier_a_prompt_file", "prompts/outreach_mail_v1.md")
        tier_b_path = PROJECT_ROOT / outreach_cfg.get("tier_b_prompt_file", "prompts/outreach_mail_tier_b_v1.md")

        if not tier_a_path.exists():
            print(f"ERROR: Tier-A-Prompt nicht gefunden: {tier_a_path}")
            sys.exit(1)
        with open(tier_a_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()
        print(f"Niche-Modus: {args.niche} | Prompt: {tier_a_path.name} | Output: {output_dir}")
    elif args.followup:
        if not FOLLOWUP_PROMPT_FILE.exists():
            print(f"ERROR: Follow-up prompt not found at {FOLLOWUP_PROMPT_FILE}")
            sys.exit(1)
        with open(FOLLOWUP_PROMPT_FILE, "r", encoding="utf-8") as f:
            system_prompt = f.read()
        output_dir = FOLLOWUP_DIR
        if args.niche:
            output_dir = niche_outreach_dir(args.niche) / "followup"
            output_dir.mkdir(parents=True, exist_ok=True)
        output_dir.mkdir(parents=True, exist_ok=True)
        print("Follow-up Modus aktiv — nutze followup_v1.md")
    elif args.prompt:
        custom_path = Path(args.prompt)
        if not custom_path.exists():
            print(f"ERROR: Prompt-Datei nicht gefunden: {custom_path}")
            sys.exit(1)
        with open(custom_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()
        output_dir = niche_outreach_dir(args.niche) if args.niche else OUTREACH_DIR
        print(f"Custom Prompt: {custom_path.name}")
    else:
        system_prompt = load_prompt()
        output_dir = OUTREACH_DIR

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

    print(f"Gefunden: {len(tier_a)} Leads (Score {args.min_score}+)")

    # Check webhook URL if --draft
    webhook_url = None
    if args.draft:
        webhook_url = os.getenv("N8N_WEBHOOK_URL")
        if not webhook_url:
            print("ERROR: --draft gesetzt, aber N8N_WEBHOOK_URL fehlt in .env")
            sys.exit(1)
        print(f"Draft-Modus aktiv — Webhook: {webhook_url[:50]}...")

    previous_mails: list[str] = []
    stats = {"generated": 0, "drafted": 0, "no_email": 0, "errors": 0}

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

        # Per-lead prompt selection: score 7 → Tier B, score 8+ → Tier A
        if not args.followup and not args.prompt and not args.force:
            if score <= 7:
                # Determine Tier B prompt path (niche config or default)
                if niche_config:
                    tier_b_file = PROJECT_ROOT / niche_config.get("outreach", {}).get(
                        "tier_b_prompt_file", "prompts/outreach_mail_tier_b_v1.md")
                else:
                    tier_b_file = PROMPT_TIER_B_FILE
                if not tier_b_file.exists():
                    print(f"  -> WARNUNG: Tier-B-Prompt nicht gefunden ({tier_b_file}) — nutze Tier-A")
                    active_prompt = system_prompt
                else:
                    with open(tier_b_file, "r", encoding="utf-8") as f:
                        active_prompt = f.read()
                    print(f"  -> Tier B Prompt aktiv (Score {score})")
            else:
                active_prompt = system_prompt
        else:
            active_prompt = system_prompt

        # Generate mail
        original_mail = find_original_mail(company) if args.followup else None
        if args.followup and not original_mail:
            print(f"  -> WARNUNG: Keine Erstmail gefunden für {company} — generiere ohne Kontext")
        try:
            mail_text = generate_mail(lead, active_prompt, cta_index=i, previous_mails=previous_mails, original_mail=original_mail, inject_cta=args.prompt is None)
        except RuntimeError as e:
            print(f"  -> FEHLER: {e} — überspringe {company}")
            stats["errors"] += 1
            continue
        previous_mails.append(mail_text)  # only append on success

        # If no email, add placeholder
        if not email:
            mail_text = mail_text.replace("Hi,", "An: [EMAIL MANUELL EINTRAGEN]\n\nHi,", 1)
            stats["no_email"] += 1

        # Quality gate validation (niche config)
        if niche_config:
            gate_failures = validate_quality_gates(mail_text, niche_config)
            if gate_failures:
                print(f"  -> Quality Gate WARN:")
                for f in gate_failures:
                    print(f"     - {f}")

        # Save locally
        output_dir.mkdir(parents=True, exist_ok=True)
        slug = slugify(company)
        filename = f"{slug}.txt"
        filepath = output_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(mail_text)
        print(f"  -> Gespeichert: {filepath}")
        stats["generated"] += 1

        # Print mail
        print(f"{'-'*40}")
        print(mail_text)
        print(f"{'-'*40}")

        # Send draft if --draft and email exists
        if args.draft and email:
            subject = parse_subject(mail_text)
            # Follow-up: prefix subject with "Re: " if not already present
            if args.followup and not subject.lower().startswith("re:"):
                subject = f"Re: {subject}"
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
    if stats["errors"]:
        print(f"  Fehler: {stats['errors']} Mails nicht generiert (API-Fehler)")
    if args.draft:
        print(f"  Gmail-Entwürfe: {stats['drafted']}")
    print(f"  Ausgabeverzeichnis: {output_dir}/")


if __name__ == "__main__":
    main()