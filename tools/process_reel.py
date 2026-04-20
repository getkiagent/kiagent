#!/usr/bin/env python3
"""
Wrapper around summarize_reel.py.
1. Runs reel analysis via summarize_reel.py
2. One Sonnet call: generates summary + fact-check + relevance + insights
3. Appends to Obsidian wiki (daily file)
4. Prints terminal summary for the user (summary, relevance, insights)

Lessons.md is NOT touched here — it's reserved for real GetKiAgent work
errors, not third-party reel/post content.

Usage: python tools/process_reel.py <url>
"""

import sys
import os
import re
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = Path(r"C:\Users\ilias\obsidian-vault\projects\getkiagent\wiki\reels")
MODEL = "claude-sonnet-4-6"

MAX_URLS_TO_FETCH = 5
MAX_URL_CONTENT_CHARS = 2500
URL_FETCH_TIMEOUT = 10
META_MIN_POSTS = 3
META_MIN_AGE_HOURS = 72  # auto-run synthesis at most every 3 days; --synthesize overrides

URL_PATTERN = re.compile(r'https?://[^\s<>"\'\]\)]+')

ANALYSIS_PROMPT = """\
Du analysierst einen Reel/Post für Ilias (Solo-Founder von GetKiAgent — DACH KI-Kundenservice-Automatisierung für E-Commerce, pre-revenue, Wave 2 Outreach läuft, AI-tool-fluent aber kein klassischer Entwickler).

Reel-Analyse:
{analysis}

Das Feld `linked_content_excerpts` enthält (falls vorhanden) Auszüge aus bis zu 3 im Post verlinkten Ressourcen — GitHub-READMEs, Artikel, Produkt-Seiten. Nutze diese Auszüge als primäre Quelle für ZUSAMMENFASSUNG und FAKTENCHECK: sie sind belastbarer als der Post-Text selbst. Wenn Auszüge leer sind oder Fetch fehlschlug, halte dich an den Post-Text und markiere Claims als [UNVERIFIED].

Aufgabe — liefere EXAKT diese sechs Blöcke in dieser Reihenfolge, jeweils mit dem Block-Namen als eigener Zeile in GROSSBUCHSTABEN gefolgt von einem Doppelpunkt:

ZUSAMMENFASSUNG:
2-4 Sätze auf Deutsch: Was behauptet/zeigt/empfiehlt der Post konkret? Welche Tools, Techniken oder Zahlen werden genannt? Keine Meta-Bewertung, nur der Inhalt.

ITEMS:
Enthält der Post eine Liste/Sammlung aus ≥3 eigenständigen Elementen (Guides, Tools, Tipps, Techniken, Ressourcen, Hacks, Frameworks)?
- Ja → Bullet pro Element, Format: "- <Name/Titel>: HOCH|MITTEL|NIEDRIG|KEINE — <1-Satz Begründung mit GetKiAgent-Bezug>". Nutze die `linked_content_excerpts` um die Inhalte der einzelnen Elemente zu erschliessen, nicht nur den Post-Text. Wenn ein Element nur als Label existiert und Excerpt fehlt, markiere mit [UNVERIFIED].
- Nein → schreibe: "kein Listen-Post"

FAKTENCHECK:
Enthält der Post konkrete Product-/Feature-/Metrik-Claims (z.B. "95% weniger Tokens", "Feature X macht Y")?
- Ja → Bullet-Liste pro Claim mit [UNVERIFIED]-Flag, Bedingungen (intrinsisch vs. spezifische Config) und Primärquelle zum Verifizieren.
- Nein → schreibe: "keine verifizierungspflichtigen Claims"

RELEVANZ:
Erste Zeile: HOCH | MITTEL | NIEDRIG | KEINE
Danach 2-3 Sätze Begründung: Wie bezieht sich das auf Ilias' aktuelle Situation (pre-revenue, Wave 2 Outreach, DACH E-Commerce-Fokus, Token-Kostensensitiv, Solo-Operator)? Wenn KEINE: warum nicht.
Bei Listen-Posts: Gesamt-Relevanz = höchste Einzel-Relevanz aus ITEMS. Begründung nennt die Top-1 oder Top-2 HOCH/MITTEL-Items namentlich.
HOCH = diese Woche umsetzbar oder direkt Outreach-/Pipeline-relevant.
MITTEL = relevant, aber Trigger fehlt (später Wave / erster Kunde / spezifische Bedingung).
NIEDRIG = Inspiration, nicht handlungsrelevant.
KEINE = kein Bezug.

INSIGHTS:
2-3 Bullet Points auf Deutsch (max 80 Wörter insgesamt): Konkrete Take-aways. Bei Listen-Posts beziehe dich nur auf HOCH/MITTEL-Items, nicht auf den Gesamt-Post. Bei unverifizierten Claims mit "Laut Post [UNVERIFIED]: ..." formulieren.
Falls RELEVANZ = KEINE: schreibe nur "Kein direkter Bezug."

UMSETZUNG:
Nur falls RELEVANZ = HOCH oder MITTEL. Maximal 3 konkrete Handlungen, die Ilias JETZT oder bei passendem Trigger ausführen kann. Bei Listen-Posts: eine Handlung pro HOCH/MITTEL-Item. Jede Zeile: "- [Aktion, Item-Name] — [Aufwand in Min/Std] — [Trigger falls MITTEL]".
Falls RELEVANZ = NIEDRIG oder KEINE: schreibe nur "keine Umsetzung empfohlen".

Ausgabe exakt in diesem Format — keine Einleitung, keine Trennlinien zwischen Blöcken, kein Text ausserhalb der Blöcke."""


