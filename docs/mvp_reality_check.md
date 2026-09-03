# MVP reality check

This classification is based on repository evidence on 3 September 2026. “Functional now” means executable locally, not hosted or production-ready.

## FUNCTIONAL NOW

| Capability | Evidence and boundary |
|---|---|
| Local reference-video intake | `mvp/app.py` accepts the registered MORE demo shortcut, an uploaded MP4, or a public direct MP4 URL. Upload safety plus URL scheme, credentials, DNS/address, redirects, timeout, MIME, byte cap, generated filename, cleanup and provenance-redaction cases are tested. This remains a local control rather than a production fetch service. |
| MediaPipe processing | The MVP calls the existing `poc/src` extraction, normalization and analysis functions. It does not duplicate the CV implementation. |
| Run isolation | Each run uses a generated ID under ignored `mvp/runs/`; upload filenames do not determine filesystem paths. |
| Landmark/skeleton preview | The pipeline writes a run-specific landmark-overlay video and browser-facing H.264 copy when ffmpeg is available. |
| Real movement metrics | Run responses contain calculated frames, pose/hand coverage, missing frames, gaps and technical status. |
| Controlled CV result states | The service distinguishes pass, review needed, insufficient coverage and processing failure. |
| POC evidence | The current app demo is the registered MORE reference. The committed Round 1 WATER run remains supporting evidence with 332 frames, 100% pose coverage, 93.98% dominant-hand coverage, 20 missing hand frames and a partial motion-representation result. |
| Grounded visual review | MORE, HELP, EAT, SLEEP, MILK and WATER use the unchanged registered Open Peeps bust as the sole character base and a shared upper-limb grammar. Sign mechanics come from each sign’s functional reference and curated knowledge; video/frame/landmark data is supporting geometry. Human review controls printable-proof readiness. |
| Sign-aware EAT fallback | The observed EAT run remains reviewable at 76.57% hand coverage and explicitly routes to knowledge/sign-reference fallback with a required operator rationale. It is not sign certification. |
| Separate illustrative motion demo | After pose approval, the local UI can stream hash-verified registered Google Labs FX / Gemini FX outputs for MORE, HELP and MILK. The service exposes safe sign routes rather than filesystem paths. EAT, SLEEP and WATER fail closed to an honest unavailable state, and the preview never replaces current-run evidence or blocks visual preparation. |
| Flashcard Studio | Internal KinderFlow tool with English/Spanish output, distinct Flashcard and Routine Card layouts, deterministic preview and human-controlled local proof approval. Routine guidance occupies its own row. |
| Browser print | The builder opens a dedicated A5 portrait route. That route validates the exact local approval, waits for images, renders one card and then enables Print / Save as PDF. Final saved-PDF visual QA remains pending. No PNG action is exposed. |
| Structured sign source | `prototype/data/signs.json` supplies five local bilingual records for rendering/regression. It is not a professionally approved library. |
| Content-operations rules | Separate technical, content, visual and publication states are implemented in Python. Invalid status jumps are rejected. |
| Deterministic readiness checks | Required content, visual assets, hand review, technical state and explicit human approval are checked with specific blocking reasons. |
| Provenance and hashes | The canonical six-sign registry separates each reference, output and evidence asset by sign; WATER owns the committed demo diagnostics. Content Operations separately verifies that its MORE package hashes match and change when an input changes. |
| Idempotent local package build | Rebuilding the same package inputs yields the same package identity and files. |
| Local audit log helper | Unique structured events can be appended; duplicate event IDs are ignored. This is not a production audit service. |
| Five-sign regression harness | MORE, EAT, WATER, ALL DONE and HELP are checked together. All schemas pass and all five are honestly blocked from publication. |
| LLM deterministic quality gate | The sample family draft can be checked locally without API keys. |
| LangSmith dry-run | The script builds the prompt, loads the sample output, runs the gate and records what would be traced without a network call. |
| n8n workflow artifact | A credential-free workflow/export and node specification exist. Import/runtime compatibility still needs verification in the target n8n installation. |

Environment note: the validated local prototype uses the existing `poc_env` with Python 3.9.6 and MediaPipe 0.10.14. Do not upgrade or substitute the machine's default environment for this checkpoint.

## PROTOTYPE / LOCAL STATE

| Capability | Evidence and boundary |
|---|---|
| Human approval controls | Buttons can record a local browser proof-approval state. A logical publication gate exists in Content Operations, but no reviewer identity, signature or persistent production approval exists. |
| Demo publication | A local publication package and UI concepts exist, but MORE remains Draft/Blocked. No current sign is evidenced as published or available to schools. |
| Master Content Library | The UI demonstrates scope and filtering. It is not backed by a production content database. |
| School plan | The Little Steps Nursery workspace uses synthetic family records and session-only assignments. No permission engine or production persistence exists. |
| Group/child assignment | Client-side controls show the intended hierarchy and confirmation. Demo assignments are saved only in browser session storage; nothing is sent or persisted to a backend. |
| Family access | Family guidance is rendered locally. No delivery, account or live school-channel integration exists. |
| Story generation | A constrained, deterministic prototype draft illustrates generation/evaluation/HITL. It does not call a live model. |
| Content-operations admin | The readiness matrix reads generated JSON and exposes blocking reasons. Admin actions do not persist production state. |
| Publication package | A real local JSON package is built, but MORE remains draft/blocked and is not a publishable content claim. |
| Pilot event model | A machine-readable event schema and metric definitions exist, but no product instrumentation is active. |

## PLANNED / NOT YET IMPLEMENTED

| Capability | Missing evidence or work |
|---|---|
| Professionally approved reference library | Source rights, sign identity and professional suitability are not confirmed for the current local reference. |
| Approved illustrative-motion rights and fidelity | The three registered Gemini FX demonstration files are pre-generated and separate from the current reference run. Display/redistribution permission, landmark-driven provenance, motion fidelity and qualified human approval are not established. |
| Production-approved sign artwork | Source-grounded Open Peeps-derived vectors exist for all six canonical visual signs, but every option remains a draft requiring qualified human review; none is professionally certified or published by this implementation. |
| Professional hand-pose review | Candidate review is operator-controlled local state; professional sign-language review evidence remains outside this prototype. |
| Production avatar | No validated retargeting, generation or movement-fidelity result exists. |
| Live LangSmith evaluation | The repository proves dry-run behaviour, not a captured live trace. |
| Executed content-ops n8n adapter | The contract is documented; target-runtime execution evidence is missing. |
| Production publishing | No database, authenticated reviewer, immutable approval record, rollback or release service exists. |
| Authentication and permissions | Not implemented. |
| Cloud storage and retention controls | Not implemented. Local run artifacts have no production retention policy. |
| Production analytics | Not implemented. Dashboard/prototype figures are market or illustrative evidence, not live product telemetry. |
| Real integrations | No school communication, payment or external content integrations are implemented. |
| Live pilot | No educator/family behaviour, willingness-to-pay, retention or operational-cost results exist. |
| Production scale and security | Concurrency, hosted MediaPipe runtime, threat modelling, backup and incident controls are not validated. |
