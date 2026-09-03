# Kinder Signs n8n workflow

## Purpose

This workflow transforms approved Kinder Signs content into a structured family-facing draft while preserving deterministic checks and professional approval as mandatory gates.

```text
approved sign content + CV motion summary
→ LLM-generated family draft
→ deterministic quality checks
→ optional LangSmith trace/evaluation for the LLM step
→ draft pending professional approval
```

There is no automatic publication. The current repository evidences the deterministic dry-run, not execution of this workflow in the target n8n runtime and not a live external LangSmith trace.

## Node design

| Node | Input | Output | Purpose | Failure path |
|---|---|---|---|---|
| 1. Manual Trigger | Manual execution | Execution event | Starts a controlled demonstration | No downstream action until manually started |
| 2. Set: Approved Sign Object | Embedded generic sample or approved internal object | `sign` object | Establishes the content source of truth | Stop if object is absent |
| 3. Code: CV Motion Summary | Incoming approved-sign item | Incoming item plus `cv_motion_summary` | Adds a stable technical summary while preserving the approved sign object | Always returns a JSON object; schema check rejects missing upstream data |
| 4. Code: Schema Check | Sign and CV objects | `schema_check.passed` plus the input bundle | Checks required fields, review flag, and CV boundary | Returns a structured rejected state; does not throw a raw JavaScript error |
| 5. IF: Schema Valid? | `schema_check.passed` | Valid or rejected branch | Prevents invalid input from reaching the LLM | Invalid branch routes directly to Rejected draft |
| 6. LLM: Family Draft | Exact governed prompt and validated objects | JSON-only family draft | Transforms approved content into the required schema | Fail closed on provider, parsing, or schema error |
| 7. Code: Quality Gate | LLM draft and upstream approved source | `quality_gate` result plus draft | Applies deterministic claim, ID, review, and movement checks | Returns `passed=false` with reasons |
| 8. IF: Pass / Fail | `quality_gate.passed` | Pass or fail branch | Prevents failed drafts reaching the approval queue | Fail branch ends as rejected draft |
| 9. Set: Draft pending professional approval | Passing draft | Draft with `workflow_status=draft_pending_professional_approval` | Produces a reviewable artifact | Human/professional review remains required |

The example export also contains a fail-state Set node so rejected drafts are explicit rather than discarded silently.

## Exact LLM prompt

The Python dry-run injects formatted JSON where the n8n expressions appear below. All other wording is identical.

```text
You are KinderFlow's family-facing content transformation assistant.

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
{
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
}

APPROVED SIGN OBJECT:
{{ JSON.stringify($json.sign, null, 2) }}

CV MOTION SUMMARY:
{{ JSON.stringify($json.cv_motion_summary, null, 2) }}
```

## Schema Check node

The pre-LLM Code node must return `schema_check.passed=false` when:

- `sign_id`, `sign_name`, `source_id`, or `approved_description` is missing
- `movement_notes` does not exist as a string
- `do_not_claim` does not exist as an array
- `requires_human_review` is not the boolean `true`
- `cv_motion_summary` is missing
- the CV summary lacks `motion_representation_status`

An empty `movement_notes` string remains valid and triggers the fixed no-instruction fallback. A missing or non-string field is rejected before the LLM.

## Troubleshooting CV Motion Summary

If the CV Motion Summary node returns `Cannot convert undefined or null to object`, the node is not returning a valid `cv_motion_summary` object. Configure it as a Code node, or as a Set/Edit Fields node that returns the expected JSON payload while preserving the incoming approved-sign item.

The importable workflow uses a defensive Code node. It treats a missing/non-object input as an empty object, adds the complete `cv_motion_summary`, and lets Schema Check return a structured rejection if the approved sign object is absent.

## Quality Gate node

The example Code node implements the portable core of the local `quality_gate.py` policy:

- valid JSON object
- all output fields present
- `requires_human_review=true`
- exact review status `draft_requires_professional_approval`
- preserved `sign_id` and `source_id`
- no banned claim terms
- exact source movement note, or the fixed fallback

