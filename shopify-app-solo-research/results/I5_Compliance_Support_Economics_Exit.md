# I5 — Compliance, Support-SLA, Economics und Exit-Markt DACH

**Researcher:** Agent A3
**Datum:** 2026-04-17
**Scope:** Solo-No-Code-Operator DACH, Shopify App Store
**Confidence gesamt:** medium-high (Economics & Shopify-Policy: high; DACH-Steuer: medium; Support-Last-Benchmarks: low-medium)

---

## Executive Summary

Ein Solo-Operator DACH muss fuer einen App-Launch realistisch **2.000–4.500 EUR Einmal-Compliance-Kosten** und **30–60 EUR/Monat laufend** einplanen (Anwalt fuer AVV/Datenschutz + Hosting EU). Die drei Mandatory Privacy Webhooks sind technisch **Komplexitaet 3/5** fuer Non-Coder — mit Shopify-CLI-Templates machbar, aber HMAC-Verification und Raw-Body-Handling sind die haeufigsten Fehlerquellen. Shopify-Revenue-Share ist seit 01.01.2025 klar: **0% auf die ersten 1M USD Lifetime-Gross, 15% darueber**, plus 19 USD Partner-Fee einmalig. Exit-Multiples 2026: Micro-SaaS ≤1M TTM Revenue liegt bei **5–7x ARR** (Growth ≥30%, NRR ≥110%), niedrigere Multiples (3–5x) bei flat Growth. Die 30-Minuten-Response fuer kritische Tickets gilt nur fuer den **optionalen Technology Partner Track** — reguläre App-Store-Apps haben keine harte SLA.

---

## A) DACH-Compliance-Overhead (in EUR)

### A1. Mandatory Privacy Webhooks — technische Anforderungen

Shopify verlangt drei Webhook-Endpoints fuer jede oeffentliche App:

| Webhook | Trigger | Deadline |
|---|---|---|
| `customers/data_request` | Merchant fordert Kundendaten an | 30 Tage Antwort |
| `customers/redact` | Merchant fordert Loeschung | 30 Tage (verzoegert 10 Tage wenn keine Orders, ansonsten 6 Monate Wartefrist) |
| `shop/redact` | 48h nach App-Uninstall | 30 Tage |

