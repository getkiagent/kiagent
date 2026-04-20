---
tags: [projekt/getkiagent, typ/wiki, typ/analyse, thema/claude-ecosystem, thema/tokens, thema/agents]
related: [[index]], [[claude-code-stack-optimierung]], [[claude-managed-agents]], [[architecture]]
source: 12 X-Posts (2026-04-04 bis 2026-04-20), reels/2026-04-20.md, 3 parallele Deep-Research-Runs
status: Analyse-Snapshot, teilweise nicht verifiziert
---

# Claude-Ecosystem Deep Dive (Stand 2026-04-20)

Konsolidierte Analyse aus 10 unique X-Posts + ~30 referenzierten Repos/Tools/Features. Gegliedert nach: (1) Faktencheck zu Social-Media-Hype, (2) Immediate Actions, (3) Future Ideas, (4) Skip-Liste mit Begründung.

Die Einzel-Einträge pro Post liegen in `reels/2026-04-20.md`.

---

## 0 — Faktencheck: Social-Media-Claims vs. Anthropic-Realität

Drei Claims aus den Posts haben sich in der Recherche als übertrieben oder falsch herausgestellt. Wichtig, weil wir fast eine "95%-less-tokens"-Botschaft in Outreach-Narrative übernommen hätten.

| Claim im Post | Realität laut Anthropic/Community |
|---|---|
| "Opus 4.7 — 95% less token usage" (0xMarioNawfal) | **Präzisierung:** Claim bezieht sich auf 4.7 **in Kombination mit dem offiziellen Memory-Tool** (`memory_20250818`), nicht auf 4.7 intrinsisch. Pro Einzel-Call verbraucht 4.7 durch neuen Tokenizer 0–35% MEHR als 4.6. Aber: bei Multi-Session-Workflows mit Memory-Tool lädt Claude via `view`/`view_range` just-in-time nur relevante Memory-Files statt ganze Conversation im Context → 95% effektive Ersparnis plausibel |
| "Opus 4.7 — no context limits" (0xMarioNawfal) | Falsch. Context bleibt 1M, max output 128k. „Effektiv kein Limit" gilt nur in Verbindung mit Memory-Tool + Compaction, wo Historie ausgelagert wird |
| "Permanent memory" built-in | Präzisierung: Memory-Tool ist Client-side. Anthropic liefert Protocol (`memory_20250818`), Persistenz muss selbst implementiert werden (File, SQLite, Cloud). Default-Pfad im Beispiel: `/memories/*.xml` |
| "18-min tutorial with motion.size.ai" | Tool heißt **motion.dev** (nicht motion.size.ai). AI-Kit via MCP, 330+ Animation-Examples |
| "Head of Claude Code Boris Turnie" (Movez) | Heißt **Boris Cherny**, nicht Turnie |
| "15 free guides" (Ruben Hassid) | Tatsächlich **17 Guides**, gelistet auf ruben.substack.com/p/claude |

**Regel daraus:** Vor jedem Reel-Derivat-Outreach-Claim → Anthropic-Primärquelle checken. Siehe Lessons-Eintrag 2026-04-20.

---

## 1 — Immediate Actions (diese Woche umsetzen)

Alle fünf sind niedriger Aufwand, messbarer Hebel, kein neues Produkt.

### A1. `/claude-api migrate this project to claude-opus-4-7`
Skill ist in Claude Code gebündelt. Aktualisiert Model-IDs, entfernt nicht mehr unterstützte Parameter (`temperature`, `top_p`, `top_k` erzeugen in 4.7 einen 400-Error), kalibriert Effort-Settings, ersetzt Extended-Thinking durch Adaptive-Thinking.

- Anwenden auf: `scripts/discover_leads.py`, `scripts/generate_outreach.py`, `tools/summarize_reel.py`, `tools/process_reel.py`
- Coverage: ~90% automatisch; Rest manueller Review
- **Vorsicht:** 4.7 verbraucht bis 35% mehr Tokens als 4.6. Nach Migration `max_tokens`-Werte und monatliches Budget re-checken

### A2. ccusage installieren — Baseline-Messung vor jeder Optimierung
```
npx ccusage@latest
```
Zero-install. Liest lokale JSONL und zeigt Tokens pro Session/Project/Subagent. Ohne Baseline keine Aussage über Caveman-Ersparnis oder 4.7-Mehrverbrauch.

### A3. Caveman-Skill installieren (Output-Compression)
Höchster unmittelbarer Hebel in Claude-Code-Sessions. Zwingt Output zu fragmentarischer Caveman-Sprache. 65% Ø Output-Savings laut Community-Tests.

