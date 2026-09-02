"""Local Content Pack service built on the shared content-operations contract."""

from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
import time
import uuid
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
SIGN_DATA_PATH = REPO_ROOT / "prototype/data/signs.json"
CONTENT_RUNS_ROOT = REPO_ROOT / "mvp/runs/content_packs"
PROMPT_VERSION = "kinder_signs_content_pack_v1"
DEFAULT_MODEL = "gpt-5-mini"
RUN_ID_PATTERN = re.compile(r"^content_[A-Za-z0-9_-]+$")
LANGSMITH_DIMENSIONS = [
    "clarity",
    "brevity",
    "consistency_with_supplied_context",
    "family_friendly_language",
    "unsupported_claim_risk",
    "hallucination_against_structured_source",
]


class ContentPackError(ValueError):
    """Controlled Content Pack error safe to return to the local operator."""

    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.status = status


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_local_environment() -> None:
    """Load only approved provider settings from the ignored local .env file."""
    env_path = REPO_ROOT / ".env"
    if not env_path.is_file():
        return
    allowed = {"OPENAI_API_KEY", "OPENAI_MODEL", "LANGSMITH_API_KEY", "LANGSMITH_PROJECT", "LANGSMITH_TRACING"}
    for raw_line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        name, value = name.strip(), value.strip().strip('"').strip("'")
        if name in allowed and value:
            os.environ.setdefault(name, value)


