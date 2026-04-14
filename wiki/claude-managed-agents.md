# Claude Managed Agents

Quelle: Corey Ganim + Nick (BZAC), X-Video, 2026-04-09
Artefakt: `reels/20260411_151641_2042613085672812544.json`

## Was es ist
Platform-as-a-Service für AI Agents auf Anthropic-Stack.
Entkoppelt: **Harness (Claude Code)** ↔ **Tools / Sessions / Sandbox / Orchestration**.
Deploy via neuer CLI (`ant`) oder Web-Console `platform.claude.com`.
Kein eigenes Infra-Management nötig.

## Pricing-Modell
- Token-as-a-Service (normale API-Token-Kosten)
- **plus** Compute-Minuten für Agent-Runs auf Anthropic-Stack
- Beispiel aus Video: AI-Tools-Assessment-Agent → **$2,58/Run**

## Persona-Matrix
| Persona | Passt? | Begründung |
|---|---|---|
| Chat-User (Claude.ai) | Ja | Out-of-the-box Ergebnisse, non-technical |
| Claude Code User | Ja | Flexibilität + Reuse, CLI-affin → Hauptzielgruppe |
| Agent SDK Power-User | Nein | Will eigene Infra + volle Kontrolle |
| AI Tinkerer / Solopreneur | Nein | Zu teuer, Claude Code Subscription besser |

## Relevanz für GetKiAgent

**Jetzt: Skip.** Pipeline läuft auf n8n + lokalen Python-Scripts → klassischer "eigene Infra"-Case, bleibt günstiger.

**Wiedervorlage sobald:**
- Erster zahlender Pilot läuft
- Bezahlter Deliverable isolierbar (z.B. AI-Audit, Custom-Support-Agent als Service-Package)
- Dann: Token-Kosten durchreichen, Marge bleibt trivial bei Setup-Preisen >€2k

## Faustregel
Managed Agents nur wirtschaftlich, wenn Agent **direkt Kundenumsatz** generiert.
Für internes Housekeeping (Lead-Scoring, Outreach-Drafts) → eigene Infra bleibt Pflicht.
