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
import os
import tempfile
import time
from contextlib import contextmanager
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
    # ── Beauty / Kosmetik DTC ─────────────────────────────────────────────────
    ("Beauty Brand Eigenmarke Deutschland online kaufen", "de-de"),
    ("Kosmetik Eigenmarke DTC direct-to-consumer Shop", "de-de"),
    ("Lippenstift Lipgloss Eigenmarke Shop Deutschland", "de-de"),
    ("Foundation Concealer Eigenmarke online kaufen", "de-de"),
    ("Parfum Eigenmarke Online Shop Deutschland", "de-de"),
    ("Körperpflege Eigenmarke DTC nachhaltiger Shop", "de-de"),
    ("Make-up Eigenmarke vegan cruelty-free online kaufen", "de-de"),
    ("Beauty Startup gegründet Eigenmarke Shop Deutschland", "de-de"),
    ("Haarpflege Eigenmarke Shop Österreich", "at-de"),
    ("Beauty Kosmetik Eigenmarke Schweiz DTC shop", "ch-de"),
    # ── Supplements DACH — Long-Tail / Nische ────────────────────────────────
    ("Magnesium Bisglycinat Kapseln Eigenmarke kaufen", "de-de"),
    ("Omega 3 Algenöl vegan Abo bestellen Deutschland", "de-de"),
    ("Kollagen Peptide Trinkampullen Eigenmarke Shop", "de-de"),
    ("Pre Workout Booster vegan Eigenmarke online kaufen", "de-de"),
    ("Nootropika Fokus Kapseln Shop Deutschland", "de-de"),
    ("Probiotika Darmflora Kapseln Eigenmarke kaufen", "de-de"),
    ("Vitamin D3 K2 Tropfen hochdosiert online Shop", "de-de"),
    ("Startup Nahrungsergänzung gegründet Deutschland Eigenmarke", "de-de"),
    ("Bio Superfood Pulver Adaptogen Shop versandkostenfrei", "de-de"),
    ("Nahrungsergänzung Abo Box Deutschland bestellen", "de-de"),
    # ── Supplements AT ────────────────────────────────────────────────────────
    ("Vitamine Mineralstoffe Eigenmarke Abo site:.at", "at-de"),
    ("Bio Supplements Kapseln online Shop Österreich site:.at", "at-de"),
    # ── Supplements CH ────────────────────────────────────────────────────────
    ("Nahrungsergänzungsmittel Eigenmarke Schweiz Abo site:.ch", "ch-de"),
    # ── Pet Care DTC — Long-Tail / Nische ────────────────────────────────────
    ("Bio Hundefutter Abo Eigenmarke kaufen", "de-de"),
    ("Insektenprotein Hundefutter nachhaltig Shop Deutschland", "de-de"),
    ("getreidefreies Katzenfutter Eigenmarke Abo bestellen", "de-de"),
    ("kaltgepresstes Hundefutter direkt Hersteller kaufen", "de-de"),
    ("Nassfutter Katze hoher Fleischanteil Eigenmarke Shop", "de-de"),
    ("BARF Rohfutter Hund Eigenmarke online kaufen", "de-de"),
    ("Nahrungsergänzung Hund Gelenke Lachsöl Shop", "de-de"),
    ("Höhle der Löwen Hundefutter Startup", "de-de"),
    ("Startup Pet Food gegründet Deutschland Eigenmarke", "de-de"),
    ("Bio Hundesnacks getreidefrei Abo versandkostenfrei", "de-de"),
    # ── Pet Care AT ───────────────────────────────────────────────────────────
    ("Premium Hundefutter Eigenmarke online kaufen site:.at", "at-de"),
    ("Bio Katzenfutter Abo Österreich site:.at", "at-de"),
    # ── Pet Care CH ───────────────────────────────────────────────────────────
    ("Hundefutter Eigenmarke Schweiz DTC site:.ch", "ch-de"),
    # ── Vegan Food DTC — Long-Tail / Nische ──────────────────────────────────
    ("vegane Fleischalternative Eigenmarke online kaufen", "de-de"),
    ("pflanzliche Milchalternative Haferdrink Eigenmarke Shop", "de-de"),
    ("vegane Fertiggerichte Abo bestellen Deutschland", "de-de"),
    ("Bio veganer Käse Eigenmarke online kaufen", "de-de"),
    ("plant based Protein Riegel DTC Shop Deutschland", "de-de"),
    ("vegane Bio Snacks Abo versandkostenfrei Deutschland", "de-de"),
    ("Tempeh Tofu Eigenmarke Hersteller direkt kaufen", "de-de"),
    ("Höhle der Löwen vegan Food Startup", "de-de"),
    ("Startup vegane Lebensmittel gegründet Deutschland", "de-de"),
    ("vegane Schokolade Manufaktur Eigenmarke online kaufen", "de-de"),
    # ── Vegan Food AT ─────────────────────────────────────────────────────────
    ("vegane Lebensmittel Eigenmarke Abo site:.at", "at-de"),
    ("Bio vegan Shop Österreich versandkostenfrei site:.at", "at-de"),
    # ── Vegan Food CH ─────────────────────────────────────────────────────────
    ("vegane Produkte Eigenmarke Schweiz online site:.ch", "ch-de"),
    # ── Mens Grooming — Long-Tail / Nische ───────────────────────────────────
    ("Bartöl Bartpflege Eigenmarke online kaufen", "de-de"),
    ("Herren Pflegeset Rasur Abo bestellen Deutschland", "de-de"),
    ("Rasierhobel Rasierklingen Eigenmarke Shop Deutschland", "de-de"),
    ("Männer Gesichtspflege Serum Eigenmarke online kaufen", "de-de"),
    ("nachhaltiger Herren Duschgel Shampoo DTC Shop", "de-de"),
    ("Herrenparfum Manufaktur Eigenmarke direkt kaufen", "de-de"),
    ("Bartpflege Abo Box versandkostenfrei Deutschland", "de-de"),
    ("Höhle der Löwen Männerpflege Startup", "de-de"),
    ("Startup Herrenkosmetik gegründet Deutschland Eigenmarke", "de-de"),
    ("Naturkosmetik Männer vegan Eigenmarke Shop", "de-de"),
    # ── Mens Grooming AT ──────────────────────────────────────────────────────
    ("Herren Pflege Bartöl Eigenmarke site:.at", "at-de"),
    ("Männerkosmetik online Shop Österreich site:.at", "at-de"),
    # ── Mens Grooming CH ──────────────────────────────────────────────────────
    ("Männerpflege Eigenmarke Schweiz DTC site:.ch", "ch-de"),
    # ── Shopify / WooCommerce Store Signals ───────────────────────────────────
    ("Naturkosmetik Shop \"Powered by Shopify\" Deutschland", "de-de"),
    ("Beauty Kosmetik Eigenmarke Shopify Store DACH", "de-de"),
    ("Kosmetik WooCommerce Shop Eigenmarke Deutschland", "de-de"),
    ("Skincare Beauty Brand Shopify gegründet", "de-de"),
    ("Naturkosmetik beauty brand direct consumer shopify", "de-de"),
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
    # Supplements DACH — retailers & aggregators
    "fitnessking", "sportnahrung-engel", "sportnahrung24", "powerstar-food",
    "sanct-bernhard", "fatburnerking", "apodiscounter", "medikamente-per-klick",
    # Pet Care — retailers & marketplaces
    "fressnapf", "zooplus", "bitiba", "zooroyal", "das-futterhaus",
    "futterhaus", "kolle-zoo", "maxizoo", "tiierisch", "hundeland",
    # Vegan Food — retailers & aggregators
    "alles-vegetarisch", "vantastic-foods", "veganversand", "vekoop",
    "kokku-online", "reformhaus-shop",
    # Mens Grooming — retailers & big brands
    "gillette", "wilkinson", "braun-shop", "mankind", "mrporter", "hairshop24",
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
    # Blocklist prüfen: Einträge mit "." matchen exakt auf Domain,
    # sonst gegen Host-Labels + Hyphen-Splits. Verhindert False Positives
    # wie "hm" in "meritbeauty.com" oder "dm" in "dmlab.de".
    exact_blocks = {b for b in DOMAIN_BLOCKLIST if "." in b}
    if domain in exact_blocks:
        return False
    registrable = domain.split(".", 1)[0]
    tokens = {registrable, *registrable.split("-")}
    if tokens & (DOMAIN_BLOCKLIST - exact_blocks):
        return False
    # TLD prüfen
    return any(domain.endswith(tld) for tld in ALLOWED_TLDS)


