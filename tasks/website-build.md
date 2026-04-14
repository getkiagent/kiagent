# GetKiAgent Website — Build Task List

**Ziel:** Vollständige Single-Page-Website für getkiagent.de, Vanilla HTML + CSS + JS, static deploybar (Netlify/Cloudflare Pages).

**Gesamt:** 20 atomare Tasks in 2 Phasen.
**Phase 1:** Tasks 1–13 (Setup, Struktur, Core Design, QA)
**Phase 2:** Tasks 14–20 (Preise, Polish, SEO, Cookie, Final QA)

---

## 🔑 Global Settings — für alle Tasks gültig

| Setting | Wert |
|---|---|
| Projekt-Ordner | `website/` (relativ zum Repo-Root) |
| Tech-Stack | Vanilla HTML + CSS + JS, kein Build-Step |
| Domain | `getkiagent.de` |
| E-Mail (überall) | `getkiagent@gmail.com` |
| Name | Ilias Tebque |
| Adresse | Eichelstraße 87, 40599 Düsseldorf |
| USt-Status | Kleinunternehmer § 19 UStG |
| Font | Inter self-hosted (kein Google CDN) |
| Farbschema | Dark — siehe Design Tokens in Task 4 |
| Modell | Sonnet (nicht Opus) |
| Sprache | Deutsch für UI, Englisch für Code-Kommentare |
| Kommentare | Sparsam — nur wo WHY nicht-offensichtlich |

---

## 🎨 Design Tokens (in Task 4 als CSS Custom Properties)

```css
--color-bg: #0f172a;          /* Dark Background */
--color-bg-alt: #1e293b;      /* Cards, Section-BG */
--color-bg-elevated: #334155; /* Hover states */
--color-accent: #3b82f6;      /* Electric Blue — Primary CTA */
--color-accent-hover: #2563eb;
--color-accent-soft: rgba(59, 130, 246, 0.1);
--color-text: #e2e8f0;        /* Body text, AAA contrast */
--color-text-muted: #94a3b8;  /* Secondary text, AAA contrast */
--color-text-heading: #f8fafc;
--color-border: #334155;
--container-max: 1200px;
--section-padding-y: 6rem;
--section-padding-x: 1.5rem;
--radius: 0.75rem;
--radius-lg: 1rem;
--transition-base: 0.3s ease;
--shadow-card: 0 4px 20px rgba(0, 0, 0, 0.3);
--shadow-card-hover: 0 10px 40px rgba(59, 130, 246, 0.15);
```

**Breakpoints:** Mobile-first → 640px (sm) → 768px (md) → 1024px (lg) → 1280px (xl)

---

# PHASE 1 — Setup + Struktur + Core Design

---

## Task 1 — Ordnerstruktur + leere Platzhalter-Dateien erstellen

**Ziel:** Komplettes Dateigerüst anlegen, damit nachfolgende Tasks nur noch befüllen.

**Dateien erstellen (leer oder mit Minimal-Inhalt):**
```
website/
├── index.html              (leer)
├── impressum.html          (leer)
├── datenschutz.html        (leer)
├── robots.txt              (leer)
├── sitemap.xml             (leer)
├── favicon.svg             (leer)
├── assets/
│   ├── style.css           (leer)
│   ├── script.js           (leer)
│   ├── logo.svg            (leer)
│   └── fonts/              (Ordner, leer)
└── images/
    └── .gitkeep            (leere Datei)
```

**Akzeptanz:** `ls website/` zeigt alle Top-Level-Files + `assets/` + `images/`. `ls website/assets/` zeigt 3 Files + `fonts/` Ordner.

---

## Task 2 — Referenz-Scrape (Firecrawl MCP)

**Ziel:** Design-Muster der direkten DACH-Konkurrenz extrahieren.

**Schritte:**
1. Firecrawl-Scrape: `https://deinekiagentur.com` (markdown output)
2. Extrahiere aus Output:
   - Hero-Headline-Muster (Länge, Tonalität, Call-to-Benefit-Struktur)
   - Section-Reihenfolge
   - CTA-Copy-Muster
   - Social-Proof-Strategie
3. Schreibe 5–8 Zeilen Insights in `tasks/lessons.md` unter Überschrift `## 2026-04-11 — Website-Referenz-Analyse`

**Fallback:** Wenn Firecrawl fehlschlägt oder Site JS-heavy ist → skip, baue aus Spec-Wissen. Eintrag in `tasks/blocked.md`.

**Akzeptanz:** `lessons.md` enthält neuen Eintrag ODER `blocked.md` dokumentiert Skip.

---

## Task 3 — Inter Font Files beschaffen

**Ziel:** Inter als self-hosted WOFF2 in `/website/assets/fonts/`.

