# Website-v2 Redesign — Design Brief

**Target:** Tier-A DACH E-Commerce Founders receiving cold outreach. Skeptical-curious mix.
**Goal:** Contact-Click. Seriös, erfahren, authentisch, kompetent in <10s.
**Reference priority:** ki-agentur.com (primary), peter-krause.net (typography), digirelation (minimal corporate).

---

## Positioning insight (was unterscheidet uns?)

Ilias ist Solo-Builder ohne Customer-Base. Fake Testimonials = Glaubwürdigkeitskiller. Statt Social Proof → **Transparenz-Proof**: Live-Demo, Tech-Stack, konkrete Deliverables, ehrliche Sprache, "Ich baue jeden Agenten individuell". Differenzierung: **Nicht noch eine KI-Agentur mit Templates**, sondern Custom-Build-Werkstatt.

## Palette — "Seriös-Corporate DACH B2B, nicht Startup-SaaS"

Weg vom generischen AI-Purple/Blau. Gewählt: **Deep Slate + warmes Off-White + gedämpftes Gold**. Vermittelt Mittelstands-Seriosität ohne Tech-Startup-Look.

| Token | Hex | Verwendung |
|---|---|---|
| `--bg` | `#0b0e14` | Page background (near-black navy) |
| `--bg-elevated` | `#131720` | Card / section alt |
| `--border` | `#23293a` | Hairlines |
| `--border-strong` | `#2e3548` | Emphasised borders |
| `--text` | `#f5f3ec` | Primary text (warm off-white) |
| `--text-muted` | `#8892a6` | Secondary text |
| `--text-subtle` | `#5a6278` | Tertiary (captions, legal) |
| `--accent` | `#c9a66b` | CTA, highlights (muted gold) |
| `--accent-hover` | `#d9b87e` | Hover state |
| `--accent-soft` | `rgba(201,166,107,0.12)` | Glow / tints |

Kein Gradient-Missbrauch. Ein einziges accent-color. Keine Purple/Cyan/Neon-Farben.

## Typography — Google Fonts

- **Display (Headlines):** `Fraunces` (variable serif) — wght 400–600, optical-size 144. Seriöser Serif-Anchor, sticht aus Standard-Sans heraus, aber nicht barock.
- **Body:** `Inter Tight` (variable sans) — wght 400–600. Clean, lesbar, neutral.
- **Sizes:**
  - Display XL: clamp(2.75rem, 6vw, 4.75rem) / line-height 1.05 / tracking -0.02em
  - Display L: clamp(2rem, 4.5vw, 3.25rem) / line-height 1.1
  - Body L: 1.125rem / 1.65
  - Body: 1rem / 1.65
  - Body S: 0.875rem / 1.55
  - Caption: 0.75rem / uppercase / tracking 0.12em

## Spacing system

Base 8px. Section padding: `clamp(4rem, 9vw, 7rem) clamp(1.5rem, 4vw, 3rem)`. Max container width: 1120px. Content text max: 640px.

---

## Section order + copy

### 1. Nav
- Logo left (GetKiAgent, "Agent" in accent gold)
- Right: single button "Kostenloses Gespräch" → scrolls to #kontakt
- Sticky, shrinks to solid bg with hairline on scroll
- NO nav-links (one-pager focus, no "Leistungen/Preise")

### 2. Hero
- Eyebrow: `KI-SUPPORT-AUTOMATION · DACH E-COMMERCE`
- **Headline (DE, 11 words):** *"Individuelle KI-Support-Automation für deinen Shop — nicht zusammengeklickt."*
- **Subline:** *"Ich baue n8n-basierte Agenten, die auf deinem Stack laufen, deine echten Tickets beantworten und in deiner eigenen Cloud gehostet werden. Kein SaaS-Abo, kein Template."*
- Primary CTA: `Kostenloses Erstgespräch →`
- Secondary CTA: `Live-Demo ansehen` (scrollt zu Credibility/Loom)
- Trust-Row (unterhalb CTAs, subtil): `DSGVO-konform · EU-gehostet · Individueller Build · Setup in 2 Wochen`
- Hintergrund: dezenter radial glow bottom-center, Accent-Gold 6% Opacity. Kein Hero-Bild.

### 3. "Was du bekommst" (Features → Deliverables)
- Eyebrow: `LIEFERUMFANG`
- Headline (Serif): *"Konkrete Deliverables. Keine Buzzwords."*
- Sub: *"Was du nach zwei Wochen in der Hand hast."*
- 4 Cards (2×2 grid, 1 col mobile):
  1. **n8n-Workflow auf deinem Stack** — "Läuft in deiner eigenen n8n-Instanz oder bei uns. Du behältst volle Kontrolle über Code, Daten und Workflows."
  2. **Gmail-Draft-Automation** — "Eingehende Support-Mails werden automatisch analysiert und als Entwurf in Gmail vorformuliert. Du prüfst und sendest — oder aktivierst Auto-Versand."
  3. **Shop-Anbindung** — "Direkt an Shopify/WooCommerce/Shopware angebunden. Bestellstatus, Tracking, Retouren werden aus echten Daten beantwortet — nicht halluziniert."
  4. **DSGVO-konform & EU-gehostet** — "Alle Daten bleiben in der EU. Auftragsverarbeitungsvertrag inklusive. Keine US-Hyperscaler im Daten-Pfad."

