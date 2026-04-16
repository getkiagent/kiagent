# I1 — Unterversorgte Shopify App-Kategorien 2026

**Date:** 2026-04-17
**Agent:** A1
**Source Corpus:** StoreInspect (376k-Store-Studie), Shopify App Store Category Pages, Shopify Dev Docs (AI Toolkit, Checkout Extensibility), StoreInspect Retention Gap Study (358k), App Market Share Study (508k)

---

## Executive Summary

Drei Thesen, in Reihenfolge ihrer Base Rate:

1. **Checkout-Extension-getriebene Nischen-Apps (Loyalty-at-Checkout, Upsell, Custom Shipping-Rules) sind 2026 Green-Field** — Shopify hat Checkout UI Extensions im Januar 2026 (Checkout API v2) auf alle Paid-Plans ausgerollt, der Markt startet neu, Incumbents haben noch keine dominanten Positionen bei den neuen Surfaces.
2. **Shopify-Native-Absorption kill list ist konkret**: Product-Description-Generation, Alt-Text, Basic-SEO-Meta, A/B-Testing, native SMS (Shopify Messaging), native Subscriptions sind bereits absorbiert oder <12 Monate entfernt. Finger weg.
3. **DACH-spezifische Compliance + Accounting-Integrationen (Lexoffice, Billbee, Trusted Shops, TDDDG) bleiben 24+ Monate safe** — Shopify kommt regulatorisch nicht schnell hinterher, 72% der Deutschen wollen Reviews in Deutsch.

**Ranking nach 12-Monats-Base-Rate für 5-25k USD MRR:**

1. Loyalty-at-Checkout-Extension für DACH (höchste Base Rate)
2. DACH-Compliance-Stack für Checkout (TDDDG + Trusted Shops Badges + Lexoffice-Handoff)
3. Niche-Analytics für Home & Garden / Automotive Plus-Stores
4. Pre-Order + Back-in-Stock für Home & Garden / Food & Beverage
5. Functions-basiertes Shipping/Discount-Rules für B2B-DTC-Mischstores

---

## Marktkontext 2026 (Evidenz-Block)

### StoreInspect 376k-Store-Analyse (Januar 2026)

Tech-Stack-Gaps (Overall, ALL stores):

| Kategorie | Stores ohne App | Adoption |
|---|---|---|
| Subscriptions | 519.982 (98,1%) | 1,9% |
| Dedicated Analytics | 518.892 (97,9%) | 2,1% |
| Support | 519.150 (97,9%) | 2,1% |
| Reviews | 498.338 (94%) | 6% |
| Email/SMS | 341.485 (64,4%) | 35,6% |

### High-Traffic Meta-Ads-Stores (Retention-Gap, StoreInspect 358k-Study)

- 88,4% haben kein SMS Marketing
- 84,9% haben kein Loyalty-Programm
- 87,7% sammeln keine Reviews

### Retention-Gap nach Niche (absolut size)

| Niche | Stores | Gap | Prio |
|---|---|---|---|
| Fashion | 74.228 | 38,1% | sekundär (Top-Apps saturated) |
| Home & Garden | 45.362 | 42,9% | primär |
| Food & Beverage | 30.097 | 35,5% | sekundär |
| Hobby | 28.622 | 43,2% | primär (solo-friendly) |
| Beauty | 23.101 | 30,9% | gesättigt |
| Automotive | 6.305 | 51,7% | Nische, hohe WTP |
| Electronics | 8.766 | 48,3% | Nische |

### Kategorien-Konzentration (StoreInspect 508k App-Market-Share-Study)

Fragmentierte Kategorien mit weichen Leadern (Eintritts-Fenster offen):

- **Customer Support**: Leader 26,8% (WhatsApp) — fragmented
- **Analytics**: Leader 31,2% (Triple Whale) — fragmented
- **Upsell**: Leader 21,1% (BOGOS) — hochkompetitiv aber kein Monopol

Konzentrierte Kategorien (Vermeiden oder teurer Spielraum):

- Page Builders: PageFly 71,3%
- Wishlists: Swym 86,5%
- Subscriptions: Seal 61,0% (innerhalb Adopters)
- Reviews: Judge.me 58,6%
- Loyalty: Smile.io 55,0%

### Checkout-Extensibility (Green-Field-Signal)

- Checkout API v2 ab 22.01.2026 Pflicht (alte Checkout-liquid deaktiviert)
- UI-Extensions nun auf ALLEN Paid-Plans, vorher nur Plus
- Loyalty-at-Checkout als nativer Slot — neu — Top-3-Incumbents haben noch keinen etablierten BFS-Status in diesem Surface
- Pre-Purchase Upsell belegt 5-10% AOV-Lift in 30 Tagen

### Shopify-Native-Kill-List (Kategorien absorbiert bis 2027)