**Schritte:**
1. Download via `curl` von google-webfonts-helper oder direkt von rsms.me/inter
2. Benötigt: Inter 400, 500, 600, 700 — nur `latin` subset — Format `woff2`
3. Zielpfad: `website/assets/fonts/inter-{weight}.woff2`

**Konkrete URLs (rsms.me Inter v4 Variable Font Fallback-Option):**
- Primär: https://gwfh.mranftl.com/api/fonts/inter?download=zip&subsets=latin&variants=regular,500,600,700&formats=woff2
- Fallback: Einzel-Downloads von fonts.gstatic.com via google-webfonts-helper API

**Fallback:** Wenn Download fehlschlägt → Skip, setze in Task 4 `font-family` auf System-Font-Stack. Eintrag in `blocked.md`. Weiter.

**Akzeptanz:** 4 WOFF2-Dateien in `website/assets/fonts/` ODER blocked.md dokumentiert.

---

## Task 4 — `style.css` Teil 1: Design Tokens + Reset + Typography + Utilities

**Ziel:** CSS-Foundation, die alle folgenden Sections nutzen.

**Inhalt:**
1. `@font-face` Deklarationen für Inter (4 Weights), `font-display: swap` — falls Fonts aus Task 3 vorhanden; sonst System-Font-Stack
2. CSS Custom Properties (alle Tokens aus Abschnitt "Design Tokens" oben)
3. CSS Reset (`*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }`)
4. `html { scroll-behavior: smooth; }` + `@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } * { animation: none !important; transition: none !important; } }`
5. `body` — Background, Farbe, Line-Height, Font-Family, `-webkit-font-smoothing: antialiased`
6. Base Typography: `h1`–`h6`, `p`, `a`, `ul`/`li` — Sizes, Weights, Farben
7. Utilities:
   - `.container { max-width: var(--container-max); margin: 0 auto; padding: 0 var(--section-padding-x); }`
   - `.btn` Base
   - `.btn-primary` (accent bg)
   - `.btn-secondary` (outline)
   - `.section` Base (padding-y)
   - `.visually-hidden` (a11y)
8. Focus-Styles (`:focus-visible` mit Accent-Outline)
9. Skip-Link-Styling (`.skip-link`)

**Akzeptanz:** `style.css` enthält alle obigen Sektionen, valide CSS (keine Syntax-Errors).

---

## Task 5 — `style.css` Teil 2: Navigation + Hero

**Ziel:** Nav-Bar sticky mit Scroll-Effekt, Hero fullscreen.

**Nav-CSS:**
- `position: fixed; top: 0; width: 100%; z-index: 100;`
- Default: `background: transparent; backdrop-filter: blur(8px);`
- `.scrolled` Klasse: `background: rgba(15, 23, 42, 0.95); border-bottom: 1px solid var(--color-border);`
- Logo links, Links zentriert/rechts, CTA-Button rechts
- Mobile: Hamburger (44×44px Touch-Target), Links als Overlay beim Öffnen
- Mobile-Overlay: `position: fixed; inset: 0; background: var(--color-bg); display: flex; flex-direction: column; align-items: center; justify-content: center;`

**Hero-CSS:**
- `min-height: 100vh; display: flex; align-items: center; justify-content: center; text-align: center;`
- `padding-top: 120px` (wegen fixed Nav)
- `h1` groß: `clamp(2rem, 5vw, 4rem)`, Line-Height 1.1
- Subline: `max-width: 720px; color: var(--color-text-muted); font-size: clamp(1rem, 2vw, 1.25rem);`
- CTA-Container: Flex, Gap, wrap auf Mobile
- Subtiler Gradient-Background (von `--color-bg` zu `--color-bg-alt`)

**Akzeptanz:** CSS valide, keine Selektoren ohne Inhalt.

---

## Task 6 — `style.css` Teil 3: Alle übrigen Sections

**Ziel:** Problem, Services (ohne Preise), Über-mich, Demo, Kontakt, Footer.

**Section-Styles:**
- **Problem:** `display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;`. Pain-Cards mit Icon-Placeholder (CSS-Circle) + Heading + Text.
- **Services:** Grid mit 3 Cards. Card: `background: var(--color-bg-alt); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 2rem;`. Middle-Card `.featured` Klasse: stärkere Border in Accent-Farbe. Feature-Liste als Flex-Column mit Checkmarks (CSS ::before).
- **Über-mich:** `display: grid; grid-template-columns: 300px 1fr; gap: 3rem;` — Mobile: `grid-template-columns: 1fr;`. Foto-Placeholder: `background: var(--color-bg-alt); aspect-ratio: 3/4; border-radius: var(--radius); display: flex; align-items: center; justify-content: center;` mit Initialen "IT" als Text.
- **Demo:** Zentriert, Placeholder-Box für Voiceflow (gestylt mit "Demo folgt" Label) + Placeholder für Loom.
- **Kontakt:** Zentriert, `max-width: 800px`, Calendly-Placeholder-Box + mailto-Fallback darunter.
- **Footer:** `padding: 3rem 0; border-top: 1px solid var(--color-border); text-align: center;`.

