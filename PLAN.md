# PLAN.md — GetKiAgent Pipeline Control File

Read this file before any pipeline command. Follow stages, decision rules, and error handling
exactly. No manual confirmation between stages. Emails land as Gmail Drafts — never trigger send.

---

## Autonomous Depth Decision

When no scope is specified, Claude Code decides how far to run based on current state:

1. `leads/discovered-urls.txt` empty or last-modified >3 days → start from Stage 1
2. `discovered-urls.txt` exists but URLs not all in `scrape-cache/` → start from Stage 2
3. `leads/qualified-leads.json` exists with entries lacking matching `outreach/*.txt` → start from Stage 4
4. All qualified leads have outreach files → run Status Sync only (Stage 7)

Default full run: Stage 1 → 2 → 4 → 5

---

## Trigger Commands

| Command | Stages Run |
|---------|-----------|
| `Pipeline starten` | Autonomous depth (see above) |
| `Pipeline starten, nur Research` | Stage 1 only |
| `Pipeline starten, nur Score` | Stage 2 only (uses existing discovered-urls.txt) |
| `Pipeline starten, N Leads max` | Full pipeline, stop after N qualified leads reach Stage 5 |
| `Pipeline starten, Follow-Up` | Stage 6 only |
| `Status Sync` | Stage 7 only |

---

## Stage 1 — Research (Lead Discovery)

**Script:** `python scripts/discover_leads.py [--niche {niche}]`
**Output:** `leads/discovered-urls.txt` (legacy) or `leads/{niche}/discovered-urls.txt` (niche mode)
**n8n sync:** automatic via `N8N_DISCOVERY_WEBHOOK` (inside script, non-blocking)

With `--niche`: loads queries from `configs/{niche}.yaml` → `discovery.ddg_queries`.
Without `--niche`: uses hardcoded SEARCH_QUERIES (legacy).

Rules:
- Run ALL queries — no early exit, no artificial limit
- Skip URLs already in `leads/scrape-cache/` (already analyzed, cost control)
- DuckDuckGo rate-limit → wait 30s, retry once, skip query, continue with next

---

## Stage 2 — Score + Export

**Script:** `python scripts/batch_analyze.py leads/discovered-urls.txt --output leads/batch-results-new.json [--niche {niche}]`
**Output 1:** `leads/batch-results-new.json` (legacy) or `leads/{niche}/batch-results.json` (niche mode)
**Output 2:** `leads/qualified-leads.json` (legacy) or `leads/{niche}/qualified-leads.json` (niche mode)
**n8n sync:** automatic via `N8N_RESULTS_WEBHOOK` (inside script, non-blocking)

With `--niche`: loads pain_signals + disqualifiers from `configs/{niche}.yaml` → injected as extra context into Claude scoring prompt. Cache goes to `leads/{niche}/scrape-cache/`.
Without `--niche`: uses base prompt only (legacy).

If `batch-results-new.json` from today already exists → skip re-analysis, proceed to Stage 4.
If run was interrupted → `python scripts/batch_analyze.py --heal-only --output leads/batch-results-new.json [--niche {niche}]`

Scoring (source: `prompts/lead_analysis_v1.md`):
- Pain signal weight: no chat/bot > bad bot > slow support
- Minimum size: 5 employees
- **Score ≥7** → written to `leads/qualified-leads.json` → Stage 4
- **Score 5-6** → batch-results-new.json only, logged to `leads/scored-not-sent.txt`
- **Score <5** → batch-results-new.json only, discarded

Error handling:
- Firecrawl timeout → retry once after 10s → skip if still failing
- Claude parse error → retry with strict JSON suffix → skip if still failing
- Persistent failure (>2 retries) → log, continue

---

## Stage 4 — Outreach Generation

**Input:** `leads/qualified-leads.json` (legacy) or `leads/{niche}/qualified-leads.json` (niche mode)
**Script:** `python scripts/generate_outreach.py leads/qualified-leads.json --min-score 7 --max-score 10 [--niche {niche}]`
**Prompt routing:** score 8-10 → `outreach_mail_v1.md` (Tier A) | score 7 → `outreach_mail_tier_b_v1.md` (Tier B). With `--niche`: prompt paths from `configs/{niche}.yaml`.
**Output:** `outreach/{company-slug}.txt` (legacy) or `outreach/{niche}/{company-slug}.txt` (niche mode)

Rules:
- Skip if `outreach/{company-slug}.txt` already exists (never regenerate)
- On generation failure → log, skip, continue

Quality gate (check each generated file before Stage 5):
1. Contains `P.S. Hier eine kurze Demo` + Loom URL
2. Does NOT contain `Kein Skript-Bot` or `24/7, auf Deutsch`
3. Subject line contains company name
4. Ends with `Ilias\nGetKiAgent — KI-Support für E-Commerce`
5. Gate fails → regenerate once (`--force --only <company>`) → skip if still failing

---

## Stage 5 — Gmail Drafts

**Script:** `python scripts/send_existing_drafts.py --keep-existing`
**Post-run:** `python scripts/cleanup_drafts.py`

Rules:
- Always `--keep-existing` — never overwrite existing drafts
- Gmail OAuth expired → **STOP**, report: `"Gmail auth expired — refresh token.json manually"`
- User reviews Entwürfe and sends manually — pipeline never triggers send

---

## Stage 6 — Follow-Up

