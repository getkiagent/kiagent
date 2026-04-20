# Plan: Outreach V2 — Specific-Question-Framework

Erstellt: 2026-04-20. Basis-Prompt: `prompts/outreach_mail_v1.md`. Rollout-Entscheidung: sequenziell (erst Text, dann Video). **Framework-Entscheidung (2026-04-20): Specific Question, ~50 Wörter, keine Mini-Audit-Expansion.**

## Grund-Prinzip der V2-Mail

Eine einzige, wortnah aus der FAQ gezogene Kundenfrage wird im Betreff und im Opener zitiert. Das ist der Beweis: "Ich habe eure Seite gelesen." Kein Audit-Block, keine Agent-Antwort-Vorschau, kein Vorschlag-Absatz — das ist alles Fleisch, das man verkürzen kann. Nur: Frage → Warum-das-Volumen-ergibt → CTA. Maximal 70 Wörter Body.

## Context

**Problem:** Wave 1+2 (13 gesendete Mails) produziert nur Absagen oder keine Antworten. Der Opener nutzt Pain-Daten schon, aber das Loom-Video im PS ist für ALLE dieselbe URL — generisch, wirkt wie Massenware. Die Mail verspricht Spezifität im Text und bricht sie im Anhang.

**Data-Realität (Stand jetzt):** 78 qualifizierte Tier-A Leads haben alle ≥ 3 `support_pain_signals` + `likely_automation_opportunity` + `recommended_next_action` — die Personalisierungs-Rohdaten sind bereits da, nur nicht maximal genutzt. Die nächste Stufe: FAQ-Seiten scrapen und echte Kundenfragen ziehen, die der Lead selbst kennt.

**Ziel:** Reply-Rate von geschätzt 10-15 % (mit überwiegend Absagen) auf 20-25 % (mit Mehrheit Question/Positive) heben. Messbar jetzt via Reply-Classifier.

**Kern-Strategie:** Drei Personalisierungs-Layer, sequenziell validiert:
- **Layer A (Text):** Mini-Audit mit 3 echten Kunden-Fragen aus der FAQ-Seite des Leads → ~$0.09/Mail
- **Layer B (Video):** AI-Avatar-Video mit Lead-Name und einer konkreten Frage aus Layer A → ~$1/Mail
- **Layer C (Live-Demo-Page):** Per-Lead deployete Demo-URL mit funktionierendem Agent → später

Layer C nur bauen, wenn A+B A/B-bestätigt sind. User-Entscheidung: sequenziell.

---

## Phase 1 — Layer A (Mini-Audit im Text) — diese Woche

### 1.1 FAQ-Scrape-Script `scripts/enrich_lead_faqs.py` (NEU)

- Input: `leads/qualified-leads.json` (oder Liste via `--only slug1,slug2`)
- Pro Lead:
  - Firecrawl (existing integration, gleiche creds wie `Lead URL Scorer`): `/faq`, `/hilfe`, `/kontakt`, `/widerruf`, `/retouren` — max 5 Pages, dedupe identische Längen (soft-404-Filter wie in `Build Claude Prompt` Node)
  - Claude Haiku (1 Call pro Lead, `claude-haiku-4-5`): extrahiert strict-JSON mit genau drei Feldern
    - `pointed_question` (string): EINE konkrete Frage, wortnah aus der FAQ (mit Anführungszeichen erhalten), die das Lead-Team vermutlich täglich beantwortet
    - `question_source_page` (string): welche Page (z.B. "/faq", "/hilfe") die Frage geliefert hat
    - `volume_hint` (string, ≤ 10 Wörter): warum das Volumen ergibt — z.B. "sieben Länder + Abo", "Multi-Produkt-Katalog mit Inhaltsstoff-Fragen"
- Output: `leads/faqs/<slug>.json` (slug-Funktion konsistent mit `generate_outreach.py`)
- Skip-Logik: File existiert und `--force` nicht gesetzt → skip
- Bei 0 scrapebare FAQ-Pages: Fallback = `pointed_question` aus `support_pain_signals` formulieren (Haiku), Source = "general"
- Cost: ~$0.04/Lead × 78 = $3 initial (Haiku statt Sonnet, weil die Extraktion trivial ist)