**Media Queries:** Alle Section-Layouts ab `max-width: 768px` auf Single-Column stacken.

**Akzeptanz:** CSS valide, jede Section hat eigene Styles.

---

## Task 7 — `index.html` Teil 1: Head + Nav + Hero

**Ziel:** Head mit Basics, Nav-Struktur, Hero-Section.

**Head:**
- `<!DOCTYPE html>`, `<html lang="de">`
- `<meta charset="UTF-8">`
- `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- Basic `<title>` — SEO-vollständig kommt in Task 16
- `<link rel="icon" type="image/svg+xml" href="favicon.svg">`
- `<link rel="preload" href="assets/fonts/inter-400.woff2" as="font" type="font/woff2" crossorigin>` (falls Fonts da, sonst weglassen)
- `<link rel="preload" href="assets/fonts/inter-600.woff2" as="font" type="font/woff2" crossorigin>` (ditto)
- `<link rel="stylesheet" href="assets/style.css">`
- `<script src="assets/script.js" defer></script>`

**Body-Start:**
- Skip-Link: `<a href="#main" class="skip-link">Zum Hauptinhalt springen</a>`

**Nav:**
```html
<nav id="main-nav">
  <div class="container nav-container">
    <a href="#" class="logo">Get<span class="accent">Ki</span>Agent</a>
    <button class="nav-toggle" aria-label="Menü öffnen" aria-expanded="false">...</button>
    <ul class="nav-links">
      <li><a href="#services">Services</a></li>
      <li><a href="#about">Über mich</a></li>
      <li><a href="#pricing">Preise</a></li>
      <li><a href="#demo">Demo</a></li>
      <li><a href="#kontakt">Kontakt</a></li>
    </ul>
    <a href="#kontakt" class="btn btn-primary nav-cta">Kostenloses Erstgespräch</a>
  </div>
</nav>
```

**Hero:**
```html
<main id="main">
  <section id="hero">
    <div class="container">
      <h1>Ich automatisiere den Kundenservice, der Sie täglich bremst.</h1>
      <p class="hero-subline">KI-Chatbots und Workflow-Automatisierung für E-Commerce & Einzelhandel im DACH-Raum. Gebaut von jemandem, der 4 Jahre lang selbst einen Filialbetrieb mit 50 Mitarbeitern geführt hat.</p>
      <div class="hero-ctas">
        <a href="#kontakt" class="btn btn-primary">Kostenloses KI-Audit buchen</a>
        <a href="#demo" class="btn btn-secondary">Live-Demo testen</a>
      </div>
    </div>
  </section>
```

**Akzeptanz:** HTML valide, `<main>` offen (wird in Task 8 geschlossen).

---

## Task 8 — `index.html` Teil 2: Problem + Services + Über-mich + Demo + Kontakt + Footer

**Ziel:** Alle verbleibenden Sektionen.

**Problem-Section:**
```html
<section id="problem" class="section">
  <div class="container">
    <h2>Die drei Zeitfresser im Kundenservice</h2>
    <div class="problem-grid">
      <div class="problem-card">
        <div class="problem-icon"></div>
        <h3>Immer dieselben Fragen</h3>
        <p>Ihr Support-Team beantwortet dieselben 20 Fragen — jeden Tag.</p>
      </div>
      <div class="problem-card">
        <div class="problem-icon"></div>
        <h3>Retouren & WISMO</h3>
        <p>Retouren und WISMO-Anfragen fressen Stunden.</p>
      </div>
      <div class="problem-card">
        <div class="problem-icon"></div>
        <h3>Keine Antwort am Abend</h3>
        <p>Kunden schreiben abends — niemand antwortet bis morgen.</p>
      </div>
    </div>
    <p class="problem-solution">Ich baue KI-Systeme, die diese Probleme in 2–4 Wochen lösen.</p>
  </div>
