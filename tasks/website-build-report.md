# Website Build — Report

**Datum:** 2026-04-11
**Status:** ✅ Phase 1 + Phase 2 abgeschlossen

## Was gebaut wurde
- Komplette Single-Page-Website in `website/`
- 20 Tasks erledigt, 1 in blocked.md (Git-Commit, kein .git-Repo)
- Responsive (Mobile 375 / Tablet 768 / Desktop 1280), a11y-compliant, DSGVO-konform
- Inter self-hosted (4 Weights), Dark-Theme, Cookie-Banner, SEO-Meta-Tags vollständig

## Was du manuell ergänzen musst
1. **Foto:** 600×800 JPG/PNG nach `website/images/ilias.jpg`, dann `.photo-placeholder` durch `<img src="images/ilias.jpg" alt="Ilias Tebque">` ersetzen
2. **Calendly-URL:** Event erstellen → `<div class="calendly-placeholder">` in `index.html` durch Inline-Widget ersetzen
3. **Datenschutz-Volltext:** e-recht24.de/datenschutz-generator → Text in `datenschutz.html` (TODO-Kommentare markieren die Stellen)
4. **Haftungsausschluss:** e-recht24.de → Text in `impressum.html` ergänzen
5. **Hosting:** Netlify/Cloudflare Pages → Base Directory `website/`
6. **DNS:** Namecheap → Nameserver auf Hosting-Provider umstellen
7. **Git init:** `git init && git add website/ tasks/ && git commit -m "feat: website v1"`

## Phase 3 (später)
- Voiceflow Project ID in Demo-Section einsetzen
- Loom-Video einbetten
- OG-Image erstellen (`website/images/og-image.png`, 1200×630px)