### 1.2 Neuer Prompt `prompts/outreach_mail_v2.md` (NEU)

Komplett neu geschrieben (nicht Kopie von v1 — v1 ist zu lang strukturiert). Struktur:

**Betreff:** exakt die `pointed_question` in Anführungszeichen + Firmenname
- Beispiel: `"Bio- oder Beauty-Kollagen?" bei JARMINO`
- KEINE Verallgemeinerung des Betreffs — die Frage muss wortnah stehen

**Opener (1 Satz):** die Frage nochmal + Quell-Page + "vermutlich täglich"
- Beispiel: `die Frage "Bio- oder Beauty-Kollagen?" steht auf eurer FAQ-Seite — vermutlich kommt sie täglich rein.`

**Hebel-Satz (1 Satz):** `volume_hint` + was ein Agent daran ändern würde
- Beispiel: `Bei sieben Ländern und Abo-Modell ergibt das viel manuelle Arbeit für Antworten, die ein Agent in eurem Ton sofort geben könnte.`

**CTA (1 kurze Frage):** maximal 5 Wörter
- Beispiele: `Kurze Demo?` / `Interesse an 5-Min-Demo?` / `Soll ich es zeigen?`
- KEINE "Habt ihr 15 Minuten"-Formulierungen — zu generisch

**PS-Zeile:** bleibt Loom-Link wortidentisch wie v1
**Opt-out:** bleibt wortidentisch wie v1
**Signatur:** bleibt `Ilias Tebque\nGetKiAgent — KI-Support für E-Commerce`

**Harte Limits:**
- Body (ohne Betreff, PS, Opt-out, Signatur): ≤ 60 Wörter
- Gesamte Mail ≤ 90 Wörter
- Genau 1 Fragezeichen im Body (am CTA) + 1 Fragezeichen im Opener = 2 Fragezeichen max
- `pointed_question` muss wortidentisch im Body vorkommen (in Anführungszeichen)

**Verbote (strikter als v1):**
- Keine "Ich hab gesehen"-Floskeln — gleich die Frage zitieren
- Kein Vorschlags-Absatz ("Ein Agent der...") — das gehört ins Hebel-Satz, nicht eigener Abschnitt
- Kein Demo-Teaser-Satz im Body — PS-Link reicht
- Kein Nachname in Signatur
- Kein "ehrlich gesagt", "übrigens", "Hinweis"

### 1.3 Modifikation `scripts/generate_outreach.py`

- Neuer Flag `--v2` → lädt Prompt aus `prompts/outreach_mail_v2.md`, hängt `pointed_question` + `question_source_page` + `volume_hint` aus `leads/faqs/<slug>.json` an den User-Message-Teil
- Wenn FAQ-File fehlt: skip mit Log `SKIP: kein FAQ-File, erst enrich_lead_faqs.py laufen lassen`
- Neue Quality-Gates für V2 (zusätzlich zu den bestehenden):
  - Body-Wordcount ≤ 60 (sonst FAIL)
  - `pointed_question` (string-literal) im Body vorhanden
  - Fragezeichen-Count im Body ≤ 2
- `_ensure_signature` + `_ensure_impressum` bleiben unverändert
- Dedup-Ordner separat: `outreach/v2/<slug>.txt` (damit V1 und V2 koexistieren für A/B)

### 1.4 Firmenname-Gate-Fix (parallel, ~15 Min)

In `validate_quality_gates`:
```
if company_name and company_name.lower() not in subject.lower():
    failures.append(...)
```
ersetzen durch Token-Match mit Normalisierung:
- Beide Seiten: lowercase + strip non-alphanumeric + split → tokens
- Stopwords entfernen (`gmbh, ag, co, ltd, skincare, beauty, cosmetics, the`)
- Falls mindestens 1 content-token des Firmennamens im Subject → PASS