def extract_domain(url: str) -> str | None:
    try:
        parsed = urlparse(url if url.startswith("http") else "https://" + url)
        domain = parsed.netloc.lower().removeprefix("www.")
        return domain if domain else None
    except (ValueError, AttributeError):
        return None


# ── Discovery ─────────────────────────────────────────────────────────────────

class SearchError(RuntimeError):
    """DDG-Suche ist hart fehlgeschlagen (kein Rate-Limit) — Run als fehlerhaft markieren."""


def search_ddg(query: str, region: str, max_results: int) -> list[str]:
    """DDG search with PLAN.md rate-limit handling: 30s wait + retry once.

    Leere Result-Liste = wirklich 0 Treffer.
    SearchError = Netzwerk-/API-Fehler — Caller entscheidet, ob Run weiter läuft oder abbricht.
    """
    try:
        from ddgs import DDGS
    except ImportError:
        print("ERROR: ddgs nicht installiert. Run: pip install ddgs")
        sys.exit(1)

    last_error: Exception | None = None
    for attempt in range(2):
        try:
            results = DDGS().text(query, region=region, max_results=max_results)
            return [r.get("href", "") for r in results if r.get("href")]
        except Exception as e:
            last_error = e
            msg = str(e).lower()
            is_rate_limit = any(s in msg for s in ("ratelimit", "rate limit", "429", "202", "too many"))
            if is_rate_limit and attempt == 0:
                print(f"  Rate-Limit — warte 30s und versuche erneut...")
                time.sleep(30)
                continue
            # Rate-Limit nach Retry oder anderer harter Fehler → propagieren
            raise SearchError(f"DDG-Suche fehlgeschlagen: {e}") from e
    raise SearchError(f"DDG-Suche fehlgeschlagen: {last_error}") from last_error


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
            except (json.JSONDecodeError, OSError) as e:
                print(f"  WARN: {p.name} nicht lesbar: {e}")
    return known


