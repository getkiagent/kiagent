# I4 — Discovery, Ranking und Built-for-Shopify-Badge

**Research window:** 2025-04 bis 2026-04
**Date compiled:** 2026-04-17
**Focus:** Ranking-Algorithmus 2026, App-Store-SEO, BFS-Badge-Machbarkeit für Solo-No-Coder, Acquisition-Kanäle, CAC-Benchmarks.

---

## Executive Summary

Der Shopify-App-Store-Ranking-Algorithmus gewichtet 2026 Rating + Reviews + Install-Velocity + Behavioral Signals + BFS-Badge + Update-Frequenz. Organische App-Store-Search ist mit 55-70% der Installs der klar dominante Kanal, Shopify Search Ads sekundär (CPA ~$125-150 pro aktivem Store), Google Ads tertiär (~$50+ CPC). BFS-Badge ist für einen Solo-No-Coder in 12 Monaten **machbar, aber nicht trivial** (Feasibility 5-6/10): der harte Filter ist der "≤10 Lighthouse-Punkte Storefront-Impact"-Test plus 50 net installs + 5 Reviews + Polaris-Design-Compliance. Realistische Time-to-First-100-Installs für eine gute Solo-App: **6-12 Wochen** bei solider ASO.

---

## Shopify App Store Ranking-Faktoren 2026

### Bestätigte Signale (höchste Gewichtung oben)

| Faktor | Gewichtung | Quelle |
|---|---|---|
| **Average Rating** (≥4.0 als Schwelle) | Sehr hoch | "Apps with rating <4.0 see 40-50% fewer installs" |
| **Anzahl Reviews** | Sehr hoch | Review-Velocity dient als social-proof Multiplikator |
| **Install-Volumen** (absolut + Velocity) | Hoch | Shopify bestätigt Behavioral-Data-Integration Feb 2025 |
| **Behavioral Signals** (Click, Dwell, Install-nach-Click) | Hoch | Offizielle Bestätigung: "how merchants interact with results" |
| **Built-for-Shopify Badge** | Hoch | Explizites Search-Ranking-Boost, Priority-Placements |
| **Keyword-Match** (Title, Description, Tagged-Terms) | Mittel (früher hoch) | "Keyword stuffing now has less impact" |
| **Update-Frequenz** | Mittel | Inaktive Apps verlieren Ranking über Zeit |
| **Free Plan / Trial Availability** | Mittel-Niedrig | "Free options increase adoption likelihood, weak correlation" |
| **Small-App-Trending-Boost** | Mittel | Algorithmus hebt trending kleinere Apps aktiv |
| **Performance (Storefront Lighthouse)** | Niedrig (harter Filter statt Ranking-Faktor) | Relevanz erst bei BFS-Qualifikation |

### Was Shopify nicht veröffentlicht
- Exakte Weights
- Ob Install-Velocity fenster-basiert (7/28/90d) gewichtet wird
- Churn/Uninstall-Rate als Negativ-Signal (wahrscheinlich, nicht bestätigt)

---

## App Store SEO — was funktioniert

### Title-Optimization
- 1-2 primäre Keywords direkt im App-Namen (z.B. "Newclick — Pop-Ups & Banners")
- Branded-Part + Descriptor-Part getrennt durch "—" oder "|"
- Unter 30 Zeichen für sauberes Navigation-Display (BFS-Requirement)

### Keyword-Slots
- 20 Search-Term-Slots im Backend — **alle nutzen**
- Priorität: Popularity >20, Difficulty <60 (Artemov-ASO-Heuristik)
- Keine Duplikate mit Title/Description — Verschwendung

### Description
- 2.800 Zeichen hard-limit
- PAS-Framework (Problem-Agitate-Solution) schlägt Feature-Listing
- Keywords organisch in ersten 160 Zeichen (Google-Preview)

### Screenshots
- 4-6 Screenshots optimal: Before/After/Dashboard/Outcome
- ALT-Text mit Top-Keywords (separates ASO-Signal)
- Clean, single-message per screenshot

### Dokumentierte CTR/Conversion-Uplift
- Embarque-Case-Study: Listing-Optimization **8% → 15% install conversion** (view-to-install)
- BigMoves-Case "Because Shopify App": **250-300 monatliche Installs** (von 50-60) nach Full-Stack-Optimierung, davon App-Store organic 55%, Shopify paid 30%, Google Ads 10%

---

## Built-for-Shopify-Badge — Kriterien und Machbarkeit

