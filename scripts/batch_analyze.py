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
from utils import normalize_url
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


def analyze_one(url: str, firecrawl_key: str, anthropic_key: str,
                cache_dir: Path | None = None, extra_suffix: str = "") -> dict:
    """Gibt ein Result-Objekt zurück — auch bei Fehler. Bei Timeout: 1 Retry."""
    for attempt in range(2):
        try:
            pages = scrape_pages(url, firecrawl_key, cache_dir=cache_dir)
            result = analyze_with_claude(url, pages, anthropic_key,
                                         extra_system_suffix=extra_suffix)
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


def _classify_error(result: dict) -> str:
    """
    Klassifiziert einen Fehler in: timeout / parse_error / api_error / soft_404 / other.
    Basis: error_detail.category + Schlüsselwörter in der Message.
    """
    detail = result.get("error_detail", {}) or {}
    category = detail.get("category", "")
    message = (detail.get("message", "") or "").lower()

    if category == "firecrawl_timeout":
        return "timeout"
    if category == "claude_parse_error":
        return "parse_error"
    if category == "claude_api_error":
        return "api_error"
    if category == "firecrawl_error":
        # Soft-404: Seite antwortet, aber kein brauchbarer Content
        if any(kw in message for kw in ("404", "not found", "no content", "empty", "blocked")):
            return "soft_404"
        return "soft_404"
    return "other"


