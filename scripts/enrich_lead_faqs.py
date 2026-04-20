#!/usr/bin/env python3
"""
enrich_lead_faqs.py

Scrape FAQ/Kontakt/Hilfe pages per lead and extract the single best
pointed_question + question_source_page + volume_hint for the
outreach_mail_v2 prompt (Braun 4T framework).

Reuses analyze_lead.scrape_pages (Jina-based, no Firecrawl key required).

Usage:
    python scripts/enrich_lead_faqs.py
    python scripts/enrich_lead_faqs.py --only jarmino,ylumi --force
    python scripts/enrich_lead_faqs.py --limit 5
"""

import argparse
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from analyze_lead import scrape_pages, extract_json  # reuse Jina scraper + JSON parser

import anthropic


LEADS_FILE = PROJECT_ROOT / "leads" / "qualified-leads.json"
FAQS_DIR = PROJECT_ROOT / "leads" / "faqs"
CACHE_DIR = PROJECT_ROOT / "leads" / "scrape-cache"

FAQ_PAGE_HINTS = [
    "faq", "hilfe", "help", "kontakt", "contact",
    "widerruf", "retoure", "return", "versand", "shipping",
]
MAX_PAGES_FOR_EXTRACTION = 5
MAX_CONTENT_CHARS_PER_PAGE = 4000
ANTHROPIC_MODEL = "claude-haiku-4-5-20251001"


EXTRACT_SYSTEM_PROMPT = """Du extrahierst aus gescrapten Shop-Seiten die EINE beste Kundenfrage, die das Team des Shops wahrscheinlich täglich beantwortet.

Regeln für pointed_question:
- EIN konkreter Satz mit Fragezeichen.
- Wortnah aus der FAQ/Kontakt-Seite übernommen. Keine Zusammenfassung, keine Umformulierung.
- Wenn die Originalfrage "Ist euer Kollagen vegan?" lautet, gib exakt diesen String zurück (inklusive Anführungszeichen sollen NICHT im Wert stehen, nur der reine Fragentext).
- Wähle die Frage mit dem höchsten wahrscheinlichen täglichen Volumen (fachlich, beratungsrelevant — nicht triviale Versandfragen wie "Wann kommt mein Paket?").

Regeln für question_source_page:
- Der Page-Label wo die Frage gefunden wurde (z.B. "/faq", "/hilfe", "/kontakt", "homepage").

Regeln für volume_hint:
- KURZ, ≤ 10 Wörter.
- Erklärt in Business-Sprache, warum diese Frage Volumen ergibt.
- Beispiele: "sieben Märkte und Abo-Modell", "komplexer Katalog mit Inhaltsstoff-Varianten", "hochpreisige Beratungsprodukte".

Wenn keine echte Kundenfrage findbar ist: gib pointed_question = "" (leer).

Output: AUSSCHLIESSLICH strict JSON mit exakt diesen drei Feldern. Kein Kommentar, kein Markdown-Codeblock um das JSON, nur das JSON-Objekt.
"""


def slugify(name: str) -> str:
    """Filename-safe ASCII slug matching generate_outreach.py convention."""
    s = name.strip()
    for src, dst in [("ä", "ae"), ("ö", "oe"), ("ü", "ue"),
                     ("Ä", "ae"), ("Ö", "oe"), ("Ü", "ue"), ("ß", "ss")]:
        s = s.replace(src, dst)
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "unbekannt"


def filter_faq_pages(pages: dict) -> dict:
    """Keep only pages that likely contain customer-facing Q&A content."""
    keep = {}
    for label, content in pages.items():
        lower = label.lower()
        if any(hint in lower for hint in FAQ_PAGE_HINTS):
            keep[label] = content
    return dict(list(keep.items())[:MAX_PAGES_FOR_EXTRACTION])


def build_user_message(lead: dict, pages: dict) -> str:
    data = lead.get("data", {})
    parts = [
        f"Shop: {data.get('company_name') or lead.get('url', '?')}",
        f"Website: {lead.get('url', '?')}",
        f"Kategorie: {data.get('category', '?')} | Land: {data.get('country', '?')}",
    ]
    sigs = data.get("support_pain_signals", [])
    if sigs:
        parts.append(f"Bekannte Pain-Signale: {', '.join(sigs[:3])}")
    parts.append("")
    parts.append("Gescrapte Seiten:")
    for label, content in pages.items():
        parts.append(f"=== PAGE: {label} ===")
        parts.append(content[:MAX_CONTENT_CHARS_PER_PAGE])
    return "\n".join(parts)


