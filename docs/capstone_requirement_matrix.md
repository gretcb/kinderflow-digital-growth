# KinderFlow capstone requirement matrix

Statuses reflect the reconciled documentation package. `COMPLETE` means the required artifact and evidence are present at the stated scope. It does not mean commercial validation, legal certification or production deployment.

## Round 1 requirements

| Requirement | Status | Exact repository evidence | Current limitation | Final action |
|---|---|---|---|---|
| Sector research and public data | COMPLETE | `research/sector_research.md`; `data/source_register.csv`; `data/tableau_master.csv` | Public context does not prove KinderFlow demand. | Preserve evidence labels and limitations. |
| Opportunity and risk mapping | COMPLETE | `research/opportunities_risks.md` | Historical Round 1 scope and terminology remain visible. | Use current conclusions in final decision documents. |
| Two or three use case proposals | COMPLETE | `research/use_cases.md` | Scoring is consulting analysis, not observed performance. | Preserve three-use-case comparison and selected use case. |
| Stakeholder-focused BI dashboard | COMPLETE | `dashboard/tableau/Kinder Signs - Market Opportunity.twbx`; `dashboard/tableau/kinder_signs_market_opportunity.png`; `dashboard/dashboard_documentation.md` | Static Round 1 decision artifact, not production BI. | Retain source and hypothesis labels. |
| n8n or similar POC | COMPLETE AT CAPSTONE LOW-CODE POC SCOPE | Exact 12-node export: `workflow/kinder_signs_n8n_workflow.json`; specification: `workflow/kinder_signs_n8n_workflow.md`; historical execution: `workflow/evidence/n8n_successful_execution_2026-08-31.png` | The 31 August 2026 execution (`#21441`, 14.499 seconds) is not production deployment or proof of the later MVP Content Pack adapter. The former OpenAI course credential is unavailable. | Use a new authorised credential only if a fresh provider-backed reproducibility or adapter run is needed. |
| LangSmith monitoring sample | PARTIAL | `workflow/langsmith_eval.py`; `workflow/langsmith_evaluation_plan.md`; `workflow/langsmith_dry_run_summary.json`; `workflow/evaluation_cases.json` | Dry-run only; no live external trace. | Run only if the optional LLM path is enabled and permitted. |
| Cost and timeline estimate | COMPLETE | `cost_timeline/estimate.md`; `roi_risk_assessment.md` | Estimate, not approved spend. Production build is TBD. | Replace pilot estimates with actuals after the pilot. |
| Round 1 feedback and KEEP or CHANGE decision | COMPLETE | `feedback/round1_decision.md` | KEEP is historical and does not equal a launch decision. | Preserve history and use `PROCEED WITH CONDITIONS` for the current decision. |

## Round 2 requirements