def _persist(results: list[dict], output_path: Path, run_at: str):
    output_path.write_text(
        json.dumps({"run_at": run_at, "total": len(results), "results": results}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def heal_errors(results: list[dict], firecrawl_key: str, anthropic_key: str,
                output_path: Path, run_at: str,
                cache_dir: Path | None = None) -> list[dict]:
    """
    Scannt results nach status=="error", klassifiziert jeden Fehler und retried
    mit Exponential Backoff (5s, 15s). Bei parse_error wird der System-Prompt um
    einen strikten JSON-Zwang ergänzt. Schreibt results nach jedem Heilversuch zurück.
    """
    error_indices = [i for i, r in enumerate(results) if r.get("status") == "error"]
    if not error_indices:
        print("\nheal_errors: keine Fehler zu reparieren.")
        return results

    print("\n" + "=" * 66)
    print(f"  HEAL-PHASE — {len(error_indices)} Fehler gefunden")
    print("=" * 66)

    backoff_schedule = [5, 15]
    parse_suffix = "WICHTIG: Antworte ausschließlich im geforderten JSON-Format. Kein Fließtext, keine Kommentare, nur das JSON-Objekt."
    healed = 0

    for idx in error_indices:
        original = results[idx]
        url = original["url"]
        kind = _classify_error(original)
        print(f"\n[heal] {url}")
        print(f"  Kategorie: {kind}")

        success = False
        for attempt, wait_s in enumerate(backoff_schedule, 1):
            print(f"  Retry {attempt}/{len(backoff_schedule)} nach {wait_s}s...")
            time.sleep(wait_s)

            try:
                pages = scrape_pages(url, firecrawl_key, cache_dir=cache_dir)
                if kind == "parse_error":
                    data = analyze_with_claude(url, pages, anthropic_key, extra_system_suffix=parse_suffix)
                else:
                    data = analyze_with_claude(url, pages, anthropic_key)
                validate_result(data)
                results[idx] = {
                    "url": url, "status": "ok", "data": data,
                    "healed_from": kind, "heal_attempt": attempt,
                }
                healed += 1
                success = True
                print(f"  → OK (healed nach {attempt} Versuch)")
                break
            except Exception as e:
                err_msg = f"{type(e).__name__}: {str(e)[:120]}"
                print(f"  → Fehlgeschlagen: {err_msg}")
                if attempt == len(backoff_schedule):
                    results[idx] = {
                        **original,
                        "heal_attempts": len(backoff_schedule),
                        "heal_last_error": err_msg,
                    }

        _persist(results, output_path, run_at)
        if not success:
            print(f"  → endgültig fehlgeschlagen")

    print(f"\n  Healed: {healed}/{len(error_indices)}")
    print("=" * 66)
    return results


def _export_qualified(results: list[dict], output_path: Path):
    """Exports leads with score >= 7 to a separate file for direct handoff to Stage 4."""
    qualified = [
        r for r in results
        if r.get("status") == "ok" and r.get("data", {}).get("score_1_to_10", 0) >= 7
    ]
    if not qualified:
        print("  → Keine qualifizierten Leads (Score ≥7) in diesem Batch.")
        return
    qualified_path = output_path.parent / "qualified-leads.json"
    qualified_path.write_text(
        json.dumps(
            {"exported_at": datetime.now(timezone.utc).isoformat(), "total": len(qualified), "results": qualified},
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"  → {len(qualified)} qualifizierte Leads (Score ≥7) exportiert nach: {qualified_path}")


def _sync_to_sheet(results: list[dict], run_at: str):
    """Postet analysierte Leads an n8n Outreach Agent (Sync-Modus)."""
    import os
    import requests as req
    webhook_url = os.getenv("N8N_RESULTS_WEBHOOK")
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


def preflight_check(output_file: str, niche_config: dict | None = None):
    """
    Prüft alle Voraussetzungen bevor ein einziger Credit verbrannt wird.
    Bricht mit klarer Fehlermeldung ab wenn etwas fehlt.
    """
    import os
    errors = []

    # 1. Prompt-Datei
    prompt_path = Path("prompts/lead_analysis_v1.md")
    if not prompt_path.exists():
        errors.append(f"  FEHLT: {prompt_path}  (→ alle Claude-Analysen würden fehlschlagen)")

    # 2. API-Keys (FIRECRAWL_API_KEY optional — scraping via Jina/crawl4ai)
    if not os.getenv("ANTHROPIC_API_KEY"):
        errors.append("  FEHLT: ANTHROPIC_API_KEY  (→ keine Claude-Analyse möglich)")

    # 3. Output-Pfad schreibbar
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        test_file = output_path.parent / ".preflight_write_test"
        test_file.write_text("ok", encoding="utf-8")
        test_file.unlink()
    except Exception as e:
        errors.append(f"  NICHT SCHREIBBAR: {output_path.parent}  ({e})")

    # 4. Niche config validation
    if niche_config:
        scoring = niche_config.get("scoring", {})
        if not scoring.get("pain_signals"):
            errors.append("  WARNUNG: Keine pain_signals in Niche-Config")

    if errors:
        print("\n" + "=" * 66)
        print("  PREFLIGHT FEHLGESCHLAGEN — kein API-Call wird gemacht")
        print("=" * 66)
        for e in errors:
            print(e)
        print("=" * 66 + "\n")
        sys.exit(1)

    print(f"Preflight OK — prompt, keys, output-pfad ({output_path.parent}) bereit.")


def _build_niche_suffix(niche_config: dict) -> str:
    """Build extra system prompt suffix from niche config pain signals + disqualifiers."""
    scoring = niche_config.get("scoring", {})
    pain = scoring.get("pain_signals", [])
    disq = scoring.get("disqualifiers", [])
    thresholds = scoring.get("tier_thresholds", {})
    niche_name = niche_config.get("niche", {}).get("display_name", "")

    parts = []
    if niche_name:
        parts.append(f"\n\n## Nische: {niche_name}")
    if pain:
        parts.append("\n\nZusätzliche Pain Signals für diese Nische (erhöhen Score):")
        for s in pain:
            parts.append(f"- {s}")
    if disq:
        parts.append("\n\nZusätzliche Disqualifikatoren für diese Nische (senken Score):")
        for d in disq:
            parts.append(f"- {d}")
    if thresholds:
        a_min = thresholds.get("tier_a_min", 7)
        b_min = thresholds.get("tier_b_min", 4)
        parts.append(f"\n\nTier-Schwellen: A ab {a_min}, B ab {b_min}")

    return "\n".join(parts) if parts else ""


def main():
    import argparse
    from niche_config import load_niche_config

    parser = argparse.ArgumentParser(description="GetKiAgent Batch Lead Analyzer")
    parser.add_argument("url_file", nargs="?", default=None, help="Path to URL text file")
    parser.add_argument("--output", default=None, help="Output JSON path (auto-set with --niche)")
    parser.add_argument("--heal-only", action="store_true", help="Only retry errors in existing results")
    parser.add_argument("--niche", default=None, help="Niche name — loads config from configs/{niche}.yaml")
    args = parser.parse_args()

    if not args.heal_only and not args.url_file:
        print("Usage: python scripts/batch_analyze.py leads/urls.txt [--output ...] [--niche ...] [--heal-only]")
        sys.exit(1)

    # Load .env before preflight so os.getenv picks up keys from .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    niche_config = load_niche_config(args.niche)
    extra_suffix = _build_niche_suffix(niche_config) if niche_config else ""

    # Set paths based on niche
    if args.niche:
        leads_dir = f"leads/{args.niche}"
        output_file = args.output or f"{leads_dir}/batch-results.json"
        cache_dir = Path(f"{leads_dir}/scrape-cache")
        print(f"\nNiche-Modus: {args.niche}")
        if extra_suffix:
            print(f"  Pain Signals + Disqualifiers aus Config geladen")
    else:
        output_file = args.output or "leads/batch-results.json"
        cache_dir = Path("leads/scrape-cache")

    preflight_check(output_file, niche_config)
    firecrawl_key, anthropic_key = load_and_validate_env()
    cache_dir.mkdir(parents=True, exist_ok=True)

    # --heal-only: nur heal_errors() auf bestehender Results-Datei
    if args.heal_only:
        output_path = Path(output_file)
        if not output_path.exists():
            print(f"ERROR: --heal-only benötigt existierende Datei: {output_path}")
            sys.exit(1)
        payload = json.loads(output_path.read_text(encoding="utf-8"))
        results = payload.get("results", [])
        run_at = payload.get("run_at", datetime.now(timezone.utc).isoformat())
        print(f"\n--heal-only: {len(results)} Einträge aus {output_path} geladen")
        heal_errors(results, firecrawl_key, anthropic_key, output_path, run_at, cache_dir=cache_dir)
        print_batch_summary(results)
        print(f"\nAktualisierte Ergebnisse: {output_path}")
        _sync_to_sheet(results, run_at)
        _export_qualified(results, output_path)
        return

    url_file = args.url_file
    urls = load_urls(url_file)

    print(f"\n{len(urls)} URLs geladen aus {url_file}")
    urls = prefilter_urls(urls)

    if not urls:
        print("Alle URLs vom Vorfilter aussortiert — nichts zu analysieren.")
        sys.exit(0)

    print(f"Starte Batch-Analyse ({len(urls)} URLs)...\n")

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    run_at = datetime.now(timezone.utc).isoformat()

    results = []
    for i, url in enumerate(urls, 1):
        url = normalize_url(url)
        print(f"[{i}/{len(urls)}] {url}")
        result = analyze_one(url, firecrawl_key, anthropic_key, cache_dir=cache_dir,
                             extra_suffix=extra_suffix)
        results.append(result)

        # Zwischenspeichern nach jedem URL — Crash-sicher
        output_path.write_text(
            json.dumps({"run_at": run_at, "total": len(results), "results": results}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        if i < len(urls):
            time.sleep(DELAY_BETWEEN_URLS)

    # Automatische Heal-Phase am Ende jedes Batch-Runs
    heal_errors(results, firecrawl_key, anthropic_key, output_path, run_at, cache_dir=cache_dir)

    print_batch_summary(results)
    print(f"\nVollständige Ergebnisse gespeichert in: {output_path}")
    _sync_to_sheet(results, run_at)
    _export_qualified(results, output_path)


if __name__ == "__main__":
    main()