**Technische Pflichten** (aus [shopify.dev/privacy-law-compliance](https://shopify.dev/docs/apps/build/compliance/privacy-law-compliance)):
- POST-Endpoint mit `application/json`
- HMAC-SHA256-Verification via `X-Shopify-Hmac-SHA256` Header
- 200-Series-Status bei Erfolg, 401 bei invalider HMAC
- Konfiguration ueber `compliance_topics` in `shopify.app.toml`

**Komplexitaet fuer Non-Coder: 3/5**
- Shopify CLI generiert Template-Endpoints (Boilerplate vorhanden)
- Haeufigste Stolperfalle: Raw-Body muss VOR JSON-Parsing gehasht werden (mehrere Reports in der Shopify-Community — z.B. [community.shopify.dev HMAC issues](https://community.shopify.dev/t/issue-verifying-webhook-hmac-from-shopify/16928))
- Secret ist das App-Client-Secret (kein separates Webhook-Secret wie bei Stripe)
- Shopify-Automated-Checker testet GDPR-Webhooks automatisch vor App-Approval — wenn nur spezifische Topics behandelt werden, faellt der Check durch

**Realistischer Aufwand:** 4–8 Stunden Setup mit AI-Coding-Assist, inkl. Debugging. Einmalig.

### A2. TDDDG (Telekommunikations-Digitale-Dienste-Datenschutz-Gesetz)

Das TDDDG hat am 14.05.2024 das TTDSG abgeloest. Relevant fuer Shopify-Apps, die auf dem Merchant-Store **JavaScript/Cookies/Tracking** platzieren:

- **Pflicht:** Aktive Einwilligung (Opt-in) **bevor** irgendwelche nicht-essentiellen Cookies gesetzt oder Tracking-Scripts geladen werden
- **Shopify Privacy API:** Moderne Consent-Tools (Usercentrics, Consentmanager) integrieren ueber die Shopify Privacy API — App-Entwickler muss diese nutzen, wenn die App Tracking macht ([qualimero.com/shopify-dsgvo](https://qualimero.com/blog/shopify-dsgvo))
- **Relevanz fuer App-Typ:** Apps ohne Frontend-Tracking (Backoffice-Tools, Order-Management) sind TDDDG-neutral. Analytics-, Marketing-, Popup-Apps **muessen** Privacy API respektieren.

### A3. AVV / Data Processing Agreement

**Pflicht-Layer:**
1. **AVV mit Shopify:** Automatisch mit Merchant-Account ([shopify.com/legal/dpa](https://www.shopify.com/legal/dpa)) — als App-Dev nicht direkt betroffen
2. **AVV App-Dev → Merchant:** Als Datenverarbeiter im Auftrag des Merchants MUSS der App-Entwickler einen eigenen AVV bereitstellen (Art. 28 DSGVO)
3. **AVV mit Subprozessoren:** Jeder Hoster, jedes externes Tool (SendGrid, OpenAI, Sentry) braucht eigenen AVV

**Einmal-Kosten Rechts-Setup DACH (EUR, Stand 2025):**

| Leistung | Kosten (netto) | Quelle |
|---|---|---|
| Datenschutzerklaerung (individuell) | 390–600 EUR | [derstartupanwalt.de](https://www.derstartupanwalt.de/leistungen/online-rechtspaket) |
| AVV-Template fuer Merchants | 590–900 EUR | derstartupanwalt.de |
| AGB/Nutzungsbedingungen App | 500–800 EUR | juraforum.de-Umfragen |
| Impressum + Erstberatung | 150–300 EUR | anwalt.de |
| **Summe Einmal (konservativ)** | **1.630–2.600 EUR** | — |
| **Kombi-Paket "Startup"** | **990–1.500 EUR** | derstartupanwalt.de |

**Laufend:**
- Legal-Updates (Datenschutzerklaerung bei neuen Features): ~200–400 EUR/Jahr
- Merchant-Support fuer DSGVO-Fragen: 1–2 Tickets/Woche bei 500 Installs = ~2–4h/Woche

### A4. Hosting — DACH/EU-Pflicht?

**Nicht strikt Pflicht, aber Best Practice:**
- Hetzner (DE, Falkenstein/Nuernberg): DSGVO-native, 4–15 EUR/Monat fuer Cloud-VPS ([hetzner.com/cloud](https://www.hetzner.com/cloud))
- AWS Frankfurt / GCP Europe: erlaubt, aber wegen US-Muttergesellschaft MUSS EU-US-Data-Privacy-Framework-Zertifizierung (DPF) geprueft werden. Shopify selbst laeuft auf GCP mit DPF.
- IONOS (DE): ~10–30 EUR/Monat, DSGVO-ok
- **Vercel/Netlify:** US-basiert, DPF-zertifiziert, aber riskanter fuer konservative DACH-Kundschaft

**Empfehlung fuer Solo:** Hetzner Cloud CX22 (~6 EUR/Monat) + Supabase EU-Region (Frankfurt) fuer DB = ~30–50 EUR/Monat Infrastruktur bis 500 Installs.

### A5. Impressumspflicht

Seit 14.05.2024: **§ 5 DDG** (Digitale-Dienste-Gesetz) ersetzt § 5 TMG. Inhaltlich gleich, aber die Rechtsgrundlage im Impressum muss auf "§ 5 DDG" geaendert werden — sonst Abmahnrisiko.

**Pflichtangaben Shopify-App-Entwickler:**
- Name, Adresse (keine Postfach), Email, Telefon
- USt-IdNr. oder Wirtschafts-IdNr. (ab Dezember 2026 Pflicht W-IdNr.)
- Impressum muss aus App selbst UND aus App-Store-Listing einen Klick entfernt erreichbar sein

**Relevanz:** [e-recht24.de bestaetigt Abmahnungen fuer fehlendes Impressum im App-Store-Listing](https://www.e-recht24.de/impressum/10176-app-impressum.html).

### A6. Compliance-Cost-Summary (EUR)

| Posten | Einmal | Laufend/Monat |
|---|---|---|
| Rechts-Review (AVV + DS + AGB + Impressum) | 1.500–2.600 | 15–30 |
| Hosting EU (Hetzner + Supabase EU) | 0 | 30–60 |
| Webhook-Impl. Zeit-Aequivalent | 200–400 | — |
| Consent-Tool-Integration (falls Frontend) | 300–800 | 20–50 |
| Legal-Updates jaehrlich | — | 15–35 |
| **Summe Solo-Operator DACH** | **2.000–3.800 EUR** | **~60–140 EUR** |

**compliance_cost_eur_eu:** 2000–3800 EUR einmal / 60–140 EUR laufend monatlich
**mandatory_webhooks_complexity:** 3/5

---

## B) Support-SLA und Solo-Betrieb

### B1. Gibt es eine 30-Minuten-SLA-Pflicht?

**Nein — NICHT fuer normale App-Store-Apps.**

Die 30-Minuten-First-Response bei kritischen Tickets ist eine Anforderung des **optionalen "Technology Partner Track"** (frueher "Certified Technology Partner Program"), der Apps fuer Shopify Plus / Enterprise-Merchants zulassen will ([help.shopify.com Technology Track](https://help.shopify.com/en/partners/partner-program/technology-partner-track/how-to-qualify)):

| Prioritaet | First Response | Beispiele |
|---|---|---|
| Kritisch | **30 Minuten** | Service-Outage mehrerer Kunden, Security-Vulnerability-Reports |
| Hoch | 12 Stunden | Einzelne User koennen Produkt nicht nutzen |
| Niedrig | 3 Tage | Fragen, Feature-Requests |

Erlaubte Response-Kanaele: Phone, SMS, Email, In-Product.

**Fuer Solo-Operator Standard-App-Store (ohne Plus/Enterprise-Fokus):**
- Keine formelle SLA
- App-Store-Reviews bestrafen aber schlechte Response (typisch <24h erwartet)
- Built-for-Shopify-Badge-Requirements fordern "adequate support" — ungenau, aber <24h Median ueber die Review-Periode ist faktisch noetig

**Fazit:** Solo kann Standard-Apps fahren ohne 30-Min-SLA. Sobald du Plus-Apps machst (hoehere Preispunkte 200–500 USD/Monat), wird die 30-Min-Pflicht zum Bottleneck.

**support_sla_required:** Nein fuer Standard-App; Ja (30min kritisch / 12h hoch / 3d niedrig) fuer Technology Partner Track (Plus-Apps)

### B2. Realistische Support-Last (Tickets/Woche)

**Keine harten Benchmarks publiziert — nur Proxies aus Indie-Hackers-Threads + Shopify-Allgemein-Benchmarks** (uncertain):

Aus Indie-Hacker-Interviews und Community-Posts ([Bjoern Forsberg Case](https://www.indiehackers.com/post/100k-mo-from-4-shopify-apps-solo-not-me-9ab6034f5c), Tabarnapp-Exit, Erikas-Malisauskas):

| Installs (paying) | Tickets/Woche | Std/Woche Support |
|---|---|---|
| 100 | 5–15 | 2–5 |
| 500 | 20–60 | 5–15 |
| 1.000 | 40–120 | 10–25 |

**Variance-Treiber:**
- Konfigurations-lastige Apps (Popup, Bundles, Checkout-Mods): hohe Ticket-Rate (1 Ticket / 8 Installs)
- Passive Apps (Currency, Image-Optim): niedrig (1 Ticket / 40 Installs)
- Plus-Merchants: weniger Volume, aber komplexere Tickets, >45 Min pro Fall

**Tabarnapp-Datenpunkt:** 2.500 paying Customers, Team vor Exit mit Publisher-Partnership um Support auszulagern ([theygotacquired.com](https://theygotacquired.com/saas/tabarnapp-acquired-by-staytuned/)).

### B3. AI-Helpdesk-Stack als Solo-Ersatz

**Pricing Q2 2026:**

| Tool | Entry-Pricing | Ideal fuer |
|---|---|---|
| Gorgias + AI Agent | 10 USD/Monat (50 tickets) + 1 USD/AI-resolved | B2C-heavy Apps |
| Intercom Fin | 0.99 USD/resolved conversation | Hohe Deflection-Rate |
| Commslayer (Solo-focused) | ~29 USD/Monat | Bootstrapper |
| Crisp | 25 EUR/Monat unlimited | Chat-first, DACH-freundlich |
| Plain | 29 USD/Monat | Developer-focused Inbox |

**Realismus:** AI deflectet 40–70% der Tier-1-Tickets (Password-Reset, Setup-Anleitung, Billing-Frage). Bei 100 Tickets/Woche bleibt Solo auf ~30–50 manuelle Tickets/Woche = 5–10h Arbeitszeit.

**Kosten-Beispiel 500 Installs, 40 Tickets/Woche:**
- Gorgias Starter + AI: ~60–120 USD/Monat
- Plus Solo-Zeit 10h/Woche

### B4. Wann braucht Solo einen VA oder Partner?

**Trigger-Punkte aus dokumentierten Cases:**
1. **≥60 Tickets/Woche** mit ≥20% komplexe Tier-2-Issues → VA sinnvoll
2. **Plus-Merchant-Customer** (30-Min-SLA) → Partner/VA mit Timezone-Coverage zwingend
3. **Portfolio 3+ Apps** → Shared-Support-VA (Beispiel Bjoern Forsberg, Tabarnapp)
4. **Tarbanapp-Pattern:** "Publisher" uebernimmt Support/Reviews/User-Feedback, Entwickler fokussiert auf Code (siehe [30-app-portfolio Case](https://www.indiehackers.com/post/tech/from-failed-app-to-30-app-portfolio-making-22k-mo-in-less-than-a-year-myy3U7K9evxGOVOHti8s))

**VA-Kosten DACH-kompatibel:** Englisch-VA Philippines/Osteuropa: 8–15 USD/h; DACH-Muttersprache-VA: 25–40 EUR/h.

### B5. Burnout-Signale aus Solo-Cases

Aus Indie-Hackers-Posts ([What It Takes to Survive as a Solo Founder](https://www.indiehackers.com/post/what-it-takes-to-survive-as-a-solo-founder-50f95dc404)):
- **Signal 1:** Support-Queue nie <24h leer → Feature-Dev stoppt
- **Signal 2:** Weekend-Support-Stress
- **Signal 3:** 2-3 schlechte Reviews in Folge wegen Response-Zeit
- **Signal 4:** Shopify-API-Breaking-Changes treffen 3+ Apps gleichzeitig
- **Bjoern Forsberg:** Explizit erwaehnt "deliberate time management, compressing into few hours daily" — Bootstrap-Solo mit Familie geht nur mit rigiden Grenzen.

**maintenance_hours_per_week** (Support-Anteil, ohne Feature-Dev):
- 100 installs: 2–5h
- 500 installs: 5–15h
- 1.000 installs: 10–25h (mit AI-Tools ~7–18h)

---

## C) Economics und Exit-Markt

### C1. Shopify Revenue Share 2025+

**Verifiziert ueber [shopify.dev/revenue-share](https://shopify.dev/docs/apps/launch/distribution/revenue-share):**

| Bracket | Rate |
|---|---|
| Lifetime Gross 0 – 1.000.000 USD (ab 01.01.2025) | **0%** |
| > 1.000.000 USD | **15%** (Shopify) / 85% (Dev) |
| High-Volume (≥20M USD prev. year oder ≥100M Company Rev) | 15% auf alles |

**Wichtig fuer Financial Model:**
- 1M-Schwelle ist **Lifetime**, nicht mehr annual (frueher: jaehrlich zurueckgesetzt)
- Revenue vor 01.01.2025 zaehlt nicht
- Alle Associated Developer Accounts zaehlen zusammen
- Nach Erreichen 1M: kein Zurueck zu 0%
- **Processing Fee 2.9%** auf alles (Shopify-Billing)
- **Partner-Fee: 19 USD** (einmalig, nicht 99 USD — 99 USD war Pre-2021-Marketing fuer Partner-Accounts, heute 19 USD)

**revenue_share_band:** 0–1M USD Lifetime = 0%; >1M USD = 15% (85% Dev)

### C2. Managed Pricing 180-Tage-Trial-Tracking

**Quelle:** [shopify.dev Managed Pricing](https://shopify.dev/docs/apps/launch/billing/managed-pricing)

- Shopify trackt Trial-Tage ueber **180 Tage** pro Shop, um Re-Install-Abuse zu blocken
- Impact Financial Model: **Gleiche Shop-Domain** kann innerhalb 180 Tagen nicht mehrfach Trial nutzen — reduziert Free-Rider-Rate
- Billing-Cycle: 30-Tage, Trial wird am Start des naechsten Cycles als prorated-credit abgerechnet
- Revenue Recognition: Income wird zum Cycle-Start verbucht, nicht bei Trial-Start

**Implikation:** Solo-App mit 14-Tage-Trial verliert kaum Revenue durch Wiederholungs-Trials — Model kann eher aggressiv lange Trials (30d) fahren ohne Churn-Manipulation.

### C3. Exit-Multiples 2025/2026

**SaaS-Median-Multiple (aktuellster Stand Q1 2026):**

Aus [Aventis Advisors SaaS Multiples 2015–2026](https://aventis-advisors.com/saas-valuation-multiples/) und [Flippa Multiples 2026](https://flippa.com/blog/saas-multiples/):

| Segment | EV/Revenue Multiple |
|---|---|
| Public SaaS Median (Maerz 2026) | **3.4x** |
| EV 5–10M USD | 3–4x Revenue |
| EV 10–25M USD | 4–5x |
| EV 25–50M USD | 5–7x |
| **Micro-SaaS ≤1M TTM Revenue** | **5–7x ARR (2025/2026)** |

**Micro-SaaS Growth-Tiers:**
- <20% YoY: 3–5x ARR
- 20–40% YoY: 5–7x ARR
- **>40% YoY + NRR ≥110%: 7–10x ARR**
- 2024 Baseline war ~4x; 2025 Shift zu 5–7x wegen AI-Disruption-Interest und strategischen Buyern

**Acquire.com Datenpunkte (konkrete Listings):**

| App | Revenue TTM | Profit TTM | Growth | Asking/Note |
|---|---|---|---|---|
| Bulk Price Scheduler | 42.363 USD | 41.500 USD | 105% YoY | 500+ merchants, Listing aktiv |
| Built-for-Shopify Portfolio | 91.200 USD (7.6k MRR) | ~84k (92% Marge) | Top 10 ranks | 3 Apps Bundle |
| Tabarnapp Exit (2022) | nicht disclosed | — | — | Sale ~4M USD, Mid-7-Figures |
| Erikas Malisauskas Exit | 78k USD (6.5k MRR) | — | — | Sold 250k USD = ~3.2x Revenue |
| Acquire.com Marketplace avg. | — | — | — | **4.3x TTM Profit** Durchschnitt (Jan 2024 Report) |

**Case-Beispiel: App mit 200k USD Revenue / 150k USD Profit (75% Marge), +30% YoY, NRR ≥110%:**

| Scenario | Multiple | Asking Price (USD) |
|---|---|---|
| Konservativ (Revenue-basiert) | 4x TTM Rev | **~800.000 USD** |
| Standard (Profit-basiert) | 4.3x TTM Profit | **~645.000 USD** |
| Aggressive (Growth >30%, NRR >110%) | 5.5–6x ARR | **1.1–1.2M USD** |
| Selten (Strategic Buyer, BFS-Status) | 7x ARR | **1.4M USD** |

**Realistisches Asking** fuer 200k Rev / 150k Profit 2026: **700k–1.2M USD**, erwartete Sale: **550k–900k USD** nach Verhandlung.

**exit_multiple_benchmark_ttm_revenue:** 4–6x TTM Revenue (Base Case); 3x niedrig Growth / 6–7x hoch Growth + NRR>110% + BFS

### C4. Tax-Implikationen DACH (Exit-Besteuerung)

**uncertain** — Steuerberater vor Exit zwingend konsultieren. Grobe Einordnung:

**Einzelunternehmer / Freelancer Asset-Deal (typisch Solo-App-Entwickler ohne Holding):**
- Verkaufsgewinn = Einkommensteuer-pflichtig
- Spitzensteuersatz **bis 45%** (Reichensteuer) + ggf. Kirchensteuer + Solidaritaetszuschlag (fuer Spitzenverdiener)
- **§ 16 Abs. 4 EStG Freibetrag:** 45.000 EUR einmalig im Leben, aber NUR wenn Verkaeufer 55+ Jahre oder dauernd berufsunfaehig (fuer Solo-Founder meist irrelevant)
- Abschmelzung ab 136.000 EUR Gewinn
- **Fuenftelregelung** (§ 34 EStG) bei Betriebsaufgabe kann Progression glaetten

**GmbH Share-Deal (App-Entwickler mit GmbH-Struktur):**
- **95% steuerfrei**, 5% steuerpflichtig (koerperschaftsteuer + gewerbesteuer, effektiv ~1.5%)
- Voraussetzung: Holding-GmbH-Struktur
- **Teileinkuenfteverfahren** bei natuerlicher Person: 60% steuerpflichtig auf Dividenden/Veraeusserung

**Holding-Struktur (GmbH unter GmbH):**
- Verkauf der operativen GmbH durch die Holding: effektiv **~1.5% Steuer** auf Exit-Erloes
- Thesaurierung in Holding moeglich
- Vorlauf: **mind. 12 Monate** vor Verkauf strukturieren (idealerweise 7+ Jahre)

**Einzelunternehmer vs. GmbH fuer App-Exit bei 1M EUR Verkaufserloes:**

| Struktur | Effektive Steuer | Netto |
|---|---|---|
| Einzelunternehmer (Spitzensatz, kein §16-4) | ~42% | ~580.000 EUR |
| GmbH-Gewinnausschuettung (KSt + Teileinkuenfte) | ~40% gesamt | ~600.000 EUR |
| Holding-Struktur (Share-Deal via Holding) | ~1.5% | ~985.000 EUR (in Holding, nicht privat) |
| Holding → spaetere Entnahme privat (Teileinkuenfte) | zusaetzlich ~26% auf Entnahme | ~730.000 EUR privat |

**Empfehlung:** Ab 200k EUR geplantem Exit-Wert GmbH/UG gruenden lohnt; ab 500k EUR Holding-Struktur pruefen. Quellen: [rosepartner.de](https://www.rosepartner.de/rechtsberatung/gesellschaftsrecht-ma/unternehmenskauf-ma-venture-capital-und-private-equity/besteuerung-des-unternehmenskaufs.html), [exit-coach.de](https://exit-coach.de/unternehmensverkauf-steuern/), [firmenzukaufen.de](https://www.firmenzukaufen.de/blog/steuern-beim-unternehmensverkauf-share-deal-asset-deal-34-estg).

**uncertain:** Individuelle Steuerlast haengt stark von Gesamteinkommen, Wohnsitz (DE/AT/CH unterschiedlich), Holding-Historie, Asset-vs-Share-Deal ab. Steuerberater-Konsultation zwingend vor Exit-Verhandlung.

---

## Merchant-Tier-Fit

**merchant_tier_fit fuer DACH-Solo-No-Code:**
- **Basic/Shopify (Sweet Spot):** 10–30 USD/Monat Price Point, Standard-SLA <24h, hohes Volumen, niedrige Support-Komplexitaet pro Ticket
- **Advanced:** Grenzbereich — noch machbar mit AI-Helpdesk
- **Shopify Plus (NICHT empfohlen fuer Solo):** 30-Min-Kritisch-SLA des Technology-Partner-Tracks nicht alleine haltbar, 200–2000 USD/Monat Preispunkt braucht Account-Management

---

## Sources and References

1. [Shopify Revenue Share Official Docs](https://shopify.dev/docs/apps/launch/distribution/revenue-share) — Revenue-Share 2025+
2. [Shopify Privacy Law Compliance](https://shopify.dev/docs/apps/build/compliance/privacy-law-compliance) — Mandatory Webhooks
3. [Shopify Technology Partner Track Qualifications](https://help.shopify.com/en/partners/partner-program/technology-partner-track/how-to-qualify) — 30-Min-SLA
4. [Shopify Data Processing Addendum](https://www.shopify.com/legal/dpa) — DPA mit Merchants
5. [Shopify Managed Pricing](https://shopify.dev/docs/apps/launch/billing/managed-pricing) — 180-Tage-Trial
6. [Shopify Compliance Webhook Changelog](https://shopify.dev/changelog/apps-now-need-to-use-gdpr-webhooks) — Webhook-Pflicht
7. [av-vertrag.org Shopify AVV](https://av-vertrag.org/dienst-anbieter/shopify/) — AVV Shopify
8. [e-recht24.de TDDDG](https://www.e-recht24.de/datenschutz/12834-tdddg.html) — TDDDG Erklaerung
9. [qualimero.com Shopify DSGVO 2026](https://qualimero.com/blog/shopify-dsgvo) — DACH Compliance Guide
10. [e-recht24.de App-Impressum](https://www.e-recht24.de/impressum/10176-app-impressum.html) — Impressum-Pflicht Apps
11. [it-recht-kanzlei.de DDG](https://www.it-recht-kanzlei.de/tmg-ttdsg-ausser-kraft-impressum-datenschutz.html) — TMG → DDG Wechsel
12. [Latori Shopify GDPR](https://www.latori.com/en/blogpost/shopify-dsgvo) — DACH Shopify Compliance
13. [derstartupanwalt.de Rechtspaket](https://www.derstartupanwalt.de/leistungen/online-rechtspaket) — AGB/DS-Paket Kosten
14. [juraforum.de Anwaltskosten AGB/DS](https://www.juraforum.de/forum/t/kosten-fuer-die-erstellung-von-agb-und-datenschutzerklaerung-durch-anwalt.652023/) — Kosten-Range
15. [Aventis SaaS Valuation Multiples 2015–2026](https://aventis-advisors.com/saas-valuation-multiples/) — Public Multiples
16. [Flippa SaaS Multiples 2026](https://flippa.com/blog/saas-multiples/) — Micro-SaaS 2026
17. [Acquire.com Annual SaaS Report 2025](https://blog.acquire.com/annual-saas-report-2025/) — Median 4.3x Profit
18. [Acquire.com Shopify Apps For Sale](https://acquire.com/shopify-apps-for-sale/) — Listings-Overview
19. [Bulk Price Scheduler Listing](https://app.acquire.com/startup/iwowpkjrif-shopify-bulk-price-scheduler-app-105-yoy-growth-41-5k-ttm-profit-500-merchants) — 105% YoY Case
20. [BFS Portfolio Listing](https://app.acquire.com/startup/2psxipjknh-built-for-shopify-app-portfolio-7-6k-mrr-92-margins-top-10-rankings-proven-organic-growth) — BFS Portfolio
21. [Tabarnapp Exit Story](https://theygotacquired.com/saas/tabarnapp-acquired-by-staytuned/) — 4M USD Exit
22. [Bjoern Forsberg 100k/mo Solo](https://www.indiehackers.com/post/100k-mo-from-4-shopify-apps-solo-not-me-9ab6034f5c) — Solo-Portfolio
23. [30-App Portfolio Case](https://www.indiehackers.com/post/tech/from-failed-app-to-30-app-portfolio-making-22k-mo-in-less-than-a-year-myy3U7K9evxGOVOHti8s) — Publisher-Modell
24. [rosepartner.de Unternehmensverkauf Besteuerung](https://www.rosepartner.de/rechtsberatung/gesellschaftsrecht-ma/unternehmenskauf-ma-venture-capital-und-private-equity/besteuerung-des-unternehmenskaufs.html) — Exit-Steuer DE
25. [exit-coach.de Unternehmensverkauf Steuern](https://exit-coach.de/unternehmensverkauf-steuern/) — Holding-Strategie
26. [firmenzukaufen.de Share Deal vs Asset Deal](https://www.firmenzukaufen.de/blog/steuern-beim-unternehmensverkauf-share-deal-asset-deal-34-estg) — Deal-Struktur
27. [steuerkurse.de § 16 Abs. 4 EStG](https://www.steuerkurse.de/einkommensteuer-vertiefung/freibetrag-nach-16-4-estg.html) — 45k Freibetrag
28. [Hetzner Cloud](https://www.hetzner.com/cloud) — DACH Hosting
29. [Gorgias Pricing](https://www.gorgias.com/pricing) — Helpdesk-Kosten
30. [Fin AI Pricing](https://fin.ai/learn/fin-vs-gorgias) — Intercom Fin

---

## Confidence and Uncertainty

**confidence_level:** medium-high
- HIGH: Shopify-Policy (Revenue-Share, Webhooks, SLA-Requirements), DACH-Rechtsgrundlagen (DSGVO, DDG, TDDDG, § 16 EStG)
- MEDIUM: Multiples (Range ist breit, abhaengig von Growth/NRR), AVV/Legal-Kosten-Range (regional variabel), Compliance-Kosten-Schaetzung
- LOW-MEDIUM: Support-Tickets/Install-Benchmarks (kein publiziertes Dataset, Proxy aus Community-Posts)

**uncertain:**
- DACH-Tax-Implikationen individuell stark variabel — Steuerberater vor Exit zwingend. Nur grobe Einordnung in diesem Report.
- Support-Last-Zahlen sind Schaetzungen aus 4–5 Indie-Hackers-Interviews, kein Peer-Review-Dataset.
- Multiples Q1 2026 auf Micro-SaaS: 5–7x Range gut dokumentiert, aber Einzeltransaktionen stark spreaded (0.63x bis 34x laut Acquire.com historischem Dataset).
- 99 USD vs 19 USD Partner-Fee: 19 USD ist aktuell, 99 USD Referenzen in aelteren Quellen koennen historische Gebuehr fuer Partner-Accounts vor 2021 gewesen sein.
- "Built-for-Shopify" Badge-Impact auf Multiple: anekdotisch +20–40%, kein hard Benchmark.

---