- **Product Descriptions** (Shopify Magic) — absorbiert, existierend
- **Alt-Text-Generation** (Shopify Magic) — absorbiert
- **Basic-SEO-Meta** (Shopify Magic + Semantic Density 2026) — absorbiert
- **Simple A/B-Testing** (Shopify Rollouts) — absorbiert (Winter 26)
- **Basic SMS** (Shopify Messaging, native) — absorbiert
- **Shopify Subscriptions App** (native, free) — existiert aber schwach (3,6 Sterne)
- **Theme-Generation** (Shopify Tinker) — absorbiert
- **Product-Data-Scraping aus Manufacturer-PDFs** (Magic) — absorbiert Winter 26

**Merchanthaltung:** "Warning: Shopify AI hallucinates technical data and sabotages strategic SEO" (Shopify Community Februar 2026) — Native-Tools liefern Quality-Lücke, die Premium-Apps mit Verifizierungsworkflow füllen können. Aber **risky** wenn Shopify Q-Updates schneller werden.

---

## Shortlist: 5 konkrete App-Ideen

### App-Idee 1 — CheckoutLoyal DACH: Loyalty-Punkte-Redemption im Checkout Side-Rail für deutschsprachige Stores

**Problem:** Loyalty-Apps (Smile.io, Growave, Rivo) leben historisch im Account-Bereich oder als On-Page-Widget. Mit Checkout API v2 wird Loyalty-Redemption-im-Side-Rail der neue Standard. DACH-Stores haben 84,9% Loyalty-Gap und 6,6% nationale Adoption. Kein Top-3-Player hat 2026 eine native-deutsche Checkout-Loyalty-Extension, die mit Trusted Shops, TDDDG-conform und Points-Engine-light kommt.

**Zielgruppe:** DACH Shopify-Stores mit 30k-200k Monatstraffic (Plus-Kandidaten), Home & Garden + Hobby + Food & Beverage, die bisher kein Loyalty-Tool nutzen.

