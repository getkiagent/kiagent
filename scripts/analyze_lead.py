"""
GetKiAgent — Single-URL Lead Analyzer v1

Usage:
    python scripts/analyze_lead.py <url>

Requires .env with:
    ANTHROPIC_API_KEY=...

Optional (legacy fallback):
    FIRECRAWL_API_KEY=...

Scraping stack: Jina AI Reader (primary, free) → crawl4ai (fallback, JS support)
Install crawl4ai once: pip install crawl4ai && crawl4ai-setup
"""

import sys
import json
import os
import re
import asyncio
import requests as _requests
from pathlib import Path
from utils import normalize_url


class FirecrawlError(Exception):
    pass


class FirecrawlTimeoutError(FirecrawlError):
    pass


class ClaudeParseError(Exception):
    pass

# Windows-Konsole auf UTF-8 setzen damit Umlaute/Sonderzeichen nicht crashen
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Environment ──────────────────────────────────────────────────────────────

def load_and_validate_env():
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("ERROR: python-dotenv not installed. Run: pip install python-dotenv")
        sys.exit(1)

    load_dotenv()

    firecrawl_key = os.getenv("FIRECRAWL_API_KEY", "").strip()  # optional — legacy
    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "").strip()

    if not anthropic_key:
        print("ERROR: ANTHROPIC_API_KEY fehlt in .env")
        print("Create a .env file in the project root with ANTHROPIC_API_KEY set.")
        sys.exit(1)

    return firecrawl_key, anthropic_key


# ── Scraping ─────────────────────────────────────────────────────────────────

MAX_SUBPAGES = 4           # max. Unterseiten zusätzlich zur Homepage
MAX_CHARS_HOMEPAGE = 8000
MAX_CHARS_SUBPAGE = 5000
MIN_CONTENT_LENGTH = 300

# Keyword → Prioritätsscore für URL-Auswahl aus der Sitemap (DE + EN)
URL_PRIORITY = {
    "kontakt": 10, "contact": 10,
    "faq": 9, "hilfe": 9, "help": 9,
    "widerruf": 8, "retoure": 8, "rueckgabe": 8, "rückgabe": 8,
    "returns": 8, "refund": 8,
    "versand": 7, "lieferung": 7, "shipping": 7,
    "policies": 6,
    "uber-uns": 5, "ueber-uns": 5, "über-uns": 5, "about": 5,
}

# URL-Segmente die wir grundsätzlich nicht scrapen wollen
URL_EXCLUDES = [
    "/products/", "/collections/", "/cart", "/checkout",
    "/account", "/search", "/blogs/", "/cdn/", "/apps/",
    ".jpg", ".png", ".gif", ".webp", ".css", ".js",
    "/orders/", "/pages/profile", "/pages/edit",
]

# Soft-404-Signale im Content (DE + EN)
SOFT_404_SIGNALS = [
    "404", "not found", "nicht gefunden", "seite nicht gefunden",
    "page not found", "diese seite existiert nicht",
    "die seite wurde nicht gefunden", "oops", "something went wrong",
]


def score_url(url: str) -> int:
    """Gibt Prioritätsscore für eine URL zurück. 0 = nicht relevant."""
    lower = url.lower()
    if any(ex in lower for ex in URL_EXCLUDES):
        return 0
    score = 0
    for keyword, points in URL_PRIORITY.items():
        if keyword in lower:
            score = max(score, points)
    return score


def pick_subpages(all_urls: list, base_url: str, n: int) -> list[str]:
    """Wählt die n relevantesten Unterseiten aus der Sitemap."""
    base = base_url.rstrip("/").lower()
    scored = []

    for link in all_urls:
        url = getattr(link, "url", link) if not isinstance(link, str) else link
        if not url or url.rstrip("/").lower() == base:
            continue
        s = score_url(url)
        if s == 0:
            continue
        scored.append((s, url))

    scored.sort(key=lambda x: x[0], reverse=True)
    # Nimm die Top-n, aber nie zwei URLs mit exakt gleichem Keyword
    selected = []
    used_keywords = set()
    for s, url in scored:
        lower = url.lower()
        kw = next((k for k in URL_PRIORITY if k in lower), None)
        if kw and kw not in used_keywords:
            selected.append(url)
            used_keywords.add(kw)
        if len(selected) >= n:
            break

    return selected


def is_soft_404(content: str) -> bool:
    sample = content[:500].lower()
    return any(signal in sample for signal in SOFT_404_SIGNALS)


JINA_BASE = "https://r.jina.ai/"
JINA_HEADERS = {"Accept": "text/markdown", "X-Return-Format": "markdown"}
JINA_TIMEOUT = 30


