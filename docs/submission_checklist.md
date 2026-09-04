# KinderFlow capstone submission checklist

This checklist is the final manual gate for the `release/capstone-demo` submission package. `COMPLETE` means the required artifact and bounded evidence are present at the stated scope. It does not mean commercial validation, legal certification, production readiness, or deployment.

## Round 1 evidence

| Requirement | File | Status | Manual check | Remaining action | Owner |
|---|---|---|---|---|---|
| Sector research and public data | `research/sector_research.md`; `data/source_register.csv`; `data/tableau_master.csv` | COMPLETE | Confirm citations and evidence dates remain readable. | Preserve as historical evidence. | Product Owner |
| Opportunity and risk mapping | `research/opportunities_risks.md` | COMPLETE | Confirm limitations are stated during presentation. | Preserve as historical evidence. | Product Owner |
| Three use case proposals and selection | `research/use_cases.md`; `feedback/round1_decision.md` | COMPLETE | Explain that historical KEEP differs from the current conditional decision. | Use `PROCEED WITH CONDITIONS` in current materials. | Product Owner |
| Tableau dashboard | `dashboard/tableau/Kinder Signs - Market Opportunity.twbx`; `dashboard/tableau/kinder_signs_market_opportunity.png`; `dashboard/dashboard_documentation.md` | COMPLETE | Open the packaged workbook and inspect all four worksheets and the dashboard. | Keep target position labelled as a hypothesis. | Product Owner |
| n8n low-code workflow | `workflow/kinder_signs_n8n_workflow.json`; `workflow/kinder_signs_n8n_workflow.md`; `workflow/evidence/n8n_successful_execution_2026-08-31.png` | COMPLETE AT CAPSTONE LOW-CODE POC SCOPE | Confirm the exact 12-node export and the separate screenshot showing the 31 August 2026 successful execution (`#21441`, 14.499 seconds). | Do not call it production or claim it exercised the later final MVP adapter. A fresh provider-backed rerun needs a new authorised credential. | Technical Owner |
| LangSmith monitoring sample | `workflow/langsmith_dry_run_summary.json`; `workflow/langsmith_evaluation_plan.md` | PARTIAL | Confirm the presentation says local dry-run and network calls false. | Create a live trace only if optional LLM use is enabled and permitted. | Technical Owner |
| Cost and timeline estimate | `cost_timeline/estimate.md`; `roi_risk_assessment.md` | COMPLETE | Recheck all totals against the ROI input table. | Replace estimates with actuals after validation. | Finance Owner |

## Round 2 product and decision evidence

