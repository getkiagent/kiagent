# I2 — Solo-No-Code-Build mit Shopify AI Toolkit + Claude Code

**Date:** 2026-04-17
**Agent:** A1
**Focus:** Ist ein vollständiger Shopify-App-Build mit Claude Code + Shopify AI Toolkit realistisch für einen DACH-Solo-No-Code-Operator mit AI-Fluency aber ohne Coding-Background?

---

## Executive Summary

**Kurz: Ja, aber mit Asterisk.** Der Shopify AI Toolkit (offiziell launched 9. April 2026) macht Checkout UI Extensions, Shopify Functions, Admin-Apps und Polaris-Dashboards für Non-Coder realistisch baubar. TinyTwo's ReviewMate beweist 87-Tage-End-to-End-Production-App mit Claude Code. ABER: "Non-Coder" muss GraphQL lesen können, OAuth-Flow verstehen, Webhook-Logs debuggen und Polaris-Pattern-Matching betreiben. Reines No-Code ist es nicht.

**Für Ilias:** Der realistische Stack ist **Claude Code + Shopify AI Toolkit + Gadget.dev**. Gadget.dev übernimmt Infrastructure (Hosting, Scaling, Auth, Webhooks, Billing-Wiring) als Managed-Backend, Claude Code + AI Toolkit handeln Code-Generation und Shopify-API-Verständnis. Solo-MVP-Timeline für eine Checkout-Extension-App realistisch **8-14 Wochen**, für komplexe Analytics-App 16-22 Wochen.

**Nicht-buildable solo-no-code** (mit aktuellem Stack): Multi-tenant Daten-Pipelines mit Stream-Processing, komplexe Background-Job-Queues mit Fan-Out, Custom-Payment-Gateways, Enterprise-SLA-Apps.

---

## Stack-Layer-Überblick

### Layer 1 — Shopify AI Toolkit (April 2026)

**Was es ist:** Offizieller Open-Source MCP-Server + Plugin-System. Vor dem Launch hieß die Alpha-Version "dev-mcp", jetzt heißt das Plugin-Bundle `shopify-ai-toolkit`. Ships mit 16 Skill-Files.

**Install:**
```
/plugin marketplace add Shopify/shopify-ai-toolkit
/plugin install shopify-plugin@shopify-ai-toolkit
```

**7 Core-Tools (dokumentiert):**

1. `learn_shopify_api` — Platform-Orientierung
2. `search_docs_chunks` — Docs-Query
3. `fetch_full_docs` — Full-Docs-Retrieval
4. `introspect_graphql_schema` — Live-Schema (2.796+ Types)
5. `validate_graphql_codeblocks` — Queries vor Deployment prüfen
6. `validate_component_codeblocks` — Hydrogen-Component-Syntax
7. `validate_theme_codeblocks` — Liquid-Theme-Code

**Skill-Areas (dokumentierte aus mehreren Quellen — vollständige 16er-Liste nicht öffentlich enumerated, aber Themen klar):**

- Admin operations
- Product management
- Liquid themes
- Hydrogen storefronts
- Shopify Functions
- Partner tools (App-Creation-Primitives)
- `shopify-admin-execution` (live-store-Changes)
- Checkout UI Extensions
- Customer Account Extensions
- Metafields / Metaobjects
- Webhooks (scaffolding + validation)
- GraphQL Admin API queries/mutations
- Polaris components
- TOML app config
- App billing
- OAuth + session token patterns

**Unterstützte Clients:** Claude Code, OpenAI Codex, Cursor, Gemini CLI, VS Code.

**Kritische Limitation:** Das Toolkit ist explizit ein **Developer-Tool**. Es tut NICHT:

- Konversationelles Store-Management (Preise ändern, Orders anzeigen) — dafür ist Sidekick gedacht
- Store-Daten-Zugriff, Collections lesen, Produkte erstellen via MCP-Admin ohne zusätzlichen Community-MCP-Server mit Access-Token
- Undo/Rollback (Delete-Operationen sind permanent)
- Confirmation-Dialogs vor Execution

### Layer 2 — Claude Code

**Rolle:** Code-Generation-Driver. TinyTwo's ReviewMate wurde zu 95%+ von Claude AI (Opus-Vorgänger-Serie 2025) geschrieben. Menschen-Anteil: Produktvision, Testing/QA, Deployment-Entscheidungen, UX-Validation.

**Realistisches Capability-Set für No-Coder:**

