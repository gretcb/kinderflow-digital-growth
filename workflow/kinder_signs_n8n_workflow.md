# Kinder Signs n8n workflow specification

## Evidence status

**COMPLETE AT CAPSTONE LOW-CODE POC SCOPE.** `workflow/kinder_signs_n8n_workflow.json` is the exact n8n export stored in the repository. It parses as JSON, contains 12 nodes, has `active` set to `false`, and is named **Kinder Signs — Governed Family Draft (Example)**.

`workflow/evidence/n8n_successful_execution_2026-08-31.png` records a real historical n8n execution of that named governed workflow on 31 August 2026 at 21:30:27. The screenshot shows status **Succeeded**, duration 14.499 seconds, execution ID `#21441`, and the visible successful governed path.

The exact export and the execution screenshot are separate evidence artifacts. Together they satisfy the capstone low-code POC requirement, but they are not production-deployment evidence, a current reproducibility record, or proof that the later final MVP Content Pack endpoint was called. The export contains a placeholder credential reference but no API key.

The course OpenAI credential used at the time of the historical execution was removed or revoked shortly afterwards and is no longer available. A fresh provider-backed rerun requires a new authorised credential. The former key must never be reconstructed, exposed, or committed.

## Purpose

The design transforms an approved sign object into a structured family-facing draft while retaining deterministic checks and professional review:

    approved sign object and bounded CV summary
    → schema check
    → optional LLM wording transformation
    → deterministic quality gate
    → rejected draft or draft pending professional approval

There is no publication node.

## Exported nodes

### Governance boundary

Type: sticky note.

Purpose: states that the flow creates a draft only and cannot validate sign correctness.

### Manual Trigger

Type: manual trigger.

Purpose: starts an operator-controlled demonstration. The export is not scheduled or event driven.

### Approved Sign Object

Type: Set.

Purpose: supplies the generic approved source object. This object, not the model, is the content source of truth.

Failure rule: missing or malformed source fields must stop before the model node.

### CV Motion Summary

Type: Code.

Purpose: adds bounded technical context while preserving the approved source.

Boundary: the summary can report extraction and motion-representation state. It cannot state that a sign is correct.

### Schema Check

Type: Code.

Purpose: validates the approved sign and CV summary before generation.

It must reject when:

- sign_id is missing;
- sign_name is missing;
- source_id is missing;
- approved_description is missing;
- movement_notes is not a string;
- do_not_claim is not an array;
- requires_human_review is not true;
- cv_motion_summary is missing; or
- motion_representation_status is missing.

An empty movement_notes string is valid. It triggers a fixed no-instruction fallback in the draft.

### Schema Valid?

Type: IF.

Purpose: routes a valid object to Family Draft and an invalid object to Rejected draft.

### Family Draft

Type: LangChain chain LLM.

Purpose: transforms only the supplied approved content into the required JSON structure.

Boundary: model or parsing failure must stop the branch. A result remains a draft.

### OpenAI Chat Model

Type: LangChain OpenAI chat-model subnode.

Purpose: provides the optional model to Family Draft after a local credential is selected.

Evidence boundary: the node exists in the exact export, and the named governed workflow has a successful historical execution record. The screenshot does not establish the request or response payload, current reproducibility, or use of the later final MVP adapter.

### Quality Gate

Type: Code.

Purpose: checks the structured draft against identifiers, review rules, unsupported claims, and movement-note requirements.

### Pass / Fail

Type: IF.

Purpose: sends a passing draft to the professional-review queue and a failed draft to the rejected state.

### Draft pending professional approval

Type: Set.

Purpose: records workflow_status as draft_pending_professional_approval.

This state is not Approved or Published.

### Rejected draft

Type: Set.

Purpose: preserves a visible fail state rather than discarding an invalid item silently.

## Governed model instruction

The exported instruction requires the model to:

1. transform only the approved sign content;
2. treat the approved sign object as the source of truth;
3. treat the CV summary as technical context only;
4. return only the required JSON object;
5. preserve sign_id and source_id exactly;
6. set review_status to draft_requires_professional_approval;
7. set requires_human_review to true;
8. avoid invented movement detail;
9. copy supplied movement_notes exactly into motion_note;
10. use the fixed missing-instruction sentence when movement_notes is empty;
11. avoid unsupported developmental, clinical, ASL, or LSE claims;
12. use clear family language; and
13. preserve the school-home connection.