Test-Cases die jetzt durchlaufen müssen:
- `"4 ELEPHANTS SKINCARE"` + Subject `"Pre-Purchase-Beratung bei 4 Elephants"` → PASS
- `"dr. oh® - The Clean Beauty Expert"` + Subject `"Support-Automatisierung bei dr oh"` → PASS
- `"CellBeauté (Swiss Nutri Cosmetics SA)"` + Subject `"Ingredient-Fragen bei CellBeaute"` → PASS

### 1.5 A/B-Test-Setup

- **Split:** `qualified-leads.json` nach deterministic hash auf `url` in 2 Pools:
  - Pool V1 (Control, 40 %): weiter mit existing `outreach_mail_v1.md`
  - Pool V2 (Treatment, 60 %): neuer `outreach_mail_v2.md` mit Mini-Audit
- **Logging:** in `outreach/<version>/<slug>.txt` wird via extended filename oder Meta-JSON die Version getagged
- **Auswertung:** Reply-Watcher schreibt `reply_intent` ins Sheet. Separates Spalte `outreach_version` (V1/V2) muss angelegt werden — ein zweiter Bootstrap-Workflow wie Task 8 heute.
- **Sample-Size:** min. 20 Replies pro Variante (= ~120 sent Mails bei 15 % Reply-Rate) — 3-4 Wochen bei 30/Tag
- **Decision-Rule:** V2 wins wenn 2 Kriterien erfüllt: (a) Reply-Rate V2 ≥ 1.3× Reply-Rate V1, (b) `positive+question` Anteil in V2 Replies ≥ 50 %

### 1.6 Outreach-Stats-Script `scripts/outreach_stats.py` (NEU, klein)

- Liest Sheet via gspread, filtert letzte 30 Tage
- Gruppiert nach `outreach_version` × `reply_intent`
- Schreibt Tabelle in `tasks/outreach-stats-weekly.md`
- Wird in Windows Task Scheduler eingehängt (Mo 08:00), Ergebnis als Telegram-Alert

---

## Phase 2 — Layer B (Cinematic Hook-Video via Higgsfield) — ab Woche 3, wenn V2 gewinnt

**Kategorie-Wechsel gegenüber initialem Gedanken:** Higgsfield ≠ HeyGen. Higgsfield ist Cinematic/Stylized Video (Kling 3.0, Sora 2, Veo 3.1 als Backends, Text/Image-to-Video), kein Talking-Head-Avatar. Use-Case wird entsprechend angepasst: **5-10 Sek visueller Pattern-Interrupt**, nicht 60-Sek gesprochene Nachricht. Der Loom-Link für die Deep-Demo bleibt erhalten.

### 2.1 Tool-Setup (Higgsfield)

- **Plan:** Plus $39/mo (1000 Credits, ~150 Kling-3.0-Videos/Monat) — reicht für 30/Tag
- **API:** `cloud.higgsfield.ai` direkt, oder Segmind-Wrapper ($0.16-$0.70 per Image-to-Video bei Pay-as-you-go)
- **Model-Wahl initial:** Kling 3.0 Image-to-Video (~6 Credits/Video, schneller, günstiger). Sora 2 / Veo 3.1 nur für Hero-Videos (40-70 Credits, teuer).
- **Render-Zeit:** 30-90 Sek pro 5-Sek-Clip

### 2.2 Einmal-Setup

- **Brand-Template:** Intro-Frame mit GetKiAgent-Logo + Ilias-Foto → als Image-to-Video-Seed für alle Outputs
- **Prompt-Template:** `prompts/video_prompt_v1.md` — definiert 5-10 Sek Cinematic Hook Struktur: Company-Name Text-Overlay, Pain-Visualization, Logo-Reveal
- **KEIN Voice-Clone nötig** (kein gesprochenes Audio in diesen Clips) → entfernt Onboarding-Barriere

### 2.3 `scripts/render_lead_video.py` (NEU)

- Input: `leads/<slug>.json` + `leads/faqs/<slug>.json` + Screenshot der Lead-Website (Playwright, 1280×720 Hero-Shot)
- Flow:
  1. Playwright scrapes Hero-Screenshot der Lead-URL
  2. Claude Sonnet baut Image-to-Video-Prompt: *"Cinematic zoom-in on beauty-shop website, overlay text 'JARMINO', smooth transition to chat-bubble showing 'Wie dosiere ich das Kollagen?' answered instantly. 5 seconds, golden-hour lighting."*
  3. POST to Higgsfield API mit Hero-Image + Prompt
  4. Poll bis `completed` oder Timeout (3 Min)
  5. Download mp4 → upload to own CDN (Cloudflare R2, $0.015/GB) oder nutze Loom-Upload-API für Gmail-Kompatibilität
