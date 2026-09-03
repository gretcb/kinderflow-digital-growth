# KinderFlow Create a Sign MVP

This local MVP serves two connected internal capabilities: the existing Create a Sign movement workflow and a governed Content Pack service. It reuses the Round 1 POC and the shared `content_ops` contracts rather than duplicating either method.

## Requirements

- the existing `poc_env` with Python 3.9.6;
- MediaPipe 0.10.14 using the legacy Solutions API;
- ffmpeg with an H.264 encoder available on PATH;
- an MP4 reference video; and
- the local MORE reference at *../resources/video_input/more.mp4* for the current demo-reference path.

Do not upgrade or replace this environment for the current prototype. The machine's default Python/MediaPipe installation is not equivalent to the validated local path.

## Start

From the repository root:

~~~bash
source poc_env/bin/activate
python mvp/app.py
~~~

Open [http://127.0.0.1:8000/create-sign.html](http://127.0.0.1:8000/create-sign.html).

The service also serves the existing prototype routes, including the Flashcard Builder.

## Generate Content Pack API

`POST /api/content-packs/generate` accepts one `GENERATE_CONTENT_PACK` request containing canonical structured sign context and `generation_method` set to `human` or `llm_assisted`.

- Human mode packages the existing human-authored source and marks LangSmith `NOT_APPLICABLE`.
- LLM-assisted mode calls the configured OpenAI model when provider credentials and the optional dependency are available.
- Without provider credentials, the same request runs as deterministic `DRY_RUN`.
- Every attempt is stored under an isolated ignored `mvp/runs/content_packs/content_.../` directory.
- Deterministic checks run before review. They are not replaced by LangSmith.

Review endpoints:

```text
POST /api/content-packs/<run_id>/approve
POST /api/content-packs/<run_id>/request-changes
POST /api/content-packs/<run_id>/restore
GET  /api/content-packs/<run_id>
```

Approval records the generic actor type `human_reviewer` and creates a reviewed content version. Printable creation remains unavailable until the same sign also has an approved visual. It does not publish anything. Repeated approval of the same run is idempotent.

The server loads only allowlisted provider settings from the ignored repository `.env` when present. No key is returned, printed or written into a run. `OPENAI_MODEL` controls the model configuration.

## Demonstration paths

- **Demo reference:** choose **Use demo reference**, then **Review the sign reference**. This processes the registered MORE reference through the real pipeline and keeps the selected identity fixed to MORE. The product does not infer a sign from the video.
- **Custom reference:** select another MP4 validated reference. Metrics and artifacts are calculated for that upload.

MP4 is the supported MVP format. Uploads are limited to 100 MB, remain local and are stored under a generated *mvp/runs/run_...* directory. Run artifacts are ignored by Git. The canonical Round 1 files in *poc/output* are not overwritten.

MediaPipe/OpenCV first writes the real landmark overlay as an intermediate MPEG-4 Part 2 file. The MVP then uses ffmpeg to create a browser-facing H.264 MP4 with yuv420p pixel format and fast-start metadata. MediaPipe is not rerun. If ffmpeg or H.264 encoding is unavailable, the run stops with a controlled preview error rather than presenting an unplayable video.

## Operator-facing status and evidence routes

- **Pass:** extraction is EXTRACTION_PASS and all five automated POC quality dimensions are PASS.
- **Review needed:** extraction produced usable movement data with conditions, or a sign-aware exception applies. EAT at 65–80% dominant-hand coverage with strong pose coverage remains reviewable because near-face occlusion is expected.
- **Fail:** extraction is unusable outside an explicit sign-aware exception. Visual-package availability is reported separately and is not a MediaPipe result.

The POC's raw statuses remain available under technical details. Proceed with conditions is not shown as the main operator status.

The visual flow records one explicit route: `LANDMARK_KEY_POSE`, `HUMAN_SELECTED_FRAME`, `KNOWLEDGE_REFERENCE_FALLBACK`, or the last-resort `INTERNAL_POSE_GUIDE`. Review-needed video can expose four selectable frame suggestions. Grounded fallback requires a rationale. The observed local EAT reference returns **Review needed** at 76.57% dominant-hand coverage and can continue through grounded fallback.

Visual approval records **Approved for internal printable** in session state. It does not certify the sign or publish the asset. The Flashcard Studio hands off to a dedicated A5 route so Flashcards and Routine Cards print as one deterministic portrait card.

For live presentations, keep a short screen recording of the completed demo flow as a fallback. The recording should show the input, stage progression, visual comparison, metrics and review boundary without including private filesystem paths.

The current app sample is MORE reference material, not a production library asset. Its sign identity is confirmed by its byte-for-byte match with the registered MORE input. The committed POC reference and Round 1 diagnostics remain supporting WATER evidence and are never relabelled. Confirm source rights and presentation permission before showing either reference or overlay externally; otherwise replace it with an owned or appropriately licensed reviewed reference.

## Tests

~~~bash
python -m unittest discover -s mvp/tests -v
python -m unittest discover -s poc/tests -v
~~~

The real demo-reference integration test is opt-in because it runs MediaPipe:

~~~bash
KINDERFLOW_RUN_INTEGRATION=1 python -m unittest mvp.tests.test_mvp.DemoIntegrationTest -v
~~~

## Boundaries

The technical result answers whether the captured movement produced usable structured evidence for review. It does not certify linguistic sign correctness. Movement review and content review remain separate, and human review remains the publication gate. LangSmith can trace only LLM wording; it does not evaluate MediaPipe or movement. Local review controls are demo state only; no authentication, database, cloud storage, automatic publication, production avatar or child-video processing is implemented.
