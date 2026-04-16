#!/usr/bin/env python3
"""
Append impressum_line from configs/ecommerce-beauty.yaml to every .txt
in the target directory (default: outreach/followup) that does not
already contain it. Idempotent.

Usage:
    python scripts/append_impressum.py [DIR]
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_ROOT / "configs" / "ecommerce-beauty.yaml"
DEFAULT_DIR = PROJECT_ROOT / "outreach" / "followup"


def main():
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DIR
    if not target.exists():
        print(f"ERROR: {target} missing")
        sys.exit(1)

    cfg = yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8"))
    impressum = cfg.get("niche", {}).get("impressum_line") or cfg.get("impressum_line")
    if not impressum:
        for section in cfg.values():
            if isinstance(section, dict) and "impressum_line" in section:
                impressum = section["impressum_line"]
                break
    if not impressum:
        print("ERROR: impressum_line missing in config")
        sys.exit(1)

    marker = "Kleinunternehmer §19 UStG"
    appended = skipped = 0
    for f in sorted(target.glob("*.txt")):
        content = f.read_text(encoding="utf-8")
        if marker in content:
            skipped += 1
            continue
        new = content.rstrip() + "\n\n--\n" + impressum + "\n"
        f.write_text(new, encoding="utf-8")
        appended += 1
        print(f"  + {f.name}")

    print(f"\nAppended to {appended} files, skipped {skipped} (already had impressum).")


if __name__ == "__main__":
    main()
