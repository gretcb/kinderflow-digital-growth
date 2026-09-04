# KinderFlow presentation documentation handoff

This file records the verified content and evidence boundaries for the delivered 19-slide PowerPoint package at `presentation.pptx`. The story framework below has ten parts; it is not a claim that the deck has ten slides. This record does not claim a new slide-by-slide visual QA. The earlier `presentation/kinder_signs_deck.pptx` remains preserved as historical/versioned presentation evidence.

## Decision statement

**Recommendation: PROCEED WITH CONDITIONS.** KinderFlow has enough technical and product evidence to fund pilot-readiness work and a controlled Kinder Signs test. It does not yet have the rights, operational review, privacy and security controls, or commercial evidence needed for an unconditional live pilot or full launch.

## Ten-part story framework

| Part | Decision message | Verified inputs | Evidence | Required limitation |
|---:|---|---|---|---|
| 1. Title | KinderFlow is a school-led early-childhood digital platform. Kinder Signs is its first active AI-enabled product. | Use `PROCEED WITH CONDITIONS` as the current decision. | `README.md`; `use_case_definition.md` | Do not call the platform deployed or commercially validated. |
| 2. Problem | Cleo has Baby Sign knowledge and observed family requests for sign materials, but limited time and no recurring school-family content service. | Little Steps has 9 people involved, not 9 market-salary FTEs; 3 groups; capacity 42; about 38 children at 90% occupancy. | `docs/little_steps_operating_case_kpis.md` | Pseudonymised operating case; not audited client financial information. Commercial demand and willingness to pay are unvalidated. |
| 3. Proposed AI solution | KinderFlow Team prepares and governs reusable content; the nursery chooses an available sign, materials, and a group or fictional child; Family View reads the synthetic browser/session assignment. | Computer Vision supports movement review. Deterministic tools create materials. Human review controls release. The assignment-driven Family Experience is implemented locally. | `use_case_definition.md`; `docs/kinder_signs_system_one_page.md`; `prototype/school.js`; `prototype/family.html` | Production identities, accounts, access control, durable cross-device persistence, notifications, delivery, tenancy, correction/deletion, and integrations remain pending. |
| 4. POC demo | The formal low-code POC is the governed n8n workflow; the Computer Vision POC is separate technical feasibility evidence. | Exact 12-node export plus successful historical run on 31 August 2026 (`#21441`, 14.499 seconds). Versioned WATER result: 332 frames, 100.00% pose, 93.98% dominant-hand coverage, 20 missing, one interpolated, 19 unresolved, `EXTRACTION_PASS`, `MOTION_REPRESENTATION_PARTIAL`. | `workflow/kinder_signs_n8n_workflow.json`; `workflow/evidence/n8n_successful_execution_2026-08-31.png`; `poc/poc_documentation.md`; `poc/output/validation_summary.json` | n8n is complete at capstone low-code POC scope, not production or later-adapter proof. CV coverage is not sign correctness and one WATER run does not prove generalisation. |
| 5. Business case and ROI | A per-centre subscription is proportionate to the nursery revenue envelope, but provider returns depend on scale. | Pricing hypotheses: EUR 600, EUR 1,200, EUR 1,800 per centre-year. Base ROI: -66.7% at 12 months and 22.3% at 36 months; modelled break-even month 29.3. | `roi_risk_assessment.md`; `presentation/roi_slide_inputs.md` | Scenario model, not forecast or willingness-to-pay evidence. |
| 6. Top three risks | Quality, commercial adoption and rights can each stop the pilot. | Sign-content fidelity and hand articulation; willingness to pay and repeat use; reference and asset rights. | `roi_risk_assessment.md`; `docs/facts_risk.md` | Privacy, security and review throughput remain material gates even if not in the top three. |
| 7. EU AI Act and GDPR | The narrow intended purpose avoids child assessment and Annex III education decisions, but a real pilot creates governance duties. | No admission, outcome, level, proctoring, emotion, biometric identity or automated educational decision. Current processing is local and synthetic; pilot roles, legal bases, retention, recipients, rights and DPIA need sign-off. | `compliance/eu_ai_act_compliance.md`; `compliance/gdpr_documentation.md` | Preliminary assessment only. No legal advice or compliance certification. |
| 8. POC to pilot to deployment | Buy evidence in stages and stop if the core assumptions fail. | 8-9 weeks total; about 3-4 weeks controlled service testing; 2-3 nurseries; 3-5 reviewed signs; EUR 5.5k-EUR 17.3k validation budget. | `strategic_plan.md`; `cost_timeline/estimate.md`; `docs/kinder_signs_pilot_measurement.md` | Production build and recurring operations are outside that budget. |
| 9. MVP demo | The connected local flow links reference review, movement evidence, visual choice, family materials, nursery assignment, and an assignment-driven Family Experience. | Upload, public direct MP4 and MORE demo paths; tracked or selected poses; Flashcard, Routine Card, Story; Song Coming soon; session assignment and exact duplicate control; Family View reads the assignment. | `mvp/mvp_documentation.md`; `prototype/`; `mvp/` | No current sign is production-published. No real accounts, authentication, durable cross-device persistence, notifications, production delivery, tenancy, or production correction/deletion flow. |
| 10. Recommendation | Proceed only through named readiness gates and a pre-agreed decision rule. | GO on repeated educator use, family value, manageable qualified review, complete rights, no critical content incident and credible paid continuation. ITERATE on fixable workflow or cost gaps. STOP on no WTP, no repeat use, unapprovable content, unresolved rights/safety or structurally weak economics. | `strategic_plan.md`; `docs/kinder_signs_pilot_measurement.md` | Do not recommend full launch now. |