| Feld | Wert |
|---|---|
| name | CheckoutLoyal DACH |
| description | Loyalty-Redemption + Punkte-Display nativ im Checkout Side-Rail mit deutscher UI, Trusted-Shops-Badge-Slot, GDPR/TDDDG-konformer Consent-Flow |
| category_slug | loyalty-and-rewards + checkout-extensions |
| demand_signal | 84,9% der Meta-Ads-Stores ohne Loyalty (StoreInspect), Checkout-UI-Extensions Januar 2026 neu auf Non-Plus-Plans, 72% der DE-Kunden wollen UX in Muttersprache |
| competitor_count | ~15 Loyalty-Apps mit Checkout-UI-Extension, davon 0 mit dediziertem DACH-Fokus (Stand April 2026). Kaching Subscriptions/BLOY sind die Nahkonkurrenten |
| top_competitor_review_count | Smile.io 6.000+ Reviews, Growave 2.000+, BLOY <200, Rivo 2.000+. Aber: Checkout-Extension-Surface ist neu, Reviews dort noch <50 je App |
| category_growth | Ja, getrieben durch Checkout-API-v2-Rollout und "Retention is core experience" (Shopify Winter 26 Statement) |
| review_velocity_benchmark | Top-Apps: 20-40 Reviews/Monat. Checkout-Extension-Segment: <5/Monat (Green-Field) |
| ai_toolkit_buildable_bool | Partial ja. AI Toolkit deckt Checkout-UI-Extension-Scaffolding, GraphQL-Schemas, Polaris-Components ab. Points-Engine (Earn-Rules, Background-Jobs, Queue) muss manuell strukturiert werden, ist aber mit Claude Code + Gadget.dev machbar |
| build_time_weeks_solo_nocode | Optimistisch 10 Wochen MVP, konservativ 16 Wochen inklusive DACH-Compliance + BFS-Prep |
| required_skills | GraphQL-Lesen, JSON-Config, OAuth-Flow verstehen, Prompt-Iteration, Polaris-Component-Matching, Basic-Debugging, Vertrags-Bewusstsein (AVV, DPA) |
| api_deprecation_exposure | Niedrig. Checkout UI Extensions API v2 ist neu. Keine Script-Abhängigkeit. Keine Legacy-REST-Nutzung nötig |
| maintenance_hours_per_week | 100 Installs: 3h/Wo. 500: 8h. 1000: 15h (Support-SLA-Treiber) |
| checkout_extensibility_surface_bool | true |
| documented_mrr_range | Loyalty-Apps solo: 5-20k USD MRR in 18 Monaten realistisch (BLOY Case, Rivo Growth Path). Kaching Bundle 6-fig. Checkout-Specialist-Subsegment: unverifiziert, schätzbar 3-10k USD MRR Jahr 1 |
| pricing_model_typical | Tiered basierend auf aktiven Mitgliedern oder Orders/Monat. 29/79/199 USD Breakpoints |
| install_to_paid_conversion | Loyalty-Kategorie: 8-15% typisch |
| revenue_share_band | 0% bis 1M USD ARR (Shopify Revenue Share Reform 2022 bleibt 2026) |
| exit_multiple_benchmark_ttm_revenue | 3-5x TTM Revenue (MicroAcquire Shopify-App-Median 2025) |
| primary_channel | Shopify App Store Search + DACH-SEO-Content ("Shopify Loyalty GDPR", "Shopify Kundenbindung Checkout") + Partner-Content (Latori, Etribes, Shopify-DACH-Agenturen) |
| store_ranking_mechanism | Installs-Velocity erste 28 Tage + Review-Rating + BFS-Badge-Signals (Dashboard <500ms, Design, GraphQL-only) |
| paid_ads_viability | Google Ads auf deutschsprachige Shopify-Long-Tail-Keywords rentabel wenn LTV >300 EUR. Meta Ads schwach |
| cac_estimate | 60-150 EUR (SEO-Content-Weighted Mix) |
| built_for_shopify_feasibility_1_10 | 7. Realistisch in 12 Monaten wenn AI-Toolkit-Stack diszipliniert, weil Category-Specific-BFS-Criteria moderat und Checkout-Extensions "neu" bedeutet Review-Team-Bar noch milder |
| platform_risk_score_1_10 | 4. Shopify kann Loyalty-Primitives bauen (siehe Subscriptions-Native), aber Points-Engine + Tier-Logic + Custom-Earn-Rules sind zu spezifisch für Shopify-Core. Shop-App integriert Loyalty aber nicht an allen Touchpoints |
| shopify_native_absorption_horizon_months | 24-30. Shopify hat Loyalty nicht native, Shop App hat schwache Primitives, Checkout UI Extension slot ist explizit für Partner-Apps ausgelegt |
| competition_risk | Mittel-hoch. Smile.io, Growave, Rivo werden DACH-Lokalisierung nachziehen innerhalb 12-18 Monaten. First-Mover-Advantage im Checkout-Extension-Surface existiert, muss aggressiv genutzt werden |
| compliance_cost_eur_eu | Setup 2.500-4.000 EUR (AVV-Templates, DSFA light, Legal-Review), laufend 150-300 EUR/mo (Hosting EU, Backups, Monitoring) |
| mandatory_webhooks_complexity | 2/5. Customer-Data-Request, Customer-Redact, Shop-Redact — Standard-Handler-Pattern, AI-Toolkit-Scaffolded |
| dach_localization_advantage_score | 9/10. Deutschsprachige Merchant-UI, Trusted-Shops-Badge-Integration, TDDDG-Consent, Lexoffice-Points-Export — jedes Einzel-Feature ist ein sichtbarer Moat |
| support_sla_required | Ja, 30-Min-Response für Technology Partner Track nötig wenn BFS angestrebt. Solo machbar mit Plain/Front + Timezone-Shifting |
| portfolio_compatibility_bool | true. Shared Points-Engine-Core + Checkout-Extension-Framework wiederverwendbar für Wishlist, Gift-Card-im-Checkout, Referral-at-Checkout |
| merchant_tier_fit | Shopify + Advanced + Plus (nicht Basic — Loyalty-Setup-Komplexität zu hoch für Basic-Merchant) |
| confidence_level | medium-high |
| uncertain | MRR-Range für Checkout-Extension-Specialist-Subsegment — keine 2026-dokumentierten Solo-Cases öffentlich. Annahme: erste-12-Monate-Benchmark 30-50% unter klassischem Loyalty-App weil Top-of-Funnel fehlt |

---

### App-Idee 2 — DACHGuard Checkout: Trusted Shops Badge + TDDDG-Consent + Lexoffice-Handoff als Checkout-Extension-Stack

**Problem:** DACH-Shopify-Stores brauchen (1) Trusted-Shops-Siegel visuell im Checkout, (2) TDDDG-konformen Cookie/Tracking-Consent vor Payment, (3) strukturierte Rechnung zu Lexoffice für GoBD. Aktuell drei separate Apps (Consentmo, Trusted-Shops-App, Lexware-Office). Keine integriert im Checkout selbst. TDDDG (Telekommunikation-Digitale-Dienste-Datenschutz-Gesetz) erzwingt spezifische Consent-Patterns.

**Zielgruppe:** DACH-Shopify-Stores 20k-500k Monatstraffic, die regulatorisch "clean" verkaufen müssen (Beauty, Food, Supplements, Home & Garden).

