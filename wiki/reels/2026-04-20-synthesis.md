# Meta-Analyse 2026-04-20

Aggregation aus 57 Posts (siehe [[2026-04-20]]). Generiert: 2026-04-20 16:37

---

# Immediate Actions

---

**1. Outreach-Copy auf Problem-Solution-Replaces-Format umstellen**

- **Was konkret tun:** In `scripts/generate_outreach.py` den System-Prompt um folgendes Framing erweitern:
  ```
  Problem: [konkrete Zahl — z.B. "40% eurer Tickets sind Bestellstatus-Nachfragen"]
  Solution: [was der KI-Agent macht]
  Replaces: [was wegfällt — z.B. "2h täglich Support-Routine, verpasste Nachtanfragen"]
  ```
  Neue Variante als A/B-Variante gegen aktuellen Prompt deployen; Wave-2-Replies als Messbasis nutzen.
- **Herkunft:** Post by lvl_aiautomations (B2B Lead Generation AI, Slide-Deck)
- **Aufwand:** 30–45 Minuten
- **Warum jetzt:** Das Framing mit konkreten Zahlen und „Replaces"-Liste ist das nachweislich stärkste Conversion-Muster in diesem Marktsegment — Wave 2 läuft, jede verbesserter Reply-Rate zählt direkt.

---

**2. Positioning-Differenzierung schriftlich fixieren (1 Seite)**

- **Was konkret tun:** Ein internes Dokument (`docs/positioning.md`) anlegen, das explizit abgrenzt: GetKiAgent ≠ AI Voice Receptionist, sondern Text-Ticket-Automatisierung (Email/Chat) für DACH-E-Commerce mit Shopify/Shopware-Integration und Retouren-Fokus. Dieses Dokument als Grundlage für alle Outreach-Prompts referenzieren.
- **Herkunft:** lvl_aiautomations — Kiss/Marry/Kill Framework (Instagram)
- **Aufwand:** 20–30 Minuten
- **Warum jetzt:** Der Markt für „AI Kundenservice" wird als übersättigt wahrgenommen — ohne schriftlich fixierte Differenzierung schleicht sich generisches Framing in Pitches ein.

---

**3. ROI-Kennzahl als erste Zeile in alle Pitch-Varianten setzen**

