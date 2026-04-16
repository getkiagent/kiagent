"""
Generate research report for ki-solo-operator-decision.
Reads all JSON results (M1-M5) and markdown files (C3-C6),
outputs a single report.md.
"""
import json
import re
from pathlib import Path

RESULTS_DIR = Path(__file__).parent / "results"
OUTPUT = Path(__file__).parent / "report.md"
FIELDS_YAML = Path(__file__).parent / "fields.yaml"

UNCERTAIN_MARKER = "[uncertain]"

# Fields to show in TOC
TOC_FIELDS = [
    ("fit_feasibility", "operator_fit_1_10", "Fit"),
    ("revenue_economics", "revenue_month_12_conservative_eur", "Mon12-konservativ"),
    ("delivery_risk", "moat_1_10", "Moat"),
]

CATEGORY_ORDER = [
    "fit_feasibility",
    "revenue_economics",
    "acquisition",
    "delivery_risk",
    "evidence",
    "honest_verdict",
]

CATEGORY_LABELS = {
    "fit_feasibility": "Fit & Machbarkeit",
    "revenue_economics": "Umsatz-Ökonomie",
    "acquisition": "Kundengewinnung",
    "delivery_risk": "Delivery-Risiko",
    "evidence": "Nachweise & Evidenz",
    "honest_verdict": "Ehrliches Fazit",
}

ITEM_ORDER = ["M1", "M2", "M3", "M4", "M5"]