| Feld | Wert |
|---|---|
| name | DACHGuard Checkout |
| description | Checkout-Extension-App, die Trusted-Shops-Badge im Checkout rendert, TDDDG-Consent-Gateway vor Payment erzwingt und Order-Daten strukturiert an Lexoffice pusht |
| category_slug | store-management-store-security + marketing-lead-capture + finances-accounting |
| demand_signal | 84 Mrd EUR DE-E-Com-Markt, TDDDG seit 2024 aktiv, Consentmo dominiert aber sitzt nicht im Checkout, Trusted-Shops-App hat <200 Reviews trotz 40k DACH-Merchants mit Trusted-Shops-Konto |
| competitor_count | 0 direkte Checkout-Extension-Integration (Stand April 2026). Consentmo (Consent), Trusted Shops (Badge), Lexoffice-App (Accounting) — drei getrennte Silos |
| top_competitor_review_count | Consentmo 3.500+, Trusted Shops App <300, Lexware Office 250+ (4,4 Sterne) |
| category_growth | Ja. TDDDG-Enforcement steigt, Shopify Winter 26 hat Agentic Storefronts aktiviert — Consent-Komplexität wächst |
| review_velocity_benchmark | 10-20/Monat für Consentmo, <5/Monat für Trusted Shops App |
| ai_toolkit_buildable_bool | Ja. Checkout UI Extension + GraphQL Admin API + Webhooks sind AI-Toolkit-Primitives. Lexoffice-API ist REST — Claude Code handled, AVV-Prozess muss manuell geschrieben werden |
| build_time_weeks_solo_nocode | Optimistisch 8 Wochen, konservativ 14 Wochen |
| required_skills | GraphQL-Lesen, REST-API-Config (Lexoffice), Legal-Template-Verstehen (AVV), GDPR-Text-Compliance, JSON-Config |
| api_deprecation_exposure | Niedrig |
| maintenance_hours_per_week | 3-6h/Wo plus Quartals-Legal-Review |
| checkout_extensibility_surface_bool | true |
| documented_mrr_range | Compliance-App-Segment: 5-15k USD MRR (Consentmo-Skalen sind höher aber seit 2016). DACH-Spezial: 3-10k USD MRR Jahr 1 realistic, 15k+ bei Partner-Deal mit Trusted Shops |
| pricing_model_typical | Flat monthly 49-149 EUR, Plus-Tier mit Lexoffice-Sync 199+ EUR |
| install_to_paid_conversion | Compliance: 12-20% (hohe Pain-Intensity) |
| revenue_share_band | 0% bis 1M USD |
| exit_multiple_benchmark_ttm_revenue | 3-5x TTM, Compliance-Apps eher am oberen Ende wegen Sticky-Revenue |
| primary_channel | DACH-Content-SEO ("Shopify TDDDG", "Shopify Lexoffice"), Partner-Listing bei Trusted Shops + Lexware, Shopify-Agentur-Netzwerk |
| store_ranking_mechanism | Category-specific BFS-Kriterien + DACH-Recommendations-Collection (apps.shopify.com/collections/recommendations-for-germany) |
| paid_ads_viability | Google-Ads auf DACH-Compliance-Terms rentabel, LTV hoch |
| cac_estimate | 80-180 EUR |
| built_for_shopify_feasibility_1_10 | 8 |
| platform_risk_score_1_10 | 3. Shopify wird DACH-Compliance niemals nativ lösen — regulatorisches Feld, zu fragmentiert |
| shopify_native_absorption_horizon_months | 36+ |
| competition_risk | Niedrig-mittel. Consentmo kann nachziehen, aber Checkout-Extension-First-Mover ist vorne. Trusted-Shops-Owned-Solution wäre das echte Risiko — aber Trusted Shops hat historisch schwache Product-Execution |
| compliance_cost_eur_eu | Setup 4.000-7.000 EUR (Anwalt für AVV + TDDDG-Gutachten), laufend 300-500 EUR/mo |
| mandatory_webhooks_complexity | 3/5 (Consent-Audit-Log-Persistenz treibt Komplexität) |
| dach_localization_advantage_score | 10/10 |
| support_sla_required | Ja, Compliance-Fragen verlangen kurze Response. B2B-tier macht das leichter handhabbar |
| portfolio_compatibility_bool | true. Consent-Engine + Webhooks-Core wiederverwendbar für separate Lexoffice-Sync-App, separate Trusted-Shops-Reviews-App |
| merchant_tier_fit | Shopify + Advanced + Plus |
| confidence_level | medium |
| uncertain | Ob Trusted Shops bereit ist offizielle Partnerschaft zu geben. Muss abgeklärt werden. Ohne Partnership ist Badge-Rendering-Feature nur marginal differenziert |

---

### App-Idee 3 — RestockHeld: Niche-Back-in-Stock für Home & Garden + Automotive Plus-Stores mit Seasonal-Forecasting

