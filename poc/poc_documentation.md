# Kinder Signs technical feasibility POC

## Decision question

Generated video can look plausible while changing hand shape, palm orientation, contact, timing, or trajectory. KinderFlow therefore needs an inspectable motion representation before any future rendering experiment.

This POC asks:

> Can one selected adult reference be converted into body-relative, temporally ordered hand and pose data that is suitable for controlled motion-preservation experiments?

The experiment evaluates extraction coverage and representation quality. It does not evaluate language correctness, pedagogy, clinical outcomes, market demand, avatar fidelity, or synthetic-video quality.

## Evidence identity and version status

The Round 1 Computer Vision feasibility result belongs to WATER.

The local file poc/input/sign_reference.mp4 is byte-identical to the registered local WATER input at ../resources/video_input/water.mp4. Both have:

- byte size: 586,766; and
- SHA-256: 28f844d5af72ef1bcd351048ba57d74b2ad32bb6584fed919e27d3e59f8f44ea.

The source MP4 is ignored by Git. It is not part of a fresh clone. The repository versions the POC code, metadata, summary JSON, diagnostic JSON, plots, and the asset-registry identity record. An authorised copy of the WATER source is required for a full rerun.

Do not relabel this evidence as MORE. The current MORE MVP run is a different, ignored local run with different measurements.

## Technical hypothesis

A local Computer Vision pipeline can:

- extract observed body and hand coordinates;
- preserve raw-evidence hashes;
- transform hand points into a shoulder-relative coordinate system;
- make missing observations explicit;
- reconstruct only short internal gaps;
- store a lightly smoothed derivative without overwriting earlier stages; and
- expose movement continuity for human inspection.

The hypothesis concerns structured representation. It does not claim semantic understanding.

## Architecture

    Selected adult reference
    → MediaPipe pose and hand extraction
    → raw landmark records
    → complete expected index
    → shoulder-relative normalization
    → conservative internal-gap interpolation
    → centered smoothing
    → temporal diagnostics and plots
    → qualified human comparison
    → future rendering experiment

The recorded lineage is:

    raw → normalized → interpolated → smoothed → diagnostics

Raw and derived coordinates remain separate. The versioned normalization metadata records SHA-256 values for the local raw hand CSV, pose CSV, and extraction metadata.

## Source and extraction method

MediaPipe processes each frame of one adult reference and emits:

- 33 pose landmarks for each detected pose frame;
- 21 landmarks for each detected hand;
- normalized image coordinates x, y, and z;
- frame number; and
- timestamp.

The result contains 332 processed frames at 29.970 frames per second and 640 by 360 pixels. The right hand is the dominant detected hand for this experiment.

Extraction thresholds are:

- EXTRACTION_PASS: pose coverage at least 95% and hand coverage at least 90%;
- EXTRACTION_PARTIAL: hand coverage at least 70% when the pass criteria are not met; and
- EXTRACTION_FAIL: hand coverage below 70%.

An extraction pass means there is enough landmark coverage for downstream analysis under these thresholds. It does not show biomechanical or linguistic correctness.

## Complete expected index

The detected-hand CSV omits a row when the hand is absent. The normalization stage reconstructs the expected sequence:

    332 frames × one dominant Right hand × 21 landmarks = 6,972 rows

Missing observations become explicit rows with null raw coordinates. The stage records:

- is_detected;
- is_interpolated; and
- is_unresolved.

This prevents missing detection from being mistaken for an absent frame or a zero coordinate.

## Shoulder-relative normalization

For every frame with valid shoulder landmarks:

    shoulder_midpoint = (left_shoulder_xyz + right_shoulder_xyz) / 2
    shoulder_width = EuclideanDistance(left_shoulder_xyz, right_shoulder_xyz)
    norm_axis = (raw_axis - shoulder_mid_axis) / shoulder_width

The original values remain in raw_x, raw_y, and raw_z. Derived values are stored in norm_x, norm_y, and norm_z with the frame's shoulder reference.

