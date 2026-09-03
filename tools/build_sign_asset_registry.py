#!/usr/bin/env python3
"""Build and validate the canonical Kinder Signs asset registry.

The registry stores repository-relative paths only. External source material is read
to calculate metadata and is never copied into the repository.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import mimetypes
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "assets/registry/sign_asset_registry.json"
SCHEMA_PATH = REPO_ROOT / "assets/registry/sign_asset_registry.schema.json"
REPORT_PATH = REPO_ROOT / "assets/registry/sign_asset_inventory.md"
RESOURCE_ROOT = (REPO_ROOT / "../resources").resolve()
POINTING_EXPECTED = "../resources/Flat Assets/Separate Atoms/pose/standing/pointing_finger-1.svg"
POINTING_ASSET_ID = "open_peeps_pointing_finger_reference"

CANONICAL_LABELS = {
    "more": ("MORE", "MÁS"),
    "help": ("HELP", "AYUDA"),
    "eat": ("EAT", "COMER"),
    "sleep": ("SLEEP", "DORMIR"),
    "milk": ("MILK", "LECHE"),
    "water": ("WATER", "AGUA"),
}
ASSET_CLASSES = {
    "THIRD_PARTY_REFERENCE",
    "FOUNDER_PROVIDED_REFERENCE",
    "TECHNICAL_EVIDENCE",
    "PREGENERATED_DEMO_OUTPUT",
    "KINDERFLOW_DERIVED_ASSET",
    "KINDERFLOW_RUNTIME_ASSET",
}
ASSET_REFERENCE_FIELDS = (
    "knowledge_sources",
    "reference_video_input",
    "reference_flashcard",
    "functional_sign_illustration",
    "supplementary_hand_sheet",
    "open_peeps_base",
    "open_peeps_hand_style_reference",
    "open_peeps_arm_reference",
    "gemini_demo_video",
    "contextual_image",
    "routine_icon_reference",
    "landmark_evidence",
    "static_visual_candidates",
    "reviewed_static_visual",
    "flashcard_outputs",
    "routine_card_outputs",
)
REQUIRED_EXISTING_FIELDS = (
    "reference_video_input",
    "reference_flashcard",
    "functional_sign_illustration",
    "open_peeps_base",
    "open_peeps_arm_reference",
)
SIGN_SPECIFIC_FIELDS = (
    "reference_video_input",
    "reference_flashcard",
    "functional_sign_illustration",
    "gemini_demo_video",
)
EXPECTED_DEMOS = {"more": "demo_more", "help": "demo_help", "milk": "demo_milk"}

WATER_SOURCE_ASSETS = {
    "input_water": {
        "path": "../resources/video_input/water.mp4",
        "workflow_role": "Reference input video and identity source for supporting WATER evidence",
        "asset_class": "FOUNDER_PROVIDED_REFERENCE",
        "licence_or_provenance_status": "FOUNDER_PROVIDED_PRESENTATION_RIGHTS_CONFIRMATION_NEEDED",
        "redistribution_allowed": False,
        "demo_display_allowed": None,
        "printable_allowed": False,
        "known_limitation": "Reference input is not automatic sign recognition or linguistic certification.",
    },
    "functional_water": {
        "path": "../resources/ilustraciones/water.jpg",
        "workflow_role": "Functional sign mechanics and pose reference",
        "asset_class": "FOUNDER_PROVIDED_REFERENCE",
        "licence_or_provenance_status": "FOUNDER_PROVIDED_RIGHTS_CONFIRMATION_NEEDED",
        "redistribution_allowed": None,
        "demo_display_allowed": None,
        "printable_allowed": False,
        "known_limitation": "Defines mechanics only and must not define KinderFlow character identity.",
    },
    "flashcard_water_reference": {
        "path": "../resources/flashcards/water-flash-card.pdf",
        "workflow_role": "Reference-only sign flashcard",
        "asset_class": "FOUNDER_PROVIDED_REFERENCE",
        "licence_or_provenance_status": "FOUNDER_PROVIDED_RIGHTS_CONFIRMATION_NEEDED",
        "redistribution_allowed": None,
        "demo_display_allowed": None,
        "printable_allowed": False,
        "known_limitation": "Reference-only source; never a distributable KinderFlow output.",
    },
}

WATER_EVIDENCE_RENAMES = {
    "more_landmark_summary": "water_landmark_summary",
    "more_detection_timeline": "water_detection_timeline",
    "more_validation_summary": "water_validation_summary",
}


class RegistryValidationError(ValueError):
    """Raised when registry data fails closed validation."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_type(path: Path) -> str:
    custom_types = {
        ".eps": "application/postscript",
        ".json": "application/json",
        ".md": "text/markdown",
        ".svg": "image/svg+xml",
    }
    return custom_types.get(path.suffix.lower()) or mimetypes.guess_type(path.name)[0] or "application/octet-stream"


