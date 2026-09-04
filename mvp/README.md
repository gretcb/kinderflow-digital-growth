# KinderFlow local MVP guide

## Scope

The local service connects three internal prototype areas:

- Create a Sign reference processing and visual preparation;
- governed Content Pack generation and review; and
- the static KinderFlow product routes.

It reuses the Round 1 POC and Content Operations contracts. It does not publish a sign or deliver content to a real school or family.

## Evidenced environment

The frozen local environment uses:

- Python 3.9.6;
- MediaPipe 0.10.14 with the legacy Solutions API;
- OpenCV through the POC requirements;
- ffmpeg 8.1.2 with an H.264 encoder; and
- the repository-local poc_env.

Python 3.11 or 3.12 remains the preferred clean-environment target, but that setup was not revalidated in this evidence pass. The local MediaPipe runtime may require a macOS graphics context even when inference uses the CPU delegate.

The demo shortcut also requires the local, ignored MORE file registered at ../resources/video_input/more.mp4.

## Start

From the repository root:

    poc_env/bin/python mvp/app.py

Open http://127.0.0.1:8000/create-sign.html.

The service root at http://127.0.0.1:8000 also opens create-sign.html.

## Page routes

The service exposes these prototype files:

- /index.html: KinderFlow platform overview;
- /kinder-signs.html: Kinder Signs product overview;
- /admin.html: KinderFlow Team operations overview;
- /content-studio.html: internal workspace selector;
- /create-sign.html: connected reference and visual flow;
- /library.html: content and readiness review;
- /flashcards.html: Flashcard and Routine Card builder;
- /print-card.html: A5 print proof;
- /create-story.html: deterministic MORE story prototype;
- /create-song.html: Coming soon page;
- /school.html: Little Steps Nursery assignment demonstration; and
- /family.html: family-facing preview.

## Create a Sign path

The visible five-step flow is:

1. Sign & reference.
2. Review reference.
3. Choose poses.
4. Approve visual.
5. Family materials.

Choose MORE, HELP, EAT, SLEEP, MILK, or WATER. Add a source with Upload a video or Use a direct video URL, or select the separate Use demo reference shortcut. Then select Review the sign reference.

The interface compares Reference video and Pose preview. Technical and source details contains:

- Frames analysed;
- Pose detection coverage;
- Dominant-hand detection coverage;
- Missing hand frames;
- Unresolved frames; and
- Processing duration.

The operator result is Pass, Review needed, or Fail. Raw extraction and motion-representation statuses remain visible separately.

### Evidence routes

- Use tracked poses is available when dominant-hand coverage is at least 90%.
- Choose reference frames accepts one or two generated frame suggestions.
- Use reviewed references requires a written rationale.
- EAT can remain Review needed and use the reviewed-reference route when near-face occlusion produces partial but usable evidence.

The action is Create family materials.

### Visual review

Create visual options loads two deterministic draft SVGs for the selected sign. Create another visual option requests one distinct registered SVG with a new ID, path, version, and verified hash. This action does not call a paid or external generator.

Approve selected visual records APPROVED_FOR_INTERNAL_PRINTABLE in browser session storage. The record still has publication_status DRAFT. It is not professional approval or library publication.

## Reference input boundaries

### Upload

- MP4 is the supported format.
- The maximum request body is 100 MB plus multipart overhead.
- The file is written under a generated mvp/runs directory.
- Run artifacts are ignored by Git.
- Filenames are sanitized for display and do not determine the run path.

### Demo shortcut

Use demo reference processes the registered local MORE input through the same pipeline. The shortcut fixes the selected identity to MORE. The product does not infer identity from frames.

### Direct video URL

Use a direct public MP4 URL only. The backend:

- accepts http or https on the default ports;
- rejects credentials, fragments, control characters, local names, private addresses, reserved addresses, and unsafe DNS results;
- pins each connection to a validated public address;
- follows no more than three redirects and validates every hop;
- rejects an HTTPS to HTTP downgrade;
- disables environment proxies;
- accepts video/mp4 or application/mp4 responses;
- enforces declared and streamed size limits of 100 MB;
- applies a 12-second total retrieval deadline;
- writes to a temporary staging file;
- deletes partial files on failure; and
- stores redacted provenance without credentials, query parameters, or fragments.

This is a bounded media fetcher, not a generic webpage scraper or permission check.

## Processing

Each run receives a generated identifier and isolated directory. Processing is serialized to protect the legacy MediaPipe runtime.

The pipeline:

1. validates the input;
2. extracts pose and hand landmarks;
3. creates an OpenCV landmark overlay;
4. normalizes hand coordinates to shoulder midpoint and width;
5. identifies missing intervals;
6. interpolates only internal gaps of no more than three frames;
7. applies centered three-frame smoothing;
8. writes diagnostic JSON and plots;
9. selects four reference-frame suggestions when available; and
10. transcodes the overlay to browser-compatible H.264, yuv420p, fast-start MP4.

