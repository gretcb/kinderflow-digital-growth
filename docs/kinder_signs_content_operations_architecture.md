# Kinder Signs content operations architecture

## Operating principle

The character defines the visual style. The reviewed reference defines the movement. A qualified person controls publication.

KinderFlow separates technical capture, wording, visual preparation, review, and publication so that one successful check cannot be mistaken for complete approval.

## End-to-end target flow

    Reviewed adult reference
    → MediaPipe extraction and diagnostics
    → structured sign and routine context
    → optional bounded wording assistance
    → deterministic content checks
    → source-grounded visual options
    → qualified human review
    → versioned publication package
    → eligible school library
    → school assignment
    → family delivery

The repository implements only parts of this target flow. It does not contain a published sign or real school-to-family delivery.

## Current evidence layers

### Computer Vision

The versioned Round 1 diagnostics belong to WATER. They report 332 frames, 100.00% pose coverage, 93.98% dominant right-hand coverage, 20 missing hand frames, 1 interpolated frame, 19 unresolved frames, EXTRACTION_PASS, and MOTION_REPRESENTATION_PARTIAL.

An ignored local MORE run reports 285 frames, 100.00% pose coverage, 91.93% dominant-hand coverage, 25 missing hand frames, 4 interpolated frames, 21 unresolved frames, EXTRACTION_PASS, and MOTION_REPRESENTATION_PARTIAL. It is local run evidence, not a committed artifact. The two runs must never be merged.

### Visual preparation

The canonical asset registry contains six signs: MORE, HELP, EAT, SLEEP, MILK, and WATER. Each has two initial Open Peeps-derived options and one deterministic regeneration option. All 18 options are drafts. There are no reviewed static visuals, distributable printables, or signs available to schools.

Open Peeps supplies the fixed character style and line references. It does not supply or validate sign mechanics. The sign-specific hand and arm layers remain subject to qualified review.

### Content Operations

The Content Operations regression set has five records: MORE, EAT, WATER, ALL DONE, and HELP. This set tests wording, state, provenance, and package rules. It is separate from the six-sign visual registry. All five regression records are blocked from publication.

The blocked MORE package under build/publication/more/v1 binds hashes and component versions. It is evidence of package construction, not evidence of publication.

### School and family experience

The Little Steps Nursery page simulates selection of a sign, group, material set, and audience. It blocks an exact duplicate with: "This exact sign, audience and material combination is already active." It also supports edit and removal actions. State remains in browser session storage.

Family View reads the synthetic assignment state and displays the corresponding sign and material set as an assignment-driven mini-library. This is implemented at local/session-based MVP scope. There are no real family identities or accounts, authentication or authorisation, real delivery, notifications, production school accounts, tenant isolation, durable cross-session or cross-device assignments, production correction/deletion workflows, or external nursery-platform integrations.

## Responsibility boundaries

### Computer Vision

Does: extracts and represents observed pose and hand landmarks; reports coverage, gaps, and movement diagnostics.

Does not: identify the sign automatically, certify linguistic correctness, assess a child, or approve content.

### Optional LLM step

Does: transforms supplied approved wording into a bounded family draft when configured.

Does not: invent movement mechanics, validate a sign, or publish content. For the later final MVP Content Pack adapter, only dry-run and mocked provider-path evidence is committed; the separate historical n8n execution does not prove that adapter ran.

### LangSmith

Does: represents an evaluation and trace path for optional LLM wording.

Does not: evaluate hand movement, MediaPipe output, the reference video, sign correctness, linguistic correctness, or professional approval. The repository contains dry-run evidence, not a live external trace.

### n8n

Does: provides the exact importable 12-node JSON export, currently marked `active: false`. The versioned screenshot at `workflow/evidence/n8n_successful_execution_2026-08-31.png` records **Kinder Signs — Governed Family Draft (Example)** on 31 August 2026 at 21:30:27, status **Succeeded**, execution ID #21441, and duration 14.499 seconds. Evidence status: **COMPLETE AT CAPSTONE LOW-CODE POC SCOPE**.

Does not: prove production deployment, autonomous publication, current provider-backed reproducibility, or execution of the later final MVP Content Pack adapter. The OpenAI course credential used historically was removed/revoked; a fresh provider-backed rerun requires a new authorised credential.

### Deterministic gates

Do: enforce explicit schema, wording, asset, state, and publication requirements.

Do not: replace professional judgement.

### Human review

Does: selects the evidence route, reviews the visual and content, and controls any future publication decision.

Does not: become a production approval merely because a local browser button was selected.

## State model

Keep these states separate:

1. extraction coverage;
2. motion-representation status;
3. content readiness;
4. visual review;
5. printable eligibility;
6. publication status; and
7. school availability.

The current visual workflow can record APPROVED_FOR_INTERNAL_PRINTABLE in browser session state while publication remains DRAFT. Every canonical registry record remains BLOCKED for printable output, DRAFT_BLOCKED for publication, and UNAVAILABLE to schools.

## Provenance and versioning

Sign manifests live under content_ops/signs. The canonical visual and source record is assets/registry/sign_asset_registry.json. SHA-256 hashes identify exact local files and generated documents. A rebuilt package can reuse its deterministic identity when inputs are unchanged.

The local input videos and Gemini FX files are outside the versioned repository. Their hashes and classifications are recorded in the registry. Rights and external-display permission remain a release gate.

## Deployment boundary

This is a local product and technical prototype using JSON, Python, static JavaScript, and browser session storage. It has no production authentication, reviewer identity, tenant isolation, database, cloud media store, retention service, billing, school integration, family delivery, or autonomous publication.
