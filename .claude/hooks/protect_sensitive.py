#!/usr/bin/env python3
"""PreToolUse hook: block Write/Edit on sensitive files.

Reads hook JSON from stdin, writes decision JSON to stdout.
Blocks:
  - .env, .env.* (anywhere)
  - configs/*.yaml (any yaml under configs/)
  - outreach/send_*.py, outreach/dispatch_*.py, outreach/**/send_*.py
"""
import json
import re
import sys

PATTERNS = [
    (re.compile(r"(^|[\\/])\.env(\.[^\\/]+)?$"), ".env file"),
    (re.compile(r"(^|/)configs/[^/]+\.ya?ml$"), "configs/*.yaml"),
    (re.compile(r"(^|/)outreach/.*(send|dispatch)_[^/]+\.py$"), "outreach send/dispatch script"),
]

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    path = (data.get("tool_input") or {}).get("file_path") or ""
    norm = path.replace("\\", "/")

    for pat, label in PATTERNS:
        if pat.search(norm):
            out = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"Blocked: {label} is protected. Ask user explicitly before editing {path}.",
                },
                "systemMessage": f"File protection: {path} blocked ({label}).",
            }
            print(json.dumps(out))
            sys.exit(0)

    sys.exit(0)

if __name__ == "__main__":
    main()
