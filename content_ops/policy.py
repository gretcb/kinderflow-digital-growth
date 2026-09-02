"""Deterministic content, asset, and publication policy checks."""

from __future__ import annotations

import re
from typing import Any


BIOMECHANICAL_TERMS = re.compile(
    r"\b(?:palm|finger|fingers|thumb|rotate|bend|tap|touch|handshape|wrist)\b",
    re.IGNORECASE,
)


def _result(failures: list[dict[str, str]], warnings: list[str] | None = None) -> dict[str, Any]:
    warnings = warnings or []
    return {
        "passed": not failures,
        "failed_checks": failures,
        "warnings": warnings,
        "blocking_reasons": [failure["detail"] for failure in failures],
    }


def check_content_quality(package: dict[str, Any]) -> dict[str, Any]:
    sign = package.get("sign", {})
    content = package.get("content_package", {})
    failures: list[dict[str, str]] = []
    required = {
        "sign.sign_id": sign.get("sign_id"),
        "sign.display_name": sign.get("display_name"),
        "sign.spanish_label": sign.get("spanish_label"),
        "sign.routine": sign.get("routine"),
        "content.family_guidance": content.get("family_guidance"),
        "content.try_it_during": content.get("try_it_during"),
        "content.language": content.get("language"),
        "content.generation_method": content.get("generation_method"),
        "content.content_version": content.get("content_version"),
    }
    for name, value in required.items():
        if value is None or value == "" or value == {}:
            failures.append({"check": "required_content", "detail": f"Missing required field: {name}."})
    if content.get("language") not in {"es", "en", "bilingual"}:
        failures.append({"check": "allowed_language", "detail": "Content language must be es, en, or bilingual."})
    if content.get("generation_method") not in {"human", "llm_assisted", "imported"}:
        failures.append({"check": "generation_method", "detail": "Unknown content generation method."})
    for field in ("family_guidance", "try_it_during"):
        value = content.get(field)
        values = value.values() if isinstance(value, dict) else [value]
        for text in values:
            if isinstance(text, str) and BIOMECHANICAL_TERMS.search(text):
                failures.append({"check": "no_biomechanical_instructions", "detail": f"{field} contains unsupported movement-detail wording."})
                break
    return _result(failures)


def check_asset_readiness(package: dict[str, Any]) -> dict[str, Any]:
    sign = package.get("sign", {})
    technical = package.get("technical", {})
    visual = package.get("visual_package", {})
    failures: list[dict[str, str]] = []
    if not sign.get("source_reference"):
        failures.append({"check": "source_reference", "detail": "Validated source reference is missing."})
    if not technical.get("evidence_reference"):
        failures.append({"check": "technical_evidence", "detail": "Technical evidence reference is missing."})
    if visual.get("illustration_status") != "READY":
        failures.append({"check": "illustration_ready", "detail": "Illustration artwork is not ready."})
    if not visual.get("character_asset"):
        failures.append({"check": "character_asset", "detail": "Character asset is missing."})
    if not visual.get("hand_pose_asset"):
        failures.append({"check": "hand_pose_asset", "detail": "Sign-specific hand-pose asset is missing."})
    if visual.get("hand_review_status") != "REVIEWED":
        failures.append({"check": "hand_review", "detail": "Sign-specific hand pose has not completed human review."})
    return _result(failures)


def check_publication_policy(package: dict[str, Any]) -> dict[str, Any]:
    technical = package.get("technical", {})
    content = package.get("content_package", {})
    visual = package.get("visual_package", {})
    review = package.get("review", {})
    publication = package.get("publication_package", {})
    failures: list[dict[str, str]] = []
    if technical.get("state") not in {"PASS", "REVIEW_NEEDED"}:
        failures.append({"check": "technical_state", "detail": "Technical state is not acceptable for human publication review."})
    if content.get("state") != "APPROVED":
        failures.append({"check": "content_approved", "detail": "Family content is not approved."})
    if visual.get("state") != "READY":
        failures.append({"check": "visual_ready", "detail": "Visual package is not ready."})
    if visual.get("hand_review_status") != "REVIEWED":
        failures.append({"check": "hand_review", "detail": "Hand-pose review is incomplete."})
    if review.get("review_status") != "APPROVED" or review.get("reviewer_type") != "human":
        failures.append({"check": "human_approval", "detail": "Explicit human publication approval is missing."})
    if publication.get("publication_status") not in {"APPROVED", "PUBLISHED"}:
        failures.append({"check": "publication_state", "detail": "Publication package has not reached APPROVED."})
    return _result(failures)


def evaluate_package(package: dict[str, Any]) -> dict[str, Any]:
    content = check_content_quality(package)
    assets = check_asset_readiness(package)
    publication = check_publication_policy(package)
    blocking = content["blocking_reasons"] + assets["blocking_reasons"] + publication["blocking_reasons"]
    return {
        "passed": content["passed"] and assets["passed"] and publication["passed"],
        "failed_checks": content["failed_checks"] + assets["failed_checks"] + publication["failed_checks"],
        "warnings": content["warnings"] + assets["warnings"] + publication["warnings"],
        "blocking_reasons": list(dict.fromkeys(blocking)),
        "domains": {"content_quality": content, "asset_readiness": assets, "publication_policy": publication},
    }