- Output: `outreach/videos/<slug>.json` mit `{video_url, thumbnail_url, model_used, credits_consumed}`
- Fallback: Render-Fehler → `has_video: false` → V2-Mail fällt auf Loom-URL zurück (Layer-A-only)

### 2.4 Mail-Integration

Die Mail-Struktur ändert sich **nicht** grundlegend:
- Opener + Mini-Audit (Layer A) bleibt
- PS-Zeile Phase 2: **ZWEI Video-Links**
  - `▶ 5-Sek-Hook (Higgsfield): {{hook_video_url}}` (visuelles Attention-Magnet, Preview vom Thumbnail im Inline-Bild)
  - `▶ 2-Min-Demo (Loom, wie zuvor): https://loom.com/...`
- Wenn `hook_video_url` fehlt: PS-Zeile fällt auf nur-Loom zurück

Alternative kompakter: Ein Embedded-GIF (die ersten 3 Sek des Cinematic-Clips) direkt im Mail-Body als Hero-Image. Aber: GIF-Quality begrenzt + Gmail-Rendering-Heuristiken (manche Empfänger sehen GIF als static image).

### 2.5 Cost-Control

- Higgsfield Plus: $39/mo + Overage. Bei 30/Tag × 20 Werktage × 6 credits (Kling 3.0) = 3600 credits/Monat → Plus (1000) reicht nicht → Ultra $99 (3000) oder Plus + Overage
- **Realistische Monats-Rechnung:** Ultra-Plan $99 + ~600 Overage-Credits ≈ $150-200/Monat. Deutlich günstiger als HeyGen-Route.
- Hardcap im Script: prüft täglich `videos/`-Volume, abortiert ab 35 neuen am Tag (Sicherheitspuffer)

---

## Phase 3 — Layer C (Live-Demo-Page) — nur bei V2+Video-Win

Aufriss, kein Commitment:
- Next.js-Template + Tailwind, branded via Firecrawl-Scrape (Logo, Colors)
- Deploy per Lead: Vercel-URL `getkiagent.app/demo/<slug>` (oder Cloudflare Pages, günstiger)
- Eingebautes Chat-Widget: Haiku-Agent mit FAQ als System-Prompt
- Kosten: ~$0.30/Lead Hosting + Initial Dev ~8h
- Legal: Demo-Hinweis prominent, Auto-Takedown nach 30 Tagen ohne Interaktion

---

## Subagents vs. Workflows: Entscheidung

**Python-Haiku-Chains** (Muster wie `batch_analyze.py`), keine Claude-Subagents pro Lead. Begründung:
- Deterministisch, debugbar, günstiger pro Run
- Pattern ist im Projekt schon etabliert
- Subagents wären Overkill für 1-2 sequenzielle LLM-Calls
- n8n bleibt zuständig für: Cron-Trigger (Daily-Discovery+Enrich), Sheet-Sync, Gmail-Draft, Reply-Classifier

Wenn später die Recherche pro Lead offener wird (LinkedIn-Profile lesen, News scannen, Social-Signals aggregieren): dann Claude Code Agent SDK evaluieren.

---

## Kritische Dateien

| Datei | Phase | Rolle |
|---|---|---|
| `scripts/enrich_lead_faqs.py` | 1.1 | NEU — FAQ-Scrape + Question-Extraktion |
| `leads/faqs/<slug>.json` | 1.1 | NEU — per-Lead FAQ-Output |
| `prompts/outreach_mail_v2.md` | 1.2 | NEU — Prompt mit Mini-Audit |
| `scripts/generate_outreach.py` | 1.3, 1.4 | MOD — `--v2` Flag, FAQ-Integration, Firmenname-Gate-Fix |
| `scripts/outreach_stats.py` | 1.6 | NEU — A/B-Ergebnis-Auswertung |
| `scripts/render_lead_video.py` | 2.3 | NEU — Phase 2 (Higgsfield Image-to-Video + Playwright-Screenshot) |
| `prompts/video_prompt_v1.md` | 2.2 | NEU — Phase 2 Cinematic-Prompt-Template |
| Sheet-Spalte `outreach_version` | 1.5 | Bootstrap-Workflow analog zu heute |