def load_jsons():
    items = {}
    for f in sorted(RESULTS_DIR.glob("M*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        item_id = data.get("id", f.stem.split("_")[0])
        items[item_id] = data
    return items


def is_uncertain(value, field_name, uncertain_list):
    if field_name in uncertain_list:
        return True
    if isinstance(value, str) and UNCERTAIN_MARKER in value:
        return True
    return False


def extract_toc_value(data, category, field):
    cat_data = data.get(category, {})
    field_data = cat_data.get(field, {})
    if isinstance(field_data, dict):
        v = field_data.get("score") or field_data.get("value") or ""
    else:
        v = field_data or ""
    # Extract first number if value is a long string
    if isinstance(v, str) and len(v) > 20:
        m = re.search(r"(\d+(?:[/,]\d+)?(?:\.\d+)?)", v)
        return m.group(1) if m else "?"
    return v


def slugify(text):
    return re.sub(r"[^a-z0-9-]", "-", text.lower().strip()).strip("-")


def format_value(val, depth=0):
    if isinstance(val, dict):
        parts = []
        for k, v in val.items():
            if k in ("marked_uncertain",):
                continue
            parts.append(f"**{k}:** {format_value(v, depth+1)}")
        return "\n\n".join(parts)
    if isinstance(val, list):
        if all(isinstance(i, dict) for i in val):
            return "\n".join(
                "- " + " | ".join(f"{k}: {v}" for k, v in item.items())
                for item in val
            )
        return "\n".join(f"- {i}" for i in val)
    s = str(val)
    if len(s) > 120:
        return s
    return s


def render_category(category, cat_data, uncertain_list):
    label = CATEGORY_LABELS.get(category, category)
    lines = [f"### {label}\n"]
    if isinstance(cat_data, dict):
        for field, val in cat_data.items():
            if is_uncertain(val, field, uncertain_list):
                continue
            if isinstance(val, str) and not val.strip():
                continue
            formatted = format_value(val)
            lines.append(f"**{field}**\n\n{formatted}\n")
    return "\n".join(lines)


def render_item(item_id, data):
    uncertain_list = data.get("uncertain", [])
    name = data.get("name", item_id)
    desc = data.get("description", "")
    anchor = slugify(f"{item_id}-{name}")

    lines = [f"## {item_id} — {name} {{#{anchor}}}\n"]
    if desc:
        lines.append(f"*{desc}*\n")

    for cat in CATEGORY_ORDER:
        cat_data = data.get(cat)
        if not cat_data:
            continue
        lines.append(render_category(cat, cat_data, uncertain_list))

    sources = data.get("sources", [])
    if sources:
        lines.append("### Quellen\n")
        for s in sources:
            title = s.get("title", "")
            url = s.get("url", "")
            if url:
                lines.append(f"- [{title}]({url})")
            else:
                lines.append(f"- {title}")
        lines.append("")

    return "\n".join(lines)


def build_toc(items_ordered, items_data):
    lines = ["## Inhaltsverzeichnis\n"]
    lines.append("### Modelle (M1–M5)\n")
    header_parts = ["Nr", "Modell"] + [label for _, _, label in TOC_FIELDS]
    lines.append("| " + " | ".join(header_parts) + " |")
    lines.append("| " + " | ".join("---" for _ in header_parts) + " |")

    for i, item_id in enumerate(items_ordered, 1):
        data = items_data[item_id]
        name = data.get("name", item_id)
        anchor = slugify(f"{item_id}-{name}")
        toc_vals = []
        for cat, field, _ in TOC_FIELDS:
            v = extract_toc_value(data, cat, field)
            if isinstance(v, dict):
                v = v.get("score") or v.get("value") or ""
            toc_vals.append(str(v) if v != "" else "—")
        row = [str(i), f"[{item_id}: {name}](#{anchor})"] + toc_vals
        lines.append("| " + " | ".join(row) + " |")

    lines.append("")
    lines.append("### Cross-Sections (C3–C6)\n")
    cross = [
        ("C3", "Bewertung bestehendes Projekt", "c3-bewertung-bestehendes-projekt"),
        ("C4", "Quit-or-Stay Entscheidungsmatrix", "c4-quit-or-stay-entscheidungsmatrix"),
        ("C5", "Dokumentierte Vorbilder", "c5-dokumentierte-vorbilder"),
        ("C6", "Anti-Hype-Filter", "c6-anti-hype-filter"),
    ]
    for cid, label, anchor in cross:
        lines.append(f"- [{cid}: {label}](#{anchor})")
    lines.append("")

    return "\n".join(lines)


def load_markdown(filename, heading_id):
    path = RESULTS_DIR / filename
    if not path.exists():
        return f"## {filename} — Datei nicht gefunden\n"
    content = path.read_text(encoding="utf-8")
    # Inject anchor on the first heading
    first_heading = re.match(r"^(#+\s+.+)", content, re.MULTILINE)
    if first_heading:
        h = first_heading.group(1)
        content = content.replace(h, h + f" {{#{heading_id}}}", 1)
    return content


def main():
    items_data = load_jsons()
    items_ordered = [i for i in ITEM_ORDER if i in items_data]

    sections = []

    # Title
    sections.append("# KI Solo-Operator Entscheidungsreport — DACH 2025/2026\n")
    sections.append(
        "> Optimales KI-Geschäftsmodell für Solo-Operator ohne Dev-Background.\n"
        "> Alle Modelle evaluiert nach Fit, Ökonomie, Akquise, Delivery-Risiko und belegter Evidenz.\n"
    )

    # TOC
    sections.append(build_toc(items_ordered, items_data))

    # Divider
    sections.append("---\n")

    # Model sections
    for item_id in items_ordered:
        sections.append(render_item(item_id, items_data[item_id]))
        sections.append("---\n")

    # Cross-cutting sections
    cross_files = [
        ("C3_Existing_Project_Assessment.md", "c3-bewertung-bestehendes-projekt"),
        ("C4_Quit_Decision_Matrix.md", "c4-quit-or-stay-entscheidungsmatrix"),
        ("C5_Precedents.md", "c5-dokumentierte-vorbilder"),
        ("C6_Anti_Hype_Filter.md", "c6-anti-hype-filter"),
    ]
    for fname, anchor in cross_files:
        sections.append(load_markdown(fname, anchor))
        sections.append("---\n")

    OUTPUT.write_text("\n".join(sections), encoding="utf-8")
    print(f"Report written to: {OUTPUT}")
    print(f"Size: {OUTPUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
