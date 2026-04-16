#!/usr/bin/env python3
"""
Fix Impressum — Post-Patch existing Outreach .txt files

Hängt die kanonische Impressum-Zeile aus configs/{niche}.yaml an alle
bestehenden outreach/**/*.txt Dateien an, die sie noch nicht enthalten.
Idempotent: Files mit Impressum werden übersprungen.

Usage:
    python scripts/fix_impressum.py --niche ecommerce-beauty
    python scripts/fix_impressum.py --niche ecommerce-beauty --dry-run
    python scripts/fix_impressum.py --niche ecommerce-beauty --folder outreach/followup
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from generate_outreach import _ensure_impressum, _impressum_from_config  # reuse canonical logic
from niche_config import load_niche_config


def collect_txt_files(folder: Path) -> list[Path]:
    """Return all .txt files under folder recursively."""
    if not folder.exists():
        return []
    return sorted(folder.rglob("*.txt"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Append canonical Impressum to existing outreach .txt files")
    parser.add_argument("--niche", required=True, help="Niche name — loads configs/{niche}.yaml")
    parser.add_argument("--folder", default=None, help="Override scan folder (default: outreach/ and outreach/followup/)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing")
    args = parser.parse_args()

    config = load_niche_config(args.niche)
    imp = _impressum_from_config(config)
    if not imp:
        print(f"ERROR: impressum_line fehlt in configs/{args.niche}.yaml")
        return 1

    if args.folder:
        folders = [Path(args.folder) if Path(args.folder).is_absolute() else PROJECT_ROOT / args.folder]
    else:
        folders = [
            PROJECT_ROOT / "outreach",
            PROJECT_ROOT / f"outreach/{args.niche}",
            PROJECT_ROOT / "outreach" / "followup",
            PROJECT_ROOT / f"outreach/{args.niche}/followup",
        ]

    txt_files: list[Path] = []
    for f in folders:
        txt_files.extend(collect_txt_files(f))
    # dedup while preserving order
    seen = set()
    txt_files = [p for p in txt_files if not (p in seen or seen.add(p))]

    if not txt_files:
        print("Keine .txt Dateien gefunden.")
        return 0

    print(f"Scan: {len(txt_files)} Dateien. Impressum-Check…\n")

    stats = {"patched": 0, "skipped": 0, "errors": 0}
    for path in txt_files:
        try:
            original = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"  ERROR lesen {path}: {exc}")
            stats["errors"] += 1
            continue
        patched = _ensure_impressum(original, config)
        if patched == original:
            stats["skipped"] += 1
            continue
        rel = path.relative_to(PROJECT_ROOT)
        if args.dry_run:
            print(f"  [dry] würde patchen: {rel}")
        else:
            path.write_text(patched, encoding="utf-8")
            print(f"  patched: {rel}")
        stats["patched"] += 1

    print(f"\nFertig. Patched: {stats['patched']} | Skipped (ok): {stats['skipped']} | Errors: {stats['errors']}")
    if args.dry_run:
        print("(dry-run: keine Dateien geändert)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