Claude Code kann selbständig:
- OAuth + Token-Exchange-Flow scaffolden
- HMAC-Webhook-Verification einbauen (ohne explizite Instruktion)
- XSS-Protection-Patterns anwenden
- Database-Schema entwerfen (Prisma-Migrations)
- GraphQL-Queries gegen Live-Schema validieren (via AI Toolkit)
- Polaris-Components konsistent rendern
- Billing-API-Integration konfigurieren
- Mandatory Privacy Webhooks implementieren

Claude Code braucht Mensch-Input bei:
- Product-Vision ("Was soll die App tatsächlich tun")
- Edge-Case-Testing (Checkout mit 80+ Line-Items, Timeout-Szenarien)
- Deployment-Decision (Fly.io vs Vercel vs Railway)
- UX-Validation (Macht der Flow Sinn?)
- Support-Response (kein AI-Vollersatz)

### Layer 3 — Gadget.dev (empfohlene Infrastructure-Abstraktion)

**Problem, das Gadget.dev löst:** Shopify-App-Hosting + Auth + Webhook-Registration + Billing-Wiring + Scaling ist für Solo-No-Coder der größte Pain. Fly.io/Railway/Vercel + Postgres + Redis + Cron manuell zu orchestrieren bricht die Illusion "nur Claude Code".

**Was Gadget.dev liefert:**

- Auto-generated CRUD-API
- Built-in Shopify OAuth + session token handling
- Webhook-Subscriptions automatisch registriert via TOML
- File-based routing (Remix-kompatibel)
- Managed Postgres + Background-Jobs + Cron
- App-Store-Deploy-Pipeline

**2026-Stand:** Gadget.dev + Remix wurde durch **Gadget.dev + React Router v7** ersetzt (April 2025 Shopify CLI-Änderung). Codebase ist praktisch identisch weil React Router v7 = Remix.

**Trade-off:** Vendor-Lock-in bei Gadget. Exit-Weg existiert aber (Gadget exportiert Code). Pricing: ab $75/mo beim Start.

### Layer 4 — Shopify CLI + Remix/React-Router-v7-Template

**Alternative zu Gadget:** Offizielles `shopify-app-template-remix` + eigenes Hosting. Mehr Kontrolle, aber No-Coder muss:

- Hosting-Provider wählen und konfigurieren
- Postgres-Instanz provisionieren
- Webhook-Registration manuell synchronisieren
- SSL-Zertifikate
- Log-Aggregation

Für einen AI-Tool-fluent Non-Coder ist das machbar mit Claude Code aber 30-50% mehr Zeit. **Gadget.dev ist für Solo-DACH-Operator die bessere Wahl.**

---

## Case Study: TinyTwo ReviewMate (87-Tage-End-to-End)

### Fakten

- **Dauer:** 87 Tage (10.06.-05.09.2025)
- **Arbeitszeit:** ~300h über 3 Monate
- **Kosten:** "<$5k" laut Autor (versus traditionelle Dev-Schätzung $50k+)
- **Ergebnis:** Production-App mit 200+ Merchants, Tausende Reviews pro Monat
- **AI-Anteil:** "95%+ aller Code generiert von Claude AI"

### Tech Stack

- Frontend: React 18.2, Remix 2.16, TypeScript 5.2, Shopify Polaris 12
- Backend: Node.js 18+, Prisma 6.2, PostgreSQL, GraphQL
- Infrastructure: Docker, Fly.io, Cloudflare R2 (Bilder/Videos), Redis Queue, BullMQ, Resend (Email)

### Implementierte Features

- Review-Collection + Display
- GDPR-Compliance inklusive Customer-Redact
- Orders-Paid-Webhook-Subscription-System (trigger Review-Request-Mails)
- Subscription + Billing via Shopify Billing API
- Media-Upload (Images + Videos) mit R2-Storage
- Multi-Language (DACH-relevant)

### Non-Coder-Learnings aus dem 14-teiligen Medium-Series

**Was Claude selbständig gemacht hat:**
- HMAC-Webhook-Verification (ohne Prompt-Aufforderung)
- XSS-Protection-Patterns
- Prisma-Schema-Design + Migrations
- Polaris-Component-Matching
- Billing-Flow-Scaffolding

**Was TinyTwo (Entwickler mit Background) manuell verifizieren musste:**
- Extension-Responsive-Design (Mobile-Edge-Cases) — explizit als "hidden challenge" gelabelled
- Database-Queries-Performance bei Skalierung
- Webhook-Delivery-Failure-Retry-Logic
- Production-Deployment-Strategie

