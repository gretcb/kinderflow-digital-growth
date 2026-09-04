# KinderFlow digital growth capstone

KinderFlow turns reviewed nursery content into reusable family guidance so educators can support school-home continuity without repeatedly creating and sending the same material.

KinderFlow is the early-childhood digital platform. Kinder Signs is its first active AI-enabled product. Kinder Daily and Kinder Food are future products, not current capabilities.

## Current status

**Recommendation: PROCEED WITH CONDITIONS.** The frozen repository contains enough technical and product evidence to fund pilot readiness and a controlled Kinder Signs service test. It does not contain the rights, qualified content approval, production controls, or commercial evidence required for an unconditional live pilot or full launch.

The current product is a connected local prototype:

- the KinderFlow Team can process an adult reference, inspect movement evidence, prepare deterministic visual candidates, and create family materials;
- a nursery can choose a sign, material set, and synthetic group or fictional child, then store that assignment in browser/session state;
- Family View reads the assignment state and presents the corresponding sign and materials as a local, assignment-driven mini-library; and
- the exact duplicate sign, audience, and material combination is blocked.

No current sign is production-published or available through a real school or family account.

## Key evidence

| Evidence | What is supported | Decisive limitation |
|---|---|---|
| MediaPipe Computer Vision | Versioned WATER evidence has 332 frames, 100% pose coverage, 93.98% dominant-hand coverage, 20 missing hand frames, 1 interpolated frame, and 19 unresolved frames. | Capture coverage is not sign recognition or linguistic correctness. |
| Connected local MVP | Upload, bounded direct MP4 URL, demo reference, review, pose selection, visual choice, family-material creation, nursery assignment, and the assignment-driven Family Experience / mini-library are connected locally. | State is local or session-based. There is no real identity, delivery, or durable multi-user persistence. |
| Visual system | Six sign packages contain 18 deterministic Open Peeps-derived SVG options. The registry records the official source and founder-verified CC0 basis. | Every current option is a draft requiring qualified sign and visual review. Open Peeps defines style, not sign mechanics. |
| Gemini FX | Separate local illustrative previews exist for MORE, HELP, and MILK. | They are not current-run or landmark-generated output. Rights, fidelity, and transparency gates remain open. |
| Low-code workflow evidence | The exact 12-node n8n export is versioned, and a screenshot records successful execution ID #21441 on 31 August 2026 in 14.499 seconds. | This is historical capstone POC execution of a governed draft workflow, not production deployment or proof that the later final MVP Content Pack adapter ran. A fresh provider-backed rerun requires a new authorised credential. |
| LangSmith evidence | A committed network-free `DRY_RUN` summary documents the optional wording-evaluation boundary. | No live LangSmith trace is claimed; LangSmith does not validate hand movement, MediaPipe output, sign or linguistic correctness, or professional approval. |
| Automated checks | The standard local suites contain 184 tests: 183 pass and 1 environment-dependent test is skipped. | The explicit MediaPipe integration rerun failed in headless macOS graphics-context creation and is not claimed as fresh success. |
| Tableau | A packaged Round 1 workbook, static image, source data, four worksheets, and one dashboard are versioned. | It is a market-decision artifact, not a production or pilot dashboard. |

Detailed claim wording and evidence paths are controlled in the [final claims matrix](docs/final_claims_matrix.md).

## Quick start

The locally evidenced presentation environment uses Python 3.9.6 and MediaPipe 0.10.14 with the legacy Solutions API. The deployment dependency is separately pinned to MediaPipe 0.10.21 in `poc/requirements.txt`; that pin is not a claim about the historical local measurements. Python 3.11 or 3.12 remains the clean future rebuild target.

The application default remains port 8000:

```bash
poc_env/bin/python mvp/app.py
```

The final presentation/demo used port 8765:

```bash
poc_env/bin/python mvp/app.py --port 8765
```

Canonical demonstrated routes:

- [KinderFlow overview](http://127.0.0.1:8765/index.html)
- [Kinder Signs](http://127.0.0.1:8765/kinder-signs.html)
- [Create a Sign](http://127.0.0.1:8765/create-sign.html)
- [School assignment](http://127.0.0.1:8765/school.html?sign=more&focus=share)
- [Family Experience](http://127.0.0.1:8765/family.html)

Use only reference media that is authorized for the intended processing and display. The direct video URL path accepts a bounded direct public MP4; it is not a general video-platform scraper or a production security boundary.

Run the standard local suites:

```bash
poc_env/bin/python -m unittest discover -s content_ops/tests -q
poc_env/bin/python -m unittest discover -s mvp/tests -q
poc_env/bin/python -m unittest discover -s poc/tests -q
poc_env/bin/python -m unittest discover -s prototype/tests -q
poc_env/bin/python -m unittest discover -s tools/tests -q
```

See the [MVP README](mvp/README.md) for environment details and controlled error behaviour.

## What the two POCs prove

The formal low-code POC is the governed n8n workflow. Its [exact 12-node export](workflow/kinder_signs_n8n_workflow.json), [workflow documentation](workflow/kinder_signs_n8n_workflow.md), and [successful historical execution screenshot](workflow/evidence/n8n_successful_execution_2026-08-31.png) satisfy the execution-evidence requirement at capstone low-code POC scope. The screenshot records **Kinder Signs — Governed Family Draft (Example)** on 31 August 2026 at 21:30:27, status **Succeeded**, execution ID #21441, and duration 14.499 seconds. This is not autonomous publication, production deployment, or evidence that the later final MVP Content Pack adapter was exercised. The OpenAI course credential used then was subsequently removed/revoked and is unavailable; a fresh provider-backed rerun requires a new authorised credential.

The separate Computer Vision POC answers a bounded technical question: can an adult sign-reference video become structured, body-relative, human-inspectable movement evidence?

The versioned WATER run supports:

- frame-level pose and hand extraction;
- raw and normalized landmark outputs;
- explicit missing-frame, interpolation, and unresolved-gap accounting;
- trajectory and displacement diagnostics;
- a technical result of `EXTRACTION_PASS`; and
- a movement-representation result of `MOTION_REPRESENTATION_PARTIAL`.

It does not prove sign correctness, linguistic interpretation, generalisation across signs or people, professional approval, production performance, or commercial value. The full method, charts, lineage, and reproduction boundary are in the [POC documentation](poc/poc_documentation.md).

## What the MVP proves

The local MVP connects evidence to a product workflow:

```text
adult reference
-> MediaPipe and OpenCV evidence
-> reference review
-> tracked poses, selected frames, or reviewed-reference fallback
-> deterministic visual candidates
-> human approval boundary
-> Flashcard, Routine Card, or Story
-> local nursery assignment
-> assignment-driven Family Experience / mini-library
```

The current Create a Sign interface has five steps: Sign & reference, Review reference, Choose poses, Approve visual, and Family materials. The dominant-hand tracked-pose rule requires at least 90% coverage. Lower coverage routes the user to selected frames or a reviewed-reference fallback with a recorded rationale.

Flashcard and Routine Card outputs are deterministic Bilingual or Spanish browser layouts. Print or Save as PDF is available through the browser; no PNG export or server-generated PDF is claimed. Story is a deterministic local MORE example. Song is Coming soon.

School Admin uses three synthetic groups and six fictional children, supports group or child selection, and prevents an exact duplicate with: "This exact sign, audience and material combination is already active." Family View reads browser/session state and displays the assigned sign and materials. This implements the assignment-driven mini-library at local/session-based MVP scope, not a production assignment-to-family service.

See the [MVP documentation](mvp/mvp_documentation.md), [prototype guide](prototype/README.md), and [reality check](docs/mvp_reality_check.md).

## Business and pilot decision

Little Steps Nursery is the pseudonymised operating archetype and Cleo is its owner/director and economic-buyer persona. The commercial model is school-led B2B/B2B2C with a per-centre annual subscription. Families and children are users and beneficiaries, not the primary payer.

The proposed validation programme is:

- 8-9 weeks total;
- about 3-4 weeks of controlled service testing inside that period;
- 2-3 nursery centres;
- 3-5 reviewed signs; and
- EUR 5.5k-EUR 17.3k for readiness plus controlled testing.

The existing prototype is sunk work. A production build and recurring operations sit outside that range and remain TBD.

| Scenario | Annual price per centre | 12-month ROI | 36-month ROI | Modelled break-even |
|---|---:|---:|---:|---:|
| Low | EUR 600 | -84.3% | -60.9% | More than 36 months |
| Base | EUR 1,200 | -66.7% | 22.3% | Month 29.3 |
| High | EUR 1,800 | -44.3% | 116.1% | Month 17.2 |

These are calculated decision scenarios, not forecasts or willingness-to-pay evidence. Core add-on revenue is EUR 0. The Little Steps price lens represents about 0.25%-0.92% of the selected EUR 195k-EUR 238k central-to-upper tuition planning envelope, depending on price and fee assumption. The 85% occupancy case is a lower sensitivity outside those selected endpoints.

Proceed only if rights and privacy gates close, reviewers can approve content efficiently, educators repeat assignments, families observe value, and paid continuation is credible. Use the [strategic plan](strategic_plan.md), [ROI and risk assessment](roi_risk_assessment.md), [cost and timeline](cost_timeline/estimate.md), and [pilot measurement plan](docs/kinder_signs_pilot_measurement.md) for the decision rules.

## Architecture

```mermaid
flowchart LR
    P["KinderFlow<br/>platform"] --> S["Kinder Signs<br/>active product"]
    P -. "future" .-> D["Kinder Daily"]
    P -. "future" .-> O["Kinder Food"]
    T["KinderFlow Team<br/>prepare, review, govern, version"] --> S
    S --> N["Nursery<br/>choose sign, group, materials, audience"]
    N -. "implemented in browser/session state" .-> F["Family<br/>assignment-driven mini-library"]
```

Kinder Signs, Kinder Daily, and Kinder Food sit at the same platform level; only Kinder Signs is active. The dotted nursery-to-family line marks the local/session prototype boundary. Real identities and accounts, authentication and authorisation, durable cross-session and cross-device persistence, notifications and delivery, production school accounts, tenant isolation, production correction/deletion workflows, and external nursery-platform integrations remain future work.

Inside Kinder Signs, Computer Vision produces technical evidence; deterministic rules and people control content readiness. The school does not operate MediaPipe, LLM, n8n, or LangSmith workflows.

## Repository map

```text
assets/          Source and asset registries, visual provenance, review records
build/           Versioned draft publication packages
compliance/      Preliminary EU AI Act and GDPR assessments
content_ops/     States, provenance, contracts, gates, audit events, regression set
cost_timeline/   Validation investment and staging
dashboard/       Round 1 Tableau artifact and documentation
data/            Tableau source data and source register
docs/            Evidence controls, architecture, audits, business, pilot, reality checks
feedback/        Historical Round 1 feedback and KEEP decision
mvp/             Local Python service and content-package logic
poc/             Versioned Computer Vision source, outputs, diagnostics, and tests
presentation/    Historical deck, final demo recording, and presentation support files
prototype/       Local role-based HTML, CSS, and JavaScript interfaces
research/        Historical sector, opportunity, and use-case research
workflow/        n8n export, deterministic gate, and LangSmith dry-run
```

## Documentation

Start with:

- [Final deliverables audit](docs/final_deliverables_audit.md)
- [Final claims matrix](docs/final_claims_matrix.md)
- [Capstone requirement matrix](docs/capstone_requirement_matrix.md)
- [Submission checklist](docs/submission_checklist.md)

Product and technical evidence:

- [Use case definition](use_case_definition.md)
- Formal low-code POC: [exact n8n export](workflow/kinder_signs_n8n_workflow.json), [workflow documentation](workflow/kinder_signs_n8n_workflow.md), and [successful execution evidence](workflow/evidence/n8n_successful_execution_2026-08-31.png)
- Separate technical feasibility artifact: [Computer Vision POC documentation](poc/poc_documentation.md)
- Connected broader MVP demonstration: [final demo recording](presentation/kinderflow_demo.mp4)
- Working MVP: [application directory](mvp/), [MVP documentation](mvp/mvp_documentation.md), [root requirements](requirements.txt), and [placeholder-only environment example](.env.example)
- [System one-page summary](docs/kinder_signs_system_one_page.md)
- [Technology and course methods](docs/course_technologies_applied.md)
- [Dashboard documentation](dashboard/dashboard_documentation.md)

Business and decision evidence:

- [Little Steps operating case and KPIs](docs/little_steps_operating_case_kpis.md)
- [ROI and risk assessment](roi_risk_assessment.md)
- [Cost and timeline](cost_timeline/estimate.md)
- [Strategic plan](strategic_plan.md)
- [Pilot measurement plan](docs/kinder_signs_pilot_measurement.md)

Governance and delivery:

- [EU AI Act assessment](compliance/eu_ai_act_compliance.md)
- [GDPR documentation](compliance/gdpr_documentation.md)
- [Responsible AI audit](docs/audits/responsible_ai_audit.md)
- [Green AI audit](docs/audits/green_ai_audit.md)
- [Presentation handoff](presentation/documentation_handoff.md)
- [Demo script and backup plan](presentation/demo_script.md)
- [Final delivered presentation](presentation.pptx)

Historical Round 1 materials remain versioned in [research](research/), [the Round 1 decision record](feedback/round1_decision.md), and [dashboard](dashboard/). The older [Kinder Signs deck](presentation/kinder_signs_deck.pptx) remains presentation history and has not been replaced.

## Known limitations

- The assignment-driven Family Experience exists only in local browser/session state; no real family identities or accounts, authentication/authorisation, durable cross-session or cross-device persistence, notifications, delivery integration, production school accounts, tenant isolation, production correction/deletion workflow, or external nursery-platform integration exists.
- No production authentication, role-based access control, tenant isolation, rate limiting, egress control, decoder isolation, monitoring, backup, deletion service, or deployment is claimed.
- The six-sign asset registry and older five-sign content-operation package are not fully reconciled.
- All 18 static visual candidates need qualified hand, sign, visual, accessibility, and publication review.
- Reference, contextual, and Gemini rights are not fully cleared for every intended external, print, or commercial use.
- Gemini files are separate demonstration media, not current pipeline output.
- A successful historical n8n execution is evidenced, but it is not production deployment or proof of the later final MVP adapter; the former OpenAI course credential is unavailable, so a new authorised credential is required for a fresh provider-backed rerun. A live LangSmith trace and live final LLM call remain unclaimed.
- Browser Print or Save as PDF exists, but final saved-PDF visual QA with approved assets is pending.
- The explicit headless integration rerun failed because a macOS graphics context could not initialize.
- No real pilot data, paid customer, recurring revenue, product-market fit, compliance certification, or production deployment is claimed.

The final [presentation file](presentation.pptx) and [demo recording](presentation/kinderflow_demo.mp4) are present, and the presentation has been delivered. Package and media validation are recorded in the final audit; technical file validation alone is not a visual end-to-end review.