def extract_faq(lead: dict, pages: dict, client: anthropic.Anthropic) -> dict:
    """Single Haiku call that returns {pointed_question, question_source_page, volume_hint}."""
    faq_pages = filter_faq_pages(pages)

    # Fallback: if no FAQ/contact pages found, use homepage only
    if not faq_pages and "homepage" in pages:
        faq_pages = {"homepage": pages["homepage"]}

    if not faq_pages or not any(str(v).strip() for v in faq_pages.values()):
        return {
            "pointed_question": "",
            "question_source_page": "none",
            "volume_hint": "",
            "_error": "no_scrapable_pages",
        }

    user_msg = build_user_message(lead, faq_pages)

    resp = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=500,
        system=EXTRACT_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )

    raw = resp.content[0].text if resp.content else ""
    parsed = extract_json(raw)

    if not parsed or not isinstance(parsed, dict):
        return {
            "pointed_question": "",
            "question_source_page": "parse_error",
            "volume_hint": "",
            "_raw_response": raw[:300],
        }

    # Normalize fields + strip surrounding quotes from question if model added them
    pq = (parsed.get("pointed_question") or "").strip().strip('"').strip("'")
    qsp = (parsed.get("question_source_page") or "").strip() or "unknown"
    vh = (parsed.get("volume_hint") or "").strip()

    # Fallback from pain signals if model returned empty
    if not pq:
        sigs = lead.get("data", {}).get("support_pain_signals", [])
        if sigs:
            pq = f"Frage zu {sigs[0][:80]}"
            qsp = "fallback_pain_signal"
            if not vh:
                vh = (lead.get("data", {}).get("category") or "E-Commerce")[:60]

    return {
        "pointed_question": pq,
        "question_source_page": qsp,
        "volume_hint": vh,
    }


def match_slug(slug_filter: set, lead_slug: str) -> bool:
    """Match if any filter substring is in the lead slug."""
    return any(f in lead_slug for f in slug_filter)


def main():
    parser = argparse.ArgumentParser(description="Extract pointed FAQ questions per lead for outreach_mail_v2")
    parser.add_argument("--leads", default=str(LEADS_FILE), help="Path to qualified-leads.json")
    parser.add_argument("--only", default=None, help="Comma-separated slug substrings to filter leads")
    parser.add_argument("--limit", type=int, default=None, help="Max leads to process")
    parser.add_argument("--force", action="store_true", help="Overwrite existing FAQ files")
    args = parser.parse_args()

    try:
        from dotenv import load_dotenv
        load_dotenv(PROJECT_ROOT / ".env")
    except ImportError:
        pass

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY missing in env", file=sys.stderr)
        sys.exit(1)

    FAQS_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    with open(args.leads, "r", encoding="utf-8") as f:
        data = json.load(f)
    results = data.get("results", data if isinstance(data, list) else [])
    leads = [r for r in results if r.get("status") == "ok"]

    if args.only:
        only_filters = {s.strip().lower() for s in args.only.split(",") if s.strip()}
        leads = [
            l for l in leads
            if match_slug(only_filters, slugify(l.get("data", {}).get("company_name", "") or l.get("url", "")))
        ]

    if args.limit:
        leads = leads[: args.limit]

    client = anthropic.Anthropic(api_key=api_key)

    stats = {"processed": 0, "skipped": 0, "errors": 0, "empty": 0}

    for i, lead in enumerate(leads, 1):
        d = lead.get("data", {})
        company = d.get("company_name") or lead.get("url", "?")
        url = lead.get("url") or d.get("website") or ""
        slug = slugify(company)
        out_path = FAQS_DIR / f"{slug}.json"

        print(f"\n[{i}/{len(leads)}] {company}")

        if out_path.exists() and not args.force:
            print(f"  SKIP: {out_path.name} existiert bereits")
            stats["skipped"] += 1
            continue

        if not url:
            print(f"  WARN: keine URL")
            stats["errors"] += 1
            continue

        try:
            pages = scrape_pages(url, api_key=None, cache_dir=CACHE_DIR)
        except Exception as e:
            print(f"  ERROR scrape: {type(e).__name__}: {e}")
            stats["errors"] += 1
            continue

        try:
            extracted = extract_faq(lead, pages, client)
        except Exception as e:
            print(f"  ERROR extract: {type(e).__name__}: {e}")
            stats["errors"] += 1
            continue

        extracted["_meta"] = {
            "company_name": company,
            "url": url,
            "slug": slug,
            "scraped_page_labels": list(pages.keys()),
            "extracted_from_labels": list(filter_faq_pages(pages).keys()) or ["homepage"],
        }

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(extracted, f, ensure_ascii=False, indent=2)

        pq = extracted.get("pointed_question", "")
        qsp = extracted.get("question_source_page", "")
        vh = extracted.get("volume_hint", "")
        print(f"  -> pointed_question: {pq[:90]!r}")
        print(f"  -> source_page:      {qsp}")
        print(f"  -> volume_hint:      {vh}")
        print(f"  -> saved:            {out_path.name}")

        if pq:
            stats["processed"] += 1
        else:
            stats["empty"] += 1

    print(f"\n{'=' * 60}")
    print(f"FERTIG")
    print(f"  Mit Frage:  {stats['processed']}")
    print(f"  Leer:       {stats['empty']}")
    print(f"  Übersprungen: {stats['skipped']}")
    print(f"  Fehler:     {stats['errors']}")
    print(f"  Output:     {FAQS_DIR}")


if __name__ == "__main__":
    main()