| Requirement | Status | Exact repository evidence | Current limitation | Final action |
|---|---|---|---|---|
| Use case definition | COMPLETE | `use_case_definition.md` | User and commercial validation remain low or unproven. | Test the stated jobs, targets and stop rules. |
| No-code or low-code POC with demo evidence | COMPLETE AT CAPSTONE LOW-CODE POC SCOPE | `workflow/kinder_signs_n8n_workflow.json`; `workflow/kinder_signs_n8n_workflow.md`; `workflow/evidence/n8n_successful_execution_2026-08-31.png` | Exact export and successful historical execution are evidenced separately; this is a governed draft workflow, not autonomous publication or production deployment. | Preserve the export and screenshot; do not imply that the historical run executed the later final MVP integration. |
| Working MVP with core AI capability running | COMPLETE | `mvp/`; `prototype/`; `poc/`; `content_ops/tests/`; `mvp/tests/`; `poc/tests/`; `prototype/tests/`; `tools/tests/` | Current service is local; the explicit headless integration rerun failed on macOS graphics-context creation. | Use the evidenced desktop environment or validate a deployable runtime. |
| ROI and risk assessment | COMPLETE | `roi_risk_assessment.md` | Results are scenarios, not forecasts. | Replace variables with pilot evidence. |
| 12-month ROI | COMPLETE | `roi_risk_assessment.md`; `presentation/roi_slide_inputs.md` | Every scenario is negative at 12 months under the selected assumptions. | Validate price, conversion and costs. |
| 36-month ROI | COMPLETE | `roi_risk_assessment.md`; `presentation/roi_slide_inputs.md` | Base and High depend on customer growth and retention assumptions. | Measure paid continuation and churn. |
| Break-even | COMPLETE | `roi_risk_assessment.md`; `presentation/roi_slide_inputs.md` | Timing assumes even monthly recognition and the stated annual school counts. | Recalculate from actual contracts and cash timing. |
| EU AI Act assessment | COMPLETE | `compliance/eu_ai_act_compliance.md` | Preliminary intended-purpose assessment, not legal advice or certification. | Confirm the final pilot design and roles. |
| Conformity Assessment Summary | COMPLETE | `compliance/eu_ai_act_compliance.md` | No formal high-risk conformity assessment is claimed. | Maintain an internal evidence pack and reassess changes. |
| Technical Documentation Outline | COMPLETE | `compliance/eu_ai_act_compliance.md` | Production operating records do not yet exist. | Complete the outline before deployment. |
| GDPR data-flow map | COMPLETE | `compliance/gdpr_documentation.md` | Future pilot flow depends on final delivery design. | Approve the actual flow before real data enters it. |
| Processing-activities register | COMPLETE | `compliance/gdpr_documentation.md` | RoPA entries are working proposals. | Confirm controller/processor roles and lawful bases. |
| Legal-basis analysis | COMPLETE | `compliance/gdpr_documentation.md` | Lawful basis is purpose and role specific and remains a pilot decision. | Obtain qualified review and record the basis before processing. |
| Retention | COMPLETE | `compliance/gdpr_documentation.md` | Current ignored local runs have no enforced production schedule. | Implement tested deletion and backup rules. |
| Recipients | COMPLETE | `compliance/gdpr_documentation.md` | Vendors and recipients depend on the final architecture. | Complete processor and recipient register. |
| Short DPIA | COMPLETE | `compliance/gdpr_documentation.md` | Screening document only, not an approved production DPIA. | Complete and sign off the pilot DPIA. |
| Data-subject rights | COMPLETE | `compliance/gdpr_documentation.md` | No production identity, request or deletion workflow exists. | Test access, correction, objection and deletion handling. |
| Third-party and transfer analysis | COMPLETE | `compliance/gdpr_documentation.md` | Live vendors, regions and transfer tools are not selected. | Complete due diligence before vendor use. |
| Strategic POC to pilot to deployment plan | COMPLETE | `strategic_plan.md`; `cost_timeline/estimate.md` | Full deployment is conditional, not recommended now. | Run readiness and pilot gates before a deployment decision. |
| GTM | COMPLETE | `strategic_plan.md` | Channel and conversion assumptions are untested. | Begin with 2-3 controlled nursery partners. |
| Buyer | COMPLETE | `use_case_definition.md`; `docs/little_steps_operating_case_kpis.md` | Cleo is a pseudonymised archetype, not evidence of a signed buyer. | Validate budget ownership in each pilot centre. |
| Pricing hypothesis | COMPLETE | `roi_risk_assessment.md`; `strategic_plan.md` | EUR 600, EUR 1,200 and EUR 1,800 per centre-year are hypotheses. | Test price and contract preference. |
| KPIs and explicit success criteria | COMPLETE | `docs/kinder_signs_pilot_measurement.md`; `strategic_plan.md` | No pilot outcomes exist. | Freeze targets before launch and collect evidence. |
| Commercialisation model | COMPLETE | `strategic_plan.md`; `roi_risk_assessment.md` | School-led subscription has no current recurring revenue. | Test repeated use and paid continuation. |
| Final presentation | COMPLETE as delivered artifact | `presentation.pptx`; `presentation/documentation_handoff.md`; `presentation/source_notes.md` | The root PowerPoint is present and a readable ZIP package. This record does not claim a new slide-by-slide visual QA. | Preserve `presentation/kinder_signs_deck.pptx` as historical presentation evidence. |
| Working MVP demo | COMPLETE | `mvp/app.py`; `prototype/`; `mvp/tests/`; `prototype/tests/`; `presentation/demo_script.md` | Local desktop demo only; no hosted deployment. | Follow the scripted bounded claims and fallback. |
| Final demo recording | COMPLETE as present artifact | `presentation/kinderflow_demo.mp4`; `presentation/demo_script.md` | The 4:04.450 H.264 file is present and metadata-validated; no audio stream exists. File validation is not visual end-to-end review. | Preserve the recording used/prepared for the final presentation and record visual QA only if actually performed. |

## Additional readiness items

| Item | Status | Exact repository evidence | Current limitation | Final action |
|---|---|---|---|---|
| Assignment-driven Family Experience / mini-library | IMPLEMENTED AT LOCAL / SESSION-BASED MVP SCOPE | `prototype/family.html`; `prototype/school.js`; `prototype/tests/test_final_product_ux.py` | No real identities, authentication, durable or cross-device persistence, notifications, tenant isolation, production correction/deletion flow, or nursery-platform integration. | Design and test those production capabilities only after pilot privacy, security, and operating decisions. |
| Pilot asset rights | PARTIAL | `assets/registry/sign_asset_registry.json`; `assets/registry/source_assets_provenance.md` | Several external-display, print and commercial permissions remain unresolved. | Obtain explicit permission per asset and use. |
| Saved-PDF visual QA | PARTIAL | Print path in `prototype/print-card.html`; local screenshots under `tmp/pdfs/` | Final approved-asset PDF QA is not versioned as a completed review. | Inspect target browsers, paper sizes and accessibility. |
| Production deployment | NOT APPLICABLE | `strategic_plan.md` | Optional and pending; not required to prove the local MVP. | Decide only after pilot evidence. |
