#!/usr/bin/env python3
"""
GetKiAgent Lead Observations Scraper

Nimmt eine enriched Leads-JSON, holt pro Domain 3 konkrete Observations:
  1. Live-Chat-Widget: welcher Anbieter (falls vorhanden) oder None
  2. FAQ-Status: Seite vorhanden + grobe Anzahl Fragen
  3. Kontakt-Kanäle: E-Mail, Telefon, WhatsApp, Kontaktformular

Source-HTML-Scan reicht — Chat-Widgets stehen als <script>-Tag drin, auch ohne JS-Render.

Usage:
    python scripts/scrape_observations.py leads/beauty/qualified-top50-enriched.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Safari/537.36"
REQUEST_TIMEOUT = 15
DELAY_BETWEEN_LEADS = 3.0

CHAT_WIDGETS = {
    "Intercom":    ["widget.intercom.io", "intercomcdn"],
    "Tidio":       ["code.tidio.co", "tidio.co/chat"],
    "Userlike":    ["userlike.com/api", "userlike.com/s"],
    "HubSpot":     ["js.hs-scripts.com", "js.hs-banner.com"],
    "Zendesk":     ["static.zdassets.com", "zopim.com"],
    "Crisp":       ["client.crisp.chat"],
    "LiveChat":    ["cdn.livechatinc.com"],
    "Shopify Inbox": ["shopify.com/chat", "apps.shopify.com/inbox"],
    "Freshchat":   ["wchat.freshchat.com"],
    "Drift":       ["js.driftt.com", "widget.drift.com"],
    "Trengo":      ["static.trengo.eu"],
}

FAQ_PATHS = ["/faq", "/pages/faq", "/haeufige-fragen", "/haeufig-gestellte-fragen", "/hilfe", "/help", "/support"]
CONTACT_PATHS = ["/kontakt", "/pages/kontakt", "/contact", "/impressum", "/pages/impressum"]

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:\+?49[\s\-]?|0)[\s\d\-/()]{7,}")
WHATSAPP_RE = re.compile(r"(?:wa\.me|api\.whatsapp\.com|whatsapp://)", re.IGNORECASE)
FAQ_ITEM_HINTS = [
    re.compile(r"<details[\s>]", re.IGNORECASE),
    re.compile(r"<summary[\s>]", re.IGNORECASE),
    re.compile(r'class=["\'][^"\']*(accordion|faq-item|faq__item)', re.IGNORECASE),
]


def get(url: str) -> str | None:
    try:
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=REQUEST_TIMEOUT, allow_redirects=True)
    except requests.RequestException:
        return None
    if r.status_code != 200 or not r.text:
        return None
    return r.text


def detect_chat_widget(html: str) -> str | None:
    low = html.lower()
    for name, needles in CHAT_WIDGETS.items():
        if any(n.lower() in low for n in needles):
            return name
    return None


def count_faq_items(html: str) -> int:
    count = 0
    for pat in FAQ_ITEM_HINTS:
        count += len(pat.findall(html))
    return count


def probe_paths(base: str, paths: list[str]) -> tuple[str | None, str | None]:
    """Try each path; return (matched_path, html) on first success."""
    for p in paths:
        html = get(base.rstrip("/") + p)
        if html and len(html) > 500:
            return p, html
    return None, None


def extract_contact_channels(html: str) -> dict:
    emails = sorted({e for e in EMAIL_RE.findall(html) if not e.lower().endswith((".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif"))})
    phones = PHONE_RE.findall(html)
    phones_clean = sorted({re.sub(r"\s+", " ", p.strip()) for p in phones if len(re.sub(r"\D", "", p)) >= 7})
    has_whatsapp = bool(WHATSAPP_RE.search(html))
    has_form = ("<form" in html.lower()) and ("contact" in html.lower() or "kontakt" in html.lower())
    return {
        "email": emails[0] if emails else "",
        "phone": phones_clean[0] if phones_clean else "",
        "whatsapp": has_whatsapp,
        "contact_form": has_form,
    }


def scrape_one(lead: dict) -> dict:
    domain = lead.get("domain") or ""
    if not domain:
        return {"chat_widget": None, "faq": {"found": False, "item_count": 0}, "contact": {}}

    base = f"https://{domain}"
    home = get(base)
    widget = detect_chat_widget(home) if home else None

    faq_path, faq_html = probe_paths(base, FAQ_PATHS)
    faq_info = {"found": bool(faq_path), "path": faq_path or "", "item_count": count_faq_items(faq_html) if faq_html else 0}

    contact_path, contact_html = probe_paths(base, CONTACT_PATHS)
    contact_info = extract_contact_channels(contact_html) if contact_html else {"email": "", "phone": "", "whatsapp": False, "contact_form": False}
    contact_info["source_path"] = contact_path or ""

    return {"chat_widget": widget, "faq": faq_info, "contact": contact_info}


def main() -> int:
    parser = argparse.ArgumentParser(description="Scrape 3 observations per lead (chat/faq/contact)")
    parser.add_argument("input_file", help="Path to enriched leads JSON (from enrich_contacts.py)")
    parser.add_argument("--output", default=None, help="Output path (default: overwrite input)")
    args = parser.parse_args()

    in_path = Path(args.input_file)
    if not in_path.exists():
        print(f"ERROR: {in_path} nicht gefunden")
        return 1

    data = json.loads(in_path.read_text(encoding="utf-8"))
    leads = data.get("results", [])
    if not leads:
        print("Keine Leads in Input-File.")
        return 1

    print(f"Scrape {len(leads)} Domains...\n")

    for i, lead in enumerate(leads, 1):
        domain = lead.get("domain") or ""
        if not domain:
            # Fallback: derive from url field
            url = lead.get("url", "")
            domain = url.replace("https://", "").replace("http://", "").split("/")[0].lstrip("www.")
            lead["domain"] = domain
        print(f"[{i}/{len(leads)}] {domain}")
        try:
            obs = scrape_one(lead)
        except Exception as exc:
            print(f"    FEHLER: {exc}")
            obs = {"chat_widget": None, "faq": {"found": False, "item_count": 0}, "contact": {}, "error": str(exc)[:200]}
        lead.setdefault("data", {})["observations"] = obs
        print(f"    chat={obs.get('chat_widget') or 'none'} faq={obs['faq'].get('found')} contact_email={obs['contact'].get('email') or '-'}")
        time.sleep(DELAY_BETWEEN_LEADS)

    out_path = Path(args.output) if args.output else in_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nGeschrieben: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