| Requirement | File | Status | Manual check | Remaining action | Owner |
|---|---|---|---|---|---|
| Final use case and recommendation | `use_case_definition.md` | COMPLETE | Confirm Cleo, Little Steps, stakeholder roles, confidence levels, and kill criteria are clear. | Test the Low-confidence user and commercial assumptions. | Product Owner |
| Little Steps operating case | `docs/little_steps_operating_case_kpis.md` | COMPLETE | Keep the non-audited, pseudonymised disclaimer visible. | Validate time, budget ownership, and willingness to pay directly. | Product Owner |
| Computer Vision POC | `poc/poc_documentation.md`; `poc/output/validation_summary.json` | COMPLETE | Demonstrate WATER as versioned evidence and keep its metrics separate from MORE. | Reproduce representative runs in a stable supported environment. | Technical Owner |
| Connected local MVP | `mvp/mvp_documentation.md`; `mvp/`; `prototype/` | COMPLETE | Use `poc_env/bin/python mvp/app.py --port 8765` for the demonstrated route set; the application default remains 8000. | Validate a stable deployable runtime before any production claim. | Technical Owner |
| Direct video URL | `mvp/app.py`; `mvp/mvp_documentation.md` | COMPLETE at local prototype scope | Use only an authorized direct public MP4 and explain remote-host disclosure. | Add production egress, decoder, authentication, and abuse controls if retained. | Technical Owner |
| Tracked-pose and fallback choices | `mvp/pipeline.py`; `prototype/create-sign.html`; `mvp/mvp_documentation.md` | COMPLETE at local prototype scope | Explain the 90% dominant-hand coverage rule and fallback rationale. | Test with more representative, rights-cleared references. | Technical Owner and Sign Reviewer |
| Deterministic visual candidates | `prototype/data/visual_sign_packages.json`; `prototype/assets/signs/`; `assets/registry/sign_asset_registry.json` | PARTIAL | State that all 18 SVGs are drafts. | Complete qualified sign, hand, visual, and readability review. | Sign Reviewer and Visual Reviewer |
| Open Peeps provenance | `assets/flashcards/open_peeps/provenance.json`; `assets/registry/source_assets_provenance.md` | COMPLETE for the recorded style source | Confirm attribution and the style-only boundary. | Retain source evidence with every derived asset. | Rights Owner |
| Gemini FX previews | `assets/registry/source_assets_provenance.md`; `assets/registry/sign_asset_registry.json` | PARTIAL / DEMO ONLY | Show only if external-display permission is confirmed. | Close rights, fidelity, reviewer, and transparency gates for each file. | Rights Owner and Sign Reviewer |
| Flashcard and Routine Card | `prototype/flashcards.html`; `prototype/print-card.html`; `prototype/README.md` | COMPLETE at local prototype scope | Inspect bilingual and Spanish print layouts in target browsers. | Complete final saved-PDF visual and accessibility QA with approved assets. | Product Owner and Visual Reviewer |
| Story | `prototype/create-story.html`; `prototype/story.js` | COMPLETE at local prototype scope | State that the current deterministic example is limited to MORE. | Validate content value before expanding. | Content Lead |
| Song | `prototype/create-song.html`; `prototype/README.md` | FUTURE | Confirm the screen says Coming soon. | Do not claim generation or delivery. | Product Owner |
| Nursery assignment | `prototype/school.html`; `prototype/school.js` | COMPLETE at local/session MVP scope | Demonstrate group or fictional-child selection and the exact duplicate message: “This exact sign, audience and material combination is already active.” | Add real identity, authorisation, durable persistence, and tenancy only after pilot design. | Product Owner and Technical Owner |
| Family Experience | `prototype/family.html`; `prototype/school.js` | COMPLETE at local/session MVP scope | Confirm Family View reads browser/session assignment state and displays the corresponding sign and materials. | Keep records synthetic; there is no real notification or account delivery. | Product Owner |
| Assignment-driven family mini-library | `prototype/family.html`; `prototype/school.js`; `prototype/tests/test_final_product_ux.py` | IMPLEMENTED AT LOCAL / SESSION-BASED MVP SCOPE | Demonstrate assignment filtering without claiming real family identity or cross-device continuity. | Production still needs accounts, authentication, authorisation, durable and cross-device persistence, notifications, tenant isolation, correction/deletion, and external integrations. | Product Owner and Technical Owner |
| Content Operations and publication gates | `content_ops/`; `docs/kinder_signs_content_operations_architecture.md` | COMPLETE at local governance scope | Confirm no current sign is production-published. | Reconcile the five-sign content package with the six-sign asset registry and add authenticated approvals. | Content Operations Owner |
| Automated tests | `content_ops/tests/`; `mvp/tests/`; `poc/tests/`; `prototype/tests/`; `tools/tests/` | COMPLETE for standard local suites | Record the final command results and the one expected skip. | Stabilize the explicit MediaPipe integration environment. | Technical Owner |

## Business, pilot, and compliance

| Requirement | File | Status | Manual check | Remaining action | Owner |
|---|---|---|---|---|---|
| Low, Base, and High ROI scenarios | `roi_risk_assessment.md`; `presentation/roi_slide_inputs.md` | COMPLETE as calculated scenarios | Check assumptions, 12-month results, 36-month results, and formulas together. | Replace price, centre count, retention, and cost assumptions with evidence. | Finance Owner |
| Break-even and affordability | `roi_risk_assessment.md`; `docs/little_steps_operating_case_kpis.md` | COMPLETE as calculated scenarios | Keep provider economics separate from nursery time-value estimates. | Validate contracts, cash timing, and budget ownership. | Finance Owner |
| Risk register and controls | `roi_risk_assessment.md`; `docs/facts_risk.md` | COMPLETE | Confirm the top three and all stop gates have named owners. | Close content, rights, privacy, security, and adoption gates before live use. | Product Owner |
| Pilot scope and cost | `strategic_plan.md`; `cost_timeline/estimate.md`; `docs/kinder_signs_pilot_measurement.md` | COMPLETE as proposal | Use 8-9 weeks total, about 3-4 weeks controlled testing, 2-3 centres, 3-5 signs, and EUR 5.5k-EUR 17.3k. | Obtain owner approval and freeze targets before starting. | Product Owner |
| Pilot metrics and GO, ITERATE, STOP | `docs/kinder_signs_pilot_measurement.md`; `strategic_plan.md` | COMPLETE as measurement plan | Confirm event definitions, thresholds, and decision rules before collection. | Run only after data and rights gates are signed off. | Product Owner and Measurement Owner |
| EU AI Act assessment | `compliance/eu_ai_act_compliance.md` | COMPLETE as preliminary internal assessment | Confirm final intended purpose and excluded child-decision functions. | Reassess material scope, model, or actor changes with qualified advice. | Compliance Owner |
| Conformity summary and technical outline | `compliance/eu_ai_act_compliance.md` | COMPLETE at documentation scope | Confirm no formal conformity assessment or certification is claimed. | Complete production records only if the final classification and deployment require them. | Compliance Owner |
| GDPR flows, RoPA, legal basis, retention, recipients, transfers, rights, and short DPIA | `compliance/gdpr_documentation.md` | COMPLETE as working assessment | Review the actual pilot design, roles, notices, vendors, and deletion procedure. | Obtain qualified sign-off before real personal data enters the pilot. | Privacy Owner |
| Responsible AI audit | `docs/audits/responsible_ai_audit.md` | COMPLETE at current evidence scope | Check open controls and complaints/correction route. | Re-audit after the pilot design or any new AI component. | Responsible AI Owner |
| Green AI audit | `docs/audits/green_ai_audit.md` | COMPLETE at current evidence scope | State that energy and carbon are unmeasured. | Instrument future runs before making an environmental claim. | Technical Owner |
| Asset and reference rights | `assets/registry/sign_asset_registry.json`; `assets/registry/source_assets_provenance.md` | PARTIAL | Check each intended display, processing, adaptation, print, and distribution use. | Obtain explicit written permission for unresolved sources and Gemini outputs. | Rights Owner |
| Production deployment | `strategic_plan.md`; `docs/capstone_requirement_matrix.md` | OPTIONAL / PENDING | Do not imply a hosted or production service exists. | Decide only after controlled pilot evidence and readiness gates. | Product Owner and Technical Owner |

