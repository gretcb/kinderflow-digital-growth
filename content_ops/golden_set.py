"""Evaluate the five-sign Kinder Signs engineering/product regression set."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .policy import evaluate_package
from .provenance import build_publication_package, sha256_file


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTENT_ROOT = Path(__file__).resolve().parent
SIGN_DATA_PATH = REPO_ROOT / "prototype/data/signs.json"
SIGN_ORDER = ["more", "eat", "water", "all_done", "help"]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_domain_package(sign_id: str) -> dict[str, Any]:
    source = load_json(SIGN_DATA_PATH)
    sign_data = next(sign for sign in source["signs"] if sign["id"] == f"ks-{sign_id.replace('_', '-')}")
    manifest = load_json(CONTENT_ROOT / f"signs/{sign_id}/manifest.json")
    return {
        "sign": {
            "sign_id": sign_id,
            "display_name": sign_data["display_name"],
            "spanish_label": sign_data["spanish_label"],
            "routine": sign_data["routine"],
            "source_reference": manifest["source_reference"],
        },
        "sign_version": {
            "version": manifest["version"],
            "created_at": manifest["created_at"],
            "source_reference": manifest["source_reference"],
            "technical_evidence_reference": manifest["technical_evidence_reference"],
            "sign_data_sha256": manifest["sign_data_sha256"],
        },
        "technical": {
            "state": manifest["technical_state"],
            "evidence_reference": manifest["technical_evidence_reference"],
            "evidence_sha256": manifest["technical_evidence_sha256"],
            "evidence_scope": manifest.get("technical_evidence_scope"),
        },
        "content_package": {
            "family_guidance": sign_data["short_family_guidance"],
            "try_it_during": sign_data["try_it_during"],
            "language": "bilingual",
            "generation_method": manifest["generation_method"],
            "content_version": manifest["content_version"],
            "state": manifest["content_state"],
            "langsmith_evaluation": manifest["langsmith_evaluation"],
        },
        "visual_package": {
            "visual_version": manifest["visual_version"],
            "character_asset": manifest["character_asset"],
            "hand_pose_asset": manifest["hand_pose_asset"],
            "illustration_status": manifest["illustration_status"],
            "hand_review_status": manifest["hand_review_status"],
            "state": manifest["visual_state"],
        },
        "review": {
            "reviewer_type": manifest["reviewer_type"],
            "review_status": manifest["review_status"],
            "reviewed_at": manifest["reviewed_at"],
            "notes": manifest["review_notes"],
        },
        "publication_package": {
            "sign_version": manifest["version"],
            "content_version": manifest["content_version"],
            "visual_version": manifest["visual_version"],
            "publication_status": manifest["publication_status"],
            "library_readiness": manifest["library_readiness"],
            "published_version": manifest["published_version"],
            "published_at": manifest["published_at"],
        },
    }


def human_status(value: str | None) -> str:
    if not value:
        return "Pending"
    return value.replace("_", " ").title()


def verify_manifest_provenance(manifest: dict[str, Any]) -> dict[str, Any]:
    checks = []
    sign_data_path = REPO_ROOT / manifest["sign_data_reference"]
    checks.append({
        "artifact": "sign_data",
        "reference": manifest["sign_data_reference"],
        "matched": sign_data_path.is_file() and sha256_file(sign_data_path) == manifest["sign_data_sha256"],
    })
    evidence_reference = manifest.get("technical_evidence_reference")
    if evidence_reference:
        evidence_path = REPO_ROOT / evidence_reference
        checks.append({
            "artifact": "technical_evidence",
            "reference": evidence_reference,
            "matched": evidence_path.is_file() and sha256_file(evidence_path) == manifest.get("technical_evidence_sha256"),
        })
    return {"passed": all(check["matched"] for check in checks), "checks": checks}


def evaluate_golden_set() -> dict[str, Any]:
    results = []
    for sign_id in SIGN_ORDER:
        package = build_domain_package(sign_id)
        gate = evaluate_package(package)
        manifest = load_json(CONTENT_ROOT / f"signs/{sign_id}/manifest.json")
        provenance = verify_manifest_provenance(manifest)
        package["quality_gate"] = gate
        results.append({
            "sign_id": sign_id,
            "display_name": package["sign"]["display_name"],
            "schema": "PASS",
            "provenance": "PASS" if provenance["passed"] else "FAIL",
            "provenance_checks": provenance["checks"],
            "source": human_status(manifest["source_status"]),
            "source_reference": manifest["source_reference"],
            "technical": human_status(package["technical"]["state"]),
            "content": human_status(package["content_package"]["state"]),
            "artwork": human_status(package["visual_package"]["illustration_status"]),
            "hand_review": human_status(package["visual_package"]["hand_review_status"]),
            "quality_gate": "Passed" if gate["passed"] else "Blocked",
            "human_review": human_status(package["review"]["review_status"]),
            "library": human_status(package["publication_package"]["library_readiness"]),
            "llm": "Assisted" if package["content_package"]["generation_method"] == "llm_assisted" else "Not used",
            "publication": human_status(package["publication_package"]["publication_status"]),
            "blocking_reasons": gate["blocking_reasons"],
        })
        if sign_id == "more":
            destination = REPO_ROOT / "build/publication/more/v1"
            build_publication_package(package, destination)
    return {
        "schema_version": "1.0",
        "set_name": "kinder_signs_golden_mvp_v1",
        "purpose": "Engineering and product regression; not linguistic sign certification.",
        "results": results,
    }


def main() -> int:
    report = evaluate_golden_set()
    report_path = CONTENT_ROOT / "reports/golden_set_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    report_path.write_text(rendered, encoding="utf-8")
    prototype_path = REPO_ROOT / "prototype/data/content_operations.json"
    prototype_path.write_text(rendered, encoding="utf-8")
    for result in report["results"]:
        print(result["display_name"])
        print(f"  schema: {result['schema']}")
        print(f"  content: {result['content']}")
        print(f"  visual: {result['artwork']}")
        print(f"  publication: {result['library']}")
    print(f"JSON report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