</section>
```

**Services-Section (id="services"):** 3 Cards (Starter, Professional mit `.featured`, Enterprise) mit:
- Titel + Positionierung
- Feature-Liste (ul mit Checkmarks)
- Zeitrahmen
- Support-Level
- **KEINE Preise, KEIN CTA-Button** (kommt in Task 14)

Exakte Content-Strings:
- **Starter:** "1 n8n-Workflow (z.B. automatische E-Mail-Sortierung oder FAQ-Bot)" / "1–2 Wochen Laufzeit" / "E-Mail-Support"
- **Professional:** "3–5 Workflows + KI-Chatbot oder Voice Agent" / "3–4 Wochen Laufzeit" / "Slack/Teams-Support" / "30-Tage-Monitoring inklusive"
- **Enterprise:** "Multi-Agent-System, Custom Integrations" / "Strategie-Workshop inklusive" / "6–12 Wochen Laufzeit" / "Dedicated Support"

**Preis-Anker:** Füge eine leere `<section id="pricing"></section>` ein **vor** Services oder kombiniere mit Services — Nav-Link "Preise" muss zu `#services` scrollen. Einfachste Lösung: Services-Section auch mit `id="pricing"` ausstatten → `<section id="services" class="section"><a id="pricing"></a>...`.

**Über-mich-Section (id="about"):**
```html
<section id="about" class="section">
  <div class="container about-grid">
    <div class="about-photo">
      <div class="photo-placeholder">IT</div>
    </div>
    <div class="about-text">
      <h2>Warum ich weiß, wo es hakt</h2>
      <p>Mein Name ist Ilias. Bevor ich KI-Automatisierung gemacht habe, habe ich 4 Jahre lang einen Filialbetrieb im Einzelhandel geleitet — 50 Mitarbeiter, siebenstelliger Jahresumsatz. Ich kenne die Prozesse, die Zeit fressen, weil ich sie selbst erlebt habe.</p>
      <p>Heute löse ich genau diese Probleme mit KI und Automatisierung. Kein Buzzword-Bingo. Keine generischen Lösungen. Jedes Projekt wird individuell auf Ihren Betrieb zugeschnitten.</p>
      <p class="credentials">B.A. BWL Handel (DHBW) | M.A. International Management</p>
    </div>
  </div>
</section>
```

**Demo-Section (id="demo"):**
```html
<section id="demo" class="section">
  <div class="container">
    <h2>Live-Demo: Lumi, der KI-Support-Agent</h2>
    <p>Testen Sie selbst: Das ist Lumi, unser KI-Support-Agent. Fragen Sie nach Bestellstatus, Retouren oder Produktinfos.</p>
    <div class="demo-placeholder">
      <p>Interaktiver Chat folgt in Kürze</p>
      <!-- Voiceflow Widget kommt in Phase 3 -->
    </div>
    <div class="demo-video-placeholder">
      <p>Demo-Video folgt in Kürze</p>
      <!-- Loom Embed kommt in Phase 3 -->
    </div>
  </div>
</section>
```

**Kontakt-Section (id="kontakt"):**
```html
<section id="kontakt" class="section">
  <div class="container">
    <h2>Kostenloses 30-Minuten-Erstgespräch</h2>
    <p>Buchen Sie ein kostenloses 30-Minuten-Erstgespräch. Ich analysiere Ihre Support-Prozesse und zeige Ihnen 3 konkrete Automatisierungspotenziale.</p>
    <div class="calendly-placeholder">
      <p>Terminbuchung folgt in Kürze</p>
      <!-- Calendly Inline-Widget kommt manuell -->
    </div>
    <p class="contact-fallback">Oder direkt per E-Mail: <a href="mailto:getkiagent@gmail.com">getkiagent@gmail.com</a></p>
  </div>
</section>
</main>
```

**Footer:**
```html
<footer>
  <div class="container">
    <p>&copy; 2026 GetKiAgent — Ilias Tebque</p>
    <ul class="footer-links">
      <li><a href="impressum.html">Impressum</a></li>
      <li><a href="datenschutz.html">Datenschutz</a></li>
    </ul>
  </div>
</footer>
</body>
</html>
```

**Akzeptanz:** HTML valide, alle Anchors matchen Nav-Links, keine unbalanced Tags.

---

## Task 9 — `script.js`

**Ziel:** Interaktivität — Nav-Scroll, Mobile-Menu, Smooth-Scroll.

**Inhalt:**
```javascript
// Nav scroll effect
const nav = document.getElementById('main-nav');
let ticking = false;
window.addEventListener('scroll', () => {
  if (!ticking) {
    requestAnimationFrame(() => {
      nav.classList.toggle('scrolled', window.scrollY > 50);
      ticking = false;
    });
    ticking = true;
  }
});

// Mobile menu toggle
const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');
navToggle?.addEventListener('click', () => {
  const isOpen = navLinks.classList.toggle('open');
  navToggle.setAttribute('aria-expanded', isOpen);
  navToggle.setAttribute('aria-label', isOpen ? 'Menü schließen' : 'Menü öffnen');
  document.body.classList.toggle('nav-open', isOpen);
});

// Close mobile menu on link click
document.querySelectorAll('.nav-links a').forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
    navToggle.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('nav-open');
  });
});
```

