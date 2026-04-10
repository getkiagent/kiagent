"""
GetKiAgent — Stage 3: Lead Discovery

Findet DACH-Ecommerce-Brands via DuckDuckGo-Suche.
Gibt eine bereinigte URL-Liste aus, die direkt in batch_analyze.py genutzt werden kann.

Usage:
    python scripts/discover_leads.py
    python scripts/discover_leads.py --queries 5 --results 15

Output:
    leads/discovered-urls.txt   — neue, noch nicht analysierte Domains
"""

import sys
import argparse
import time
from pathlib import Path
from urllib.parse import urlparse

# Windows-Konsole auf UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Suchqueries ───────────────────────────────────────────────────────────────

SEARCH_QUERIES = [
    # ── Skincare DE — Long-Tail / Nische ─────────────────────────────────────
    ("Naturkosmetik online Shop versandkostenfrei", "de-de"),
    ("vegane Hautpflege Serum kaufen", "de-de"),
    ("clean beauty Shop Deutschland", "de-de"),
    ("nachhaltige Kosmetik Shop Deutschland", "de-de"),
    ("zero waste Kosmetik online kaufen", "de-de"),
    ("Naturkosmetik Marke gegründet", "de-de"),
    ("Bio Gesichtspflege zertifiziert COSMOS BDIH kaufen", "de-de"),
    ("plastikfreie Naturkosmetik online Shop", "de-de"),
    # ── Ingredient-basierte Queries ──────────────────────────────────────────
    ("Hyaluron Serum kaufen", "de-de"),
    ("Niacinamid Serum kaufen", "de-de"),
    ("Retinol Creme online kaufen", "de-de"),
    ("Vitamin C Serum Shop Deutschland", "de-de"),
    ("Bakuchiol Serum kaufen", "de-de"),
    # ── Supplements DE ────────────────────────────────────────────────────────
    ("Nahrungsergänzungsmittel Shop Kollagen Abo", "de-de"),
    ("vegane Proteinpulver Eigenmarke online kaufen", "de-de"),
    ("adaptogene Ashwagandha Nahrungsergänzung kaufen", "de-de"),
    ("Bio Supplements Vitamine Kapseln Online Shop", "de-de"),
    ("Vitamin Supplements Shop schweiz", "de-de"),
    # ── Wellness / CBD DE ─────────────────────────────────────────────────────
    ("Bio Skincare Abo bestellen", "de-de"),
    ("CBD Kosmetik Shop Österreich", "de-de"),
    ("CBD Öl Naturprodukte Shop online kaufen", "de-de"),
    # ── Natural Cosmetics / Hair / Body ──────────────────────────────────────
    ("vegane Naturkosmetik ohne Tierversuche Shop", "de-de"),
    ("Haarpflege Bio Shampoo Conditioner Online Shop", "de-de"),
    ("Naturkosmetik Deo vegan kaufen", "de-de"),
    ("Bio Körperpflege Shop nachhaltig", "de-de"),
    # ── Höhle der Löwen / Startup-Signals ────────────────────────────────────
    ("Höhle der Löwen Kosmetik", "de-de"),
    ("Höhle der Löwen Supplements", "de-de"),
    ("Startup Naturkosmetik Deutschland gegründet", "de-de"),
    # ── AT ────────────────────────────────────────────────────────────────────
    ("Naturkosmetik versandkostenfrei kaufen Eigenmarke site:.at", "at-de"),
    ("Nahrungsergänzungsmittel Bio Vitamine Shop site:.at", "at-de"),
    ("CBD Kosmetik Shop Österreich site:.at", "at-de"),
    # ── CH ────────────────────────────────────────────────────────────────────
    ("Naturkosmetik Schweiz online Shop Eigenmarke site:.ch", "ch-de"),
    ("Nahrungsergänzungsmittel Supplements kaufen site:.ch", "ch-de"),
]

# ── Filter ────────────────────────────────────────────────────────────────────