## Presentation and submission package

| Requirement | File | Status | Manual check | Remaining action | Owner |
|---|---|---|---|---|---|
| Ten-part final story inputs | `presentation/documentation_handoff.md`; `presentation/source_notes.md` | COMPLETE as documentation record | Check every retained presentation claim against its evidence and limitation. | Keep the record aligned with future evidence changes. | Presenter |
| ROI slide inputs | `presentation/roi_slide_inputs.md` | COMPLETE | Recalculate or cross-check every displayed number. | Keep assumptions visible on the slide or in backup. | Presenter and Finance Owner |
| POC and MVP demo script | `presentation/demo_script.md` | COMPLETE | Confirm it preserves the formal n8n POC, separate CV evidence, canonical routes, and product boundaries. | Retain as the reproducibility and fallback record. | Presenter and Technical Owner |
| Presentation Q&A | `presentation/qa_preparation.md` | COMPLETE | Confirm answers do not broaden the evidence claims. | Update only if product evidence or pilot decisions change. | Presenter |
| Final presentation | `presentation.pptx` | COMPLETE as delivered artifact | Confirm the file remains a readable PowerPoint ZIP package. | Do not infer a new slide-by-slide visual QA from package validation alone. | Presenter |
| Historical PowerPoint deck | `presentation/kinder_signs_deck.pptx` | PRESERVED | Keep as historical/versioned presentation evidence. | Do not replace or delete it. | Presenter |
| Final demo recording | `presentation/kinderflow_demo.mp4`; `presentation/demo_script.md` | COMPLETE as present artifact | Metadata confirms 4:04.450 H.264 video at 1906x988 with no audio stream. | File validation is not visual end-to-end QA; record that only if performed. | Presenter and Technical Owner |
| Saved-PDF visual QA | `prototype/print-card.html`; `docs/manual_qa_checklist.md` | PARTIAL / MANUAL QA PENDING | Inspect target browser, paper sizes, clipping, contrast, and text. | Retain an approved QA record after rights-cleared assets are available. | Visual Reviewer |
| Executive README and navigation | `README.md` | COMPLETE after reconciliation | Read the first screen as a decision-maker and test all links. | Keep it aligned if evidence or pilot decisions change. | Product Owner |
| Claims and requirement control | `docs/final_claims_matrix.md`; `docs/capstone_requirement_matrix.md` | COMPLETE | Compare presentation language with permitted and prohibited wording. | Reconcile again after any implementation change. | Product Owner |

## Submission decision

The documentation supports **PROCEED WITH CONDITIONS** into pilot readiness and a controlled service test. It does not support an unconditional live pilot, full launch, product-market-fit claim, compliance certification, production publication, or production deployment.

The presentation and final recording are present, and the assignment-driven Family Experience exists at local/session MVP scope. Remaining production and pilot blockers are rights confirmation, qualified sign and visual approval, saved-PDF visual QA, real identity and access controls, durable cross-device persistence, delivery and notification design, correction/deletion workflows, tenant isolation, and pilot privacy and security sign-off.