def load_signs() -> list[dict[str, Any]]:
    try:
        payload = json.loads(SIGN_DATA_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ContentPackError("The structured sign library could not be loaded.", 500) from error
    signs = payload.get("signs") if isinstance(payload, dict) else None
    if not isinstance(signs, list):
        raise ContentPackError("The structured sign library is invalid.", 500)
    return signs


def find_sign(sign_id: str) -> dict[str, Any]:
    for sign in load_signs():
        if sign.get("sign_id") == sign_id:
            return sign
    raise ContentPackError("The selected sign does not exist.", 404)


def _content_engine():
    from content_ops.content_engine import (
        approve_content_locally,
        build_dry_run_candidate,
        content_input_from_sign,
        prepare_flashcard_handoff,
        validate_content_input,
        validate_generated_output,
    )

    return {
        "approve": approve_content_locally,
        "build": build_dry_run_candidate,
        "input": content_input_from_sign,
        "handoff": prepare_flashcard_handoff,
        "validate_input": validate_content_input,
        "validate_output": validate_generated_output,
    }


def build_content_request(sign_id: str, language: str = "bilingual") -> dict[str, Any]:
    engine = _content_engine()
    return engine["input"](find_sign(sign_id), language)


def validate_canonical_input(payload: Any) -> tuple[dict[str, Any], dict[str, Any]]:
    engine = _content_engine()
    result = engine["validate_input"](payload)
    if not result["passed"]:
        raise ContentPackError("Content Pack input failed validation: " + " ".join(result["blocking_reasons"]))
    sign = find_sign(payload["sign_id"])
    expected = engine["input"](sign, payload["language"])
    if payload != expected:
        raise ContentPackError("Content Pack input does not match the approved structured sign source.")
    return sign, expected


def new_run_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    return f"content_{stamp}_{uuid.uuid4().hex[:8]}"


def run_directory(run_id: str) -> Path:
    if not RUN_ID_PATTERN.fullmatch(run_id):
        raise ContentPackError("Content Pack run was not found.", 404)
    candidate = (CONTENT_RUNS_ROOT / run_id).resolve()
    if CONTENT_RUNS_ROOT.resolve() not in candidate.parents:
        raise ContentPackError("Content Pack run was not found.", 404)
    return candidate


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_content_run(run_id: str) -> dict[str, Any]:
    path = run_directory(run_id) / "run.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ContentPackError("Content Pack run was not found.", 404) from error
    if not isinstance(payload, dict):
        raise ContentPackError("Content Pack run is invalid.", 500)
    return payload


def build_prompt(source_input: dict[str, Any], run_id: str) -> str:
    template = {
        "schema_version": "1.0",
        "run_id": run_id,
        "sign_id": source_input["sign_id"],
        "source_context_id": source_input["approved_context"]["context_id"],
        "source_reference": source_input["approved_context"]["context_id"],
        "prompt_version": PROMPT_VERSION,
        "generation_method": "llm_assisted",
        "generation_mode": "LIVE",
        "language": source_input["language"],
        "family_guidance": {"en": "...", "es": "..."},
        "try_it_during": {"en": "...", "es": "..."},
        "routine_context": source_input["routine"],
        "teacher_message": {"en": "...", "es": "..."},
        "family_message": {"en": "...", "es": "..."},
        "flashcard_copy": {"primary_label": source_input["display_name"], "secondary_label": source_input["spanish_label"]},
        "review_status": "READY_FOR_REVIEW",
        "requires_human_review": True,
        "automatic_publication": False,
    }
    return (
        "You prepare short Kinder Signs school and family wording from an approved structured source.\n"
        "Return valid JSON only, with exactly the keys and fixed metadata in the output template.\n"
        "Use only the supplied source. Write concise English and Spanish variants.\n"
        "Do not add hand shape, finger, palm, wrist, direction, contact, movement steps, sign correctness, diagnosis, clinical advice, therapy, cure, or developmental acceleration claims.\n"
        "Do not approve or publish content. Human review must remain required.\n\n"
        f"STRUCTURED SOURCE:\n{json.dumps(source_input, ensure_ascii=False, indent=2)}\n\n"
        f"OUTPUT TEMPLATE:\n{json.dumps(template, ensure_ascii=False, indent=2)}"
    )


def _live_provider(prompt: str, model: str) -> tuple[str, dict[str, Any], bool]:
    try:
        from openai import OpenAI
    except ImportError as error:
        raise ContentPackError("Live AI dependencies are unavailable. The run can use DRY-RUN instead.", 503) from error

    client: Any = OpenAI()
    langsmith_traced = False
    if os.environ.get("LANGSMITH_API_KEY"):
        try:
            from langsmith.wrappers import wrap_openai

            os.environ.setdefault("LANGSMITH_TRACING", "true")
            os.environ.setdefault("LANGSMITH_PROJECT", "kinderflow-kinder-signs-workflow")
            client = wrap_openai(client)
            langsmith_traced = True
        except ImportError:
            langsmith_traced = False

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content
    if not content:
        raise ContentPackError("The live model returned an empty Content Pack.", 502)
    usage = getattr(response, "usage", None)
    usage_data = {
        "input_tokens": getattr(usage, "prompt_tokens", None),
        "output_tokens": getattr(usage, "completion_tokens", None),
        "total_tokens": getattr(usage, "total_tokens", None),
    }
    return content, usage_data, langsmith_traced


def _live_dependency_available() -> bool:
    return importlib.util.find_spec("openai") is not None


def _langsmith_status(generation_method: str, generation_mode: str, traced: bool) -> dict[str, Any]:
    if generation_method == "human":
        return {"mode": "NOT_APPLICABLE", "trace_status": "NOT_SENT", "evaluation_status": "NOT_APPLICABLE", "dimensions": []}
    if generation_mode == "DRY_RUN":
        return {"mode": "DRY_RUN", "trace_status": "NOT_SENT", "evaluation_status": "DRY_RUN_ONLY", "dimensions": LANGSMITH_DIMENSIONS}
    if traced:
        return {"mode": "LIVE", "trace_status": "SENT", "evaluation_status": "TRACE_RECORDED_EVALUATION_PENDING", "dimensions": LANGSMITH_DIMENSIONS}
    return {"mode": "DRY_RUN", "trace_status": "NOT_SENT", "evaluation_status": "LIVE_TRACE_UNAVAILABLE", "dimensions": LANGSMITH_DIMENSIONS}


def generate_content_pack(
    request: Any,
    live_provider: Callable[[str, str], tuple[str, dict[str, Any], bool]] | None = None,
) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ContentPackError("Request must be a JSON object.")
    if request.get("operation") != "GENERATE_CONTENT_PACK":
        raise ContentPackError("Unsupported content operation.")
    method = request.get("generation_method")
    if method not in {"human", "llm_assisted"}:
        raise ContentPackError("generation_method must be human or llm_assisted.")
    sign, source_input = validate_canonical_input(request.get("input"))

    load_local_environment()
    run_id = new_run_id()
    run_dir = run_directory(run_id)
    started_at = utc_now()
    started_clock = time.perf_counter()
    run_record: dict[str, Any] = {
        "schema_version": "1.0",
        "run_id": run_id,
        "operation": "GENERATE_CONTENT_PACK",
        "state": "RUNNING",
        "started_at": started_at,
        "completed_at": None,
        "source": {"sign_id": sign["sign_id"], "context_id": source_input["approved_context"]["context_id"]},
        "generation": {"method": method, "mode": "WAITING", "model_configuration": None, "prompt_version": PROMPT_VERSION, "latency_ms": None, "token_usage": None},
        "quality_gate": None,
        "langsmith": None,
        "review": {"status": "PENDING", "actor_type": None, "reviewed_content_version": None},
        "automatic_publication": False,
        "content_pack": None,
        "flashcard_handoff": None,
        "error": None,
    }
    write_json(run_dir / "input.json", source_input)
    write_json(run_dir / "run.json", run_record)

    engine = _content_engine()
    provider = live_provider or _live_provider
    traced = False
    usage: dict[str, Any] | None = None
    fallback_warning: str | None = None
    model = os.environ.get("OPENAI_MODEL", DEFAULT_MODEL)
    try:
        if method == "human":
            candidate = engine["build"](sign, "human", run_id, source_input["language"])
            generation_mode = "NOT_APPLICABLE"
            model_used = None
        elif os.environ.get("OPENAI_API_KEY") and (live_provider is not None or _live_dependency_available()):
            generated, usage, traced = provider(build_prompt(source_input, run_id), model)
            candidate = json.loads(generated) if isinstance(generated, str) else deepcopy(generated)
            generation_mode = "LIVE"
            model_used = model
        else:
            candidate = engine["build"](sign, "llm_assisted", run_id, source_input["language"])
            generation_mode = "DRY_RUN"
            model_used = None
            if os.environ.get("OPENAI_API_KEY"):
                fallback_warning = "Live provider dependency unavailable; the isolated run used DRY-RUN."
    except json.JSONDecodeError:
        candidate = None
        generation_mode = "LIVE"
        model_used = model
        run_record["error"] = {"code": "malformed_model_output", "message": "The model returned malformed JSON."}
    except ContentPackError as error:
        run_record.update({"state": "FAILED", "completed_at": utc_now(), "error": {"code": "provider_error", "message": str(error)}})
        write_json(run_dir / "run.json", run_record)
        raise
    except Exception as error:
        run_record.update({"state": "FAILED", "completed_at": utc_now(), "error": {"code": "provider_error", "message": "Live Content Pack generation could not be completed."}})
        write_json(run_dir / "run.json", run_record)
        raise ContentPackError("Live Content Pack generation could not be completed.", 502) from error

    gate = {"passed": False, "failed_checks": [{"check": "valid_json", "detail": "The model returned malformed JSON."}], "warnings": [], "blocking_reasons": ["The model returned malformed JSON."]}
    if candidate is not None:
        candidate, gate = engine["validate_output"](candidate, source_input)
    if fallback_warning:
        gate["warnings"].append(fallback_warning)

    completed_at = utc_now()
    latency_ms = round((time.perf_counter() - started_clock) * 1000)
    langsmith = _langsmith_status(method, generation_mode, traced)
    run_record.update({
        "state": "READY_FOR_REVIEW" if gate["passed"] else "REJECTED",
        "completed_at": completed_at,
        "generation": {"method": method, "mode": generation_mode, "model_configuration": model_used, "prompt_version": PROMPT_VERSION, "latency_ms": latency_ms, "token_usage": usage},
        "quality_gate": gate,
        "langsmith": langsmith,
        "content_pack": candidate,
    })
    if not gate["passed"] and run_record["error"] is None:
        run_record["error"] = {"code": "quality_gate_failed", "message": "The Content Pack did not pass deterministic checks."}
    if candidate is not None:
        write_json(run_dir / "candidate.json", candidate)
    write_json(run_dir / "run.json", run_record)
    return run_record


def approve_content_pack(run_id: str) -> dict[str, Any]:
    run = load_content_run(run_id)
    if run.get("review", {}).get("status") == "APPROVED":
        return run
    if run.get("state") != "READY_FOR_REVIEW" or not run.get("quality_gate", {}).get("passed") or not isinstance(run.get("content_pack"), dict):
        raise ContentPackError("Only a Content Pack that passed deterministic checks can be approved.", 409)
    engine = _content_engine()
    approved = engine["approve"](run["content_pack"], "explicit_demo_approval")
    version = f"reviewed_{run_id}_v1"
    approved["human_review"].update({"actor_type": "human_reviewer", "reviewed_content_version": version})
    handoff = engine["handoff"](approved)
    run["state"] = "APPROVED_LOCALLY"
    run["content_pack"] = approved
    run["review"] = {"status": "APPROVED", "actor_type": "human_reviewer", "reviewed_content_version": version, "reviewed_at": utc_now()}
    run["flashcard_handoff"] = handoff
    write_json(run_directory(run_id) / "reviewed.json", approved)
    write_json(run_directory(run_id) / "run.json", run)
    return run


def request_content_changes(run_id: str) -> dict[str, Any]:
    run = load_content_run(run_id)
    if run.get("state") not in {"READY_FOR_REVIEW", "APPROVED_LOCALLY"}:
        raise ContentPackError("This Content Pack is not available for review changes.", 409)
    run["state"] = "CHANGES_REQUESTED"
    run["review"] = {"status": "CHANGES_REQUESTED", "actor_type": "human_reviewer", "reviewed_content_version": None, "reviewed_at": utc_now()}
    run["flashcard_handoff"] = None
    write_json(run_directory(run_id) / "run.json", run)
    return run


def restore_human_copy(run_id: str) -> dict[str, Any]:
    existing = load_content_run(run_id)
    source = json.loads((run_directory(run_id) / "input.json").read_text(encoding="utf-8"))
    return generate_content_pack({"operation": "GENERATE_CONTENT_PACK", "generation_method": "human", "input": source})
