# Kinder Signs system summary

## Product

Kinder Signs is KinderFlow's first active AI-enabled product. The proposition is a centrally governed Signs and Flashcards Library that helps a nursery introduce a sign in context and gives families simple material for the same routine.

The current repository is a local prototype. It does not yet operate as a production library or delivery service.

## Product roles

- KinderFlow prepares reference evidence, content, draft visuals, and publication records.
- A qualified reviewer must assess movement, hand pose, wording, and suitability before release.
- Little Steps Nursery represents the school buyer and educator workflow with synthetic data.
- The family page demonstrates an assignment-driven sign-and-material mini-library from synthetic browser-session state.

The Family Experience and mini-library is implemented at local, session-based MVP scope. It is not a production service and has no real family identity, account, access, persistence, notification, or delivery layer.

## Current local flow

    Choose one of six signs
    → add an adult reference by upload, direct MP4 URL, or MORE demo shortcut
    → select Review the sign reference
    → inspect reference and pose preview
    → inspect coverage and gap evidence
    → choose tracked poses, reference frames, or reviewed references
    → create and review deterministic visual options
    → record local internal-printable approval
    → create a Flashcard, Routine Card, or MORE Story proof
    → open Little Steps Nursery
    → select the sign, materials, group, and group or fictional-child audience
    → share the synthetic assignment
    → choose View family experience
    → inspect the corresponding sign and materials on family.html

The Create a Sign page presents five steps: Sign & reference; Review reference; Choose poses; Approve visual; Family materials.

The Python application default remains port 8000. The final presentation used `poc_env/bin/python mvp/app.py --port 8765` and the routes `http://127.0.0.1:8765/index.html`, `http://127.0.0.1:8765/kinder-signs.html`, `http://127.0.0.1:8765/create-sign.html`, `http://127.0.0.1:8765/school.html?sign=more&focus=share`, and `http://127.0.0.1:8765/family.html`.

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

The locally evidenced presentation environment used Python 3.9.6 and MediaPipe 0.10.14. `poc/requirements.txt` separately pins MediaPipe 0.10.21 for deployment; that pin is not the environment used for the historical measurements and is not evidence of a successful hosted deployment. Python 3.11 or 3.12 remains the clean future rebuild target.

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
- the exact versioned 12-node n8n workflow export at `workflow/kinder_signs_n8n_workflow.json`; and
- the screenshot at `workflow/evidence/n8n_successful_execution_2026-08-31.png` of the successful historical n8n execution of `Kinder Signs — Governed Family Draft (Example)` on 31 August 2026: status Succeeded, execution ID #21441, and duration 14.499 seconds.

Evidence status: COMPLETE AT CAPSTONE LOW-CODE POC SCOPE. The historical run remained a governed draft workflow, not autonomous publication or production deployment, and does not prove that the later final MVP Content Pack adapter was exercised. Its former OpenAI course credential was removed or revoked and is unavailable, so a fresh provider-backed rerun needs a new authorised credential.

LangSmith is separate and has only committed dry-run evidence, not a live trace. It does not validate hand movement, MediaPipe output, sign correctness, linguistic correctness, or professional approval.

## School and family prototype

The Little Steps Nursery route uses three synthetic groups and six fictional child records. It supports sign, group, materials, and audience selection, assignment edit or removal, and the exact duplicate control `This exact sign, audience and material combination is already active.` Assignments remain in browser session storage.

The family route reads that session state and filters or combines relevant assignments. It also supplies a synthetic MORE fallback when no assignment state exists. This implements the assignment-driven mini-library at local/session MVP scope. It does not provide real family identities or accounts, authentication or authorisation, durable cross-session or cross-device persistence, real notifications or delivery, production school accounts, tenant isolation, production correction or deletion workflows, or external nursery-platform integrations.

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
- real accounts, access control, durable storage, delivery, and audit records;
- a new authorised provider credential for any fresh n8n rerun, evidence of any final-adapter execution, and any production deployment;
- a live LangSmith trace only if separately needed, authorised, and safely scoped;
- production identity, persistence, notification, correction, deletion, tenant, and nursery-integration support for the implemented family mini-library;
- a live pilot; and
- commercial validation.