# Bekannte Plattformen, Marktplätze und irrelevante Domains ausschließen
DOMAIN_BLOCKLIST = {
    # Große Online-Marktplätze (DACH + international)
    "amazon", "ebay", "etsy", "otto", "zalando", "aboutyou", "about-you",
    "kaufland", "real.de", "netto-online",
    # Lebensmitteleinzelhandel mit Online-Shop
    "aldi", "lidl", "netto", "penny", "rewe", "edeka",
    # Elektronik-Retailer
    "mediamarkt", "saturn", "cyberport", "notebooksbilliger",
    # Fashion-Retailer
    "bonprix", "tchibo", "deichmann", "snipes", "galeria", "peek-cloppenburg",
    "hm", "zara", "c-und-a", "cunda",
    # Drogerie / Beauty-Retailer (nicht DTC)
    "dm", "rossmann", "mueller", "douglas", "flaconi", "notino",
    "shop-apotheke", "docmorris", "apotheke", "parfumdreams", "medpex",
    "galaxus", "breuninger",
    # Preisvergleich & Aggregatoren
    "idealo", "billiger", "geizhals", "preisvergleich", "check24", "verivox",
    "zecplus", "pricespy", "testberichte", "codecheck", "inci-beauty",
    # Supplement non-DTC
    "myprotein", "bulk.com", "nu3", "vitafy",
    # Medien / Beauty-Aggregatoren
    "utopia", "beautypunk",
    # Möbel / Home (Marktplätze)
    "wayfair", "westwing", "home24", "ikea",
    # Bücher / Medien
    "thalia", "weltbild", "hugendubel",
    # Soziale Netzwerke & Plattformen
    "google", "facebook", "instagram", "pinterest", "youtube", "wikipedia",
    "trustpilot", "reddit", "twitter", "tiktok", "linkedin", "xing",
    # CMS / Shop-Plattformen (keine Brands)
    "shopify", "woocommerce", "wordpress", "squarespace", "wix",
    # Presse / Medien
    "mynewsdesk", "presseportal", "businesswire", "prnewswire",
    "t-online", "spiegel", "focus", "stern", "zeit", "faz", "handelsblatt",
    "cosmopolitan", "vogue", "elle", "instyle", "glamour",
}

# Bereits analysierte Domains (aus batch-results.json) — nie erneut vorschlagen
ANALYZED_DOMAINS = {
    "junglueck.de", "junglück.de",
    "puremetics.de",
    "notino.de",
    "erbolario.de",
    "provida.de",
    "the-glow.com",
    "undgretel.com",
    "raw-naturkosmetik.de",
    "naturalsophy.com",
    "teamdrjoseph.com",
    "wesentlich.shop",
    "fiveskincare.de",
    "nature-heart.de",
    "tallows.de",
    "zendou.de",
    "pure-soul-shop.de",
    "nooideo.de",
    "meritbeauty.com",
    "feelslike.sport",
    "plantsarepurple.de",
    "yves-rocher.de",
    "grueneerde.com",
    "iplusm.berlin",
    "neo-organic.de",
}

# Nur diese TLDs sind relevant (DACH + international DTC)
ALLOWED_TLDS = {".de", ".at", ".ch", ".com", ".shop", ".store", ".berlin", ".bio"}


def is_relevant_domain(domain: str) -> bool:
    domain = domain.lower().removeprefix("www.")
    # Bereits analysierte Domains ausschließen
    if domain in ANALYZED_DOMAINS:
        return False
    # Blocklist prüfen
    for blocked in DOMAIN_BLOCKLIST:
        if blocked in domain:
            return False
    # TLD prüfen
    return any(domain.endswith(tld) for tld in ALLOWED_TLDS)


def extract_domain(url: str) -> str | None:
    try:
        parsed = urlparse(url if url.startswith("http") else "https://" + url)
        domain = parsed.netloc.lower().removeprefix("www.")
        return domain if domain else None
    except Exception:
        return None


# ── Discovery ─────────────────────────────────────────────────────────────────

def search_ddg(query: str, region: str, max_results: int) -> list[str]:
    try:
        from ddgs import DDGS
    except ImportError:
        print("ERROR: ddgs nicht installiert. Run: pip install ddgs")
        sys.exit(1)

    try:
        results = DDGS().text(query, region=region, max_results=max_results)
        return [r.get("href", "") for r in results if r.get("href")]
    except Exception as e:
        print(f"  Suche fehlgeschlagen: {e}")
        return []