### Harte Kriterien (2025 Update, wirksam Juli 2025)

**Performance:**
- Admin: LCP ≤2.5s, CLS ≤0.1, INP ≤200ms (alle 75th percentile, min. 100 calls/28d)
- Storefront: App darf Lighthouse-Score um **max. 10 Punkte** senken
- Checkout (wenn genutzt): Carrier-Rate p95 ≤500ms, <0.1% failure, min. 1000 requests/28d

**Merchant Utility (Adoption-Schwellen):**
- **50 net installs** von active paid-plan shops
- **mindestens 5 Reviews**
- Mindest-Recent-Rating (nicht veröffentlicht, faktisch ≥4.5)

**Design:**
- Polaris-konform, App-Bridge aktuell, Session-Token-Auth
- Theme App Extensions (nicht Asset API)
- Keine Dark Patterns, keine Pressure-Language
- Mobile responsive, kein horizontal scroll

**Category-specific** (ab Juli 2025): Ads, Affiliate, Analytics, Email, Forms, SMS — zusätzliche API/Standards-Anforderungen.

### BFS-Feasibility für Solo-No-Coder in 12 Monaten — **5-6/10**

Begründung pro Score:
- **Performance-Gate (5/10):** ≤10 Lighthouse-Punkte ist der tötungs-wahrscheinlichste Filter. No-Code/Low-Code-Stacks (Remix Templates + AI) schaffen das, wenn keine heavy JS-Widgets auf Storefront injiziert werden.
- **Design-Gate (7/10):** Polaris + App Bridge über Remix-Template ist Standard. Schaffbar mit Claude-generiertem Code.
- **Adoption-Gate (6/10):** 50 paid installs + 5 Reviews in 12M ist machbar bei solider ASO + Freemium. Seguno wiederholte diesen Zyklus für neue Apps: **Page-1-Ranking in 6 Tagen** post-BFS.
- **Annual-Review-Gate (4/10):** BFS wird jährlich re-validiert — Wartungs-Load für Solo-Operator nicht zu unterschätzen.

### BFS-Impact nach Erreichen
- Seguno: **+14% Installs** über ganze App-Suite nach BFS
- Neue Apps von BFS-zertifizierten Partnern: Page-1-Search-Ranking **innerhalb 6 Tagen**
- Priority-Placement: App-Store-Homepage, "Recommended for you"-Category-Sections
- Exklusiver Zugang zu zielgruppen-spezifischen Search-Ads (nach Plan, Desktop/Mobile)
- Merchant-Side Filter "BFS only" → direkter Discovery-Boost

---

## Review-Velocity — was organisch erreichbar ist

### Policy-Rahmen (hart)
- **Incentivierte Reviews verboten** — Unpublishing + Partner-Programm-Risk
- Neutral formulierte Requests erlaubt: "We value feedback! It helps us improve."
- Shopify detektiert per Algorithmus, manual, und community-reports

### Benchmarks (aus Case-Studies)
- **DelightChat:** 1.500 paying / 20.000 active = 7.5% paid ratio nach 14 Monaten; Reviews nicht publiziert, aber impliziert mehrere hundert
- **Guarantees & Features Icons:** 1.800 Merchants mit 5.0-Rating-Fokus — exakte Reviews nicht veröffentlicht
- **Industrie-Indikator:** Top-Apps einer Category sammeln **~10-50 Reviews/Monat**, mittlere Apps **1-5/Monat**
- **Install-to-Review-Ratio** (branchenüblich): **1-3%** organisch — d.h. 50-150 Installs für 1-3 Reviews
- Um 50 net installs + 5 Reviews (BFS-Minimum) zu erreichen: realistisch 100-200 Installs nötig

### Review-Request Best Practice
- In-App-Prompt nach N Tagen Nutzung oder nach Value-Event ("User hat erste Rule aktiviert")
- Kein Incentive, neutrale Sprache
- Support-Ticket-Resolution als Trigger → höchste Review-Rate

---

## Third-Party Acquisition-Channels — Ranking

### 1. App-Store-Organic-Search (55-70% der Installs, CAC €0-20)
- Primärkanal bei **allen dokumentierten Erfolgs-Cases**
- Kaching: 40% organic keyword + 50% branded = 90% "App-Store-Gravitation"
- Embarque/BigMoves-Case: 55% organic share
- **ROI:** unschlagbar, aber 4-12 Wochen Vorlauf für Ranking

