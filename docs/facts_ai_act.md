# AI-role facts for later EU AI Act analysis

This document records intended roles and controls. It does not make a legal classification or certify compliance.

| Component | Intended role | Not its role | Human control | Current evidence |
|---|---|---|---|---|
| Computer Vision | Extract and structure movement from controlled reference material; report capture diagnostics | Certify linguistic correctness; score children; infer development; approve publication | A person reviews the source, technical evidence and content before release | `poc/`; `mvp/`; `content_ops/contracts/ai_responsibility_matrix.json` |
| LLM | Optionally draft or edit short family wording from supplied approved context | Create hand shape/movement; diagnose; make developmental claims; validate a sign; publish | Draft must retain `requires_human_review`; deterministic checks run before professional review | `workflow/langsmith_eval.py`; `workflow/quality_gate.py`; sample inputs/outputs |
| LangSmith | Trace and evaluate the LLM-assisted content transformation | Evaluate video, MediaPipe, hand movement or professional correctness | A reviewer uses criterion-level evidence; the tool does not make publication final | `workflow/langsmith_evaluation_plan.md`; dry-run summary |
| n8n | Move structured content through defined preparation, check and routing steps | Decide sign correctness; approve or publish autonomously | Contract requires human review and `automatic_publication: false` | n8n workflow docs/export; `content_ops/contracts/n8n_content_operations_contract.json` |
| Human review | Decide whether controlled content can advance to publication | Delegate accountability to a technical score or pretend missing evidence exists | Explicit approval is required; changes/rejection remain possible | State machine, publication policy and tests |

## Intended-purpose boundary to preserve

Kinder Signs currently supports production and distribution of reviewed educational sign material. It does not assess a child, make an educational placement decision or provide clinical advice.

Future changes—especially child video, performance scoring, developmental inference, biometric functions or automated decision-making—would require a new product, privacy and legal assessment. They are not implied by the current MVP.
