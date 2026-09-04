# Kinder Signs MVP reality check

## Current status

Kinder Signs is a working local product and technical prototype. It contains real MediaPipe processing, deterministic content checks, draft visual assets, and browser interaction. It is not a production service and no sign is published or available to a real school.

## Working local capabilities

### Reference processing

- Accepts one adult MP4 by local upload.
- Accepts one public direct MP4 URL within a 100 MB and 12-second retrieval boundary.
- Provides a registered MORE demo-reference shortcut.
- Runs pose and hand landmark extraction, body-relative normalization, conservative interpolation, smoothing, and movement diagnostics.
- Produces isolated ignored run records, a reference preview, an H.264 pose preview, charts, and measured coverage.
- Returns Pass, Review needed, or Fail for operator routing.

The direct URL path rejects credentials, fragments, unsafe ports, local or private destinations, unsafe DNS results, HTTPS downgrade, non-MP4 responses, oversized bodies, and excessive redirects. It redacts query data from stored provenance. It is not a webpage scraper.

### Human evidence routes

- Use tracked poses is available at 90% or higher dominant-hand coverage.
- Choose reference frames supports one or two generated frame suggestions.
- Use reviewed references requires a written rationale.
- EAT can use the reviewed-reference route when near-face hand occlusion leaves otherwise usable evidence.

The operator then selects a draft visual option. Local visual approval makes an exact asset eligible for the internal printable proof. Publication remains Draft.

### Family-material proofs

- Flashcard and Routine Card support Bilingual and Spanish modes.
- The A5 print route opens browser Print or Save as PDF.
- Story produces a deterministic English or Spanish prototype for MORE only.
- Song is marked Coming soon and is inactive.

There is no PNG export, server-side PDF service, production avatar, or completed saved-PDF visual quality check.

### School and family demonstrations

Little Steps Nursery uses synthetic groups and fictional child records. The school page supports sign, group, material, and audience selection, exact-duplicate control, and active-assignment editing or removal. Data remains in browser session storage.

The family page can read and filter that session state, but it is still a demonstration. A family-facing guidance prototype exists. A personalised assignment-driven family library remains a next product iteration.

## Evidence separation

### Versioned WATER result

The committed Round 1 diagnostics report 332 frames, 100.00% pose coverage, 93.98% dominant right-hand coverage, 20 missing frames, EXTRACTION_PASS, and MOTION_REPRESENTATION_PARTIAL. The source video itself is local and ignored; the JSON diagnostics, plots, and registry record are versioned.

### Ignored local MORE result

The successful local run at mvp/runs/run_20260904T061136125509Z_eb661bc3/run.json reports 285 frames, 100.00% pose coverage, 91.93% dominant-hand coverage, 25 missing frames, 4 interpolated frames, 21 unresolved frames, EXTRACTION_PASS, and MOTION_REPRESENTATION_PARTIAL. Processing took 8.37 seconds locally.

That directory is ignored by Git. Treat these values as local run evidence only.

### Verification on 4 September 2026

The standard suites ran 184 tests: 183 passed and one opt-in integration test was skipped. The counts were:

- Content Operations: 35 passed;
- MVP: 44 passed and one skipped;
- POC: 6 passed;
- prototype: 80 passed; and
- tools: 18 passed.

Running the skipped integration explicitly produced one failure before frame processing. MediaPipe could not create an NSOpenGLPixelFormat in the current headless macOS session. The application returned a controlled processing error. This does not invalidate the earlier local MORE record, but it means that run was not reproduced in this session.

## Draft visual and asset status

The canonical registry contains six signs and 56 asset records. MORE, HELP, EAT, SLEEP, MILK, and WATER each have three deterministic draft SVG options. All six remain:

- printable: BLOCKED;
- publication: DRAFT_BLOCKED; and
- school availability: UNAVAILABLE.

Open Peeps supplies a fixed character base and style references. Custom sign-specific arms, hands, and movement marks are present in the draft SVGs. None has completed qualified sign and visual review.

The three registered Gemini FX demonstrations map MORE to mas.mp4, HELP to ayuda.mp4, and MILK to leche.mp4. They are separate pre-generated files with unresolved usage permission and professional-review gates. EAT, SLEEP, and WATER have no such file.

## Content and workflow status

Content Operations has five regression records: MORE, EAT, WATER, ALL DONE, and HELP. This differs intentionally from the six-sign visual registry. Every regression record is blocked from publication.

The repository has an inactive, importable n8n JSON export and LangSmith dry-run evidence. It does not have a final n8n target-runtime execution record, a live external LLM run, or a live LangSmith trace.

## Production gaps

- no qualified sign or hand-pose approval;
- no published content package;
- no authenticated reviewer identity;
- no user accounts or tenant separation;
- no production database or media store;
- no enforced retention or deletion service;
- no real school or family delivery;
- no personalised family library;
- no live product analytics;
- no payment or billing;
- no tested hosted MediaPipe runtime; and
- no commercial pilot evidence.

The safe claim is that the repository demonstrates a connected local prototype with explicit review and publication boundaries.
