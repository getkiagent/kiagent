# Blocked Tasks — Website Build

Dokumentation von Tasks, die während des Overnight-Builds geskippt wurden.

**Format:** Task-Nummer | Titel | Grund | Was manuell getan werden muss

---

<!-- Einträge werden während des Builds hier hinzugefügt -->
<!-- Beispiel:
## Task 3 — Inter Font Files beschaffen
**Grund:** google-webfonts-helper API nicht erreichbar (404)
**Workaround:** Fonts System-Stack gesetzt als Fallback
**Manuell:** Inter-WOFF2 von rsms.me/inter herunterladen und nach website/assets/fonts/ legen
-->

## 2026-04-11 — Task 13: Git-Commit übersprungen
Kein .git-Repository im Projektordner vorhanden.
Action: `git add website/ tasks/ && git commit -m "feat: Phase 1 — website structure, nav, sections, QA"` manuell ausführen nach `git init`.