def resolve_asset_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        raise RegistryValidationError("Asset paths must be relative: {0}".format(relative_path))
    resolved = (REPO_ROOT / path).resolve()
    allowed_roots = (REPO_ROOT.resolve(), RESOURCE_ROOT)
    if not any(resolved == root or root in resolved.parents for root in allowed_roots):
        raise RegistryValidationError("Asset path escapes the allowed roots: {0}".format(relative_path))
    return resolved


def find_pointing_reference() -> Optional[Path]:
    standing_root = RESOURCE_ROOT / "Flat Assets/Separate Atoms/pose/standing"
    if not standing_root.is_dir():
        return None
    matches = sorted(
        path for path in standing_root.rglob("*")
        if path.is_file() and path.name.casefold() == "pointing_finger-1.svg"
    )
    if len(matches) > 1:
        raise RegistryValidationError(
            "Multiple case-insensitive pointing_finger-1.svg matches found: {0}".format(
                ", ".join(str(path) for path in matches)
            )
        )
    return matches[0] if matches else None


def _iter_asset_ids(value: Any) -> Iterable[str]:
    if value is None:
        return
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, str):
                yield item


def get_sign(registry: Dict[str, Any], sign_id: str) -> Dict[str, Any]:
    if sign_id not in CANONICAL_LABELS:
        raise RegistryValidationError("Unknown sign_id fails closed: {0}".format(sign_id))
    for sign in registry["signs"]:
        if sign["sign_id"] == sign_id:
            return sign
    raise RegistryValidationError("Canonical sign is missing from registry: {0}".format(sign_id))


def _new_asset(spec: Dict[str, Any], sign_mapping: List[str]) -> Dict[str, Any]:
    """Return a complete registry record whose file facts are refreshed later."""
    return {
        "path": spec["path"],
        "exists": False,
        "file_type": None,
        "byte_size": None,
        "sha256": None,
        "sign_mapping": sign_mapping,
        "workflow_role": spec["workflow_role"],
        "asset_class": spec["asset_class"],
        "licence_or_provenance_status": spec["licence_or_provenance_status"],
        "redistribution_allowed": spec["redistribution_allowed"],
        "demo_display_allowed": spec["demo_display_allowed"],
        "printable_allowed": spec["printable_allowed"],
        "known_limitation": spec["known_limitation"],
    }


