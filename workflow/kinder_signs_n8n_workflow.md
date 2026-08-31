# Kinder Signs n8n Workflow

## Purpose

Transform an approved Kinder Signs content object into a concise parent-facing microlearning draft while preserving expert review as the publication gate.

The workflow demonstrates governance: the LLM helps with wording and structure, but it does not invent sign movement, benefits or professional claims.

## Workflow summary

```text
Manual Trigger
  ↓
Approved Sign Object
  ↓
Schema Check
  ↓
LLM Draft
  ↓
Structured Output Parser
  ↓
Quality Gate
  ↓
Human Review
  ↓
Approved Output Placeholder
```

## Node design

| Step | Node | Role | Failure handling |
|---|---|---|---|
| 1 | Manual Trigger | Starts the demonstration workflow | Not applicable |
| 2 | Set / JSON Input | Loads approved sign content | Stop if required fields are missing |
| 3 | Code / Schema Check | Validates required fields and review status | Route to correction if incomplete |
| 4 | LLM Call | Creates parent-facing draft from approved input only | Route to quality gate |
| 5 | Structured Output Parser | Ensures valid JSON output | Fail closed; require regeneration |
| 6 | Quality Gate | Runs deterministic checks | Fail output if claims or invented details appear |
| 7 | Human Review | Educator/professional approves or edits draft | No auto-publication |
| 8 | Output Placeholder | Writes approved draft to Airtable, Notion, file or CMS later | Placeholder only |

## LLM instruction prompt

```text
You are KinderFlow's parent-facing content assistant.

Use only the approved sign object provided in the input.

Your task is to transform approved content into a concise parent-facing microlearning draft.

Rules:
1. Do not invent sign movement details.
2. Do not add benefits not present in the approved input.
3. Do not claim that Baby Sign accelerates language development.
4. Do not diagnose communication delay or developmental needs.
5. Do not mention ASL or LSE unless explicitly present in the approved input.
6. Do not replace professional advice.
7. Keep the tone warm, clear and professional.
8. Preserve the school-home connection.
9. Keep requires_human_review set to true.
10. Output valid JSON only.

Return this schema:
{
  "sign_id": "...",
  "source_id": "...",
  "review_status": "draft_requires_human_review",
  "requires_human_review": true,
  "parent_title": "...",
  "short_explanation": "...",
  "when_to_use": ["...", "..."],
  "practice_tip": "...",
  "school_home_connection": "...",
  "boundaries": ["...", "..."]
}
```

## Deterministic quality gate

| Risk | Check | Fail action |
|---|---|---|
| Unsupported developmental claim | Block phrases such as “accelerates speech”, “boosts IQ”, “guarantees language” | Reject draft and require rewrite |
| Diagnosis or treatment | Block diagnosis/treatment language | Reject draft and flag human review |
| Invented movement | Compare output movement text against approved movement notes | Reject if additional steps appear |
| ASL/LSE confusion | Block ASL/LSE mentions unless present in input | Reject draft |
| Missing review gate | `requires_human_review` must be true | Reject draft |
| Broken traceability | `sign_id` and `source_id` must be present | Reject draft |
| Invalid JSON | Parser must validate schema | Reject draft |

## What can be shown in the pitch

- A simple n8n workflow screenshot.
- The approved sign input.
- The generated parent-facing draft.
- The quality gate table.
- LangSmith trace/evaluation evidence for the LLM step.

## What this does not prove

This workflow does not prove sign correctness, clinical benefit, willingness to pay or product-market fit. It demonstrates a controlled content transformation layer with traceability and human review.