This reduces sensitivity to where the performer appears in the image and to apparent body scale. It does not create full viewpoint invariance. Camera angle, body rotation, occlusion, detector behavior, and MediaPipe depth convention still affect the coordinates.

## Missing-data policy

The interpolation rule permits a linear fill only when:

- the gap is internal;
- the gap contains no more than three consecutive frames; and
- valid observations exist on both sides.

The pipeline performs no leading extrapolation, trailing extrapolation, or automatic reconstruction of longer gaps.

Gap analysis is saved before interpolation.

## Smoothing

A centered three-frame rolling mean creates smooth_x, smooth_y, and smooth_z.

The smoother:

- does not overwrite normalized coordinates;
- does not bridge unresolved gaps; and
- has no causal lag because it uses neighboring frames on both sides.

This representation is intended for offline content preparation, not real-time control.

## Motion diagnostics

The analysis covers:

- wrist, landmark 0;
- thumb tip, landmark 4;
- index tip, landmark 8;
- middle tip, landmark 12;
- ring tip, landmark 16; and
- pinky tip, landmark 20.

Frame displacement is the Euclidean distance between consecutive smoothed shoulder-relative coordinates. Trajectory length is the sum of valid consecutive displacements.

An unusual transition is flagged separately for each landmark when:

    displacement > median displacement + 6 × median absolute deviation

The threshold identifies observations for comparison with the source. A flag is not an accuracy error; intentional fast motion can also cross it.

## Extraction results

Facts:

- frames processed: 332;
- pose detections: 332 of 332, or 100.00%;
- dominant right-hand detections: 312 of 332, or 93.98%;
- missing dominant-hand frames: 20;
- hand landmarks per detected frame: 21;
- pose landmarks per detected frame: 33;
- duplicate hand keys: 0;
- duplicate pose keys: 0; and
- extraction status: EXTRACTION_PASS.

Interpretation:

The reference has enough detected pose and dominant-hand frames for the defined downstream representation checks.

Limitation:

Coverage does not demonstrate accurate coordinates in every frame, correct sign performance, or professional approval.

## Missing-data results

The 20 missing dominant-hand frames form three gaps.

Gap 1:

- frames: 0 through 8;
- length: 9 frames;
- approximate duration: 300.30 milliseconds;
- type: leading; and
- decision: unresolved.

Gap 2:

- frame: 320;
- length: 1 frame;
- approximate duration: 33.37 milliseconds;
- type: internal; and
- decision: interpolated.

Gap 3:

- frames: 322 through 331;
- length: 10 frames;
- approximate duration: 333.67 milliseconds;
- type: trailing; and
- decision: unresolved.

Summary:

- gap count: 3;
- longest gap: 10 frames;
- median gap length: 9 frames;
- interpolated frames: 1; and
- unresolved frames: 19, or 5.72%.

Interpretation:

The one-frame internal gap meets the predefined rule. The edge gaps lack valid observations on both sides and remain missing by design.

Limitation:

The representation does not reconstruct movement outside the detected interval. A future renderer must preserve that uncertainty or use a separately reviewed editing decision.

## Normalization results

Facts:

- valid shoulder references: 332 of 332 frames;
- median shoulder width in MediaPipe coordinate space: 0.310152;
- shoulder-width median absolute deviation: 0.014723;
- normalized origin: shoulder midpoint;
- normalized scale: shoulder width; and
- smoothing window: 3 frames.

The normalization metadata records the raw-input hashes and states that downstream processing did not overwrite those sources.

Interpretation:

The full sequence supports a per-frame shoulder-relative transform.

Limitation:

The POC has no multi-camera or viewpoint-invariance test.

## Wrist results

For the dominant-hand wrist:

- valid consecutive transitions: 312;
- missing transitions: 19;
- median frame displacement: 0.019707 shoulder widths;
- maximum frame displacement: 0.280319 shoulder widths;
- normalized trajectory length: 11.643874 shoulder widths;
- transition threshold: 0.113406 shoulder widths;
- flagged transitions: 20; and
- flagged-transition rate: 6.41%.

