#!/usr/bin/env python3
"""
Inserts Loom demo link before the signature in outreach .txt files
that don't already contain a loom.com URL.

Usage:
    python scripts/add_loom_link.py [--dry-run]
"""

import sys
import os
import glob

OUTREACH_DIR = os.path.join(os.path.dirname(__file__), "..", "outreach")
LOOM_BLOCK = (
    "Hier eine kurze Demo, wie das konkret aussehen kann:\n"
    "https://www.loom.com/share/a243a6f8c920487a9db15e9c9816c36e"
)

def find_signature_line(lines):
    """Return index of the first line that starts with 'Ilias', or -1."""
    for i, line in enumerate(lines):
        if line.strip().startswith("Ilias"):
            return i
    return -1

def process_file(path, dry_run):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "loom.com" in content:
        return False  # already has link

    lines = content.splitlines(keepends=True)
    sig_idx = find_signature_line(lines)

    if sig_idx == -1:
        print(f"  SKIP (no signature found): {os.path.basename(path)}")
        return False

    # Insert blank line + loom block before the signature line
    insert = LOOM_BLOCK + "\n\n"
    # Ensure there's exactly one blank line before the block
    # (trim trailing blank lines before sig, then re-add one)
    while sig_idx > 0 and lines[sig_idx - 1].strip() == "":
        lines.pop(sig_idx - 1)
        sig_idx -= 1

    lines.insert(sig_idx, "\n")           # blank separator after loom block
    lines.insert(sig_idx, insert)         # loom block itself
    lines.insert(sig_idx, "\n")           # blank line before loom block

    new_content = "".join(lines)

    if not dry_run:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)

    return True

def main():
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print("[DRY RUN] No files will be modified.\n")

    txt_files = sorted(glob.glob(os.path.join(OUTREACH_DIR, "*.txt")))
    if not txt_files:
        print(f"No .txt files found in {OUTREACH_DIR}")
        sys.exit(1)

    fixed = []
    for path in txt_files:
        if process_file(path, dry_run):
            fixed.append(os.path.basename(path))
            print(f"  {'WOULD FIX' if dry_run else 'FIXED'}: {os.path.basename(path)}")

    print(f"\n{'Would fix' if dry_run else 'Fixed'}: {len(fixed)} / {len(txt_files)} files")

if __name__ == "__main__":
    main()
