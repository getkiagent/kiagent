#!/usr/bin/env python3
"""
GetKiAgent Reply-Alert (Telegram)

Scannt die Google Sheet "Lead Pipeline" nach Rows mit status=replied,
dedupliziert via tasks/alerted-replies.json und sendet pro neuen Reply
eine Telegram-Nachricht an den konfigurierten Chat.

Optional: --refresh triggert vor dem Check den Gmail Status Sync Webhook,
damit der Sheet-Status aktuell ist.

Setup:
    1. Telegram-Bot erstellen: @BotFather -> /newbot -> Token kopieren
    2. Bot anschreiben (eine Nachricht senden)
    3. https://api.telegram.org/bot<TOKEN>/getUpdates -> chat.id ablesen
    4. In .env setzen:
         TELEGRAM_BOT_TOKEN=123456:ABC...
         TELEGRAM_CHAT_ID=123456789
         GOOGLE_SERVICE_ACCOUNT_JSON=/path/to/sa.json
         GOOGLE_SHEET_ID=1OReC3... (optional, default hardcoded)
         N8N_GMAIL_SYNC_WEBHOOK=https://getkiagent.app.n8n.cloud/webhook/gmail-status-sync (optional)

Usage:
    python scripts/check_replies.py
    python scripts/check_replies.py --refresh
    python scripts/check_replies.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

try:
    import gspread
    from google.oauth2.service_account import Credentials
except ImportError:
    print("ERROR: gspread or google-auth nicht installiert.")
    print("  pip install gspread google-auth")
    sys.exit(1)

SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "1OReC3rBa6bMImrw96dbTryW5LlB0SYWnbpn_t7x0-u0")
SHEET_TAB = "Lead Pipeline"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
ALERTED_FILE = PROJECT_ROOT / "tasks" / "alerted-replies.json"
SYNC_WAIT_SECONDS = 30


def get_sheet():
    creds_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not creds_path:
        print("ERROR: GOOGLE_SERVICE_ACCOUNT_JSON fehlt in .env")
        sys.exit(1)
    creds_file = Path(creds_path)
    if not creds_file.exists():
        print(f"ERROR: Service-Account-Datei nicht gefunden: {creds_file}")
        sys.exit(1)
    creds = Credentials.from_service_account_file(str(creds_file), scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).worksheet(SHEET_TAB)


def load_alerted() -> set[str]:
    if not ALERTED_FILE.exists():
        return set()
    try:
        data = json.loads(ALERTED_FILE.read_text(encoding="utf-8"))
        return set(data.get("alerted_urls", []))
    except (json.JSONDecodeError, OSError):
        return set()


def save_alerted(urls: set[str]) -> None:
    ALERTED_FILE.parent.mkdir(parents=True, exist_ok=True)
    ALERTED_FILE.write_text(
        json.dumps({"alerted_urls": sorted(urls)}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def trigger_gmail_sync() -> None:
    webhook = os.getenv("N8N_GMAIL_SYNC_WEBHOOK")
    if not webhook:
        print("  [refresh] N8N_GMAIL_SYNC_WEBHOOK nicht gesetzt — überspringe.")
        return
    print(f"  [refresh] triggere Gmail Status Sync...")
    try:
        r = requests.post(webhook, timeout=15)
        print(f"  [refresh] HTTP {r.status_code} — warte {SYNC_WAIT_SECONDS}s auf Sync-Abschluss")
        time.sleep(SYNC_WAIT_SECONDS)
    except requests.RequestException as exc:
        print(f"  [refresh] ERROR: {exc}")


def send_telegram(token: str, chat_id: str, text: str) -> bool:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}
    try:
        r = requests.post(url, json=payload, timeout=15)
    except requests.RequestException as exc:
        print(f"  Telegram ERROR: {exc}")
        return False
    if r.status_code != 200:
        print(f"  Telegram HTTP {r.status_code}: {r.text[:200]}")
        return False
    return True


def format_alert(row: dict) -> str:
    company = row.get("company_name") or row.get("url") or "Unbekannt"
    url = row.get("url") or ""
    tier = row.get("tier") or "?"
    score = row.get("score_1_to_10") or "?"
    return (
        f"<b>Reply erhalten</b>\n"
        f"Firma: <b>{company}</b>\n"
        f"URL: {url}\n"
        f"Tier: {tier} | Score: {score}\n\n"
        f"Gmail öffnen und reagieren."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Reply-Check + Telegram-Alert")
    parser.add_argument("--refresh", action="store_true", help="Trigger Gmail Status Sync vor Check (wartet 30s)")
    parser.add_argument("--dry-run", action="store_true", help="Zeige neue Replies, sende aber nichts")
    args = parser.parse_args()

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not args.dry_run and (not token or not chat_id):
        print("ERROR: TELEGRAM_BOT_TOKEN oder TELEGRAM_CHAT_ID fehlt in .env")
        return 1

    if args.refresh:
        trigger_gmail_sync()

    print(f"Lese Sheet {SHEET_TAB}...")
    sheet = get_sheet()
    rows = sheet.get_all_records()
    print(f"  -> {len(rows)} Zeilen")

    replied = [r for r in rows if str(r.get("status", "")).strip() == "replied"]
    if not replied:
        print("Keine replied-Einträge im Sheet.")
        return 0

    alerted = load_alerted()
    new_replies = [r for r in replied if r.get("url") and r["url"] not in alerted]

    if not new_replies:
        print(f"Alle {len(replied)} Replies bereits alertiert. Nichts zu tun.")
        return 0

    print(f"\n{len(new_replies)} neue Replies erkannt.\n")
    for row in new_replies:
        alert = format_alert(row)
        company = row.get("company_name") or row.get("url")
        print(f"  -> {company}")
        if args.dry_run:
            print(alert)
            print("---")
            continue
        ok = send_telegram(token, chat_id, alert)
        if ok:
            alerted.add(row["url"])

    if not args.dry_run:
        save_alerted(alerted)
        print(f"\nGesendet: {len(new_replies)} Alerts. State: {ALERTED_FILE.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