def _check_content(content: str, label: str, seen_lengths: set) -> str | None:
    """Shared validation: length, soft-404, dedup."""
    content = (content or "").strip()
    if len(content) < MIN_CONTENT_LENGTH:
        print(f"  {label}: skipped (zu kurz: {len(content)} chars)")
        return None
    if is_soft_404(content):
        print(f"  {label}: skipped (soft-404)")
        return None
    if len(content) in seen_lengths:
        print(f"  {label}: skipped (Duplikat)")
        return None
    seen_lengths.add(len(content))
    return content


def scrape_url_jina(url: str, label: str, max_chars: int, seen_lengths: set) -> str | None:
    """Scrape via Jina AI Reader — free, no key needed."""
    try:
        r = _requests.get(f"{JINA_BASE}{url}", headers=JINA_HEADERS, timeout=JINA_TIMEOUT)
        if r.status_code != 200:
            print(f"  {label}: Jina HTTP {r.status_code}")
            return None
        content = _check_content(r.text, label, seen_lengths)
        if content:
            print(f"  {label}: {len(content)} chars (jina)")
        return content[:max_chars] if content else None
    except Exception as e:
        print(f"  {label}: jina fehler — {e}")
        return None


async def _crawl4ai_async(url: str) -> str:
    from crawl4ai import AsyncWebCrawler
    async with AsyncWebCrawler(headless=True, verbose=False) as crawler:
        result = await crawler.arun(url=url)
        return result.markdown or ""


def scrape_url_crawl4ai(url: str, label: str, max_chars: int, seen_lengths: set) -> str | None:
    """Fallback scraper via crawl4ai — handles JS-rendered sites."""
    try:
        import crawl4ai  # noqa — check installed
    except ImportError:
        print(f"  {label}: crawl4ai nicht installiert (pip install crawl4ai && crawl4ai-setup)")
        return None
    try:
        raw = asyncio.run(_crawl4ai_async(url))
        content = _check_content(raw, label, seen_lengths)
        if content:
            print(f"  {label}: {len(content)} chars (crawl4ai)")
        return content[:max_chars] if content else None
    except Exception as e:
        print(f"  {label}: crawl4ai fehler — {e}")
        return None


def discover_subpages(base_url: str) -> list[str]:
    """Discover subpage URLs from sitemap.xml. Returns empty list on failure."""
    from xml.etree import ElementTree
    base = base_url.rstrip("/")
    for path in ["/sitemap.xml", "/sitemap_index.xml"]:
        try:
            r = _requests.get(f"{base}{path}", timeout=10, allow_redirects=True)
            if r.status_code != 200:
                continue
            root = ElementTree.fromstring(r.content)
            ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            urls = [loc.text for loc in root.findall(".//sm:loc", ns) if loc.text]
            if urls:
                print(f"  sitemap: {len(urls)} URLs gefunden")
                return urls
        except Exception:
            continue
    print("  sitemap: nicht gefunden — fahre ohne Unterseiten fort")
    return []


def _cache_domain(url: str) -> str:
    """https://absolem.at/ → absolem.at"""
    from urllib.parse import urlparse
    host = urlparse(url).netloc or url
    return host.replace("www.", "").rstrip("/")


def _cache_load(url: str, cache_dir: Path) -> dict | None:
    """Gibt gecachte pages zurück oder None bei Cache-Miss."""
    path = cache_dir / f"{_cache_domain(url)}.json"
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            print(f"  [cache HIT] {_cache_domain(url)}")
            return data
        except Exception:
            pass
    return None


