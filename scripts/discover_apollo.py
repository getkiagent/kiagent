"""
GetKiAgent — Apollo Lead Discovery

Queries Apollo REST API for DACH e-commerce companies by niche.
Deduplicates against all known leads and writes a URL list for batch_analyze.py.

Usage:
    python scripts/discover_apollo.py --niche beauty
    python scripts/discover_apollo.py --niche supplements --pages 3
    python scripts/discover_apollo.py --niche cbd --all-tech
    python scripts/discover_apollo.py --niche pet --pages 5 --per-page 100

Environment:
    APOLLO_API_KEY  — required

Output:
    leads/apollo-domains-{niche}-{YYYY-MM-DD}.txt
"""

import argparse
import json
import os
import sys
import time
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

load_dotenv()

# ── Apollo API ────────────────────────────────────────────────────────────────

APOLLO_API_BASE = "https://api.apollo.io/api/v1"
APOLLO_ORGS_ENDPOINT = f"{APOLLO_API_BASE}/mixed_companies/search"

# Rate limit: Apollo free/basic allows ~10 req/s — 1s delay is safe
DELAY_BETWEEN_PAGES = 1.5


# ── Niche configs ─────────────────────────────────────────────────────────────

NICHE_CONFIGS: dict[str, dict] = {
    "beauty": {
        "label": "Beauty / Skincare",
        "keyword_tags": [
            "beauty", "skincare", "cosmetics", "skin care",
            "naturkosmetik", "kosmetik", "personal care",
            "direct-to-consumer", "dtc", "subscription box",
            "clean beauty", "vegan cosmetics", "indie beauty",
        ],
        "output_suffix": "beauty",
    },
    "supplements": {
        "label": "Supplements / Nutrition",
        "keyword_tags": [
            "dietary supplements", "supplements", "nutrition", "vitamins",
            "nutraceuticals", "health supplements", "nahrungsergaenzung",
        ],
        "output_suffix": "supplements",
    },
    "cbd": {
        "label": "CBD / Hemp",
        "keyword_tags": [
            "cbd", "hemp", "cannabis", "cannabidiol", "hanf",
        ],
        "output_suffix": "cbd",
    },
    "pet": {
        "label": "Pet Supplies / Pet Food",
        "keyword_tags": [
            "pet food", "pet supplies", "pet care", "dog food",
            "cat food", "tiernahrung", "tierfutter", "heimtierbedarf",
        ],
        "output_suffix": "pet",
    },
    "wellness": {
        "label": "Wellness / Health",
        "keyword_tags": [
            "wellness", "health", "holistic health", "natural health",
            "ayurveda", "herbal", "bio", "organic",
        ],
        "output_suffix": "wellness",
    },
}

# DACH location strings Apollo understands
DACH_LOCATIONS = ["Germany", "Austria", "Switzerland"]

# Employee range: small DTC brands (1–200)
EMPLOYEE_RANGES = ["1,10", "11,50", "51,200"]

# E-commerce platform UIDs in Apollo (active by default)
ECOMMERCE_PLATFORMS = ["shopify", "woocommerce", "shopware", "magento", "bigcommerce", "prestashop"]


# ── Dedup helpers ─────────────────────────────────────────────────────────────

def extract_domain(url: str) -> str | None:
    """Normalize URL to bare domain without www."""
    try:
        parsed = urlparse(url if url.startswith("http") else f"https://{url}")
        domain = parsed.netloc.lower().removeprefix("www.")
        return domain if domain else None
    except Exception:
        return None


def load_known_domains() -> set[str]:
    """Load all previously seen domains from txt and json result files."""
    known: set[str] = set()

    txt_files = [
        "leads/discovered-urls.txt",
        "leads/urls.txt",
    ] + list(Path("leads").glob("apollo-domains-*.txt"))

    for path_str in txt_files:
        p = Path(path_str)
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                d = extract_domain(line)
                if d:
                    known.add(d)

    json_files = list(Path("leads").glob("batch-results*.json"))
    for p in json_files:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            # Support both list-of-objects and {"results": [...]}
            items = data if isinstance(data, list) else data.get("results", [])
            for item in items:
                url = item.get("url") or item.get("website") or ""
                d = extract_domain(url)
                if d:
                    known.add(d)
        except Exception:
            pass

    return known