**Akzeptanz:** JS-File geschrieben, keine Syntax-Errors (quick-check mit `node -c` falls verfügbar).

---

## Task 10 — `impressum.html` + `datenschutz.html`

**Ziel:** Rechtliche Pflichtseiten mit echten Daten (soweit vorhanden).

### `impressum.html`

**Inhalt:**
```html
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Impressum — GetKiAgent</title>
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <nav id="main-nav" class="scrolled">
    <div class="container nav-container">
      <a href="index.html" class="logo">Get<span class="accent">Ki</span>Agent</a>
      <a href="index.html" class="btn btn-secondary">Zurück zur Startseite</a>
    </div>
  </nav>
  <main class="legal-page">
    <div class="container">
      <h1>Impressum</h1>
      <h2>Angaben gemäß § 5 TMG</h2>
      <p>
        Ilias Tebque<br>
        Eichelstraße 87<br>
        40599 Düsseldorf<br>
        Deutschland
      </p>
      <h2>Kontakt</h2>
      <p>E-Mail: <a href="mailto:getkiagent@gmail.com">getkiagent@gmail.com</a></p>
      <h2>Umsatzsteuer</h2>
      <p>Gemäß § 19 UStG wird keine Umsatzsteuer erhoben (Kleinunternehmerregelung).</p>
      <h2>Verantwortlich für den Inhalt nach § 55 Abs. 2 RStV</h2>
      <p>Ilias Tebque, Eichelstraße 87, 40599 Düsseldorf</p>
      <h2>Haftungsausschluss</h2>
      <p><!-- TODO: Volltext von e-recht24.de generieren und einfügen --></p>
      <p><em>Dieser Abschnitt wird in Kürze ergänzt.</em></p>
    </div>
  </main>
  <footer>
    <div class="container">
      <p>&copy; 2026 GetKiAgent — Ilias Tebque</p>
      <ul class="footer-links">
        <li><a href="impressum.html">Impressum</a></li>
        <li><a href="datenschutz.html">Datenschutz</a></li>
      </ul>
    </div>
  </footer>
</body>
</html>
```

### `datenschutz.html`

**Struktur identisch, aber Content:**
- `<h1>Datenschutzerklärung</h1>`
- Sektionen: "Verantwortliche Stelle" (Ilias-Daten), "Erhebung personenbezogener Daten" (Platzhalter), "Cookies" (nur technisch notwendig), "Eingebundene Dienste" (Calendly + später Voiceflow/Loom als Platzhalter), "Ihre Rechte" (DSGVO-Standard-Text als Platzhalter)
- Überall `<!-- TODO: Volltext von e-recht24.de/datenschutz-generator generieren und einfügen -->` Kommentare

**Akzeptanz:** Beide HTML-Files valide, echte Impressum-Daten von Ilias eingesetzt, Platzhalter klar markiert.

---

## Task 11 — `logo.svg` + `favicon.svg`

**Ziel:** Text-Logo als SVG + simplifizierte Favicon-Variante.

### `website/assets/logo.svg` (volles Logo für Nav — Fallback, primär wird CSS-Text verwendet)

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 40" role="img" aria-label="GetKiAgent">
  <text x="0" y="28" font-family="Inter, system-ui, sans-serif" font-weight="700" font-size="24" fill="#f8fafc">Get<tspan fill="#3b82f6">Ki</tspan>Agent</text>
</svg>
```

### `website/favicon.svg` (kompakter, nur "K" auf Akzent-BG)

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="12" fill="#0f172a"/>
  <text x="32" y="46" text-anchor="middle" font-family="Inter, system-ui, sans-serif" font-weight="700" font-size="40" fill="#3b82f6">K</text>
</svg>
```

**Akzeptanz:** Beide SVG-Files valide, öffnen im Browser ohne Errors.

---

## Task 12 — `robots.txt` + `sitemap.xml`

**Ziel:** SEO-Basics für Crawler.

### `website/robots.txt`
```
User-agent: *
Allow: /

Sitemap: https://getkiagent.de/sitemap.xml
```

### `website/sitemap.xml`
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://getkiagent.de/</loc>
    <lastmod>2026-04-11</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://getkiagent.de/impressum.html</loc>
    <lastmod>2026-04-11</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.3</priority>
  </url>
  <url>
    <loc>https://getkiagent.de/datenschutz.html</loc>
    <lastmod>2026-04-11</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.3</priority>
  </url>