**Problem:** Back-in-Stock-Kategorie hat 2,28% Adoption (nur 10.809 von 474.871 Stores), Top-App "Back in Stock" 7.574 Installs, "Notify Me!" 2.677. Home & Garden hat 1,73% Adoption (41.348 Stores ohne App), Automotive 1,58% (7.773 Stores ohne App). Automotive-Stores haben die höchste Retention-Gap (51,7%) und gleichzeitig saisonale Nachfrage-Patterns, die Generic-Apps nicht modellieren.

**Zielgruppe:** Plus + Mid-Market Home & Garden / Automotive / Hobby-Stores mit 50k-200k Monatstraffic (3,1 Apps-avg, 59,5% Plus-Penetration — budget-starkes Segment).

| Feld | Wert |
|---|---|
| name | RestockHeld |
| description | Back-in-Stock + Pre-Order + Seasonal-Forecast-Apprisal für Home-Garden und Automotive, integriert mit Lieferanten-ETA und E-Mail-Sequences, deutschsprachige UI |
| category_slug | store-management-inventory-stock-management |
| demand_signal | 41.348 Home-Garden-Stores ohne App, 7.773 Automotive ohne App, Retention-Gap 42,9% bzw 51,7%. Plus-Stores adoptieren Back-in-Stock bei 4,58% — eindeutiger Budget-Signal |
| competitor_count | 68 Seiten in Shopify App Store (~800+ Listings), aber dominierend nur 3 (Back-in-Stock, Notify Me!, STOQ). Niche-Differentiation leer |
| top_competitor_review_count | Back-in-Stock ~2.500+, Notify Me ~1.800+, STOQ ~800+ |
| category_growth | Langsam-stetig. Shopify-Plus-Adoption wächst 5,4x schneller als Standard |
| review_velocity_benchmark | Top-3: 15-30/Monat |
| ai_toolkit_buildable_bool | Ja. Admin-App mit Webhooks (product/update, inventory_levels/update) + Email-Templates + Scheduler ist AI-Toolkit-Standardpfad |
| build_time_weeks_solo_nocode | 6-10 Wochen MVP |
| required_skills | GraphQL-Lesen, JSON-Config, Email-Template-Handling, Cron-Scheduling-Verständnis, Prompt-Iteration |
| api_deprecation_exposure | Low. Product-webhook-API ist stabil. Inventory-API-Migration auf Graphql bereits seit 2025 |
| maintenance_hours_per_week | 2-5h/Wo |
| checkout_extensibility_surface_bool | false (primary) — optional "Notify me" im Produkt-Page (Theme-App-Extension) |
| documented_mrr_range | Back-in-Stock-Segment: 2-10k USD MRR solo (Notify Me Story 25k USD MRR in einem Jahr — aber mit stärkerem Team). Niche-Vertical-Positioning: 3-8k USD MRR realistisch |
| pricing_model_typical | Tiered by notifications/month. 19/49/99 USD Breakpoints |
| install_to_paid_conversion | 10-15% |
| revenue_share_band | 0% bis 1M USD |
| exit_multiple_benchmark_ttm_revenue | 3-4x TTM |
| primary_channel | Shopify App Store Search + Niche-SEO ("Shopify Back in Stock Automotive", "Shopify Restock Home & Garden") |
| store_ranking_mechanism | Installs-Velocity + Niche-Reviews (Authenticity-Trigger für Algorithm) |
| paid_ads_viability | Niedrig. Category ist Search-intent-getrieben |
| cac_estimate | 40-80 EUR |
| built_for_shopify_feasibility_1_10 | 7 |
| platform_risk_score_1_10 | 5. Shopify könnte Back-in-Stock native bauen (wie Subscriptions), aber Notification-Copy + Forecasting sind Partner-safer-Space. Mittleres Risiko |
| shopify_native_absorption_horizon_months | 18-24 (Shopify Magic kann Forecasting triggern, aber Delivery-Layer bleibt Partner-Land) |
| competition_risk | Mittel. Niche-Positioning schützt vor Generic-Apps, aber andere Solo-Devs können gleiche Nische erkennen |
| compliance_cost_eur_eu | 1.500-2.500 EUR Setup, 100-200 EUR/mo laufend |
| mandatory_webhooks_complexity | 2/5 |
| dach_localization_advantage_score | 6/10 |
| support_sla_required | Ja, aber Low-Touch |
| portfolio_compatibility_bool | true. Notification-Engine wiederverwendbar für Low-Stock-Alerts, Price-Drop-Alerts, Preorder-Wait-Lists |
| merchant_tier_fit | Shopify + Advanced + Plus (Mid-Market sweet spot) |
| confidence_level | medium-high |
| uncertain | Ob DACH-Niche-Lokalisierung ausreicht um Notify Me! global zu schlagen. Annahme: innerhalb DACH ja, international nein |

