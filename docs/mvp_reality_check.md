# MVP reality check

This classification is based on repository evidence on 2 September 2026. “Functional now” means executable locally, not hosted or production-ready.

## FUNCTIONAL NOW

| Capability | Evidence and boundary |
|---|---|
| Local reference-video intake | `mvp/app.py` accepts a demo reference or an uploaded MP4. Extension, empty-file and filename-safety cases are tested. |
| MediaPipe processing | The MVP calls the existing `poc/src` extraction, normalization and analysis functions. It does not duplicate the CV implementation. |
| Run isolation | Each run uses a generated ID under ignored `mvp/runs/`; upload filenames do not determine filesystem paths. |
| Landmark/skeleton preview | The pipeline writes a run-specific landmark-overlay video and browser-facing H.264 copy when ffmpeg is available. |
| Real movement metrics | Run responses contain calculated frames, pose/hand coverage, missing frames, gaps and technical status. |
| Controlled CV result states | The service distinguishes pass, review needed, insufficient coverage and processing failure. |
| POC evidence | One reference has 332 frames, 100% pose coverage, 93.98% dominant-hand coverage, 20 missing hand frames and a partial motion-representation result. |
| Flashcard Studio | Local sign selection, Spanish/English switch, three templates, A6/A5 sizing, routine/tips controls and immediate preview are implemented. |
| Browser print | Print actions call `window.print()` and print CSS isolates the selected output. This is not server-side PDF generation. |
| Structured sign source | `prototype/data/signs.json` supplies five local bilingual records for rendering/regression. It is not a professionally approved library. |
| Content-operations rules | Separate technical, content, visual and publication states are implemented in Python. Invalid status jumps are rejected. |
| Deterministic readiness checks | Required content, visual assets, hand review, technical state and explicit human approval are checked with specific blocking reasons. |
| Provenance and hashes | MORE references current local evidence and structured data; tests verify that recorded hashes match and change when a file changes. |
| Idempotent local package build | Rebuilding the same package inputs yields the same package identity and files. |
| Local audit log helper | Unique structured events can be appended; duplicate event IDs are ignored. This is not a production audit service. |
| Five-sign regression harness | MORE, EAT, WATER, ALL DONE and HELP are checked together. All schemas pass and all five are honestly blocked from publication. |
| LLM deterministic quality gate | The sample family draft can be checked locally without API keys. |
| LangSmith dry-run | The script builds the prompt, loads the sample output, runs the gate and records what would be traced without a network call. |
| n8n workflow artifact | A credential-free workflow/export and node specification exist. Import/runtime compatibility still needs verification in the target n8n installation. |

Environment note: the non-integration MVP tests pass in the existing `poc_env` with MediaPipe 0.10.14, but that environment reports Python 3.9.6. The documented target is Python 3.11/3.12, and the machine's default Python 3.13 cannot import the required legacy `mediapipe.solutions` API. A clean supported environment still needs to be reproduced.

## PROTOTYPE / LOCAL STATE

| Capability | Evidence and boundary |
|---|---|
| Human approval controls | Buttons can move a browser session through review/publication states. No reviewer identity, signature or persistent approval exists. |
| Demo publication | Prototype pages can show “Published” or “Published demo.” This is UI state, not evidence that professional approval occurred. |
| Master Content Library | The UI demonstrates scope and filtering. It is not backed by a production content database. |
| School entitlements | Example access for School A/B/C is static and uses fictional names. No permission engine exists. |
| Group/child assignment | Client-side controls show the intended hierarchy and confirmation. Nothing is sent or saved. |
| Family access | Family guidance is rendered locally. No delivery, account or live school-channel integration exists. |
| Story generation | A constrained, deterministic prototype draft illustrates generation/evaluation/HITL. It does not call a live model. |
| Content-operations admin | The readiness matrix reads generated JSON and exposes blocking reasons. Admin actions do not persist production state. |
| Publication package | A real local JSON package is built, but MORE remains draft/blocked and is not a publishable content claim. |
| Pilot event model | A machine-readable event schema and metric definitions exist, but no product instrumentation is active. |

## PLANNED / NOT YET IMPLEMENTED

| Capability | Missing evidence or work |
|---|---|
| Professionally approved reference library | Source rights, sign identity and professional suitability are not confirmed for the current local reference. |
| Final Open Peeps/character artwork | Only the asset contract/integration point exists; no final approved artwork is in the flashcard asset directory. |
| Reviewed MORE hand-pose asset | A sign-specific SVG and documented hand review are missing. |
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
