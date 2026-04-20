# Pipeline-Revival Run — 2026-04-20

## Context

Pipeline hatte seit 15.–16.04. kein neues Output mehr produziert. Ursache: alle Stages (Discovery, Scoring, Draft-Gen) laufen nur auf manuellen Trigger; Ilias hat aufgehört zu triggern. Plan-File: `~/.claude/plans/shimmying-puzzling-crab.md`.

## Phase 0 — Sofort-Revival (ausgeführt)

### Apollo-Diagnose
- `leads/apollo-raw-beauty-2026-04-19.json` enthält 5 valide Leads (Spirit of Rügen, Yepoda, KLAPP, JUNGLÜCK, Théobroma). **Kein API-Fehler** — Output ist nur klein (5 Einträge = 1.8 KB).
- `.env` vorhanden, Apollo-Key nicht einzeln geprüft. Apollo wird heute nicht verarbeitet — die 5 Domains können in nächstem Discovery-Lauf aufgenommen werden.

### Discovery gelaufen ✓
- Befehl: `python scripts/discover_leads.py --niche ecommerce-beauty --queries 8 --results 20`
- Ergebnis: **94 neue Domains**, gespeichert in `leads/ecommerce-beauty/discovered-urls.txt`.
- Bereits bekannt: 886 Domains (Dedup funktioniert).
- 8 Queries aus 100 Config-Queries genutzt — restliche 92 Queries sind ungenutzt (Reserve für morgen).

### Outreach-Drafts gelaufen ✓ (finale Zahlen nach Script-Abschluss)
- Befehl: `python scripts/generate_outreach.py leads/qualified-leads.json --min-score 7`
- **Generiert: 24 Drafts** (von 78 Tier-A+B Leads)
- **15 Leads ohne Email** → `leads/no-email-queue.txt`
- **39 Fehler** (API-Fehler oder Quality-Gate-FAIL nach Retry) — **50% Fehlerquote, neues Open Issue**
- Beispiel-Fehler: "Signatur nicht wortidentisch am Ende" (Quality Gate im Script)
- Qualitätscheck an `jarmino__jarmino-de.txt`: personalisiert, Demo-Link, Opt-out — OK.

### Lead URL Scorer NICHT getriggert (verschoben)
- Scorer `jGDcEjOD8RIbXKpq` läuft Daily 8am, filtert Sheet nach `status===""`.
- Die 94 neuen Discovery-URLs sind **nur lokal**, nicht im Sheet. Sync-Bindeglied ist `batch_analyze.py` mit `_sync_to_sheet` (bisher nicht ausgeführt).
- **Entschieden:** heute nicht triggern — würde leer laufen. In Phase 2 (Scheduler-Setup) wird die Kette `discover_leads.py → batch_analyze.py → Sheet-Sync → Scorer` automatisiert.

## Ergebnis Phase 0

- Send-Workflow `TQMPiSl8a8hHtbq7` hat morgen (Di 9:00) wieder **Input**.
- Pool-Status: 78 Tier-A qualified Leads (Stand 15.04.). Davon ~13 bereits gesendet/gedrafted (Waves 1+2). Heute +21 Drafts = ~34 Leads in Draft-Pipeline. Rest: ~44 ungenutzt.
- Discovery hat **94 neue Domains** zusätzlich erzeugt (noch nicht gescored).

## Phase 1.1 — Sheet-Spalten (Ilias bitte manuell anlegen)

Google Sheet `1OReC3rBa6bMImrw96dbTryW5LlB0SYWnbpn_t7x0-u0`, Tab **Lead Pipeline**. **3 neue Spalten rechts** am Ende anhängen (Reihenfolge egal, Namen exakt):

| Spaltenname | Typ | Zweck |
|---|---|---|
| `reply_intent` | Text | Automatisch gesetzt auf eine der 4 Kategorien: `positive` / `question` / `negative` / `auto_responder` |
| `reply_snippet` | Text | Automatisch: erste 200 Zeichen der tatsächlichen Antwort (kein Snippet aus Gmail, echtes Body) |
| `reply_analyzed_at` | Text (ISO Timestamp) | Automatisch: wann der Classifier gelaufen ist |

Keine Validierung/Dropdown nötig — der n8n-Workflow schreibt exakt diese 4 Werte. **Sobald Ilias diese 3 Spalten angelegt hat**, kann Phase 1.2 (Workflow-Erweiterung) starten.

## Nächste Schritte