def _detect_region(query: str) -> str:
    """Detect DDG region from query string: site:.at → at-de, site:.ch → ch-de, else de-de."""
    if "site:.at" in query:
        return "at-de"
    if "site:.ch" in query:
        return "ch-de"
    return "de-de"


def discover(num_queries: int, results_per_query: int, niche_queries: list[str] | None = None, leads_dir: str = "leads") -> list[str]:
    if niche_queries is not None:
        # Config-driven: list of query strings, region auto-detected
        queries = [(q, _detect_region(q)) for q in niche_queries[:num_queries]]
    else:
        # Legacy: hardcoded SEARCH_QUERIES tuples
        queries = SEARCH_QUERIES[:min(num_queries, len(SEARCH_QUERIES))]

    existing = load_existing_urls([
        f"{leads_dir}/urls.txt",
        f"{leads_dir}/batch-results.json",
        f"{leads_dir}/discovered-urls.txt",
        "leads/urls.txt",
        "leads/batch-results.json",
        "leads/discovered-urls.txt",
    ])
    print(f"  Bereits bekannte Domains: {len(existing)}")

    found_domains: dict[str, str] = {}  # domain -> full url
    failed_queries = 0

    for i, (query, region) in enumerate(queries, 1):
        print(f"\n  [{i}/{len(queries)}] {query}")
        try:
            urls = search_ddg(query, region, results_per_query)
        except SearchError as e:
            failed_queries += 1
            print(f"           FEHLER: {e}")
            time.sleep(1)
            continue
        new = 0
        for url in urls:
            domain = extract_domain(url)
            if not domain:
                continue
            if domain in existing or domain in found_domains:
                continue
            if not is_relevant_domain(domain):
                continue
            found_domains[domain] = f"https://{domain}"
            new += 1
        print(f"           {new} neue Kandidaten")
        time.sleep(1)  # Rate-limit respektieren

    # Wenn alle Queries fehlgeschlagen sind: Run ist nicht vertrauenswürdig
    if queries and failed_queries == len(queries):
        raise SearchError(
            f"Alle {failed_queries} Queries fehlgeschlagen — DDG unerreichbar oder blockiert."
        )
    if failed_queries:
        print(f"\n  WARN: {failed_queries}/{len(queries)} Queries fehlgeschlagen")

    return list(found_domains.values())


# ── Output ────────────────────────────────────────────────────────────────────

