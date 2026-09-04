# KinderFlow POC and MVP demo script

## Before the session

1. Use a normal local desktop session. The current MediaPipe runtime can fail in a headless macOS context.
2. Start the final demonstrated route set from the repository root with `poc_env/bin/python mvp/app.py --port 8765`. The application default remains port 8000; it was not changed for the presentation.
3. Check the canonical demonstrated routes:
   - `http://127.0.0.1:8765/index.html`;
   - `http://127.0.0.1:8765/kinder-signs.html`;
   - `http://127.0.0.1:8765/create-sign.html`;
   - `http://127.0.0.1:8765/school.html?sign=more&focus=share`; and
   - `http://127.0.0.1:8765/family.html`.
4. Test every link and clear unintended browser-session state.
5. Use only reference and illustrative video whose presentation rights have been confirmed. If rights are not confirmed, use the versioned plots and redacted screenshots.
6. Keep the POC and MVP claims separate.

## Formal low-code POC evidence

Show the two repository artifacts separately:

1. `workflow/kinder_signs_n8n_workflow.json` is the exact inactive 12-node export for **Kinder Signs — Governed Family Draft (Example)**.
2. `workflow/evidence/n8n_successful_execution_2026-08-31.png` records a real historical execution on 31 August 2026 at 21:30:27, status **Succeeded**, duration 14.499 seconds, execution ID `#21441`, with the successful governed path visible.

State: **COMPLETE AT CAPSTONE LOW-CODE POC SCOPE.** The path creates a governed draft pending professional approval; it does not publish autonomously and is not production deployment. The screenshot does not prove that the later final MVP Content Pack adapter ran. The OpenAI course credential used then was removed or revoked and is no longer available, so a fresh provider-backed rerun requires a new authorised key. Never reconstruct, expose, or commit the former key.

LangSmith is separate: the committed evidence is a network-free dry-run, not a live trace. It does not validate hand movement, MediaPipe output, sign correctness, linguistic correctness, or professional approval.

## Computer Vision technical POC demo

### Objective

Show that an adult reference video can become stable, body-relative and reviewable movement evidence.

### Sequence

1. Show the reference-video role. Explain that it is an adult content-production source, not a child-performance input.
2. Start or describe MediaPipe processing. Point out pose landmarks, hand landmarks, raw evidence and body-relative normalization.
3. Compare the reference and landmark-overlay preview.
4. Show `poc/output/diagnostics/sign_reference_detection_timeline.png`. Explain that the chart reveals where pose and the dominant hand were detected.
5. Show `poc/output/diagnostics/sign_reference_wrist_trajectory.png`. Explain that the plot supports movement-path review, not correctness scoring.
6. Show the pose route: use tracked poses when dominant-hand coverage meets the 90% rule; otherwise choose one or two reference frames or use reviewed-reference fallback with a rationale.
7. State the versioned WATER result: 332 frames, 100.00% pose coverage, 93.98% dominant-hand coverage, 20 missing dominant-hand frames, one interpolated frame, 19 unresolved frames, `EXTRACTION_PASS`, `MOTION_REPRESENTATION_PARTIAL`.

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

Show the complete local/session-based governed flow while keeping production boundaries explicit.

### Sequence

1. From the KinderFlow overview, open Kinder Signs and select **Create a sign**.
2. Select MORE and choose one intake path: **Upload a video**, **Use a direct video URL**, or **Use demo reference**.
3. Select **Review the sign reference**. Explain that a direct URL must point to a public MP4 and is not a webpage scraper or rights check.
4. Review the reference, metrics, and charts. Keep extraction, motion, and content states separate. For the connected local MORE demonstration, use only its own figures: 285 frames, 100.00% pose coverage, 91.93% dominant-hand coverage, 25 missing dominant-hand frames, four interpolated frames, 21 unresolved frames, `EXTRACTION_PASS`, and `MOTION_REPRESENTATION_PARTIAL`.
5. Choose **Use tracked poses**, **Choose reference frames**, or **Use reviewed references**. Explain why a reviewer may override or use a fallback.
6. Compare deterministic Open Peeps-derived visual candidates. State: the character defines the look; the reviewed reference defines the sign.
7. If showing an illustrative Gemini FX preview, state that it was prepared separately and was not generated from the current run or landmarks.
8. Select **Approve selected visual** for the local printable proof, then **Create family materials**. Clarify that the local approval does not publish the sign.
9. Open a Flashcard or Routine Card. Show Bilingual or Spanish mode and **Print / Save as PDF**. Do not claim PNG export or completed final PDF QA.
10. Mention Story as a local MORE prototype and Song as **Coming soon**.
11. Open Little Steps Nursery. Choose a sign, materials, and a group or fictional child, then share the assignment. Show the exact duplicate control: **“This exact sign, audience and material combination is already active.”**
12. Select **View family experience** and open `family.html`. Show that Family View reads browser/session assignment state and displays the corresponding sign and materials. State exactly: **the assignment-driven Family Experience / mini-library is implemented at local/session-based MVP scope.**

### What it proves

- The local roles and interfaces connect across one demo flow.
- The service supports real CV processing and controlled errors.
- Deterministic visual and family-material paths exist.
- Local nursery assignment, exact duplicate handling, and assignment-driven Family View work with synthetic browser/session records.

### What it does not prove

- a production-approved sign library;
- authenticated school or family accounts;
- real delivery or notifications;
- persistent cross-session assignments;
- live LLM or LangSmith execution;
- execution of the later final MVP Content Pack adapter by the historical n8n run;
- current provider-backed n8n reproducibility without a new authorised credential;
- production family identities, authentication, authorisation, tenant isolation, correction/deletion workflows, or cross-device persistence;
- commercial adoption.

## Final recording status

The final recording is present at `presentation/kinderflow_demo.mp4` and was used/prepared for the final presentation. Metadata validation records 4:04.450 duration, H.264 video, 1906x988 resolution, 11,701,274 bytes (11.159 MiB), and no audio stream. This validates the file structure and metadata; it is not a claim that a visual end-to-end review was performed.

The recording should continue to be handled with these controls:

1. Confirm video and image display rights.
2. Keep visible wording aligned with this script.
3. Do not expose credentials, private URLs, local paths, personal data, or unconfirmed media.
4. Record visual playback, legibility, focus, and limitation-statement QA only if that review is actually performed.

## Live failure fallback

| Failure | Fallback | Claim boundary |
|---|---|---|
| A fresh n8n provider-backed rerun is unavailable | Show the exact export and historical execution screenshot. | Say that the old credential was revoked and the 31 August 2026 run is historical; do not imply current reproducibility or later-adapter execution. |
| MediaPipe cannot create its graphics context | Show the versioned WATER JSON and diagnostic PNGs. | Say the current headless rerun failed; do not claim a fresh successful run. |
| The MORE demo media is unavailable or rights are not confirmed | Use an owned/cleared reference or show redacted evidence only. | Do not display or distribute unconfirmed source media. |
| Gemini preview is unavailable | Continue with the static visual review. | Gemini is optional demo direction, not pipeline evidence. |
| Local API is unavailable | Use the final recording if playback has been checked, or use prepared screenshots. | Static pages alone do not prove API execution. |
| Browser session state is inconsistent | Reset the demo or show the recording. | Do not imply durable or cross-device persistence or real delivery. |
| Print dialog varies by browser | Show the on-screen card and explain pending final saved-PDF QA. | Do not claim a production PDF exporter. |
