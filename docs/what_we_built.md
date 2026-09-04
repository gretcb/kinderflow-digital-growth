# What KinderFlow built

Repository status reviewed on 4 September 2026.

## Product summary

Kinder Signs tests whether one reviewed adult sign reference can become reusable nursery and family material without asking each school to operate the technical content-production process.

The repository joins real local Computer Vision, human evidence selection, deterministic draft visuals, printable and story proofs, content-governance code, and synthetic school and family pages. It does not complete production publication or delivery.

## Product route map

The prototype has 12 HTML routes:

1. index.html: KinderFlow platform overview.
2. kinder-signs.html: Kinder Signs product overview.
3. admin.html: internal operations overview.
4. content-studio.html: internal workspace selector.
5. create-sign.html: connected sign-production flow.
6. library.html: content and readiness review.
7. flashcards.html: Flashcard and Routine Card builder.
8. print-card.html: A5 print proof.
9. create-story.html: MORE story prototype.
10. create-song.html: Coming soon page.
11. school.html: Little Steps Nursery assignment demonstration.
12. family.html: basic family-facing preview.

When served by mvp/app.py, the root route opens create-sign.html. A static prototype server opens index.html at its root.

## Reference intake

### What it does

The local MVP accepts one adult MP4 through upload, a registered MORE demo shortcut, or a bounded public direct-MP4 URL.

### Why it exists

Movement must come from a selected source rather than a visual generator.

### Boundary

The operator selects the sign identity. The software does not recognise the sign. Source identity, rights, and professional suitability remain human responsibilities.

The direct URL path accepts a public MP4 only. It validates scheme, port, DNS result, redirects, MIME type, size, and timeout; rejects local or private targets; stages a temporary file safely; and removes query data from stored provenance. It is not a webpage scraper.

## MediaPipe extraction

### What it does

The pipeline extracts 33 pose landmarks and 21 landmarks per detected hand for each readable frame. It preserves timestamps and the dominant detected hand.

### Why it exists

The coordinates make observed movement inspectable over time.

### Boundary

Landmark coverage is not sign correctness, language recognition, or child assessment.

## Movement representation

### What it does

The POC:

- preserves raw coordinates;
- creates a complete frame and landmark index;
- normalizes hand coordinates to shoulder midpoint and width;
- interpolates only internal gaps of no more than three frames;
- leaves leading, trailing, and longer gaps unresolved;
- applies a centered three-frame smoothing window; and
- creates wrist and fingertip displacement diagnostics.

### Why it exists

An operator can compare the reference, pose preview, coverage timeline, and hand path before selecting evidence for the visual.

### Boundary

The representation is not a family-facing avatar and is not fully viewpoint invariant.

## Technical evidence

### Versioned WATER evidence

The Round 1 JSON and plot artifacts describe WATER:

- 332 frames;
- 100.00% pose coverage;
- 93.98% dominant right-hand coverage;
- 20 missing hand frames;
- 1 interpolated frame;
- 19 unresolved frames;
- EXTRACTION_PASS; and
- MOTION_REPRESENTATION_PARTIAL.

The source video is local and ignored by Git. The evidence JSON, plots, and asset-registry record are versioned.

### Local MORE evidence

The ignored successful run at mvp/runs/run_20260904T061136125509Z_eb661bc3 records:

- 285 frames;
- 100.00% pose coverage;
- 91.93% dominant-hand coverage;
- 25 missing dominant-hand frames;
- 4 interpolated frames;
- 21 unresolved frames;
- EXTRACTION_PASS; and
- MOTION_REPRESENTATION_PARTIAL.

It is local evidence only. Do not combine its numbers with the WATER result.

### Current verification

Standard discovery ran 184 tests on 4 September 2026: 183 passed and one opt-in MVP integration test was skipped. Running that integration explicitly failed before frame processing because MediaPipe could not create a graphics context in the current headless macOS session. The service returned a controlled error. The prior local MORE run was not reproduced during this check.

## Reference review and pose selection

### What it does

The Create a Sign interface presents five steps:

1. Sign & reference.
2. Review reference.
3. Choose poses.
4. Approve visual.
5. Family materials.

Pass, Review needed, and Fail translate technical states into operator routing. The three evidence choices are Use tracked poses, Choose reference frames, and Use reviewed references.

Tracked poses require at least 90% dominant-hand coverage. The frame route supports one or two generated suggestions. The reviewed-reference route requires a written reason. EAT can use that route when near-face occlusion leaves partial but reviewable evidence.

### Boundary

The action Create family materials accepts an evidence route for visual preparation. It does not approve or publish the sign.