The fixed missing-instruction sentence is:

    Movement instructions are unavailable in the approved input; use an approved reference only after professional review.

The required output fields are:

- sign_id;
- source_id;
- review_status;
- requires_human_review;
- parent_title;
- short_explanation;
- when_to_use;
- practice_tip;
- school_home_connection;
- motion_note; and
- boundaries.

## Quality-gate relationship

The n8n Code node contains the portable core checks:

- valid JSON object;
- every required field present;
- requires_human_review is true;
- exact draft review status;
- unchanged sign and source IDs;
- no forbidden claim terms; and
- exact movement note or fixed fallback.

workflow/quality_gate.py is the auditable local reference implementation. It also applies a conservative check for anatomy or direction language outside motion_note.

If the n8n Code node changes, compare the same sample through the n8n node and Python implementation before presenting the workflow. A difference is an unresolved validation issue.

The local sample gate passed on 4 September 2026 with no failures or warnings.

## LangSmith boundary

LangSmith observability is represented through a documented evaluation path and dry-run evidence for the optional LLM content step.

The committed dry-run records no network calls and no API keys. It uses dataset kinder_signs_microlearning_v1 and project kinderflow-kinder-signs-workflow. It shows that a future trace could contain:

- the generic approved sign object;
- the bounded CV summary;
- the governed prompt;
- the structured draft;
- evaluation tags; and
- gate results.

LangSmith does not evaluate or validate:

- the reference MP4;
- MediaPipe;
- hand movement, hand or pose detection, or MediaPipe output;
- movement fidelity;
- Baby Sign or linguistic correctness;
- professional validity or approval; or
- publication readiness.

No live external trace is committed.

## Fresh-run and integration validation procedure

The successful 31 August 2026 execution is historical evidence. If current reproducibility or the later adapter needs to be tested, obtain a new authorised provider credential and then:

1. Import workflow/kinder_signs_n8n_workflow.json.
2. Confirm all 12 nodes load without substitution.
3. Inspect expressions and Code syntax against that version.
4. Select an approved local credential only if the optional model path remains in scope.
5. Confirm the model node supports JSON-object output.
6. Execute the generic valid sample.
7. Remove a required source field and confirm the rejected branch.
8. Force an unsupported claim and confirm the quality-gate failure.
9. Confirm the passing state is draft_pending_professional_approval.
10. Confirm no publication system is connected.
11. Save a non-sensitive execution record if the final adapter contract is exercised.

Do not present the historical screenshot as proof of the later adapter. Report a current adapter execution only when a new saved record corresponds to the current export and final adapter contract.

## Content Operations adapter

The broader contract is content_ops/contracts/n8n_content_operations_contract.json.

Its review operation identifies:

- sign_id;
- sign_version; and
- operation prepare_for_review.

The intended flow is:

    receive sign and version
    → load structured source and manifest
    → validate schema
    → inspect technical state
    → inspect visual readiness
    → preserve human copy or prepare bounded draft
    → apply deterministic content gate
    → optionally evaluate LLM wording
    → build or reuse review package
    → READY_FOR_HUMAN_REVIEW or BLOCKED

The operation key joins sign_id, sign_version, and operation. Repeating the same operation should reuse or update the same package instead of creating a duplicate version.

The local Python Content Operations module demonstrates deterministic package identity. The historical n8n execution does not prove persistence or execution of this later adapter.

## GENERATE_CONTENT_PACK adapter

The local MVP exposes POST /api/content-packs/generate. Input and output schemas are:

- content_ops/contracts/content_pack_input.schema.json; and
- content_ops/contracts/content_pack_output.schema.json.

The local path can:

- package approved human copy;
- return an explicit DRY_RUN for optional LLM wording without credentials;
- call a configured provider when dependencies and credentials are available;
- apply deterministic checks;
- record an isolated local run; and
- expose local human-review actions.

The repository has tests with injected provider behavior, but no committed real external `LIVE` run of this adapter. The historical n8n execution is not evidence that the final endpoint contract was exercised.

Generation method and generation mode describe how a draft was prepared. They do not approve it.

## Data and publication boundary

Do not put child, caregiver, school-user, private-media, or identifiable-landmark data into this workflow. The supplied samples are generic.

A passing gate can move a draft to professional review. n8n, the LLM, and LangSmith must not set PUBLISHED autonomously.
