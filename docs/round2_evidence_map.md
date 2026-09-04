# Round 2 evidence map

## Use Case Definition

Evidence:

- use_case_definition.md;
- feedback/round1_decision.md; and
- research/use_cases.md.

Supported claim: Kinder Signs addresses school-home continuity through a school-led B2B or B2B2C proposition. Little Steps Nursery and Cleo are pseudonymised business-case personas.

Remaining proof: nursery demand, educator adoption, family use, and willingness to pay.

## Computer Vision technical POC

Evidence:

- poc/src;
- poc/tests;
- poc/output/validation_summary.json;
- poc/output/diagnostics/sign_reference_motion_summary.json;
- poc/output/diagnostics/sign_reference_detection_timeline.png;
- poc/output/diagnostics/sign_reference_wrist_trajectory.png; and
- poc/poc_documentation.md.

Supported claim: the versioned WATER result contains 332 frames, 100.00% pose coverage, 93.98% dominant-hand coverage, 20 missing dominant-hand frames, one interpolated frame, 19 unresolved frames, `EXTRACTION_PASS`, and `MOTION_REPRESENTATION_PARTIAL`. The method preserves raw evidence, normalizes to the shoulders, fills only short internal gaps, and exposes movement diagnostics.

Remaining proof: professional correspondence review and repeat tests across more signs, performers, viewpoints, and capture conditions.

## Working MVP

Evidence:

- mvp/app.py and mvp/pipeline.py;
- prototype/create-sign.html and prototype/create-sign.js;
- prototype/flashcards.html and prototype/flashcards.js;
- prototype/print-card.html and prototype/print-card.js;
- prototype/create-story.html and prototype/story.js;
- prototype/school.html and prototype/school.js;
- prototype/family.html and prototype/app.js;
- assets/registry/sign_asset_registry.json; and
- the standard test suites.

Supported claim: the local service processes an adult reference, reports run-specific evidence, supports three human evidence routes, prepares deterministic draft visuals, and hands an exact local visual to printable or story proofs. School Admin stores a synthetic assignment in browser/session state; Family View reads it and displays the corresponding sign and materials. Exact duplicate assignments are blocked.

The connected MORE demonstration is local evidence: 285 frames, 100.00% pose coverage, 91.93% dominant-hand coverage, 25 missing dominant-hand frames, four interpolated frames, 21 unresolved frames, `EXTRACTION_PASS`, and `MOTION_REPRESENTATION_PARTIAL`. It is separate from the committed WATER proof. On 4 September 2026, standard discovery ran 184 tests: 183 passed and one opt-in integration test was skipped. Running that integration separately failed in the headless session before frame processing because MediaPipe could not create the required graphics context.

The application default remains port 8000. The final demonstrated command and routes use port 8765:

- `poc_env/bin/python mvp/app.py --port 8765`;
- `http://127.0.0.1:8765/index.html`;
- `http://127.0.0.1:8765/kinder-signs.html`;
- `http://127.0.0.1:8765/create-sign.html`;
- `http://127.0.0.1:8765/school.html?sign=more&focus=share`; and
- `http://127.0.0.1:8765/family.html`.

Remaining proof: confirmed source and display rights, professional visual and sign review, completed saved-PDF quality review, a hosted runtime, real family and school identities, authentication and authorisation, durable cross-session and cross-device persistence, notifications and delivery, tenant isolation, production correction/deletion workflows, and external nursery-platform integration.

## Visual assets

Evidence:

- assets/registry/sign_asset_registry.json;
- assets/registry/sign_asset_inventory.md;
- assets/registry/source_assets_provenance.md; and
- prototype/data/visual_sign_packages.json.

Supported claim: six signs have 18 deterministic Open Peeps-derived draft options. No sign has a reviewed static visual, distributable printable, publication approval, or school availability.

Remaining proof: qualified hand-pose and visual review, rights closure, and release approval.

## Content Operations

Evidence:

- content_ops;
- content_ops/reports/golden_set_report.json; and
- build/publication/more/v1.

