#!/usr/bin/env python3
"""
GetKiAgent Contact Enrichment — Apollo People Search

Liest eine batch-results.json, wählt Top-N qualifizierte Leads (Tier A+B, score >= 4),
sucht pro Domain einen Named Contact via Apollo mixed_people/search und schreibt
eine angereicherte JSON-Datei.

Usage:
    python scripts/enrich_contacts.py leads/batch-results.json
    python scripts/enrich_contacts.py leads/batch-results.json --output leads/beauty/qualified-top50-enriched.json --limit 50
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

APOLLO_API_BASE = "https://api.apollo.io/api/v1"
APOLLO_PEOPLE_ENDPOINT = f"{APOLLO_API_BASE}/mixed_people/api_search"
DELAY_BETWEEN_CALLS = 1.5

# Titles ranked by priority — Apollo returns matches, we pick first hit.
PERSON_TITLES = [
    "CEO", "Founder", "Co-Founder", "Gründer", "Geschäftsführer",
    "Managing Director", "Owner", "Inhaber",
    "Head of Customer Experience", "Head of Customer Service",
    "Head of E-Commerce", "E-Commerce Manager", "Head of Operations",
    "Kundenservice Leitung", "Customer Support Manager",
]

MIN_SCORE = 4  # Tier A (>=7) + Tier B (4-6)


def domain_from_url(url: str) -> str:
    if not url:
        return ""
    parsed = urlparse(url if "://" in url else f"https://{url}")
    host = parsed.netloc or parsed.path
    return host.lower().lstrip("www.").split("/")[0]


def load_qualified(batch_file: Path, limit: int) -> list[dict]:
    """Read batch-results, filter tier A+B, sort desc by score, cut to limit.

    Returns batch-compatible records: {"url", "status": "ok", "data": {...}, "domain"}.
    """
    with open(batch_file, encoding="utf-8") as f:
        data = json.load(f)
    results = data.get("results", [])
    qualified = []
    for r in results:
        if r.get("status") != "ok":
            continue
        d = r.get("data") or {}
        score = d.get("score_1_to_10")
        if not isinstance(score, (int, float)) or score < MIN_SCORE:
            continue
        qualified.append({
            "url": r.get("url", ""),
            "status": "ok",
            "domain": domain_from_url(r.get("url", "")),
            "data": d,
        })
    qualified.sort(key=lambda x: x["data"].get("score_1_to_10", 0), reverse=True)
    return qualified[:limit]


def search_person(api_key: str, domain: str) -> dict | None:
    """Call Apollo mixed_people/search for one domain. Return best match or None."""
    payload = {
        "q_organization_domains_list": [domain],
        "person_titles": PERSON_TITLES,
        "page": 1,
        "per_page": 5,
    }
    headers = {
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
        "accept": "application/json",
        "X-Api-Key": api_key,
    }
    try:
        r = requests.post(APOLLO_PEOPLE_ENDPOINT, json=payload, headers=headers, timeout=30)
    except requests.RequestException as exc:
        print(f"    ERROR: {exc}")
        return None
    if r.status_code != 200:
        print(f"    Apollo HTTP {r.status_code}: {r.text[:120]}")
        return None
    body = r.json()
    people = body.get("people") or body.get("contacts") or []
    if not people:
        return None
    # Prefer match whose title contains an early PERSON_TITLES entry.
    def rank(person: dict) -> int:
        title = (person.get("title") or "").lower()
        for i, t in enumerate(PERSON_TITLES):
            if t.lower() in title:
                return i
        return 999
    people.sort(key=rank)
    return people[0]


def enrich(lead: dict, person: dict | None) -> dict:
    d = lead.setdefault("data", {})
    if not person:
        d["enriched_contact"] = {"contact_source": "generic"}
        return lead
    d["enriched_contact"] = {
        "contact_source": "apollo",
        "first_name": person.get("first_name", ""),
        "last_name": person.get("last_name", ""),
        "title": person.get("title", ""),
        "linkedin_url": person.get("linkedin_url", ""),
        "apollo_email": person.get("email") or "",
    }
    return lead


def main() -> int:
    parser = argparse.ArgumentParser(description="Enrich qualified leads with Apollo people data")
    parser.add_argument("batch_file", help="Path to batch-results.json")
    parser.add_argument("--output", default="leads/beauty/qualified-top50-enriched.json")
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()

    api_key = os.getenv("APOLLO_API_KEY")
    if not api_key:
        print("ERROR: APOLLO_API_KEY fehlt in .env")
        return 1

    batch_path = Path(args.batch_file)
    if not batch_path.exists():
        print(f"ERROR: {batch_path} nicht gefunden")
        return 1

    leads = load_qualified(batch_path, args.limit)
    if not leads:
        print(f"Keine qualifizierten Leads (Tier A+B, score >= {MIN_SCORE}) in {batch_path}")
        return 1

    print(f"Gefunden: {len(leads)} qualifizierte Leads (Score >= {MIN_SCORE}), Top-{args.limit}.")
    print(f"Starte Apollo People Search...\n")

    enriched = []
    hits = 0
    for i, lead in enumerate(leads, 1):
        domain = lead["domain"]
        d = lead["data"]
        print(f"[{i}/{len(leads)}] {domain:<35} score={d.get('score_1_to_10')} tier={d.get('tier')}")
        person = search_person(api_key, domain)
        if person:
            hits += 1
            print(f"    -> {person.get('first_name','?')} {person.get('last_name','?')} | {person.get('title','')[:40]}")
        else:
            print(f"    -> kein Named Contact")
        enriched.append(enrich(lead, person))
        time.sleep(DELAY_BETWEEN_CALLS)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({"total": len(enriched), "named_contacts": hits, "results": enriched}, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nGeschrieben: {out_path}  ({hits}/{len(enriched)} mit Named Contact, {100*hits//len(enriched)}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
