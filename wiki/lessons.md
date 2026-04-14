# Lessons Learned

## 2026-04-09 | Projekt-Audit & Strukturbereinigung

**Kontext:** Erster vollständiger Audit des getkiagent-Projektordners.

**Findings:**

1. **Falsche Extensions** — `lead-engine-brief.mdclaude` war ein Claude-Fehler-Artefakt. Sofort löschen wenn Extension falsch.

2. **Datei-Duplikate** — `glowlab-knowledge.txt` war 100% Duplikat von `.md`. Bei Voiceflow-KBs immer nur eine Version behalten.

3. **Ordner-Scope** — `summarize_reel.py` war in `/scripts` aber kein Lead-Engine-Script → nach `/tools` verschoben. Regel: `/scripts` nur für Lead-Engine-Pipeline.

4. **Leere Ordner** — `/workflows` war seit Erstellung leer. n8n-Workflows leben in n8n, nicht im Repo. Platzhalter-Ordner ohne Plan vermeiden.

5. **Prozess-Gaps** — `tasks/lessons.md` existierte als Template aber ohne Einträge. Prozess war nicht etabliert.

**Regeln going forward:**
- Nach jedem Task einen Eintrag in `tasks/lessons.md` anlegen.
- Neue Dateien sofort in die richtige Kategorie einordnen (`/scripts`, `/tools`, `/archive`), nicht im Root ablegen.