---

### App-Idee 4 — NicheAnalytics 45k: Attribution + Retention-KPIs für Home & Garden Plus-Stores

**Problem:** Analytics-Kategorie ist fragmentiert (Leader Triple Whale 31,2%, fünfstellige Enterprise-Pricing). 97,9% aller Stores haben keine Dedicated-Analytics-App. Home-Garden + Fashion + Food&Beverage-Stores brauchen Kategorie-spezifische KPIs (Saisonalität, Wiederkauf-Zyklus, Bundle-AOV), die Triple-Whale-Generic-Dashboards nicht liefern. 50k-200k-Traffic-Stores haben 3,1 Apps-avg + 81% Decision-Maker-Contact-Rate — WTP gegeben.

**Zielgruppe:** Plus-Stores 50-200k Traffic, Home & Garden + Food & Beverage + Hobby.

| Feld | Wert |
|---|---|
| name | NicheAnalytics 45k |
| description | Kategorie-spezifische Analytics-Dashboards für Home/Garden/Food/Hobby Plus-Stores — Saisonalität, Wiederkauf-Zyklus, Bundle-AOV, Ad-Attribution, alles in deutscher UI |
| category_slug | store-data-analytics |
| demand_signal | 97,9% Analytics-Gap, 41,3k Home-Garden-Stores ohne Retention-Tool, Triple Whale Pricing €199-€21k/mo macht Lower-Mid-Market underserved |
| competitor_count | 30+ Analytics-Apps, aber <5 mit Vertical-Positioning |
| top_competitor_review_count | Triple Whale ~2.000, Lifetimely ~600, Peel ~300 |
| category_growth | Ja, AI-attributed orders 11x YoY seit Agentic-Storefronts-Rollout |
| review_velocity_benchmark | 10-25/Monat für Top-Apps |
| ai_toolkit_buildable_bool | Partial. Dashboard + GraphQL-Pulls + Polaris-Charts baubar. Attribution-Modeling (Multi-Touch, Server-Side-Pixel) ist Grenzbereich — benötigt produktiv mehr als Claude Code, z.B. Gadget.dev für Managed-Infrastructure |
| build_time_weeks_solo_nocode | 14-22 Wochen (Daten-Pipeline macht Scope) |
| required_skills | GraphQL-Lesen, Basic-SQL-Verständnis, Chart-Bibliothek-Auswahl, Aggregation-Queries-Debuggen. Anspruchsvollster Solo-Pfad der Shortlist |
| api_deprecation_exposure | Low-medium (Admin API 2025-10 ist Baseline) |
| maintenance_hours_per_week | 5-12h/Wo (Daten-Quality-Issues) |
| checkout_extensibility_surface_bool | false |
| documented_mrr_range | Analytics-Solo: 5-20k USD MRR in 18 Monaten (Lifetimely-Story, Mantle-Techtonic-Report) |
| pricing_model_typical | Tiered by GMV tracked. 99/299/599 USD Breakpoints |
| install_to_paid_conversion | 5-10% (niedriger weil Setup-Komplexität) |
| revenue_share_band | 0% bis 1M USD |
| exit_multiple_benchmark_ttm_revenue | 4-6x TTM (höher wegen Data-Moat) |
| primary_channel | Content-SEO tief, Partner mit Agenturen, Case-Studies |
| store_ranking_mechanism | Rating + BFS |
| paid_ads_viability | Hoch (Keyword "Shopify attribution German") |
| cac_estimate | 200-400 EUR |
| built_for_shopify_feasibility_1_10 | 6 |
| platform_risk_score_1_10 | 6. Shopify-Analytics native ist 2026 stark, Magic-Reports kommen. Aber Vertical-KPIs bleiben Partner-safer |
| shopify_native_absorption_horizon_months | 12-18 für Generic-Metriken, 24+ für Vertical-spezifische |
| competition_risk | Hoch. Triple-Whale + Peel + Lifetimely können DACH-Version in 6 Monaten bauen |
| compliance_cost_eur_eu | 3.000-5.000 Setup, 200-400/mo |
| mandatory_webhooks_complexity | 3/5 |
| dach_localization_advantage_score | 7/10 |
| support_sla_required | Ja, B2B-Analytics erwartet <4h Response |
| portfolio_compatibility_bool | false (Category-spezifische Codebase schwer zu splitten) |
| merchant_tier_fit | Advanced + Plus |
| confidence_level | medium |
| uncertain | Build-Time für Solo-No-Coder mit AI-Toolkit. Daten-Pipeline ist der Bottleneck. Wahrscheinlich 1,5x der konservativen Schätzung realistisch |

---

### App-Idee 5 — FlexShip DACH: Shopify Functions für DACH-Versandregeln (DHL, Hermes, GLS, Deutsche-Post-Integration + Conditional-Shipping)