| Wann | Was | Wer |
|---|---|---|
| **Heute abend** | Sheet-Spalten anlegen (Phase 1.1) | Ilias (2 Min) |
| **Morgen** | n8n Reply Watcher erweitern (Phase 1.2: Gmail-Body-Fetch + Claude-Classify + Sheet-Update) | Claude |
| **Morgen** | Validator-Test mit 2 historischen Replies (Grüne Erde / vivatrue) | Claude |
| **Übermorgen** | Windows Task Scheduler Setup (Phase 2) — Daily Discovery 06:30, Draft-Gen 07:30 | Claude |
| **Übermorgen** | Follow-up-Slug-Mismatch fixen (50%-Fehlerquote vom 16.04.) | Claude |
| **Tag 4** | Staleness-Monitor (Phase 3) + Woche Beobachtung | Claude |

## Follow-up-Arbeit am selben Tag (nach Userfeedback)

### Quality-Gate-Fix ✓
- `scripts/generate_outreach.py:_ensure_signature()` NEU: strippt jede Signatur-Variante am Mail-Ende und appended canonical `Ilias Tebque\nGetKiAgent — KI-Support für E-Commerce`. Eingebaut zwischen `_strip_premature_signature` und `_ensure_impressum`.
- Unit-Tests: 5/5 PASS (no-sig, partial-Ilias, Ilias-Tebque, bereits-korrekt-kein-Duplikat, gate akzeptiert Output).
- Retry-Run fertig: **+30 neue Drafts** (von 24 auf 54 gesamt). Fehler von 39 auf 9 (77% Reduktion). Die verbleibenden 9 Fails sind alle am `Firmenname fehlt im Betreff`-Gate (strict substring-match bei Firmennamen mit Sonderzeichen wie "4 ELEPHANTS", "dr. oh®", "CellBeauté", "O'right").

### Reply Watcher v2 deployed ✓
- Workflow `qTptgWEJF5fvCkwj` erweitert auf 11 Nodes.
- Neue Kette nach `Filter New Replies`: `Find Inbox Reply` (Gmail getAll) → `Get Reply Body` (Gmail get full) → `Claude Haiku Classify` (HTTP Request → Anthropic API, 4 Kategorien) → `Parse Classification` → `Mark Alerted + Intent` (Google Sheets mit 4 Feldern) → `Notify Telegram` (erweitert mit Intent + Snippet).
- Auto-assigned credentials: Gmail OAuth2 ✓, Google Sheets OAuth2 ✓, Telegram ✓.
- **ILIAS MANUELL:** im n8n UI den Node `Claude Haiku Classify` öffnen und den bestehenden Anthropic-Credential (identisch zu dem, der im Lead URL Scorer läuft) zuweisen. Ohne das klassifiziert der Watcher nicht.

### Sheet-Spalten angelegt ✓
- Via Bootstrap-Workflow `qBcMn1OLg94XkeRa` → Execution 892 status=success.
- Angelegt: `reply_intent`, `reply_snippet`, `reply_analyzed_at` (leer, werden beim ersten echten Reply befüllt).
- Bootstrap-Workflow kann archiviert werden (einmalig, nicht mehr gebraucht).

### Validator-Test steht aus
- Voraussetzung: Anthropic-Credential im Reply Watcher zugewiesen.
- Testpfad: historische Replies (Grüne Erde = auto_responder, vivatrue = positive/question) sind bereits alerted und werden vom Filter geskippt. Einfachster Test: Test-Mail an eigene Gmail schicken mit Domain einer gesendeten Outreach-URL, abwarten bis `status=replied` gesetzt wird (nächster Gmail Status Sync um 08:00), dann Reply Watcher triggert und klassifiziert.

## Open Issues / Nächster Tag

1. **Firmenname-Gate entschärfen:** `validate_quality_gates` Gate 3 (`company_name.lower() not in subject.lower()`) failt bei Sonderzeichen. Fix: normalize vor Vergleich (strip non-alnum, lowercase, compare tokens). Zeit: ~15 Min.
2. **Discovery→Sheet-Sync:** `batch_analyze.py` mit `_sync_to_sheet` wird in Phase 2 Scheduler-Kette eingebunden.
3. **generate_outreach.py `--limit` Flag:** fehlt für bounded Daily-Runs. Zeit: ~10 Min.
4. **Apollo-API:** nicht getestet. Separater Lauf.
5. **Anthropic credential assignment:** siehe oben.

## Run Summary

- **Stages revived:** Discovery ✓, Outreach-Draft-Gen ✓, Reply-Classifier deployed (credential fehlt).
- **Drafts generiert:** 54 (24 erster Run + 30 Retry nach Quality-Gate-Fix). Fehler von 39 → 9.
- **Leads ohne Email:** 15 (no-email-queue.txt)
- **Domains entdeckt:** 94
- **n8n Workflows geändert:** 1 updated (Reply Watcher), 1 neu (Bootstrap, archivierbar).
- **Sheet-Spalten:** reply_intent, reply_snippet, reply_analyzed_at angelegt.