SYNTHESIS_PROMPT = """\
Du bekommst den gesamten Tagesinhalt von wiki/reels/{date}.md — mehrere Reel-/Post-Analysen mit Faktencheck und Insights für GetKiAgent (DACH KI-Kundenservice-Automatisierung für E-Commerce).

Aggregiere eine Meta-Analyse mit genau diesen drei Sektionen:

# Immediate Actions
Konkrete Schritte, die GetKiAgent diese Woche umsetzen sollte. Pro Aktion:
- **Was konkret tun** (Befehl, Änderung, Setup)
- **Herkunft:** Post-Titel oder Account
- **Aufwand:** Minuten/Stunden grob
- **Warum jetzt:** in einem Satz

# Future Ideas
Ideen die noch nicht relevant sind (Wave 3+, €3k MRR, DACHGuard, Shopify-App, Inbound-Pivot). Pro Idee:
- **Was**
- **Trigger-Bedingung** (wann aktivieren)
- **Warum jetzt nicht**

# Skip-Liste
Was wir bewusst nicht übernehmen, mit 1-Satz-Begründung.

Tagesinhalt:
{daily_content}

Regeln:
- Nur verifizierte oder gesicherte Actions in „Immediate Actions" — [UNVERIFIED]-Claims gehören in „Future Ideas" bis geprüft.
- Deutsch, Markdown.
- Keine Einleitung, keine Zusammenfassung am Ende, nur die drei Sektionen."""


def extract_urls(text: str) -> list[str]:
    if not text:
        return []
    seen = set()
    urls = []
    for raw in URL_PATTERN.findall(text):
        url = raw.rstrip('.,);:!?')
        if url in seen:
            continue
        seen.add(url)
        urls.append(url)
    return urls


def fetch_url_content(url: str) -> str:
    """Fetch URL content. GitHub repos: try raw README.md on main/master. Generic: strip HTML."""
    try:
        parsed = urlparse(url)
        if parsed.netloc.lower() in ("github.com", "www.github.com"):
            parts = parsed.path.strip('/').split('/')
            if len(parts) >= 2:
                owner, repo = parts[0], parts[1].replace('.git', '')
                for branch in ('main', 'master'):
                    for fname in ('README.md', 'readme.md', 'Readme.md'):
                        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{fname}"
                        try:
                            req = Request(raw_url, headers={'User-Agent': 'Mozilla/5.0'})
                            with urlopen(req, timeout=URL_FETCH_TIMEOUT) as resp:
                                if resp.status == 200:
                                    body = resp.read().decode('utf-8', errors='ignore')
                                    return f"[GitHub README {owner}/{repo}]\n{body[:MAX_URL_CONTENT_CHARS]}"
                        except (URLError, HTTPError, TimeoutError):
                            continue
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=URL_FETCH_TIMEOUT) as resp:
            body = resp.read().decode('utf-8', errors='ignore')
        stripped = re.sub(r'<script[^>]*>.*?</script>', ' ', body, flags=re.DOTALL | re.IGNORECASE)
        stripped = re.sub(r'<style[^>]*>.*?</style>', ' ', stripped, flags=re.DOTALL | re.IGNORECASE)
        stripped = re.sub(r'<[^>]+>', ' ', stripped)
        stripped = re.sub(r'\s+', ' ', stripped).strip()
        return stripped[:MAX_URL_CONTENT_CHARS]
    except Exception as e:
        return f"[fetch failed: {type(e).__name__}: {e}]"