def _sync_visual_candidates(registry: Dict[str, Any]) -> None:
    """Project deterministic browser candidates into the canonical registry."""
    package_path = REPO_ROOT / registry["assets"]["visual_sign_packages"]["path"]
    packages = json.loads(package_path.read_text(encoding="utf-8"))["signs"]
    package_ids = [item["sign_id"] for item in packages if item["sign_id"] in CANONICAL_LABELS]
    registry["assets"]["visual_sign_packages"]["sign_mapping"] = package_ids
    registry["assets"]["visual_sign_packages"]["known_limitation"] = (
        "All six canonical signs have controlled visual options; every option still requires human review."
    )

    for asset_id in [key for key in registry["assets"] if key.startswith("static_")]:
        del registry["assets"][asset_id]

    packages_by_id = {item["sign_id"]: item for item in packages}
    for sign in registry["signs"]:
        package = packages_by_id.get(sign["sign_id"])
        sign["knowledge_sources"] = [
            item for item in sign["knowledge_sources"] if item != "visual_sign_packages"
        ]
        sign["static_visual_candidates"] = []
        if not package:
            continue
        sign["knowledge_sources"].append("visual_sign_packages")
        candidates = package.get("candidates", []) + package.get("regeneration_candidates", [])
        for candidate in candidates:
            browser_path = Path(candidate["asset"])
            asset_id = "static_{0}".format(browser_path.stem.replace("-", "_"))
            registry["assets"][asset_id] = _new_asset(
                {
                    "path": (Path("prototype") / browser_path).as_posix(),
                    "workflow_role": "Source-grounded deterministic sign visual option",
                    "asset_class": "KINDERFLOW_DERIVED_ASSET",
                    "licence_or_provenance_status": "OPEN_PEEPS_CC0_DERIVATIVE_WITH_KINDERFLOW_CUSTOM_LAYER",
                    "redistribution_allowed": True,
                    "demo_display_allowed": True,
                    "printable_allowed": False,
                    "known_limitation": "Requires human visual review; not published or linguistically certified.",
                },
                [sign["sign_id"]],
            )
            sign["static_visual_candidates"].append(asset_id)
        if candidates:
            sign["visual_status"] = "SOURCE_GROUNDED_OPTIONS_NEED_HUMAN_REVIEW"
            sign["known_gaps"] = [
                gap for gap in sign["known_gaps"]
                if "artwork" not in gap.casefold() and "static visual" not in gap.casefold()
            ]
            review_gap = "Sign visual options need human review; no distributable card output is approved."
            if review_gap not in sign["known_gaps"]:
                sign["known_gaps"].append(review_gap)


def upgrade_prompt_2b_registry(registry: Dict[str, Any]) -> None:
    """Register WATER support evidence and distinguish the current MORE demo."""
    registry["canonical_sign_ids"] = list(CANONICAL_LABELS)
    assets = registry["assets"]

    for asset_id, spec in WATER_SOURCE_ASSETS.items():
        assets[asset_id] = _new_asset(spec, ["water"])

    more_input = assets.get("input_more")
    if more_input:
        more_input["workflow_role"] = "Reference input video and identity source for the local MORE demo reference"
        more_input["known_limitation"] = (
            "Local demo reference only; presentation rights still need confirmation and it is not linguistic certification."
        )

    for old_id, new_id in WATER_EVIDENCE_RENAMES.items():
        if old_id in assets:
            assets[new_id] = assets.pop(old_id)
        if new_id in assets:
            assets[new_id]["sign_mapping"] = ["water"]
            assets[new_id]["workflow_role"] = assets[new_id]["workflow_role"].replace(
                "canonical demo run", "local WATER supporting run"
            ).replace(
                "local WATER demo run", "local WATER supporting run"
            )

    shared_ids = (
        "canonical_sign_content",
        "open_peeps_bust_base",
        "open_peeps_arm_reference",
        "open_peeps_pointing_finger_reference",
        "functional_hand_sheet_jpg",
        "functional_hand_sheet_eps",
    )
    for asset_id in shared_ids:
        assets[asset_id]["sign_mapping"] = list(CANONICAL_LABELS)

    signs = {item["sign_id"]: item for item in registry["signs"]}
    if "more" in signs:
        signs["more"]["landmark_evidence"] = []
        signs["more"]["technical_status"] = "REFERENCE_INPUT_AVAILABLE_NOT_ANALYSED_IN_CANONICAL_RUN"

    signs["water"] = {
        "sign_id": "water",
        "label_en": "WATER",
        "label_es": "AGUA",
        "knowledge_sources": ["canonical_sign_content"],
        "reference_source_urls": [{
            "url": "https://www.openpeeps.com/",
            "role": "Official Open Peeps source and founder-verified CC0 basis",
            "status": "FOUNDER_VERIFIED",
        }],
        "reference_video_input": "input_water",
        "reference_video_hash": "",
        "reference_flashcard": "flashcard_water_reference",
        "functional_sign_illustration": "functional_water",
        "supplementary_hand_sheet": ["functional_hand_sheet_jpg", "functional_hand_sheet_eps"],
        "open_peeps_base": "open_peeps_bust_base",
        "open_peeps_hand_style_reference": "open_peeps_pointing_finger_reference",
        "open_peeps_arm_reference": "open_peeps_arm_reference",
        "open_peeps_reference_status": "AVAILABLE_REFERENCE_ONLY",
        "gemini_demo_video": None,
        "gemini_demo_status": "NOT_AVAILABLE_STATIC_FLOW_ALLOWED",
        "gemini_demo_provider": None,
        "gemini_demo_disclosure": "No pre-generated demo output exists; the registered WATER reference remains available as supporting multi-sign evidence.",
        "contextual_image": None,
        "routine_icon_reference": [],
        "landmark_evidence": ["water_landmark_summary", "water_detection_timeline", "water_validation_summary"],
        "static_visual_candidates": [],
        "reviewed_static_visual": [],
        "flashcard_outputs": [],
        "routine_card_outputs": [],
        "technical_status": "SUPPORTING_REFERENCE_IDENTITY_CONFIRMED_REVIEW_NEEDED",
        "visual_status": "FUNCTIONAL_REFERENCE_AVAILABLE_ARTWORK_NOT_CREATED",
        "printable_status": "BLOCKED",
        "publication_status": "DRAFT_BLOCKED",
        "school_availability": "UNAVAILABLE",
        "rights_or_provenance_status": "MIXED_OPEN_PEEPS_VERIFIED_EXTERNAL_REFERENCES_NEED_CONFIRMATION",
        "known_gaps": [
            "No pre-generated demo output exists; the registered WATER reference remains valid supporting evidence.",
            "No distributable flashcard or routine-card output is approved.",
        ],
    }
    registry["signs"] = [signs[sign_id] for sign_id in CANONICAL_LABELS]
    _sync_visual_candidates(registry)


