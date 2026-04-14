# Website-v2 Redesign — Autonomous Execution Plan

**Status:** Ready to execute. Trigger: user says "Führe tasks/website-redesign-plan.md aus" OR scheduled run.
**Mode:** AUTONOM — no confirmations during run. Drafts only, no email send, no deploy without user confirm.

---

## Context

- **Project:** GetKiAgent — AI customer-support automation for DACH e-commerce
- **Pain:** Website v2 exists but converts no outreach leads. No customers yet. Biggest blocker.
- **Target audience:** Tier-A DACH e-commerce Founders receiving cold outreach. Skeptical + curious mix.
- **Primary goal:** Contact-Click from outreach-landing-visitor. Single metric.
- **Sub-goal:** Convey seriousness, expertise, authenticity in <10 seconds.

## Current State (website-v2/)

- **Stack:** React 19.2 + Vite 8 + Tailwind 4 + lucide-react
- **Structure:** One-Pager, 8 components in `src/components/`:
  - Nav, Hero, Features, HowItWorks, Pricing, Testimonials, CTA, Footer
- **LOC:** ~1.118 total
- **Domain:** getkiagent.de (not yet deployed anywhere)
- **QA baseline:** `qa-desktop.png` + `qa-mobile.png` exist in project root

## User Answers (Fragebogen)

| # | Question | Answer |
|---|---|---|
| 1 | Current folder | `website-v2/` |
| 4 | Biggest pain | Setup exists, zero customers |
| 5 | Primary goal | (a) Conversion: Outreach → Contact |
| 6 | 10-sec impression | Seriös, erfahren, authentisch, kompetent |
| 7 | Desired action | Kontakt aufnehmen, Seriosität wahrnehmen |
| 8 | Audience | Outreach Tier-A DACH |
| 9 | Decision-maker | Founder |
| 10 | Knowledge level | Mixed skeptisch + interessiert |
| 11 | Assets | Loom video, workflow screenshots |
| 12 | Pricing visible | **NO** |
| 13 | Pages | One-Pager only |
| 14 | Reference sites | digirelation.com/n8n-agentur, peter-krause.net, ki-agentur.com, deinekiagentur.com |
| 15 | Tone | Seriös-corporate |
| 16 | Brand colors | Open for new |
| 17 | Deadline | None, overnight work |
| 18 | Time budget | Unlimited |
| 19 | Constraints | None |

## Locked Decisions

- **Host:** Vercel (prepare config, do NOT deploy without user confirm)
- **Contact mechanic:** Cal.com embed → `https://cal.com/getkiagent`
- **Loom video:** `https://www.loom.com/share/a243a6f8c920487a9db15e9c9816c36e`
- **Legal:** Placeholder pages (Impressum/Datenschutz) with clear TODO markers
- **Top reference:** `ki-agentur.com` (leading stylistic direction)
- **REMOVE:** Testimonials.jsx (no customers → fake social proof = credibility killer), Pricing.jsx (user explicit)
- **ADD:** Cal.com embed, Loom hero-video (lazy-loaded), workflow screenshots section, legal placeholders

---

## Execution Phases

### Phase A — Research & Foundation (≈30 min)

1. Take Playwright screenshots of current `website-v2` dev build (desktop + mobile) → save to `tasks/redesign-before-desktop.png`, `tasks/redesign-before-mobile.png`
2. Firecrawl scrape all 4 reference sites:
   - `https://www.digirelation.com/n8n-agentur/`
   - `https://peter-krause.net/`
   - `https://ki-agentur.com/` ← primary
   - `https://deinekiagentur.com/`
   Save markdown to `.firecrawl/refs-*.md`
3. Analyze patterns: Hero style, font pairings, color palettes, section order, CTA placement, credibility signals used when there are no testimonials
4. Invoke `ui-ux-pro-max` skill → derive:
   - Color palette (primary, neutral, accent) fitting "seriös-corporate DACH B2B"
   - Font pairing (display + body) via Google Fonts
   - Spacing system
5. Write `tasks/redesign-design-brief.md`:
   - Hero headline (DE, <12 words)
   - Hero subheadline (1-2 sentences)
   - Section order + copy for each
   - Primary + secondary CTA text
   - Credibility elements (NO fake testimonials — use tech stack logos, "built with", self-authored proof)

### Phase B — Rebuild One-Pager (≈2-3h)

**DELETE** `Pricing.jsx` + `Testimonials.jsx`. Remove their imports from `App.jsx`.

**REBUILD each component** to match the design brief:

6. `Nav.jsx` — minimal: logo-left + single "Kontakt" CTA-right. Sticky, shrink on scroll.
7. `Hero.jsx` — Headline + subline + primary CTA (→ scroll to Cal) + secondary CTA (→ scroll to Loom). Loom embed lazy-loaded below fold or as section.
8. `HowItWorks.jsx` — 3-4 concrete steps with workflow-screenshot thumbnails. Focus on outputs not features.
9. `Features.jsx` → **rename conceptually to "Was du bekommst"**. Concrete deliverables (z.B. "n8n-Workflow auf deinem Stack", "Gmail-Draft-Automation", "DSGVO-konform"). No buzzwords.
10. **NEW component `Credibility.jsx`** — replaces Testimonials slot. Contains:
    - "Entwickelt mit" tech stack row (n8n, Claude, Gmail, Playwright logos/icons)
    - 1 self-authored statement: *"Ich baue seit [X] AI-Support-Workflows. Kein Template, kein Baukasten — jeder Agent wird für deinen Shop gebaut. Hier ist eine Live-Demo:"* + Loom-link
    - Optional: workflow-screenshot as visual proof
11. **NEW component `Contact.jsx`** — Cal.com iframe embed (`cal.com/getkiagent`) with fallback `mailto:` below.
12. `Footer.jsx` — minimal: copyright, Impressum-link, Datenschutz-link, contact-email
13. Create `src/pages/impressum.html` + `src/pages/datenschutz.html` — **placeholder content** with giant `TODO: Ilias muss das ausfüllen` comment at top. Include bare-minimum structure so legal links don't 404.

### Phase C — Polish & Build (≈1h)

14. Mobile pass: test every component at 375px, 768px, 1280px (Playwright viewports)
15. Accessibility basics: alt tags on all imgs, aria-labels on icon-only buttons, contrast check, skip-link keep
16. Meta tags in `index.html`:
    - `<title>GetKiAgent — AI-Support-Automation für DACH E-Commerce</title>`
    - Description, OG-Image (generate or use Loom thumbnail), Twitter-card
    - favicon (already exists in `public/`)
17. `npm run build` — must succeed without warnings
18. Playwright screenshots of NEW build → save `tasks/redesign-after-desktop.png`, `tasks/redesign-after-mobile.png`
19. Prepare Vercel config: `vercel.json` if needed, verify `dist/` output works
20. **DO NOT deploy** — leave deploy command in run report for user to trigger manually

### Phase D — Builder-Validator (≈15 min)

21. Spawn subagent (`Explore` or general) as **Validator** with prompt:
    > Re-read `tasks/website-redesign-plan.md` (primary goal, decisions). Open `tasks/redesign-after-desktop.png` and `-mobile.png`. Assess: "Would a skeptical Tier-A DACH e-commerce Founder perceive this as serious, experienced, authentic?" Check: (a) no fake testimonials remain, (b) no pricing visible, (c) Cal.com embed functional, (d) Loom accessible, (e) mobile layout not broken, (f) legal links present, (g) DE copy grammatically correct, no Denglisch. Return PASS / WARN (with reason) / FAIL (with fix) per check.
22. If any FAIL → fix → re-run validator
23. Only mark phase complete when all PASS or WARN-with-justification

### Phase E — Run Report

24. Write `tasks/website-redesign-run-YYYY-MM-DD.md`:
    - What was built (component-by-component diff summary)
    - Screenshots before/after
    - Validator results
    - Deploy instruction: exact command for user to trigger (`cd website-v2 && vercel --prod`)
    - Remaining TODOs (Impressum-content, Datenschutz-content, Cal.com link verification, OG-image final)
    - Any warnings/blockers hit during run
25. Append errors (if any) to `tasks/lessons.md` per CLAUDE.md rules
26. Send notification: `~/.local/bin/notify-claude.sh done "Website-Redesign fertig, Build + Report liegen in tasks/"`

---

## Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Fake testimonials leak into build | Hard-delete `Testimonials.jsx`, grep for imports |
| React 19 + Vite 8 + TW 4 bugs | Run `npm run build` after every component change |
| Legal links 404 → abmahnrisiko | Always create placeholder pages, never skip |
| Cal.com embed blocked by CSP | Test in dev, add iframe src to meta if needed |
| Loom embed hurts Lighthouse score | Lazy-load with thumbnail poster |
| Copy-pattern from references too obvious | Take 1 element from each, never clone 1 site |
| User doesn't like the result in the morning | Keep old components in `website-v2/src/_archive/` for quick rollback |

---

## Out of Scope

- Blog, case studies, multi-page
- Pricing visible
- Backend/form API
- A/B testing
- Multi-language (DE-only)
- Actual deploy to Vercel (prepare config, user triggers)
- Writing real Impressum/Datenschutz content
- Deleting `website/` (separate cleanup)

---

## Trigger Command

```
Führe tasks/website-redesign-plan.md aus. AUTONOM.
```
