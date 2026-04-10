"""
GetKiAgent — Batch Lead Analyzer v1

Liest URLs aus einer Textdatei und analysiert jede einzeln.

Usage:
    python scripts/batch_analyze.py leads/urls.txt

Output:
    leads/batch-results.json   — alle Ergebnisse als JSON-Array
    stdout                     — kompakte Zusammenfassung pro URL
"""

import sys
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

# Aus dem Single-URL-Skript importieren — keine Logik duplizieren
sys.path.insert(0, str(Path(__file__).parent))
from analyze_lead import (
    load_and_validate_env, scrape_pages, analyze_with_claude, validate_result,
    FirecrawlTimeoutError, FirecrawlError, ClaudeParseError,
)

DELAY_BETWEEN_URLS = 3  # Sekunden Pause zwischen Requests


def _base_domain(domain: str) -> str:
    """shop.example.de → example.de  (letzten 2 Parts, reicht für DACH-TLDs)"""
    parts = domain.split(".")
    return ".".join(parts[-2:]) if len(parts) >= 2 else domain


def prefilter_urls(urls: list[str]) -> list[str]:
    """
    Vorfilter VOR dem teuren Firecrawl-Scraping:
    1. Domain-Blacklist (Marktplätze, große Retailer) → sofort skip
    2. HTTP HEAD → nicht erreichbar oder Redirect auf fremde Domain → skip
    Gibt bereinigte URL-Liste zurück.
    """
    try:
        import requests as req
    except ImportError:
        print("WARNING: 'requests' nicht installiert — Vorfilter übersprungen (pip install requests)")
        return urls

    from discover_leads import DOMAIN_BLOCKLIST, extract_domain

    kept = []
    skipped = 0

    print(f"Vorfilter läuft ({len(urls)} URLs)...")

    for url in urls:
        domain = extract_domain(url) or ""

        # 1. Blacklist-Check
        if any(blocked in domain for blocked in DOMAIN_BLOCKLIST):
            print(f"  SKIP (blacklist)    : {url}")
            skipped += 1
            continue

        # 2. HEAD-Request
        try:
            resp = req.head(
                url, allow_redirects=True, timeout=6,
                headers={"User-Agent": "Mozilla/5.0 (compatible; GetKiAgent/1.0)"},
            )
            # Redirect auf andere Domain?
            final_domain = extract_domain(resp.url) or ""
            if _base_domain(domain) and _base_domain(final_domain) and \
                    _base_domain(domain) != _base_domain(final_domain):
                print(f"  SKIP (redirect→{_base_domain(final_domain)}): {url}")
                skipped += 1
                continue
            # HTTP-Fehler (405 = HEAD nicht erlaubt, aber Server lebt → behalten)
            if resp.status_code >= 400 and resp.status_code != 405:
                print(f"  SKIP (HTTP {resp.status_code})      : {url}")
                skipped += 1
                continue
        except req.exceptions.Timeout:
            print(f"  SKIP (HEAD timeout) : {url}")
            skipped += 1
            continue
        except Exception:
            print(f"  SKIP (nicht erreichbar): {url}")
            skipped += 1
            continue

        kept.append(url)

    print(f"  → {len(kept)} behalten, {skipped} übersprungen\n")
    return kept


def load_urls(path: str) -> list[str]:
    p = Path(path)
    if not p.exists():
        print(f"ERROR: Datei nicht gefunden: {path}")
        sys.exit(1)

    urls = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            if not line.startswith("http"):
                line = "https://" + line
            urls.append(line)

    if not urls:
        print(f"ERROR: Keine URLs in {path} gefunden.")
        sys.exit(1)

    return urls


def analyze_one(url: str, firecrawl_key: str, anthropic_key: str) -> dict:
    """Gibt ein Result-Objekt zurück — auch bei Fehler. Bei Timeout: 1 Retry."""
    for attempt in range(2):
        try:
            pages = scrape_pages(url, firecrawl_key)
            result = analyze_with_claude(url, pages, anthropic_key)
            validate_result(result)
            return {"url": url, "status": "ok", "data": result}
        except FirecrawlTimeoutError as e:
            if attempt == 0:
                print(f"  Timeout — 1 Retry in 10s...")
                time.sleep(10)
                continue
            return {
                "url": url, "status": "error",
                "error": "Firecrawl Timeout (nach Retry)",
                "error_detail": {"category": "firecrawl_timeout", "message": str(e)},
            }
        except FirecrawlError as e:
            return {
                "url": url, "status": "error",
                "error": "Firecrawl Fehler",
                "error_detail": {"category": "firecrawl_error", "message": str(e)},
            }
        except ClaudeParseError as e:
            return {
                "url": url, "status": "error",
                "error": "Claude Parse Fehler",
                "error_detail": {"category": "claude_parse_error", "message": str(e)},
            }
        except SystemExit:
            return {
                "url": url, "status": "error",
                "error": "Setup-Fehler",
                "error_detail": {"category": "setup_error", "message": "sys.exit — fehlendes Paket oder Config-Problem"},
            }
        except Exception as e:
            error_type = type(e).__name__
            if any(kw in error_type for kw in ("APIError", "RateLimitError", "AuthenticationError")):
                category = "claude_api_error"
            else:
                category = "unknown_error"
            return {
                "url": url, "status": "error",
                "error": str(e)[:80],
                "error_detail": {"category": category, "message": str(e)},
            }
    # Sollte nie erreicht werden
    return {"url": url, "status": "error", "error": "Unbekannter Fehler", "error_detail": {"category": "unknown_error", "message": ""}}