- **Was konkret tun:** In allen aktiven Outreach-Templates (n8n-Node `QxBuMHhSHuCpq3m6` und Gmail-Draft-Node) prüfen, ob die erste inhaltliche Zeile eine konkrete ROI-Zahl enthält (z.B. „Shops wie eurer sparen durchschnittlich X Stunden/Woche"). Falls nicht: Prompt anpassen, sodass Claude die ROI-Aussage an Stelle 1 setzt, Features erst danach.
- **Herkunft:** lvl_aiautomations — Kiss/Marry/Kill, „MARRY = strongest ROI conversation"
- **Aufwand:** 20–30 Minuten
- **Warum jetzt:** Laut Markt-Sentiment ist ROI-Argumentation das stärkste Verkaufsgespräch überhaupt — jede ausgehende Email ohne ROI-Einstieg verschenkt Conversion-Potenzial.

---

**4. API-Modellnamen in bestehenden Workflows auf Opus-4.7-Kompatibilität prüfen**

- **Was konkret tun:** Alle n8n-Nodes und Skripte, die Claude-API-Calls machen, auf aktuell verwendete Modellnamen durchsuchen (`grep -r "claude-" scripts/ n8n/`). Prüfen, ob veraltete Modellnamen hinterlegt sind, die nach dem Anthropic-Naming-Update brechen könnten. Ggf. in Claude Code „migrate to Opus 4.7" ausführen lassen.
- **Herkunft:** ClaudeDevs — claude-api skill update (X/Twitter)
- **Aufwand:** 15–20 Minuten
- **Warum jetzt:** Anthropic hat das Modell-Naming-Schema aktiv geändert — ein stiller API-Fehler durch veralteten Modellnamen unterbricht laufende Wave-2-Automatisierungen ohne explizite Fehlermeldung.

---

**5. Prompt-Audit: Token-Ballast in den drei Kern-Prompts reduzieren**

- **Was konkret tun:** System-Prompts in `scripts/generate_outreach.py`, n8n-Outreach-Agent (`zVvZmfOWADGcN6kp`) und Gmail-Draft-Node auf redundante Wiederholungen, doppelte Instruktionen und unnötige Kontext-Blöcke prüfen. Ziel: Prompt-Länge um mindestens 30% kürzen ohne Qualitätsverlust. Für einfache Klassifikations-Steps (Reply-Kategorisierung, URL-Scoring) Haiku-4.5 statt Sonnet testen.
- **Herkunft:** Charly Wargnier (@DataChaz) + Indu Tripathi (@InduTripat82427) — Token-Optimierungs-Posts (X/Twitter)
- **Aufwand:** 45–60 Minuten
- **Warum jetzt:** 70–80% Context-Window-Verschwendung sind bei hochvolumigen Outreach-Pipelines direkte Betriebskosten — bei Wave 2 mit mehreren Hundert Calls summiert sich das messbar.

---

# Future Ideas

---

**1. Live-Demo-Agent: Shop-spezifische Kundenservice-Demo per Crawler**

- **Was:** Agent nimmt Shop-URL aus Lead-Liste → scraped FAQ, Retourenpage, Impressum, Produktkatalog → Claude trainiert Mini-Kundenservice-Bot auf diese Daten → Deploy auf `{shop-slug}.demo.getkiagent.de` → Outreach-Email enthält 3 echte Beispiel-Antworten mit der tatsächlichen Policy des Shops. „Show, don't tell."
- **Trigger-Bedingung:** Wave-2-Reply-Rate bleibt unter 15 % nach vollständigem Durchlauf; oder Wave 3 Tier-A wird gestartet
- **Warum jetzt nicht:** Wave 1 und 2 laufen noch; Conversion-Daten fehlen als Baseline. Aufwand von 2–3 Entwicklungstagen wäre vor dem ersten Daten-Signal verfrüht investiert.

---

**2. Level-5-Orchestrator: Vollautomatischer Nacht-Workflow (Discovery → Outreach → Follow-up)**

- **Was:** Ein n8n-Orchestrator-Workflow, der nachts autonom läuft: neue Leads discovern → scoren → Outreach-Draft generieren → Follow-up-Timing setzen → Reply-Watch auslösen. Isolierte Worktrees pro Nische (beauty/pflege/fashion), analog zu Claude Codes EnterWorktree-Tool.
- **Trigger-Bedingung:** Wave-2-Replies kommen rein und Ilias koordiniert mehr als 2 Agenten-Sessions manuell gleichzeitig (aktuell: Level 4)
- **Warum jetzt nicht:** Manuelle Orchestration ist bei aktuellem Volumen noch beherrschbar; Orchestrator-Design ohne Daten über Reply-Patterns würde zu früh auf unvalidierte Hypothesen optimieren.

---

**3. AgentShield-Integration als DSGVO-Trust-Signal**

- **Was:** Open-Source-Security-Test-Suite (1.282 Tests) in den GetKiAgent-Auslieferungsprozess integrieren. Jede Kundenkonfiguration durchläuft die Test-Suite vor Go-Live. Im Pitch kommunizierbar: „Jede Konfiguration wird gegen 1.282 Sicherheitsszenarien getestet."
- **Trigger-Bedingung:** Erster Paying-Customer ist gewonnen; Onboarding-Prozess wird formalisiert
- **Warum jetzt nicht:** Kein Paying-Customer, kein Onboarding-Prozess — Integration ohne Ziel-Kontext ist verfrühte Infrastruktur.

---

**4. Remotion-Video-Generator für automatisierte Case-Study-Videos**

- **Was:** `/remotion-video`-Skill in Claude Code nutzen, um wöchentlich kurze Case-Study-Videos zu generieren („Shop X: 40 % Ticket-Reduktion in 2 Wochen") für LinkedIn/Instagram-Distribution.
- **Trigger-Bedingung:** Erster Paying-Customer vorhanden und hat Einverständnis für Case Study gegeben
- **Warum jetzt nicht:** Kein Content-Push geplant, kein Paying-Customer als Basis — Marketing-Content ohne echte Ergebnisse ist glaubwürdigkeitsschädlich im DACH-B2B-Segment.

---

**5. Instagram-DM-Funnel via Boosend.ai + Claude Connector**

- **Was:** Meta-verifizierter DM-Automation-Funnel: Kommentar „KI-Demo" unter Post → automatisch DM mit Calendly-Link + Mini-Demo. Keyword-Trigger, Voice-Clone-Replies als Differenzierungsmerkmal.
- **Trigger-Bedingung:** Organische Content-Engine auf Instagram ist aktiv und generiert regelmäßig Reichweite (>500 Likes/Post)
- **Warum jetzt nicht:** Kein Instagram-Funnel aktiv, Outreach-Kanal ist Cold Email — Infrastruktur ohne Traffic ist wertlos.

---

**6. Claude Design für Landing-Page-Varianten (A/B-Tests)**

- **Was:** claude.ai/design nutzen, um schnell alternative Landing-Page-Varianten zu generieren und Conversion-Unterschiede zu testen (z.B. ROI-fokussierte vs. Feature-fokussierte Headline).
- **Trigger-Bedingung:** Genug inbound Traffic für statistisch signifikante A/B-Tests (>200 Besucher/Woche)
- **Warum jetzt nicht:** Aktuelle Website funktioniert; bei Pre-Revenue-Traffic-Volumina sind A/B-Tests nicht aussagekräftig.

---

**7. DACHGuard / Compliance-Layer als eigenständiges Modul**

- **Was:** Dedizierter Sicherheits- und DSGVO-Compliance-Layer für GetKiAgent-Deployments, vermarktbar als „DACHGuard"-Add-on für besonders regulierungssensible Händler.
- **Trigger-Bedingung:** €3k MRR erreicht; mindestens 2 Kunden haben Compliance explizit als Kaufhürde genannt
- **Warum jetzt nicht:** Wave-3+-Thema; ohne Kundenfeedback ist unklar, ob Compliance als Zahlungsbereitschaft oder nur als Hygienefaktor wahrgenommen wird.

---

**8. Shopify-App-Listing**

- **Was:** GetKiAgent als native Shopify-App im App-Store listen, um Inbound-Leads über Shopify-Ökosystem zu generieren.
- **Trigger-Bedingung:** Shopify-Integration technisch stabil und von mindestens 3 Paying-Customers validiert; App-Review-Prozess (~4–8 Wochen) eingeplant
- **Warum jetzt nicht:** App-Store-Listing ohne stabile Integration und Kundenbewertungen verbrennt Reputation; außer