def enrich_with_links(data: dict) -> str:
    candidates: list[str] = []
    text = data.get("text") or ""
    candidates.extend(extract_urls(text))
    for page in data.get("linked_pages", []) or []:
        u = page.get("url")
        if u and u not in candidates:
            candidates.append(u)
    own_url = data.get("url", "")
    candidates = [u for u in candidates if u and u != own_url and not u.startswith("https://t.co/")]
    candidates = candidates[:MAX_URLS_TO_FETCH]
    if not candidates:
        return ""
    blocks = []
    for url in candidates:
        print(f"  fetching link: {url}", flush=True)
        content = fetch_url_content(url)
        blocks.append(f"URL: {url}\n{content}")
    return "\n\n---\n\n".join(blocks)


def run_summarize(url: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "summarize_reel.py"), url],
        capture_output=True, text=True, encoding="utf-8",
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    # Skip any warnings/output before the JSON object
    stdout = result.stdout
    json_start = stdout.find('\n{')
    if json_start >= 0:
        return json.loads(stdout[json_start + 1:])
    return json.loads(stdout.strip())


SECTION_NAMES = ("ZUSAMMENFASSUNG", "ITEMS", "FAKTENCHECK", "RELEVANZ", "INSIGHTS", "UMSETZUNG")
SECTION_PATTERN = re.compile(
    r'^\s*(' + '|'.join(SECTION_NAMES) + r')\s*:\s*',
    re.MULTILINE,
)


def parse_sections(raw: str) -> dict:
    """Split Sonnet response into named sections. Robust to missing/misordered blocks."""
    sections = {name: "" for name in SECTION_NAMES}
    matches = list(SECTION_PATTERN.finditer(raw))
    if not matches:
        return sections
    for i, m in enumerate(matches):
        name = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(raw)
        sections[name] = raw[start:end].strip().strip("-").strip()
    return sections


def call_sonnet(data: dict) -> dict:
    from dotenv import load_dotenv
    import anthropic

    load_dotenv(ROOT / ".env")
    client = anthropic.Anthropic()

    linked_content = enrich_with_links(data)

    analysis = json.dumps({
        "title": data.get("title"),
        "uploader": data.get("uploader"),
        "text": (data.get("text") or "")[:3000],
        "linked_pages": [
            {"title": p.get("title"), "url": p.get("url")}
            for p in data.get("linked_pages", [])[:3]
        ],
        "linked_content_excerpts": linked_content[:8000] if linked_content else "",
    }, ensure_ascii=False)

    response = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        messages=[{
            "role": "user",
            "content": ANALYSIS_PROMPT.format(
                analysis=analysis,
                date=datetime.now().strftime("%Y-%m-%d"),
            ),
        }],
    )

    raw = response.content[0].text.strip()
    sec = parse_sections(raw)

    umsetzung_raw = sec["UMSETZUNG"].strip()
    umsetzung = "" if umsetzung_raw.lower().startswith("keine umsetzung") else umsetzung_raw

    items_raw = sec["ITEMS"].strip()
    items = "" if items_raw.lower().startswith("kein listen-post") else items_raw

    return {
        "summary": sec["ZUSAMMENFASSUNG"] or "(keine Zusammenfassung)",
        "items": items,
        "fact_check": sec["FAKTENCHECK"],
        "relevance": sec["RELEVANZ"],
        "insights": sec["INSIGHTS"] or raw if not any(sec.values()) else sec["INSIGHTS"],
        "umsetzung": umsetzung,
    }


