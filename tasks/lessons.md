# Tasks & Lessons

### 2026-04-16 — research-deep + web-search-agent
`research-deep` + `web-search-agent` für strategische Selbstanalyse = massive Overshoot. Nur für echte Produkt-/Markt-Discovery verwenden, wo Websuche zwingend nötig ist.

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

### 2026-04-14 — Pipeline Audit: 8 Scripts gefixt, 5 n8n Workflows inspiziert
**Kontext:** Vollständiger Audit aller Python-Scripts + n8n-Workflows gegen PLAN.md.

**Kritischste Findings:**
- `generate_outreach.py`: 4 von 5 PLAN.md Stage-4 Quality Gates waren unvollständig oder fehlten komplett. Subject-Check war als "Can't validate — skip here" gestubbt, obwohl company_name verfügbar war. PS-Gate prüfte nur "P.S." aber nicht Loom-URL. Signatur-Gate fehlte komplett. Skip-if-exists fehlte → Scripts überschrieben existierende Outreach-Files. No-email-queue.txt wurde nie geschrieben — stattdessen Placeholder `[EMAIL MANUELL EINTRAGEN]` injiziert.
- `send_existing_drafts.py`: `--keep-existing` Flag fehlte (Regression, bereits 2026-04-11 dokumentiert, nicht umgesetzt). PLAN.md Stage 5 griff ins Leere.
- `discover_leads.py`: DDG-Rate-Limit-Matrix nicht implementiert. Einfaches `return []` bei Exception, keine 30s-Retry.
- `analyze_lead.py`: Jina Timeouts wurden als generische Errors maskiert — Retry-Logic in `batch_analyze.analyze_one` triggerte nie.
- `delete_all_drafts.py`: Kein Confirmation-Prompt, kein --yes Flag. Footgun.
- `cleanup_drafts.py`: Bearbeitete ALLE Gmail-Drafts ohne Filter. Risiko: löscht Ilias' persönliche Drafts.
- 5 Gmail-Scripts: Keine einzige hatte `RefreshError`-Handling auf `creds.refresh()`.
- n8n WF2 "Outreach Agent": Inline-Prompt fordert EXPLIZIT verbotene Phrasen ("Kein Skript-Bot", "24/7, auf Deutsch") + "Ilias Tebque" (Nachname verboten) + PS-Zeile mit Loom-URL KOMPLETT FEHLEND.

**Fixes:**
- `generate_outreach.py`: Konstanten `SIGNATURE_REQUIRED`, `LOOM_URL_SUBSTR`, `PS_REQUIRED_SUBSTR`, `HARDCODED_FORBIDDEN` ergänzt. `validate_quality_gates(mail_text, config, company_name)` komplett neu: 4 PLAN.md-Gates + optionale niche-config-Gates. Main loop: skip-if-exists am Start, no-email-queue statt Placeholder, Regenerate-Once bei Gate-Fail. Jina `except Exception` → `except requests.RequestException`.
- `send_existing_drafts.py`: `--keep-existing` Flag + `fetch_existing_draft_recipients()`. `RefreshError`-Handling in get_gmail_service. Exponential backoff in create_draft (HTTP 429/5xx, 3 retries). `--niche` Flag für output_dir.
- `discover_leads.py`: DDG rate-limit retry (30s wait, 1 retry). `mkdir(parents=True)`. Narrow excepts.
- `analyze_lead.py`: Jina `Timeout` → raise `FirecrawlTimeoutError` (nicht silently None). `scrape_pages`: Homepage timeout propagiert; Subpage timeouts weiter non-fatal. Sitemap + Cache excepts narrowed.
- `delete_all_drafts.py`: Interaktive Confirmation ("DELETE" tippen) oder `--yes`. RefreshError-Handling. Exponential backoff.
- `cleanup_drafts.py`: `--filter-subject PATTERN` für Safety. Interaktive Warnung wenn kein Filter. Deterministisches "keep" (prefer drafts with Loom, sonst neuester). RefreshError-Handling. Try/except + backoff im delete loop.
- `batch_analyze.py`: `mkdir(parents=True)` für niche-Pfade.
- `lead_schema.py`: `confidence_level` null-safety (`isinstance str`).

