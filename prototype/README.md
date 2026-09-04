# KinderFlow product prototype

## Purpose

The prototype shows KinderFlow as an early-childhood digital platform and Kinder Signs as its first active AI-enabled product. It separates internal content preparation, a nursery assignment demonstration, and a browser/session-based assignment-driven Family Experience.

Kinder Daily and Kinder Food are future products.

## Current boundary

The interface demonstrates the proposed roles:

- KinderFlow Team prepares reference evidence, wording, visuals, and publication records;
- a qualified reviewer controls any future release;
- Little Steps Nursery selects configured sign and material previews for synthetic groups or children; and
- a family page presents simple sign guidance and selected materials.

No real content is published or delivered. Every canonical sign remains unavailable to schools in the asset registry.

School Admin stores a synthetic assignment in browser/session state. Family View reads that state and displays the matching sign and materials as an assignment-driven mini-library. This is implemented at local/session-based MVP scope, not as a production family service.

## Run modes

### Static review

From the repository root:

    cd prototype
    python -m http.server 8000

Open http://127.0.0.1:8000. Static mode opens index.html and supports the informational and client-side demonstration routes. Create a Sign cannot process media without the MVP service. The Content Library can use its labelled static fallback.

### Connected local MVP

From the repository root:

    poc_env/bin/python mvp/app.py

Open http://127.0.0.1:8000/create-sign.html. The service root also opens this page.

The application default remains port 8000. The final presentation/demo used:

    poc_env/bin/python mvp/app.py --port 8765

with `http://127.0.0.1:8765/index.html`, `http://127.0.0.1:8765/kinder-signs.html`, `http://127.0.0.1:8765/create-sign.html`, `http://127.0.0.1:8765/school.html?sign=more&focus=share`, and `http://127.0.0.1:8765/family.html`.

## Route map

The prototype has 12 HTML routes:

- index.html: KinderFlow platform overview;
- kinder-signs.html: Kinder Signs product overview;
- admin.html: KinderFlow Team operations overview;
- content-studio.html: internal workspace selector;
- create-sign.html: connected reference, visual, and material flow;
- library.html: Content Library and wording-readiness demonstration;
- flashcards.html: Flashcard and Routine Card builder;
- print-card.html: A5 print proof;
- create-story.html: deterministic MORE story prototype;
- create-song.html: Song Coming soon page;
- school.html: Little Steps Nursery assignment demonstration; and
- family.html: session-based assignment-driven Family Experience and mini-library.

## Product architecture

    KinderFlow
    ├── Kinder Signs: active local prototype
    ├── Kinder Daily: future
    └── Kinder Food: future

All three use the KinderFlow name and visual system. They do not have separate logos.

## KinderFlow Team routes

The internal navigation links:

- Overview;
- Kinder Signs;
- Content Library; and
- Schools.

The administrative activity cards use example values only. No account, entitlement service, permission system, or live analytics feed is connected.

## Create a Sign

### Visible flow

The page shows five steps:

1. Sign & reference.
2. Review reference.
3. Choose poses.
4. Approve visual.
5. Family materials.

The sign choices are MORE, HELP, EAT, SLEEP, MILK, and WATER.

The two input modes are Upload a video and Use a direct video URL. Use demo reference is a separate shortcut to the registered MORE file. The operator then selects Review the sign reference.

### Processing evidence

When served by mvp/app.py, the page:

- processes the selected adult MP4 through the real MediaPipe pipeline;
- displays Reference video and Pose preview;
- reports Frames analysed, Pose detection coverage, Dominant-hand detection coverage, Missing hand frames, Unresolved frames, and Processing duration;
- shows Pass, Review needed, or Fail;
- keeps raw extraction and motion-representation values under Technical and source details; and
- isolates each run under the ignored mvp/runs directory.

Computer Vision supports movement review. It does not recognise the selected sign or certify correctness.

### Evidence routes

Use tracked poses requires at least 90% dominant-hand coverage.

Choose reference frames lets the operator select one or two generated suggestions.

Use reviewed references requires a written rationale. EAT can use this route when partial hand visibility near the face leaves otherwise reviewable evidence.

The action after selecting a route is Create family materials.

### Direct video URL

The backend accepts public direct MP4 links only. It validates scheme, port, DNS result, redirect targets, MIME type, size, and deadline. It rejects credentials, fragments, local or private destinations, unsafe resolution, nonstandard ports, HTTPS downgrade, non-MP4 content, and responses over 100 MB. It stages bytes in a temporary file, removes partial files on failure, and omits credentials, queries, and fragments from stored provenance.

This route is not a generic webpage scraper.

## Evidence separation

### Versioned WATER diagnostics

The committed Round 1 JSON and plot evidence belongs to WATER:

- 332 frames;
- 100.00% pose coverage;
- 93.98% dominant right-hand coverage;
- 20 missing hand frames;
- 1 interpolated frame;
- 19 unresolved frames;
- EXTRACTION_PASS; and
- MOTION_REPRESENTATION_PARTIAL.

The source MP4 is local and ignored. The evidence records and registry preserve the WATER identity.

### Ignored local MORE run

The successful run mvp/runs/run_20260904T061136125509Z_eb661bc3 reports:

- 285 frames;
- 100.00% pose coverage;
- 91.93% dominant-hand coverage;
- 25 missing hand frames;
- 4 interpolated frames;
- 21 unresolved frames;
- EXTRACTION_PASS; and
- MOTION_REPRESENTATION_PARTIAL.

It is local run evidence, not a committed artifact. The WATER and MORE values must not be combined.

On 4 September 2026, the opt-in integration failed before frame processing in the current headless macOS session because MediaPipe could not create the required graphics context. Standard discovery still ran 184 tests: 183 passed and one integration test was skipped.

