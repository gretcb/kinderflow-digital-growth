"""Offline-first LangSmith trace harness for the Kinder Signs LLM step."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

try:
    from .quality_gate import evaluate_quality_gate, load_json_object
except ImportError:
    from quality_gate import evaluate_quality_gate, load_json_object


WORKFLOW_DIR = Path(__file__).resolve().parent
DATASET_NAME = "kinder_signs_microlearning_v1"
PROJECT_NAME = "kinderflow-kinder-signs-workflow"
DEFAULT_MODEL = "gpt-5-mini"

OUTPUT_SCHEMA_TEXT = """{
  "sign_id": "...",
  "source_id": "...",
  "review_status": "draft_requires_professional_approval",
  "requires_human_review": true,
  "parent_title": "...",
  "short_explanation": "...",
  "when_to_use": ["...", "..."],
  "practice_tip": "...",
  "school_home_connection": "...",
  "motion_note": "...",
  "boundaries": ["...", "..."]
}"""


def build_prompt(sign_input: dict[str, Any], cv_summary: dict[str, Any]) -> str:
    return f"""You are KinderFlow's family-facing content transformation assistant.

Transform only the approved sign content below into a concise family-facing draft.
The approved sign object is the content source of truth.
The CV motion summary is technical context only. It does not establish movement
fidelity, professional sign correctness, linguistic correctness, or developmental benefit.

Rules:
1. Return valid JSON only, with exactly the requested schema.
2. Preserve sign_id and source_id exactly.
3. Set review_status to "draft_requires_professional_approval".
4. Set requires_human_review to true.
5. Do not invent movement details.
6. If movement_notes is present, copy it verbatim into motion_note. If it is empty,
   set motion_note exactly to: "Movement instructions are unavailable in the approved
   input; use an approved reference only after professional review."
7. Do not claim language acceleration or other unsupported developmental benefit.
8. Do not diagnose, describe treatment, or replace professional advice.
9. Do not mention ASL or LSE unless explicitly supplied as approved content.
10. Use the CV motion summary only for bounded technical context, never as evidence
    that the sign is correct.
11. Keep the language clear, practical, and appropriate for families.
12. Preserve the approved school-home connection.

Required output schema:
{OUTPUT_SCHEMA_TEXT}

APPROVED SIGN OBJECT:
{json.dumps(sign_input, indent=2)}

CV MOTION SUMMARY:
{json.dumps(cv_summary, indent=2)}
"""


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def dry_run() -> int:
    sign_input = load_json_object(WORKFLOW_DIR / "sample_sign_input.json")
    cv_summary = load_json_object(WORKFLOW_DIR / "sample_cv_motion_summary.json")
    sample_output = load_json_object(WORKFLOW_DIR / "sample_llm_output.json")
    prompt = build_prompt(sign_input, cv_summary)
    gate_result = evaluate_quality_gate(sample_output, sign_input)

    summary = {
        "mode": "dry_run",
        "network_calls_made": False,
        "api_keys_required": False,
        "dataset": DATASET_NAME,
        "langsmith_project": PROJECT_NAME,
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "inputs_loaded": [
            "sample_sign_input.json",
            "sample_cv_motion_summary.json",
        ],
        "output_loaded": "sample_llm_output.json",
        "would_trace": {
            "run_name": "kinder_signs_family_draft",
            "run_type": "chain_with_nested_llm_call",
            "inputs": ["approved_sign_object", "cv_motion_summary", "governed_prompt"],
            "output": "structured_family_draft",
            "tags": [
                "kinderflow",
                "kinder-signs",
                "approved-content",
                "human-review-required",
            ],
            "metadata": {
                "dataset": DATASET_NAME,
                "evaluation_scope": "llm_content_transformation_only",
            },
        },
        "would_not_trace_or_evaluate": [
            "MP4 video",
            "sign movement correctness",
            "Baby Sign correctness",
            "Computer Vision quality",
            "professional validity",
        ],
        "quality_gate": gate_result,
    }
    output_path = WORKFLOW_DIR / "langsmith_dry_run_summary.json"
    write_json(output_path, summary)

    print("LangSmith dry run completed without network calls or API keys.")
    print(f"Summary: {output_path}")
    print("Would trace the governed prompt, approved sign object, CV status context, and structured LLM draft.")
    print("Would not trace or evaluate the MP4, movement correctness, CV quality, or professional validity.")
    print(json.dumps(gate_result, indent=2))
    return 0 if gate_result["passed"] else 1


def live_run() -> int:
    missing = [
        name
        for name in ("OPENAI_API_KEY", "LANGSMITH_API_KEY")
        if not os.environ.get(name)
    ]
    if missing:
        print("Live run not started. Missing environment variables: " + ", ".join(missing))
        print("Set them in the invoking shell or the local n8n credential store; do not commit them.")
        print("Then run: python workflow/langsmith_eval.py --run")
        return 2

    try:
        from langsmith import traceable
        from langsmith.wrappers import wrap_openai
        from openai import OpenAI
    except ImportError as exc:
        print(f"Live run dependencies are unavailable: {exc}")
        print("Install the optional packages locally: python -m pip install openai langsmith")
        return 2

    os.environ.setdefault("LANGSMITH_TRACING", "true")
    os.environ.setdefault("LANGSMITH_PROJECT", PROJECT_NAME)

    sign_input = load_json_object(WORKFLOW_DIR / "sample_sign_input.json")
    cv_summary = load_json_object(WORKFLOW_DIR / "sample_cv_motion_summary.json")
    prompt = build_prompt(sign_input, cv_summary)
    model = os.environ.get("OPENAI_MODEL", DEFAULT_MODEL)

    client = wrap_openai(OpenAI())

    @traceable(
        name="kinder_signs_family_draft",
        run_type="chain",
        tags=[
            "kinderflow",
            "kinder-signs",
            "approved-content",
            "human-review-required",
        ],
        metadata={
            "dataset": DATASET_NAME,
            "evaluation_scope": "llm_content_transformation_only",
        },
    )
    def generate_family_draft(governed_prompt: str) -> str | None:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": governed_prompt}],
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content

    try:
        content = generate_family_draft(prompt)
    except Exception as exc:
        print(f"Live LLM/trace request failed ({type(exc).__name__}): {exc}")
        return 1
    if not content:
        print("The LLM returned an empty response.")
        return 1
    try:
        generated_output = json.loads(content)
    except json.JSONDecodeError as exc:
        print(f"The LLM response was not valid JSON: {exc}")
        return 1
    if not isinstance(generated_output, dict):
        print("The LLM response must be a JSON object.")
        return 1

    generated_path = WORKFLOW_DIR / "generated_llm_output.json"
    write_json(generated_path, generated_output)
    gate_result = evaluate_quality_gate(generated_output, sign_input)
    print(f"Generated output: {generated_path}")
    print(f"LangSmith project: {os.environ['LANGSMITH_PROJECT']}")
    print(json.dumps(gate_result, indent=2))
    return 0 if gate_result["passed"] else 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Dry-run or execute the governed Kinder Signs LLM trace."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--run", action="store_true")
    args = parser.parse_args()
    return dry_run() if args.dry_run else live_run()


if __name__ == "__main__":
    sys.exit(main())