def load_existing_urls(paths: list[str]) -> set[str]:
    """Lädt bereits bekannte Domains aus urls.txt und batch-results.json."""
    known = set()
    for path in paths:
        p = Path(path)
        if not p.exists():
            continue
        if p.suffix == ".txt":
            for line in p.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    d = extract_domain(line)
                    if d:
                        known.add(d)
        elif p.suffix == ".json":
            import json
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                for r in data.get("results", []):
                    d = extract_domain(r.get("url", ""))
                    if d:
                        known.add(d)
            except Exception:
                pass
    return known


def discover(num_queries: int, results_per_query: int) -> list[str]:
    queries = SEARCH_QUERIES[:min(num_queries, len(SEARCH_QUERIES))]
    existing = load_existing_urls([
        "leads/urls.txt",
        "leads/batch-results.json",
        "leads/discovered-urls.txt",
    ])
    print(f"  Bereits bekannte Domains: {len(existing)}")

    found_domains: dict[str, str] = {}  # domain -> full url

    for i, (query, region) in enumerate(queries, 1):
        print(f"\n  [{i}/{len(queries)}] {query}")
        urls = search_ddg(query, region, results_per_query)
        new = 0
        for url in urls:
            domain = extract_domain(url)
            if not domain:
                continue
            if domain in existing or domain in found_domains:
                continue
            if not is_relevant_domain(domain):
                continue
            found_domains[domain] = url
            new += 1
        print(f"           {new} neue Kandidaten")
        time.sleep(1)  # Rate-limit respektieren

    return list(found_domains.values())


# ── Output ────────────────────────────────────────────────────────────────────

def save_discovered(urls: list[str], output_path: str):
    p = Path(output_path)
    p.parent.mkdir(exist_ok=True)
    lines = ["# GetKiAgent — Discovered Leads (automatisch generiert)", ""]
    lines += [url for url in sorted(urls)]
    p.write_text("\n".join(lines), encoding="utf-8")


# ── Main ──────────────────────────────────────────────────────────────────────

def _sync_urls_to_sheet(urls: list[str]):
    """Trägt neue URLs mit leerem Status ins Sheet ein (Lead URL Scorer holt sie ab)."""
    import os
    import requests as req
    webhook_url = os.getenv("N8N_OUTREACH_WEBHOOK")
    if not webhook_url:
        return
    try:
        resp = req.post(
            webhook_url,
            json={"sync": True, "leads": [{"url": u} for u in urls]},
            timeout=30,
        )
        if resp.status_code == 200:
            print(f"  → Sheet sync OK: {len(urls)} URLs eingetragen")
        else:
            print(f"  → Sheet sync WARN: HTTP {resp.status_code}")
    except Exception as e:
        print(f"  → Sheet sync FEHLER: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--queries", type=int, default=99, help="Anzahl Suchqueries (Standard: alle)")
    parser.add_argument("--results", type=int, default=15, help="Ergebnisse pro Query")
    parser.add_argument("--output", default="leads/discovered-urls.txt")
    args = parser.parse_args()

    num_queries = min(args.queries, len(SEARCH_QUERIES))
    print(f"\nLead Discovery gestartet ({num_queries} von {len(SEARCH_QUERIES)} Queries)")
    print(f"  {num_queries} Queries x {args.results} Ergebnisse = max. {num_queries * args.results} URLs\n")

    urls = discover(num_queries, args.results)

    if not urls:
        print("\nKeine neuen Kandidaten gefunden.")
        return

    save_discovered(urls, args.output)
    _sync_urls_to_sheet(urls)

    print(f"\n{'=' * 50}")
    print(f"  {len(urls)} neue Domains gefunden")
    print(f"  Gespeichert in: {args.output}")
    print(f"{'=' * 50}")
    print("\nNaechster Schritt:")
    print(f"  python scripts/batch_analyze.py {args.output}")


if __name__ == "__main__":
    main()
