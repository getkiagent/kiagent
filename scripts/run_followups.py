"""
GetKiAgent — Follow-Up Orchestrator

Fetches leads due for follow-up from n8n → finds lead data in batch-results →
generates follow-up mails → saves to outreach/followup/ → creates Gmail drafts.

Usage:
    python scripts/run_followups.py
    python scripts/run_followups.py --dry-run
    python scripts/run_followups.py --input leads/followup-queue.json
"""

import sys
import json
import os
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timezone

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv not installed. Run: pip install python-dotenv")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# Search order for lead data — most recent first
BATCH_RESULTS_PATHS = [
    PROJECT_ROOT / "leads" / "qualified-leads.json",
    PROJECT_ROOT / "leads" / "batch-results-wave3.json",
    PROJECT_ROOT / "leads" / "batch-results-wave2.json",
    PROJECT_ROOT / "leads" / "batch-results.json",
    PROJECT_ROOT / "leads" / "batch-results-new.json",
]

FOLLOWUP_DIR = PROJECT_ROOT / "outreach" / "followup"
GENERATE_SCRIPT = PROJECT_ROOT / "scripts" / "generate_outreach.py"
SEND_SCRIPT = PROJECT_ROOT / "scripts" / "send_existing_drafts.py"


def fetch_followup_queue() -> list[dict]:
    """Calls N8N_FOLLOWUP_WEBHOOK to get leads due for follow-up."""
    try:
        import requests
    except ImportError:
        print("WARNING: requests not installed — cannot fetch from n8n")
        return []

    webhook_url = os.getenv("N8N_FOLLOWUP_WEBHOOK")
    if not webhook_url:
        print("WARNING: N8N_FOLLOWUP_WEBHOOK not set — use --input for local queue")
        return []

    try:
        resp = requests.post(webhook_url, json={"action": "get_queue"}, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            leads = data if isinstance(data, list) else data.get("leads", [])
            print(f"  → {len(leads)} Follow-Up Leads von n8n erhalten")
            return leads
        else:
            print(f"  → n8n Webhook Fehler: HTTP {resp.status_code} — nutze leere Queue")
            return []
    except Exception as e:
        print(f"  → n8n Webhook nicht erreichbar: {e} — nutze leere Queue")
        return []


def load_local_queue(path: Path) -> list[dict]:
    """Loads follow-up queue from a local JSON file."""
    if not path.exists():
        print(f"ERROR: Datei nicht gefunden: {path}")
        sys.exit(1)
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else data.get("leads", [])


def find_lead_data(url: str) -> dict | None:
    """Searches all batch-results files for a lead by URL."""
    target = (
        url.rstrip("/").lower()
        .replace("https://", "").replace("http://", "").replace("www.", "")
    )
    for path in BATCH_RESULTS_PATHS:
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            results = data.get("results", []) if isinstance(data, dict) else data
            for r in results:
                if r.get("status") != "ok":
                    continue
                r_url = (
                    r.get("url", "").rstrip("/").lower()
                    .replace("https://", "").replace("http://", "").replace("www.", "")
                )
                if r_url == target or target in r_url or r_url in target:
                    return r
        except Exception:
            continue
    return None


def slugify(name: str) -> str:
    """Converts company name to filename-safe slug."""
    import re
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9äöüß]+", "-", slug)
    return slug.strip("-") or "unbekannt"


