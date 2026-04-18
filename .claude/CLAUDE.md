# CLAUDE.md — GetKiAgent

## Context
GetKiAgent — AI customer-support automation for DACH e-commerce.
Ilias: no coding background, high AI-tool fluency.
Phase: Pre-revenue. Lead engine live. Wave 1 (7 Tier-A) sent, Wave 2 (6 Tier-A) drafted.

## Knowledge Base
Vault: `C:\Users\ilias\obsidian-vault\` — Rules siehe dort, Wiki unter `projects/getkiagent/wiki/`

## n8n Workflow IDs
- Lead URL Scorer — `jGDcEjOD8RIbXKpq`
- Gmail Draft from Outreach — `QxBuMHhSHuCpq3m6`
- Outreach Agent — `zVvZmfOWADGcN6kp`
- Gmail Status Sync — `PP2vkOQDsNcZcrig`
- Follow-up Checker — `Ox1mvhTkhVrJoaox`
- Reply Watcher — `qTptgWEJF5fvCkwj` (Cron 30min, Sheet → Telegram)
- Outreach Draft Batch Send — `TQMPiSl8a8hHtbq7` (Mo-Fr 9 Uhr, 30/Tag; Manual = Dry Run)

Reference docs: `/docs/architecture.md`, `/docs/business.md`, `/docs/delivery-checklist.md`, `PLAN.md`.
Niche configs: `configs/{niche}.yaml` — drives discovery queries, scoring, outreach prompts, pricing.

## Execution
- Default: Sonnet. Opus nur bei `sauber` oder komplexen Plans.
- Default: direkt ausführen. Rückfrage NUR bei destruktiven Ops (Dateien löschen, Workflows überschreiben, Outreach senden). Keyword `AUTONOM` überspringt auch das.
- Bei Unsicherheit über Dateipfade, Datenstrukturen oder API-Parameter: erst verifizieren, nicht raten.
- Bei mehreren Interpretationen: alle nennen und ranken, nicht still eine wählen.
- "schnell" → deliver directly. "sauber" → Plan Mode, verify first.
- Vor Implementierung: Success Criteria in 1-2 Sätzen formulieren.
- Multi-Step Tasks: kurzer Plan mit Verify-Check pro Schritt.
- 3+ Schritte oder architektonische Entscheidung → Plan Mode automatisch, nicht nur bei `sauber`.
- "Fix the bug" → erst reproduzieren, dann fixen, dann verifizieren.
- Never mark done without proving it works.
- Vor "done": "Würde ein Staff Engineer das so abnehmen?" — wenn nein, nachbessern.

## Subagents
- Research, Exploration, parallele Analysen → Subagent (Explore/general-purpose), nicht inline im Main-Context.
- Ein Task pro Subagent. Bei Multi-File-Debugs oder >3 Grep/Glob-Runden: delegieren.
- Builder-Validator bei n8n-Workflows und Scripts >20 Zeilen (siehe `rules/builder-validator.md`).

## Reel/Video Analysis
- Bei Instagram/TikTok/YouTube-Shorts/YouTube URLs im Prompt → sofort `python tools/summarize_reel.py <url>` ausführen, dann Transkript analysieren. Keine Rückfrage.

## Code Standards
- Simplicity first. English comments, descriptive names, no magic numbers.
- API keys: always `.env`, validate at startup.
- n8n workflows: always include error handling.
- Output: strict JSON → `/leads/` or `/outreach/`.
- If 200 lines could be 50, rewrite it.

## Surgical Changes
- Jede geänderte Zeile muss direkt auf den Auftrag zurückführbar sein.
- Adjacent Code, Comments, Formatting nicht "verbessern".
- Bestehenden Stil matchen, auch wenn man es anders machen würde.
- Eigene Imports/Vars aufräumen, aber bestehenden Dead Code nur melden — nicht löschen.
- Don't create files, refactor, or suggest alternatives unless asked.

## Behavior
- German chat, English code/docs. No boilerplate.
- Lead with analysis. Multiple paths → force-rank. "Both are good" is unacceptable.
- Pricing: never below €2k setup. Reduce scope, not price.
- Tool choice: default n8n unless another saves >2h.

## Post-Task & Error Logging
- After ANY error, failed command, or unexpected behavior: immediately append to `tasks/lessons.md` before continuing. Don't wait for task completion.
- After any correction from Ilias: update `tasks/lessons.md` before continuing.
- Check if CLAUDE.md is outdated after any task. Propose specific edit or stay silent.
- Format: `### YYYY-MM-DD — [short title]` + `**Error:**` what happened + `**Root cause:**` why + `**Fix:**` what solved it.
- CLAUDE.md darf nur wachsen wenn gleichzeitig etwas entfernt oder zusammengeführt wird.

### What counts as loggable
- Command-Fehler (Shell, Python, Dependency/Install)
- Falsche Annahme über Pfade, Datenstrukturen, API-Responses
- n8n Node-Config fehlerhaft oder unerwartetes Verhalten
- Prompt mit falschem Output-Format/-Inhalt
- Jede Korrektur durch Ilias

# Pipeline Control

Before any pipeline command ("Pipeline starten", "Follow-Up", "Status Sync"):
1. Read `PLAN.md` in project root — defines all stages, scripts, decision rules, error handling
2. Follow PLAN.md exactly — no improvisation between stages
3. No scope given → apply Autonomous Depth Decision from PLAN.md
4. Drafts only — never trigger email send
5. On n8n workflow issues: use `mcp__claude_ai_n8n__*` tools to inspect and debug inline
6. End of every run: send curl to `N8N_NOTIFICATION_WEBHOOK` (skip silently if not set)
7. Run report format: follow PLAN.md "Run Report Format" section exactly