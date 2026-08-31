# Kinder Signs Technical Feasibility POC

## Business problem

Generative video may create visually plausible presenters while altering detailed sign biomechanics. KinderFlow therefore needs a motion-preservation checkpoint before any future rendering experiment.

This POC asks one bounded question:

> Can a validated sign video be converted into a stable, body-relative and temporally coherent structured motion representation suitable for future motion-preserving content production?

The experiment evaluates motion representation. It does not evaluate language, pedagogy, clinical outcomes, market demand, avatars, or synthetic video.

## Technical hypothesis

A Computer Vision pipeline can extract observed body and hand coordinates, preserve the raw evidence, transform the coordinates into a body-relative reference frame, handle only short recoverable gaps, and expose temporal behavior for inspection.

The intended benefit is not semantic understanding. The intended benefit is that observed movement becomes structured, traceable data before any future rendering stage.

## Architecture

```text
Validated adult reference
  → MediaPipe
  → raw landmarks
  → body-relative normalization
  → conservative gap handling
  → temporal diagnostics
  → human/professional review
  → future rendering
```

The stored lineage is explicit:

```text
raw → normalized → interpolated → smoothed → diagnostics
```

Raw coordinate CSVs in `poc/output/landmarks/` are treated as immutable extraction evidence. Derived coordinates are written to `poc/output/normalized/`; diagnostic evidence is written to `poc/output/diagnostics/`.

## Method

### Source and extraction

The local source is one adult reference video. MediaPipe Holistic processes each video frame and emits:

- 33 pose landmarks per detected pose frame
- 21 landmarks for each detected hand
- normalized image coordinates `x`, `y`, and `z`
- frame number and timestamp

The current evidence contains 332 processed frames. The right hand is the dominant detected hand and is the relevant hand for this experiment.

Extraction status is coverage-only:

- `EXTRACTION_PASS`: pose coverage at least 95% and hand coverage at least 90%
- `EXTRACTION_PARTIAL`: hand coverage at least 70% but the pass criteria are not met
- `EXTRACTION_FAIL`: hand coverage below 70%

An extraction pass means landmark coverage is sufficient for downstream motion analysis. It does not establish motion fidelity or sign correctness.

### Missing-data analysis

The hand CSV omits frames where no hand is detected. The pipeline reconstructs the complete expected index:

```text
332 frames × dominant Right hand × 21 landmark IDs = 6,972 rows
```

Missing observations become explicit rows with null raw coordinates. Gap analysis is saved before interpolation and classifies each run as leading, internal, or trailing.

### Body-relative normalization

For each frame with valid pose landmarks:

```text
shoulder_midpoint = (left_shoulder_xyz + right_shoulder_xyz) / 2
shoulder_width = EuclideanDistance(left_shoulder_xyz, right_shoulder_xyz)
norm_axis = (raw_axis - shoulder_mid_axis) / shoulder_width
```

Raw coordinates remain in `raw_x`, `raw_y`, and `raw_z`. Derived values are stored separately in `norm_x`, `norm_y`, and `norm_z`, with the shoulder reference used for each frame.

Body-relative normalization reduces sensitivity to performer position and apparent scale. It does not provide full viewpoint invariance.

### Conservative interpolation

The default policy permits linear interpolation only when all conditions are true:

- the gap is internal
- the gap is no more than three consecutive frames
- valid observations exist on both sides

The pipeline performs no leading extrapolation, no trailing extrapolation, and no silent filling of longer gaps. Each row records `is_detected`, `is_interpolated`, and `is_unresolved`.

### Smoothing

A centered three-frame rolling mean creates `smooth_x`, `smooth_y`, and `smooth_z`. It does not overwrite normalized values and does not bridge unresolved gaps.

Minimal smoothing reduces frame-level detector jitter while preserving temporal structure. A centered window avoids causal lag but uses neighboring frames, so this representation is intended for offline content preparation rather than real-time control.

### Motion diagnostics

Diagnostics cover the wrist and five fingertips:

| Landmark ID | Point |
|---:|---|
| 0 | Wrist |
| 4 | Thumb tip |
| 8 | Index tip |
| 12 | Middle tip |
| 16 | Ring tip |
| 20 | Pinky tip |