```
claude plugin marketplace add JuliusBrussee/caveman
claude plugin install caveman@caveman
```
In `.claude/CLAUDE.md` initial `caveman: lite` setzen (Grammatik bleibt, spart ~40%). Bei heavy Dev-Sessions `caveman: full`. Repo: github.com/JuliusBrussee/caveman

### A4. n8n-MCP installieren
`github.com/czlonkowski/n8n-mcp` — MCP-Server für 1.505 n8n-Nodes, 2.709 Templates. Eliminiert den in `.claude/rules/n8n-workflows.md` dokumentierten Quirk, dass `create_workflow_from_code` bei inline Credentials scheitert.

Erwarteter Hebel: Jede n8n-Änderung 30–50% schneller, weil Claude die Node-Configs strukturiert lesen und validieren kann.

### A5. claude.ai-Project "GetKiAgent Strategy" anlegen
Projects sind Web-App-Container mit Knowledge-Files. Bisher ungenutzt.

- ICP-Dokumente, Pricing-Regeln, Wave-1-Results als Knowledge-Files
- Strategische Fragen im Web-UI ohne jedes Mal Kontext zu pasten
- Ergänzt (nicht ersetzt) Claude-Code-CLI-Skills

---

## 2 — Token-Effizienz Toolbox (Top 10 aus DataChaz + Indu Tripathi)

Beide Threads überlappen zu ~70%. Die 10 konsolidierten Tools, mit Relevanz-Einstufung für GetKiAgent.

