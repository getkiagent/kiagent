# CLAUDE.md — GetKiAgent

## Context
GetKiAgent — AI customer-support automation for DACH e-commerce.
Ilias: no coding background, high AI-tool fluency.
Phase: Pre-revenue. Lead engine live. Wave 1 (7 Tier-A) sent, Wave 2 (6 Tier-A) drafted.

## n8n Workflow IDs
- Lead URL Scorer — `jGDcEjOD8RIbXKpq`
- Gmail Draft from Outreach — `QxBuMHhSHuCpq3m6`
- Outreach Agent — `zVvZmfOWADGcN6kp`
- Gmail Status Sync — `PP2vkOQDsNcZcrig`
- Follow-up Checker — `Ox1mvhTkhVrJoaox`

Reference docs: `/docs/architecture.md`, `/docs/business.md`, `/docs/delivery-checklist.md`, `PLAN.md`.
Niche configs: `configs/{niche}.yaml` — drives discovery queries, scoring, outreach prompts, pricing.

## Execution
- Default: Sonnet. Opus nur bei `sauber` oder komplexen Plans.
- Default: direkt ausführen. Rückfrage NUR bei destruktiven Ops (Dateien löschen, Workflows überschreiben, Outreach senden). Keyword `AUTONOM` überspringt auch das.
- Bei Unsicherheit über Dateipfade, Datenstrukturen oder API-Parameter: erst verifizieren, nicht raten.
- "schnell" → deliver directly. "sauber" → Plan Mode, verify first.
- Never mark done without proving it works.

## Reel/Video Analysis
- Bei Instagram/TikTok/YouTube-Shorts/YouTube URLs im Prompt → sofort `python tools/summarize_reel.py <url>` ausführen, dann Transkript analysieren. Keine Rückfrage.

## Code Standards
- Simplicity first. English comments, descriptive names.
- API keys: always `.env`, validate at startup.
- n8n workflows: always include error handling.
- Output: strict JSON → `/leads/` or `/outreach/`.

## Behavior
- Lead with analysis. State trade-offs explicitly.
- Multiple paths → force-rank. "Both are good" is unacceptable.
- German chat, English code/docs. No boilerplate.
- Don't create files, refactor, or suggest alternatives unless asked.
- Pricing: never below €2k setup. Reduce scope, not price.
- Tool choice: default n8n unless another saves >2h.

## Post-Task & Error Logging
- After ANY error, failed command, or unexpected behavior: immediately append to `tasks/lessons.md` before continuing. Don't wait for task completion.
- After any correction from Ilias: update `tasks/lessons.md` before continuing.
- Check if CLAUDE.md is outdated after any task. Propose specific edit or stay silent.
- Format: `### YYYY-MM-DD — [short title]` + `**Error:**` what happened + `**Root cause:**` why + `**Fix:**` what solved it.
- CLAUDE.md darf nur wachsen wenn gleichzeitig etwas entfernt oder zusammengeführt wird.

### What counts as loggable
- Shell/Python command that errors out
- Wrong file path, missing file, wrong data structure assumption
- API call failure (wrong params, auth, rate limits, unexpected response shape)
- n8n node config that doesn't validate or behaves unexpectedly
- Any task where Ilias had to correct Claude
- Dependency/install issue (pip, npm, missing package)
- Prompt that produced wrong output format or content

# Pipeline Control

Before any pipeline command ("Pipeline starten", "Follow-Up", "Status Sync"):
1. Read `PLAN.md` in project root — defines all stages, scripts, decision rules, error handling
2. Follow PLAN.md exactly — no improvisation between stages
3. No scope given → apply Autonomous Depth Decision from PLAN.md
4. Drafts only — never trigger email send
5. On n8n workflow issues: use `mcp__claude_ai_n8n__*` tools to inspect and debug inline
6. End of every run: send curl to `N8N_NOTIFICATION_WEBHOOK` (skip silently if not set)
7. Run report format: follow PLAN.md "Run Report Format" section exactly