</urlset>
```

**Akzeptanz:** Beide Files existieren, valider Inhalt.

---

## Task 13 — Playwright-QA Phase 1

**Ziel:** Visuelle + funktionale Verifikation der gesamten Phase 1.

**Schritte:**
1. Starte lokalen Server: `python -m http.server 8000 --directory website` (im Hintergrund mit `run_in_background: true`)
2. Playwright MCP `browser_navigate` zu `http://localhost:8000/`
3. Playwright MCP `browser_snapshot` (Accessibility-Tree, NICHT Screenshot — spart Tokens)
4. Playwright MCP `browser_console_messages` → prüfe auf Errors
5. Playwright MCP `browser_resize` → 375×800 (Mobile) → `browser_snapshot` → prüfe Mobile-Layout
6. Playwright MCP `browser_resize` → 768×1024 (Tablet) → `browser_snapshot`
7. Playwright MCP `browser_resize` → 1280×800 (Desktop) → `browser_snapshot`
8. Klicke alle Nav-Links → verifiziere Scroll-Verhalten (via snapshot nach Klick)
9. Teste Impressum-Link → navigate + snapshot → back
10. **Fix-Loop:** Alle gefundenen Issues sofort in HTML/CSS fixen. Iteriere bis sauber.
11. Server-Process killen am Ende

**Akzeptanz-Kriterien:**
- ✅ Keine Console-Errors
- ✅ Alle Sections sichtbar und im Accessibility-Tree
- ✅ Mobile: kein horizontaler Scroll
- ✅ Nav sticky funktioniert
- ✅ Anchor-Links funktional
- ✅ Impressum + Datenschutz öffnen

**Commit nach Task 13:** `git add website/ tasks/ && git commit -m "feat: Phase 1 — website structure, nav, sections, QA"`
(Falls kein .git existiert → Skip-Commit, Eintrag in blocked.md)

---

# ========== /clear HIER ==========
# Nach Task 13 → /clear → tasks/website-build.md neu lesen → weiter mit Task 14
# ==================================

---

# PHASE 2 — Preise + Polish + SEO + Cookie + Final QA

---

## Task 14 — Preise in Service-Cards einbauen

**Ziel:** Pricing in alle 3 Cards + CTA-Button hinzufügen.

**Änderungen in `index.html`:**

**Starter-Card:**
```html
<div class="price-block">
  <span class="price-amount">ab 2.900 €</span>
  <span class="price-label">Setup</span>
</div>
<div class="price-monthly">+ 190 € / Monat Betrieb</div>
<a href="#kontakt" class="btn btn-secondary card-cta">Erstgespräch buchen</a>
```

**Professional-Card:**
```html
<div class="card-badge">Empfohlen</div>
<!-- ...existing content... -->
<div class="price-block">
  <span class="price-amount">ab 7.500 €</span>
  <span class="price-label">Setup</span>
</div>
<div class="price-monthly">+ 390 € / Monat Betrieb</div>
<a href="#kontakt" class="btn btn-primary card-cta">Erstgespräch buchen</a>
```

**Enterprise-Card:**
```html
<div class="card-badge">Individuell</div>
<!-- ...existing content... -->
<div class="price-block">
  <span class="price-amount">ab 15.000 €</span>
  <span class="price-label">Setup</span>
</div>
<div class="price-monthly">ab 590 € / Monat Betrieb</div>
<a href="#kontakt" class="btn btn-secondary card-cta">Erstgespräch buchen</a>
```

**Änderungen in `style.css`:**
- `.price-block`, `.price-amount` (groß, `font-size: 2rem`, Accent-Farbe), `.price-label`
- `.price-monthly` (muted)
- `.card-badge` (absolute positioned, top-right corner, accent bg, small padding)
- `.card-cta` (full-width der Card)
- `.service-card.featured` — stärkere Border, `transform: scale(1.03)`

**Akzeptanz:** 3 Cards haben Preise, Badges, CTAs. Cards scrollen zu `#kontakt`.

---

## Task 15 — Trust-Bar nach Hero

**Ziel:** 4 Trust-Badges direkt unter Hero.

**HTML (vor `#problem` Section einfügen):**
```html
<section id="trust" class="trust-bar">
  <div class="container">
    <p class="trust-label">Gebaut mit:</p>
    <div class="trust-items">
      <span class="trust-item">n8n</span>
      <span class="trust-item">Anthropic Claude</span>
      <span class="trust-item">Voiceflow</span>
      <span class="trust-item">✓ DSGVO-konform</span>
    </div>
  </div>
</section>
```

**CSS:**
```css
.trust-bar { padding: 2rem 0; border-top: 1px solid var(--color-border); border-bottom: 1px solid var(--color-border); background: var(--color-bg-alt); }
.trust-label { text-align: center; color: var(--color-text-muted); font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1rem; }
.trust-items { display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; }
.trust-item { padding: 0.5rem 1rem; border: 1px solid var(--color-border); border-radius: 999px; color: var(--color-text); font-size: 0.9rem; font-weight: 500; }
```