def refresh_registry(registry: Dict[str, Any]) -> Dict[str, Any]:
    upgrade_prompt_2b_registry(registry)
    pointing_match = find_pointing_reference()
    pointing = registry["assets"][POINTING_ASSET_ID]
    gap_text = "Exact pointing_finger-1.svg is missing at {0}.".format(POINTING_EXPECTED)
    if pointing_match:
        pointing["path"] = Path(os.path.relpath(str(pointing_match), str(REPO_ROOT))).as_posix()
        pointing["licence_or_provenance_status"] = "FOUNDER_VERIFIED_CC0_OFFICIAL_SOURCE"
        pointing["demo_display_allowed"] = True
        pointing["known_limitation"] = "Hand-style reference only; it is not a final pose or sign-mechanics source."
        for sign in registry["signs"]:
            sign["open_peeps_reference_status"] = "AVAILABLE_REFERENCE_ONLY"
            sign["known_gaps"] = [
                gap for gap in sign["known_gaps"]
                if "pointing_finger-1.svg is missing" not in gap
            ]
    else:
        pointing["path"] = POINTING_EXPECTED
        pointing["licence_or_provenance_status"] = "FOUNDER_VERIFIED_CC0_OFFICIAL_SOURCE_FILE_MISSING"
        pointing["demo_display_allowed"] = False
        pointing["known_limitation"] = (
            "BLOCKING GAP: the exact filename is absent. Separate Atoms/body/Pointing Up.svg "
            "is not an approved substitute."
        )
        for sign in registry["signs"]:
            sign["open_peeps_reference_status"] = "BLOCKED_MISSING_EXACT_HAND_STYLE_REFERENCE"
            if gap_text not in sign["known_gaps"]:
                sign["known_gaps"].insert(0, gap_text)

    for asset in registry["assets"].values():
        path = resolve_asset_path(asset["path"])
        exists = path.is_file()
        asset["exists"] = exists
        asset["file_type"] = file_type(path) if exists else None
        asset["byte_size"] = path.stat().st_size if exists else None
        asset["sha256"] = sha256_file(path) if exists else None

    for sign in registry["signs"]:
        input_asset = registry["assets"][sign["reference_video_input"]]
        sign["reference_video_hash"] = input_asset["sha256"] or ""
        demo_id = sign["gemini_demo_video"]
        if demo_id:
            if registry["assets"][demo_id]["exists"]:
                sign["gemini_demo_status"] = "AVAILABLE_PREGENERATED_DEMO_ONLY"
                sign["gemini_demo_disclosure"] = (
                    "Pre-generated demo output; not generated from the current landmark run, "
                    "not the reference input video, and not linguistically certified."
                )
            else:
                sign["gemini_demo_status"] = "OPTIONAL_DEMO_FILE_MISSING_STATIC_FLOW_ALLOWED"
                sign["gemini_demo_disclosure"] = (
                    "The mapped optional pre-generated demo file is absent; the static flow remains valid."
                )
    return registry


