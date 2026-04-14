# Architecture

## Lead Engine (lokal)

Pipeline:
```
discover_leads.py → batch_analyze.py → generate_outreach.py --draft → n8n Webhook → Gmail Drafts
```

**Scripts:**
- `discover_leads.py` — DuckDuckGo-Suche, Long-tail-Queries + Domain-Blacklist
- `analyze_lead.py` — einzelne URL → Firecrawl-Scrape → Claude Haiku Scoring
- `batch_analyze.py` — URL-Liste → Batch-Analyse → batch-results.json
- `batch_retry_errors.py` — fehlgeschlagene URLs wiederholen
- `generate_outreach.py` — Lead-JSON → personalisierte deutsche Outreach-Mail

**Prompts:**
- `prompts/lead_analysis_v1.md` — Lead-Scoring-System-Prompt
- `prompts/outreach_mail_v1.md` — Outreach-Mail-System-Prompt

## n8n Workflows (Produktion)

| Workflow | ID | Funktion |
|---|---|---|
| Lead URL Scorer | `jGDcEjOD8RIbXKpq` | Sheet → Firecrawl → Claude Haiku → Sheet. 28 Sek/URL |
| Gmail Draft from Outreach | `QxBuMHhSHuCpq3m6` | Webhook POST → Gmail Draft |
| Outreach Agent | `zVvZmfOWADGcN6kp` | Sheet → Filter Tier A+B → Claude Sonnet → Gmail Draft |
| Gmail Status Sync | `PP2vkOQDsNcZcrig` | Status-Abgleich |
| Follow-up Checker | `Ox1mvhTkhVrJoaox` | Follow-up-Logik |

## Demo

- Voiceflow Chatbot "GlowLab Support Demo" (live, GPT-basiert)
- 5 Szenarien: WISMO, Returns, Produkt-FAQ, Versand, Human Handoff
- Loom-Demo aufgezeichnet

## Tech Stack

- **Lokal:** Python + Firecrawl + Claude Haiku + DuckDuckGo
- **Automation:** n8n (getkiagent.app.n8n.cloud)
- **Demo:** Voiceflow
- **Outreach:** Gmail + Google Sheets
- **APIs:** Firecrawl, Anthropic, OpenAI
- **Kein CRM, keine DB, kein UI** — bewusst für diese Phase