---

## Verification

| Check | Wie |
|---|---|
| 1.1 | `python scripts/enrich_lead_faqs.py --only jarmino --limit 1` → File in `leads/faqs/jarmino.json` mit 5 Questions, manual-Review plausibel |
| 1.3 | `python scripts/generate_outreach.py leads/qualified-leads.json --v2 --only jarmino` → Draft in `outreach/v2/jarmino__*.txt` enthält ≥ 2 Fragezeichen und die Questions-Strings aus `leads/faqs/jarmino.json` |
| 1.4 | Regression-Lauf auf vorher gefailte Leads (`4 ELEPHANTS`, `dr. oh®`, `O'right`) → alle 3 Drafts werden generiert, nicht mehr skipped |
| 1.5 | Nach ersten 10 V1+10 V2 sent: Sheet-Check ob Spalte `outreach_version` korrekt getagged |
| 1.6 | `python scripts/outreach_stats.py --window 30d` → Tabelle mit Reply-Rate per Version |
| 2.3 | First-Video: 5-Sek Clip lädt, Firmenname-Text-Overlay lesbar, Cinematic-Quality nicht kitschig, Thumbnail extrahierbar |

---

## Open Items / Blocker

1. **Video-Tool:** ~~HeyGen vs andere~~ → **Higgsfield** (via User bestätigt). Model-Default: Kling 3.0 Image-to-Video. Phase 2 entsprechend angepasst (Cinematic Hook, kein Talking-Head).
2. **Higgsfield-Plan:** Start Plus $39/mo zum Testen, bei Volume-Bedarf Ultra $99. Entscheidung erst mit ersten 10 Test-Videos.
3. **Firecrawl-Quota:** 78 Leads × 5 Pages initial = 390 Scrapes; danach ~150/Monat. Im Current-Plan OK.
4. **`outreach_version`-Spalte** im Lead-Pipeline-Sheet anlegen — ein-Shot Bootstrap-Workflow wie bei den Reply-Intent-Spalten heute.

---

## Reihenfolge / Ship-Order

- **Tag 1 (morgen):** 1.1 (enrich_lead_faqs.py) + 1.4 (Firmenname-Gate-Fix) + 1.2 (v2-Prompt). Test an 3 Leads manual-Review.
- **Tag 2:** 1.3 (`--v2` Flag in generate_outreach.py). Lauf auf 5 Leads, manual-Review. Wenn OK: Split-Setup 1.5.
- **Tag 3-5:** Parallel zu laufendem V1: V2 für 60 % neuer Drafts. Send-Workflow läuft unverändert.
- **Woche 1-3:** A/B-Daten sammeln. 1.6 Stats-Script wöchentlich.
- **Ende Woche 3:** Decision-Review — wenn V2 wins: Phase 2 kickoff (Tool-Klärung + Voice-Sample).
- **Woche 4-5:** Phase 2 Setup + Deploy. Erste 10 Videos manual-gated.
- **Woche 6+:** Phase 2 automated rollout. A/B V2-text-only vs V2+Video starten.
- **Monat 3:** Phase 3 (Demo-Pages) nur wenn Phase 2 liefert.

---

## Nicht im Scope

- Re-engagement der 13 Wave-1/2-Empfänger mit V2 (eigener Follow-up-Plan, braucht „Nein heißt nein"-Respekt)
- LinkedIn-Outreach parallel (eigener Dual-Channel-Plan)
- CRM-Integration (HubSpot / Pipedrive) — Sheet bleibt Source-of-Truth bis 50+ Deals
- Video-Hosting-Infra falls Tool-Provider kein Hosting liefert (Fallback: Cloudflare R2 oder Loom-Upload-API)
