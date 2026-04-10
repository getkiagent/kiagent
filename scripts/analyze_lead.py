"""
GetKiAgent — Single-URL Lead Analyzer v1

Usage:
    python scripts/analyze_lead.py <url>

Requires .env with:
    FIRECRAWL_API_KEY=...
    ANTHROPIC_API_KEY=...
"""

import sys
import json
import os
import re
from pathlib import Path


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

    firecrawl_key = os.getenv("FIRECRAWL_API_KEY", "").strip()
    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "").strip()

    missing = []
    if not firecrawl_key:
        missing.append("FIRECRAWL_API_KEY")
    if not anthropic_key:
        missing.append("ANTHROPIC_API_KEY")

    if missing:
        print(f"ERROR: Missing required environment variables: {', '.join(missing)}")
        print("Create a .env file in the project root with these keys set.")
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


def scrape_url(app, url: str, label: str, max_chars: int, seen_lengths: set) -> str | None:
    try:
        result = app.scrape(url, formats=["markdown"], wait_for=2000)
        if isinstance(result, dict):
            content = result.get("markdown") or result.get("content") or ""
        else:
            content = getattr(result, "markdown", "") or getattr(result, "content", "") or ""

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
        print(f"  {label}: {len(content)} chars")
        return content[:max_chars]

    except Exception as e:
        err = str(e)
        err_lower = err.lower()
        if "timeout" in err_lower or "timed out" in err_lower or "read timed out" in err_lower:
            raise FirecrawlTimeoutError(f"{label}: {err}")
        if any(c in err for c in ["404", "403", "Not Found", "Forbidden", "Payment"]):
            short = "nicht gefunden" if "404" in err or "Not Found" in err else "fehler"
            print(f"  {label}: {short}")
        else:
            print(f"  {label}: failed — {err}")
        return None


def scrape_pages(base_url: str, api_key: str) -> dict[str, str]:
    try:
        from firecrawl import FirecrawlApp
    except ImportError:
        print("ERROR: firecrawl-py nicht installiert.")
        sys.exit(1)

    app = FirecrawlApp(api_key=api_key)
    pages = {}
    seen_lengths: set = set()

    print(f"\nScraping: {base_url}")

    # 1. Homepage scrapen
    content = scrape_url(app, base_url, "homepage", MAX_CHARS_HOMEPAGE, seen_lengths)
    if not content:
        raise FirecrawlError("Homepage nicht erreichbar — leerer oder zu kurzer Inhalt")
    pages["homepage"] = content

    # 2. Sitemap per map() holen (1 Credit) → beste Unterseiten auswählen
    print(f"  map: Sitemap abrufen...")
    try:
        map_result = app.map(base_url, limit=300)
        all_urls = map_result.links if hasattr(map_result, "links") else []
        subpages = pick_subpages(all_urls, base_url, MAX_SUBPAGES)
        print(f"  map: {len(all_urls)} URLs gefunden → {len(subpages)} ausgewählt")
    except Exception as e:
        print(f"  map: fehlgeschlagen ({e}) — fahre ohne Unterseiten fort")
        subpages = []

    # 3. Ausgewählte Unterseiten scrapen
    for url in subpages:
        label = "/" + url.split(base_url.rstrip("/"), 1)[-1].lstrip("/")
        try:
            content = scrape_url(app, url, label, MAX_CHARS_SUBPAGE, seen_lengths)
        except FirecrawlTimeoutError:
            print(f"  {label}: timeout (übersprungen)")
            continue
        if content:
            pages[label] = content

    print(f"\n  Gesamt: {len(pages)} Seiten | ~{1 + 1 + len(pages) - 1} Credits verbraucht")
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


def analyze_with_claude(url: str, pages: dict[str, str], api_key: str) -> dict:
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

    url = sys.argv[1].strip()
    if not url.startswith("http"):
        url = "https://" + url

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