**SVG-Logos optional:** Falls schnell auffindbar (n8n/Anthropic Brand-Pages), inline SVG statt Text. Sonst Text-Pills — sind völlig OK.

**Akzeptanz:** Trust-Bar erscheint zwischen Hero und Problem, responsive.

---

## Task 16 — Zahlen-Highlights + SEO Meta-Tags

**Ziel:** Stats in Über-mich + volle SEO in `<head>`.

### Stats-Highlights (in Über-mich-Section, vor dem Text):

```html
<div class="about-stats">
  <div class="stat">
    <span class="stat-number">4</span>
    <span class="stat-label">Jahre Filialleitung</span>
  </div>
  <div class="stat">
    <span class="stat-number">50+</span>
    <span class="stat-label">Mitarbeiter geführt</span>
  </div>
  <div class="stat">
    <span class="stat-number">7-stellig</span>
    <span class="stat-label">Jahresumsatz</span>
  </div>
</div>
```

**CSS:**
```css
.about-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; margin-bottom: 3rem; text-align: center; }
.stat-number { display: block; font-size: 3rem; font-weight: 700; color: var(--color-accent); line-height: 1; }
.stat-label { display: block; color: var(--color-text-muted); font-size: 0.9rem; margin-top: 0.5rem; }
@media (max-width: 640px) { .about-stats { grid-template-columns: 1fr; gap: 1.5rem; } }
```

### SEO Meta-Tags in `<head>` von `index.html`:

```html
<title>GetKiAgent — KI-Automatisierung für E-Commerce & Einzelhandel | DACH</title>
<meta name="description" content="KI-Chatbots und Workflow-Automatisierung für Shopify & WooCommerce. Setup ab 2.900 €. Gebaut von einem Ex-Filialleiter mit 4 Jahren operativer Erfahrung.">
<meta name="author" content="Ilias Tebque">
<link rel="canonical" href="https://getkiagent.de/">
<meta name="robots" content="index, follow">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://getkiagent.de/">
<meta property="og:title" content="GetKiAgent — KI-Automatisierung für E-Commerce & Einzelhandel">
<meta property="og:description" content="KI-Chatbots und Workflow-Automatisierung für Shopify & WooCommerce. Setup ab 2.900 €.">
<meta property="og:image" content="https://getkiagent.de/images/og-image.png">
<meta property="og:locale" content="de_DE">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="GetKiAgent — KI-Automatisierung für E-Commerce & Einzelhandel">
<meta name="twitter:description" content="KI-Chatbots und Workflow-Automatisierung für Shopify & WooCommerce.">
<meta name="twitter:image" content="https://getkiagent.de/images/og-image.png">
```

**Akzeptanz:** `<head>` vollständig, Stats sichtbar in Über-mich.

---

## Task 17 — Cookie-Banner

**Ziel:** DSGVO-konformer Hinweis (rein informativ, keine Consent-Logik).

**HTML (vor `</body>` einfügen):**
```html
<div id="cookie-banner" class="cookie-banner" hidden>
  <div class="cookie-content">
    <p>Diese Website verwendet ausschließlich technisch notwendige Cookies. Mehr Infos in der <a href="datenschutz.html">Datenschutzerklärung</a>.</p>
    <button id="cookie-accept" class="btn btn-primary">Verstanden</button>
  </div>
</div>
```

**CSS:**
```css
.cookie-banner { position: fixed; bottom: 0; left: 0; right: 0; z-index: 1000; background: var(--color-bg-alt); border-top: 1px solid var(--color-border); padding: 1rem var(--section-padding-x); }
.cookie-banner[hidden] { display: none; }
.cookie-content { max-width: var(--container-max); margin: 0 auto; display: flex; align-items: center; justify-content: space-between; gap: 1.5rem; }
.cookie-content p { color: var(--color-text); font-size: 0.9rem; margin: 0; }
.cookie-content a { color: var(--color-accent); text-decoration: underline; }
@media (max-width: 640px) { .cookie-content { flex-direction: column; text-align: center; } }
```

**JS (an `script.js` anhängen):**
```javascript
// Cookie banner
const cookieBanner = document.getElementById('cookie-banner');
const cookieAccept = document.getElementById('cookie-accept');
if (cookieBanner && !localStorage.getItem('cookieAccepted')) {
  cookieBanner.hidden = false;
}
cookieAccept?.addEventListener('click', () => {
  localStorage.setItem('cookieAccepted', 'true');
  cookieBanner.hidden = true;
});
```

