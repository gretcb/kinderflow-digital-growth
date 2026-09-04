# Kinder Signs system summary

## Product

Kinder Signs is KinderFlow's first active AI-enabled product. The proposition is a centrally governed Signs and Flashcards Library that helps a nursery introduce a sign in context and gives families simple material for the same routine.

The current repository is a local prototype. It does not yet operate as a production library or delivery service.

## Product roles

- KinderFlow prepares reference evidence, content, draft visuals, and publication records.
- A qualified reviewer must assess movement, hand pose, wording, and suitability before release.
- Little Steps Nursery represents the school buyer and educator workflow with synthetic data.
- The family page demonstrates basic guidance and materials.

A family-facing guidance prototype exists. A personalised assignment-driven family library remains a next product iteration.

## Current local flow

    Choose one of six signs
    → add an adult reference by upload, direct MP4 URL, or MORE demo shortcut
    → select Review the sign reference
    → inspect reference and pose preview
    → inspect coverage and gap evidence
    → choose tracked poses, reference frames, or reviewed references
    → create and review deterministic visual options
    → record local internal-printable approval
    → open a Flashcard, Routine Card, or MORE Story proof

The Create a Sign page presents five steps: Sign & reference; Review reference; Choose poses; Approve visual; Family materials.

## Technical evidence

### Versioned WATER evidence

The committed Round 1 JSON diagnostics and plots describe WATER:

- 332 processed frames;
- 100.00% pose coverage;
- 93.98% dominant right-hand coverage;
- 20 missing hand frames;
- 1 interpolated frame;
- 19 unresolved frames;
- EXTRACTION_PASS; and
- MOTION_REPRESENTATION_PARTIAL.

The local source video is ignored by Git. The versioned evidence files and registry preserve its identity and measured results.

### Local MORE evidence

One successful ignored MORE run records:

- 285 processed frames;
- 100.00% pose coverage;
- 91.93% dominant-hand coverage;
- 25 missing dominant-hand frames;
- 4 interpolated frames;
- 21 unresolved frames;
- EXTRACTION_PASS; and
- MOTION_REPRESENTATION_PARTIAL.

This is local run evidence, not committed proof. A fresh opt-in integration run failed before frame processing in the current headless session because MediaPipe could not create the required graphics context.

Computer Vision supports movement review. It does not identify or certify a sign.

## Visual and family-material state

The visual registry contains six signs and 18 deterministic Open Peeps-derived SVG options. Each sign has two initial options and one additional local option. All options need qualified human review. No sign has a reviewed visual, distributable Flashcard, distributable Routine Card, publication approval, or school availability in the registry.

The character controls the look. The reviewed reference controls the mechanics.

Current material routes:

- Flashcard: deterministic Bilingual or Spanish proof;
- Routine Card: deterministic Bilingual or Spanish proof;
- Story: deterministic local English or Spanish draft for MORE only;
- Song: Coming soon; and
- print: browser Print or Save as PDF through the A5 proof route.

There is no PNG export and no completed saved-PDF visual quality check.

## Illustrative motion previews

Three local Gemini FX files are registered:

- MORE maps to mas.mp4;
- HELP maps to ayuda.mp4; and
- MILK maps to leche.mp4.

EAT, SLEEP, and WATER have no current Gemini FX preview.

These videos were prepared separately as illustrative motion previews. They are not generated automatically from the current MediaPipe run or its landmarks. Rights, external-display permission, movement fidelity, and professional suitability remain unresolved.

## Content and orchestration evidence

The five-record Content Operations set covers MORE, EAT, WATER, ALL DONE, and HELP. It is a wording and readiness regression set, not the six-sign visual catalog. All five records are blocked from publication.

The repository contains:

- deterministic quality-gate code and passing sample evidence;
- human and optional LLM-assisted content-pack paths;
- LangSmith dry-run evidence for the optional wording step;
- an exact, inactive n8n workflow export; and
- no live external LLM trace or target-runtime n8n execution record.

## School and family prototype

The Little Steps Nursery route uses three synthetic groups and six fictional child records. It supports sign, group, materials, and audience selection, duplicate control, and assignment edit or removal. Assignments remain in browser session storage.

The family route can read that session state and filter or combine relevant assignments. It also supplies a synthetic MORE fallback when no assignment state exists. This behavior demonstrates interface logic only. It does not provide identity, authorisation, real delivery, persistence, or notifications.

## Evidence status

Working locally:

- MediaPipe extraction and movement diagnostics;
- bounded upload and direct-MP4 intake;
- reference and pose previews;
- human-selectable evidence routes;
- deterministic visual options;
- local printable and story proofs;
- deterministic content checks; and
- session-based school and family demonstrations.

Pending:

- owned or confirmed presentation rights;
- qualified sign, hand-pose, visual, and content review;
- a production avatar tied to reviewed landmarks;
- published library assets;
- real accounts, access control, storage, delivery, and audit records;
- live n8n and LangSmith evidence;
- a personalised family mini-library;
- a live pilot; and
- commercial validation.
