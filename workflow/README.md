# Kinder Signs Workflow

This folder documents the lightweight LLM workflow used to turn approved Kinder Signs content into a parent-facing microlearning draft.

The workflow is intentionally narrow. The LLM does not validate a sign, create movement instructions or act as the source of educational authority. It only rewrites approved content into a clearer family-facing format, then routes the draft to human review.

## What this demonstrates

- Approved content remains the source of truth.
- The LLM performs controlled transformation, not expert validation.
- Deterministic checks catch unsupported claims before review.
- Human approval remains the publication gate.
- LangSmith can trace and evaluate the LLM step.

## Files

| File | Purpose |
|---|---|
| `sample_sign_input.json` | Example approved sign object used as the workflow input |
| `sample_llm_output.json` | Example parent-facing structured output |
| `kinder_signs_n8n_workflow.md` | n8n workflow design and node-level logic |
| `evaluation_cases.json` | Test cases for groundedness and safety checks |
| `langsmith_evaluation_plan.md` | Minimal LangSmith tracing and evaluation plan |

## Scope

This workflow does not perform Computer Vision. The motion-extraction POC is documented separately under `poc/`.

This workflow also does not publish content automatically. Drafts require human/professional review before family use.