def save_discovered(urls: list[str], output_path: str):
    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# GetKiAgent — Discovered Leads (automatisch generiert)", ""]
    lines += [url for url in sorted(urls)]
    # Atomic write: erst tmp, dann rename — verhindert halb-geschriebene Dateien
    fd, tmp_name = tempfile.mkstemp(prefix=p.name + ".", suffix=".tmp", dir=p.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        os.replace(tmp_name, p)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


@contextmanager
def run_lock(leads_dir: str):
    """Lockfile-Guard: verhindert, dass zwei Discovery-Runs parallel dieselbe Niche bearbeiten.

    Race ohne Lock: beide Runs lesen denselben Cache, finden dieselben Domains,
    überschreiben discovered-urls.txt und syncen Duplikate ans Sheet.
    """
    lock_dir = Path(leads_dir)
    lock_dir.mkdir(parents=True, exist_ok=True)
    lock_path = lock_dir / ".discover.lock"
    try:
        fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise RuntimeError(
            f"Discovery-Run läuft bereits ({lock_path}). "
            f"Falls das ein Überbleibsel ist, Datei manuell löschen."
        )
    try:
        with os.fdopen(fd, "w") as f:
            f.write(f"pid={os.getpid()} started={int(time.time())}\n")
        yield
    finally:
        try:
            lock_path.unlink()
        except OSError:
            pass


# ── Main ──────────────────────────────────────────────────────────────────────

def _sync_urls_to_sheet(urls: list[str]):
    """Trägt neue URLs mit leerem Status ins Sheet ein (Lead URL Scorer holt sie ab)."""
    import os
    import requests as req
    webhook_url = os.getenv("N8N_DISCOVERY_WEBHOOK")
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


def _positive_int(raw: str) -> int:
    try:
        n = int(raw)
    except ValueError:
        raise argparse.ArgumentTypeError(f"muss eine Ganzzahl sein, nicht {raw!r}")
    if n <= 0:
        raise argparse.ArgumentTypeError(f"muss > 0 sein, nicht {n}")
    return n


def main():
    from niche_config import load_niche_config

    parser = argparse.ArgumentParser()
    parser.add_argument("--queries", type=_positive_int, default=99, help="Anzahl Suchqueries (Standard: alle)")
    parser.add_argument("--results", type=_positive_int, default=15, help="Ergebnisse pro Query")
    parser.add_argument("--output", default=None, help="Output path (auto-set when --niche used)")
    parser.add_argument("--niche", default=None, help="Niche name — loads queries from configs/{niche}.yaml")
    args = parser.parse_args()

    config = load_niche_config(args.niche)
    niche_queries = None
    leads_dir = "leads"

    if config:
        niche_queries = config.get("discovery", {}).get("ddg_queries", [])
        if not niche_queries:
            print(f"ERROR: Keine ddg_queries in configs/{args.niche}.yaml gefunden")
            sys.exit(1)
        leads_dir = f"leads/{args.niche}"
        total_queries = len(niche_queries)
        print(f"\nNiche-Modus: {args.niche} ({total_queries} Queries in Config)")
    else:
        total_queries = len(SEARCH_QUERIES)

    output = args.output or f"{leads_dir}/discovered-urls.txt"
    num_queries = min(args.queries, total_queries)

    print(f"\nLead Discovery gestartet ({num_queries} von {total_queries} Queries)")
    print(f"  {num_queries} Queries x {args.results} Ergebnisse = max. {num_queries * args.results} URLs\n")

    try:
        with run_lock(leads_dir):
            urls = discover(num_queries, args.results, niche_queries=niche_queries, leads_dir=leads_dir)

            if not urls:
                print("\nKeine neuen Kandidaten gefunden.")
                return

            save_discovered(urls, output)
            _sync_urls_to_sheet(urls)
    except SearchError as e:
        print(f"\nERROR: {e}")
        sys.exit(2)
    except RuntimeError as e:
        print(f"\nERROR: {e}")
        sys.exit(3)

    print(f"\n{'=' * 50}")
    print(f"  {len(urls)} neue Domains gefunden")
    print(f"  Gespeichert in: {output}")
    print(f"{'=' * 50}")
    print("\nNaechster Schritt:")
    print(f"  python scripts/batch_analyze.py {output}" + (f" --niche {args.niche}" if args.niche else ""))


if __name__ == "__main__":
    main()
