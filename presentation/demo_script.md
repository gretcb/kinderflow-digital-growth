# KinderFlow POC and MVP demo script

## Before the session

1. Use a normal local desktop session. The current MediaPipe runtime can fail in a headless macOS context.
2. Start from the repository root with `poc_env/bin/python mvp/app.py`.
3. Open `http://127.0.0.1:8000/index.html`, then open the Kinder Signs flow.
4. Test every link and clear unintended browser-session state.
5. Use only reference and illustrative video whose presentation rights have been confirmed. If rights are not confirmed, use the versioned plots and redacted screenshots.
6. Keep the POC and MVP claims separate.

## POC demo

### Objective

Show that an adult reference video can become stable, body-relative and reviewable movement evidence.

### Sequence

1. Show the reference-video role. Explain that it is an adult content-production source, not a child-performance input.
2. Start or describe MediaPipe processing. Point out pose landmarks, hand landmarks, raw evidence and body-relative normalization.
3. Compare the reference and landmark-overlay preview.
4. Show `poc/output/diagnostics/sign_reference_detection_timeline.png`. Explain that the chart reveals where pose and the dominant hand were detected.
5. Show `poc/output/diagnostics/sign_reference_wrist_trajectory.png`. Explain that the plot supports movement-path review, not correctness scoring.
6. Show the pose route: use tracked poses when dominant-hand coverage meets the 90% rule; otherwise choose one or two reference frames or use reviewed-reference fallback with a rationale.
7. State the versioned WATER result: 332 frames, 100.00% pose coverage, 93.98% dominant-hand coverage, 20 missing hand frames, `EXTRACTION_PASS`, `MOTION_REPRESENTATION_PARTIAL`.

### What it proves

- Real landmark extraction ran on one adult reference; the result artifacts and registry identity are versioned.
- Raw and derived evidence remain separate.
- Missing data and short-gap handling are explicit.
- Reviewers can inspect coverage, movement path and representative frames.

### What it does not prove

- linguistic correctness;
- sign certification;
- motion-retargeting fidelity;
- generalisation across signs or capture conditions;
- a production avatar;
- product-market fit.

## MVP demo

### Objective

Show the beginning of a connected governed content and school workflow, while keeping the current Family View boundary explicit.

### Sequence

1. From KinderFlow, open Kinder Signs and select **Create a sign**.
2. Select MORE and choose one intake path: **Upload a video**, **Use a direct video URL**, or **Use demo reference**.
3. Select **Review the sign reference**. Explain that a direct URL must point to a public MP4 and is not a webpage scraper or rights check.
4. Review the reference, metrics and charts. Keep extraction, motion and content states separate.
5. Choose **Use tracked poses**, **Choose reference frames**, or **Use reviewed references**. Explain why a reviewer may override or use a fallback.
6. Compare deterministic Open Peeps-derived visual candidates. State: the character defines the look; the reviewed reference defines the sign.
7. If showing an illustrative Gemini FX preview, state that it was prepared separately and was not generated from the current run or landmarks.
8. Select **Approve selected visual** for the local printable proof, then **Create family materials**. Clarify that the local approval does not publish the sign.
9. Open a Flashcard or Routine Card. Show Bilingual or Spanish mode and **Print / Save as PDF**. Do not claim PNG export or completed final PDF QA.
10. Mention Story as a local MORE prototype and Song as **Coming soon**.
11. Open Little Steps Nursery. Choose a sign, group, materials and audience. Create an assignment and show duplicate control.
12. Open the family experience. State exactly: a basic family-facing guidance prototype exists; the final personalised assignment-driven family mini-library remains a next product iteration.

### What it proves

- The local roles and interfaces connect across one demo flow.
- The service supports real CV processing and controlled errors.
- Deterministic visual and family-material paths exist.
- Local nursery assignment and duplicate handling work with synthetic records.

### What it does not prove

- a production-approved sign library;
- authenticated school or family accounts;
- real delivery or notifications;
- persistent cross-session assignments;
- live LLM or LangSmith execution;
- final n8n target-runtime execution;
- a personalised family mini-library;
- commercial adoption.

## Backup recording plan

No final backup recording is currently versioned. Before presentation day:

1. Confirm video and image display rights.
2. Record the POC and MVP as separate chapters at the final screen resolution.
3. Keep the visible sequence and wording aligned with this script.
4. Capture the reference review, diagnostic charts, pose route, visual review, one printable, nursery assignment and basic family preview.
5. Do not include credentials, private URLs, local paths, personal data or unconfirmed media.
6. Review audio, captions, focus order, legibility and all limitation statements.
7. Store the approved recording in the agreed submission location and add its evidence path to `../docs/submission_checklist.md`.

## Live failure fallback

| Failure | Fallback | Claim boundary |
|---|---|---|
| MediaPipe cannot create its graphics context | Show the versioned WATER JSON and diagnostic PNGs. | Say the current headless rerun failed; do not claim a fresh successful run. |
| The MORE demo media is unavailable or rights are not confirmed | Use an owned/cleared reference or show redacted evidence only. | Do not display or distribute unconfirmed source media. |
| Gemini preview is unavailable | Continue with the static visual review. | Gemini is optional demo direction, not pipeline evidence. |
| Local API is unavailable | Use the reviewed backup recording or prepared screenshots. | Static pages alone do not prove API execution. |
| Browser session state is inconsistent | Reset the demo or show the recording. | Do not imply persistence or real delivery. |
| Print dialog varies by browser | Show the on-screen card and explain pending final saved-PDF QA. | Do not claim a production PDF exporter. |