## Backup-slide inputs

### Technology choices and why

- MediaPipe extracts pose and hand landmarks because the source problem is visual and temporal.
- OpenCV processes frames and produces technical video evidence. It is not AI by itself.
- ffmpeg creates a browser-compatible H.264 review preview. It does not alter landmark extraction.
- Python runs the local service, pipeline, rules and APIs.
- HTML, CSS and JavaScript provide role-specific local interfaces and browser-session state.
- Open Peeps supplies the reusable character and line grammar. Reviewed references define sign mechanics.
- Deterministic SVG composition, templates and gates make outputs reproducible and reviewable.
- n8n has an exact inactive 12-node export and a separate successful historical execution screenshot. That is complete at capstone low-code POC scope; it is not production deployment or proof of the later final adapter.
- LangSmith is represented by a documented dry-run for optional LLM wording only.
- No RAG or product agent is needed for the current small, exact, governed library.

Evidence: `docs/course_technologies_applied.md`.

### Technical architecture

```text
adult reference input
-> MediaPipe and OpenCV
-> raw and body-relative landmarks
-> gaps, diagnostics and H.264 preview
-> tracked pose, selected frames or reviewed-reference fallback
-> deterministic visual and material preparation
-> human review
-> local nursery assignment in browser/session state
-> assignment-driven local Family Experience
```

Evidence: `poc/poc_documentation.md`, `mvp/mvp_documentation.md` and `docs/kinder_signs_content_operations_architecture.md`.

### Deliberately not automated

- sign-language correctness;
- source and rights approval;
- visual hand and contact review;
- publication;
- child assessment, scoring or educational decisions;
- personalised recommendations;
- production delivery to families.

### Detailed ROI assumptions

Use `presentation/roi_slide_inputs.md`. Keep add-on revenue at EUR 0 in the core scenarios. Do not mix school time release into KinderFlow provider revenue.

### Detailed risks

Use the full owner, control, residual-risk and gate table in `roi_risk_assessment.md`.

### Compliance reasoning

Use the intended-purpose sequence in `compliance/eu_ai_act_compliance.md` and the current-versus-pilot data flows in `compliance/gdpr_documentation.md`.

### Evidence paths

Use `docs/final_claims_matrix.md`, `docs/capstone_requirement_matrix.md` and `presentation/source_notes.md` as the claim control layer.

## Final artifact status and residual gates

- The final delivered PowerPoint is present at `presentation.pptx`; the older `presentation/kinder_signs_deck.pptx` remains historical evidence.
- The final recording is present at `presentation/kinderflow_demo.mp4` and was used/prepared for the final presentation.
- Readable-package and video-metadata checks do not by themselves prove visual end-to-end QA.
- Keep every number aligned with `presentation/roi_slide_inputs.md`.
- Confirm external-display rights before showing any reference or Gemini video.
- Keep WATER and MORE run metrics separate.
- Label the dashboard target position as a hypothesis.
- Describe the Family Experience as implemented only at local/session MVP scope, with production identity, access, persistence, delivery, tenancy, and correction/deletion capabilities still pending.