If ffmpeg or H.264 encoding fails, the run stops with a controlled preview error. Raw paths and tracebacks are not returned to the browser.

## Status model

Pass requires EXTRACTION_PASS and PASS across automated quality dimensions A to E.

Review needed means extraction produced usable movement evidence but one or more automated dimensions is PARTIAL, or an explicit sign-aware exception applies.

Fail means extraction or motion representation failed, or an automated quality dimension failed outside an allowed sign-aware case.

Content state, visual state, printable eligibility, publication, and school availability are separate. Computer Vision never sets Published.

## Evidence from distinct runs

### Versioned WATER diagnostics

The committed Round 1 JSON and plots report:

- 332 frames;
- 100.00% pose coverage;
- 93.98% dominant right-hand coverage;
- 20 missing hand frames;
- 1 interpolated frame;
- 19 unresolved frames;
- EXTRACTION_PASS; and
- MOTION_REPRESENTATION_PARTIAL.

The local source MP4 is ignored by Git. The versioned artifacts and registry identify the result as WATER.

### Ignored local MORE run

The successful run at mvp/runs/run_20260904T061136125509Z_eb661bc3/run.json reports:

- 285 frames;
- 100.00% pose coverage;
- 91.93% dominant-hand coverage;
- 25 missing hand frames;
- 4 interpolated frames;
- 21 unresolved frames;
- EXTRACTION_PASS;
- MOTION_REPRESENTATION_PARTIAL; and
- 8.37 seconds of local pipeline processing.

This directory is ignored. Cite it only as local run evidence.

### Headless integration result

On 4 September 2026, the opt-in demo integration failed before frame processing because MediaPipe could not create an NSOpenGLPixelFormat in the current headless macOS session. The service returned a controlled processing_error. A normal unlocked desktop session is required for this local runtime, or the runtime must be redesigned and validated for hosting.

## Illustrative Gemini FX videos

Registered local mappings are:

- MORE to mas.mp4;
- HELP to ayuda.mp4; and
- MILK to leche.mp4.

EAT, SLEEP, and WATER have no current Gemini FX output.

These videos were prepared separately as illustrative motion previews. They are not generated automatically from the current MediaPipe run or its landmarks. The service exposes a file only after path, size, sign mapping, type, and SHA-256 match the registry. Usage rights, external-display permission, fidelity, and professional suitability remain unresolved.

## Family-material handoff

After local visual approval:

- Flashcard and Routine Card offer Bilingual or Spanish proofs;
- print-card.html provides an A5 browser Print or Save as PDF route;
- Story provides a deterministic English or Spanish draft for MORE only; and
- Song remains Coming soon.

There is no PNG export, server PDF service, or live LLM call from the Story page.

## Content Pack API

POST /api/content-packs/generate accepts a GENERATE_CONTENT_PACK object under the shared schema.

- Human mode packages approved human-authored source and records LangSmith as NOT_APPLICABLE.
- LLM-assisted mode can call a configured OpenAI model when optional dependencies and credentials are present.
- Without provider credentials, the request returns explicit DRY_RUN evidence.
- Every attempt is stored under an isolated ignored mvp/runs/content_packs directory.
- Deterministic checks run before human review.

Review endpoints:

- POST /api/content-packs/{content_id}/approve
- POST /api/content-packs/{content_id}/request-changes
- POST /api/content-packs/{content_id}/restore
- GET /api/content-packs/{content_id}

Local approval records the generic actor type human_reviewer and creates a reviewed content version. It does not publish a library item.

## Reference and asset API

Reference-run endpoints:

- POST /api/runs/demo
- POST /api/runs/upload
- POST /api/runs/url
- GET /api/runs/{run_id}
- GET /runs/{run_id}/{artifact}

Asset endpoints:

- GET /api/illustrative-videos
- GET /api/illustrative-videos/{sign}
- GET /api/visual-assets/open-peeps
- POST /api/visual-candidates/regenerate
- GET /api/health

## Verification

Run the standard suites from the repository root:

    poc_env/bin/python -m unittest discover -s content_ops/tests -v
    poc_env/bin/python -m unittest discover -s mvp/tests -v
    poc_env/bin/python -m unittest discover -s poc/tests -v
    poc_env/bin/python -m unittest discover -s prototype/tests -v
    poc_env/bin/python -m unittest discover -s tools/tests -v

Verified result on 4 September 2026:

- Content Operations: 35 passed;
- MVP: 44 passed and one skipped;
- POC: 6 passed;
- prototype: 80 passed;
- tools: 18 passed; and
- total: 184 run, 183 passed, one skipped.

The skipped integration invokes private local media and MediaPipe. Its separate headless failure is documented above.

## Production gaps

The service has no authentication, production database, reviewer identity, tenant isolation, cloud store, enforced retention policy, real publication, school integration, family accounts, notifications, payment, or production monitoring. It processes adult references only and performs no child scoring, language recognition, or autonomous educational decision.
