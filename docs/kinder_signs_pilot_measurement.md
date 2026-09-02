# Kinder Signs pilot measurement contract

This document defines future pilot signals. It contains no invented usage results, targets or ROI claims.

## Event contract

The machine-readable schema is `content_ops/contracts/pilot_event_schema.json`.

Useful events include assignment completion, family-output preparation, flashcard views/print requests, video views, pack inclusion and review start/completion. Demo identifiers must be synthetic. Event metadata must not contain child names, photos, video, health information or developmental profiles.

## Metric definitions

| Metric | Definition | Minimum events/data |
|---|---|---|
| School adoption | Distinct schools activating Kinder Signs ÷ schools invited | Invitation register + activation state |
| Educator activation | Distinct synthetic educator IDs completing at least one assignment | `TEACHER_ASSIGNMENT_COMPLETED` |
| Family engagement | Distinct family IDs accessing at least one prepared output ÷ families receiving output | delivery record + view event |
| Flashcard utilisation | Flashcard view and print-request events per delivered flashcard | `FAMILY_OUTPUT_PREPARED`, `FLASHCARD_VIEWED`, `FLASHCARD_PRINT_REQUESTED` |
| Content operations time | Time from source-ready event to human-approved review completion | source-ready timestamp + review events |
| Review rework | Packages requiring changes ÷ packages reviewed | review decision events |

No benchmark is defined before pilot evidence exists.

## Minimum-data inventory

| Field | Purpose | Personal data required? | MVP/demo retention |
|---|---|---:|---|
| `event_id` | Deduplicate and trace an event | No | Local pilot period, then review/delete |
| `timestamp` | Sequence actions and calculate duration | No | Local pilot period, then aggregate/delete |
| `event_type` | Identify meaningful product action | No | Retain in aggregate evidence |
| `school_id` | Measure school-level adoption | Synthetic/pseudonymous only | Local pilot period |
| `group_id` | Measure group assignment | Synthetic/pseudonymous only | Local pilot period |
| `family_id` | Measure output reach without names | Synthetic/pseudonymous only | Shortest practical pilot period |
| `sign_id` | Attribute content usage | No | Retain with content operations record |
| `duration_ms` | Measure review or task time | No | Aggregate after pilot |
| `metadata` | Minimal event-specific context | No free text or PII | Review and minimise per event |

No real child personal data is required. This inventory demonstrates data minimisation; it is not a legal-compliance certification.
