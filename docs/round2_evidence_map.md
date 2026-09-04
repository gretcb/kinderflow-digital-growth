# Round 2 evidence map

## Use Case Definition

Evidence:

- use_case_definition.md;
- feedback/round1_decision.md; and
- research/use_cases.md.

Supported claim: Kinder Signs addresses school-home continuity through a school-led B2B or B2B2C proposition. Little Steps Nursery and Cleo are pseudonymised business-case personas.

Remaining proof: nursery demand, educator adoption, family use, and willingness to pay.

## Stronger POC

Evidence:

- poc/src;
- poc/tests;
- poc/output/validation_summary.json;
- poc/output/diagnostics/sign_reference_motion_summary.json;
- poc/output/diagnostics/sign_reference_detection_timeline.png;
- poc/output/diagnostics/sign_reference_wrist_trajectory.png; and
- poc/poc_documentation.md.

Supported claim: the versioned WATER result contains 332 frames, 100.00% pose coverage, 93.98% dominant right-hand coverage, EXTRACTION_PASS, and MOTION_REPRESENTATION_PARTIAL. The method preserves raw evidence, normalizes to the shoulders, fills only short internal gaps, and exposes movement diagnostics.

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

Supported claim: the local service processes an adult reference, reports run-specific evidence, supports three human evidence routes, prepares deterministic draft visuals, and hands an exact local visual to printable or story proofs. School and family pages demonstrate browser-session behavior with synthetic data.

The successful MORE run with 285 frames is ignored local evidence. It is not part of the committed proof. On 4 September 2026, standard discovery ran 184 tests: 183 passed and one opt-in integration test was skipped. Running that integration separately failed in the headless session before frame processing because MediaPipe could not create the required graphics context.

Remaining proof: confirmed source and display rights, professional visual and sign review, completed saved-PDF quality review, a hosted runtime, real persistence, and real delivery.

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
- workflow/langsmith_dry_run_summary.json;
- workflow/evaluation_cases.json; and
- workflow/quality_gate.py.

Supported claim: the repository contains an exact inactive n8n export, a deterministic passing sample gate, five evaluation cases, and LangSmith dry-run evidence for optional LLM wording.

Remaining proof: final adapter execution in the target n8n runtime, a live external model call if retained, and a live LangSmith trace.

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

- presentation/kinder_signs_deck.pptx;
- presentation/demo_script.md;
- presentation/qa_preparation.md; and
- presentation/source_notes.md.

Supported claim: the presentation can demonstrate the local flow and bounded evidence.

Remaining proof: a desktop-session backup recording, current screenshots, and rehearsal of the failure fallback. The personalised family mini-library must remain a future step.
