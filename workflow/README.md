# Kinder Signs governed workflow

## Purpose

This folder documents a bounded content-transformation path:

    approved sign content and CV summary
    → optional LLM family draft
    → deterministic quality checks
    → optional LangSmith trace for the wording step
    → draft pending professional approval

The workflow cannot certify movement or publish content.

## Current evidence status

The repository contains an importable n8n orchestration design and its exact export. Live execution of the final adapter contract is not claimed.

The exact export is workflow/kinder_signs_n8n_workflow.json. It is valid JSON, has active set to false, and contains 12 nodes. Its name is Kinder Signs: Governed Family Draft (Example).

LangSmith observability is represented through a documented evaluation path and dry-run evidence for the optional LLM content step. No live external model output or live LangSmith trace is committed.

## Files

- sample_sign_input.json: generic approved-content example;
- sample_cv_motion_summary.json: bounded technical context;
- sample_llm_output.json: example structured draft;
- quality_gate.py: dependency-free deterministic validation;
- langsmith_eval.py: keyless dry-run and optional live-provider script;
- langsmith_dry_run_summary.json: committed offline trace plan and passing gate result;
- evaluation_cases.json: five governed evaluation cases;
- langsmith_evaluation_plan.md: dataset and evaluation design;
- kinder_signs_n8n_workflow.md: node, prompt, and adapter specification; and
- kinder_signs_n8n_workflow.json: exact inactive n8n export.

## Deterministic gate

The gate compares the example draft with the approved source. It checks required fields, identifier preservation, review state, human-review requirement, unsupported claims, and movement-note adherence.

Verified on 4 September 2026:

- passed: true;
- failed checks: none; and
- warnings: none.

The executable expects workflow/sample_llm_output.json as the input document and workflow/sample_sign_input.json as the source document. A failed check returns structured reasons and a nonzero exit status.

## LangSmith dry-run

The committed workflow/langsmith_dry_run_summary.json records:

- mode: dry_run;
- network calls made: false;
- API keys required: false;
- dataset: kinder_signs_microlearning_v1;
- project: kinderflow-kinder-signs-workflow; and
- deterministic gate: passed.

The dry-run builds the governed prompt, loads the supplied example output, applies the same deterministic gate, and records what a future trace would contain. It does not contact OpenAI or LangSmith.

## Optional live-provider path

workflow/langsmith_eval.py includes an optional path that reads OPENAI_API_KEY, LANGSMITH_API_KEY, LANGSMITH_PROJECT, and an optional OPENAI_MODEL from the invoking environment. Credentials must not be stored in this repository.

This code path is not current evidence of a live run. If it is used later, the generated draft must remain pending professional approval and the resulting trace must exclude personal data and private media.

## n8n export

The exact inactive export contains:

1. Governance boundary.
2. Manual Trigger.
3. Approved Sign Object.
4. CV Motion Summary.
5. Schema Check.
6. Schema Valid?
7. Family Draft.
8. OpenAI Chat Model.
9. Quality Gate.
10. Pass / Fail.
11. Draft pending professional approval.
12. Rejected draft.

The export includes a placeholder credential reference, not a secret.

## Manual target-runtime validation

Future validation in the selected n8n installation should:

1. Import workflow/kinder_signs_n8n_workflow.json.
2. Review node compatibility with the installed version.
3. Select an approved local OpenAI credential only if the optional LLM path is retained.
4. Confirm JSON-object output support.
5. Test the valid and rejected branches with non-sensitive samples.
6. Confirm that the final passing state remains draft_pending_professional_approval.
7. Leave publication systems disconnected.
8. Save a non-sensitive execution record if the final adapter is executed.

Until that record exists, describe the file as an importable design, not an executed workflow.

## LangSmith scope

LangSmith may evaluate:

- source adherence;
- unsupported-claim suppression;
- movement-note adherence;
- family clarity;
- JSON validity; and
- preservation of the professional-review gate.

LangSmith does not evaluate:

- an MP4;
- MediaPipe;
- hand or pose detection;
- movement fidelity;
- Baby Sign correctness;
- professional validity; or
- publication readiness.

## Content Pack adapter

The local MVP exposes GENERATE_CONTENT_PACK at POST /api/content-packs/generate. Its schemas are:

- content_ops/contracts/content_pack_input.schema.json; and
- content_ops/contracts/content_pack_output.schema.json.

The content path is:

    structured sign and approved source
    → human copy or optional LLM-assisted draft
    → structured JSON
    → deterministic gate
    → optional LangSmith evaluation for LLM wording
    → human review
    → reviewed printable handoff

Generation method records human or llm_assisted. Generation mode records LIVE, DRY_RUN, or NOT_APPLICABLE. None of these values is publication approval.

The local service stores content attempts in ignored mvp/runs/content_packs directories. Provider-path tests use mocks. The n8n export has not been executed against this final endpoint contract.

## Safety boundary

Use only approved, non-sensitive structured source content. Do not send reference video, landmarks linked to an identifiable person, child data, caregiver data, or school-user personal data to the optional LLM or LangSmith path.

A deterministic pass, n8n pass branch, or LangSmith result may prepare a draft for review. None may publish it.