Across the wrist and five fingertips, the highest flagged-transition rate is 8.01%.

Interpretation:

The stored data contains a continuous detected or interpolated interval from frames 9 through 321. Flagged regions should be compared with the source and overlay.

Limitation:

There is no marker-based motion-capture ground truth. Displacement alone cannot separate intentional rapid movement from detector instability.

## Structured quality assessment

### A. Detection coverage

Status: PASS.

Reason: pose coverage is 100.00%, hand coverage is 93.98%, and extraction is EXTRACTION_PASS.

### B. Missing-data continuity

Status: PARTIAL.

Reason: 19 frames, or 5.72%, remain unresolved.

### C. Short-gap recoverability

Status: PASS.

Reason: the only internal gap contains one frame and was interpolated under the predefined maximum.

### D. Body-relative stability

Status: PASS.

Reason: every frame has a finite positive shoulder reference.

### E. Temporal smoothness

Status: PARTIAL.

Reason: the highest flagged-transition rate across the wrist and fingertips is 8.01%.

### F. Human-inspectable correspondence

Status: PENDING_EXPERT_REVIEW.

Reason: plots and structured trajectories exist, but a qualified reviewer has not confirmed correspondence or sign correctness.

Overall motion status: MOTION_REPRESENTATION_PARTIAL.

Technical feasibility decision: Proceed with conditions.

### Tracked-pose decision rule

The connected MVP can offer the `Use tracked poses` route only when dominant-hand detection coverage is at least 90%. The versioned WATER result reaches 93.98%, so it clears that technical route threshold. `MOTION_REPRESENTATION_PARTIAL` and pending expert review still apply; clearing the coverage threshold does not approve the sign or prove correctness.

## What the POC demonstrates

- Local MediaPipe extraction can produce pose and hand records for one adult source.
- A complete expected frame and landmark index can expose missing data.
- Raw-evidence hashes can be preserved alongside derived output.
- Every pose-valid frame can be converted to a shoulder-relative coordinate system.
- Gap structure can be measured before reconstruction.
- A short internal gap can be filled under an explicit rule.
- Edge gaps can remain unresolved instead of being fabricated.
- Smoothing can be stored as a separate derivative.
- Wrist and fingertip paths, displacement, missing transitions, and transition flags can be generated for inspection.

## What the POC does not demonstrate

- Baby Sign, ASL, LSE, or other linguistic correctness;
- semantic sign recognition;
- clinical or developmental benefit;
- automatic child assessment;
- full viewpoint invariance;
- avatar generation or retargeting;
- final synthetic-video fidelity;
- generalisation across signs, performers, devices, lighting, clothing, backgrounds, or viewpoints;
- production performance; or
- product-market fit.

## Human validation checkpoint

Computer Vision can quantify and structure observed movement. It cannot decide whether the sign is professionally correct.

A qualified reviewer must compare the selected reference, plots, overlay, and any future reconstruction before the movement can support released educational content.

The automated status must remain separate from professional review, visual review, printable eligibility, publication, and school availability.

## Relationship to the current MORE MVP

The local MORE demo is separate from this POC. Its successful ignored run reports 285 frames, 100.00% pose coverage, 91.93% dominant-hand coverage, 25 missing dominant-hand frames, 4 interpolated frames, 21 unresolved frames, EXTRACTION_PASS, and MOTION_REPRESENTATION_PARTIAL.

The MORE run does not replace the versioned WATER evidence. Neither result proves cross-sign performance.

On 4 September 2026, the six POC unit tests passed. The opt-in MORE integration failed before frame processing in the current headless macOS session because MediaPipe could not create the required graphics context. The application recorded a controlled error. This runtime limitation concerns execution context, not the arithmetic already stored in the WATER evidence.

## Privacy and governance

