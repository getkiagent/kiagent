# Wiki Rules — GetKiAgent

Gilt **zusätzlich** zur Vault-Root `CLAUDE.md`. Backlink-Pflicht daher auch hier.

## Structure
- `index.md` — Master-Index, eine Zeile pro Seite
- `log.md` — Append-only Ingest-Log
- `[topic].md` — individuelle Seiten

## Navigation Rules
- Immer `index.md` ZUERST lesen vor jeder Query
- Nur Seiten laden die direkt relevant sind
- Seiten unter 300 Wörtern halten
- Links **immer als Wikilinks**: `[[architecture]]` statt `[architecture.md](architecture.md)`

## Backlink-Pflicht
Jede neue Wiki-Seite muss:
1. Im `index.md` verlinkt sein
2. Mindestens 2 andere Wiki-Seiten via `[[...]]` referenzieren
3. Von mindestens einer anderen Seite zurückverlinkt sein

## GetKiAgent Context
- Business: AI Customer Support Automation für E-Commerce (Shopify/WooCommerce)
- Revenue Model: €2k-10k Setup + monatliche Retainer
- Stack: n8n, Voiceflow, Claude API, Make.com, Firecrawl
- Phase: Erste Demo → erster zahlender Kunde
- Acquisition: 3-4 funktionierende Demos, kein Content

## Tags für Wiki-Seiten
- `#projekt/getkiagent` Pflicht
- `#typ/wiki`
- Thema-Tag je nach Seite (`#thema/architektur`, `#thema/business`, etc.)