### 2. Shopify Search Ads (20-30% der Installs möglich, CAC $50-150)
- Shopify-interne bezahlte Platzierungen
- BigMoves-Benchmark: Initial $80-100 CPI → optimiert $50-60 CPI → $125-150 Cost-per-Active-Store nach 40% Install-to-Active
- **Nur sinnvoll für BFS-Apps** (volle Targeting-Options) oder bei ≥$30 MRR pro Customer

### 3. Google Ads (5-15% der Installs, CPC $5+ / CPI $75-100)
- Durchschnitt Google Ads CPC: **$5.26** (cross-industry)
- Durchschnitt Cost-per-Conversion e-commerce Search: **$45.27**
- Für Shopify-App-Install (abstrakteres Conversion-Event): **$75-100 je paid install** realistisch
- **Payback-Period:** bei $15 ARPU und 12-Monat Retention → nur knapp profitable, für Solo zu capital-intense

### 4. Shopify-Agentur/Partner-Referrals (5-15% der Installs, CAC variable)
- Partner-Programm zahlt 20% lifetime recurring für Merchant-Referrals
- Für App-Entwickler: Agenturen empfehlen Apps, wenn Solid + Support-SLA
- Gate: Technology Partner Track verlangt **30-min response SLA** — harte Constraint für echten Solo
- Kaching-Case: 10% aus "affiliate partnerships and ads"

### 5. Community (FB-Groups, Reddit, Shopify-Forums) — nicht quantifiziert, 2-5%
- Kaching und Guarantees-Case nutzten beide FB-Groups für Keyword-Discovery pre-build
- Als Install-Kanal marginal, als Research- und Review-Seeding-Kanal stark

### 6. SEO-Content / Long-Tail Blog (für neue App: 1-3%, langsam aufbauend)
- Long-Tail Keywords mit Install-Intent: "shopify X app free", "best shopify app for Y", "shopify X alternative"
- DelightChat-Blog rankt für "best shopify apps for..." — aber Flywheel braucht 6+ Monate
- Für DACH: "shopify rechtssicher", "shopify DSGVO app" — unterversorgter Keyword-Cluster

---

## Time-to-First-100-Installs für eine gute Solo-App

| Szenario | Voraussetzung | Zeitfenster |
|---|---|---|
| **Optimistisch** | Saubere Niche + Keyword-Research vor Build + Freemium + Launch-Seeding | **3-5 Wochen** |
| **Realistisch** | Solide Niche + Standard-ASO + Freemium | **6-12 Wochen** |
| **Pessimistisch** | Crowded Category + Paid-Only Pricing + schwache Reviews | **4-8 Monate oder nie** |

Referenzen:
- Guarantees & Features Icons: **~500 free installs in Woche 1** bei FB-Group-Seeding → Outlier, nicht Baseline
- BigMoves "Because": **50-60 Installs/Monat** vor Optimization, **250-300/Monat** nach Optimization
- Kaching Flagship: **15.000 installs/Monat steady-state** bei 6-figure MRR — Top-Tier-Benchmark

---

## CAC-Estimate Organic vs Paid

| Kanal | CAC pro aktivem Store | Payback bei $15 ARPU | Payback bei $30 ARPU |
|---|---|---|---|
| **App-Store-Organic (nach ASO-Arbeit)** | €0-15 | <1 Monat | <1 Monat |
| **Branded Word-of-Mouth** | €0 | sofort | sofort |
| **Shopify Search Ads** | $125-150 | 8-10 Monate | 4-5 Monate |
| **Google Ads** | $150-250 (CPI + active conversion) | 10+ Monate | 5-8 Monate |
| **Agency-Referral (lifetime 20%)** | "€0 upfront, 20% lifetime share" | sofort, aber -20% LTV | sofort, aber -20% LTV |
| **SEO-Content** | €5-50 pro install wenn amortisiert über 12-24M | variiert | variiert |

**Für Solo-No-Coder mit <€10k Marketing-Budget:** Organic-Only + BFS-Jagd + 1-2 Agency-Partnerships. Paid Shopify Search Ads **erst ab $30+ ARPU und Flagship-Status**.

---

## Required Fields Summary (I4)

