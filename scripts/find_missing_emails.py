#!/usr/bin/env python3
"""Find missing emails for leads via extended Firecrawl scraping + web search."""

import os
import re
import sys
import json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from firecrawl import FirecrawlApp
app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
BLACKLIST = {"noreply@", "no-reply@", "mailer-daemon@", "postmaster@", "datenschutz@", "privacy@", "widerrufsrecht@"}
PREFERRED = ["info@", "kontakt@", "contact@", "hello@", "office@", "support@", "hallo@", "service@", "hi@"]

EXTENDED_PATHS = [
    "/impressum", "/pages/impressum", "/kontakt", "/pages/kontakt",
    "/contact", "/ueber-uns", "/about", "/datenschutz",
    "/pages/datenschutz", "/pages/uber-uns", "/pages/about-us",
    "/pages/about", "/hilfe", "/pages/hilfe",
]

TARGETS = {
    "FairNatural":              "https://fairnatural.de",
    "GIILINEA BIO":             "https://giilinea.com",
    "HelloBody":                "https://hellobody.de",
    "KIYOMI SKIN":              "https://kiyomi-skin.de",
    "kollagen.shop":            "https://kollagen.shop",
    "MERIT Beauty":             "https://meritbeauty.com",
    "Nature Heart":             "https://nature-heart.de",
    "North Glow":               "https://northglow.de",
    "Ponyhutchen":              "https://ponyhuetchen.com",
    "Provida":                  "https://provida.de",
    "RAW Naturkosmetik":        "https://raw-naturkosmetik.de",
    "Sarem Cosmetics":          "https://sarem-cosmetics.de",
    "Sports Nutritions":        "https://sports-nutritions.com",
    "Zendou":                   "https://zendou.de",
}


def best_email(emails):
    valid = [e for e in emails if not any(e.lower().startswith(b) for b in BLACKLIST)]
    for p in PREFERRED:
        for e in valid:
            if e.lower().startswith(p):
                return e
    return valid[0] if valid else None


def scrape_for_email(base: str) -> tuple[str | None, str | None]:
    """Try extended paths, return (email, path_found)."""
    for path in EXTENDED_PATHS:
        url = base.rstrip("/") + path
        try:
            r = app.scrape(url, formats=["markdown"])
            content = r.markdown if hasattr(r, "markdown") else r.get("markdown", "")
            if not content:
                continue
            emails = EMAIL_RE.findall(content)
            email = best_email(emails)
            if email:
                return email, path
        except Exception:
            pass
    return None, None


results = {}
for company, base in TARGETS.items():
    print(f"[{company}] Suche...")
    email, path = scrape_for_email(base)
    if email:
        print(f"  -> {email} ({path})")
    else:
        print(f"  -> NICHT GEFUNDEN")
    results[company] = email

print("\n" + "="*60)
print("ERGEBNIS:")
for company, email in results.items():
    status = email if email else "NICHT GEFUNDEN"
    print(f"  {company}: {status}")

# Save results
out = Path(__file__).resolve().parent.parent / "leads" / "missing_emails.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\nGespeichert: {out}")
