# Kinder Signs n8n workflow

## Purpose

This workflow transforms approved Kinder Signs content into a structured family-facing draft while preserving deterministic checks and professional approval as mandatory gates.

```text
approved sign content + CV motion summary
→ LLM-generated family draft
→ deterministic quality checks
→ LangSmith trace/evaluation
→ draft pending professional approval
```

There is no automatic publication.

## Node design

| Node | Input | Output | Purpose | Failure path |
|---|---|---|---|---|
| 1. Manual Trigger | Manual execution | Execution event | Starts a controlled demonstration | No downstream action until manually started |
| 2. Set: Approved Sign Object | Embedded generic sample or approved internal object | `sign` object | Establishes the content source of truth | Stop if object is absent |
| 3. Set: CV Motion Summary | Bounded technical summary | `sign` plus `cv_motion_summary` | Supplies technical status without claiming sign correctness | Stop if status or interpretation is absent |
| 4. Code: Schema Check | Sign and CV objects | Validated input bundle | Checks required fields, review flag, source type, and CV boundary | Throw an error; no LLM call |
| 5. LLM: Family Draft | Exact governed prompt and validated objects | JSON-only family draft | Transforms approved content into the required schema | Fail closed on provider, parsing, or schema error |
| 6. Code: Quality Gate | LLM draft and upstream approved source | `quality_gate` result plus draft | Applies deterministic claim, ID, review, and movement checks | Returns `passed=false` with reasons |
| 7. IF: Pass / Fail | `quality_gate.passed` | Pass or fail branch | Prevents failed drafts reaching the approval queue | Fail branch ends as rejected draft |
| 8. Set: Draft pending professional approval | Passing draft | Draft with `workflow_status=draft_pending_professional_approval` | Produces a reviewable artifact | Human/professional review remains required |

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

The pre-LLM Code node must fail closed when:

- `sign_id`, `source_id`, `approved_description`, or `do_not_claim` is missing
- `requires_human_review` is not the boolean `true`
- `source_type` is not `approved_internal_content`
- the CV summary lacks `motion_representation_status` or `technical_interpretation`

Missing `movement_notes` does not trigger an LLM invention. It triggers the fixed no-instruction fallback and a later quality-gate warning.

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