**n8n UI-Manual-Fixes (MCP-Update blockiert weil komplex):**
- WF2 Outreach Agent: Inline-Prompt MUSS komplett gegen `prompts/outreach_mail_v1.md` synchronisiert werden. Aktuell generiert WF2 Mails die gegen die lokale Spec verstoßen.
- WF1 Lead URL Scorer: Node "Parse Lead Score" braucht `onError: continueErrorOutput` — aktuell stoppt Workflow bei Claude-JSON-Parse-Error ohne Status-Write ins Sheet.
- WF3 Gmail Draft from Outreach: Kein Error-Handling. Wenn Gmail fails → silent loss.
- WF5 Follow-up Checker: Kein Stage-3 (14 Tage), kein Webhook-Trigger obwohl PLAN.md `N8N_FOLLOWUP_WEBHOOK` vorschreibt. Inline-Prompt hat Nachname "Tebque".

**Going forward:**
- 3 Signatur-Varianten im Projekt entdeckt: `prompts/outreach_mail_v1.md` ("Ilias\nGetKiAgent — KI-Support für E-Commerce"), n8n-Workflows ("Ilias Tebque..."), `configs/ecommerce-beauty.yaml` ("Ilias Ism | GetKiAgent"). Muss kanonisiert werden.
- Umlaut-Duplikate in outreach/ gefunden: `johannas-kräutergarten-...` + `johannas-kr-utergarten-...`, `sonnengrün.txt` + `sonnengr-n.txt`. `slugify()` in generate_outreach.py erzeugt uneinheitliche Slugs je nach Input-Encoding.
- Gmail-Auth-Util als gemeinsames Modul empfohlen (statt 5x duplizierte Logic).

### 2026-04-14 — Apollo organization_revenue_ranges bricht alle Ergebnisse
**Error:** `discover_apollo.py` returned "Keine Ergebnisse" trotz 1.484 verfügbarer Unternehmen.
**Root cause:** `organization_revenue_ranges: ["1000000,30000000"]` liefert immer 0 Treffer — Apollo akzeptiert kein Raw-Number-Format für dieses Feld. Ohne den Filter: 524+ Ergebnisse.
**Fix:** Revenue-Filter-Zeile aus `build_payload()` entfernt, `REVENUE_RANGES`-Konstante gelöscht, Print-Label angepasst. Apollo Revenue-Filter vorerst nicht verwenden bis korrektes Enum-Format bekannt.

### 2026-04-15 — Apollo mixed_people/search deprecated
**Error:** enrich_contacts.py warf 422 "endpoint deprecated" auf alle 78 Lead-Calls.
**Root cause:** Apollo hat `mixed_people/search` deprecated zugunsten von `mixed_people/api_search`.
**Fix:** Endpoint-URL in scripts/enrich_contacts.py geändert. Rerun: 40/78 Hits (51%).

### 2026-04-15 — Apollo Basic redactet Last-Name/Email/LinkedIn
**Error:** Nach Endpoint-Fix: 40 Named Contacts gefunden, aber 0 mit Email/Lastname/LinkedIn.
**Root cause:** Apollo Basic-Abo gibt aus `mixed_people/api_search` nur First-Name + Title zurück. Email/LinkedIn/Lastname sind nur via `people/match` (Reveal-Credit) abrufbar.
**Fix:** First-Name + Title in Outreach-Anrede nutzen (deutlich besser als "Hallo Team"). Reveal-Calls für Top-Leads bei Bedarf separat.