## Visual preparation

### What it does

The canonical registry covers MORE, HELP, EAT, SLEEP, MILK, and WATER. Each package offers two initial SVG options and one deterministic additional option. The fixed Open Peeps bust defines the character style; custom arm, hand, and movement layers differ by sign.

### Why it exists

Operators need a consistent visual system whose sign-specific details remain visible for review.

### Boundary

All 18 options are drafts. Open Peeps does not validate the sign. No visual has qualified hand-pose review, printable approval, publication approval, or school availability.

## Illustrative motion preview

### What it does

The service can display local pre-generated Gemini FX files for three signs:

- MORE maps to mas.mp4;
- HELP maps to ayuda.mp4; and
- MILK maps to leche.mp4.

### Boundary

EAT, SLEEP, and WATER have no current file. These videos were prepared separately as illustrative motion previews. They are not generated automatically from the current MediaPipe run or its landmarks. Usage rights, external-display permission, fidelity, and professional suitability remain unresolved.

## Flashcard and Routine Card

### What they do

These deterministic routes combine the exact session-approved draft visual with controlled bilingual wording and layout. The operator chooses Flashcard or Routine Card and Bilingual or Spanish.

### Boundary

The approval state is APPROVED_FOR_INTERNAL_PRINTABLE and publication remains DRAFT. Browser Print or Save as PDF through the A5 proof route is the only export. There is no PNG action, server PDF service, or completed saved-PDF visual review.

## Story and Song

### Story

The Story route uses the exact session-approved visual and creates a deterministic English or Spanish draft for MORE. It has local checks and review actions.

No live LLM, n8n, or LangSmith call runs from the page. Other signs fail closed.

### Song

Song is marked Coming soon and Not available yet. No song generation is implemented.

## Content Operations

### What it does

The Content Operations module keeps source, technical, wording, visual, hand review, deterministic gate, human review, publication, and library state separate. It records hashes, package identity, and local events.

### Evidence-set boundary

Its five records are MORE, EAT, WATER, ALL DONE, and HELP. The canonical visual registry has six different records. The five-record set is a wording and readiness regression fixture. All five records are blocked.

The versioned MORE package proves deterministic package construction. It remains Draft and blocked.

## Optional LLM wording and LangSmith

### What they do

The Content Pack service can use approved human copy or an optional LLM-assisted path under one schema. Deterministic checks remain separate. LangSmith is scoped only to the optional wording step.

### Current evidence

Dry-run and mocked provider-path behavior are tested. The repository contains a LangSmith dry-run summary and five evaluation cases.

### Boundary

No live external model output or live LangSmith trace is committed. Neither tool evaluates MediaPipe, movement fidelity, or sign correctness.

## n8n orchestration

### What it does

The exact JSON export describes a manual flow from an approved sign object and bounded CV summary to a draft pending professional review. It includes schema checks, a model node, deterministic quality routing, and rejected and pending-review outcomes.

### Boundary

The export is inactive. The repository contains no final adapter execution record from a target n8n runtime and no automatic publication connection.

## Content Library

### What it does

The interface shows wording readiness, asset state, and blocking reasons.

### Boundary

No production database or published library exists. The asset registry reports all six signs as UNAVAILABLE to schools.

## Little Steps Nursery assignment

### What it does

The synthetic school page offers six sign previews and supports selecting a group, materials, and either everyone in the group or one child. It blocks an exact duplicate and supports editing and removing active assignments.

### Boundary

Assignments remain in browser session storage. No permission engine, account, family notification, or backend delivery exists.

## Family View

### What it does

The family page reads the browser-session assignment fixture, filters it to a selected synthetic family context, and combines materials by sign. If no assignment state exists, it supplies a synthetic MORE example.

### Boundary

A family-facing guidance prototype exists. A personalised assignment-driven family library remains a next product iteration. Real family identity, access control, persistent data, notifications, and school integration are pending.

## Tableau decision support

The packaged Tableau workbook contains four views about Spanish institutional access, Madrid digital readiness, adult age-cohort GenAI proxies, and competitive positioning. It supports a pilot discussion only. It does not show live product telemetry, market share, demand, or willingness to pay.

## Current publication state

The repository has no published production sign:

- reviewed static visuals: 0;
- approved Flashcard outputs: 0;
- approved Routine Card outputs: 0;
- signs available to schools: 0; and
- live school or family deliveries: 0.

The work demonstrates a connected local prototype and an inspectable governance design. A controlled pilot must close source rights, professional review, runtime, privacy, security, delivery, and measurement gaps.