# ── Apollo API ─────────────────────────────────────────────────────────────────

def build_payload(
    keyword_tags: list[str],
    page: int,
    per_page: int,
    all_tech: bool,
    shopify_only: bool = False,
) -> dict:
    payload: dict = {
        "q_organization_keyword_tags": keyword_tags,
        "organization_locations": DACH_LOCATIONS,
        "organization_num_employees_ranges": EMPLOYEE_RANGES,
        "page": page,
        "per_page": per_page,
    }
    if not all_tech:
        payload["currently_using_any_of_technology_uids"] = ["shopify"] if shopify_only else ECOMMERCE_PLATFORMS
    return payload


def fetch_page(api_key: str, payload: dict, page_num: int) -> tuple[list[dict], int]:
    """
    Returns (organizations, total_entries).
    Raises on non-200 or missing data.
    """
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "X-Api-Key": api_key,
    }
    response = requests.post(
        APOLLO_ORGS_ENDPOINT,
        headers=headers,
        json=payload,
        timeout=30,
    )

    if response.status_code == 401:
        print("ERROR: Apollo API key ungueltig oder abgelaufen (401).")
        sys.exit(1)
    if response.status_code == 429:
        print(f"  WARN: Rate limit erreicht auf Seite {page_num} — warte 10s...")
        time.sleep(10)
        return fetch_page(api_key, payload, page_num)  # one retry
    if response.status_code != 200:
        print(f"  ERROR: HTTP {response.status_code} — {response.text[:200]}")
        return [], 0

    data = response.json()
    organizations = data.get("organizations", [])
    total = data.get("pagination", {}).get("total_entries", 0)
    return organizations, total


def discover(
    api_key: str,
    niche_cfg: dict,
    num_pages: int,
    per_page: int,
    all_tech: bool,
    known_domains: set[str],
    shopify_only: bool = False,
) -> tuple[list[str], list[dict]]:
    """
    Fetches `num_pages` pages from Apollo.
    Returns (new_domains, raw_orgs).
    """
    new_domains: list[str] = []
    raw_orgs: list[dict] = []
    seen_this_run: set[str] = set()
    total_entries = None

    print(f"\nNische: {niche_cfg['label']}")
    if all_tech:
        print(f"Filter: DACH | 1-200 MA | alle Tech-Stacks")
    elif shopify_only:
        print(f"Filter: DACH | 1-200 MA | nur Shopify")
    else:
        print(f"Filter: DACH | 1-200 MA | E-Commerce (Shopify/WooCommerce/Shopware/Magento/BigCommerce/PrestaShop)")

    for page in range(1, num_pages + 1):
        payload = build_payload(niche_cfg["keyword_tags"], page, per_page, all_tech, shopify_only)
        print(f"\n  Seite {page}/{num_pages} abrufen...")

        orgs, total = fetch_page(api_key, payload, page)

        if total_entries is None and total:
            total_entries = total
            print(f"  >> Gesamt verfuegbar: {total_entries} Unternehmen")

        if not orgs:
            print("  >> Keine Ergebnisse (Ende der Daten).")
            break

        page_new = 0
        for org in orgs:
            # Collect raw data for every org regardless of dedup
            raw_orgs.append({
                "name": org.get("name"),
                "website_url": org.get("website_url"),
                "primary_domain": org.get("primary_domain"),
                "estimated_num_employees": org.get("estimated_num_employees"),
                "annual_revenue_printed": org.get("annual_revenue_printed"),
                "technology_names": org.get("technology_names"),
                "phone": org.get("phone"),
                "primary_phone": org.get("primary_phone"),
            })

            # Apollo returns website_url or primary_domain
            raw_url = org.get("website_url") or org.get("primary_domain") or ""
            if not raw_url:
                continue
            domain = extract_domain(raw_url)
            if not domain:
                continue
            if domain in known_domains or domain in seen_this_run:
                continue
            seen_this_run.add(domain)
            new_domains.append(f"https://{domain}")
            page_new += 1

        print(f"  >> {len(orgs)} Ergebnisse | {page_new} neue Domains")

        if page < num_pages:
            time.sleep(DELAY_BETWEEN_PAGES)

    return new_domains, raw_orgs