- `store_ranking_mechanism`: **Rating + Review-Count + Install-Velocity + Behavioral Signals + BFS-Badge + Update-Frequency + Keyword-Match (abnehmend)** (high confidence)
- `primary_channel`: **App-Store-Organic-Search (55-70%)** (high confidence)
- `paid_ads_viability`: Shopify-Search-Ads rentabel ab $30 ARPU und BFS-Status; Google Ads für Solo meist negativ (medium confidence)
- `cac_estimate`: **Organic €0-15 / Shopify-Ads $125-150 / Google-Ads $150-250** pro aktivem Store (medium confidence, BigMoves als Einzel-Datenpunkt)
- `built_for_shopify_feasibility_1_10`: **5-6/10** für Solo-No-Coder in 12 Monaten; Performance-Gate und jährliche Re-Review sind die Risiko-Punkte (medium-high confidence)
- `review_velocity_benchmark`: **1-3% Install-to-Review-Ratio** organisch; Top-Apps 10-50 Reviews/Monat, mittlere 1-5/Monat (medium confidence, keine harte Shopify-Veröffentlichung)
- `install_to_paid_conversion`: **Trial-to-paid 15-50%** bei gutem Onboarding (Delight 50% nach Fix, BigMoves 15% optimiert) (medium confidence)
- `sources`: siehe Referenzliste unten
- `confidence_level`: **medium-high** für Ranking-Faktoren und BFS-Kriterien (offizielle Shopify-Docs + Case-Studies); **medium** für CAC-Numbers (einzelne Datenpunkte)
- `uncertain`:
  - Exakte Weights im Ranking-Algorithmus sind nicht veröffentlicht
  - Review-Velocity-Benchmarks basieren auf Case-Studies, nicht auf Shopify-Gesamtstatistik
  - BFS-Feasibility 5-6/10 ist qualitative Einschätzung — keine Studie, wie viele Solo-No-Coder BFS in 12M erreichen
  - CPI-Benchmarks aus BigMoves-Case sind ein einzelner Datenpunkt, Streuung hoch

---

## Sources and References

1. [Shopify Dev — Built for Shopify Requirements](https://shopify.dev/docs/apps/launch/built-for-shopify/requirements) — Exakte Performance-Gates und Adoption-Schwellen
2. [Shopify Partners Blog — Built for Shopify 2025 Updates](https://www.shopify.com/partners/blog/built-for-shopify-updates) — Neue Kriterien Juli 2025
3. [Shopify Partners Blog — Seguno BFS Case](https://www.shopify.com/partners/blog/seguno-built-for-shopify) — +14% Installs, Page-1 in 6 Tagen
4. [Shopify Dev Changelog — BFS Priority Visibility](https://shopify.dev/changelog/built-for-shopify-apps-get-priority-visibility-across-the-shopify-app-store) — Placement-Details
5. [Shopify Partners Blog — Search Improvements](https://www.shopify.com/partners/blog/search-improvements) — Behavioral-Signal-Integration Feb 2025
6. [Litos.io — BFS Explained 2025](https://litos.io/blog/built-for-shopify/) — Benefits und Qualifikation
7. [Praella — Category-Specific BFS Requirements July 2025](https://praella.com/blogs/shopify-news/new-category-specific-requirements-for-shopifys-built-for-shopify-program-effective-july-2025) — Marketing-Apps-Delta
8. [Embarque — Shopify App Listing Optimization](https://www.embarque.io/post/shopify-app-listing-optimization) — 8%→15% Conversion Case
9. [BigMoves — Because Shopify App Playbook](https://www.bigmoves.marketing/case-study/case-study-because-shopify-app-the-shopify-app-playbook-app-store-optimization-shopify-search-ads-multi-channel-growth) — Full-Funnel-Benchmarks, CPI/CAC
10. [Shopify Partners Blog — Best Practices App Store](https://shopify.dev/docs/apps/launch/shopify-app-store/best-practices) — Offizielle ASO-Guidelines
11. [Shopify Partners Blog — Your App Isn't Getting Installs](https://www.shopify.com/partners/blog/app-installs) — Discovery-Diagnostik
12. [Shopify — Manage App Reviews Policy](https://shopify.dev/docs/apps/launch/marketing/manage-app-reviews) — Review-Request-Regeln
13. [Moburst — App Store Ranking Factors 2026](https://www.moburst.com/blog/app-store-ranking-factors/) — Cross-Platform-Ranking-Mechanik
14. [Meetanshi — Shopify App Store Statistics 2026](https://meetanshi.com/blog/shopify-app-store-statistics/) — Volumen, Rating-Impact
15. [Shopify Blog — PPC Statistics 2026](https://www.shopify.com/blog/ppc-statistics) — Google Ads CPC-Benchmarks
16. [Shopify Help — Partner Earnings](https://help.shopify.com/en/partners/partner-program/how-to-earn) — 20% Lifetime-Commission für Referrals
