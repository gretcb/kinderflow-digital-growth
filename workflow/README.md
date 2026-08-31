# Kinder Signs governed workflow

This folder contains the smallest credible workflow layer for transforming approved Kinder Signs content into a family-facing draft:

```text
approved sign content + CV motion summary
→ LLM-generated family draft
→ deterministic quality checks
→ LangSmith trace/evaluation
→ draft pending professional approval
```

The LLM transforms approved content into a draft. The quality gate checks unsupported claims, traceability, review status, and movement-note adherence. LangSmith traces the LLM content-transformation step.

Nothing in this workflow validates sign correctness or publishes content automatically.

## Files

| File | Purpose |
|---|---|
| `sample_sign_input.json` | Generic approved-content example |
| `sample_cv_motion_summary.json` | Technical CV context with bounded interpretation |
| `sample_llm_output.json` | Example draft matching the required schema |
| `quality_gate.py` | Dependency-free deterministic validation |
| `langsmith_eval.py` | Keyless dry-run and optional traced LLM run |
| `langsmith_dry_run_summary.json` | Reproducible offline trace plan and gate result |
| `evaluation_cases.json` | Five governed evaluation cases |
| `langsmith_evaluation_plan.md` | Dataset and evaluation design |
| `kinder_signs_n8n_workflow.md` | Node-by-node workflow specification and exact prompt |
| `kinder_signs_n8n_workflow_example.json` | Credential-free illustrative n8n export |

## Run the deterministic gate

From the repository root:

```bash
python workflow/quality_gate.py \
  --input workflow/sample_llm_output.json \
  --source workflow/sample_sign_input.json
```

A passing result exits with status 0:

```json
{
  "passed": true,
  "failed_checks": [],
  "warnings": []
}
```

A failed check returns structured evidence and a non-zero exit status.

## Run the LangSmith dry-run

```bash
python workflow/langsmith_eval.py --dry-run
```

Dry-run mode requires no API keys and makes no network calls. It builds the production prompt, loads the sample LLM output, runs the same deterministic gate, and writes `workflow/langsmith_dry_run_summary.json`.

## Optional live LangSmith run

The script reads credentials only from the invoking environment:

```bash
export OPENAI_API_KEY="<local value>"
export LANGSMITH_API_KEY="<local value>"
export LANGSMITH_PROJECT="kinderflow-kinder-signs-workflow"
# Optional:
export OPENAI_MODEL="gpt-5-mini"

python -m pip install openai langsmith
python workflow/langsmith_eval.py --run
```

Do not place credentials in the repository or workflow export. If either required environment variable is absent, the live command exits before importing the SDKs or calling an API.

The live run saves `workflow/generated_llm_output.json`, traces the OpenAI LLM call through LangSmith, and applies the local deterministic gate. Generated output remains a draft requiring professional approval.

## Manual n8n setup

1. Import `kinder_signs_n8n_workflow_example.json`.
2. Review node compatibility with the installed n8n version.
3. Select the existing local credential named `OpenAI account` in the OpenAI Chat Model node.
4. Confirm the selected model supports JSON output.
5. Test both the pass and fail branches with non-sensitive sample data.
6. Keep the final output as `draft_pending_professional_approval`; do not connect it to automatic publishing.
7. If LangSmith tracing is enabled in n8n, scope it to the LLM transformation only.

The export contains a placeholder credential reference, not a credential or API key.

## Scope boundary

LangSmith evaluates:

- source adherence
- unsupported-claim suppression
- movement-note adherence
- parent clarity
- JSON validity
- preservation of the professional review gate

LangSmith does not evaluate:

- the MP4 video
- sign movement correctness
- Baby Sign correctness
- Computer Vision quality
- professional validity

Those boundaries remain with the CV diagnostics and qualified human review.

## Pitch evidence

The pitch can show:

- the governed architecture and node diagram
- the approved sign input and bounded CV summary
- the structured family draft
- a passing deterministic quality-gate result
- the LangSmith dry-run summary or a later live trace
- the n8n pass/fail routing and professional-approval status

Do not present the workflow as evidence that movement or sign content has been professionally validated.
