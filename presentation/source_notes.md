# KinderFlow presentation source notes

Use this table to verify every slide claim before it enters the presentation.

| Presentation claim | Evidence file | Evidence type | Permitted wording | Limitation |
|---|---|---|---|---|
| KinderFlow is the platform and Kinder Signs is the first active product. | `../README.md`; `../use_case_definition.md` | Current product definition | KinderFlow is an early-childhood digital platform; Kinder Signs is its first active AI-enabled product. | Kinder Daily and Kinder Food remain future products. |
| Little Steps capacity is 42. | `../docs/little_steps_operating_case_kpis.md` | Founder-observed units plus calculated total | The pseudonymised three-unit model has theoretical capacity of 8, 14 and 20 children, total 42. | Not audited client data; occupancy is not capacity. |
| Little Steps selected tuition planning envelope is EUR 195k-EUR 238k. | `../docs/little_steps_operating_case_kpis.md` | Calculated scenario | Illustrative central-to-upper annual tuition-revenue lens. | About 90% occupancy over 10 months through full capacity over 11 months; the 85% case is a lower sensitivity; not declared turnover. |
| Baby Sign is already used and monetised through training. | `../docs/little_steps_operating_case_kpis.md` | Founder-observed | Cleo already uses and sells Baby Sign activity or courses. | One nursery context; no audited margin. |
| Paid Spanish alternatives exist. | `../research/sector_research.md`; `../data/source_register.csv` | Vendor benchmark | Spanish-language paid plans and educator training exist. | Vendor evidence; not market share or KinderFlow WTP. |
| Kinder Signs differentiation is school-home continuity and governed reuse. | `../use_case_definition.md`; `../research/use_cases.md` | Product hypothesis | This is the tested differentiation. | Target position is not observed market performance. |
| WATER POC processed 332 frames. | `../poc/output/validation_summary.json`; `../assets/registry/source_assets_provenance.md` | Versioned technical evidence | 332 frames; 100.00% pose; 93.98% dominant-hand coverage; 20 missing; extraction pass and motion partial. | WATER only; no correctness or generalisation claim. |
| A local MORE run processed 285 frames. | `../mvp/runs/run_20260904T061136125509Z_eb661bc3/run.json` | Ignored local evidence | A prior local MORE run recorded 285 frames, 100.00% pose and 91.93% dominant-hand coverage. | Not versioned and not freshly reproduced in the final headless audit. |
| Standard automated suites passed. | `../content_ops/tests/`; `../mvp/tests/`; `../poc/tests/`; `../prototype/tests/`; `../tools/tests/` | Local execution record | 184 standard tests ran: 183 passed and one opt-in integration test skipped. | The explicit headless integration rerun failed on graphics-context creation. |
| Direct MP4 URL works locally. | `../mvp/pipeline.py`; `../mvp/tests/test_prompt_3.py` | Code and tests | Bounded public direct-MP4 intake exists. | Not a scraper, rights check or production security assessment. |
| Six visual sign packages exist. | `../assets/registry/sign_asset_inventory.md`; `../prototype/data/visual_sign_packages.json` | Versioned registry and assets | Six packages contain 18 deterministic draft options. | None is professionally reviewed, printable or published. |
| Open Peeps is CC0 in the registry. | `../assets/flashcards/open_peeps/provenance.json`; `../assets/registry/source_assets_provenance.md` | Versioned provenance record | Registry records founder-verified official CC0 source. | Style source only; not rights proof for other assets or sign validation. |
| Gemini previews exist for three signs. | `../assets/registry/source_assets_provenance.md` | Registry plus local-only media | MORE, HELP and MILK have separately prepared illustrative motion previews. | Not current-run output; rights, fidelity and qualified review pending. |
| Flashcard and Routine Card work locally. | `../prototype/flashcards.html`; `../prototype/print-card.html`; tests | Current local prototype | Deterministic Bilingual and Spanish previews plus browser Print or Save as PDF exist. | No PNG, server PDF, published content or final approved-asset PDF QA. |
| Story exists and Song is pending. | `../prototype/create-story.html`; `../prototype/create-song.html` | Current local prototype and future route | Story is a local MORE prototype; Song is Coming soon. | Story is not a live LLM service. |
| Nursery assignment works locally. | `../prototype/school.html`; `../prototype/school.js`; tests | Current local prototype | Synthetic sign, group, material and audience assignment with duplicate control exists. | Browser-session state only; no account or delivery. |
| Family guidance preview exists. | `../prototype/family.html`; `../prototype/app.js` | Current local prototype | A basic family-facing guidance preview exists. | Final personalised assignment-driven family mini-library remains pending. |
| n8n workflow exists. | `../workflow/kinder_signs_n8n_workflow.json`; `../workflow/kinder_signs_n8n_workflow.md` | Versioned design/export | Exact importable workflow and documentation exist. | No final target-runtime execution record. |
| LangSmith is represented. | `../workflow/langsmith_dry_run_summary.json`; `../workflow/langsmith_evaluation_plan.md` | DRY_RUN | A documented evaluation path and network-free dry-run exist for optional LLM wording. | No live trace; no CV or sign evaluation. |
| Tableau supports the pilot decision. | `../dashboard/tableau/Kinder Signs - Market Opportunity.twbx`; `../dashboard/tableau/kinder_signs_market_opportunity.png` | Versioned Round 1 BI evidence | Market, digital-readiness and competitor evidence support further pilot testing. | Does not prove demand, WTP, market share or product-market fit. |
| Validation costs EUR 5.5k-EUR 17.3k. | `../cost_timeline/estimate.md` | Project estimate | The 8-9 week readiness and controlled-test range is EUR 5.5k-EUR 17.3k. | Excludes sunk prototype valuation, production build and recurring operations. |
| Base 36-month ROI is 22.3%. | `../roi_risk_assessment.md`; `roi_slide_inputs.md` | Calculated scenario | Base scenario gives EUR 11,160 net benefit and 22.3% ROI by month 36. | Depends on unvalidated price, customer growth and cost estimates. |
| Current recommendation is PROCEED WITH CONDITIONS. | `../strategic_plan.md`; `../roi_risk_assessment.md` | Decision synthesis | Proceed to pilot-readiness and a controlled test only after gates close. | Not a recommendation for full launch. |
| Current intended use does not appear to match Annex III education functions. | `../compliance/eu_ai_act_compliance.md` | Preliminary intended-purpose assessment | No admission, outcome, level, proctoring or child-assessment function is present. | Not legal advice or certification; reassess changes. |
| Current MVP uses no real child accounts. | `../compliance/gdpr_documentation.md`; `../prototype/school.js` | Code and data-flow review | Current school and family records are synthetic/local. | Pilot personal-data design is not final. |

## Claims that must not appear

- `93.98% sign accuracy`;
- `landmark-generated Gemini video`;
- `approved six-sign library`;
- `live n8n and LangSmith production workflow`;
- `families receive a personalised library today`;
- `GDPR compliant` or `EU AI Act certified`;
- `product-market fit`;
- `production deployment`.
