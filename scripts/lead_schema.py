"""
Lead output schema definition and validation.
All fields the Claude analyzer must return.
"""

REQUIRED_FIELDS = [
    "company_name",
    "website",
    "country",
    "category",
    "visible_contact_options",
    "support_pages_found",
    "support_pain_signals",
    "speed_to_lead_signals",
    "digital_maturity_clues",
    "likely_automation_opportunity",
    "confidence_level",
    "uncertainty_notes",
    "score_1_to_10",
    "tier",
    "score_rationale",
    "recommended_next_action",
]

FIELD_TYPES = {
    "score_1_to_10": (int, float),
    "tier": str,
    "confidence_level": str,
}

VALID_TIERS = {"A", "B", "C"}
VALID_CONFIDENCE = {"high", "medium", "low"}


def validate_lead(data: dict) -> list[str]:
    """
    Returns a list of validation errors.
    Empty list means valid.
    """
    errors = []

    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    if "score_1_to_10" in data:
        score = data["score_1_to_10"]
        if not isinstance(score, (int, float)) or not (1 <= score <= 10):
            errors.append(f"score_1_to_10 must be a number between 1 and 10, got: {score!r}")

    if "tier" in data:
        if data["tier"] not in VALID_TIERS:
            errors.append(f"tier must be A, B, or C, got: {data['tier']!r}")

    if "confidence_level" in data:
        cl = data["confidence_level"]
        if not isinstance(cl, str) or cl.lower() not in VALID_CONFIDENCE:
            errors.append(f"confidence_level must be high/medium/low, got: {cl!r}")

    return errors