**Script:** `python scripts/run_followups.py`
**Flags:** `--dry-run` (preview without API calls) | `--input leads/followup-queue.json` (bypass n8n)

Flow:
1. POST to `N8N_FOLLOWUP_WEBHOOK` (workflow `Ox1mvhTkhVrJoaox`) → get `[{url, company, followup_stage, email}]`
2. For each lead: find data in `qualified-leads.json` or `batch-results-*.json`
3. Generate follow-up via `generate_outreach.py --followup --force` functions
4. Save to `outreach/followup/{slug}_followup{stage}.txt`
5. Create Gmail drafts: `python scripts/send_existing_drafts.py --keep-existing`

Thresholds: stage 1 = +3 days | stage 2 = +7 days | stage 3 = +14 days
After stage 3 no reply → 30-day queue (n8n handles this automatically)

Run every 2-3 days or on explicit trigger.

---

## Stage 7 — Status Sync

**Action:** Trigger n8n workflow `PP2vkOQDsNcZcrig` (Gmail Status Sync) via webhook
**No local script needed.**

Run every 2-3 days or after a batch of drafts is created.
If webhook fails → log warning, continue — sync catches up on next run.
Google Sheet ID: `1OReC3rBa6bMImrw96dbTryW5LlB0SYWnbpn_t7x0-u0`

---

## End-of-Run Notification

Nach jedem Pipeline-Durchlauf:

```bash
~/.local/bin/notify-claude.sh done "Pipeline: Stages {list}, {n} Leads, {m} Drafts"
```

Bei Fehler der Pipeline stoppt:

```bash
~/.local/bin/notify-claude.sh error "{was schiefging}"
```

Optional: Wenn `N8N_NOTIFICATION_WEBHOOK` gesetzt ist, zusätzlich curl POST senden:

```bash
curl -s -X POST "$N8N_NOTIFICATION_WEBHOOK" \
  -H "Content-Type: application/json" \
  -d "{\"run_at\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"stages\":\"<list>\",\"stats\":<stats_json>}"
```

---

## n8n Workflow Reference

| Workflow | ID | Called When |
|----------|----|-------------|
| Lead URL Scorer | `jGDcEjOD8RIbXKpq` | Stage 1 auto-sync |
| Gmail Draft from Outreach | `QxBuMHhSHuCpq3m6` | Fallback for Stage 5 |
| Outreach Agent | `zVvZmfOWADGcN6kp` | n8n-native alternative Stage 4+5 |
| Gmail Status Sync | `PP2vkOQDsNcZcrig` | Stage 7 |
| Follow-up Checker | `Ox1mvhTkhVrJoaox` | Stage 6 Step 1 |

- Use n8n MCP tools (`mcp__claude_ai_n8n__*`) to inspect/debug workflows inline
- Use n8n as fallback: if local script fails twice, trigger equivalent n8n workflow

---

## Error Handling Matrix

| Error | Action |
|-------|--------|
| DuckDuckGo rate limit | Wait 30s, retry once, skip query, continue |
| Firecrawl timeout | Retry once after 10s, skip if still failing |
| Firecrawl error (non-timeout) | Skip URL, log, continue |
| Claude parse error | Retry with strict JSON instruction, skip if still failing |
| Gmail OAuth expired | STOP at Stage 5, report to user |
| n8n webhook unreachable | Log warning, continue (sync eventual) |
| Score ≥7 but no email found | Log to `leads/no-email-queue.txt`, skip outreach |
| outreach file already exists | Skip generation, continue |
| N8N_NOTIFICATION_WEBHOOK missing | Skip silently |

---

## Required Environment Variables

```
ANTHROPIC_API_KEY           # Required — STOP if missing
FIRECRAWL_API_KEY           # Required — STOP if missing
N8N_DISCOVERY_WEBHOOK       # Optional — skip sync if missing
N8N_RESULTS_WEBHOOK         # Optional — skip sync if missing
N8N_FOLLOWUP_WEBHOOK        # Optional — needed for Stage 6
N8N_NOTIFICATION_WEBHOOK    # Optional — secondary logging, not primary notification
GOOGLE_SERVICE_ACCOUNT_JSON # Optional — clean_sheet.py only
GOOGLE_SHEET_ID             # Default: 1OReC3rBa6bMImrw96dbTryW5LlB0SYWnbpn_t7x0-u0
```

---

## Scope Limits

- Drafts only — never trigger email send
- No direct Google Sheet writes — use n8n for all sheet operations
- No re-analysis of URLs already in `scrape-cache/` (cost control)
- No outreach for score <7
- No Tier C prompt — skip lead entirely instead
- No regeneration of existing `outreach/{company}.txt` files

---

## Run Report Format

Print at end of every pipeline run:

```
=== GetKiAgent Pipeline Run — {YYYY-MM-DD HH:MM UTC} ===
Stages run:    {e.g. "1, 2, 4, 5"}
Stage 1:       {n} URLs discovered ({m} new)
Stage 2:       {n} analyzed | {a} score≥7 | {b} score 5-6 | {c} errors
Stage 4:       {a} emails generated | {b} skipped (exist) | {c} failed QA
Stage 5:       {a} Gmail drafts created
Follow-Up:     {a} follow-up drafts (stage 1/2/3: {x}/{y}/{z})
Notification:  sent / skipped (webhook not set)
Errors:        {list blocking errors or "none"}
===
```
