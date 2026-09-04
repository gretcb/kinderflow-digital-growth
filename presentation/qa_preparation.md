# KinderFlow presentation Q&A preparation

## Why AI?

Movement is visual and temporal. MediaPipe gives the reviewer structured pose and hand evidence that text templates cannot provide. AI is optional for family wording and is not used for deterministic layout, assignment or publication rules. Evidence: `../poc/poc_documentation.md` and `../docs/course_technologies_applied.md`.

## Why not use existing nursery software?

Existing communication tools can carry messages, but the tested gap is governed, reusable Baby Sign content linked to nursery routines. Kinder Signs should complement a delivery channel rather than claim every existing product fails. The observation about Pequebook comes from one founder-observed nursery context. Evidence: `../docs/little_steps_operating_case_kpis.md`.

## Why not use free Baby Sign resources?

Free and paid Spanish content already exists, so Spanish-language content alone is not a moat. The hypothesis is school-led continuity, reviewed provenance, reusable materials, assignment and measurable reuse. The pilot must show that centres value that layer. Evidence: `../use_case_definition.md` and `../research/use_cases.md`.

## What does MediaPipe prove?

It proves that one reference can yield detected landmarks and reviewable movement evidence at stated coverage levels. It does not prove sign correctness, educational benefit or generalisation. Evidence: `../poc/output/validation_summary.json`.

## What happens if the visual is wrong?

The reviewer rejects it or selects a different pose, creates another deterministic option, or returns to a reviewed reference. Unreviewed or blocked material must not reach families. Current buttons are local proof state; production needs reviewer identity and audit records. Evidence: `../mvp/mvp_documentation.md`.

## Who is liable?

The repository cannot determine legal liability. Working roles must be fixed by the actual product, contract, content rights and deployment. KinderFlow is likely to own provider and content-operation duties; a school's deployer role depends on whether it operates an AI function or only receives reviewed content. Obtain qualified legal advice before a real pilot. Evidence: `../compliance/eu_ai_act_compliance.md`.

## Why is it not Annex III high risk?

Under the preliminary intended-purpose assessment, Kinder Signs does not decide admission or access, evaluate learning outcomes, choose educational level, proctor tests, assess children, recognise emotion, identify people biometrically or make automated educational decisions. A future feature that does so requires reassessment. Evidence: `../compliance/eu_ai_act_compliance.md`.

## What personal data is processed?

The current local MVP can process an identifiable adult reference video and derived landmarks, which may be personal data when linked to that person. Demo school and family records are synthetic. A pilot may need staff, nursery and minimum family access data; a child-specific pseudonymous assignment ID should exist only if necessary. No personal data should enter the optional LLM or LangSmith path. Evidence: `../compliance/gdpr_documentation.md`.

## What happens on a deletion request?

Production needs a verified process to locate source media, derived landmarks, previews, logs, assignments, account data and backups, then delete or restrict them according to the applicable right and retention duty. The local prototype has no complete request workflow, so this is a pilot gate. Evidence: `../compliance/gdpr_documentation.md`.

## Where do ROI assumptions come from?

The EUR 5.5k-EUR 17.3k range comes from the current cost line items. Price, customer growth and recurring costs are labelled hypotheses or project estimates. Little Steps tuition and time figures are founder-observed inputs plus calculated scenarios. No ROI result is presented as actual. Evidence: `../roi_risk_assessment.md` and `roi_slide_inputs.md`.

## Why n8n?

n8n makes the bounded content steps, branches, and human-review handoff visible. The exact inactive 12-node export is versioned, and a separate screenshot records the named governed workflow succeeding on 31 August 2026 at 21:30:27 in 14.499 seconds as execution `#21441`. This is complete at capstone low-code POC scope. It is not autonomous publication, production deployment, or proof that the later final MVP Content Pack adapter ran. Evidence: `../workflow/kinder_signs_n8n_workflow.json`, `../workflow/kinder_signs_n8n_workflow.md`, and `../workflow/evidence/n8n_successful_execution_2026-08-31.png`.

## Can the n8n provider path be rerun now?

Not with the former credential. The OpenAI course credential used at the time was removed or revoked shortly afterwards and is no longer available. A fresh provider-backed rerun requires a new authorised key. The historical execution remains valid evidence; the old key must never be reconstructed, exposed, or committed.

## Why LangSmith if it is only a dry-run?

It demonstrates the proposed trace and evaluation boundary for optional LLM wording, including source adherence and schema checks. It is preparatory evidence, not a live trace or production monitoring. LangSmith does not validate hand movement, MediaPipe output, sign correctness, linguistic correctness, or professional approval. Evidence: `../workflow/langsmith_dry_run_summary.json`.

## Is the assignment-driven family mini-library implemented?

Yes, at local/session-based MVP scope. School Admin stores a synthetic assignment in browser/session state; Family View reads it and displays the corresponding sign and materials. The exact duplicate combination is blocked. This does not provide real family identities or accounts, authentication, authorisation, durable cross-session or cross-device persistence, notifications, production delivery, tenant isolation, production correction/deletion, or nursery-platform integrations. Evidence: `../prototype/school.js`, `../prototype/family.html`, and `../prototype/tests/test_final_product_ux.py`.

## Why do the docs mention both ports 8000 and 8765?

Port 8000 remains the application default. The delivered demonstration used `poc_env/bin/python mvp/app.py --port 8765`, so the canonical demonstrated routes use `127.0.0.1:8765`. This is a launch-time override, not a default-code change. Evidence: `../mvp/app.py` and `demo_script.md`.

## Why Open Peeps?

It provides a reusable CC0 character and line grammar with recorded provenance and hashes. KinderFlow composes sign-specific arms and hands deterministically. Open Peeps defines appearance, not the sign; a reviewed reference and qualified human define mechanics and acceptability. Evidence: `../assets/flashcards/open_peeps/provenance.json`.

## Why no RAG?

The current library is small and has exact sign IDs. Direct retrieval is simpler to govern and avoids irrelevant results. Semantic retrieval may be useful only after a much larger approved multilingual library exists. Evidence: `../docs/course_technologies_applied.md`.

## Why no agent?

The workflow is bounded and ordered, and publication needs explicit human control. Autonomous planning would add risk without solving the present constraint. Evidence: `../docs/course_technologies_applied.md`.

## What is the biggest weakness?

The connected prototype is ahead of the operational and commercial evidence. No production-published sign, qualified end-to-end review, cleared full asset set, real family delivery, repeated educator use or willingness-to-pay result exists.

## What would you do next?

Close rights, qualified review, privacy, and security readiness; define minimum real identities, access, persistence, delivery, tenancy, and correction/deletion controls; freeze targets; then run an 8-9 week programme with 2-3 centres, 3-5 reviewed signs, and about 3-4 weeks of controlled service testing. Decide GO, ITERATE, or STOP from observed use, quality, cost, and paid-continuation evidence. Evidence: `../strategic_plan.md`.
