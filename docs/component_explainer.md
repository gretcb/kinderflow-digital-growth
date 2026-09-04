# Kinder Signs component explainer

Status terms in this document describe repository evidence. Working locally does not mean production-ready.

## Reference and Computer Vision

### Adult reference input

Purpose: supply observed movement for one sign-production run.

Current state: local MP4 upload, a bounded public direct-MP4 URL, and a registered MORE demo shortcut work through the local service. Local source media is not versioned and presentation rights still need confirmation.

Boundary: the selected sign is operator supplied. The software does not recognise or certify the sign.

### MediaPipe and movement representation

Purpose: extract hand and pose landmarks, normalize coordinates relative to the shoulders, preserve gaps conservatively, and produce inspectable diagnostics.

Current state: working locally. Versioned WATER diagnostics and ignored local MORE evidence must be reported separately.

Boundary: coverage and movement diagnostics are technical signals, not a correctness or developmental score.

### Reference review

Purpose: let an operator compare the reference video, pose preview, coverage, gaps, and movement path.

Current state: working locally with Pass, Review needed, and Fail outcomes. The routes are Use tracked poses, Choose reference frames, and Use reviewed references.

Boundary: a human route selection does not publish content.

## Visual and printable components

### Open Peeps-derived visual packages

Purpose: keep one consistent character style while making sign-specific hand, arm, and movement details reviewable.

Current state: six sign packages contain 18 versioned draft SVG options. Each sign has two initial options and one deterministic additional option. The base geometry and file hashes are registered.

Boundary: Open Peeps defines visual style only. All sign-specific mechanics need qualified review. No visual is published.

### Illustrative Gemini FX videos

Purpose: demonstrate where a short family motion preview could appear.

Current state: local pre-generated files map MORE to mas.mp4, HELP to ayuda.mp4, and MILK to leche.mp4. EAT, SLEEP, and WATER have no current file.

Boundary: these videos are not generated from the current run or landmarks. Usage rights, fidelity, and professional suitability remain unresolved.

### Flashcard and Routine Card

Purpose: turn the exact locally approved draft visual into a controlled printable proof.

Current state: working local Bilingual and Spanish previews with a dedicated A5 route and browser Print or Save as PDF.

Boundary: there is no PNG export, server PDF service, approved distributable output, or completed saved-PDF visual quality check.

### Story and Song

Story current state: deterministic local English or Spanish draft for MORE only. The page makes no live LLM, n8n, or LangSmith call.

Song current state: Coming soon and inactive.

## Content and workflow components

### Structured sign data

Purpose: separate labels, translations, routine guidance, and routing metadata from interface code.

Current state: prototype/data/signs.json has seven records. The canonical visual registry has six signs. The Content Operations regression set has five records. Each set has a different test purpose and must not be described as one catalog.

### Content Operations

Purpose: keep source, technical, content, artwork, hand review, human review, publication, and library state separate.

Current state: working local code, schemas, state transitions, hashes, audit events, and five-record regression evidence. All five records remain blocked.

### Content Pack service

Purpose: package approved human copy or an optional LLM-assisted draft under one contract and apply deterministic checks.

Current state: human, dry-run, and mocked provider-path behavior are tested. Real external LIVE generation is not evidenced.

### LangSmith

Purpose: trace and evaluate only optional LLM wording.

Current state: documented evaluation path and committed dry-run summary.

Boundary: no live external trace; no evaluation of video, MediaPipe, movement, or professional correctness.

### n8n

Purpose: describe repeatable orchestration from approved inputs to a draft awaiting professional review.

Current state: exact inactive JSON export and node documentation.

Boundary: final adapter execution in a target n8n runtime is not evidenced. The workflow cannot publish autonomously.

## Delivery components

### Content Library

Purpose: show sign and family-material readiness and, later, hold published assets.

Current state: local interface and blocked package records. The registry reports every sign as unavailable to schools.

### Little Steps Nursery assignment

Purpose: demonstrate a low-effort school workflow for selecting a sign, group, materials, and audience.

Current state: synthetic session-based behavior with duplicate control, editing, and removal.

Boundary: no production account, permission service, database, or real delivery.

### Family View

Purpose: show short guidance and selected material in family language.

Current state: basic browser prototype that can read synthetic assignment state.

Boundary: a personalised assignment-driven family mini-library, family accounts, notifications, and persistent delivery remain future work.

### Pilot measurement

Purpose: define privacy-minimised future assignment, view, print, and review events.

Current state: schema and measurement plan only. No live instrumentation or pilot results exist.