### 4. HowItWorks — "Vom Gespräch zum Live-Agent"
- Eyebrow: `ABLAUF`
- Headline (Serif): *"Drei Schritte. Keine Überraschungen."*
- 3 Steps (vertikale Timeline, Nummern links, Content rechts):
  1. **Analyse (30 Min)** — "Wir schauen deinen Support-Alltag, deine häufigsten Ticket-Typen und deinen Stack an. Du bekommst eine ehrliche Einschätzung — auch wenn KI bei dir (noch) nicht sinnvoll ist."
  2. **Bauen (2–3 Wochen)** — "Ich baue deinen Agenten auf n8n, verbinde ihn mit deinem Shop und trainiere ihn auf deine echten Tickets. Du bekommst Zwischenstände, nicht nur ein Endergebnis."
  3. **Launch & Betrieb** — "Go-Live wird begleitet, erste Woche engmaschig. Danach: monatliches Reporting, Anpassungen, direkter Draht zu mir."

### 5. Credibility — "Warum mit mir"
- Eyebrow: `WARUM MIR`
- Headline (Serif): *"Kein Template. Kein Baukasten. Kein Abo."*
- **Self-authored statement** (Serif, left-aligned, large):
  > *"Ich baue seit 2024 KI-Support-Workflows auf n8n-Basis. Jeder Agent wird für einen konkreten Shop entwickelt — angepasst an Stack, Ticket-Typen und Tonalität. Statt Demo-Screenshots zeige ich dir direkt eine Live-Demo eines funktionsfähigen Systems."*
  >
  > — Ilias Tebque, Gründer GetKiAgent
- **Loom-Embed** (lazy-loaded, thumbnail poster): `https://www.loom.com/share/a243a6f8c920487a9db15e9c9816c36e`
- **Tech-Stack-Row** (subtil, unterhalb):
  `Entwickelt mit` · n8n · Claude (Anthropic) · Gmail API · Shopify/WooCommerce · Playwright · Python

**KEIN** Fake-Testimonial. **KEIN** "50+ Projekte". **KEIN** Kunden-Logo-Wall.

### 6. Contact
- Eyebrow: `KONTAKT`
- Headline (Serif): *"30 Minuten. Keine Verkaufsmasche."*
- Sub: *"Buch dir einen Call. Wir schauen deinen Support-Alltag an und ich sage dir ehrlich, ob KI bei dir Sinn ergibt."*
- **Cal.com Iframe-Embed**: `https://cal.com/getkiagent/30min` (Höhe 640px, responsive)
- Fallback darunter (kleiner Text): *"Cal.com lädt nicht? Schreib direkt an:* `getkiagent@gmail.com`"

### 7. Footer
- Minimal single-row (flex wrap)
- Left: `© 2026 GetKiAgent · Ilias Tebque`
- Center: `Impressum` · `Datenschutz`
- Right: `getkiagent@gmail.com`
- Border-top hairline, background `--bg` (same as page)

---

## Credibility strategy ohne Testimonials

| Signal | Wie |
|---|---|
| Ehrlichkeit | "Auch wenn KI bei dir (noch) nicht sinnvoll ist" – expliziter Opt-Out |
| Transparenz | Tech-Stack offengelegt, n8n als Basis benannt |
| Beweis | Live-Loom-Demo statt Stock-Screenshots |
| Personal | Gründer-Zitat signiert, kein "wir" ohne Körper |
| Kontrolle | "Läuft in deiner eigenen Cloud" – kein Lock-in-Risiko |
| Compliance | DSGVO + EU-hosted + AVV mehrfach genannt |
| Kein Hype | Serif-Headlines, gedämpftes Gold, keine Neon-Farben |

## Out (explizit entfernt)

- Pricing section
- Testimonials section
- Nav-Links "Leistungen/Preise"
- "60%/80%" Kennzahlen (unbewiesen)
- "24/7 verfügbar" als Feature (selbstverständlich)
- Mehrere Gradient-Farben
- Stock-Icons als primäre Feature-Illustration

## Assets needed

- [x] Loom embed URL (vorhanden)
- [x] Cal.com link (cal.com/getkiagent)
- [ ] Workflow-screenshots für HowItWorks Thumbnails → **Fallback falls keine vorhanden:** Nur Text-Timeline, keine Bild-Platzhalter
- [ ] Favicon (already in public/)
- [ ] OG-Image → **Fallback:** Text-only OG via Vercel OG (falls Zeit), sonst Loom-Thumbnail-URL

## Technical notes

- React 19, Vite 8, Tailwind 4 — bleibt
- lucide-react für Icons — bleibt
- Inline styles → Komponenten weiter inline styled (konsistent mit aktuellem Stil), CSS-Variablen in `index.css`
- Fonts via Google Fonts CDN import in `index.css` (existiert bereits für Plus Jakarta → ersetzen)
- Cal.com embed: iframe mit `loading="lazy"`, fallback mailto darunter
- Loom: `<iframe>` mit `loading="lazy"` + aspect-ratio 16:9