## Visual system

prototype/data/visual_sign_packages.json contains six packages and 18 deterministic Open Peeps-derived SVG options. Each sign has two initial options and one additional local option.

The registered Open Peeps bust supplies the fixed character geometry. Separate Open Peeps examples inform line style for arms and fingers. Custom sign-specific arm, hand, and movement layers make each option distinct. The reviewed reference, not Open Peeps, must define the sign mechanics.

Create another visual option returns a different registered ID, file, version, and hash. It does not call a network or paid image service.

All options remain drafts:

- reviewed static visuals: 0;
- approved Flashcard outputs: 0;
- approved Routine Card outputs: 0;
- school-available signs: 0; and
- publication status for every canonical sign: DRAFT_BLOCKED.

Local Approve selected visual records APPROVED_FOR_INTERNAL_PRINTABLE in browser session storage while publication remains DRAFT. It is not professional review or release.

## Illustrative motion previews

The local registry maps:

- MORE to mas.mp4;
- HELP to ayuda.mp4; and
- MILK to leche.mp4.

EAT, SLEEP, and WATER have no current Gemini FX output.

These videos were prepared separately as illustrative motion previews. They are not generated automatically from the current MediaPipe run or its landmarks. Their recorded provider is Google Labs FX / Gemini FX. The service verifies their registry path, sign mapping, size, type, and hash before serving them.

Rights, external-display permission, movement fidelity, and qualified review remain unresolved. The preview must not be called a landmark-generated animation, production avatar, certified video, or published sign.

## Flashcard and Routine Card

The builder requires the exact visual approved in the current browser session. It fails closed when sign, run, candidate, path, or hash does not match.

The operator can choose:

- Flashcard or Routine Card; and
- Bilingual or Spanish.

The dedicated print-card.html route creates an A5 portrait proof and opens browser Print or Save as PDF. There is no PNG export or server-side PDF service. Final saved-PDF visual quality review remains pending.

The proof does not enter the Content Library or become available to schools.

## Story

create-story.html accepts the exact session-approved visual for MORE and produces a short deterministic English or Spanish story draft. Any other sign shows an unavailable state.

The page demonstrates structured inputs, local checks, and human review actions. It does not call an LLM, n8n, or LangSmith.

## Song

create-song.html displays Song, Coming soon, and Not available yet. No song generation is active.

## Content Engine

The Content Library demonstrates GENERATE_CONTENT_PACK for the five-record Content Operations set:

- MORE;
- EAT;
- WATER;
- ALL DONE; and
- HELP.

This set tests wording, state, provenance, and package rules. It is not the six-sign visual registry.

The connected service can package approved human copy or use an optional LLM-assisted path. Without provider credentials, that path records DRY_RUN. Human copy records LangSmith as NOT_APPLICABLE. Deterministic quality checks remain separate from optional LangSmith tracing.

Local content approval creates a reviewed version but does not publish. A printable handoff also requires the exact locally approved visual.

No real external LIVE LLM generation or live LangSmith trace is committed. LangSmith does not validate hand movement, MediaPipe output, sign correctness, linguistic correctness, or professional approval.

## n8n boundary

The repository contains the exact importable 12-node n8n JSON export, currently marked `active: false`, that describes schema checks, optional wording generation, deterministic routing, and a draft-pending-professional-review outcome. The versioned screenshot at `workflow/evidence/n8n_successful_execution_2026-08-31.png` records **Kinder Signs — Governed Family Draft (Example)** on 31 August 2026 at 21:30:27, status **Succeeded**, execution ID #21441, and duration 14.499 seconds. Evidence status: **COMPLETE AT CAPSTONE LOW-CODE POC SCOPE**.

The historical run is not production deployment and does not prove execution of the later final MVP Content Pack adapter. Its former OpenAI course credential was removed/revoked and is unavailable; a fresh provider-backed rerun requires a new authorised credential. The pass branch is not connected to publication.

## Content Library readiness

The five Content Operations records all pass schema and provenance checks but remain blocked by missing technical, visual, hand-review, content-review, or publication evidence.

The six-sign asset registry separately reports every visual package as DRAFT_BLOCKED and UNAVAILABLE to schools.

The file prototype/data/approved_sign_more.json is a synthetic assignment and family-access fixture despite its filename. It is not approval evidence.

## Little Steps Nursery

The school route uses three synthetic groups and six fictional children. It shows six sign preview cards and configured material chips.

The assignment interaction supports:

- Sign;
- Group;
- Materials;
- Everyone in the group or One child;
- review summary;
- a Share action;
- exact-duplicate blocking;
- Edit and Remove; and
- Share another sign while preserving the group.

An exact duplicate is blocked with: "This exact sign, audience and material combination is already active." State remains in browser session storage. No content is sent to a family account or external school platform.

## Family View

The family route uses the headings Your Kinder Signs, Your mini-library, and Signs shared with you. Its script reads the school session fixture, filters by the selected synthetic group or child context, and combines material sets by sign. If no school state exists, it inserts a synthetic MORE example.

This is a local/session-based assignment-driven Family Experience and mini-library, not final delivery to real family accounts.

Pending work includes real identity and accounts, authentication and authorisation, durable cross-session and cross-device assignment data, notifications and delivery, production school accounts, tenant isolation, correction/deletion workflows, and external nursery-platform integration.

## Data and technology boundaries

The prototype has no:

- production authentication;
- database or cloud persistence;
- tenant isolation;
- production reviewer identity;
- real school or child records;
- family delivery;
- billing or payment;
- production analytics;
- enforced retention or deletion service;
- final avatar;
- automatic sign recognition;
- child-performance scoring;
- linguistic certification; or
- autonomous publication.

The safe claim is a connected local prototype with explicit evidence and governance boundaries.