**Akzeptanz:** Banner erscheint beim ersten Besuch, verschwindet nach Klick, bleibt weg bei Reload.

---

## Task 18 — Mobile-Audit + a11y + Micro-Interactions

**Ziel:** Finale Qualitäts-Pässe.

**Checks + Fixes:**

1. **Touch-Targets ≥ 44px:** Alle Buttons, Links in Nav, Cookie-Button. Via CSS: `min-height: 44px; min-width: 44px;` wo nötig.
2. **Horizontaler Overflow:** `body { overflow-x: hidden; }` + alle `img`/`svg`/Container mit `max-width: 100%`.
3. **ARIA:**
   - Nav: `role="navigation" aria-label="Hauptnavigation"`
   - Mobile-Toggle: `aria-expanded`, `aria-controls="nav-links"`
   - Main: `<main id="main">` mit Skip-Link-Target
4. **Card-Hover:** `.service-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-card-hover); }` + `transition: transform 0.3s ease, box-shadow 0.3s ease;`
5. **Button-Hover:** Farb-Transition auf allen `.btn`
6. **Focus-Visible:** Alle interaktiven Elemente haben sichtbares Focus-Outline (bereits in Task 4, hier verifizieren)
7. **Reduced-Motion:** Bereits in Task 4, hier verifizieren: alle Transforms/Transitions respektieren `prefers-reduced-motion`

**Akzeptanz:** Alle 7 Checks erfüllt.

---

## Task 19 — Playwright-QA Phase 2 (Final)

**Ziel:** Komplette Site nochmal durchtesten nach Phase 2.

**Schritte:**
1. Server starten (`python -m http.server 8000 --directory website` im Hintergrund)
2. Navigate → `http://localhost:8000/`
3. `browser_snapshot` Desktop (1280)
4. `browser_console_messages` → prüfen
5. Cookie-Banner sollte erscheinen
6. Klick auf "Verstanden" → Banner verschwindet (snapshot vorher/nachher)
7. Reload → Banner soll weg bleiben
8. Mobile (375): Nav-Hamburger → öffnen → Links sichtbar → Link klicken → Menu schließt → scroll passiert
9. Teste alle Service-Card CTAs → scrollen zu Kontakt
10. Navigate zu `/impressum.html` → Daten sichtbar
11. Navigate zu `/datenschutz.html` → Struktur sichtbar
12. Server killen

**Fix-Loop:** Alle Issues sofort fixen, iterieren bis clean.

**Akzeptanz-Kriterien:**
- ✅ Keine Console-Errors
- ✅ Cookie-Banner-Flow funktioniert
- ✅ Alle CTAs scrollen korrekt
- ✅ Mobile-Menu öffnet/schließt sauber
- ✅ Impressum zeigt echte Daten
- ✅ Keine horizontalen Overflows auf 375px

---

## Task 20 — Final Report schreiben

**Ziel:** Kompakter Report für Ilias am Morgen.

**Datei:** `tasks/website-build-report.md`

**Inhalt (max 150 Wörter):**
```markdown
# Website Build — Report

**Datum:** 2026-04-11 → 2026-04-12
**Status:** ✅ Phase 1 + Phase 2 abgeschlossen

## Was gebaut wurde
- Komplette Single-Page-Website in `website/`
- [X] Tasks erledigt, [Y] in blocked.md
- Responsive (Mobile/Tablet/Desktop), a11y-compliant, DSGVO-konform

## Was du manuell ergänzen musst
1. **Foto:** 600×800 JPG/PNG nach `website/images/ilias.jpg`, dann in `index.html` die `.photo-placeholder` durch `<img>` ersetzen
2. **Calendly-URL:** Sobald Event erstellt → in `#kontakt` Section einbauen (Placeholder ist markiert)
3. **Datenschutz-Volltext:** Generator auf e-recht24.de ausfüllen, Text in `datenschutz.html` einfügen (TODO-Kommentare markieren Stellen)
4. **Hosting:** Netlify/Cloudflare Pages → Base Directory `website/`
5. **DNS:** Namecheap → Nameserver auf Hosting-Provider umstellen

## Phase 3 (später)
- Voiceflow Project ID einsetzen
- Loom-Video einbetten
```

**Akzeptanz:** Report-File existiert, ausgefüllt mit echten Task-Counts.

---

# ========== Ende der Task-Liste ==========

## Zusammenfassung

| Phase | Tasks | Fokus |
|---|---|---|
| Phase 1 | 1–13 | Struktur, Design, Core-Content, QA |
| Phase 2 | 14–20 | Preise, Polish, SEO, Cookie, Final-QA, Report |

**Expected Output:** Vollständige Website in `/website/`, einsatzbereit nach 5 manuellen Ergänzungen durch Ilias.
