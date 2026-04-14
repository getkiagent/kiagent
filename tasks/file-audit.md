# File Audit — 2026-04-11

---

## Definitiv löschen

| Datei/Ordner | Grund |
|---|---|
| `.playwright-mcp/` (alle 10 Dateien) | Auto-generierte Browser-Session-Logs und Screenshots. Kein dauerhafter Wert, werden bei jeder Playwright-Session neu erstellt. |
| `scripts/__pycache__/*.pyc` (5 Dateien) | Python Bytecode, wird bei jedem Run auto-regeneriert. Gehört in `.gitignore`. |
| `archive/summarize_reel.cpython-311.pyc` | Verwaiste .pyc-Datei außerhalb von `__pycache__`. Kein Source-py in archive. |
| `leads/discovered-urls.txt` | Quasi-Duplikat von `discovered-urls-new.txt` (254 vs 253 Zeilen, identischer Inhalt). New-Version ist aktueller. |

---

## Prüfen / wahrscheinlich löschen

### Leads

| Datei | Grund |
|---|---|
| `leads/urls.txt` (28 Zeilen) | Frühe manuelle URL-Liste (z.B. nur `junglück.de`). Vollständig durch `discovered-urls-new.txt` (253 Zeilen) ersetzt. |
| `leads/unscored-urls.txt` (29 Zeilen) | Generiert 2026-04-09 — URLs die noch nicht in batch-results sind. Wenn Wave 3 alle scored hat, obsolet. |
| `leads/unscored-clean.txt` (16 Zeilen) | Gefilterter Subset von `unscored-urls.txt`. Selbe Frage: Sind diese leads noch zu bearbeiten? |
| `leads/batch-results.json` (Wave 1, 96KB) | Wave 1 Ergebnisse. Bestätigt: kann raus. Vorerst behalten. |

### Outreach-Duplikate

| Datei | Grund |
|---|---|
| `outreach/styx-naturcosmetic.txt` | Älterer Outreach-Versuch (Thema: Anfrage-Routing). `styx-naturcosmetic-gmbh.txt` ist der neuere (Thema: Pre-Purchase). Klären ob erste Version abgeschickt wurde — wenn nicht, löschen. |
| `outreach/alle-tier-a.txt` | Aggregat aller Wave-1-Entwürfe in einer Datei. Redundant wenn die Einzel-TXTs noch da sind. |
| `outreach/wave2-alle-entwuerfe.txt` | Selbes Muster — Wave-2-Aggregat. Redundant. |

### Archive

| Datei | Grund |
|---|---|
| `archive/leads/missing_emails.json` | Altes Artefakt aus E-Mail-Suche. Wahrscheinlich behoben. |
| `archive/leads/single-test.json` | Test-Datei aus früher Entwicklung. |
| `archive/prompts/lead_analysis_v1.md` | Ältere DE-Version des Prompts. Aktuelle EN-Version liegt in `prompts/`. Archiv-Kopie vermutlich unnötig. |
| `archive/prompts/outreach_mail_v1.md` | Selbes Muster — ältere Version, aktuelle in `prompts/`. |
| `archive/docs/lead-engine-brief.md` | Altes Planning-Dokument. Durch `docs/architecture.md` ersetzt? |

### Andere Tools / Hidden Folders

| Datei/Ordner | Grund |
|---|---|
| `.augment/skills/` (leerer Ordner) | Augment Code hat Skills-Ordner angelegt, aber keine Dateien drin. Toter Ordner. |
| `.bob/skills/` (leerer Ordner) | Bob AI hat Skills-Ordner angelegt, aber keine Dateien drin. Toter Ordner. |
| `.agents/skills/humanize-writing/references/ai-tells.md` | Single-file-Skill eines anderen Tools. Wird nicht von Claude Code oder n8n genutzt. |

### Reels

| Datei | Grund |
|---|---|
| `reels/*.json` (3 Dateien) | Einmalige Analyse — nicht dauerhaft gebraucht. Können nach Verarbeitung gelöscht werden. |

### Website v1

| Datei/Ordner | Grund |
|---|---|
| `website/` (statisches HTML) | Abgelöst durch `website-v2/`. 9 Dateien inkl. Fonts, CSS, JS. |

### Screenshots / Root-Artefakte

| Datei | Grund |
|---|---|
| `qa-desktop.png` + `qa-mobile.png` | Website-QA-Screenshots vom 2026-04-11. Einmalige Verifikation — wenn Website deployed ist, können die weg. |

---

## Behalten

*(Nur Dateien aufgeführt wo unklar ob aktiv)*

| Datei | Warum behalten |
|---|---|
| `credentials.json` | ⚠️ Aktiv genutzt von `cleanup_drafts.py`, `fix_signature.py`, `send_existing_drafts.py` — aber **NICHT in `.gitignore`**. Muss sofort in `.gitignore` rein. |
| `token.json` | ⚠️ OAuth-Token, aktiv. **Nicht in `.gitignore`.** |
| `token.pickle` | ⚠️ OAuth-Token (Pickle-Format), aktiv. **Nicht in `.gitignore`.** |
| `leads/discovered-urls-new.txt` | Aktive Lead-URL-Liste (253 Zeilen). Basis für neue Discovery-Runs. |
| `leads/batch-results-wave2.json` | Wave 2 Scoring-Ergebnisse — aktiv. |
| `leads/batch-results-wave3.json` | Wave 3 Scoring — 611KB, neu. Wird von `run_followups.py` + `send_existing_drafts.py` referenziert. |
| `website-v2/` | Aktive Version (React/Vite, gebaut). |
| `Chatbot Link.txt` | Voiceflow + Loom Links — nützliche Referenz, klein. |
| `Claude Code Prompts — GetKiAgent.txt` | Prompt-Bibliothek — aktiv. |
| `.firecrawl/deinekiagentur.md` | Gecrawlte eigene Website — Referenz für Chatbot o.ä. |

---

## Sicherheits-Flag

**KRITISCH:** `credentials.json`, `token.json`, `token.pickle` sind im Projektordner aber **nicht in `.gitignore`**.  
Aktuelle `.gitignore` enthält nur `.env`.  
Wenn dieses Repo jemals auf GitHub landet, werden OAuth-Credentials exponiert.

**Fix:** Diese 3 Zeilen in `.gitignore` ergänzen:
```
credentials.json
token.json
token.pickle
```