def generate_followup_mail(lead: dict, followup_stage: int, dry_run: bool) -> Path | None:
    """
    Generates a follow-up mail for a single lead via generate_outreach.py.
    Uses a temp JSON file as input to avoid modifying batch-results.
    """
    company = lead.get("data", {}).get("company_name", "unknown")
    slug = slugify(company)
    output_file = FOLLOWUP_DIR / f"{slug}_followup{followup_stage}.txt"

    if output_file.exists():
        print(f"  → Bereits vorhanden: {output_file.name} — skip")
        return output_file

    if dry_run:
        print(f"  → [DRY-RUN] Würde generieren: {output_file.name}")
        return None

    # Write lead to temp file — generate_outreach.py expects a batch-results format
    temp_path = PROJECT_ROOT / "leads" / "_followup_temp.json"
    temp_path.write_text(
        json.dumps({"results": [lead]}, ensure_ascii=False),
        encoding="utf-8",
    )

    try:
        result = subprocess.run(
            [sys.executable, str(GENERATE_SCRIPT), str(temp_path), "--followup", "--force"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=120,
            cwd=str(PROJECT_ROOT),
        )
        if result.returncode != 0:
            print(f"  → FEHLER bei {company}:\n{result.stderr[:300]}")
            return None

        # generate_outreach.py saves to outreach/followup/{slug}.txt — rename to include stage
        generated = FOLLOWUP_DIR / f"{slug}.txt"
        if generated.exists():
            generated.rename(output_file)
            print(f"  → Gespeichert: {output_file.name}")
            return output_file
        else:
            # Fallback: search for any new .txt in followup dir
            for candidate in FOLLOWUP_DIR.glob("*.txt"):
                if not candidate.name.endswith(f"_followup{followup_stage}.txt"):
                    candidate.rename(output_file)
                    print(f"  → Gespeichert: {output_file.name}")
                    return output_file
            print(f"  → WARNUNG: Generierung scheinbar erfolgreich, aber Datei nicht gefunden")
            return None
    except subprocess.TimeoutExpired:
        print(f"  → TIMEOUT bei {company} (>120s)")
        return None
    except Exception as e:
        print(f"  → FEHLER: {e}")
        return None
    finally:
        if temp_path.exists():
            temp_path.unlink()


def create_gmail_drafts(dry_run: bool) -> int:
    """Creates Gmail drafts for all files in outreach/followup/."""
    files = list(FOLLOWUP_DIR.glob("*.txt"))
    if not files:
        return 0

    if dry_run:
        print(f"  → [DRY-RUN] Würde {len(files)} Gmail Drafts erstellen")
        return 0

    if not SEND_SCRIPT.exists():
        print(f"  → WARNUNG: {SEND_SCRIPT} nicht gefunden — Drafts manuell erstellen")
        return 0

    # send_existing_drafts.py reads from OUTREACH_DIR; for followup files we copy temporarily
    # and clean up after. Avoids modifying send_existing_drafts.py.
    import shutil
    OUTREACH_DIR = PROJECT_ROOT / "outreach"
    copied = []
    try:
        for f in files:
            dest = OUTREACH_DIR / f.name
            if not dest.exists():
                shutil.copy2(f, dest)
                copied.append(dest)

        result = subprocess.run(
            [sys.executable, str(SEND_SCRIPT), "--keep-existing"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=120,
            cwd=str(PROJECT_ROOT),
        )
        if result.returncode != 0:
            print(f"  → FEHLER Gmail Drafts: {result.stderr[:300]}")
            return 0
        print(f"  → Gmail Drafts erstellt")
        return len(copied)
    except Exception as e:
        print(f"  → FEHLER Gmail Drafts: {e}")
        return 0
    finally:
        # Remove temp copies from outreach/
        for f in copied:
            if f.exists():
                f.unlink()


def main():
    parser = argparse.ArgumentParser(description="GetKiAgent Follow-Up Orchestrator")
    parser.add_argument("--dry-run", action="store_true", help="Preview without API calls or file writes")
    parser.add_argument("--input", type=str, help="Local JSON file with follow-up queue (bypasses n8n)")
    args = parser.parse_args()

    print("\n=== GetKiAgent Follow-Up Orchestrator ===")
    FOLLOWUP_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Get follow-up queue
    if args.input:
        queue = load_local_queue(Path(args.input))
        print(f"Lokale Queue: {len(queue)} Einträge aus {args.input}")
    else:
        queue = fetch_followup_queue()

    if not queue:
        print("Keine Follow-Up Leads — nichts zu tun.")
        return

    print(f"\n{len(queue)} Leads in der Follow-Up Queue\n")

    # 2. Generate follow-up mails
    stats = {"generated": 0, "skipped": 0, "no_data": 0, "errors": 0, "drafts": 0}
    stage_counts = {1: 0, 2: 0, 3: 0}

    for entry in queue:
        url = entry.get("url", "")
        company = entry.get("company", url)
        followup_stage = int(entry.get("followup_stage", 1))

        print(f"[{company}] Follow-Up Stage {followup_stage}")

        lead = find_lead_data(url)
        if not lead:
            print(f"  → Keine Lead-Daten für {url} — überspringe")
            stats["no_data"] += 1
            continue

        result = generate_followup_mail(lead, followup_stage, args.dry_run)
        if result is None and not args.dry_run:
            stats["errors"] += 1
        elif result is not None:
            stats["generated"] += 1
            stage_counts[min(followup_stage, 3)] += 1
        else:
            stats["skipped"] += 1

    # 3. Create Gmail drafts
    if not args.dry_run and stats["generated"] > 0:
        stats["drafts"] = create_gmail_drafts(args.dry_run)

    # 4. Report
    print(f"\n=== Follow-Up Run — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC ===")
    print(f"  Generiert:    {stats['generated']} (stage 1/2/3: {stage_counts[1]}/{stage_counts[2]}/{stage_counts[3]})")
    print(f"  Übersprungen: {stats['skipped']} (bereits vorhanden)")
    print(f"  Keine Daten:  {stats['no_data']}")
    print(f"  Fehler:       {stats['errors']}")
    print(f"  Gmail Drafts: {stats['drafts']}")
    print("=========================================")


if __name__ == "__main__":
    main()