**Für Ilias interpretiert:** TinyTwo hatte vermutlich Software-Engineering-Background (stack/Wortwahl deuten darauf hin). Ein echter Non-Coder mit AI-Fluency braucht realistisch **1,3-1,5x die Zeit** — also **110-130 Tage** für vergleichbar komplexe App, bei vergleichbarem Pensum.

**Risiko, das TinyTwo unterschlägt:** Production-Readiness-Claim ist nicht gleich BFS-Badge. 200+ Merchants sind aus Solo-Dev-Sicht exzellent, aber ob ReviewMate alle BFS-Performance-Kriterien (<500ms P95 Dashboard-Load, 1.000+ Requests in 28 Tagen) erfüllt, ist nicht dokumentiert.

---

## Was ein Non-Coder realistisch können MUSS

Reines No-Code ist Marketing-Sprech. Diese Skills bleiben nötig:

### Must-Have (nicht delegierbar)

1. **GraphQL lesen (nicht schreiben)** — Verstehen welche Felder eine Query zurückgibt, wo Typos Fehler verursachen. Shopify Admin API 2025-10 = 2.796+ GraphQL Types. AI Toolkit macht Introspection, aber man muss Claude-Outputs lesen.

2. **JSON/TOML Config** — `shopify.app.toml` editieren, Webhooks registrieren, Scopes definieren, Extensions-Targets setzen.

3. **OAuth-Flow-Mental-Model** — Muss verstehen: App-Install → Merchant-Authorize → Access-Token → Session-Token-Refresh. Sonst Debug unmöglich bei Auth-Failures.

4. **Prompt-Iteration** — Wissen, wann Claude auf dem falschen Pfad ist, wie man es redirected, wie man Context-Window-Grenzen managed.

5. **Git-Basics** — Commit, Branch, Revert. Ohne Git verlierst du Arbeit. Claude Code kann git aufrufen, aber der Operator trifft Merge-Entscheidungen.

6. **CLI/Terminal-Basics** — Shopify CLI nutzen (`shopify app dev`, `shopify app deploy`). Terminal ist nicht vermeidbar.

7. **Fehler-Logs-Lesen** — Wenn Webhook failed, muss man Fly.io/Gadget-Logs interpretieren. Claude hilft beim Lesen aber nicht immer ohne gezielten Prompt.

### Nice-to-Have (beschleunigt drastisch)

- Basic HTTP/REST-Verständnis (Status-Codes 401 vs 403 vs 500)
- Database-Mental-Model (was ist eine Migration, warum kann man keine Column-Löschung rückgängig machen)
- Frontend-vs-Backend-Trennung (welche Code-Teile laufen wo)

### NICHT nötig (wird von AI-Toolkit + Claude abgedeckt)

- TypeScript-Syntax beherrschen
- React-Hooks im Detail verstehen
- Prisma-ORM-Patterns
- WebAssembly/Rust für Functions
- Polaris-Design-System-Details
- Shopify-spezifische Security-Patterns

---

## Was ist AI-Toolkit-buildable, was nicht

### Grün (baubar solo-no-code mit Claude + AI Toolkit + Gadget.dev)

| App-Typ | Realistic Weeks | Kommentar |
|---|---|---|
| Checkout UI Extension (Loyalty/Upsell/Banner) | 4-10 | AI-Toolkit-Skill checkout-ui-extensions deckt komplett ab |
| Shopify Functions (Discount/Shipping/Payment-Customization) | 6-12 | Functions-Skill + Validation-Tool |
| Theme App Extension | 3-6 | Liquid-Validator erleichtert |
| Admin UI App (Polaris Dashboard + Simple CRUD) | 8-14 | Polaris-Component-Skill |
| Webhook-driven Background-App (Email-Trigger, Notification) | 6-12 | Standardmuster |
| Metafield-Editor/Config-App | 4-8 | Metafield-Skill |
| Customer Account UI Extension | 5-10 | Ähnlich Checkout-UIEx |

### Gelb (möglich aber Time-Multiplier 1,5-2x, Tech-Debt-Risiko)

| App-Typ | Grund |
|---|---|
| Analytics/Attribution mit Multi-Touch-Modelling | Daten-Pipeline-Komplexität übersteigt AI-Toolkit-Scope |
| Multi-Store-Sync / Headless | Infrastructure-Multi-Tenant-Patterns |
| Complex Subscription-Engine (Prorations, Partial-Refunds) | Edge-Cases in Billing-Logic |
| Review-App mit Moderation-Queue + Spam-ML | ML-Pipeline ausserhalb AI-Toolkit |

