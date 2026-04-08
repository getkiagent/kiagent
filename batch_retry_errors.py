"""
GetKiAgent — Batch Retry: nur fehlgeschlagene URLs erneut analysieren.

Liest leads/batch-results.json, filtert status=="error", analysiert diese
URLs neu und ersetzt die Error-Einträge in-place.

Usage:
    python scripts/batch_retry_errors.py
"""

import sys
import json
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from batch_analyze import analyze_one, prefilter_urls, print_batch_summary, DELAY_BETWEEN_URLS
from analyze_lead import load_and_validate_env

RESULTS_PATH = Path("leads/batch-results.json")


def main():
    if not RESULTS_PATH.exists():
        print(f"ERROR: {RESULTS_PATH} nicht gefunden.")
        sys.exit(1)

    data = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    results = data["results"]

    error_indices = [i for i, r in enumerate(results) if r["status"] == "error"]
    error_urls = [results[i]["url"] for i in error_indices]

    if not error_indices:
        print("Keine Fehler-Einträge gefunden — nichts zu tun.")
        sys.exit(0)

    print(f"{len(error_urls)} fehlgeschlagene URLs gefunden:")
    for url in error_urls:
        print(f"  - {url}")

    firecrawl_key, anthropic_key = load_and_validate_env()

    # Vorfilter (HEAD-Check etc.)
    urls_to_retry = prefilter_urls(error_urls)

    if not urls_to_retry:
        print("Alle URLs vom Vorfilter aussortiert — nichts zu analysieren.")
        sys.exit(0)

    # URLs die vom Vorfilter entfernt wurden: Error-Eintrag bleibt bestehen
    urls_to_retry_set = set(urls_to_retry)

    print(f"\nStarte Retry ({len(urls_to_retry)} URLs)...\n")

    retry_results = []
    for i, url in enumerate(urls_to_retry, 1):
        print(f"[{i}/{len(urls_to_retry)}] {url}")
        result = analyze_one(url, firecrawl_key, anthropic_key)
        retry_results.append(result)

        if i < len(urls_to_retry):
            time.sleep(DELAY_BETWEEN_URLS)

    # Ergebnisse in-place ersetzen
    retry_map = {r["url"]: r for r in retry_results}
    replaced = 0
    for idx in error_indices:
        url = results[idx]["url"]
        if url in retry_map:
            results[idx] = retry_map[url]
            replaced += 1

    data["retry_at"] = datetime.now(timezone.utc).isoformat()
    RESULTS_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    print_batch_summary(retry_results)

    ok_count = sum(1 for r in retry_results if r["status"] == "ok")
    err_count = sum(1 for r in retry_results if r["status"] == "error")
    print(f"\n{replaced} Einträge ersetzt in {RESULTS_PATH}")
    print(f"  Neu OK: {ok_count}  |  Weiterhin Fehler: {err_count}")


if __name__ == "__main__":
    main()