**Problem:** Shopify Scripts werden 30.06.2026 endgültig abgeschaltet. Jeder Plus-Store mit Custom-Shipping-Logic muss migrieren. DACH-Stores brauchen spezifische Logik: DHL-Paket vs Warenpost, Hermes-Pickup-Points, GLS-FlexDeliveryService, Deutsche-Post-Warenpost für <500g. Generic-Shipping-Functions-Apps sind US-first. Kein DACH-Carrier-Pack dominiert.

**Zielgruppe:** Plus-Stores mit DACH-Fulfillment (Fashion, Food & Beverage, Home & Garden).

| Feld | Wert |
|---|---|
| name | FlexShip DACH |
| description | Shopify-Functions-basierte Shipping-Rules für DACH-Carrier (DHL, Hermes, GLS, Deutsche Post), Weight/Zone/Fragility-Logic, Billbee-Handoff |
| category_slug | store-management-shipping-and-delivery |
| demand_signal | Script-Deprecation 30.06.2026 zwingt Migration. DACH-Shopify-Plus-Base ca. 2.000-5.000 Stores. Billbee dominiert DACH-Fulfillment-Backend — komplementär nicht konkurrierend |
| competitor_count | PowerX, Functions Creator, Function Studio — alles generic, keine DACH-Carrier-Native |
| top_competitor_review_count | PowerX ~150, Functions Creator ~100, Function Studio <50 |
| category_growth | Spike 2026 wegen Script-Deprecation |
| review_velocity_benchmark | 3-10/Monat |
| ai_toolkit_buildable_bool | Ja, aber Functions benötigen WebAssembly-Kompilierung und Instruction-Limits (11M), AI-Toolkit-Skill shopify-functions deckt das ab. JS-Functions slower als Rust aber non-coder realistisch |
| build_time_weeks_solo_nocode | 8-12 Wochen |
| required_skills | Shopify-Functions-Metafield-Config, JSON-Rules-Schema-Design, Carrier-API-Basics, GraphQL-Lesen |
| api_deprecation_exposure | Low (Functions sind Nachfolger von Scripts, 2026+ long-horizon) |
| maintenance_hours_per_week | 3-6h/Wo |
| checkout_extensibility_surface_bool | true (Functions + Delivery-Customization-UI-Extension) |
| documented_mrr_range | Functions-Specialist-Apps: 3-12k USD MRR (PowerX-Trajectory unpublished). Nischenfokus DACH: 5-15k realistic wenn 200+ Plus-Stores konvertiert |
| pricing_model_typical | Flat monthly 49-199 EUR |
| install_to_paid_conversion | 15-25% (Script-Migration-Urgency) |
| revenue_share_band | 0% bis 1M USD |
| exit_multiple_benchmark_ttm_revenue | 3-5x TTM |
| primary_channel | DACH-Shopify-Plus-Agency-Network + direkter Outreach + SEO ("Shopify Scripts Migration DACH") |
| store_ranking_mechanism | Plus-Merchant-Reviews schwerer, aber qualitativ hochwertig |
| paid_ads_viability | Eher Agency-Deals als Ads |
| cac_estimate | 150-300 EUR |
| built_for_shopify_feasibility_1_10 | 7 |
| platform_risk_score_1_10 | 4. Shopify wird DACH-Carrier-Mapping nie nativ lösen |
| shopify_native_absorption_horizon_months | 36+ |
| competition_risk | Niedrig-mittel. Script-Migration-Zeitfenster schließt im Juli 2026 — First-Mover-Advantage ist jetzt |
| compliance_cost_eur_eu | 2.000-3.500 EUR Setup, 150-250/mo |
| mandatory_webhooks_complexity | 2/5 |
| dach_localization_advantage_score | 9/10 |
| support_sla_required | Ja, Plus-Tier erwartet Premium-Support |
| portfolio_compatibility_bool | true. Functions-Framework wiederverwendbar für Discount-Rules-DACH, Payment-Hide-DACH, Bundle-Validation |
| merchant_tier_fit | Plus primary |
| confidence_level | medium |
| uncertain | Ob Solo-No-Coder Functions-Debugging-Complexity bei Edge-Cases (Instruction-Limits bei 80+ Line-Items) in realistischer Zeit löst |

---

## Ranking-Matrix (Base Rate für 5-25k USD MRR in 12 Monaten)

| # | App-Idee | Build-Time | Platform-Risk | DACH-Advantage | Competition | Overall-Rank |
|---|---|---|---|---|---|---|
| 1 | CheckoutLoyal DACH | 10-16 Wo | 4/10 | 9/10 | Mittel-hoch | A |
| 2 | DACHGuard Checkout | 8-14 Wo | 3/10 | 10/10 | Niedrig-mittel | A |
| 3 | FlexShip DACH | 8-12 Wo | 4/10 | 9/10 | Niedrig-mittel | A- |
| 4 | RestockHeld | 6-10 Wo | 5/10 | 6/10 | Mittel | B+ |
| 5 | NicheAnalytics 45k | 14-22 Wo | 6/10 | 7/10 | Hoch | B |