### Rot (nicht realistisch solo-no-code)

| App-Typ | Grund |
|---|---|
| Custom Payment Gateway | Regulatorik, Crypto-Signatures, PCI-Scope |
| Enterprise Accounting/ERP-Sync mit 10+ Systems | Orchestration-Komplexität |
| Real-time Video/Livestream-Commerce | Infrastructure-Sophistication |
| WMS/OMS mit physischer Barcode-Scanner-Integration | Hardware + Durchsatz |
| Search-Engine mit eigenem ML-Ranking | Ausserhalb Shopify-API-Paradigma |

---

## Realistische Build-Zeit: einzelne App vs Portfolio

### Einzelne App (First Build)

Für einen DACH-AI-Fluent-Non-Coder, erste Shopify-App:

| Phase | Optimistisch | Konservativ |
|---|---|---|
| Setup (Partner-Account, CLI, AI Toolkit Install, Gadget-Project) | 3 Tage | 1 Woche |
| Auth + Basic-Scaffolding + Polaris-Shell | 1 Woche | 2 Wochen |
| Core-Feature (z.B. Checkout-Extension-Surface) | 3 Wochen | 5 Wochen |
| Database + Webhooks + Background-Jobs | 2 Wochen | 4 Wochen |
| DACH-Compliance (TDDDG-Text, AVV-Template, Consent) | 1 Woche | 2 Wochen |
| App-Store-Listing + Review-Prep | 1 Woche | 2 Wochen |
| Shopify-Review-Zyklus (Warten + Nachbesserung) | 2 Wochen | 4 Wochen |
| **Total** | **10 Wochen** | **20 Wochen** |

**Bei TinyTwo (87 Tage): ~12,5 Wochen — mit Background.** Plus 30-50% für Non-Coder: **16-19 Wochen realistisch.**

### Portfolio-Mode (ab App 2)

Time-Savings durch Shared-Codebase:

- Auth + Polaris-Shell wiederverwendbar: 1 Woche statt 3
- Compliance-Templates wiederverwendbar: 2 Tage statt 1 Woche
- DevOps + Deployment-Pipeline vorhanden: 0 statt 1 Woche
- Testing-Patterns etabliert

**Realistisch: App 2 = 60-70% der Zeit von App 1. App 3+ = 50%.**

**Max Artemov-Vergleich:** 30 Mobile-Apps in 12 Monaten (2,5 Apps/Monat). Für Shopify-Apps wegen Shopify-Review-Cycle + App-Store-Compliance NICHT replizierbar. Realistisch für DACH-Solo: **3-6 Apps im ersten Jahr, davon 2-3 Tier-1-Fokus**.

---

## Production-Readiness: Kritische Gaps

### Risk 1 — AI-generated Code und Review-Approval

Shopify-App-Review-Team prüft:

- Performance (<500ms P95 Dashboard)
- Security (HMAC, CSRF, XSS)
- GDPR-Compliance (Privacy-Webhooks implementiert)
- GraphQL-only (keine deprecated REST)
- Design-Konsistenz (Polaris)
- App-Bridge-Version current

**AI-Toolkit + Claude decken das meiste ab**, aber:

- Performance-Testing unter Last muss manuell gemacht werden
- Security-Audit ist Mensch-Verantwortung
- Reviewer kommentiert manchmal subjektive UX — nur Mensch-Entscheidung

### Risk 2 — Debugging von AI-generated Code

Problem: Wenn Claude einen bug einführt, den er selbst nicht sieht, kann Endless-Loop-Risiko entstehen. TinyTwo's Part 12 ("10 Battle-Tested Tips") betont:

- "Tests first, code second" — aber das erfordert Test-Pattern-Verständnis
- Context-Window-Hygiene
- Plan-first, not code-first
- Rollback-Punkte definieren (via Git)

Für Non-Coder bedeutet das: **Bei Complex-Bugs nach 2-3 Runden Claude-Iteration Experten-Rate-Request** (z.B. paid Shopify Partner on Upwork oder Fiverr).

### Risk 3 — Mandatory Webhooks und Compliance

Shopify verlangt drei Privacy-Webhooks (customers/data_request, customers/redact, shop/redact). AI-Toolkit-Scaffolding deckt's ab, aber **Data-Handling-Policy (was passiert mit exportierten Daten, Retention, Audit-Log)** ist Legal-Arbeit. DACH-spezifisch:

