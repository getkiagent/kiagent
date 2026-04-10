# Architecture

## Lead Engine (built, local)

Pipeline:
```
discover_leads.py → batch_analyze.py → generate_outreach.py --draft → n8n Webhook → Gmail Drafts
```

### Scripts
- `scripts/discover_leads.py` — DuckDuckGo search, long-tail queries + domain blacklist
- `scripts/analyze_lead.py` — single URL → Firecrawl scrape → Claude Haiku scoring
- `scripts/batch_analyze.py` — URL list → batch analysis → batch-results.json
- `scripts/batch_retry_errors.py` — retry failed URLs from batch
- `scripts/generate_outreach.py` — Lead JSON → personalized German outreach mail

### Prompts
- `prompts/lead_analysis_v1.md` — lead scoring system prompt
- `prompts/outreach_mail_v1.md` — outreach mail system prompt

### Output
- `leads/batch-results.json` — Wave 1 (7x A, 15x B, 1x C)
- `leads/batch-results-wave2.json` — Wave 2 (6x A)
- `outreach/` — generated mails per company

## n8n Workflows (production)

### Lead URL Scorer — `jGDcEjOD8RIbXKpq`
Schedule Trigger → Google Sheet Read → Firecrawl Map → Pick Pages → Firecrawl Scrape → Claude Haiku → Parse JSON → Google Sheet Write. Tested at 28 sec/URL.

### Gmail Draft from Outreach — `QxBuMHhSHuCpq3m6`
Webhook POST `{to, subject, body}` → Gmail Draft.

### Outreach Agent — `zVvZmfOWADGcN6kp`
Manual Trigger → Google Sheet Read → Filter Tier A+B (Score ≥ 6, Status analysiert) → CTA Rotation → Loop: Claude Sonnet → Parse Mail → Gmail Draft → Sheet Status Update.
Error path: Format Error → Write Error Status (outreach_error) → next lead.
Needs Anthropic API credential on HTTP Request node.

## Demo
- Voiceflow chatbot "GlowLab Support Demo" (live, GPT-based, KB uploaded)
- 5 scenarios: WISMO, returns, product FAQ, shipping, human handoff
- Loom demo recorded

## Client Delivery Stack (not yet active)
- Frontend: Voiceflow widget embedded on client site
- Backend: n8n workflows for order lookup, ticket creation
- AI Layer: Claude/OpenAI API for intent + response
- Knowledge base per client

## Tech Stack
- **Local**: Python + Firecrawl + Claude Haiku + DuckDuckGo
- **Automation**: n8n (getkiagent.app.n8n.cloud)
- **Demo**: Voiceflow
- **Outreach**: Gmail (manual send), Google Sheet (tracking)
- **APIs**: Firecrawl, Anthropic, OpenAI (Voiceflow)
- **No CRM, no database, no UI** — intentional for this phase

## File Structure
```
/getkiagent
├── /scripts/               # Lead engine Python scripts
├── /prompts/               # System prompts (versioned)
├── /leads/                 # Batch results, discovered URLs
├── /outreach/              # Generated outreach mails (.txt)
├── /demo/                  # GlowLab knowledge base, Loom scripts
├── /docs/                  # Briefs and planning docs
├── /tasks/                 # Active/completed tasks + lessons.md
├── /workflows/             # n8n JSON exports (future)
├── /voiceflow/             # Voiceflow project exports (future)
└── /clients/{name}/        # Per-client configs (future)
```