def save_wiki(data: dict, analysis: dict) -> Path:
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    wiki_file = WIKI_DIR / f"{today}.md"

    header = f"# Reels {today}\n\n" if not wiki_file.exists() else ""
    account = data.get("uploader") or data.get("uploader_id") or "Unknown"
    url = data.get("url", "")
    title = (data.get("title") or url)[:80]
    raw_text = (data.get("text") or "").strip()[:1200] or "(kein Text)"

    relevance_raw = analysis.get("relevance", "").strip()
    relevance_tag = relevance_raw.split("\n", 1)[0].strip() if relevance_raw else "UNBEKANNT"

    fact_block = f"### Faktencheck\n{analysis['fact_check']}\n\n" if analysis.get("fact_check") else ""
    relevance_block = f"### Relevanz: {relevance_tag}\n{relevance_raw}\n\n" if relevance_raw else ""
    items_block = f"### Einzel-Relevanz pro Element\n{analysis['items']}\n\n" if analysis.get("items") else ""
    umsetzung_block = f"### Umsetzung\n{analysis['umsetzung']}\n\n" if analysis.get("umsetzung") else ""

    entry = (
        f"\n## [{account}]({url}) — {title}\n\n"
        f"**Analysiert:** {datetime.now().strftime('%H:%M')}\n\n"
        f"### Zusammenfassung\n{analysis.get('summary', '').strip()}\n\n"
        f"{items_block}"
        f"{relevance_block}"
        f"{fact_block}"
        f"### Insights für GetKiAgent\n{analysis.get('insights', '').strip()}\n\n"
        f"{umsetzung_block}"
        f"<details><summary>Original-Post</summary>\n\n{raw_text}\n\n</details>\n\n"
        f"---\n"
    )

    with open(wiki_file, "a", encoding="utf-8") as f:
        f.write(header + entry)

    return wiki_file


def count_daily_posts(date_str: str) -> int:
    daily_file = WIKI_DIR / f"{date_str}.md"
    if not daily_file.exists():
        return 0
    content = daily_file.read_text(encoding="utf-8")
    return len(re.findall(r'^## \[', content, re.MULTILINE))


def extract_post_id_from_url(url: str) -> str | None:
    """Extract stable post ID for dedupe. Handles X, Instagram, YouTube."""
    try:
        parts = [p for p in urlparse(url).path.split('/') if p]
    except Exception:
        return None
    if not parts:
        return None
    if "status" in parts:
        i = parts.index("status")
        if i + 1 < len(parts):
            return parts[i + 1].split("?")[0]
    for key in ("reel", "p", "tv"):
        if key in parts:
            i = parts.index(key)
            if i + 1 < len(parts):
                return parts[i + 1]
    return parts[-1].split("?")[0]


def existing_analysis_today(post_id: str) -> Path | None:
    """Return today's analysis JSON for post_id if it exists, else None."""
    today = datetime.now().strftime("%Y%m%d")
    hits = sorted((ROOT / "reels").glob(f"{today}_*_{post_id}.json"))
    return hits[-1] if hits else None


def synthesis_is_fresh() -> bool:
    """True if latest synthesis file is younger than META_MIN_AGE_HOURS."""
    synth_files = list(WIKI_DIR.glob("*-synthesis.md"))
    if not synth_files:
        return False
    latest = max(synth_files, key=lambda p: p.stat().st_mtime)
    return (time.time() - latest.stat().st_mtime) / 3600 < META_MIN_AGE_HOURS


def synthesize_day(date_str: str | None = None) -> Path | None:
    """Aggregate all posts from a given date into a meta-analysis file."""
    from dotenv import load_dotenv
    import anthropic

    load_dotenv(ROOT / ".env")
    client = anthropic.Anthropic()

    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    daily_file = WIKI_DIR / f"{date_str}.md"
    if not daily_file.exists():
        print(f"— Keine Daily-Datei für {date_str}", flush=True)
        return None

    content = daily_file.read_text(encoding="utf-8")
    post_count = len(re.findall(r'^## \[', content, re.MULTILINE))

    if post_count < META_MIN_POSTS:
        print(f"— Nur {post_count} Posts, Meta-Analyse erst ab {META_MIN_POSTS}", flush=True)
        return None

    response = client.messages.create(
        model=MODEL,
        max_tokens=3000,
        messages=[{
            "role": "user",
            "content": SYNTHESIS_PROMPT.format(
                date=date_str,
                daily_content=content[:40000],
            ),
        }],
    )

    synthesis_text = response.content[0].text.strip()

    synthesis_file = WIKI_DIR / f"{date_str}-synthesis.md"
    header = (
        f"# Meta-Analyse {date_str}\n\n"
        f"Aggregation aus {post_count} Posts (siehe [[{date_str}]]). "
        f"Generiert: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        f"---\n\n"
    )
    synthesis_file.write_text(header + synthesis_text + "\n", encoding="utf-8")
    return synthesis_file