- AVV-Template mit jedem Merchant
- DSFA (Datenschutz-Folgenabschätzung) bei sensiblen Daten
- TDDDG-Consent-Pattern im Checkout

**Kostenschätzung externe Legal-Review:** 2.500-5.000 EUR einmalig plus Quartals-Review.

### Risk 4 — Support-SLA

Shopify Technology Partner Track verlangt **30-Min-Response**. Solo machbar mit:

- Plain/Front/Help Scout als Ticket-System
- Timezone-aware-Schedule (DACH + US-Merchants)
- Escalation-Ladder (Tier-1 AI-assisted Replies, Tier-2 Mensch)
- Documented-FAQ + In-App-Help

**Nicht machbar:** Telefon-Support, Live-Chat 24/7, Plus-Enterprise-SLA.

---

## Empfohlener Stack für Ilias (konkrete Liste)

### Core-Stack

| Layer | Tool | Warum |
|---|---|---|
| AI-Pair-Programming | Claude Code (Sonnet default, Opus bei Architektur) | Bester Code-Quality + AI-Toolkit-Integration |
| Shopify-Platform-Access | Shopify AI Toolkit Plugin | Official, 7 Core-Tools + 16 Skills |
| Hosting/Backend | Gadget.dev | Managed-Infrastructure, OAuth, Webhooks |
| Frontend-Framework | Remix/React Router v7 (Gadget-default) | Shopify-empfohlen |
| UI-Library | Shopify Polaris (latest) | BFS-required |
| Database | Gadget-managed Postgres | Kein Ops-Overhead |
| Email-Transactional | Resend | Simple-API, cheap |
| Media-Storage | Cloudflare R2 | S3-compatible, cheap |
| Monitoring/Logs | Gadget built-in + Axiom | Debuggable |
| Support-Ticketing | Plain oder Front | Solo-tauglich |
| Legal-Template-Basis | Shopify Partner AVV-Template + DACH-Anwalts-Review | Pflicht |
| Payments-on-Merchant-Side | Shopify Billing API | Pflicht, keine Alternative |

### Dev-Tools-Layer

| Tool | Zweck |
|---|---|
| VS Code oder Cursor | Editor (Cursor + AI-Toolkit funktioniert auch) |
| Git + GitHub | Version Control, Private Repo |
| Shopify CLI | `shopify app dev`, `shopify app deploy` |
| Partner Dashboard | App-Registration, Billing, Analytics |
| Dev-Store (Partner-Account) | Testing-Sandbox |

### Build-Discipline-Stack (aus TinyTwo Part 12)

1. Plan-first (Markdown-Document vor Code)
2. Git-Commit alle 1-2h (Rollback-Fähigkeit)
3. Tests vor Features wo möglich
4. Context-Window-Hygiene (kein Monolith-Dumpen)
5. Wöchentlicher Progress-Review mit definierten Success-Criteria

---

## Alternative Stacks (bewertet)

| Alternative | Pro | Contra | Verdict |
|---|---|---|---|
| Shopify CLI + Eigenes Hosting (Railway/Fly.io) | Volle Kontrolle, billiger | Ops-Overhead, Scaling-Verantwortung | NEIN für Ilias |
| Gadget.dev allein (ohne AI Toolkit) | Einfacher Start | Fehlende Shopify-Docs-Introspection, mehr Prompt-Arbeit | NEIN |
| Reines Shopify Partner Dashboard + App Builder (falls es sowas gäbe) | Theoretisch No-Code | Existiert nicht für komplexe Apps | N/A |
| WordPress/WooCommerce | Nicht-Shopify | Unrelated | N/A |
| n8n als App-Backend | Vertraut für Ilias | n8n ist Workflow-Runner, nicht Shopify-App-Framework | NEIN |

**Einzige alternative sinnvolle Pfad:** Claude Code + Shopify CLI + Fly.io (ohne Gadget). 30% billiger, 40% mehr Zeitaufwand, höhere Debug-Wahrscheinlichkeit. Nicht empfohlen beim ersten App-Build.

---

## Konkrete 90-Tage-Build-Plan-Struktur

### Days 1-7: Foundation

- Shopify Partner Account + Dev-Store
- Claude Code + AI Toolkit Install
- Gadget.dev Account + erste App-Template-Generation
- Git-Repo + erster Commit
- App-Idea finalisieren (aus I1-Shortlist)

### Days 8-30: MVP-Core

- OAuth + Auth-Shell fertig
- Core-Feature-Surface (z.B. Checkout-Extension) funktional
- Basic-Polaris-Dashboard
- Erste Webhook-Subscription