The Python script remains the auditable reference implementation and adds the conservative anatomy/direction-term check outside `motion_note`. If the n8n Code node is changed, rerun the same sample through both implementations and reconcile any difference before demonstration.

## LangSmith boundary

LangSmith traces and evaluates the LLM content-transformation step. The trace can contain the generic approved content, bounded CV summary, governed prompt, and structured LLM response.

LangSmith does not evaluate:

- the MP4
- sign movement correctness
- Baby Sign correctness
- Computer Vision quality
- professional validity

The CV POC separately addresses landmark coverage, missing-frame analysis, motion diagnostics, and human visual inspection.

## Import and manual setup

The example JSON is a documentation-first, credential-free n8n export using standard nodes and an OpenAI Chat Model sub-node. n8n node versions can vary, so after import:

1. Open the OpenAI Chat Model node.
2. Select the existing local `OpenAI account` credential.
3. Confirm the installed model node supports JSON-object output.
4. Review expressions and Code-node syntax against the installed n8n version.
5. Execute with the included generic sample.
6. Force one banned-claim output and verify the fail branch.
7. Leave the final node disconnected from publishing systems.

No credentials, API keys, private media, or personal data are present in the export.

## Output state

A passing workflow produces:

```json
{
  "workflow_status": "draft_pending_professional_approval",
  "requires_human_review": true,
  "automatic_publication": false
}
```

That state is a queue for professional review, not an approval decision.

## Content-operations adapter contract

The existing family-draft workflow remains the working n8n example. The stable adapter contract for the broader content-operations layer is documented in `content_ops/contracts/n8n_content_operations_contract.json`.

Input:

```json
{
  "sign_id": "more",
  "sign_version": "v1",
  "operation": "prepare_for_review"
}
```

Controlled orchestration:

```text
receive sign/version
→ load structured source and manifest
→ validate schema
→ inspect technical state
→ inspect visual readiness
→ preserve approved human copy or prepare constrained draft
→ deterministic content gate
→ optional LangSmith evaluation for LLM-assisted wording only
→ build/reuse review package
→ READY_FOR_HUMAN_REVIEW or BLOCKED
```

After an explicit recorded human approval, a separate `build_approved_package` operation may build the versioned package. n8n must not set `PUBLISHED` autonomously.

The operation key is `sign_id:sign_version:operation`. Repeating the same operation must reuse or update the same review package rather than create a duplicate content version. The local Python content-operations harness demonstrates the idempotent package behavior; the imported n8n example does not claim production persistence.

### Generate Content Pack adapter

The Wednesday Content Engine uses one bounded operation: `GENERATE_CONTENT_PACK`. Its input and output contracts are:

- `content_ops/contracts/content_pack_input.schema.json`
- `content_ops/contracts/content_pack_output.schema.json`

```text
structured sign + approved source context
→ optional family-copy drafting
→ structured JSON
→ deterministic quality gate
→ optional LangSmith evaluation of LLM-assisted wording
→ human review
→ reviewed Flashcard Studio handoff
```

The local MVP now exposes this operation at `POST /api/content-packs/generate` and stores isolated run evidence under the ignored `mvp/runs/content_packs/` directory. It can run human, live-provider or dry-run modes. The existing importable n8n workflow remains the orchestration reference; it has not been falsely marked as executed against the new endpoint.

Manual n8n connection steps:

1. Import `workflow/kinder_signs_n8n_workflow.json` and attach the existing local OpenAI credential.
2. Replace the sample sign Set node with an input matching `content_pack_input.schema.json`.
3. Map generation to `GENERATE_CONTENT_PACK`. If n8n runs in a container, use the correct host address rather than assuming container `localhost` reaches this service.
4. Keep the deterministic Code node after generation and map failure to a rejected review package.
5. Trace/evaluate only the LLM wording step in LangSmith.
6. End at a human review package; never connect the pass branch directly to publication.
7. Run MORE once and save only non-sensitive execution evidence.

`generation_method` records whether copy is `human` or `llm_assisted`. `generation_mode` records `LIVE`, `DRY_RUN` or `NOT_APPLICABLE`. These fields must not be used as publication approval. A deterministic PASS and a LangSmith trace/evaluation can prepare content for review; neither may publish it.