- Processing occurs locally in this POC.
- No external AI service receives the reference video.
- The experiment uses an adult reference.
- Child video is not needed.
- The source MP4, raw landmark CSVs, normalized CSVs, and private preview video are ignored by Git.
- Versioned public evidence is limited to metadata, summary JSON, diagnostic JSON, and technical plots.
- Video and landmarks may still be personal data when linked to an identifiable performer.
- The performer and sign material require appropriate consent, provenance, and usage rights before external display or reuse.
- The landmarks are not used to identify a person.

## Separate formal low-code POC evidence

The Computer Vision feasibility artifact does not call n8n or LangSmith. Those tools have separate evidence paths and do not validate landmark extraction, movement representation, sign correctness, linguistic correctness, or professional approval.

The formal low-code POC is the governed n8n workflow. Its exact 12-node export is versioned at [workflow/kinder_signs_n8n_workflow.json](../workflow/kinder_signs_n8n_workflow.json), and [the workflow guide](../workflow/kinder_signs_n8n_workflow.md) documents it. The screenshot at [workflow/evidence/n8n_successful_execution_2026-08-31.png](../workflow/evidence/n8n_successful_execution_2026-08-31.png) evidences a successful historical execution of `Kinder Signs — Governed Family Draft (Example)` on 31 August 2026: status Succeeded, execution ID #21441, duration 14.499 seconds. Evidence status: COMPLETE AT CAPSTONE LOW-CODE POC SCOPE.

That historical execution remains a governed family-draft workflow, not autonomous publication or production deployment. It is not evidence that the later final MVP Content Pack adapter was exercised. The OpenAI course credential used then was removed or revoked shortly afterwards and is no longer available; a fresh provider-backed rerun would require a new authorised credential. This current reproducibility limit does not invalidate the historical execution.

The [LangSmith dry-run summary](../workflow/langsmith_dry_run_summary.json) separately records `DRY_RUN` with network calls false for the optional wording evaluation path. It is not a live trace and is not part of the Computer Vision processing loop.

## Next technical step

Proceed only with these conditions:

1. Obtain qualified professional review of the source and correspondence evidence.
2. Keep leading, trailing, and longer internal gaps unresolved unless a separate reviewed rule is adopted.
3. Compare every flagged transition with the reference.
4. Repeat the method across multiple reviewed signs, adult performers, viewpoints, and capture conditions.
5. Test future rendering against the structured reference before making a fidelity claim.
6. Validate a supported runtime for headless or hosted execution.

## Evidence paths

Versioned evidence:

- poc/output/validation_summary.json;
- poc/output/landmarks/sign_reference_metadata.json;
- poc/output/normalized/sign_reference_normalization_metadata.json;
- poc/output/diagnostics/sign_reference_missing_frames.json;
- poc/output/diagnostics/sign_reference_motion_displacements.json;
- poc/output/diagnostics/sign_reference_motion_summary.json;
- poc/output/diagnostics/sign_reference_detection_timeline.png;
- poc/output/diagnostics/sign_reference_wrist_trajectory.png;
- poc/output/diagnostics/sign_reference_fingertip_trajectories.png;
- assets/registry/sign_asset_registry.json;
- poc/src; and
- poc/tests.

Local ignored inputs and intermediate records:

- poc/input/sign_reference.mp4;
- poc/output/landmarks/sign_reference_hand_landmarks.csv;
- poc/output/landmarks/sign_reference_pose_landmarks.csv;
- poc/output/normalized/sign_reference_hand_normalized.csv; and
- poc/output/normalized/sign_reference_pose_normalized.csv.

## Reproduction boundary

The code and non-video evidence are versioned. A full extraction rerun also requires the authorised local WATER MP4 and the compatible MediaPipe environment.

The environment used for the locally evidenced historical measurements is poc_env with Python 3.9.6 and MediaPipe 0.10.14. The deployment dependency file `poc/requirements.txt` now pins MediaPipe 0.10.21; that pin is not the environment used for those measurements and is not evidence of a successful hosted deployment. A clean Python 3.11 or 3.12 environment remains a future rebuild target, not a result of this verification.

The POC test suite runs from the repository root with:

    poc_env/bin/python -m unittest discover -s poc/tests -v

Verified result on 4 September 2026: 6 tests passed.
