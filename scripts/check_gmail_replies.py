#!/usr/bin/env python3
"""
Gmail reply watcher with Telegram alerts and dedup.

Scans sent threads for the last N days, detects genuine replies
(skips auto-responders), dedups via tasks/alerted-replies.json,
and pushes one Telegram message per new real reply.

Usage:
    python scripts/check_gmail_replies.py          # alert new replies
    python scripts/check_gmail_replies.py --dry-run # show what would fire
    python scripts/check_gmail_replies.py --days 7  # narrow window
"""
from __future__ import annotations

import argparse
import html
import json
import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import requests
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

TOKEN_FILE = PROJECT_ROOT / "token.json"
ALERTED_FILE = PROJECT_ROOT / "tasks" / "alerted-replies.json"

# Heuristic: skip obvious auto-responders by subject/from patterns
AUTORESPONDER_PATTERNS = [
    "automatisch", "automatic reply", "auto-reply", "out of office",
    "abwesenheit", "urlaubsmeldung", "vielen dank für ihre nachricht",
    "ihre anfrage ist bei uns eingegangen", "ticket eröffnet",
    "dankeschön für deine nachricht",
]
AUTORESPONDER_FROM = ["noreply", "no-reply", "do-not-reply", "donotreply", "mailer-daemon"]


def get_service():
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE))
    return build("gmail", "v1", credentials=creds)


def load_alerted() -> set[str]:
    if not ALERTED_FILE.exists():
        return set()
    try:
        data = json.loads(ALERTED_FILE.read_text(encoding="utf-8"))
        return set(data.get("alerted_threads", []))
    except (json.JSONDecodeError, OSError):
        return set()


def save_alerted(alerted: set[str]) -> None:
    ALERTED_FILE.parent.mkdir(parents=True, exist_ok=True)
    ALERTED_FILE.write_text(
        json.dumps({"alerted_threads": sorted(alerted)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def is_autoresponder(subject: str, from_addr: str, body_snippet: str) -> bool:
    s = (subject or "").lower()
    f = (from_addr or "").lower()
    b = (body_snippet or "").lower()[:500]
    if any(p in f for p in AUTORESPONDER_FROM):
        return True
    for p in AUTORESPONDER_PATTERNS:
        if p in s or p in b:
            return True
    return False


def send_telegram(text: str) -> bool:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("WARNING: TELEGRAM_BOT_TOKEN/CHAT_ID missing — skipping alert")
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        r = requests.post(url, json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }, timeout=15)
        return r.status_code == 200
    except Exception as e:
        print(f"Telegram error: {e}")
        return False


def find_replies(svc, my_email: str, days: int) -> list[dict]:
    query = f"in:sent newer_than:{days}d"
    resp = svc.users().messages().list(userId="me", q=query, maxResults=500).execute()
    messages = resp.get("messages", [])

    replies: list[dict] = []
    seen_threads: set[str] = set()

    for m in messages:
        tid = m["threadId"]
        if tid in seen_threads:
            continue
        seen_threads.add(tid)

        thread = svc.users().threads().get(
            userId="me", id=tid, format="metadata",
            metadataHeaders=["From", "To", "Subject", "Date", "Snippet"],
        ).execute()
        msgs = thread.get("messages", [])
        if len(msgs) < 2:
            continue

        subject = ""
        first_to = ""
        reply_from = ""
        reply_date = ""
        snippet = thread.get("snippet", "")

        for i, msg in enumerate(msgs):
            headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
            frm = headers.get("From", "")
            if i == 0:
                subject = headers.get("Subject", "")
                first_to = headers.get("To", "")
            elif my_email.lower() not in frm.lower():
                reply_from = frm
                reply_date = headers.get("Date", "")
                snippet = msg.get("snippet", "") or snippet
                break

        if not reply_from:
            continue

        replies.append({
            "thread_id": tid,
            "subject": subject,
            "to": first_to,
            "reply_from": reply_from,
            "reply_date": reply_date,
            "snippet": snippet,
            "is_auto": is_autoresponder(subject, reply_from, snippet),
        })
    return replies


def format_alert(r: dict) -> str:
    thread_url = f"https://mail.google.com/mail/u/0/#inbox/{r['thread_id']}"
    esc = html.escape
    return (
        f"<b>📩 Neuer Reply</b>\n\n"
        f"<b>Von:</b> {esc(r['reply_from'])}\n"
        f"<b>Betreff:</b> {esc(r['subject'])}\n"
        f"<b>Datum:</b> {esc(r['reply_date'])}\n\n"
        f"<i>{esc((r['snippet'] or '')[:200])}</i>\n\n"
        f'<a href="{thread_url}">In Gmail öffnen</a>'
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--include-auto", action="store_true", help="include auto-responders")
    args = ap.parse_args()

    svc = get_service()
    profile = svc.users().getProfile(userId="me").execute()
    my_email = profile["emailAddress"]
    print(f"Account: {my_email} | window: {args.days}d | dry-run: {args.dry_run}")

    alerted = load_alerted()
    replies = find_replies(svc, my_email, args.days)
    print(f"Threads with replies: {len(replies)} | already alerted: {len(alerted)}")

    new_real = []
    new_auto = []
    for r in replies:
        if r["thread_id"] in alerted:
            continue
        if r["is_auto"] and not args.include_auto:
            new_auto.append(r)
            continue
        new_real.append(r)

    print(f"NEW real replies: {len(new_real)} | NEW auto-responders filtered: {len(new_auto)}")

    fired = 0
    for r in new_real:
        print(f"  → {r['reply_from']} | {r['subject']}")
        if args.dry_run:
            continue
        if send_telegram(format_alert(r)):
            alerted.add(r["thread_id"])
            fired += 1
        else:
            print("    (telegram failed — not marking as alerted)")

    # Auto-responders: mark as alerted silently so they don't re-appear
    if not args.dry_run:
        for r in new_auto:
            alerted.add(r["thread_id"])
        save_alerted(alerted)

    print(f"\nDone. {fired} Telegram alerts sent.")


if __name__ == "__main__":
    main()
