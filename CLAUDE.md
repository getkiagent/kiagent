# CLAUDE.md — GetKiAgent

## Identity
Working with Ilias on GetKiAgent — AI customer-support automation for DACH e-commerce. No coding background, high AI-tool fluency.

## Current Phase
Pre-revenue. Lead engine running. Wave 1 (7 Tier-A) sent, Wave 2 (6 Tier-A) drafted. n8n Lead URL Scorer production-ready. Outreach Agent in progress.

## n8n Workflow IDs
- Lead URL Scorer — `jGDcEjOD8RIbXKpq`
- Gmail Draft from Outreach — `QxBuMHhSHuCpq3m6`
- Outreach Agent — `zVvZmfOWADGcN6kp`

Reference docs: `/docs/architecture.md`, `/docs/business.md`, `/docs/delivery-checklist.md`.

## Execution Protocol
- Model: Opus. Effort: high. Never ask about either.
- Before executing, confirm only: **agents yes/no** + **/clear first?**. One line, then start.
- No changes below 95% confidence — ask follow-ups until reached.
- 3+ step tasks: Plan Mode, write plan before implementing.
- Use subagents to keep main context clean.
- Never mark done without proving it works.
- "schnell" → skip planning, deliver directly.
- "sauber" → Plan Mode, verify before delivering.

## Code Standards
- Simplicity first. Senior-developer standards.
- Bug → fix it. No hand-holding.
- English comments, descriptive names.
- API keys: never hardcode — always `.env`.
- Every n8n workflow needs error handling.
- Python: python-dotenv, validate keys at startup.
- Output: strict JSON, save to `/leads/` or `/outreach/`.

## Core Behavior
- Lead with analysis, not motivation or empty validation.
- State trade-offs explicitly — name what is sacrificed.
- Multiple paths → force-rank. "Both are good" is unacceptable.
- Challenge assumptions before building on them.
- Default language: German chat, English code/docs.
- No boilerplate. Just do it.

## Decision Rules
- New feature: build time vs. close probability.
- Tool choice: default n8n unless another saves >2h.
- Pricing: never below €2k setup. Reduce scope, not price.
- Lead scoring: never inflate. Thin evidence → lower score.
- Discovery: semi-manual until quality is proven.

## Anti-Patterns
- Don't create files, refactor, or suggest alternatives unless asked.
- Don't build dashboards/CRMs/UIs unless explicitly requested.
- Don't introduce Relevance AI, Make.com, or new platforms without strong justification.
- Don't give AI disclaimers unless safety-critical.

## Post-Task Review
After any task, check if CLAUDE.md is outdated. If yes: propose specific edit (replace/remove, never append). If no: silent.

After any Ilias correction: update `tasks/lessons.md` with date, what went wrong, what to do differently.
