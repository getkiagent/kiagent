"""
GetKiAgent — Niche Configuration Loader

Loads niche-specific settings from configs/{niche}.yaml.
Used by discover_leads.py, batch_analyze.py, generate_outreach.py.

Usage:
    from niche_config import load_niche_config
    config = load_niche_config("ecommerce-beauty")  # returns dict or exits
    config = load_niche_config(None)                 # returns None (legacy mode)
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIGS_DIR = PROJECT_ROOT / "configs"


def load_niche_config(niche: str | None) -> dict | None:
    """Load configs/{niche}.yaml. Returns None if niche is None (legacy mode)."""
    if niche is None:
        return None

    try:
        import yaml
    except ImportError:
        print("ERROR: PyYAML not installed. Run: pip install pyyaml")
        sys.exit(1)

    config_path = CONFIGS_DIR / f"{niche}.yaml"
    if not config_path.exists():
        print(f"ERROR: Config not found: {config_path}")
        print(f"Available configs: {list_niches()}")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not config:
        print(f"ERROR: Config is empty: {config_path}")
        sys.exit(1)

    return config


def list_niches() -> list[str]:
    """List all available niche names from configs/*.yaml."""
    if not CONFIGS_DIR.exists():
        return []
    return [p.stem for p in sorted(CONFIGS_DIR.glob("*.yaml"))]


def niche_leads_dir(niche: str) -> Path:
    """Return leads/{niche}/ path, creating it if needed."""
    d = PROJECT_ROOT / "leads" / niche
    d.mkdir(parents=True, exist_ok=True)
    return d


def niche_outreach_dir(niche: str) -> Path:
    """Return outreach/{niche}/ path, creating it if needed."""
    d = PROJECT_ROOT / "outreach" / niche
    d.mkdir(parents=True, exist_ok=True)
    return d