Supported claim: a separate five-record set tests state, wording, provenance, deterministic gates, and package identity. All five records remain blocked.

Remaining proof: a qualified review operation and an approved publication package.

## Workflow and observability

Evidence:

- workflow/kinder_signs_n8n_workflow.json;
- workflow/kinder_signs_n8n_workflow.md;
- workflow/evidence/n8n_successful_execution_2026-08-31.png;
- workflow/langsmith_dry_run_summary.json;
- workflow/evaluation_cases.json; and
- workflow/quality_gate.py.

Supported claim: the repository contains the exact inactive 12-node export for **Kinder Signs — Governed Family Draft (Example)**. A separate screenshot evidences a real successful historical execution on 31 August 2026 at 21:30:27, lasting 14.499 seconds, as execution `#21441`, with the successful governed path visible. This is **COMPLETE AT CAPSTONE LOW-CODE POC SCOPE**.

Boundary: the workflow remains a governed draft path, not autonomous publication or production deployment. The screenshot does not prove that the later final MVP Content Pack adapter ran. The OpenAI course credential used then was removed or revoked and is no longer available; a fresh provider-backed rerun requires a new authorised credential. Never reconstruct, expose, or commit the former key.

LangSmith remains separate. The committed evidence is a network-free dry-run, not a live trace. It does not validate hand movement, MediaPipe output, sign or linguistic correctness, or professional approval.

## Tableau decision support

Evidence:

- dashboard/tableau/Kinder Signs - Market Opportunity.twbx;
- dashboard/tableau/kinder_signs_market_opportunity.png;
- dashboard/dashboard_documentation.md;
- data/tableau_master.csv;
- data/competitive_positioning.csv; and
- data/source_register.csv.

Supported claim: a packaged Tableau workbook presents four decision views for institutional access, Madrid digital readiness, adult age-cohort GenAI proxies, and competitor positioning. Kinder Signs is a target-position hypothesis.

Remaining proof: primary market interviews, demand, willingness to pay, educator adoption, and commercial results.

## ROI, risk, and pilot

Evidence:

- roi_risk_assessment.md;
- cost_timeline/estimate.md;
- strategic_plan.md;
- docs/kinder_signs_pilot_measurement.md; and
- content_ops/contracts/pilot_event_schema.json.

Supported claim: an 8 to 9 week validation programme and a EUR 5.5k-EUR 17.3k planning range are documented. They are estimates, not measured returns.

Remaining proof: agreed thresholds, staff-time baselines, price interviews, partner commitment, reviewer capacity, family engagement, and paid-continuation evidence.

## Compliance and responsible AI

Evidence:

- compliance/eu_ai_act_compliance.md;
- compliance/gdpr_documentation.md;
- docs/audits/responsible_ai_audit.md;
- docs/audits/green_ai_audit.md; and
- content_ops/contracts/ai_responsibility_matrix.json.

Supported claim: the design excludes child assessment, emotion recognition, biometric identity, and autonomous publication. It minimises personal data in the current prototype and assigns professional decisions to people.

Remaining proof: final controller and processor roles, contracts, retention rules, notices, security controls, reviewer procedure, AI literacy, and legal review before a real pilot.

## Presentation evidence

Evidence:

- presentation.pptx;
- presentation/kinderflow_demo.mp4;
- presentation/kinder_signs_deck.pptx (preserved historical deck);
- presentation/demo_script.md;
- presentation/qa_preparation.md; and
- presentation/source_notes.md.

Supported claim: the final presentation file is present at the repository root and the presentation has been delivered. The final demo recording is present under `presentation/` and was used/prepared for the final presentation. The older deck remains preserved as historical/versioned presentation evidence.

Boundary: readable-package and video-metadata validation are not visual end-to-end review. Do not claim that review unless it was actually performed. The assignment-driven family mini-library is implemented at local/session MVP scope; production identities, accounts, authentication, authorisation, durable cross-device state, real notifications and delivery, tenant isolation, correction/deletion workflows, and integrations remain future work.