### Days 31-60: Production-Features

- Billing-Integration (Shopify Billing API)
- Privacy-Webhooks (mandatory)
- DACH-Compliance-Layer (TDDDG-Consent, AVV-Template)
- Error-Handling + Logging

### Days 61-80: Polish + Review-Prep

- Polaris-Design-Audit
- Performance-Testing (<500ms Dashboard)
- 5-10 Beta-Merchants akquirieren (über DACH-Shopify-Communities)
- App-Store-Listing-Texte + Screenshots

### Days 81-90: App-Store-Submission

- Submission an Shopify Review
- Reviewer-Feedback einarbeiten
- Launch

**Realistisch:** Dieses Plan ist optimistisch. 110-130 Tage ist die ehrlichere Schätzung für Non-Coder + erster Build.

---

## Sources and References

1. [Shopify AI Toolkit — Shopify Dev Docs](https://shopify.dev/docs/apps/build/ai-toolkit)
2. [Shopify AI Toolkit Changelog Announcement](https://shopify.dev/changelog/shopify-ai-toolkit-connect-your-ai-tools-to-the-shopify-platform)
3. [Shopify AI Toolkit GitHub](https://github.com/Shopify/Shopify-AI-Toolkit)
4. [Ask Phill — What AI Toolkit Actually Does](https://askphill.com/blogs/blog/shopify-just-released-an-ai-toolkit-for-claude-heres-what-it-actually-does)
5. [Fudge.ai — AI Toolkit + Claude Code Setup Guide](https://www.fudge.ai/guides/shopify-ai-toolkit-claude-code-setup/)
6. [FindSkill.ai — 16 Skills 5-Min Setup No Undo Button](https://findskill.ai/blog/shopify-ai-toolkit-setup-guide/)
7. [TinyTwo Part Final — 87-Day Journey to Production](https://medium.com/@guqung6/building-a-shopify-app-with-ai-final-from-zero-to-production-the-complete-87-day-journey-e65c0b482b57)
8. [TinyTwo Part 2 — Production-Ready Review Architecture](https://medium.com/@guqung6/building-a-shopify-app-with-ai-part-2-architecting-a-production-ready-review-system-4ff776861331)
9. [TinyTwo Part 12 — 10 Battle-Tested Tips for AI Pair Programming](https://medium.com/@guqung6/building-a-shopify-app-with-ai-part-12-10-battle-tested-tips-for-productive-ai-pair-programming-39b7cb9f7a34)
10. [Gadget.dev + Remix for Shopify Apps](https://gadget.dev/blog/remix-and-gadget-build-shopify-apps-faster)
11. [Gadget.dev Shopify Apps Use Case](https://gadget.dev/use-cases/shopify-app-development)
12. [Shopify App Remix Package](https://shopify.dev/docs/api/shopify-app-remix/latest)
13. [Shopify App Template Remix GitHub](https://github.com/Shopify/shopify-app-template-remix)
14. [Shopify Functions JavaScript](https://shopify.dev/docs/apps/build/functions/programming-languages/javascript-for-functions)
15. [Built for Shopify Requirements](https://shopify.dev/docs/apps/launch/built-for-shopify/requirements)
16. [John Moore — 7 Shopify Apps as Solo Developer in Ireland](https://dev.to/jmsdevlab/how-i-built-7-shopify-apps-as-a-solo-developer-in-ireland-2nfp)
17. [Weaverse Blog — AI Toolkit + Cursor + Claude Code for Hydrogen](https://weaverse.io/blogs/shopify-ai-toolkit-dev-mcp-hydrogen-2026)

---

## Confidence and Uncertainty

- **High confidence**: AI-Toolkit-Feature-Set (direkt aus Shopify-Docs + GitHub + Release Notes), TinyTwo-Build-Timeline (Primärquelle), Skills-Kategorisierung (buildable vs nicht)
- **Medium confidence**: Non-Coder-Time-Multiplier (1,3-1,5x TinyTwo) — Annahme, keine publizierte Studie
- **Uncertain**: Ob Gadget.dev 2026-Pricing für mehrere Apps im Portfolio noch wirtschaftlich bleibt (aktueller $75/mo Entry-Tier könnte sich ändern). Realistische Shopify-Review-Queue-Zeiten Q2/Q3 2026 nicht verlässlich publiziert. BFS-Badge-Timeline für Solo-Dev ohne bestehende Review-Base schwer vorhersagbar