### 2026-04-15 — Impressum-Pflicht (§5 TMG) in Outreach-Mails
**Error:** Bisherige Outreach-Mails hatten kein Impressum — §5 TMG verlangt es in geschäftlicher Mail-Kommunikation. Abmahn-Risiko in DACH.
**Root cause:** Compliance-Layer fehlte. Nur §7 UWG Opt-out war enforced.
**Fix:** `impressum_line` in configs/ecommerce-beauty.yaml. Deterministisches Post-Processing in generate_outreach.py (`_ensure_impressum`) hängt Block nach Signatur an. Quality-Gate prüft Präsenz + End-Position. Prompts markieren "wird automatisch angehängt" damit LLM keine Duplikate erzeugt.

### 2026-04-16 — Reply-Alert Setup: 4 Bugs in einer Kette
**Error:** check_replies.py (existing) crashed auf Start; kein Alert seit Inbetriebnahme, 2 Replies (13.04., 11.04.) lagen unbemerkt im Postfach.
**Root cause:**
1. `gspread`/`google-auth` nicht installiert (ImportError)
2. `GOOGLE_SERVICE_ACCOUNT_JSON` nicht in .env (nur OAuth `token.json` für Gmail vorhanden)
3. `read_thread.py` druckt Body mit Windows-cp1252 → UnicodeEncodeError bei U+FFFC (object replacement char aus Gmail-Inline-Bildern)
4. Telegram sendMessage mit `parse_mode=HTML` failed weil `"Name" <email@x>` Brackets als HTML-Tags interpretiert
**Fix:**
1. `pip install gspread google-auth`
2. Neuer `check_gmail_replies.py` nutzt direkt Gmail OAuth (`token.json`) statt Service-Account → kein Sheet nötig. Dedup via `tasks/alerted-replies.json`. Auto-Responder-Filter per Subject/From/Body-Snippet.
3. `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` am Script-Start
4. `html.escape()` um From/Subject/Date/Snippet vor HTML-parse
5. Windows Task Scheduler `GetKiAgentReplyWatcher` alle 15 Min via .bat-Wrapper
**Findings:** 2 Replies surfaced — Grüne Erde (Auto-Follow-up "wir leiten weiter"), vivatrue/BellFill (echter warm Lead, letzter Touch 11.04., braucht manuelle Nachfass-Mail).
**Caveat:** Scheduler läuft nur bei angemeldetem User. Für 24/7 später: Cloud-Deploy (n8n/Railway).

### 2026-04-16 — Follow-up Queue: 53 Drafts aus 104 gesendeten Mails (kein Reply)
**Flow:** `build_followup_queue.py` scannt Gmail Sent (30d) → filtert Replies raus → Stage-Bucket nach Alter → matched Empfänger-Domain mit batch-results → schreibt `leads/followup-queue.json`.
**Result:** 70 Queue-Einträge (35 Stage 1 + 35 Stage 2) → `run_followups.py --input leads/followup-queue.json` → 56 generiert, 14 Errors (no-original-mail), 53 Gmail Drafts erstellt.
**Bug:** `run_followups.py` übergibt kein `--niche` an `generate_outreach.py` → `_ensure_impressum` skipped → 14 Drafts (neue Followups) initial ohne Impressum.
**Fix hotfix:** Neues Script `append_impressum.py` appendet Impressum lokal zu .txt-Files. `update_drafts_impressum.py` (existing) patched 11 Gmail-Drafts in-place. Kein Neu-Versand nötig.
**Permanent fix (TODO):** In `run_followups.py` → `generate_followup_mail()` `--niche ecommerce-beauty` mitgeben, damit generate_outreach.py Impressum automatisch anhängt.
**No-match recipients (28):** Domain-Mismatch zwischen Sent-Email und Lead-URL im batch-results (z.B. sent to `info@village-cosmetics.de` aber Lead-URL ist `drbronner.de`). Kein Follow-up generiert für diese. Nachfüllen manuell wenn Priorität.
