# KinderFlow Create a Sign MVP

## Platform overview

Create a Sign converts a selected adult reference into inspectable movement evidence, a human-selected pose route, and draft family-material options. It centralises content preparation so a nursery does not need to operate Computer Vision or design sign assets.

The repository demonstrates this flow locally. It has no published sign, production library, or real school-to-family delivery.

## Product principle

The character defines the visual style. The reviewed reference defines the movement.

Computer Vision represents observed movement. It does not invent the sign, infer its identity, certify linguistic correctness, or assess a child. A qualified person must control any future publication.

## Three stakeholder perspectives

### KinderFlow Team

The internal team operates reference processing, reviews technical evidence, chooses a pose route, compares draft visuals, prepares family materials, and controls content states. This team, not the nursery, operates MediaPipe, optional LLM, n8n, or LangSmith paths.

### Nursery director and educator

Little Steps Nursery can simulate choosing an available sign, one of three synthetic groups, a material set, and either a group or fictional child audience. The local interaction prevents an exact duplicate and permits editing or removal. It does not represent a real account, entitlement, persistent assignment, or delivery service.

### Family

Family View can read local or session-based demonstration state and show basic sign guidance. A family-facing guidance prototype exists. A personalised assignment-driven family library remains a next product iteration. No current screen proves real identity, access control, notification, cross-session persistence, or delivery.

## Route map

The local service root opens Create a Sign and serves 12 HTML routes:

| Route | Current purpose | Boundary |
|---|---|---|
| `/` | Connected Create a Sign entry when the Python service runs | Service alias for `/create-sign.html` |
| `/index.html` | KinderFlow platform overview | Informational prototype |
| `/kinder-signs.html` | Kinder Signs product overview | Informational prototype |
| `/admin.html` | KinderFlow Team operations overview | No authenticated admin account |
| `/content-studio.html` | Internal workspace selector | Local navigation only |
| `/create-sign.html` | Reference, movement, pose, visual, and material workflow | Connected local MVP |
| `/library.html` | Content and readiness view | Demonstration state, no published library |
| `/flashcards.html` | Flashcard and Routine Card builder | Local deterministic proof |
| `/print-card.html` | A5 print layout | Browser Print or Save as PDF only |
| `/create-story.html` | MORE Story prototype | Deterministic local text only |
| `/create-song.html` | Song page | Coming soon; no active generation |
| `/school.html` | Little Steps Nursery assignment demonstration | Synthetic and session-based |
| `/family.html` | Basic family-facing guidance preview | No real account or delivery |

## Functional architecture

    Browser
    → local Python HTTP service
    → isolated input and run manifest
    → MediaPipe landmark extraction
    → body-relative normalization
    → conservative gap handling
    → OpenCV pose preview and diagnostics
    → operator evidence-route selection
    → deterministic visual options
    → local visual review
    → family-material proof

Content Pack generation is a separate service path:

    approved structured context
    → human copy or optional LLM-assisted draft
    → deterministic quality checks
    → local human review
    → reviewed printable handoff

Neither path publishes automatically.

## User flow and exact labels

The Create a Sign route has five visible steps:

1. Sign & reference.
2. Review reference.
3. Choose poses.
4. Approve visual.
5. Family materials.

The operator chooses MORE, HELP, EAT, SLEEP, MILK, or WATER. Reference options are Upload a video and Use a direct video URL, plus the separate Use demo reference shortcut. The processing action is Review the sign reference.

The result compares Reference video and Pose preview. The technical disclosure reports Frames analysed, Pose detection coverage, Dominant-hand detection coverage, Missing hand frames, Unresolved frames, and Processing duration.

The evidence-route labels are:

- Use tracked poses;
- Choose reference frames; and
- Use reviewed references.

The action after route selection is Create family materials.

## Input controls

### Uploaded MP4

The service accepts MP4 uploads up to 100 MB. It creates a generated run directory and a sanitized display filename. User-controlled filenames do not determine storage paths.

### Demo reference

Use demo reference loads the registered local MORE source and fixes the sign identity to MORE. It runs the same processing path as an uploaded file. The software does not infer identity.

### Direct MP4 URL

The backend accepts a public http or https URL on the default port. It rejects credentials, fragments, control characters, local hostnames, private or reserved addresses, unsafe DNS resolution, nonstandard ports, and HTTPS downgrade.