# ── Output ────────────────────────────────────────────────────────────────────

def save_output(domains: list[str], niche_suffix: str) -> str:
    today = date.today().isoformat()
    output_path = Path(f"leads/apollo-domains-{niche_suffix}-{today}.txt")
    output_path.parent.mkdir(exist_ok=True)

    lines = [
        f"# GetKiAgent — Apollo Discovery: {niche_suffix} ({today})",
        f"# {len(domains)} neue Domains",
        "",
    ] + sorted(domains)

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return str(output_path)


def save_raw(raw_orgs: list[dict], niche_suffix: str) -> str:
    today = date.today().isoformat()
    raw_path = Path(f"leads/apollo-raw-{niche_suffix}-{today}.json")
    raw_path.parent.mkdir(exist_ok=True)
    raw_path.write_text(json.dumps(raw_orgs, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(raw_path)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Apollo Lead Discovery fuer GetKiAgent")
    parser.add_argument(
        "--niche",
        required=True,
        choices=list(NICHE_CONFIGS.keys()),
        help=f"Nische: {', '.join(NICHE_CONFIGS.keys())}",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=2,
        help="Anzahl Apollo-Seiten (Standard: 2 = max. 200 Ergebnisse bei per-page=100)",
    )
    parser.add_argument(
        "--per-page",
        type=int,
        default=100,
        help="Ergebnisse pro Seite (max. 100, Standard: 100)",
    )
    parser.add_argument(
        "--all-tech",
        action="store_true",
        help="Alle Tech-Stacks einschliessen (Standard: nur E-Commerce-Plattformen)",
    )
    parser.add_argument(
        "--shopify-only",
        action="store_true",
        help="Nur Shopify-Brands (strenger DTC-Filter, kleineres Volumen)",
    )
    args = parser.parse_args()

    # Validate
    api_key = os.getenv("APOLLO_API_KEY")
    if not api_key:
        print("ERROR: APOLLO_API_KEY nicht gesetzt. Abbruch.")
        sys.exit(1)

    per_page = min(args.per_page, 100)
    niche_cfg = NICHE_CONFIGS[args.niche]

    print(f"\n{'=' * 55}")
    print(f"  GetKiAgent — Apollo Discovery")
    print(f"{'=' * 55}")

    # Load known domains for dedup
    known = load_known_domains()
    print(f"  Bekannte Domains (alle Quellen): {len(known)}")

    # Discover
    new_domains, raw_orgs = discover(
        api_key=api_key,
        niche_cfg=niche_cfg,
        num_pages=args.pages,
        per_page=per_page,
        all_tech=args.all_tech,
        known_domains=known,
        shopify_only=args.shopify_only,
    )

    # Save raw Apollo data
    if raw_orgs:
        raw_path = save_raw(raw_orgs, niche_cfg["output_suffix"])
        print(f"  Apollo-Rohdaten gespeichert: {raw_path} ({len(raw_orgs)} Orgs)")

    if not new_domains:
        print("\nKeine neuen Domains gefunden. Fertig.")
        return

    # Save
    output_path = save_output(new_domains, niche_cfg["output_suffix"])

    print(f"\n{'=' * 55}")
    print(f"  {len(new_domains)} neue Domains gespeichert: {output_path}")
    print(f"{'=' * 55}")
    print("\nNaechster Schritt:")
    print(f"  python scripts/batch_analyze.py {output_path}")


if __name__ == "__main__":
    main()