def print_usage():
    print(
        "Usage:\n"
        "  python tools/process_reel.py <url>               Process a single post\n"
        "  python tools/process_reel.py --synthesize        Meta-analyze today's posts\n"
        "  python tools/process_reel.py --synthesize DATE   Meta-analyze DATE (YYYY-MM-DD)",
        file=sys.stderr,
    )


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    arg = sys.argv[1].strip()

    if arg == "--synthesize":
        date_str = sys.argv[2].strip() if len(sys.argv) > 2 else None
        try:
            synth_file = synthesize_day(date_str)
        except Exception as e:
            print(f"ERROR synthesis: {e}", file=sys.stderr)
            sys.exit(1)
        if synth_file:
            print(f"\n✓ Synthese: {synth_file}", flush=True)
        return

    url = arg
    print(f"Analysiere: {url}", flush=True)

    post_id = extract_post_id_from_url(url)
    if post_id:
        existing = existing_analysis_today(post_id)
        if existing:
            print(f"— Duplikat: heute bereits analysiert ({existing.name}). Skip.", flush=True)
            return

    try:
        data = run_summarize(url)
    except Exception as e:
        print(f"ERROR summarize: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        analysis = call_sonnet(data)
    except Exception as e:
        print(f"ERROR sonnet: {e}", file=sys.stderr)
        sys.exit(1)

    wiki_file = save_wiki(data, analysis)
    print_chat_summary(data, analysis, wiki_file)

    today = datetime.now().strftime("%Y-%m-%d")
    if count_daily_posts(today) >= META_MIN_POSTS:
        if synthesis_is_fresh():
            print(f"— Meta-Analyse übersprungen: letzte Synthese < {META_MIN_AGE_HOURS}h alt (manuell via --synthesize erzwingbar)", flush=True)
        else:
            try:
                synth_file = synthesize_day(today)
                if synth_file:
                    print(f"\n✓ Meta-Analyse aktualisiert: {synth_file}", flush=True)
            except Exception as e:
                print(f"— Meta-Analyse übersprungen: {e}", flush=True)


def print_chat_summary(data: dict, analysis: dict, wiki_file: Path):
    """Print a structured summary to the terminal for the user."""
    account = data.get("uploader") or data.get("uploader_id") or "Unknown"
    url = data.get("url", "")
    rel_raw = (analysis.get("relevance") or "").strip()
    rel_tag = rel_raw.split("\n", 1)[0].strip() or "?"

    print("\n" + "=" * 72, flush=True)
    print(f"POST: {account} — {url}", flush=True)
    print("=" * 72, flush=True)

    print(f"\nZusammenfassung:\n{analysis.get('summary', '').strip()}", flush=True)

    items = (analysis.get("items") or "").strip()
    if items:
        print(f"\nEinzel-Relevanz pro Element:\n{items}", flush=True)

    print(f"\nRelevanz: {rel_tag}", flush=True)
    rel_body = rel_raw.split("\n", 1)[1].strip() if "\n" in rel_raw else ""
    if rel_body:
        print(rel_body, flush=True)

    fact = (analysis.get("fact_check") or "").strip()
    if fact and fact.lower() != "keine verifizierungspflichtigen claims":
        print(f"\nFaktencheck:\n{fact}", flush=True)

    insights = (analysis.get("insights") or "").strip()
    if insights:
        print(f"\nInsights:\n{insights}", flush=True)

    umsetzung = (analysis.get("umsetzung") or "").strip()
    if umsetzung:
        print(f"\nUmsetzung jetzt:\n{umsetzung}", flush=True)

    print(f"\n✓ Wiki: {wiki_file}", flush=True)


if __name__ == "__main__":
    main()