Each connection is pinned to a previously validated public address. Every redirect is revalidated, with a maximum of three redirects. Environment proxy use is disabled.

The response must identify as video/mp4 or application/mp4. Both declared and streamed content are capped at 100 MB. A 12-second total deadline applies. Bytes are written to a temporary file and moved only after validation; partial files are removed on failure. Stored provenance excludes credentials, query strings, and fragments.

This is a bounded direct-media intake, not a webpage scraper or proof of source permission.

## Error handling and security limits

The service rejects unsupported types, oversize files, missing required fields, unsafe direct URLs, failed media validation, and invalid state handoffs with controlled messages. It removes partial direct-URL downloads. If MediaPipe, preview creation, or ffmpeg fails, the run records a controlled error and stops before presenting the next state. Raw local paths and Python tracebacks are not returned to the browser.

Fail cannot advance to visual or material approval. Review needed exposes the conditions and preserves a human choice. Missing or mismatched visual, content, and printable state fails closed.

These controls are local safeguards, not production security. The prototype has no authentication, role-based access control, tenant isolation, rate limiting, general malware scanning, decoder sandbox, durable encrypted storage, automated retention or deletion, centralized monitoring, backup, or incident-response service. The direct URL checks reduce server-side request risk but do not prove authorization, licence, consent, or safe media content.

## Run isolation and output

Each reference attempt writes under mvp/runs with a generated identifier. The directory is ignored by Git. Processing is serialized because the legacy local MediaPipe runtime is not validated for concurrent hosted use.

Each successful run records:

- sign identity and routine context;
- source kind and sanitized provenance;
- video size, duration, frame rate, frame count, and resolution;
- stage status and measured processing time;
- raw and normalized landmarks;
- gap and motion diagnostics;
- technical and content states;
- four suggested reference frames when available; and
- reference, chart, and browser-preview URLs.

OpenCV first writes a real landmark overlay using MPEG-4 Part 2. ffmpeg then creates the browser-facing H.264, yuv420p, fast-start MP4. This changes delivery encoding only. It does not rerun MediaPipe.

## Movement method

The local pipeline:

- extracts pose and hand landmarks per frame;
- selects the dominant detected hand;
- preserves raw coordinates;
- normalizes hand points to shoulder midpoint and shoulder width;
- creates an explicit frame and landmark index;
- identifies leading, internal, and trailing gaps;
- interpolates only internal gaps of no more than three frames with valid data on both sides;
- keeps other gaps unresolved;
- applies a centered three-frame mean without crossing unresolved gaps; and
- calculates wrist and fingertip displacement evidence.

Four frame suggestions use positions near 18%, 40%, 62%, and 84% of the sequence. The operator may select one or two.

## Status separation

### Extraction status

EXTRACTION_PASS concerns pose and hand coverage thresholds only.

### Motion-representation status

MOTION_REPRESENTATION_PARTIAL means the structured movement remains usable for review but has unresolved continuity, smoothness, or expert-review conditions.

### Operator status

- Pass requires EXTRACTION_PASS and PASS across automated dimensions A to E.
- Review needed means the extraction is usable but one or more automated dimensions is PARTIAL, or an explicit sign-aware rule applies.
- Fail means extraction or representation failed, or a dimension failed outside a permitted sign-aware case.

### Content and publication status

Draft, local content review, visual review, internal-printable eligibility, publication, and school availability are independent. Computer Vision never sets Published.

## Evidence-route logic

Use tracked poses requires at least 90% dominant-hand coverage.

Choose reference frames is available when generated frame suggestions exist. It requires one or two selected frames.

Use reviewed references relies on reviewed sign guidance and any usable movement information. It requires a written rationale.

EAT has a narrow sign-aware rule. Dominant-hand coverage from 65% through 80%, with pose coverage of at least 75%, can remain Review needed when near-face occlusion explains the partial result. This keeps the run reviewable; it does not certify EAT.

## Visual preparation and state

prototype/data/visual_sign_packages.json contains six sign packages. Each has:

- reviewed sign knowledge fields;
- evidence-route preferences;
- two initial deterministic candidates;
- one deterministic additional candidate;
- exact asset path, version, and SHA-256; and
- publication status DRAFT.

The service returns an additional visual only when its ID, asset, and hash differ from the visible options. No network or paid generator is called.

