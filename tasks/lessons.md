# Tasks & Lessons

## Lessons Learned

### 2026-04-11 — Website-Referenz-Analyse
**Kontext:** Firecrawl-Scrape von deinekiagentur.com als Wettbewerbs-Referenz.

**Findings:**
- Hero-Headline: "Ihr Partner für KI Beratung – Wir machen Unternehmen KI-fit" — nutzen-orientiert, aber generisch. GetKiAgent differenziert durch Branchenspezifik (E-Commerce) + persönliche Expertise.
- Section-Reihenfolge: Hero → Social Proof (Zahlen-Counter) → Team → Leistungen → CTA.
- Social-Proof: Animierte Zähler direkt unter Hero — prominenter als Text. Wir nutzen Stats im About-Block.
- CTA-Copy: "Termin Buchen" zweimal im Nav — kein Benefit. GetKiAgent nutzt "Kostenloses KI-Audit" — stärker.
- Kein Preisschema sichtbar — Differenzierungsmöglichkeit für GetKiAgent mit transparenten Paketen.
- Entscheidung: Spec-Headline beibehalten, kein Anpassen nötig — bereits differenzierter als Wettbewerb.

### 2026-04-10 | Outreach-Prompt Audit & Fix (outreach_mail_v1.md)
**Kontext:** Audit der gesendeten Wave-1/Wave-2-Mails gegen den System-Prompt.

**Findings:**
- "Kein Skript-Bot, sondern ein Agent der..." erschien in 100% der Mails — war nicht in den Verboten gelistet. Template-Phrase die sofort erkennbar ist.
- "24/7, auf Deutsch" als wortidentische Kombination in ~80% der Mails — ebenfalls kein Verbot.
- Doppelte Beispiel-Fragen in Anführungszeichen ("X?" oder "Y?") in 90% der Mails — mechanisches Muster das echte Personalisierung signalisiert aber keine liefert.
- Demo-Link + Meeting-Frage in derselben Mail = 2 CTAs. Direkter Widerspruch zur "eine Handlung"-Regel, aber Prompt schwieg dazu.
- PFLICHT-GATE-Überlegungen erschienen in gesendeten Dateien (nature-heart.txt, the-glow.txt) — Output-Regel "NUR die fertige Mail" war nicht stark genug formuliert.
- "Ilias Tebque" statt "Ilias" in junglück.txt — Prompt hatte keine Nachname-Regel.

**Fixes in outreach_mail_v1.md:**
- 5 neue Verbote: "Kein Skript-Bot", "24/7, auf Deutsch", Doppel-Beispiel-Fragen, Demo-Link + Meeting-CTA gleichzeitig, Nachname in Signatur.
- CTA-Sektion verschärft: "Habt ihr diese Woche 15 Minuten für einen kurzen Walkthrough?" explizit verboten. Varianzpflicht ergänzt.
- Output-Regel: "Die Ausgabe beginnt mit 'Betreff:' und endet mit der Signatur. Nichts davor, nichts danach."
- Qualitätsprüfung: "NICHT ausgeben" ergänzt, "Kein Skript-Bot"-Check explizit als Punkt 6.

**Going forward:**
- Nach jeder neuen Mail-Welle: 3 Mails gegen den Prompt checken, ob neue Template-Muster entstanden sind.
- Verbotsliste ist lebendig — wenn eine Phrase dreimal auftaucht, kommt sie rein.

### 2026-04-09 | Projekt-Audit & Strukturbereinigung
**Kontext:** Erster vollständiger Audit des getkiagent-Projektordners.

**Findings:**
- `docs/lead-engine-brief.mdclaude` war ein Artefakt eines Claude-Fehlers (falsche Extension). Erkennbar an der Extension — künftig sofort löschen.
- `glowlab-knowledge.txt` war 100% Duplikat von `.md`. Bei Voiceflow-Wissensbasen immer nur eine Dateiversion behalten.
- `summarize_reel.py` war im `/scripts`-Ordner aber kein Lead-Engine-Script → umgelagert nach `/tools`. Faustregel: `/scripts` nur für Lead-Engine-Pipeline.
- `/workflows`-Ordner war leer seit Erstellung (03. April). n8n-Workflows leben in n8n, nicht im Repo — Ordner war Platzhalter ohne Plan.
- `tasks/lessons.md` existierte als Template aber ohne einen einzigen Eintrag — Prozess war nicht etabliert.

**Going forward:**
- Nach jedem abgeschlossenen Task einen Eintrag hier anlegen.
- Neue Dateien sofort in die richtige Kategorie (`/scripts`, `/tools`, `/archive`) einordnen, nicht im Root ablegen.

### 2026-04-11 — Pipeline Stage 4 blocked: Anthropic credit balance
**Error:** generate_outreach.py — alle 12 qualifizierten Leads übersprungen mit `Error code: 400 ... credit balance is too low to access the Anthropic API`.
**Root cause:** ANTHROPIC_API_KEY hat kein Guthaben mehr. Haiku Meta-Prompt-Call schlägt sofort fehl, kein Fallback.
**Fix:** Credits aufladen unter https://console.anthropic.com/settings/billing, dann `python scripts/generate_outreach.py leads/qualified-leads.json --min-score 7 --max-score 10` neu starten. Stage 5 (`send_existing_drafts.py --keep-existing`) danach.

### 2026-04-11 — PLAN.md drift: send_existing_drafts.py --keep-existing nicht vorhanden
**Error:** `send_existing_drafts.py --keep-existing` fehlt als Flag im Script — PLAN.md Stage 5 greift ins Leere.
**Root cause:** Script iteriert hart über alle `outreach/*.txt` und hat nur `--dry-run`. Keine Filter- oder Skip-Mechanik.
**Fix:** Für diesen Run via Python-Inline Import (`from send_existing_drafts import create_draft, resolve_email, parse_txt`) nur die 12 neuen Slugs verarbeitet. PLAN.md Stage 5 aktualisieren oder dem Script `--only-slugs` / `--since-file` ergänzen.

### 2026-04-11 — 5 Tier-B Leads ohne Email in batch-results
**Error:** GRÜNES GOLD, Johannas Kräutergarten, Sonnengrün, Vegan Fitness & Foods, Ecco Verde haben Score ≥7 aber `resolve_email` findet nichts im email_index.
**Root cause:** batch_analyze.py extrahiert contact_email teilweise nicht, wenn Shop nur Kontaktformular nutzt oder Email in Bild/JS steckt.
**Fix:** In `leads/no-email-queue.txt` geloggt. Manuell nachrecherchieren oder batch_analyze.py Extraktion verbessern.
