"""Deterministic governance checks for Kinder Signs family-facing drafts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "sign_id",
    "source_id",
    "review_status",
    "requires_human_review",
    "parent_title",
    "short_explanation",
    "when_to_use",
    "practice_tip",
    "school_home_connection",
    "motion_note",
    "boundaries",
}

BANNED_CLAIMS = {
    "accelerate": re.compile(r"\baccelerate\b", re.IGNORECASE),
    "accelerated": re.compile(r"\baccelerated\b", re.IGNORECASE),
    "boost language": re.compile(r"\bboost\s+language\b", re.IGNORECASE),
    "treat delay": re.compile(r"\btreat(?:s|ed|ing)?\s+(?:a\s+)?(?:communication\s+)?delay", re.IGNORECASE),
    "diagnose": re.compile(r"\bdiagnos(?:e|es|ed|ing|is|tic)\b", re.IGNORECASE),
    "therapy": re.compile(r"\btherapy\b", re.IGNORECASE),
    "cure": re.compile(r"\bcure(?:s|d|ing)?\b", re.IGNORECASE),
    "ASL": re.compile(r"\bASL\b", re.IGNORECASE),
    "LSE": re.compile(r"\bLSE\b", re.IGNORECASE),
}

MOVEMENT_DETAIL_TERMS = {
    "hand",
    "hands",
    "finger",
    "fingers",
    "palm",
    "palms",
    "tap",
    "touch",
    "together",
    "apart",
    "rotate",
    "circle",
    "bend",
    "point",
    "raise",
    "lower",
}

MISSING_MOVEMENT_NOTE = (
    "Movement instructions are unavailable in the approved input; "
    "use an approved reference only after professional review."
)


class JsonLoadError(ValueError):
    """Raised when a JSON file cannot be loaded as an object."""


def load_json_object(path: str | Path) -> dict[str, Any]:
    json_path = Path(path)
    try:
        value = json.loads(json_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise JsonLoadError(f"{json_path}: {exc}") from exc
    if not isinstance(value, dict):
        raise JsonLoadError(f"{json_path}: expected a JSON object")
    return value


def iter_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from iter_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_strings(child)


def add_failure(failures: list[dict[str, str]], check: str, detail: str) -> None:
    failures.append({"check": check, "detail": detail})


def evaluate_quality_gate(
    output: dict[str, Any], source: dict[str, Any]
) -> dict[str, Any]:
    """Evaluate a parsed LLM output against approved source content."""
    failures: list[dict[str, str]] = []
    warnings: list[str] = []

    missing_fields = sorted(REQUIRED_FIELDS.difference(output))
    if missing_fields:
        add_failure(
            failures,
            "required_fields_present",
            f"Missing required fields: {', '.join(missing_fields)}",
        )

    if output.get("requires_human_review") is not True:
        add_failure(
            failures,
            "human_review_required",
            "requires_human_review must be the boolean value true.",
        )

    review_status = output.get("review_status")
    if review_status != "draft_requires_professional_approval":
        add_failure(
            failures,
            "review_status_preserved",
            "review_status must be draft_requires_professional_approval.",
        )

    if output.get("sign_id") != source.get("sign_id"):
        add_failure(
            failures,
            "sign_id_preserved",
            "Output sign_id does not match the approved source.",
        )
    if output.get("source_id") != source.get("source_id"):
        add_failure(
            failures,
            "source_id_preserved",
            "Output source_id does not match the approved source.",
        )

    output_text = "\n".join(iter_strings(output))
    for label, pattern in BANNED_CLAIMS.items():
        if pattern.search(output_text):
            add_failure(
                failures,
                "banned_claims_absent",
                f"Output contains banned term or claim: {label}.",
            )

    if "when_to_use" in output and not (
        isinstance(output["when_to_use"], list)
        and output["when_to_use"]
        and all(isinstance(item, str) and item.strip() for item in output["when_to_use"])
    ):
        add_failure(
            failures,
            "when_to_use_schema",
            "when_to_use must be a non-empty list of strings.",
        )
    if "boundaries" in output and not (
        isinstance(output["boundaries"], list)
        and output["boundaries"]
        and all(isinstance(item, str) and item.strip() for item in output["boundaries"])
    ):
        add_failure(
            failures,
            "boundaries_schema",
            "boundaries must be a non-empty list of strings.",
        )

    approved_movement = str(source.get("movement_notes") or "").strip()
    expected_motion_note = approved_movement or MISSING_MOVEMENT_NOTE
    actual_motion_note = output.get("motion_note")
    if actual_motion_note != expected_motion_note:
        add_failure(
            failures,
            "movement_note_source_adherence",
            (
                "motion_note must reproduce approved movement_notes exactly, or use "
                "the fixed missing-note fallback; paraphrasing could add movement details."
            ),
        )
    if not approved_movement:
        warnings.append(
            "Approved movement_notes are missing; the fixed no-instruction fallback is required."
        )

    approved_text = "\n".join(iter_strings(source)).lower()
    non_motion_output = {
        key: value for key, value in output.items() if key != "motion_note"
    }
    non_motion_text = "\n".join(iter_strings(non_motion_output)).lower()
    invented_terms = sorted(
        term
        for term in MOVEMENT_DETAIL_TERMS
        if re.search(rf"\b{re.escape(term)}\b", non_motion_text)
        and not re.search(rf"\b{re.escape(term)}\b", approved_text)
    )
    if invented_terms:
        add_failure(
            failures,
            "no_invented_movement_details",
            "Potential unapproved movement terms: " + ", ".join(invented_terms),
        )

    scalar_fields = {
        "sign_id",
        "source_id",
        "review_status",
        "parent_title",
        "short_explanation",
        "practice_tip",
        "school_home_connection",
        "motion_note",
    }
    invalid_scalars = sorted(
        field
        for field in scalar_fields.intersection(output)
        if not isinstance(output[field], str) or not output[field].strip()
    )
    if invalid_scalars:
        add_failure(
            failures,
            "field_types_valid",
            "Required text fields must be non-empty strings: "
            + ", ".join(invalid_scalars),
        )

    return {
        "passed": not failures,
        "failed_checks": failures,
        "warnings": warnings,
    }


def run_gate(input_path: str | Path, source_path: str | Path) -> dict[str, Any]:
    try:
        output = load_json_object(input_path)
        source = load_json_object(source_path)
    except JsonLoadError as exc:
        return {
            "passed": False,
            "failed_checks": [
                {"check": "valid_json", "detail": str(exc)}
            ],
            "warnings": [],
        }
    return evaluate_quality_gate(output, source)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run deterministic checks on a Kinder Signs LLM draft."
    )
    parser.add_argument("--input", required=True, help="Path to LLM output JSON")
    parser.add_argument("--source", required=True, help="Path to approved source JSON")
    args = parser.parse_args()

    result = run_gate(args.input, args.source)
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
