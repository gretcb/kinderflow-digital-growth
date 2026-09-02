# Kinder Signs content operations architecture

## Operating model

```text
SOURCE LAYER
validated reference identifier
        ↓
AI / TECHNICAL LAYER
MediaPipe extraction, normalisation and diagnostics
        ↓
CONTENT LAYER
structured sign data + optional constrained LLM assistance
        ↓
ORCHESTRATION
n8n prepares or reuses a review package
        ↓
EVALUATION
deterministic policy gate + LangSmith for LLM wording only
        ↓
VISUAL LAYER
official modular character base + Kinder Signs reviewed hand asset
        ↓
GOVERNANCE
explicit human review + append-only local events
        ↓
DELIVERY
versioned item in the Signs & Flashcards Library
        ↓
PILOT MEASUREMENT
privacy-minimised product events
```

The character defines the look. The validated reference defines the movement. Human review controls publication.

The video teaches the movement. The flashcard reinforces the sign and its routine.

## Responsibility boundaries

| Layer | Does | Does not |
|---|---|---|
| Computer Vision | Extract movement structure and technical diagnostics | Certify linguistic sign correctness or evaluate children |
| LLM | Assist short wording from supplied context | Invent biomechanics, approve or publish |
| LangSmith | Trace and evaluate LLM-assisted wording | Evaluate movement, MediaPipe or professional validity |
| n8n | Orchestrate controlled steps and stable contracts | Publish autonomously |
| Deterministic gate | Enforce explicit content, asset and publication rules | Replace human judgment |
| Human review | Control approval and publication | Delegate accountability to an automated score |

The machine-readable version is `content_ops/contracts/ai_responsibility_matrix.json`.

## Versioning and provenance

Each sign has a local manifest under `content_ops/signs/<sign_id>/manifest.json`. A structured package contains component versions rather than duplicated video. SHA-256 hashes identify changes to local evidence and structured documents.

`build/publication/more/v1/` is currently a blocked draft package, not a published asset. Rebuilding unchanged inputs reuses the same package identity.

## Review and publication

Technical, content, visual and publication states are independent. Publication requires:

1. acceptable technical state;
2. approved family content;
3. ready illustration and character assets;
4. reviewed sign-specific hand pose;
5. explicit human approval; and
6. an approved publication package.

The policy rejects incomplete packages and exposes readable blocking reasons.

## Deployment boundary

This is a local pilot architecture using JSON, small Python modules and static JavaScript. It has no authentication, production database, cloud media store, billing, external analytics or autonomous publication.