def _cache_save(url: str, pages: dict, cache_dir: Path):
    """Speichert pages als JSON im Cache-Verzeichnis."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{_cache_domain(url)}.json"
    path.write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")


def scrape_pages(base_url: str, api_key: str | None = None, cache_dir: Path | None = None) -> dict[str, str]:
    """Scrape homepage + subpages. Uses Jina AI (free) with crawl4ai fallback. api_key unused."""
    if cache_dir is not None:
        cached = _cache_load(base_url, cache_dir)
        if cached is not None:
            return cached

    pages = {}
    seen_lengths: set = set()

    print(f"\nScraping: {base_url}")

    # 1. Homepage — Jina primary, crawl4ai fallback
    content = scrape_url_jina(base_url, "homepage", MAX_CHARS_HOMEPAGE, seen_lengths)
    if not content:
        print("  homepage: jina fehlgeschlagen → versuche crawl4ai")
        content = scrape_url_crawl4ai(base_url, "homepage", MAX_CHARS_HOMEPAGE, seen_lengths)
    if not content:
        raise FirecrawlError("Homepage nicht erreichbar — leerer oder zu kurzer Inhalt")
    pages["homepage"] = content

    # 2. Subpage discovery via sitemap.xml
    all_urls = discover_subpages(base_url)
    subpages = pick_subpages(all_urls, base_url, MAX_SUBPAGES)
    print(f"  subpages: {len(subpages)} ausgewählt")

    # 3. Scrape subpages
    for url in subpages:
        label = "/" + url.split(base_url.rstrip("/"), 1)[-1].lstrip("/")
        content = scrape_url_jina(url, label, MAX_CHARS_SUBPAGE, seen_lengths)
        if not content:
            content = scrape_url_crawl4ai(url, label, MAX_CHARS_SUBPAGE, seen_lengths)
        if content:
            pages[label] = content

    print(f"\n  Gesamt: {len(pages)} Seiten scraped")

    if cache_dir is not None and pages:
        _cache_save(base_url, pages, cache_dir)

    return pages


# ── Claude Analysis ───────────────────────────────────────────────────────────

def build_user_message(url: str, pages: dict[str, str]) -> str:
    parts = [f"Analyze this ecommerce website as a GetKiAgent lead.\n\nWebsite URL: {url}\n\nScraped content:\n"]
    for name, content in pages.items():
        parts.append(f"=== PAGE: {name} ===\n{content}")
    return "\n\n".join(parts)


def extract_json(raw: str) -> dict:
    """Parse JSON from model output, handling markdown code blocks."""
    raw = raw.strip()

    # Try direct parse
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Try extracting from ```json ... ``` block
    match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", raw)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Try finding first { ... } block
    match = re.search(r"\{[\s\S]+\}", raw)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    return None


def analyze_with_claude(url: str, pages: dict[str, str], api_key: str, extra_system_suffix: str = "") -> dict:
    try:
        import anthropic
    except ImportError:
        print("ERROR: anthropic not installed. Run: pip install anthropic")
        sys.exit(1)

    prompt_path = Path("prompts/lead_analysis_v1.md")
    if not prompt_path.exists():
        print(f"ERROR: Prompt file not found at {prompt_path}")
        sys.exit(1)

    system_prompt = prompt_path.read_text(encoding="utf-8")
    if extra_system_suffix:
        system_prompt = system_prompt + "\n\n" + extra_system_suffix
    user_message = build_user_message(url, pages)

    print("\nAnalyzing with Claude...")
    client = anthropic.Anthropic(api_key=api_key)

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    raw = response.content[0].text
    result = extract_json(raw)

    if result is None:
        debug_path = Path("leads/debug-raw.txt")
        debug_path.parent.mkdir(exist_ok=True)
        debug_path.write_text(raw, encoding="utf-8")
        raise ClaudeParseError(f"Kein valides JSON im Modell-Output (gespeichert in {debug_path})")

    return result


# ── Validation ────────────────────────────────────────────────────────────────

def validate_result(result: dict):
    # Import from sibling module
    sys.path.insert(0, str(Path(__file__).parent))
    from lead_schema import validate_lead

    errors = validate_lead(result)
    if errors:
        print("\nWARNING: Output validation issues:")
        for e in errors:
            print(f"  - {e}")


# ── Output ────────────────────────────────────────────────────────────────────

def save_output(result: dict):
    output_path = Path("leads/single-test.json")
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return output_path


def print_summary(result: dict):
    score = result.get("score_1_to_10", "?")
    tier = result.get("tier", "?")
    tier_label = {"A": "STRONG LEAD", "B": "REVIEW LATER", "C": "WEAK FIT"}.get(tier, tier)

    print("\n" + "=" * 52)
    print("  LEAD ANALYSIS SUMMARY")
    print("=" * 52)
    print(f"  Company    : {result.get('company_name', 'Unknown')}")
    print(f"  Category   : {result.get('category', '-')}")
    print(f"  Country    : {result.get('country', '-')}")
    print(f"  Score      : {score}/10  |  Tier {tier} — {tier_label}")
    print(f"  Confidence : {result.get('confidence_level', '-')}")
    print()

    pain = result.get("support_pain_signals", [])
    if pain:
        print("  Pain signals:")
        for s in pain[:3]:
            print(f"    • {s}")

    opp = result.get("likely_automation_opportunity", "")
    if opp:
        print(f"\n  Opportunity: {opp}")

    rationale = result.get("score_rationale", "")
    if rationale:
        print(f"\n  Score rationale: {rationale}")

    action = result.get("recommended_next_action", "")
    if action:
        print(f"\n  Next action: {action}")

    uncertainty = result.get("uncertainty_notes", "")
    if uncertainty:
        print(f"\n  Uncertainty: {uncertainty}")

    print("=" * 52)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/analyze_lead.py <url>")
        print("Example: python scripts/analyze_lead.py https://example-brand.de")
        sys.exit(1)

    url = normalize_url(sys.argv[1])

    firecrawl_key, anthropic_key = load_and_validate_env()

    try:
        pages = scrape_pages(url, firecrawl_key)
        result = analyze_with_claude(url, pages, anthropic_key)
    except (FirecrawlError, ClaudeParseError) as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    validate_result(result)
    output_path = save_output(result)
    print_summary(result)
    print(f"\nFull JSON saved to: {output_path}")


if __name__ == "__main__":
    main()
