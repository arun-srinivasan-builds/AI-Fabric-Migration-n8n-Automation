import json


REQUIRED_FIELDS = [
    "project_id",
    "recommended_fabric_area",
    "risk_level",
    "confidence",
    "key_risks",
    "migration_considerations",
    "human_review_required",
    "reason",
    "sources_used",
]


def parse_assessment(response_text: str) -> dict:
    """
    Convert the LLM JSON response into a Python dictionary.
    """
    try:
        assessment = json.loads(response_text)

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"LLM response is not valid JSON: {exc}"
        ) from exc

    return assessment


def validate_assessment(assessment: dict) -> None:
    """
    Check that all required migration assessment fields exist.
    """
    missing_fields = [
        field
        for field in REQUIRED_FIELDS
        if field not in assessment
    ]

    if missing_fields:
        raise ValueError(
            f"Missing required fields: {missing_fields}"
        )

    if assessment["risk_level"] not in [
        "Low",
        "Medium",
        "High",
    ]:
        raise ValueError(
            "risk_level must be Low, Medium, or High"
        )

    confidence = assessment["confidence"]

    if not isinstance(confidence, (int, float)):
        raise ValueError(
            "confidence must be numeric"
        )

    if not 0 <= confidence <= 1:
        raise ValueError(
            "confidence must be between 0 and 1"
        )

    if not isinstance(
        assessment["human_review_required"],
        bool,
    ):
        raise ValueError(
            "human_review_required must be true or false"
        )


def parse_and_validate(response_text: str) -> dict:
    """
    Parse and validate an LLM migration assessment.
    """
    assessment = parse_assessment(response_text)

    validate_assessment(assessment)

    return assessment