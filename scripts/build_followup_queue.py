#!/usr/bin/env python3
"""
Build follow-up queue from Gmail sent history.

Scans sent threads, keeps those without a reply from the recipient,
buckets by age into stage 1/2/3, and matches each recipient email
against batch-results*.json to recover the lead URL + company.

Output: leads/followup-queue.json (list of {url, company, followup_stage, email}).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TOKEN_FILE = PROJECT_ROOT / "token.json"
OUTPUT_FILE = PROJECT_ROOT / "leads" / "followup-queue.json"

BATCH_RESULTS_PATHS = [
    PROJECT_ROOT / "leads" / "qualified-leads.json",
    PROJECT_ROOT / "leads" / "batch-results-wave3.json",
    PROJECT_ROOT / "leads" / "batch-results-wave2.json",
    PROJECT_ROOT / "leads" / "batch-results.json",
    PROJECT_ROOT / "leads" / "batch-results-new.json",
]

STAGE1_DAYS = (3, 6)
STAGE2_DAYS = (7, 13)
STAGE3_DAYS = (14, 30)


def age_to_stage(age_days: int) -> int | None:
    if STAGE1_DAYS[0] <= age_days <= STAGE1_DAYS[1]:
        return 1
    if STAGE2_DAYS[0] <= age_days <= STAGE2_DAYS[1]:
        return 2
    if STAGE3_DAYS[0] <= age_days <= STAGE3_DAYS[1]:
        return 3
    return None


def extract_email(addr: str) -> str:
    m = re.search(r"[\w\.\-\+]+@[\w\.\-]+", addr or "")
    return m.group(0).lower() if m else ""


def load_all_leads() -> list[dict]:
    out: list[dict] = []
    for path in BATCH_RESULTS_PATHS:
        if not path.exists():
            continue
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            results = raw.get("results", []) if isinstance(raw, dict) else raw
            for r in results:
                if isinstance(r, dict):
                    out.append(r)
        except Exception as e:
            print(f"  warn: {path.name}: {e}")
    return out


def match_lead(to_email: str, all_leads: list[dict]) -> dict | None:
    if not to_email:
        return None
    domain = to_email.split("@", 1)[-1].lower()
    root = ".".join(domain.split(".")[-2:])  # e.g. example.com from sub.example.com

    best = None
    for r in all_leads:
        data = r.get("data", {}) if isinstance(r.get("data"), dict) else {}
        lead_email = (data.get("email") or "").lower()
        url = (r.get("url") or "").lower()

        if lead_email == to_email:
            return r
        url_domain = re.sub(r"^https?://(www\.)?", "", url).split("/", 1)[0]
        if url_domain == domain or url_domain.endswith("." + root) or url_domain == root:
            best = best or r
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--output", type=Path, default=OUTPUT_FILE)
    args = ap.parse_args()

    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE))
    svc = build("gmail", "v1", credentials=creds)

    profile = svc.users().getProfile(userId="me").execute()
    my_email = profile["emailAddress"].lower()
    now = datetime.now(timezone.utc)

    print(f"Account: {my_email} | window: {args.days}d | now: {now.isoformat()}")

    query = f"in:sent newer_than:{args.days}d"
    resp = svc.users().messages().list(userId="me", q=query, maxResults=500).execute()
    messages = resp.get("messages", [])
    print(f"Sent messages: {len(messages)}")

    all_leads = load_all_leads()
    print(f"Leads loaded from batch-results: {len(all_leads)}")

    seen_threads: set[str] = set()
    queue: list[dict] = []
    stats = {"no_reply": 0, "replied": 0, "outside_stage": 0, "matched": 0, "no_match": 0}

    for m in messages:
        tid = m["threadId"]
        if tid in seen_threads:
            continue
        seen_threads.add(tid)

        thread = svc.users().threads().get(
            userId="me", id=tid, format="metadata",
            metadataHeaders=["From", "To", "Subject", "Date"],
        ).execute()
        msgs = thread.get("messages", [])
        if not msgs:
            continue

        # First message headers
        h0 = {h["name"]: h["value"] for h in msgs[0].get("payload", {}).get("headers", [])}
        to_addr = h0.get("To", "")
        to_email = extract_email(to_addr)
        subject = h0.get("Subject", "")
        date_str = h0.get("Date", "")

        # Any message from someone other than me = reply present
        reply_present = any(
            my_email not in (h["value"].lower())
            for msg in msgs[1:]
            for h in msg.get("payload", {}).get("headers", [])
            if h["name"] == "From"
        )
        if reply_present:
            stats["replied"] += 1
            continue
        stats["no_reply"] += 1

        # Age in days
        try:
            dt = parsedate_to_datetime(date_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            age_days = (now - dt).days
        except Exception:
            continue

        stage = age_to_stage(age_days)
        if stage is None:
            stats["outside_stage"] += 1
            continue

        lead = match_lead(to_email, all_leads)
        if not lead:
            stats["no_match"] += 1
            print(f"  no match: {to_email} ({age_days}d, stage {stage}) — {subject[:60]}")
            continue

        stats["matched"] += 1
        data = lead.get("data", {}) if isinstance(lead.get("data"), dict) else {}
        queue.append({
            "url": lead.get("url", ""),
            "company": data.get("company_name") or to_email,
            "followup_stage": stage,
            "email": to_email,
            "age_days": age_days,
            "original_subject": subject,
        })

    # Sort by stage then age
    queue.sort(key=lambda e: (e["followup_stage"], -e["age_days"]))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(queue, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("\n=== Stats ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print(f"\nQueue saved: {args.output} ({len(queue)} entries)")
    by_stage = {1: 0, 2: 0, 3: 0}
    for e in queue:
        by_stage[e["followup_stage"]] += 1
    print(f"By stage — 1: {by_stage[1]}  2: {by_stage[2]}  3: {by_stage[3]}")


if __name__ == "__main__":
    main()
