# KinderFlow Create a Sign MVP

## Why this capability matters

KinderFlow converts validated reference material into a structured, reusable digital content asset. Central content production means each school does not need to manage Computer Vision, create sign assets or repeat the same production process.

A published sign is the governed upstream source for video guidance, deterministic flashcards and future derivative content. The architecture deliberately separates technical movement processing from human content approval. This supports a scalable B2B content-distribution model while limiting unnecessary operational complexity for schools.

The asset-reuse logic is:

**Validated reference → movement representation → human-controlled publication → reusable library asset → school entitlement → downstream content**

No financial savings or customer demand are inferred from this technical workflow.

## Product and governance principle

> The character defines the look. The validated reference movement defines the sign.

Computer Vision preserves and represents observed movement. It does not invent the sign and does not automatically certify linguistic correctness. A reviewer controls publication.

No child video is required. The service processes validated adult reference material locally and does not send it to an external service.

The bundled local demo path is technical fallback evidence. Its source rights, sign identity and external-presentation permission must be confirmed before it is treated as a publishable asset. A production pilot should use owned or appropriately licensed validated adult reference material with explicit provenance.

## Functional architecture

~~~text
Browser
  → local Python HTTP service
  → existing poc/src extraction, normalization and analysis functions
  → isolated mvp/runs/<run_id>/ artifacts
  → run-specific JSON response
  → reference / landmark preview + technical summary
  → local movement review
  → Content Pack generation and deterministic checks
  → local content review
  → Flashcard Studio proof
~~~

Each run stores:

- a generated run identifier;
- sign name, routine/context and controlled reference status;
- a sanitized source filename for provenance;
- input video metadata;
- stage state and measured processing duration;
- raw and normalized landmarks;
- motion diagnostics and plots; and
- the MediaPipe landmark-overlay preview.

The overlay written by OpenCV is an intermediate MPEG-4 Part 2 (mp4v) file. A post-processing step uses local ffmpeg to produce the browser-facing H.264 (avc1) MP4 with yuv420p pixel format and fast-start metadata. This changes delivery encoding only; it does not rerun or alter MediaPipe landmark extraction.

Raw local paths and tracebacks are not exposed in the UI. The *mvp/runs/* directory is ignored by Git.

## Technical and content status

Technical status is mapped conservatively from the existing POC:

- **Pass:** EXTRACTION_PASS plus PASS across automated quality dimensions A–E.
- **Review needed:** usable extraction with no automated failure, but one or more PARTIAL dimensions.
- **Fail:** EXTRACTION_FAIL, MOTION_REPRESENTATION_FAIL, or any FAIL across dimensions A–E.

Content status is separate:

- Draft;
- Ready for human review; and
- Approved locally for the limited prototype handoff.

Computer Vision never sets **Published**.

The local Content Pack service supports human source copy and LLM-assisted copy. It uses one strict input/output contract for all five signs, records isolated run metadata, and keeps deterministic checks separate from optional LangSmith tracing. Missing provider credentials produce an explicit `DRY_RUN`; human copy records LangSmith as `NOT_APPLICABLE`. Local content approval does not publish a library item, and unreviewed output cannot populate the Flashcard Studio handoff.

Pass exposes **Approve**. Review needed exposes **Approve anyway** and **Use another reference video**, with reasons shown in plain language. Fail exposes only **Use another reference video**.

## What the MVP proves

- A local reference MP4 can be accepted and validated.
- The existing MediaPipe pipeline can extract pose and hand landmarks from that run.
- Body-relative normalization and conservative gap handling can run without overwriting canonical evidence.
- Real technical coverage, missing-data and motion metrics can be surfaced in plain language.
- An operator can compare the reference with its generated landmark overlay.
- The result can be routed to an explicit human-review gate.
- Locally reviewed content can pass bounded sign, routine and family wording to the existing Flashcard Studio proof.

## What the MVP does not prove

- linguistic sign correctness;
- Baby Sign, ASL or LSE correctness;
- product-market fit or willingness-to-pay;
- production avatar generation or rendering fidelity;
- fully automated or audited publishing;
- production scalability, concurrency or cloud operations;
- security controls required for a hosted production service; or
- commercial performance across multiple schools.

## Error and safety model

The UI gives controlled messages for unsupported extensions, unreadable videos, insufficient landmark coverage and processing failure. Technical errors remain in the local run directory. Filenames are reduced to display-only provenance and never determine run paths. A generated identifier isolates every run, and processing is serialized to protect the legacy MediaPipe runtime during a live demo.

Capture guidance—visible hands, upper body, stable camera, good lighting and minimal obstruction—concerns technical capture quality only. It is not instruction about sign correctness.

## Operational and commercial limitations

The run store is local and has no retention policy, authentication, reviewer identity or production audit trail. These controls are required before deployment. Evidence currently comes from one known adult reference; broader testing across signs, performers, capture conditions and devices remains necessary. School entitlement and downstream distribution are represented elsewhere in the prototype and are not executed by this service.

The current MediaPipe 0.10 Holistic runtime on macOS requires access to a graphics context even though inference uses the CPU delegate. It works in a normal local desktop session, but headless CI or a locked-down service environment may fail before frame processing. A production deployment needs a validated container/runtime strategy rather than assuming this desktop runtime will scale unchanged.