After Approve selected visual, browser session storage records APPROVED_FOR_INTERNAL_PRINTABLE and internal_printable_eligible true. The same record preserves publication_status DRAFT.

This action approves a local proof route only. It is not qualified sign review or publication.

## Family-material paths

The locally approved visual can open:

- Flashcard;
- Routine Card;
- Story for MORE only; and
- Song as Coming soon.

Flashcard and Routine Card offer Bilingual and Spanish output. print-card.html provides a deterministic A5 proof and opens browser Print or Save as PDF. There is no PNG action or server-side PDF generation.

The Story route creates fixed-template English or Spanish text locally. It does not call an LLM, n8n, or LangSmith. Other signs show an unavailable state.

## Library, nursery assignment, and Family View

The Content Library demonstrates wording and readiness checks for the five-record Content Operations set: MORE, EAT, WATER, ALL DONE, and HELP. That regression set is separate from the six-sign visual registry. Local content approval creates a reviewed version but does not publish it. All visual packages remain DRAFT and unavailable to schools as production content.

The Little Steps Nursery route uses three synthetic groups and six fictional children. An educator can choose a sign, group, material set, and either a whole-group or one-child audience. The interface shows a review summary, blocks an exact duplicate, permits Edit and Remove, and can start another assignment while preserving the group.

Assignment state remains in browser session storage. The Family View script can filter that synthetic state by the selected group or child context and combine material types by sign. If no school state exists, it shows a synthetic MORE example. The visible `Your mini-library` label names this demonstration screen; it is not evidence of a completed personalised library.

No content is sent to a real family account or external school platform. Identity, authorisation, cross-session persistence, notifications, delivery, correction, deletion, and a personalised assignment-driven family mini-library remain pending.

## Illustrative motion previews

The asset registry maps:

- MORE to mas.mp4;
- HELP to ayuda.mp4; and
- MILK to leche.mp4.

EAT, SLEEP, and WATER have no registered Gemini FX file.

These videos were prepared separately as illustrative motion previews. They are not generated automatically from the current MediaPipe run or its landmarks. The service checks the registered path, size, hash, media type, and sign mapping before serving one. Rights, external-display permission, fidelity, and professional suitability remain unresolved.

## Golden MORE demonstration path

The recommended connected demonstration uses the registered local MORE reference and keeps its identity explicit:

1. Select MORE and Use demo reference.
2. Select Review the sign reference.
3. Compare Reference video, Pose preview, metrics, and decision charts.
4. Choose Use tracked poses because the recorded local result exceeds the 90% dominant-hand threshold, or demonstrate a human-selected alternative.
5. Compare distinct deterministic draft visuals and record local visual approval.
6. Select Create family materials.
7. Open a Flashcard or Routine Card, then demonstrate the synthetic nursery assignment and basic Family View.

This path shows one coherent local flow. It does not turn the ignored MORE metrics into versioned evidence, make the visual professionally approved, or complete real family delivery. The separately prepared Gemini preview is optional and remains demonstration material.

## Distinct evidence sets

### Versioned Round 1 WATER result

The committed JSON diagnostics and plots report:

- 332 frames;
- 100.00% pose coverage;
- 93.98% dominant right-hand coverage;
- 20 missing hand frames;
- 1 interpolated frame;
- 19 unresolved frames, or 5.72%;
- EXTRACTION_PASS;
- MOTION_REPRESENTATION_PARTIAL; and
- Proceed with conditions.

The source MP4 is local and ignored by Git. The versioned evidence and registry identify this result as WATER.

### Ignored local MORE result

The successful run mvp/runs/run_20260904T061136125509Z_eb661bc3 records:

- 285 frames;
- 100.00% pose coverage;
- 91.93% dominant-hand coverage;
- 25 missing dominant-hand frames;
- 4 interpolated frames;
- 21 unresolved frames, or 7.37%;
- EXTRACTION_PASS;
- MOTION_REPRESENTATION_PARTIAL;
- operator status Review needed; and
- 8.37 seconds processing time.

This is ignored local run evidence. It is not a committed test artifact.

Do not mix numbers from WATER and MORE.

## Verification result

On 4 September 2026, standard discovery ran 184 tests. Of those, 183 passed and one opt-in MVP integration test was skipped:

- Content Operations: 35 passed;
- MVP: 44 passed and one skipped;
- POC: 6 passed;
- prototype: 80 passed; and
- tools: 18 passed.

Running the skipped demo integration explicitly produced one failure before frame processing. MediaPipe could not create an NSOpenGLPixelFormat in the current headless macOS session. The service recorded a controlled processing_error in an ignored run. This confirms the documented runtime limitation and means the local MORE result was not freshly reproduced here.

## Run instructions

The locally evidenced environment is `poc_env` with Python 3.9.6 and MediaPipe 0.10.14. Python 3.11 or 3.12 remains the target for a clean rebuild. The default Python 3.13 installation does not expose the same legacy MediaPipe Solutions API.

From the repository root:

```bash
poc_env/bin/python mvp/app.py
```

Open `http://127.0.0.1:8000/create-sign.html`. The service root at `http://127.0.0.1:8000` opens the same connected route.

Run the standard suites from the repository root:

```bash
poc_env/bin/python -m unittest discover -s content_ops/tests -q
poc_env/bin/python -m unittest discover -s mvp/tests -q
poc_env/bin/python -m unittest discover -s poc/tests -q
poc_env/bin/python -m unittest discover -s prototype/tests -q
poc_env/bin/python -m unittest discover -s tools/tests -q
```

The private-media integration is opt-in and is not a reliable headless test in the current macOS session. Use the earlier local MORE result as local-only evidence, not as a substitute for a controlled rerun.

## Content Pack boundary

The Content Pack service supports human source copy and an optional LLM-assisted path under shared input and output schemas. Missing provider credentials return DRY_RUN. Human copy records LangSmith as NOT_APPLICABLE.

Approval records a generic human_reviewer action and creates a reviewed local content version. Repeated approval is idempotent. It does not publish and cannot populate a printable without a matching locally approved visual.

Provider-path tests use mocks. A real external LIVE model call and a live LangSmith trace are not committed evidence.

## What the MVP proves

- One adult reference can be processed into run-specific landmarks and diagnostics.
- Raw evidence can remain separate from derived values.
- Reference and pose previews can be compared.
- Coverage, gaps, and movement signals can be reported without calling them accuracy.
- An operator can choose a tracked, frame, or reviewed-reference route.
- Six signs can resolve to distinct deterministic draft visuals.
- An exact local visual can pass to printable and story proofs.
- Content checks and human review states can remain separate from publication.
- Synthetic school and family screens can demonstrate intended interaction.

## What the MVP does not prove

- linguistic, Baby Sign, ASL, or LSE correctness;
- semantic sign recognition;
- professional review or publication;
- production avatar fidelity;
- repeatability across multiple performers and conditions;
- a reliable headless or hosted MediaPipe runtime;
- production security, scalability, retention, or audit operations;
- real school accounts, assignments, or family delivery;
- a personalised family mini-library;
- commercial demand or product-market fit; or
- legal approval for a live pilot.

## Current versus future

| Area | Current evidence | Future or pilot work |
|---|---|---|
| Reference processing | Local upload, bounded direct public MP4, and registered MORE demo | Stable supported desktop or hosted runtime with production media controls |
| Technical evidence | MediaPipe landmarks, normalization, gaps, charts, and previews | Multi-reference performance and qualified correspondence review |
| Visuals | Six packages and 18 deterministic draft SVG options | Rights-cleared, qualified sign and visual approval for the 3-5 pilot signs |
| Family materials | Local Flashcard, Routine Card, and MORE Story proofs | Final saved-PDF QA, accessibility review, and approved distribution |
| Song | Coming soon page | Define only if user evidence justifies it |
| Nursery workflow | Synthetic, session-based assignment and duplicate control | Authenticated nursery identity, authorization, persistence, and audit trail |
| Family View | Basic local guidance preview | Personalised assignment-driven mini-library, verified access, real delivery, correction, and deletion |
| Content operations | Local states, gates, provenance, hashes, and five-record regression set | Reconcile with the six-sign registry and operate an identity-backed review ledger |
| n8n | Valid inactive importable 12-node export | Target-runtime execution record if the workflow is retained |
| LangSmith and LLM | Local dry-run and mocked provider-path tests | Live evidence only if needed, permitted, non-personal, traced, evaluated, and reviewed |
| Deployment | None | Optional production scope only after a successful controlled pilot decision |
