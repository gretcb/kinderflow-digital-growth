"""Local provenance, package building, and append-only event helpers."""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for chunk in iter(lambda: source.read(64 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_value(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def append_event(log_path: str | Path, event: dict[str, Any]) -> bool:
    """Append one unique event. Returns False if event_id already exists."""
    required = {"event_id", "timestamp", "sign_id", "version", "event_type", "actor_type", "metadata"}
    missing = required.difference(event)
    if missing:
        raise ValueError("Audit event missing: " + ", ".join(sorted(missing)))
    if event["actor_type"] not in {"system", "human", "llm", "workflow"}:
        raise ValueError("Unsupported audit actor_type")
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line and json.loads(line).get("event_id") == event["event_id"]:
                return False
    with path.open("a", encoding="utf-8") as destination:
        destination.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    return True


def new_event(sign_id: str, version: str, event_type: str, actor_type: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "event_id": f"evt_{uuid.uuid4().hex}",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "sign_id": sign_id,
        "version": version,
        "event_type": event_type,
        "actor_type": actor_type,
        "metadata": metadata or {},
    }


def build_publication_package(package: dict[str, Any], destination: str | Path) -> dict[str, Any]:
    """Write a deterministic, idempotent structured package without copying media."""
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    documents = {
        "content.json": package["content_package"],
        "visual.json": package["visual_package"],
        "review.json": package["review"],
        "library_item.json": package["publication_package"],
    }
    input_hash = sha256_value({"sign": package["sign"], "sign_version": package["sign_version"], **documents})
    manifest = {
        "schema_version": "1.0",
        "package_id": f"pkg_{package['sign']['sign_id']}_{package['sign_version']['version']}_{input_hash[:12]}",
        "sign_id": package["sign"]["sign_id"],
        "sign_version": package["sign_version"]["version"],
        "source_reference": package["sign"]["source_reference"],
        "technical_evidence_reference": package["technical"].get("evidence_reference"),
        "technical_evidence_sha256": package["technical"].get("evidence_sha256"),
        "sign_data_sha256": package["sign_version"].get("sign_data_sha256"),
        "input_sha256": input_hash,
        "llm_assistance_used": package["content_package"].get("generation_method") == "llm_assisted",
        "deterministic_gates_passed": package.get("quality_gate", {}).get("passed", False),
        "langsmith_evaluation": package["content_package"].get("langsmith_evaluation", "not_applicable"),
        "human_review_status": package["review"].get("review_status"),
        "published_version": package["publication_package"].get("published_version"),
        "published_at": package["publication_package"].get("published_at"),
        "document_hashes": {name: sha256_value(value) for name, value in documents.items()},
    }
    documents["manifest.json"] = manifest
    for name, value in documents.items():
        path = destination / name
        rendered = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        if not path.exists() or path.read_text(encoding="utf-8") != rendered:
            path.write_text(rendered, encoding="utf-8")
    return manifest