def _schema_type_matches(value: Any, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "string":
        return isinstance(value, str)
    if expected == "array":
        return isinstance(value, list)
    if expected == "object":
        return isinstance(value, dict)
    return False


def _resolve_schema_ref(root_schema: Dict[str, Any], reference: str) -> Dict[str, Any]:
    if not reference.startswith("#/"):
        raise RegistryValidationError("Only local JSON Schema references are supported: {0}".format(reference))
    node: Any = root_schema
    for part in reference[2:].split("/"):
        node = node[part.replace("~1", "/").replace("~0", "~")]
    return node


def _validate_schema_node(
    value: Any,
    schema: Dict[str, Any],
    root_schema: Dict[str, Any],
    location: str,
) -> List[str]:
    if "$ref" in schema:
        return _validate_schema_node(value, _resolve_schema_ref(root_schema, schema["$ref"]), root_schema, location)

    if "oneOf" in schema:
        branch_errors = [
            _validate_schema_node(value, branch, root_schema, location)
            for branch in schema["oneOf"]
        ]
        if sum(not errors for errors in branch_errors) != 1:
            return ["{0}: value must match exactly one schema branch".format(location)]
        return []

    errors: List[str] = []
    if "const" in schema and value != schema["const"]:
        errors.append("{0}: expected constant {1!r}".format(location, schema["const"]))
    if "enum" in schema and value not in schema["enum"]:
        errors.append("{0}: value {1!r} is not in the allowed enum".format(location, value))

    expected_types = schema.get("type")
    if expected_types:
        if isinstance(expected_types, str):
            expected_types = [expected_types]
        if not any(_schema_type_matches(value, expected) for expected in expected_types):
            errors.append("{0}: expected type {1}".format(location, " or ".join(expected_types)))
            return errors

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append("{0}: string is shorter than minLength".format(location))
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            errors.append("{0}: string does not match {1}".format(location, schema["pattern"]))
        if schema.get("format") == "uri":
            parsed = urlparse(value)
            if not parsed.scheme or not parsed.netloc:
                errors.append("{0}: value is not an absolute URI".format(location))

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append("{0}: array has fewer than minItems entries".format(location))
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append("{0}: array has more than maxItems entries".format(location))
        if schema.get("uniqueItems"):
            serialized = [json.dumps(item, sort_keys=True) for item in value]
            if len(serialized) != len(set(serialized)):
                errors.append("{0}: array entries must be unique".format(location))
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                errors.extend(_validate_schema_node(item, item_schema, root_schema, "{0}[{1}]".format(location, index)))

    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append("{0}: missing required property {1}".format(location, key))
        if len(value) < schema.get("minProperties", 0):
            errors.append("{0}: object has fewer than minProperties entries".format(location))
        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        for key, item in value.items():
            child_location = "{0}.{1}".format(location, key)
            if key in properties:
                errors.extend(_validate_schema_node(item, properties[key], root_schema, child_location))
            elif additional is False:
                errors.append("{0}: additional property is not allowed".format(child_location))
            elif isinstance(additional, dict):
                errors.extend(_validate_schema_node(item, additional, root_schema, child_location))
    return errors


def validate_against_schema(registry: Dict[str, Any], schema: Dict[str, Any]) -> None:
    errors = _validate_schema_node(registry, schema, schema, "registry")
    if errors:
        raise RegistryValidationError("JSON Schema validation failed:\n- " + "\n- ".join(errors))


def validate_registry(registry: Dict[str, Any], schema: Optional[Dict[str, Any]] = None) -> None:
    if schema is None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validate_against_schema(registry, schema)

    errors: List[str] = []
    expected_ids = list(CANONICAL_LABELS)
    if registry["canonical_sign_ids"] != expected_ids:
        errors.append("canonical_sign_ids must be ordered exactly as {0}".format(expected_ids))
    if set(registry["asset_classes"]) != ASSET_CLASSES:
        errors.append("asset_classes must contain exactly the six allowed classes")

    signs_by_id = {sign["sign_id"]: sign for sign in registry["signs"]}
    if set(signs_by_id) != set(CANONICAL_LABELS) or len(signs_by_id) != len(registry["signs"]):
        errors.append("signs must contain each canonical sign exactly once")

    assets = registry["assets"]
    all_paths: Dict[str, str] = {}
    for asset_id, asset in assets.items():
        if Path(asset["path"]).is_absolute():
            errors.append("{0} exposes an absolute path".format(asset_id))
        try:
            resolve_asset_path(asset["path"])
        except RegistryValidationError as exc:
            errors.append(str(exc))
        prior = all_paths.get(asset["path"])
        if prior:
            errors.append("Asset path is registered twice: {0} and {1}".format(prior, asset_id))
        all_paths[asset["path"]] = asset_id
        if asset["asset_class"] not in ASSET_CLASSES:
            errors.append("{0} has invalid asset_class".format(asset_id))

    sign_specific_paths: Dict[str, Tuple[str, str]] = {}
    actual_mappings: Dict[str, set] = {asset_id: set() for asset_id in assets}
    for sign_id, sign in signs_by_id.items():
        expected_en, expected_es = CANONICAL_LABELS[sign_id]
        if (sign["label_en"], sign["label_es"]) != (expected_en, expected_es):
            errors.append("{0} has incorrect EN/ES labels".format(sign_id))

        for field in ASSET_REFERENCE_FIELDS:
            for asset_id in _iter_asset_ids(sign[field]):
                if asset_id not in assets:
                    errors.append("{0}.{1} references unknown asset {2}".format(sign_id, field, asset_id))
                    continue
                if sign_id not in assets[asset_id]["sign_mapping"]:
                    errors.append("{0} is missing from {1}.sign_mapping".format(sign_id, asset_id))
                actual_mappings[asset_id].add(sign_id)

        for field in REQUIRED_EXISTING_FIELDS:
            asset_id = sign[field]
            if asset_id in assets and not assets[asset_id]["exists"]:
                errors.append("Required asset is missing for {0}.{1}: {2}".format(sign_id, field, assets[asset_id]["path"]))
        for asset_id in sign["supplementary_hand_sheet"] + sign["routine_icon_reference"]:
            if asset_id in assets and not assets[asset_id]["exists"]:
                errors.append("Required supplementary asset is missing for {0}: {1}".format(sign_id, assets[asset_id]["path"]))

        input_asset = assets.get(sign["reference_video_input"], {})
        if input_asset:
            if "/video_input/" not in input_asset["path"]:
                errors.append("{0} reference input is not in video_input".format(sign_id))
            if input_asset["asset_class"] != "FOUNDER_PROVIDED_REFERENCE":
                errors.append("{0} reference input has the wrong asset class".format(sign_id))
            if input_asset["sha256"] != sign["reference_video_hash"]:
                errors.append("{0} reference_video_hash does not match its input".format(sign_id))

        reference_flashcard_id = sign["reference_flashcard"]
        reference_flashcard = assets.get(reference_flashcard_id, {})
        if reference_flashcard.get("printable_allowed") is not False:
            errors.append("{0} reference flashcard must be reference-only".format(sign_id))
        distributable_ids = set(sign["flashcard_outputs"] + sign["routine_card_outputs"])
        if reference_flashcard_id in distributable_ids:
            errors.append("{0} maps a reference flashcard as a distributable output".format(sign_id))

        for field in SIGN_SPECIFIC_FIELDS:
            for asset_id in _iter_asset_ids(sign[field]):
                if asset_id not in assets:
                    continue
                path = assets[asset_id]["path"]
                previous = sign_specific_paths.get(path)
                if previous and previous != (sign_id, field):
                    errors.append(
                        "Duplicate sign-specific file mapping for {0}.{1} and {2}.{3}: {4}".format(
                            previous[0], previous[1], sign_id, field, path
                        )
                    )
                sign_specific_paths[path] = (sign_id, field)

        expected_demo = EXPECTED_DEMOS.get(sign_id)
        if sign["gemini_demo_video"] != expected_demo:
            errors.append("{0} has incorrect Gemini demo mapping".format(sign_id))
        if expected_demo:
            demo = assets.get(expected_demo, {})
            if demo.get("asset_class") != "PREGENERATED_DEMO_OUTPUT":
                errors.append("{0} Gemini demo has the wrong asset class".format(sign_id))
            if demo.get("path") == input_asset.get("path") or demo.get("sha256") == input_asset.get("sha256"):
                errors.append("{0} maps a demo output as its reference input".format(sign_id))
            expected_status = (
                "AVAILABLE_PREGENERATED_DEMO_ONLY"
                if demo.get("exists")
                else "OPTIONAL_DEMO_FILE_MISSING_STATIC_FLOW_ALLOWED"
            )
            if sign["gemini_demo_status"] != expected_status:
                errors.append("{0} Gemini demo availability status is stale".format(sign_id))
        elif sign["gemini_demo_status"] != "NOT_AVAILABLE_STATIC_FLOW_ALLOWED":
            errors.append("{0} missing demo must explicitly allow the static flow".format(sign_id))

    pointing = assets.get(POINTING_ASSET_ID, {})
    pointing_match = find_pointing_reference()
    if pointing_match is None:
        if pointing.get("exists"):
            errors.append("Missing pointing reference cannot be marked as existing")
        if pointing.get("path") != POINTING_EXPECTED:
            errors.append("Missing pointing reference must record exact expected destination {0}".format(POINTING_EXPECTED))
        for sign in registry["signs"]:
            if sign["open_peeps_reference_status"] != "BLOCKED_MISSING_EXACT_HAND_STYLE_REFERENCE":
                errors.append("{0} must expose the blocking Open Peeps reference gap".format(sign["sign_id"]))
            if not any(POINTING_EXPECTED in gap for gap in sign["known_gaps"]):
                errors.append("{0} must report the exact pointing reference destination".format(sign["sign_id"]))
    elif not pointing.get("exists"):
        errors.append("Found pointing_finger-1.svg must be marked as existing")

    for asset_id, asset in assets.items():
        if actual_mappings[asset_id] != set(asset["sign_mapping"]):
            errors.append(
                "{0}.sign_mapping does not match package references: expected {1}".format(
                    asset_id, sorted(actual_mappings[asset_id])
                )
            )

    if errors:
        raise RegistryValidationError("Registry validation failed:\n- " + "\n- ".join(errors))


def render_report(registry: Dict[str, Any]) -> str:
    missing = [asset_id for asset_id, asset in registry["assets"].items() if not asset["exists"]]
    lines = [
        "# Kinder Signs Asset Inventory",
        "",
        "Generated deterministically by `tools/build_sign_asset_registry.py` from the canonical registry.",
        "External source files are inspected in place and are never copied into this repository.",
        "",
        "## Validation summary",
        "",
        "- Canonical signs: {0}".format(", ".join(registry["canonical_sign_ids"])),
        "- Registered assets: {0}".format(len(registry["assets"])),
        "- Missing registered assets: {0}".format(len(missing)),
        "- Product-blocking reference gap: `{0}` is not present.".format(POINTING_EXPECTED) if POINTING_ASSET_ID in missing else "- Product-blocking reference gap: none.",
        "- Registry validation: PASS (a documented product gap is not a malformed registry).",
        "",
        "## Sign packages",
        "",
        "| Sign | Labels | Input | Gemini demo | Technical | Visual | Printable | School |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for sign in registry["signs"]:
        demo = sign["gemini_demo_status"]
        lines.append(
            "| {sign_id} | {label_en} / {label_es} | present | {demo} | {technical} | {visual} | {printable} | {school} |".format(
                sign_id=sign["sign_id"], label_en=sign["label_en"], label_es=sign["label_es"], demo=demo,
                technical=sign["technical_status"], visual=sign["visual_status"], printable=sign["printable_status"], school=sign["school_availability"]
            )
        )

    lines.extend([
        "",
        "## File inventory",
        "",
        "| Asset ID | Class | Sign mapping | Exists | Bytes | SHA-256 | Relative path |",
        "| --- | --- | --- | --- | ---: | --- | --- |",
    ])
    for asset_id, asset in registry["assets"].items():
        digest = asset["sha256"] if asset["sha256"] else "—"
        size = str(asset["byte_size"]) if asset["byte_size"] is not None else "—"
        mappings = ", ".join(asset["sign_mapping"]) or "shared"
        lines.append(
            "| `{0}` | {1} | {2} | {3} | {4} | `{5}` | `{6}` |".format(
                asset_id, asset["asset_class"], mappings, "yes" if asset["exists"] else "no", size, digest, asset["path"]
            )
        )

    lines.extend([
        "",
        "## Guardrails",
        "",
        "- Open Peeps defines character identity only; functional references define sign mechanics.",
        "- The exact registered `pointing_finger-1.svg` atom defines hand-style grammar only; `Separate Atoms/body/Pointing Up.svg` is not a substitute.",
        "- Gemini FX files are pre-generated demo outputs, not reference inputs, current-run products, or linguistic certification.",
        "- Reference flashcards and vendor routine icons cannot enter printable outputs.",
        "- EAT, SLEEP and WATER intentionally have no Gemini FX output and remain eligible for the local static workflow.",
        "",
    ])
    return "\n".join(lines)


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build(write: bool = False) -> Dict[str, Any]:
    original = load_json(REGISTRY_PATH)
    registry = refresh_registry(copy.deepcopy(original))
    schema = load_json(SCHEMA_PATH)
    validate_registry(registry, schema)
    report = render_report(registry)

    if write:
        REGISTRY_PATH.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        REPORT_PATH.write_text(report, encoding="utf-8")
    else:
        expected_registry = json.dumps(registry, indent=2, ensure_ascii=False) + "\n"
        if REGISTRY_PATH.read_text(encoding="utf-8") != expected_registry:
            raise RegistryValidationError("Registry metadata is stale; run with --write")
        if not REPORT_PATH.is_file() or REPORT_PATH.read_text(encoding="utf-8") != report:
            raise RegistryValidationError("Inventory report is stale; run with --write")
    return registry


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Refresh metadata and write the registry and inventory report")
    parser.add_argument("--check", action="store_true", help="Validate committed metadata without writing (the default)")
    args = parser.parse_args(argv)
    if args.write and args.check:
        parser.error("choose either --write or --check")
    return args


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    try:
        registry = build(write=args.write)
    except (OSError, KeyError, json.JSONDecodeError, RegistryValidationError) as exc:
        print("ERROR: {0}".format(exc), file=sys.stderr)
        return 1
    pointing_exists = registry["assets"][POINTING_ASSET_ID]["exists"]
    print("Registry valid: {0} signs, {1} assets.".format(len(registry["signs"]), len(registry["assets"])))
    if not pointing_exists:
        print("BLOCKING REGISTRY GAP: expected {0}".format(POINTING_EXPECTED))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