Frame-to-frame displacement is the Euclidean distance between consecutive smoothed body-relative coordinates. Trajectory length is the sum of valid consecutive displacements.

An abrupt jump is flagged separately for each landmark when:

```text
displacement > median displacement + 6 × median absolute deviation (MAD)
```

This robust rule exposes unusual transitions without labeling them as errors. Abrupt-jump flags are detector diagnostics, not an accuracy measure; fast intentional motion can also be flagged.

## Results

### Extraction and data shape

**FACT**

- 332 frames were processed.
- Pose landmarks were detected in 332 of 332 frames: 100.00%.
- Dominant right-hand landmarks were detected in 312 of 332 frames: 93.98%.
- Every detected hand frame contains 21 landmarks.
- Every pose frame contains 33 landmarks.
- No duplicate frame/hand/landmark or frame/pose-landmark keys were found.
- The raw extraction status is `EXTRACTION_PASS`.

**INTERPRETATION**

Landmark extraction coverage is sufficient for downstream motion analysis on this reference sequence.

**LIMITATION**

Coverage does not demonstrate that every coordinate is biomechanically accurate or that the performed sign is professionally correct.

### Missing data and recovery

**FACT**

The 20 missing hand frames form three gaps:

| Gap | Frames | Length | Approx. duration | Type | Decision |
|---|---:|---:|---:|---|---|
| 1 | 0–8 | 9 | 300.30 ms | Leading | Unresolved |
| 2 | 320 | 1 | 33.37 ms | Internal | Interpolated |
| 3 | 322–331 | 10 | 333.67 ms | Trailing | Unresolved |

- Gap count: 3
- Longest gap: 10 frames
- Median gap length: 9 frames
- Interpolated frames: 1
- Unresolved frames: 19, or 5.72% of the sequence

**INTERPRETATION**

The one-frame internal gap is recoverable under the predefined conservative rule. The leading and trailing gaps lack observations on both sides and remain missing by design.

**LIMITATION**

The representation does not reconstruct movement outside the detected interval. Future rendering must either respect the unresolved boundaries or use a separately validated capture/editing decision.

### Normalization

**FACT**

- Shoulder midpoint and shoulder width were available for all 332 frames.
- Median shoulder width in MediaPipe coordinate space: 0.310152.
- Shoulder-width MAD: 0.014723.
- Raw-coordinate SHA-256 values are recorded in the normalization metadata.
- The raw hand, pose, and metadata hashes remained unchanged during downstream processing.

**INTERPRETATION**

The reference sequence supports a complete per-frame body-relative coordinate transform. This reduces the direct effect of where the performer appears in the frame and their apparent scale.

**LIMITATION**

The coordinate system remains sensitive to camera viewpoint, body orientation, occlusion, detector behavior, and MediaPipe's depth convention.

### Temporal diagnostics

**FACT**

For the dominant-hand wrist, using centered three-frame smoothed body-relative XYZ coordinates:

- Valid consecutive transitions: 312
- Missing transitions: 19
- Median frame displacement: 0.019707 shoulder widths
- Maximum frame displacement: 0.280319 shoulder widths
- Normalized trajectory length: 11.643874 shoulder widths
- Robust abrupt-jump threshold: 0.113406 shoulder widths
- Abrupt-jump count: 20 of 312 valid transitions, or 6.41%

Across the wrist and five fingertips, the highest abrupt-transition rate is 8.01%.

**INTERPRETATION**

The sequence preserves a continuous detected-and-interpolated interval from frames 9 through 321. The robust flags identify transition regions that merit comparison with the source video; they do not determine whether the motion is correct or incorrect.

**LIMITATION**

There is no ground-truth motion-capture reference. The POC therefore cannot separate intentional rapid movement from detector instability based on displacement alone.

### Structured technical quality assessment

| Dimension | Status | Evidence-led reason |
|---|---|---|
| A. Detection coverage | PASS | `EXTRACTION_PASS`: 100.00% pose and 93.98% hand coverage |
| B. Missing-data continuity | PARTIAL | 19 frames, or 5.72%, remain unresolved |
| C. Short-gap recoverability | PASS | The only internal gap is one frame and was interpolated |
| D. Body-relative stability | PASS | A finite positive shoulder reference exists for 100% of frames |
| E. Temporal smoothness | PARTIAL | Maximum robust-flag rate across tracked landmarks is 8.01% |
| F. Human-inspectable correspondence | PENDING EXPERT REVIEW | Plots exist; professional correspondence has not been reviewed |

