# C4 — Quit-or-Stay Decision Matrix

**Kontext:** Solo Operator, Düsseldorf, DACH, BWL-Hintergrund, kein Coding, kein Vertriebsnetzwerk, kein Ad-Budget. GetKiAgent pre-revenue (Customer-Support-Automation, n8n-basiert). Frage: Vollzeit gehen — ja / nein / wann?

**Methodisches Vorwort:** Alle EUR-Zahlen sind entweder gesourct (Link) oder als `[estimated]` markiert. Die Recherche ist brutal ehrlich — keine Pep Talks. Wenn die Zahlen "bleib angestellt" sagen, steht das auch so drin.

---

## 1) 30 / 60 / 90-Tage-Meilensteine, die rational Vollzeit rechtfertigen

Die Literatur zu Solo-Foundern ist sich einig: **Vollzeit ist erst dann rational, wenn Umsatz schon validiert läuft — nicht umgekehrt.** Konsens-Framework aus mehreren Quellen:

> **"Quit when (runway > 12 months) AND (MRR > $3K) AND (3 consecutive months of growth)."**
> — [SoftwareSeni: Solo Founder SaaS Metrics 2025](https://www.softwareseni.com/solo-founder-saas-metrics-from-0-to-10k-mrr-in-6-months-with-realistic-timelines/)

Übersetzt auf den GetKiAgent-Kontext (B2B-Retainer statt SaaS-MRR, aber gleiche Logik):

### Meilenstein-Tabelle (GetKiAgent-spezifisch)

| Phase | Umsatz-Ziel | Kunden-Ziel | Qualitativ | Aktion |
|-------|-------------|-------------|------------|--------|
| **Tag 30** | 1 zahlender Pilot-Kunde @ min. 1.500 EUR Setup ODER 500 EUR/Monat | 1 | Signed Contract, nicht nur LOI | WEITER als Side-Hustle |
| **Tag 60** | Kumuliert 3.000 EUR Cash eingenommen + 2. Kunde in Pipeline (Termin steht) | 2 aktiv / 1 in Closing | Reply-Rate Outreach > 5%, Demo-to-Close > 20% | WEITER als Side-Hustle, Scope prüfen |
| **Tag 90** | 2.500 EUR MRR (oder Retainer-Äquivalent) — entspricht mind. 1 aktiver Retainer + wiederkehrende Setups | 2-3 zahlende | 3 Monate ununterbrochener Umsatz, Case Study aus Wave-1-Kunde publiziert | **Vollzeit prüfen — nur wenn Runway >= 12 Monate** |

### Warum diese Zahlen

- **2.500 EUR MRR ist das absolute Minimum**, nicht der Wunschwert. Die Düsseldorf-Fixkosten (siehe §2) liegen bei ca. 2.500-3.000 EUR/Monat inklusive KV und Rücklagen. MRR unter 2.500 = Substanzverzehr ab Tag 1.
- **3 Monate Wachstum in Folge** filtert Einmal-Projekte und Tier-A-Glück raus. Ein einzelner 5k-Setup im Monat 2 ist KEIN Beweis für Full-Time-Reife.
- **Die MRR-Zahl $3K aus der Literatur** wird bei Service-Agenturen traditionell höher angesetzt (6-8k MRR) weil die Marge niedriger ist als bei SaaS. Bei B2B-Retainer mit Dir als Solo-Operator darf 2.500 EUR als Floor durchgehen — aber nur weil n8n/API-Kosten und Agent-Setup vergleichsweise niedrig sind.
- **Indie-Hackers-Basisraten:** [SoftwareSeni benchmark](https://www.softwareseni.com/solo-founder-saas-metrics-from-0-to-10k-mrr-in-6-months-with-realistic-timelines/) zeigt realistische Timelines: $1K MRR in Monat 2-4, $3K in Monat 4-8, $5K in Monat 6-12. Medianfall: ~6 Monate bis $3K. Dein 90-Tage-Ziel ist aggressiv aber nicht unmöglich.
- **30% aller Micro-SaaS-Ventures erreichen nie $1K MRR** (Quelle: dto.). Das ist der nackte Survivorship-Bias-Korrektur-Wert.

### Was NICHT als Meilenstein zählt

- LOIs, "wir melden uns nächste Woche", interessierte Anfragen → **nicht zählbar**
- Einmaliger Setup-Erlös ohne Retainer-Konversion → Projektgeschäft, kein Business
- Kunden, die Du aus dem persönlichen Umfeld hast → kein Proof für Vertriebskanal
- Wave-1 Tier-A Leads ohne Close → Pipeline ist nicht Umsatz

---

## 2) Minimaler Runway in Monaten bei DE-Lebenshaltung

### Düsseldorf Fixkosten Single (realistisch, 2025/2026)

| Posten | EUR/Monat | Quelle |
|--------|-----------|--------|
| Miete warm (1-Zimmer-Wohnung Düsseldorf, keine Top-Lage) | 900-1.100 | [Düsseldorf 15,58 EUR/qm, WiWi-TReFF Praxis-Bericht](https://themen.kleinanzeigen.de/magazin/ratgeber/lebenshaltungskosten-duesseldorf/) |
| Lebensmittel / Alltag | 400-500 | [beatvest Durchschnitt Single DE](https://www.beatvest.com/blog/lebenshaltungskosten-in-deutschland) |
| Krankenversicherung freiwillig GKV (Mindestbeitrag Selbstständige) | 230-260 | [Mindestbemessungsgrundlage 1.248,33 EUR/Monat 2025](https://marcusknispel.com/mindestbemessungsgrundlage-selbststaendige/) |
| Strom / Internet / Handy | 100-130 | [estimated] |
| Transport (ÖPNV / ggf. Auto) | 60-200 | [estimated] |
| Software-Stack GetKiAgent (n8n self-host, Claude API, Apollo, Gmail Workspace, Hosting) | 150-300 | [estimated] |
| Steuerberater, Versicherungen (Haftpflicht, BU kosten extra), Buchhaltung | 150-250 | [estimated] |
| Puffer (Reparaturen, Geburtstage, Nachzahlungen) | 200 | [estimated] |
| **Summe konservativ** | **2.200-2.950** | |
| **Summe mit Komfort** | **ca. 3.200** | |

Deine eigene Einschätzung (2.000-2.500 EUR) ist am **unteren Rand** — ohne KV-Mindestbeitrag und ohne Business-Kosten. Realistisch sind **2.500-3.000 EUR Brutto-Bedarf/Monat**, weil Du als Selbstständiger zusätzlich 230 EUR KV, Steuern auf jeden Euro und Business-Tooling trägst.

### Runway-Berechnung

**Konsens-Richtwert aus der Literatur:** 12-18 Monate Runway, nicht weniger.

> "Safe transition requires 12-18 months runway plus $3K-$5K MRR already validated before you quit."
> — [Puzzle.io Founder Runway Guide 2025](https://puzzle.io/blog/how-to-calculate-your-runway-a-guide-for-founders)

> "Bootstrapped founders should have 6-12 months runway at pre-seed stage — but later stages need 18-24 months."
> — [Finvisor Startup Runway](https://finvisor.com/startup-runway/)

| Szenario | Burn/Monat | Minimaler Runway | Erforderliche Rücklage |
|----------|------------|------------------|------------------------|
| Lean (kein Komfort, 2.500 EUR) | 2.500 | 12 Monate | **30.000 EUR** |
| Realistisch (2.800 EUR) | 2.800 | 15 Monate | **42.000 EUR** |
| Sicher (3.200 EUR + Puffer für Steuer-Nachzahlung) | 3.200 | 18 Monate | **57.600 EUR** |

**Harter Floor für GetKiAgent-Szenario (BWL, kein Code, kein Netzwerk):** 15 Monate Runway = **42.000 EUR Cash** auf dem Konto, BEVOR der Vertrag gekündigt wird. Weniger = Russisches Roulette.

### Gründungszuschuss als teilweiser Hebel

Falls Du erst in ALG-1 gehst und dann gründest: [Gründungszuschuss = ALG-I-Betrag + 300 EUR Sozialpauschale für 6 Monate, weitere 9 Monate nur 300 EUR](https://www.arbeitsagentur.de/arbeitslos-arbeit-finden/arbeitslosengeld/gruendungszuschuss-beantragen). Typischer Gesamtbetrag: **10.000-15.000 EUR** über 15 Monate. **Aber:** Kann-Leistung, kein Rechtsanspruch. Voraussetzung: noch 150 Tage ALG-I-Restanspruch zum Antrag. [Details Gruenderkueche](https://www.gruenderkueche.de/fachartikel/gruendungszuschuss-anspruch-antrag-hoehe-voraussetzungen/)

**Taktische Option:** Nicht selbst kündigen (dann 3 Monate Sperrzeit), sondern Aufhebungsvertrag mit Abfindung oder vom Arbeitgeber betrieblich bedingt kündigen lassen → sofort ALG-1 + später Gründungszuschuss.

---

## 3) Ehrlicher Worst Case nach 6 Monaten Vollzeit

Vier realistische Worst-Case-Pfade, geordnet nach Wahrscheinlichkeit basierend auf Basisraten:

### Worst Case A — "Kein einziger zahlender Kunde" (Wahrscheinlichkeit: 25-35%)

- 6 Monate Outreach, ca. 200-400 versendete personalisierte Emails, Reply-Rate unter 3%, 0 Closes
- Verbranntes Kapital: **15.000-18.000 EUR** (6 × 2.800 EUR Burn)
- Psychischer Zustand: Burnout-nah, Vertrauensverlust. Vergleichsfall José León: "[every time that I want to promote something, my stomach hurts](https://www.indiehackers.com/post/after-losing-38676-as-an-indie-hacker-i-cant-do-it-anymore-i-quit-8673223598)" — 1 Jahr, 60 USD Umsatz, 38.676 USD Verlust.
- **70% der Solo-Founder scheitern in den ersten 2 Jahren** vs. 40% bei Teams. [Hypertxt Why Solo Founders Fail](https://hypertxt.ai/blog/marketing/why-solo-founders-fail)

### Worst Case B — "Ein paar Setups, kein Retainer-Stack" (Wahrscheinlichkeit: 30-40%)

- 2-4 Setup-Projekte zu je 2k-4k EUR, keine Konversion in wiederkehrenden Retainer
- Bruttoumsatz Jahr: ~8.000-15.000 EUR — unter dem Burn
- Ergebnis: klassisches "Freelancer statt Agentur" — Gewerbe läuft, Lebensstandard fällt
- Rückweg in Festanstellung wird nach 6+ Monaten schwieriger: "[Arbeitgeber fürchten, dass Selbstständigkeit gescheitert ist und Sie nun Sicherheit suchen](https://top-jobs-europe.de/aus-der-selbststaendigkeit-zurueck-ins-angestelltenverhaeltnis-wenn-man-nicht-mehr-sein-eigener-chef-sein-moechte/)."

### Worst Case C — "Marktpassung da, aber Delivery-Engpass" (Wahrscheinlichkeit: 15-20%)

- 3-5 Kunden landen gleichzeitig, Du bist alleine, jede Stunde geht in Delivery, Vertrieb stirbt
- 9-12 Monate später kein Pipeline, alte Kunden churnen, Bruch-Moment
- Wird in Indie-Hackers-Interviews als "the messy middle" beschrieben: [Why Indie Founders Fail](https://www.indiehackers.com/post/why-indie-founders-fail-the-uncomfortable-truths-beyond-build-in-public-b51fd6509b)

### Worst Case D — "Psychologischer Kollaps" (Wahrscheinlichkeit: 10-15%, unterschätzt)

- Isolation, Druck, kein Feedback-Loop aus Kollegen → Produktivität fällt um bis zu 50% [Hypertxt]. Side-Effekt: Beziehung leidet (Leóns Fall), Gesundheit leidet, mentale Erholung nach Rückkehr in Job = 3-6 Monate.

### Kombinierte Worst-Case-Bilanz (wahrscheinlicher Median)

Nach 6 Monaten:
- **Cash weg:** 16.000-20.000 EUR
- **Umsatz:** 0-8.000 EUR brutto
- **Pipeline:** 1-3 laue Opportunities
- **Netto-Cashflow/Monat:** deutlich negativ (-2.000 bis -2.500 EUR)
- **Arbeitsmarkt-Wert:** leicht gesunken (Lücke im Lebenslauf, muss erklärt werden)
- **Psychologische Kosten:** nicht quantifizierbar, aber real

**Brutaler Realitäts-Check:** José León verlor **38.676 USD** über ~12 Monate, verdiente **60 USD**. Das ist nicht die Ausnahme — das ist statistisch ein wahrscheinlicher Pfad bei Solo ohne Netzwerk/Code/Budget.

---

## 4) Objektive Abbruchkriterien — Wann DEFINITIV stoppen

Setze die Kriterien **heute** schriftlich fest, bevor Emotion ins Spiel kommt. Verhandle später **nicht** mit Dir selbst.

### Hard-Stop-Regeln (einer reicht)

| # | Kriterium | Grund |
|---|-----------|-------|
| HS-1 | **Runway < 3 Monate** und MRR < 1.500 EUR | Mathematisch nicht mehr zu drehen, je länger Du wartest, desto teurer die Rückkehr |
| HS-2 | **Monat 6 Vollzeit, kumulierter Umsatz < 6.000 EUR** | Faktor-2-Unter-Ziel, klare Message vom Markt |
| HS-3 | **Monat 9 Vollzeit, MRR < 2.500 EUR** | Break-Even nicht in Sicht trotz 3/4 Jahr Vollgas |
| HS-4 | **6 Monate keinen einzigen Retainer-Kunden über 500 EUR/Monat** | Modell-Fehler, nicht Ausführungsfehler |
| HS-5 | **Reply-Rate Outreach nach 300 gezielten Kontakten < 2%** | Kanal funktioniert nicht, keine Pipeline = keine Zukunft |
| HS-6 | **Körperliche Symptome** (Schlafstörungen >2 Wochen, Panikattacken, Beziehungsbruch-Drohung) | Nicht verhandelbar. Gesundheit > Business |

### Soft-Warning-Signale (zwei oder mehr = Alarm)

- 3 Monate in Folge Monat-über-Monat Stagnation statt Wachstum
- Demo-to-Close-Rate < 10% über 10+ Demos
- Customer Acquisition Cost > Customer Lifetime Value (Du zahlst drauf)
- Du arbeitest 60+ Std/Woche und kommst trotzdem nicht zu Vertrieb
- Die letzten 3 "fast-Closes" kamen alle nicht zum Abschluss aus Preisgründen
- Du fängst an, Scope und Preis zu reduzieren um "überhaupt" etwas zu closen

### Gegenprobe zur Hartnäckigkeit

> "Most founders quit too late because they confuse being persistent with being in denial."
> — [Upsilon Startup Success and Failure Rate 2025](https://www.upsilonit.com/blog/startup-success-and-failure-rate)

Wenn mehr als 3 der Soft-Signale gleichzeitig rot sind und Du Dir sagst "aber in 2 Monaten wird's besser" — genau das ist Denial.

---

## 5) Hybrid-Pfad — Teilzeit/Befristung + Side-Business: RATIONAL?

### Kurze Antwort: JA. Sogar optimal für Deinen Profil-Typ.

Der Hybrid-Pfad ist die mathematisch überlegene Strategie für jemanden mit Deinem Profil (BWL, kein Code, kein Netzwerk, pre-revenue Product). Grund:

### Die Literatur ist eindeutig

> "Part-time validation phase — build to $1K-$3K MRR while employed before making the transition decision, which proves product-market fit and validates your acquisition channels without career risk."
> — [Puzzle.io Founder Runway Guide](https://puzzle.io/blog/how-to-calculate-your-runway-a-guide-for-founders)

> Lukas Hermann (Stagetimer, deutscher Bootstrapper): **Job gehalten bis ca. 3.000 EUR MRR** erreicht — **1,5 Jahre Side-Hustle**, erst DANN Vollzeit.
> — [lukashermann.dev Bootstrapping SaaS in Germany](https://lukashermann.dev/writing/bootstrapping-a-saas-business-in-germany/)

### Konkrete Hybrid-Varianten gerankt

| Variante | Vorteil | Nachteil | Ranking für Dich |
|----------|---------|----------|------------------|
| **A: Vollzeit-Job + Abend/WE (20h/W Business)** | Max. finanzielle Sicherheit, Runway baut sich auf | Langsam, 60+ Std Woche, Burnout-Risiko | **#2** — solide, aber zeitlich brutal |
| **B: 30h-Teilzeit-Job + 20-25h Business** | Mehr Fokus-Zeit, ~75% Netto, KV übers Angestelltenverhältnis | Nicht alle AGs machen mit, muss aktiv verhandelt werden | **#1** — ideal wenn machbar |
| **C: Befristung 6-12 Monate + Business-Vorbereitung** | Fester Endtermin zwingt zur Disziplin, Runway sparen | Kein langfristiges Commitment vom AG, weniger Hebel | **#3** — taktisch sinnvoll vor Full-Time-Sprung |
| **D: Werkstudent/20h nur wenn noch Studium aktiv** | Günstige KV/Steuer | Nicht passend für Dein Profil (BWL abgeschlossen) | **N/A** |
| **E: Freelance-Angestellt-Mix (3 Tage Kunde, 2 Tage GetKiAgent)** | Cashflow sofort, Vertriebs-Skills bauen | Verwässert Fokus, Selbstausbeutung | **#4** — nur falls A/B/C scheitern |

### Rechnung: Wie lange dauert Hybrid-Validierung?

Bei 20h/Woche Business und realistischer B2B-Outreach:
- Monat 1-3: Pipeline aufbauen, 1 Pilot
- Monat 4-6: 2-3 Kunden, ca. 1.500-2.500 EUR MRR
- Monat 7-12: Entscheidungspunkt — bei 3K+ MRR und wachsender Pipeline → kündigen, bei Stagnation → Modell prüfen

**12-18 Monate Hybrid ist der Standard-Pfad für DACH-Solo-Bootstrapper**, nicht die Ausnahme. [Sidepreneur-Community DE](https://www.sidepreneur.de/podcasts-fuer-unternehmer-und-gruender/) bestätigt: die Mehrheit der nachhaltigen Bootstrapper in DACH macht Side-Hustle 12-24 Monate bevor Vollzeit.

### Gegenargument gegen reinen Vollzeit-Sprung

Der einzige valide Grund für Vollzeit-Sprung ohne Hybrid-Phase: **Du hast bereits 3k+ MRR signiert vor Kündigung.** Das hast Du (noch) nicht. Also: Hybrid ist nicht "vorsichtig", Hybrid ist **die rationale Default-Entscheidung**.

---

## 6) Retrospektiven vergleichbarer Solo-NoCode-DACH-Gründer

### Direkte Vergleichsfälle (dokumentiert)

#### 6.1 Lukas Hermann — Stagetimer (Deutschland, Bootstrapper)

- **Profil:** Deutscher Solo-Founder, SaaS (nicht Agency, aber vergleichbares Muster)
- **Timeline:** Nov 2020 erster Commit → Jun 2021 erster zahlender Kunde (8 Monate) → Sep 2023 10k MRR (34 Monate)
- **Kritisch:** Behielt Job bis ~3k MRR erreicht, ging erst nach **~1,5 Jahren Side-Hustle** Vollzeit
- **DE-Spezifika:** KV als Hauptkosten-Shock, Einzelunternehmer vs. GmbH-Entscheidung, EU-MwSt.-Komplexität
- **Lesson für GetKiAgent:** Ramen Profitability brauchte **~2 Jahre**, nicht 3-6 Monate. Plan mit diesem Zeithorizont, nicht mit Influencer-Timelines.
- Quelle: [lukashermann.dev/writing/bootstrapping-a-saas-business-in-germany](https://lukashermann.dev/writing/bootstrapping-a-saas-business-in-germany/)

#### 6.2 José León — AfterQuit (Full-Time Indie Hacker)

- **Profil:** Ex-Developer-Advocate (nicht BWL, aber vergleichbar: kein Coder-Elite-Level, kein starkes Vertriebsnetz)
- **Start-Kapital:** ~12.000 USD = ca. 1 Jahr Runway (zu wenig)
- **Ergebnis nach 12 Monaten Vollzeit:** ~60 USD Umsatz, 38.676 USD Verlust, aufgab
- **Root Cause:** Marketing-Aversion + Isolation. Zitat: "[every time I want to promote something, my stomach hurts](https://www.indiehackers.com/post/after-losing-38676-as-an-indie-hacker-i-cant-do-it-anymore-i-quit-8673223598)"
- **Lesson:** Ohne aktives Vertriebs-Muskeltraining (oder Netzwerk) IST das Vertriebsloch der Killer. Nicht Produkt, nicht Tech.

#### 6.3 Jan Oberhauser — n8n (Deutschland, Allgäu)

- **Profil:** Autodidakt, kein BWL, baute n8n 2019 aus Schmerz heraus
- **Heute:** 2,5 Mrd. USD Bewertung, Unicorn
- **Lesson für GetKiAgent:** Tool-Builder-Exit sind nicht das Vergleichs-Profil. Du baust eine **Service-Agentur ON n8n**, keinen Tool-Konkurrenten. Relevanter Vergleich sind Agenturen wie [Xmethod](https://www.xmethod.de/) oder [RemodifyAI](https://www.remodifyai.com/n8n-experten) — diese haben Teams, VC-Backing oder langjährige Netzwerke. Du bist solo ohne Netzwerk.
- Quelle: [Business Insider Gründerszene n8n](https://www.businessinsider.de/gruenderszene/technologie/insider-bestaetigen-berliner-ai-agent-startup-n8n-mit-24-milliarden-bewertet/)

#### 6.4 Janik Nolden — Erstes Startup gescheitert (Gründer & Zünder Podcast)

- **Profil:** Deutscher Founder, erste Gründung scheiterte, dachte über Rückkehr in sichere Anstellung nach
- **Zitat:** Saß auf der Couch und beneidete seine Freundin um die Sicherheit einer Beamtenstelle
- **Ausgang:** Gründete erneut, aber nach Pause und Lernen
- **Lesson:** Scheitern ist in DACH nicht karriere-final, ABER es ist emotional brutal. Rechne damit und baue Rücklagen für 6 Monate Nachbearbeitung ein.
- Quelle: [Gründer & Zünder Podcast](https://derstartuppodcast.com)

### Community-Basisraten

- **[Indie Hackers Germany Group](https://www.indiehackers.com/group/germany)** — aktive Community, viele Stagnations-Posts, wenige Exits
- **80%+ der erfolgreichen Startups haben Co-Founder** — Solo-Founder brauchen 3× länger zu Zielen ([Indie Hackers Research](https://www.indiehackers.com/post/bad-news-for-solo-indie-hackers-building-alone-is-killing-your-startup-2901fb8332))
- **70% aller Solo-Founder scheitern in 2 Jahren** vs. 40% Team-Founder ([Hypertxt](https://hypertxt.ai/blog/marketing/why-solo-founders-fail))

### DACH-Spezifische Hürden (oft unterschätzt)

1. **Deutsche B2B-Kunden sind langsamer als US-Markt.** US-Founder berichten von 1-2 Monaten Sales-Cycle. DACH-Mittelstand: **3-6 Monate Sales-Cycle** Standard.
2. **US-Kunden zahlen 2-3× mehr** als DE-Kunden für vergleichbare Services [SoftwareSeni]. Wenn Deine Nische erlaubt: **global verkaufen, DE wohnen**.
3. **KV-Kostenschock:** 230+ EUR/Monat GKV-Mindestbeitrag sind nicht verhandelbar. Bei privater KV im jungen Alter evtl. günstiger, aber Falle bei Einkommens-Einbrüchen.
4. **Steuervorauszahlung:** Nach gutem Startjahr kommen Nachzahlungen + Vorauszahlungen auf 12 Monate — kann 30-40% eines Monatsumsatzes sein. **Rechne 30% jedes Umsatzes weg** als mentale Rücklage.

---

## 7) Entscheidungsmatrix — GO / NO-GO / WAIT

Setze jedes Kriterium heute bewerten, bevor Du entscheidest.

| # | Kriterium | GO (Vollzeit jetzt) | WAIT (Hybrid weiter) | NO-GO (bleib angestellt) |
|---|-----------|---------------------|---------------------|--------------------------|
| A | **Liquide Rücklage** | >= 42.000 EUR | 15.000-42.000 EUR | < 15.000 EUR |
| B | **Monatlicher MRR / wiederkehrender Retainer-Umsatz** | >= 2.500 EUR, 3 Monate in Folge | 500-2.500 EUR | < 500 EUR |
| C | **Zahlende Kunden (nicht LOI, signed)** | >= 3 aktiv | 1-2 aktiv | 0 |
| D | **Pipeline / Demos nächste 30 Tage** | >= 5 qualifizierte Demos | 2-4 | < 2 |
| E | **Outreach-Reply-Rate letzte 100 Sends** | >= 5% | 2-5% | < 2% |
| F | **Demo-to-Close-Rate** | >= 20% | 10-20% | < 10% |
| G | **Gründungszuschuss-Option** | Bewilligt / sehr wahrscheinlich | Möglich, nicht geklärt | Nicht verfügbar |
| H | **KV-Entscheidung GKV/PKV** | Getroffen, kalkuliert | Noch unklar | Nicht bedacht |
| I | **Rückweg-Plan (falls Scheitern Monat 6)** | Dokumentiert, Netzwerk da | Vage | Kein Plan |
| J | **Familienstand / psychische Resilienz** | Stabil, Unterstützung da | Ok | Aktuelle Belastung |
| K | **Alternative Job-Einkommensoptionen** | Mehrere Angebote verfügbar | 1 Option | Keine |
| L | **Externes Commitment (Co-Founder, Mentor, Investor)** | Ja, aktiv | Informell | Nein |

### Entscheidungsregel

- **GO:** Min. 10 von 12 Kriterien im GO-Bereich, KEIN Kriterium im NO-GO
- **WAIT (Hybrid weiter):** Mehrheit WAIT oder Mix
- **NO-GO:** Auch nur 2 Kriterien im NO-GO → bleib angestellt und arbeite Side-Hustle weiter

### Ehrliche Selbsteinschätzung für GetKiAgent Stand heute

Basierend auf Projektkontext (Wave 1 gesendet, Wave 2 gedraftet, pre-revenue):

| Kriterium | Aktueller Stand (Annahme) | Bereich |
|-----------|---------------------------|---------|
| A Rücklage | Unbekannt — Du musst ehrlich zählen | ? |
| B MRR | 0 EUR | NO-GO |
| C Kunden | 0 zahlend | NO-GO |
| D Pipeline | Wave 1+2 = 13 Leads, Response-Rate offen | WAIT |
| E Reply-Rate | Nach Wave 1 messbar, noch keine harten Zahlen | WAIT |
| F Close-Rate | N/A — noch keine Demos | WAIT |

**Aktuelles Matrix-Ergebnis:** **Mindestens 2 NO-GO-Kriterien (B, C).** Klare Empfehlung: **NO-GO zum Vollzeit-Sprung jetzt.** Hybrid-Pfad.

---

## 8) Recommendation (3 Sätze max)

**Bleib angestellt (oder geh auf 30h-Teilzeit) und baue GetKiAgent 12-18 Monate als Side-Hustle bis 3.000 EUR MRR mit 3 Monaten Wachstum in Folge erreicht sind UND 42.000 EUR Cash liegen.** Dein aktuelles Profil — BWL, kein Code, kein Netzwerk, pre-revenue, Solo, Düsseldorf-Fixkosten — hat statistisch ~70% Scheiter-Rate bei Vollzeit-Sprung ohne validierte Revenue, und der wahrscheinlichste Worst Case ist 16.000-20.000 EUR verbrannt plus 6 Monate psychische Erholung (siehe José León: 12 Monate, 38.676 USD Verlust, 60 USD Umsatz). Falls Deine aktuelle Stelle sowieso wackelt oder Kündigung droht: ALG-1-Pfad mit Gründungszuschuss (10-15k EUR in 15 Monaten) nutzen, nicht selbst kündigen.

---

## Sources and References

1. [SoftwareSeni — Solo Founder SaaS Metrics: From $0 to $10K MRR in 6 Months](https://www.softwareseni.com/solo-founder-saas-metrics-from-0-to-10k-mrr-in-6-months-with-realistic-timelines/) — Benchmarks MRR-Timelines und Quit-Framework
2. [Puzzle.io — How to Calculate Your Runway 2025](https://puzzle.io/blog/how-to-calculate-your-runway-a-guide-for-founders) — 12-18 Monate Runway + $3-5K MRR Framework
3. [Finvisor — How Much Runway Should a Startup Have](https://finvisor.com/startup-runway/) — Pre-Seed/Seed Runway-Benchmarks
4. [Indie Hackers — "I have 5 months of runway left"](https://www.indiehackers.com/post/lifestyle/i-have-5-months-of-runway-left-successful-founders-weigh-in-on-how-to-bootstrap-startups-without-burning-through-savings-ym1dMBrroAzlh0KRA5Uu) — Founder-Perspektiven zu Burn-Rate
5. [Hypertxt — Why Solo Founders Fail](https://hypertxt.ai/blog/marketing/why-solo-founders-fail) — 70% Solo-Scheiter-Rate, 5 Kernprobleme
6. [Upsilon — Startup Success and Failure Rate 2025](https://www.upsilonit.com/blog/startup-success-and-failure-rate) — "Most founders quit too late"
7. [Indie Hackers — Why Indie Founders Fail (Uncomfortable Truths)](https://www.indiehackers.com/post/why-indie-founders-fail-the-uncomfortable-truths-beyond-build-in-public-b51fd6509b) — "Messy Middle" 6-12 Monate
8. [Indie Hackers — "After losing $38676+ I can't do it anymore. I quit." (José León)](https://www.indiehackers.com/post/after-losing-38676-as-an-indie-hacker-i-cant-do-it-anymore-i-quit-8673223598) — Konkrete Failure-Retro, 12 Monate Vollzeit
9. [Indie Hackers — Bad news for solo indie hackers: building alone is killing your startup](https://www.indiehackers.com/post/bad-news-for-solo-indie-hackers-building-alone-is-killing-your-startup-2901fb8332) — 80% erfolgreicher Startups mit Co-Founder
10. [Lukas Hermann — Bootstrapping a SaaS Business in Germany (Stagetimer)](https://lukashermann.dev/writing/bootstrapping-a-saas-business-in-germany/) — DACH-Solo-Retro, 1.5 Jahre Side-Hustle bis 3k MRR
11. [Indie Hackers Germany Group](https://www.indiehackers.com/group/germany) — Community-Stimmungsbild DACH
12. [Gründer & Zünder Podcast (Florian Kandler)](https://derstartuppodcast.com) — DACH-Founder-Interviews inkl. Failure Stories (Janik Nolden)
13. [Business Insider — n8n Unicorn Bewertung](https://www.businessinsider.de/gruenderszene/technologie/insider-bestaetigen-berliner-ai-agent-startup-n8n-mit-24-milliarden-bewertet/) — Referenz-Framing DACH-Tech
14. [Xmethod n8n Agentur Berlin](https://www.xmethod.de/) — Konkurrenz-Benchmark DACH n8n-Agenturen
15. [RemodifyAI — n8n Experten Berlin](https://www.remodifyai.com/n8n-experten) — Konkurrenz-Benchmark
16. [Digital Agency Network — AI Agency Pricing Guide 2026](https://digitalagencynetwork.com/ai-agency-pricing/) — Retainer-Benchmarks $2k-$8k/Monat
17. [Optimize with Sanwal — AI Automation Agency Pricing 2026 CFO Guide](https://optimizewithsanwal.com/ai-automation-agency-pricing-2026-a-cfos-guide/) — CFO-Perspektive auf AI-Retainer
18. [AIFire — AI Automation Agency: Why It's a Trap & 3 Better Business Models](https://www.aifire.co/p/ai-automation-agency-why-it-s-a-trap-3-better-business-models) — Kritik am AAA-Business-Modell
19. [LinkedIn — What I learned building an AI Automation Agency (and why the Business Model is Broken)](https://www.linkedin.com/pulse/what-i-learned-building-ai-automation-agency-why-nadia-privalikhina-atk0f) — Failure-Retro AAA
20. [Düsseldorf Lebenshaltungskosten — Kleinanzeigen Ratgeber](https://themen.kleinanzeigen.de/magazin/ratgeber/lebenshaltungskosten-duesseldorf/) — 15,58 EUR/qm Miete
21. [WiWi-TReFF — 2500 EUR netto als Single in Düsseldorf](https://www.wiwi-treff.de/Gehaelter/Lebenshaltungskosten/Reichen-2500-netto-dauerhaft-fuer-Single-zum-leben/Diskussion-14802/29) — Community-Realitätscheck
22. [Beatvest — Lebenshaltungskosten Deutschland](https://www.beatvest.com/blog/lebenshaltungskosten-in-deutschland) — 1.833 EUR Durchschnitt Single
23. [Statistisches Bundesamt Konsumausgaben](https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Einkommen-Konsum-Lebensbedingungen/Konsumausgaben-Lebenshaltungskosten/_inhalt.html) — Offizielle DE-Konsumdaten
24. [Marcus Knispel — Mindestbemessungsgrundlage Selbstständige GKV](https://marcusknispel.com/mindestbemessungsgrundlage-selbststaendige/) — 1.248,33 EUR/Monat Basis 2025
25. [Finanztip — Freiwillig GKV versichert: Beiträge & Kosten](https://www.finanztip.de/gkv/freiwillig-versichert/) — GKV-Beitragsrechnung
26. [Agentur für Arbeit — Gründungszuschuss beantragen](https://www.arbeitsagentur.de/arbeitslos-arbeit-finden/arbeitslosengeld/gruendungszuschuss-beantragen) — Offizielle Voraussetzungen
27. [Gruenderkueche — Gründungszuschuss 2026: Anspruch, Höhe, Voraussetzungen](https://www.gruenderkueche.de/fachartikel/gruendungszuschuss-anspruch-antrag-hoehe-voraussetzungen/) — Detaillierte Antragshinweise
28. [Deutschland-startet — Höhe und Dauer Gründungszuschuss](https://www.deutschland-startet.de/hoehe-dauer-gruendungszuschuss/) — 10-15k EUR typischer Gesamtbetrag
29. [Buergergeld.org — Höhe Single 2026](https://www.buergergeld.org/news/wie-viel-buergergeld-bekommt-man-als-single/) — 563 EUR Regelsatz + KdU
30. [Arbeitslosenselbsthilfe — Düsseldorf angemessene Bürgergeld-Miete](https://www.arbeitslosenselbsthilfe.org/duesseldorf-miete/) — 431 EUR KdU Düsseldorf
31. [Top-Jobs-Europe — Aus Selbstständigkeit zurück ins Angestelltenverhältnis](https://top-jobs-europe.de/aus-der-selbststaendigkeit-zurueck-ins-angestelltenverhaeltnis-wenn-man-nicht-mehr-sein-eigener-chef-sein-moechte/) — Rückkehr-Strategie Arbeitsmarkt
32. [Medium Luca Restagno — Micro SaaS Founder on side of 9-5](https://medium.com/@lucarestagno/learn-how-to-be-a-micro-saas-founder-on-the-side-of-a-9-5-job-cca9d9c59542) — Hybrid-Pfad-Playbook
33. [Shipped.club — Micro SaaS founder on side of 9-5 job](https://shipped.club/blog/micro-saas-founder-9-5-job) — 6 SaaS während Senior-Engineer-Job
34. [Sidepreneur — Top Deutsche Business Podcasts](https://www.sidepreneur.de/podcasts-fuer-unternehmer-und-gruender/) — DACH-Community-Quellenübersicht
35. [Gruenderplattform — Selbstständig als Student (20h-Regel)](https://gruenderplattform.de/geschaeftsideen/selbstaendig-als-studentin) — 20h/Woche Nebenberuflichkeits-Regel

---

## Additional Notes

- **Steuerberater-Konsultation dringend empfohlen** vor Kündigung. Der Unterschied zwischen Einzelunternehmer, GmbH und UG kann über die ersten 3 Jahre mehrere Tausend Euro ausmachen.
- **Aufhebungsvertrag ohne Sperrzeit** nur mit arbeitsrechtlicher Beratung — Bundesagentur prüft streng.
- **PKV vs. GKV Entscheidung:** Bei geringem/schwankendem Einkommen ist GKV fast immer besser, weil Beitrag mit Einkommen sinkt. PKV wirkt erst über ~60k EUR Jahreseinkommen attraktiv — und Rückkehr in GKV ist nach 55 quasi unmöglich.
- **Builder-Validator-Pattern** (siehe `.claude/rules/builder-validator.md`): Dieses Dokument ist Builder-Output. Vor finaler Entscheidung von einem Menschen mit Gründungserfahrung (nicht von einem Coach, der Kurse verkauft) gegenlesen lassen.
- **Was nicht recherchiert wurde, weil Quellenlage dünn war:** Konkrete Retros von BWL-No-Code-DACH-Agentur-Gründern mit publizierten Zahlen. Diese Nische ist dokumentarisch unterrepräsentiert — der engste Vergleich bleibt Lukas Hermann (aber SaaS, nicht Service-Agency).
- **Nicht berücksichtigt und separat zu prüfen:** Steuerliche Auswirkungen der ersten Einnahmen neben Anstellung, Künstlersozialkasse (irrelevant hier), IHK-Pflichtmitgliedschaft (~50 EUR/Jahr), Gewerbeanmeldung (einmalig 20-40 EUR), etwaige Berufshaftpflichtversicherung (~300-600 EUR/Jahr).