**Empfehlung für Ilias:** Start mit Idea 2 (DACHGuard Checkout) oder 3 (FlexShip DACH). Beide haben niedrigste Platform-Risk, hohen DACH-Localization-Moat, kürzeste MVP-Timeline und fallen nicht in Shopify-Native-Absorption-Horizon <24 Monate. Idea 1 (CheckoutLoyal) ist größer, aber risikoreicher wegen Loyalty-Incumbent-Nachzug.

---

## Kill-List: Apps, die NICHT gebaut werden sollten

| Kategorie | Grund |
|---|---|
| Product-Description-Generator | Shopify Magic bereits native |
| Alt-Text-Generator | Shopify Magic bereits native |
| Basic-SEO-Meta | Shopify Magic + Semantic Density 2026 absorbiert |
| A/B-Testing | Shopify Rollouts ist native 2026 |
| Simple SMS Marketing | Shopify Messaging ist native |
| Generic Subscriptions | Shopify Subscriptions App native (wenngleich schwach) |
| Theme-Generator | Shopify Tinker native |
| Generic Review-Collection | Judge.me 58,6% + Shopify Reviews kommend |
| Email-Only-Marketing | Klaviyo 57,6% + Shopify Email native |

---

## Sources and References

1. [State of Shopify 2026: 376K+ Stores Analyzed — StoreInspect](https://storeinspect.com/report/state-of-shopify)
2. [Shopify Retention Gap, 358,686-Store Study — StoreInspect](https://storeinspect.com/blog/shopify-retention-gap)
3. [Shopify App Market Share, 508,680-Store Study — StoreInspect](https://storeinspect.com/blog/shopify-app-market-share)
4. [Best Shopify Back in Stock Apps, 475K-Store Study — StoreInspect](https://storeinspect.com/blog/best-shopify-back-in-stock-apps)
5. [Best Shopify Subscription Apps, 154,065-Store Study — StoreInspect](https://storeinspect.com/blog/best-shopify-subscription-apps)
6. [What Services Do Shopify Stores Actually Need, 120k-Store Gap Analysis — StoreInspect](https://storeinspect.com/blog/what-services-do-shopify-stores-need)
7. [Shopify Checkout UI Extensions — Shopify Dev Docs](https://shopify.dev/docs/api/checkout-ui-extensions/latest)
8. [Shopify Functions Language Considerations — Shopify Dev Docs](https://shopify.dev/docs/apps/build/functions/programming-languages)
9. [Shopify Updates 2026 — Mettevo](https://mettevo.com/blog/article/shopify-updates-2026-all-latest-news-features-changes)
10. [Apps for German Businesses Collection — Shopify App Store](https://apps.shopify.com/stories/guide-built-for-germany)
11. [Shopify Checkout Extensibility Migration 2026 — Redliodesigns](https://redliodesigns.com/blog/checkout-extensibility-migration-2026-guide-for-ctos)
12. [Shopify Sidekick 2026 Features — Presta](https://wearepresta.com/shopify-sidekick-features-2026-the-merchants-guide-to-agentic-commerce/)
13. [Shopify Magic Warning Thread — Shopify Community](https://community.shopify.com/t/warning-shopify-ai-sidekick-magic-hallucinates-technical-data-and-sabotages-strategic-seo/589483)
14. [Built for Shopify Requirements — Shopify Dev Docs](https://shopify.dev/docs/apps/launch/built-for-shopify/requirements)
15. [Shopify GDPR/TDDDG Analysis — Latori](https://www.latori.com/en/blogpost/shopify-dsgvo)
16. [Billbee Review 2026 — Qualimero](https://qualimero.com/en/blog/billbee-review-features-costs-automation-limits)
17. [StoreInspect Analytics Fragmentation 2026](https://storeinspect.com/blog/shopify-app-market-share)

---

## Confidence and Uncertainty Notes

- **High confidence**: StoreInspect Zahlen (direkte Primärquelle, April 2026), Shopify-Native-Absorption-List, Checkout-Extensibility-Surface-Neuheit
- **Medium confidence**: MRR-Ranges pro App-Idee (abgeleitet aus Category-Medians, keine Solo-DACH-Primärquellen)
- **Uncertain**: Konkrete Partnership-Verfügbarkeit für Trusted-Shops/Lexoffice (nicht recherchiert). Solo-Build-Time für NicheAnalytics (Pipeline-Scope schwer schätzbar ohne Prototyp)