The automated overall status is `MOTION_REPRESENTATION_PARTIAL`. It is deliberately not collapsed into an unexplained score.

## What the POC demonstrates

- A local MediaPipe extraction can be transformed into a complete, auditable frame/hand/landmark index.
- Raw observations can be preserved alongside body-relative derived coordinates.
- Body-relative normalization can be applied for every pose-valid frame.
- Missing-data structure can be measured before interpolation.
- A short internal gap can be interpolated under a transparent, configurable rule.
- Edge gaps can remain explicitly unresolved rather than being silently fabricated.
- Minimal no-lag smoothing can be stored without overwriting normalized coordinates.
- Wrist and fingertip trajectories, displacements, missing transitions, and robust jump flags can be generated for technical and human inspection.

## What the POC does not demonstrate

- linguistic correctness
- Baby Sign, ASL, or LSE correctness
- clinical or developmental benefit
- semantic sign recognition
- full viewpoint invariance
- avatar generation
- motion retargeting
- final synthetic-video or motion-preservation fidelity
- generalization across signs, performers, cameras, lighting, clothing, or backgrounds
- product-market fit

PASS language is bounded. An extraction pass indicates that coverage meets the predefined threshold for analysis. A future motion-representation pass would indicate only that the representation meets predefined technical feasibility criteria for further experimentation.

## Human validation checkpoint

Computer Vision can quantify and structure observed movement.

It cannot determine whether the sign is professionally correct without expert review.

A qualified reviewer must compare the validated reference, diagnostic plots, and any future reconstruction before the representation can be used as a trusted motion source. Human review is an architecture stage, not a post-launch disclaimer.

## Privacy / governance

- Processing remains local.
- The reference video is not uploaded to external AI services.
- Adult reference material is used.
- Child video is not required for this feasibility experiment.
- Git excludes `poc/input/*.mp4`, `poc/input/*.mov`, raw landmark CSVs, normalized CSVs, private preview MP4s, virtual environments, macOS metadata, Python bytecode, and cache directories.
- Public evidence is limited to non-video metadata, JSON diagnostics, and technical plots that do not reconstruct a person.
- The reference performer and sign material must have appropriate consent and usage rights before any wider distribution.

## Next technical step

### Technical feasibility: Proceed with conditions

The evidence supports further controlled motion-representation experimentation, not avatar production.

Conditions:

- professional sign validation remains mandatory
- flagged transitions must be compared with the source video
- leading, trailing, and long internal gaps must not be automatically reconstructed
- the method must be tested across multiple validated signs, adult performers, capture conditions, and viewpoints
- future rendering must be evaluated against the structured reference before any fidelity claim

Avatar generation, n8n orchestration, and LangSmith evaluation are outside this closed POC and should not begin until these conditions and the human-validation checkpoint are accepted.

## Reproducibility and evidence map

Run from the repository root:

```bash
python poc/src/extract_landmarks.py --video poc/input/sign_reference.mp4
python poc/src/normalize_landmarks.py --video-name sign_reference
python poc/src/analyse_motion.py --video-name sign_reference
python -m unittest discover -s poc/tests -v
```

The extraction baseline uses MediaPipe's 0.10 legacy Solutions API. Use Python 3.11 or 3.12 and install the bounded dependency range in `poc/requirements.txt`; MediaPipe 1.x is not compatible with this unchanged extractor.

Key evidence:

- `poc/output/validation_summary.json`
- `poc/output/landmarks/sign_reference_metadata.json`
- `poc/output/normalized/sign_reference_normalization_metadata.json`
- `poc/output/diagnostics/sign_reference_missing_frames.json`
- `poc/output/diagnostics/sign_reference_motion_displacements.json`
- `poc/output/diagnostics/sign_reference_motion_summary.json`
- `poc/output/diagnostics/sign_reference_detection_timeline.png`
- `poc/output/diagnostics/sign_reference_wrist_trajectory.png`
- `poc/output/diagnostics/sign_reference_fingertip_trajectories.png`