def _sync_to_sheet(results: list[dict], run_at: str):
    """Postet analysierte Leads an n8n Outreach Agent (Sync-Modus)."""
    import os
    import requests as req
    webhook_url = os.getenv("N8N_OUTREACH_WEBHOOK")
    if not webhook_url:
        return
    ok_count = sum(1 for r in results if r.get("status") == "ok")
    try:
        resp = req.post(
            webhook_url,
            json={"sync": True, "results": results, "run_at": run_at},
            timeout=30,
        )
        if resp.status_code == 200:
            print(f"  → Sheet sync OK: {ok_count} Leads eingetragen")
        else:
            print(f"  → Sheet sync WARN: HTTP {resp.status_code}")
    except Exception as e:
        print(f"  → Sheet sync FEHLER: {e}")


def print_batch_summary(results: list[dict]):
    print("\n" + "=" * 66)
    print("  BATCH-ERGEBNIS")
    print("=" * 66)
    print(f"  {'URL':<35} {'Score':>6}  {'Tier':>5}  {'Status'}")
    print("  " + "-" * 62)

    for r in results:
        url = r["url"].replace("https://", "").replace("http://", "")[:34]
        if r["status"] == "ok":
            d = r["data"]
            score = d.get("score_1_to_10", "?")
            tier = d.get("tier", "?")
            company = d.get("company_name", "")[:20]
            print(f"  {url:<35} {score:>6}  {tier:>5}  {company}")
        else:
            detail = r.get("error_detail", {})
            category = detail.get("category", "")
            tag = f"[{category}] " if category else ""
            print(f"  {url:<35} {'—':>6}  {'—':>5}  FEHLER: {tag}{r['error']}"[:100])

    ok = [r for r in results if r["status"] == "ok"]
    tier_a = [r for r in ok if r["data"].get("tier") == "A"]
    tier_b = [r for r in ok if r["data"].get("tier") == "B"]
    tier_c = [r for r in ok if r["data"].get("tier") == "C"]
    errors = [r for r in results if r["status"] == "error"]

    print("  " + "-" * 62)
    print(f"  Gesamt: {len(results)}  |  Tier A: {len(tier_a)}  |  Tier B: {len(tier_b)}  |  Tier C: {len(tier_c)}  |  Fehler: {len(errors)}")
    print("=" * 66)


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/batch_analyze.py leads/urls.txt [--output leads/batch-results-wave2.json]")
        sys.exit(1)

    url_file = sys.argv[1]
    output_file = "leads/batch-results.json"
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]

    firecrawl_key, anthropic_key = load_and_validate_env()
    urls = load_urls(url_file)

    print(f"\n{len(urls)} URLs geladen aus {url_file}")
    urls = prefilter_urls(urls)

    if not urls:
        print("Alle URLs vom Vorfilter aussortiert — nichts zu analysieren.")
        sys.exit(0)

    print(f"Starte Batch-Analyse ({len(urls)} URLs)...\n")

    output_path = Path(output_file)
    output_path.parent.mkdir(exist_ok=True)
    run_at = datetime.now(timezone.utc).isoformat()

    results = []
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] {url}")
        result = analyze_one(url, firecrawl_key, anthropic_key)
        results.append(result)

        # Zwischenspeichern nach jedem URL — Crash-sicher
        output_path.write_text(
            json.dumps({"run_at": run_at, "total": len(results), "results": results}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        if i < len(urls):
            time.sleep(DELAY_BETWEEN_URLS)

    print_batch_summary(results)
    print(f"\nVollständige Ergebnisse gespeichert in: {output_path}")
    _sync_to_sheet(results, run_at)


if __name__ == "__main__":
    main()
