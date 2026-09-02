"""Structured, offline-first content-pack contracts and deterministic checks."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any


REQUIRED_OUTPUTS = {"family_guidance", "try_it_during", "teacher_message", "family_message", "flashcard_copy"}
ALLOWED_LANGUAGES = {"es", "en", "bilingual"}
ALLOWED_GENERATION_METHODS = {"human", "llm_assisted"}
PROMPT_VERSION = "kinder_signs_content_pack_v1"
GENERATED_FIELDS = {
    "schema_version", "run_id", "sign_id", "source_context_id", "source_reference",
    "prompt_version", "generation_method", "generation_mode", "language",
    "family_guidance", "try_it_during", "routine_context", "teacher_message",
    "family_message", "flashcard_copy", "review_status", "requires_human_review",
    "automatic_publication",
}
TEXT_LIMITS = {"family_guidance": 240, "try_it_during": 160, "routine_context": 160, "teacher_message": 320, "family_message": 320}
BIOMECHANICS = re.compile(r"\b(?:hand|hands|palm|finger|fingers|thumb|wrist|handshape|rotate|bend|tap|touch|mano|manos|palma|dedo|dedos|muñeca|gira|dobla)\b", re.IGNORECASE)
UNSUPPORTED_CLAIMS = re.compile(r"\b(?:accelerat(?:e|es|ed|ing)|boost language|treat(?:s|ed|ing)? delay|diagnos(?:e|es|ed|ing|is|tic)|therapy|cure(?:s|d|ing)?|acelera(?:r|do)?|diagnóstic[oa]|terapia|cura)\b", re.IGNORECASE)
CORRECTNESS_CLAIMS = re.compile(r"\b(?:the sign is correct|correct sign|linguistically correct|professionally validated sign|signo correcto|signo validado profesionalmente)\b", re.IGNORECASE)
BIOMECHANICS_KEYS = {"hand_shape", "handshape", "biomechanics", "finger_position", "movement_steps"}


def _result(failures: list[dict[str, str]], warnings: list[str] | None = None) -> dict[str, Any]:
    return {"passed": not failures, "failed_checks": failures, "warnings": warnings or [], "blocking_reasons": [item["detail"] for item in failures]}


def _is_bilingual_text(value: Any) -> bool:
    return isinstance(value, dict) and all(isinstance(value.get(code), str) and value[code].strip() for code in ("en", "es"))


def validate_content_input(payload: Any) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    if not isinstance(payload, dict):
        return _result([{"check": "input_object", "detail": "Content Pack input must be a JSON object."}])
    for field in ("sign_id", "display_name", "spanish_label", "audience", "language"):
        if not isinstance(payload.get(field), str) or not payload[field].strip():
            failures.append({"check": field, "detail": f"{field} must be a non-empty string."})
    if not _is_bilingual_text(payload.get("routine")):
        failures.append({"check": "routine", "detail": "routine must contain non-empty English and Spanish values."})
    context = payload.get("approved_context")
    if not isinstance(context, dict) or not context.get("context_id") or not isinstance(context.get("scope"), str) or not context["scope"].strip() or not _is_bilingual_text(context.get("school_use")) or not _is_bilingual_text(context.get("family_use")):
        failures.append({"check": "approved_context", "detail": "Approved source context with context_id, scope, school_use and family_use is required."})
    requested = payload.get("requested_outputs")
    if not isinstance(requested, list) or len(requested) != len(REQUIRED_OUTPUTS) or set(requested) != REQUIRED_OUTPUTS:
        failures.append({"check": "requested_outputs", "detail": "The required Content Pack output list is incomplete or unsupported."})
    if payload.get("language") not in ALLOWED_LANGUAGES:
        failures.append({"check": "language", "detail": "language must be es, en, or bilingual."})
    if payload.get("audience") != "family":
        failures.append({"check": "audience", "detail": "The current Content Pack contract supports the family audience only."})
    if BIOMECHANICS.search(" ".join(_walk_strings(payload))):
        failures.append({"check": "input_biomechanics", "detail": "Content Pack input cannot contain free-form movement or hand instructions."})
    return _result(failures)


def content_input_from_sign(sign: dict[str, Any], language: str = "bilingual") -> dict[str, Any]:
    return {
        "sign_id": sign["sign_id"], "display_name": sign["display_name"], "spanish_label": sign["spanish_label"],
        "routine": deepcopy(sign["routine"]), "audience": "family", "language": language,
        "approved_context": deepcopy(sign["approved_source_context"]), "requested_outputs": sorted(REQUIRED_OUTPUTS),
    }


def build_dry_run_candidate(
    sign: dict[str, Any],
    generation_method: str = "llm_assisted",
    run_id: str | None = None,
    language: str = "bilingual",
) -> dict[str, Any]:
    if generation_method not in ALLOWED_GENERATION_METHODS:
        raise ValueError("Unsupported generation method")
    return {
        "schema_version": "1.0", "run_id": run_id or f"content_dry_run_preview_{sign['sign_id']}",
        "sign_id": sign["sign_id"], "source_context_id": sign["approved_source_context"]["context_id"],
        "source_reference": sign["approved_source_context"]["context_id"], "prompt_version": PROMPT_VERSION,
        "generation_method": generation_method, "generation_mode": "DRY_RUN" if generation_method == "llm_assisted" else "NOT_APPLICABLE",
        "language": language,
        "family_guidance": deepcopy(sign["short_family_guidance"]), "try_it_during": deepcopy(sign["try_it_during"]),
        "routine_context": deepcopy(sign["routine"]), "teacher_message": deepcopy(sign["teacher_message"]),
        "family_message": deepcopy(sign["family_message"]),
        "flashcard_copy": {"primary_label": sign["display_name"], "secondary_label": sign["spanish_label"]},
        "review_status": "READY_FOR_REVIEW", "requires_human_review": True, "automatic_publication": False,
    }


def _walk_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for nested in value.values():
            yield from _walk_strings(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _walk_strings(nested)


def _walk_keys(value: Any):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield str(key).lower()
            yield from _walk_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _walk_keys(nested)


def validate_generated_output(raw: Any, source_input: dict[str, Any]) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    failures: list[dict[str, str]] = []
    try:
        candidate = json.loads(raw) if isinstance(raw, str) else deepcopy(raw)
    except (json.JSONDecodeError, TypeError) as error:
        detail = error.msg if hasattr(error, "msg") else str(error)
        return None, _result([{"check": "valid_json", "detail": f"Generated output is not valid JSON: {detail}."}])
    if not isinstance(candidate, dict):
        return None, _result([{"check": "output_object", "detail": "Generated output must be a JSON object."}])

    required = GENERATED_FIELDS
    missing = sorted(required.difference(candidate))
    if missing:
        failures.append({"check": "required_fields", "detail": f"Missing required output fields: {', '.join(missing)}."})
    extras = sorted(set(candidate).difference(GENERATED_FIELDS))
    if extras:
        failures.append({"check": "unsupported_fields", "detail": f"Unsupported output fields found: {', '.join(extras)}."})
    if candidate.get("sign_id") != source_input.get("sign_id"):
        failures.append({"check": "sign_id", "detail": "Generated sign_id does not match the structured source."})
    if candidate.get("source_context_id") != source_input.get("approved_context", {}).get("context_id"):
        failures.append({"check": "source_context_id", "detail": "Generated source_context_id does not match the approved context."})
    if candidate.get("source_reference") != source_input.get("approved_context", {}).get("context_id"):
        failures.append({"check": "source_reference", "detail": "Generated source_reference does not match the approved context."})
    if candidate.get("prompt_version") != PROMPT_VERSION:
        failures.append({"check": "prompt_version", "detail": "Generated prompt_version is missing or unsupported."})
    if candidate.get("generation_method") not in ALLOWED_GENERATION_METHODS:
        failures.append({"check": "generation_method", "detail": "generation_method must be human or llm_assisted."})
    expected_modes = {"llm_assisted": {"DRY_RUN", "LIVE"}, "human": {"NOT_APPLICABLE"}}
    if candidate.get("generation_mode") not in expected_modes.get(candidate.get("generation_method"), set()):
        failures.append({"check": "generation_mode", "detail": "generation_mode must match the recorded generation method."})
    if candidate.get("language") != source_input.get("language"):
        failures.append({"check": "language", "detail": "Generated language does not match the structured request."})
    if candidate.get("review_status") != "READY_FOR_REVIEW":
        failures.append({"check": "review_status", "detail": "Generated content must remain READY_FOR_REVIEW."})
    if candidate.get("requires_human_review") is not True:
        failures.append({"check": "human_review", "detail": "Generated content must require human review."})
    if candidate.get("automatic_publication") is not False:
        failures.append({"check": "automatic_publication", "detail": "Generated content cannot enable automatic publication."})

    for field in TEXT_LIMITS:
        value = candidate.get(field)
        if not _is_bilingual_text(value):
            failures.append({"check": field, "detail": f"{field} must contain non-empty English and Spanish values."})
            continue
        for language, text in value.items():
            if len(text) > TEXT_LIMITS[field]:
                failures.append({"check": f"{field}_length", "detail": f"{field}.{language} exceeds {TEXT_LIMITS[field]} characters."})

    labels = candidate.get("flashcard_copy")
    if not isinstance(labels, dict) or labels.get("primary_label") != source_input.get("display_name") or labels.get("secondary_label") != source_input.get("spanish_label"):
        failures.append({"check": "flashcard_copy", "detail": "Flashcard labels must match the structured source."})
    prohibited_keys = sorted(set(_walk_keys(candidate)).intersection(BIOMECHANICS_KEYS))
    if prohibited_keys:
        failures.append({"check": "biomechanics_fields", "detail": f"Unsupported biomechanics fields found: {', '.join(prohibited_keys)}."})
    combined_text = " ".join(_walk_strings(candidate))
    if BIOMECHANICS.search(combined_text):
        failures.append({"check": "biomechanics_content", "detail": "Content Pack contains unsupported movement or hand-shape wording."})
    if UNSUPPORTED_CLAIMS.search(combined_text):
        failures.append({"check": "unsupported_claim", "detail": "Content Pack contains an unsupported developmental or clinical claim."})
    if CORRECTNESS_CLAIMS.search(combined_text):
        failures.append({"check": "sign_correctness_claim", "detail": "Content Pack contains an unsupported sign-correctness claim."})
    return candidate, _result(failures)


def approve_content_locally(candidate: dict[str, Any], reviewer_action: str) -> dict[str, Any]:
    if reviewer_action != "explicit_demo_approval":
        raise ValueError("Explicit local human approval is required")
    approved = deepcopy(candidate)
    approved["review_status"] = "APPROVED"
    approved["human_review"] = {"mode": "LOCAL_DEMO", "approved": True}
    approved["automatic_publication"] = False
    return approved


def prepare_flashcard_handoff(candidate: dict[str, Any]) -> dict[str, Any]:
    if candidate.get("review_status") != "APPROVED" or candidate.get("human_review", {}).get("approved") is not True:
        raise ValueError("Only human-reviewed content can populate the Flashcard Studio handoff")
    return {
        "schema_version": "1.0", "run_id": candidate["run_id"], "sign_id": candidate["sign_id"], "generation_method": candidate["generation_method"],
        "review_status": candidate["review_status"], "family_guidance": deepcopy(candidate["family_guidance"]),
        "try_it_during": deepcopy(candidate["try_it_during"]), "routine_context": deepcopy(candidate["routine_context"]),
        "flashcard_copy": deepcopy(candidate["flashcard_copy"]),
    }


def build_demo_report(signs_path: str | Path) -> dict[str, Any]:
    signs = json.loads(Path(signs_path).read_text(encoding="utf-8"))["signs"]
    results = []
    for sign in signs:
        input_payload = content_input_from_sign(sign)
        candidate = build_dry_run_candidate(sign)
        _, gate = validate_generated_output(candidate, input_payload)
        results.append({
            "sign_id": sign["sign_id"], "display_name": sign["display_name"], "input": input_payload,
            "candidate_output": candidate, "deterministic_quality_gate": gate,
            "langsmith": {"mode": "DRY_RUN", "trace_status": "NOT_SENT", "evaluates": "LLM-assisted wording only", "dimensions": ["clarity", "brevity", "source consistency", "unsupported-claim risk", "hallucination against structured input"], "evidence": "workflow/langsmith_dry_run_summary.json"},
            "readiness": {"movement_intelligence": sign["video_status"], "character": sign["character_status"], "context": sign["context_status"], "hand_pose": sign["hand_pose_status"], "content": sign["content_status"], "flashcard": sign["flashcard_status"], "library": "BLOCKED_BY_HAND_REVIEW" if sign["sign_id"] == "more" else "BLOCKED"},
            "content_review": "PENDING", "flashcard_handoff": "BLOCKED_UNTIL_CONTENT_APPROVAL",
        })
    return {"schema_version": "1.0", "operation": "GENERATE_CONTENT_PACK", "results": results}