| # | Tool | Mechanismus | Einstufung | Repo |
|---|---|---|---|---|
| 1 | Caveman | Output-Caveman-Sprache, 65% Ø Savings | **JETZT** | JuliusBrussee/caveman |
| 2 | ccusage | Messung pro Session | **JETZT** | ryoppippi/ccusage |
| 3 | Token Optimizer | Ghost-Tokens, Delta-Mode (97%) | JETZT (Lizenz check) | alexgreensh/token-optimizer |
| 4 | claude-mem | 3-Layer-Retrieval, ~10× Savings Cross-Session | JETZT (A/B ggü. bestehendem Skill) | thedotmack/claude-mem |
| 5 | context-mode | MCP-Tool-Output in Sandbox → Summaries | **JETZT** | mksglu/context-mode |
| 6 | MCPlex | MCP-Gateway, -96.9% tools/list-Payload | JETZT (8+ MCP aktiv) | modernops888/mcplex |
| 7 | RTK | Hook-Proxy filtert CLI-Output | SPÄTER | rtk-ai/rtk |
| 8 | Superpowers | Progressive Skill-Disclosure | SPÄTER (Coding-heavy) | obra/superpowers |
| 9 | Repomix | Codebase-Packing mit Tree-Sitter | NICHT-RELEVANT (kein Codebase-Feed) | yamadashy/repomix |
| 10 | MCP-Context-Provider + Memory-Service | Rule-based Contexts + SQLite+Vector Memory | SPÄTER (Overlap claude-mem) | doobidoo/* |

**Lizenz-Warnung:** Token Optimizer ist PolyForm NonCommercial. Für interne Dev-Arbeit erlaubt, bei kommerzieller Kundennutzung riskant.

**Reality-Check:** 65%-Output-Savings ≠ 65%-Rechnung-weniger. In echten Coding-Sessions mit Input-Context eher 25–30% Gesamt-Ersparnis. Trotzdem signifikant pre-revenue.

---

## 3 — Claude Code Ecosystem (Suryansh, kaize, Nawfal)

### 3.1 `affaan-m/everything-claude-code` — "Most Complete Setup"
27 Agents · 64 Skills · 33 Commands · AgentShield (1.282 Security-Tests)

- **Agents:** planner, architect, tdd-guide, code-reviewer, security-reviewer, build-error-resolver, e2e-runner, refactor-cleaner, doc-updater, docs-lookup, chief-of-staff, loop-operator, harness-optimizer + Sprach-Reviewer für Python, TS, Go, Rust, C++, Java, Kotlin, Swift, PyTorch
- **Skills:** tdd-workflow, security-review, backend/frontend-patterns, e2e-testing, verification-loop, eval-harness, strategic-compact, content-engine, market-research, investor-materials, investor-outreach, videodb, security-scan, mcp-server-patterns
- **Commands:** /tdd, /plan, /code-review, /build-fix, /e2e, /refactor-clean, /checkpoint, /verify, /eval, /update-docs, /skill-create, /instinct-status, /pm2, /multi-plan, /multi-execute, /orchestrate, /quality-gate, /model-route, /harness-audit
- **AgentShield:** 14 Secret-Patterns, Permission-Audit, Hook-Injection-Analyse, MCP-Risk-Profiling, Agent-Config-Review. Mit `--opus` Flag spawnen 3 Opus-Agents für Red-Team-Adversarial-Scan.

**Bewertung GetKiAgent:**
- **Jetzt nur AgentShield-Modul ziehen** für einmaligen Scan über `.claude/`, `scripts/`, `intel/` — wir hosten Kunden-Outreach-Daten (`apollo-raw-beauty-2026-04-19.json`), 14 Secret-Patterns fangen `.env`-Leaks ab, die ich heute nur per Eye-Ball prüfe
- **Full Harness erst ab €3–5k MRR** oder bei 2. Produkt (DACHGuard-Reaktivierung)

### 3.2 `nextlevelbuilder/ui-ux-pro-max-skill`
67 UI-Styles · 161 Color-Palettes · 57 Font-Pairings · 99 UX-Rules · 161 Industry-Reasoning-Regeln · 15 Tech-Stacks.

**Bewertung:** Website-v2 ist in Arbeit. Eine Session mit B2B-SaaS-Style + passender Palette ersetzt eine halbtägige Design-Loop. **Immediate Action Kandidat**, Priorität nach A1–A5.

### 3.3 `thedotmack/claude-mem`
SQLite + Chroma-Vector-DB, 4 MCP-Tools, Web-UI auf localhost:37777, `<private>`-Tags.

**Bewertung:** A/B gegen meinen bestehenden `claude-mem`-Skill testen. Wenn sauberer: migrieren. Relevanz besonders für Outreach-Agent-Continuity Wave-1 → Wave-2 → Wave-3.

### 3.4 Weitere Repos aus Suryanshs Liste
- **hkuds/lightrag** — Graph+Vector RAG für Codebase-Verständnis. Relevant ab ~10k LoC oder Shopify-App (DACHGuard). **FUTURE.**
- **FlorianBruniaux/claude-code-ultimate-guide** — 23k Zeilen Docs + 271 Quizzes. **SKIP**, Lernmaterial nicht Operativwissen.
- **VoltAgent/awesome-agent-skills** — 1.000+ Skills. Fundgrube für spezifische Skills (z.B. pdf-compliance für DACHGuard). **FUTURE.**
- **mbailey/voicemode** — Whisper+Kokoro Voice-Dialog. **SKIP**, Gimmick ohne Business-Hebel.

### 3.5 Skill-Sammlungen aus Mario Nawfals "full developer"-Thread
- **ComposioHQ/awesome-claude-skills** — Composio-kuratiert. Wir nutzen Composio MCP bereits (siehe Memory-Entry) → natürliche Fundgrube für weitere Skills
- **coreyhaines31/marketingskills** — 23 Marketing-Skills (SEO, Copy, CRO). **FUTURE**, aktivieren sobald wir auf Inbound/SEO/Content umschalten
- **kepano/obsidian-skills** — Obsidian-Bridge (Markdown, Bases, JSON-Canvas). Relevant wenn Vault-Struktur komplexer wird
- **anthropics/skills** — offizielle Skills, baseline
- **walidboulanouar/Ay-Skills** — 10 Production-Skills (SEO, Browser, Video, Diagrams)

### 3.6 Aus kaize's "Week 2 — 10 MORE repos"
Nicht 1:1 verifizierbar (Thread paywalled). Wahrscheinliche Treffer:
- `github/github-mcp-server` — offizieller GitHub-MCP
- `steipete/claude-code-mcp` — Claude Code als MCP für parallele Sub-Agents
- `zilliztech/claude-context` — Semantic Code Search via Vector Embeddings
- `agent-0x/claude-recall` — Repetitive Workflows → Skills

**Alle FUTURE**, keine unmittelbare Wave-2-Relevanz.

---

## 4 — Opus 4.7 Features in Zahlen

Release 2026-04-16. Wichtig für die Migration:

| Feature | Status | GetKiAgent-Implikation |
|---|---|---|
| Adaptive Thinking | Pflicht, kein `budget_tokens` mehr (400-Error) | Scripts mit explizitem `budget_tokens` müssen gefixt werden |
| `xhigh` Effort-Level | Neu, zwischen high und max | Für komplexe Plan-Sessions nutzbar, teurer |
| Task Budgets (Beta) | Beta-Header `task-budgets-2026-03-13` | FUTURE: advisory Token-Cap in Discovery-Pipeline |
| Temperature/top_p/top_k | 400-Error in 4.7 | Aus allen API-Calls entfernen |
| High-Res Images | bis 2576px | Relevant falls wir Produkt-Screenshots analysieren |
| Memory-Tool | File-system-basiert | FUTURE für Support-Produkt |
| Tokenizer-Änderung | +0–35% Tokens ggü. 4.6 | Max_tokens und Budget-Alerts anpassen |

---

## 5 — Claude Design + motion.dev für website-v2

`claude.ai/design` ist Anthropics neues AI-Design-Tool. Generiert Code statt Pixel — Output ist lauffähiges HTML/CSS/JS. Kann animierte Landing-Pages, Slide-Decks, Design-Systeme im Liquid-Glass-Stil, 3D, Particle-Effekte.

Ergänzung: **motion.dev AI-Kit** als MCP-Server mit 330+ Animation-Examples. GSAP + AI-Video-Gen ist der Stack-Standard für "award-style" Sites.

**Limits:** Export als Video noch nicht möglich (Screen-Recording-Workaround). Code ist manuell tweakbar. Kosten: <$10 API-Credits pro Landing laut Tutorials.

**Bewertung:** Wenn website-v2 aktuell statisch ist → Claude Design + motion.dev MCP könnte eine scroll-animierte Hero-Section in 1–2h generieren. Wirkung bei DACH-E-Commerce-Prospects potenziell hoch (viele deutsche SaaS-Landings sind statisch/nüchtern → Differenzierung). Priorität niedrig aber cheap, nach A1–A5.

---

## 6 — Prompts vs Projects vs Skills (Primitive-Klärung)

Ruben Hassids Framing (Prompts = stranger, Projects = binder, Skills = trained employee) ist prägnant, aber die Engineering-Zuordnung ist die wichtigere:

| Primitiv | Wo | Persistenz | GetKiAgent-Status |
|---|---|---|---|
| **Prompt** | Überall | keine | Standard im API |
| **Project** | claude.ai Web + Desktop Cowork | pro Projekt | **ungenutzt** |
| **Skill** | Claude Code CLI + Cowork + API | wiederverwendbar | Aktiv (`pipeline`, `niche-explorer`, `quality-gate`, `claude-mem`) |

**Lücke:** Claude Projects im Web-UI ist komplett ungenutzt. Immediate Action A5 adressiert das.

---

## 7 — Boris Cherny Podcast — 7 strategische Takeaways

1. **"Software Engineer" → "Builder"** (Cherny prognostiziert Titel-Verschwinden bis Ende 2026). Framing-Test für Wave-2-Outreach: "Builder statt Dev-Team" als Positionierung.
2. **Underfunded Teams + unlimited Tokens → bessere Produkte.** Kleine Teams mit Rechenzeit schlagen große mit Budget. Lean bleiben, Token-Spend ist nicht das Limit (nach Optimierung).
3. **100% AI-Code seit Nov 2025.** Cherny editiert keine Zeile manuell. Soziale Permission, das Pattern auch in unserer Pipeline zu normalisieren.
4. **Claude Code = 4% aller Public-GitHub-Commits.** Brauchbar als Stat in Outreach-Mails.
5. **"Build for the 1% power user"** — Power-User halten das Produkt am Leben, Mass-Adoption folgt. Wave-1/2-Strategie: erste 7 Tier-A-Prospects über Qualität begeistern, nicht Menge skalieren.
6. **Latent Demand shaped Claude Code + Cowork** — User wollten beides, niemand fragte. Signal: DACH-Commerce-Kunden-Interviews jetzt, nicht nach Wave 2.
7. **"Coding is solved"** — Chernys These. Implikation: Unser Pricing-Narrativ "wir bauen euch was Custom" erodiert langfristig. Positionierung muss auf **Domain-Expertise + Integration-Pain** (n8n, Shopify, DACH-Compliance) statt "wir coden" lenken.

Long-Form-Summaries: lennysnewsletter.com, waydev.co.

---

## 8 — Ruben Hassids 17 Guides — Kuratierte Picks

Nur drei sind für unseren Stack wirklich relevant:

- **#3 Claude Skills** — Skill-Creator-Walkthrough, 7 Hacks — relevant für bessere Skill-Designs
- **#12 Claude to Sound Like You** — Voice/Tone-Training via Text-Files — relevant für Outreach-Stimme-Konsistenz
- **#17 I Am Just a Text File** — Markdown-Context-File-Pattern, validiert das CLAUDE.md-Muster

Rest (Claude in Excel, 1M Followers, Nano Banana 2, Cowork) = B2C-Noise für unseren Use-Case.

---

## 9 — Future Ideas: noch nicht relevant, aber merken

Geordnet nach Trigger-Bedingung.

### 9.1 Trigger: €3–5k MRR oder DACHGuard-Reaktivierung
- **everything-claude-code Full Harness** (27 Agents, 64 Skills, 33 Commands) — sobald Pipeline skaliert oder 2. Produkt beginnt
- **Memory-Tool für Kundenservice-Bot-Produkt** — Multi-Session-Context pro Endkunde (Order-History, Sprach-Präferenz, Support-History). Passt thematisch zu DACHGuard-Timing
- **Claude Skills als Kundendeliverable** — bei Agency-Onboarding liefern wir vordefinierte Skills (Lead-Scoring, Reply-Drafting) als fertiges Paket → Pricing-Hebel

### 9.2 Trigger: Wave 3+ oder Multi-Niche-Parallelisierung
- **steipete/claude-code-mcp** — parallele Claude-Instanzen als MCP, für paralleles Scraping/Scoring mehrerer Nischen
- **Task Budgets (Beta)** in Discovery-Pipeline — advisory Token-Cap verhindert Runaway-Costs bei großen Niche-Scrapes

### 9.3 Trigger: Pivot auf Inbound/SEO/Content
- **coreyhaines31/marketingskills** — 23 Marketing-Skills (SEO, Copy, CRO)
- **1M-Followers-with-AI-Playbook** (Ruben #7) — falls wir Content-Distribution starten
- **Claude Design für Content-Ops** — Slide-Decks für Sales, Demo-Animationen

### 9.4 Trigger: Shopify-App / echte Code-Engineering
- **hkuds/lightrag** — Codebase-RAG ab ~10k LoC
- **obra/superpowers** — TDD-Phasen-Enforcement
- **zilliztech/claude-context** — Semantic Code Search via Vector Embeddings
- **yamadashy/repomix** — Codebase-Packing für externe Model-Reviews

### 9.5 Trigger: Vault-Komplexität wächst
- **kepano/obsidian-skills** — Markdown/Bases/JSON-Canvas direkt in Claude verfügbar
- **doobidoo/mcp-memory-service** — SQLite+Vector-Memory, wenn claude-mem nicht reicht

### 9.6 Strategisches Watch-List
- **Opus-4.8-Release** (typischer Cycle ~2–3 Monate nach 4.7) — neue Migration nötig
- **Claude Cowork** (Web-App, Post-April) — wenn Team wächst oder externer Co-Worker einsteigt
- **claude.ai/design Video-Export** — aktuell nur Screen-Recording-Workaround

---

## 10 — Skip-Liste mit Begründung

- **anthropics/claude-code (Repo selbst)** — wir nutzen es, keine Aktion
- **jeffallan/claude-skills** — Full-Stack-Dev-fokussiert, Bottleneck ist Outreach nicht Coding
- **langgenius/dify, FlowiseAI, onyx** — alternative Agent-Plattformen, n8n-Wechsel wäre Scope-Explosion
- **VoltAgent/awesome-agent-skills als Ganzes** — 1.200+ Skills = Noise ohne konkreten Use-Case (gezielt greifen, nicht sammeln)
- **mbailey/voicemode** — Voice-Gimmick
- **FlorianBruniaux/claude-code-ultimate-guide** — Lernmaterial nicht Operativwissen
- **yamadashy/repomix** — kein Codebase-Feed in unserer Pipeline

---

## 11 — Wie weiter

1. **Diese Woche:** A1–A5 umsetzen, Baseline mit ccusage, Caveman aktivieren, n8n-MCP installieren, Claude-Project anlegen
2. **Nach Wave 2 Launch:** AgentShield-Scan, ui-ux-pro-max für website-v2
3. **Monatlich:** Diese Analyse-Seite auf veraltete Claims prüfen (besonders Tokenizer-Kosten, neue Anthropic-Features)
4. **Bei jedem neuen Reel-Claim über Anthropic-Features:** Primärquelle gegen-checken (siehe Lessons 2026-04-20)

## Quellen

Alle Detail-Quellen in den drei parallelen Deep-Research-Agent-Outputs vom 2026-04-20 (nicht persistiert). Primärlinks:

- Anthropic Docs: `platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7`
- Migration Guide: `platform.claude.com/docs/en/about-claude/models/migration-guide`
- Motion AI Kit: `motion.dev/docs/ai-kit`
- Ruben-Guides-Hub: `ruben.substack.com/p/claude`
- Lennys Newsletter Cherny: `lennysnewsletter.com/p/head-of-claude-code-what-happens`
- Finout "Real Cost Story": `finout.io/blog/claude-opus-4.7-pricing`
- Alle genannten Repos: direkt github.com/<owner>/<repo>
