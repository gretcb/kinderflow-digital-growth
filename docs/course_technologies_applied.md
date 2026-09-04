# Technology and course methods applied to KinderFlow

KinderFlow uses technology only where it solves a product or evidence problem. Computer Vision is the strongest current AI implementation. Other AI-adjacent components are optional, dry-run, or demonstration evidence unless a stronger status is stated below.

Evidence statuses used in this document:

- **CURRENT WORKING:** implemented and locally testable in the frozen repository;
- **VERSIONED EVIDENCE:** a fixed artifact or result is committed, but it may not represent a fresh run;
- **PARTIAL:** some implementation evidence exists and a material proof remains open;
- **DEMO ONLY:** illustrative evidence that is outside the current pipeline;
- **FUTURE:** planned or proposed, not implemented; and
- **NOT NEEDED:** deliberately excluded from the bounded MVP.

## MediaPipe Computer Vision

**What problem it solves:** Converts an adult sign-reference video into time-ordered pose and hand landmarks that can be inspected as movement evidence.

**Where it appears:** `poc/src/extract_landmarks.py`, `poc/output/`, and `mvp/pipeline.py`.

**Why it fits:** KinderFlow needs more than a still image to inspect movement. Frame-level landmark evidence gives a reviewer a visible bridge between a source video and later visual work.

**Current evidence status:** **CURRENT WORKING** for the local pipeline and **VERSIONED EVIDENCE** for the WATER POC. The committed WATER result contains 332 frames, 100% pose coverage, 93.98% dominant-hand coverage, 20 missing dominant-hand frames, 1 interpolated frame, and 19 unresolved frames. An ignored local MORE run exists, but it is not versioned evidence and was not freshly reproduced during final reconciliation because the headless macOS graphics context failed.

**What it does not do:** It does not recognize a sign, certify linguistic correctness, assess a child, or approve educational content.

## OpenCV

**What problem it solves:** Reads video metadata and frames, extracts selected frames, converts colour space for MediaPipe, and writes technical previews.

**Where it appears:** `poc/src/extract_landmarks.py` and `mvp/pipeline.py`.

**Why it fits:** It provides dependable frame and video handling around the Computer Vision model without adding another hosted service.

**Current evidence status:** **CURRENT WORKING** as local pipeline infrastructure and covered by POC and MVP tests.

**What it does not do:** OpenCV is not described as AI. It does not validate a sign or make a publication decision.

## ffmpeg

**What problem it solves:** Converts the technical overlay to browser-compatible H.264 video and checks media properties with `ffprobe`.

**Where it appears:** `mvp/pipeline.py` and the environment-dependent tests in `mvp/tests/test_mvp.py`.

**Why it fits:** A browser needs a predictable playback format even when the intermediate local preview uses a different codec.

**Current evidence status:** **CURRENT WORKING** when the local binaries are installed. The service reports a controlled preview error when they are unavailable.

**What it does not do:** ffmpeg is delivery infrastructure, not AI, movement analysis, rights validation, or sign review.

## Python

**What problem it solves:** Runs the local service, MediaPipe pipeline, deterministic content logic, registry checks, workflow support, and automated tests.

**Where it appears:** `poc/`, `mvp/`, `content_ops/`, `workflow/`, and `tools/`.

**Why it fits:** One local language can connect video processing, structured evidence, API responses, and repeatable validation while the project remains a controlled prototype.

**Current evidence status:** **CURRENT WORKING**. The frozen repository contains executable modules and automated suites rather than only design notes.

**What it does not do:** Python does not make the prototype production-ready. Authentication, durable multi-user persistence, monitoring, deployment controls, and operational security remain outside the local build.

## JavaScript, HTML, and CSS

**What problem it solves:** Presents role-specific flows, carries browser state between screens, renders print layouts, and makes the service evidence understandable to educators and families.

**Where it appears:** `prototype/`, including the overview, creation, Flashcard, Routine Card, Story, school, and family routes.

**Why it fits:** Static browser technology keeps the capstone demonstrable without introducing a front-end framework or build service that the current scope does not require.

**Current evidence status:** **CURRENT WORKING** as a local interactive prototype. Automated tests cover route content and state behaviour.

**What it does not do:** Browser `sessionStorage` is not a database, identity system, access-control layer, family account, notification channel, or production delivery service.

## Open Peeps by Pablo Stanley

**What problem it solves:** Supplies a reusable character base and coherent line grammar across sign-specific visual candidates.

**Where it appears:** `assets/flashcards/open_peeps/`, `prototype/assets/signs/`, `prototype/data/visual_sign_packages.json`, and `assets/registry/sign_asset_registry.json`.

**Why it fits:** A fixed visual foundation improves consistency and reuse while KinderFlow controls sign-specific arms, hands, and movement marks separately. The registry records the official source and founder-verified CC0 basis.

> The character defines the look. The reviewed reference defines the sign.

**Current evidence status:** **VERSIONED EVIDENCE**. Six visual packages contain 18 deterministic Open Peeps-derived draft SVGs. Each sign has two initial options and one deterministic additional option. All require qualified sign and visual review.

**What it does not do:** Open Peeps does not determine fingers, palm orientation, contact, direction, motion, sign meaning, or sign accuracy. Its licence record does not clear unrelated reference, context, or Gemini assets.

## Deterministic SVG composition

**What problem it solves:** Produces repeatable visual candidates that can be compared, hashed, versioned, and regenerated without uncontrolled model variation.

**Where it appears:** `mvp/app.py`, `prototype/assets/signs/`, `prototype/data/visual_sign_packages.json`, and the asset registry.

**Why it fits:** Stable candidate differences are easier to audit and review than unconstrained image generation. Deterministic composition also supports reuse across family materials.

**Current evidence status:** **CURRENT WORKING** for candidate creation and **PARTIAL** for content readiness. The 18 current SVGs are drafts, not reviewed or published assets.

**What it does not do:** Determinism does not make hand articulation correct. It does not replace qualified review for fingers, palms, contact, direction, movement, and readability.

## Google Labs FX or Gemini FX

**What problem it solves:** Shows optional illustrative motion direction during a demonstration.

**Where it appears:** The local asset registry maps MORE to `mas.mp4`, HELP to `ayuda.mp4`, and MILK to `leche.mp4`. EAT, SLEEP, and WATER have no current Gemini file.

**Why it fits:** A separately prepared moving example can help communicate future direction without being treated as the product's processing result.

**Current evidence status:** **DEMO ONLY**. The three local files were prepared separately and were not generated from the current run or its landmarks. External-display rights, fidelity review, and applicable transparency treatment remain open.

**What it does not do:** It is not the current pipeline, a landmark-controlled generator, a reviewed sign, a certified sign video, or evidence that every library item has animation.

## n8n orchestration

**What problem it solves:** Makes a repeatable content-operations sequence visible through explicit steps, branching, structured handoffs, quality-gate routing, and human-review preparation.

**Where it appears:** `workflow/kinder_signs_n8n_workflow.json`, `workflow/kinder_signs_n8n_workflow.md`, `workflow/evidence/n8n_successful_execution_2026-08-31.png`, and `content_ops/contracts/n8n_content_operations_contract.json`.

**Why it fits:** A visual workflow can make ownership and exceptions easier to inspect when content volume grows beyond local manual coordination.

**Current evidence status:** **VERSIONED EVIDENCE / COMPLETE AT CAPSTONE LOW-CODE POC SCOPE**. The repository contains the exact valid 12-node importable export (currently `active: false`), its contract and documentation, and a screenshot of **Kinder Signs — Governed Family Draft (Example)** on 31 August 2026 at 21:30:27, status **Succeeded**, execution ID #21441, and duration 14.499 seconds.

**What it does not do:** n8n is not the product, does not validate sign accuracy, and cannot approve or publish a sign autonomously. The historical run is not production deployment or proof that the later final MVP Content Pack adapter ran. The former OpenAI course credential is unavailable, so a fresh provider-backed rerun requires a new authorised credential.

## LangSmith observability

**What problem it solves:** Records and evaluates the optional language-model wording step for source adherence, allowed claims, movement-note fidelity, JSON structure, and preservation of the review gate.

**Where it appears:** `workflow/langsmith_eval.py`, `workflow/evaluation_cases.json`, `workflow/langsmith_evaluation_plan.md`, and `workflow/langsmith_dry_run_summary.json`.

**Why it fits:** If model-assisted copy is introduced, reviewers need to see what the model received, produced, and failed.

**Current evidence status:** **PARTIAL**. A local `DRY_RUN` summary exists with network calls false. No live external trace is claimed.

**What it does not do:** LangSmith does not assess hand movement, MediaPipe output, sign correctness, linguistic correctness, visual rights, or professional approval.

## Optional LLM content drafting

**What problem it solves:** Can draft concise family wording from supplied, controlled sign and routine context when content volume justifies assistance.

**Where it appears:** `workflow/langsmith_eval.py`, its prompt and sample artifacts, and the content-operation contracts.

**Why it fits:** It is limited to a reversible text draft while deterministic rules and people retain approval authority.

**Current evidence status:** **PARTIAL**. Prompt, optional live script path, sample output, evaluation cases, and deterministic checks exist. The current content manifests use human-authored copy, and no live model call is evidenced for the later final MVP Content Pack adapter. The separate historical n8n POC execution does not prove that adapter ran.

**What it does not do:** It does not invent sign mechanics, interpret movement, certify content, approve rights, or publish automatically.

## Structured output and JSON Schema

**What problem it solves:** Keeps model and workflow handoffs predictable through named fields, explicit allowed values, and rejectable malformed output.

**Where it appears:** `content_ops/contracts/content_pack_input.schema.json`, `content_ops/contracts/content_pack_output.schema.json`, `content_ops/contracts/n8n_content_operations_contract.json`, and `workflow/quality_gate.py`.

**Why it fits:** A content workflow needs machine-checkable boundaries between optional drafting, deterministic evaluation, and human decisions.

**Current evidence status:** **CURRENT WORKING** for local JSON contracts and validation. The project uses JSON Schema and explicit Python checks, not Pydantic.

**What it does not do:** Valid structure is not evidence that wording, movement, rights, or educational content is correct.

## Deterministic quality gates

**What problem it solves:** Enforces objective rules for required fields, known sources, review states, banned claims, identifiers, and allowed state transitions.

**Where it appears:** `workflow/quality_gate.py`, `content_ops/policy.py`, `content_ops/content_engine.py`, and their tests.

**Why it fits:** Missing evidence and blocked states are facts that belong in code, not subjective model judgement.

**Current evidence status:** **CURRENT WORKING** and locally tested. A candidate cannot become `PUBLISHED` through the automated content path alone.

**What it does not do:** A passing technical gate is not qualified sign approval, rights clearance, user validation, or a production security review.

## Human in the loop

**What problem it solves:** Keeps accountable people in control of sign content, visual quality, rights, publication, exceptions, and fallbacks.

**Where it appears:** The content state machine, review packages, local approval controls, UI disclosures, and compliance documentation.

**Why it fits:** KinderFlow prepares educational material for very young children. Automation can expose evidence and drafts, while qualified people make content and release decisions.

**Current evidence status:** **CURRENT WORKING** as a local policy and state boundary. The current approval is `APPROVED_FOR_INTERNAL_PRINTABLE`, publication remains `DRAFT`, and the reviewer UI is not authenticated.

**What it does not do:** A simulated local approval is not an identity-backed approval ledger, external professional validation, or production governance.

## Provenance, registry, and SHA-256 hashes

**What problem it solves:** Preserves exact asset identity, evidence linkage, versions, and silent-change detection across references, technical results, visuals, and packages.

**Where it appears:** `assets/registry/sign_asset_registry.json`, `assets/registry/source_assets_provenance.md`, `assets/flashcards/open_peeps/provenance.json`, and `content_ops/provenance.py`.

**Why it fits:** Review must attach to a known source and asset version rather than a label whose underlying files can change.

**Current evidence status:** **CURRENT WORKING** for local registry checks and package fingerprints. The canonical registry covers six signs and 56 assets.

**What it does not do:** A hash is not proof of ownership, rights clearance, authenticity, tamper-proof storage, or complete security.

## State machine, audit log, and idempotency

**What problem it solves:** Prevents skipped review states, records important local events, and makes repeated workflow operations safe.

**Where it appears:** `content_ops/domain.py`, `content_ops/policy.py`, `content_ops/events/audit_log.jsonl`, and the content-operation tests.

**Why it fits:** Content preparation will be retried and corrected. Fixed transitions and stable identifiers keep the history understandable.

**Current evidence status:** **CURRENT WORKING** as local helpers and tested policy. Publication packages remain draft or blocked where required evidence is missing.

**What it does not do:** The JSONL log is not tamper-proof, centrally monitored, identity-backed, or a substitute for a production audit service.

## Git and GitHub

**What problem it solves:** Preserves versions of code, documentation, contracts, source records, exports, and evidence so a reviewer can trace changes to an exact checkpoint.

**Where it appears:** The repository history, the shared functional checkpoint `8eb0742dae49d8a1ac032d0f53d4475cc694c8b2`, and the final `release/capstone-demo` line that combines the deployment pin, reconciled documentation, and submission artifacts.

**Why it fits:** Capstone claims are more reproducible when they point to versioned artifacts and an exact baseline.

**Current evidence status:** **CURRENT WORKING** for local version control and evidence preservation. The release branch preserves exact exported artifacts, historical execution evidence, and the current prototype separately.

**What it does not do:** Git history alone does not prove a live service ran, an external right exists, a reviewer was qualified, or a product claim is valid.

## Tableau

**What problem it solves:** Makes the Round 1 market and opportunity evidence easier to compare and discuss.

**Where it appears:** `dashboard/tableau/Kinder Signs - Market Opportunity.twbx`, `dashboard/tableau/kinder_signs_market_opportunity.png`, `data/tableau_master.csv`, and `dashboard/data_dictionary.md`.

**Why it fits:** A visual evidence artifact supports the decision to investigate KinderFlow further while keeping product judgement separate from the chart.

**Current evidence status:** **VERSIONED EVIDENCE**. The packaged workbook contains four worksheets and one dashboard. The static image and source dataset are present. No visible end-user filter controls are evidenced.

**What it does not do:** It is not a production or pilot dashboard, does not contain real pilot behaviour, and does not prove product-market fit.

## Statistical analysis

**What problem it solves:** Can describe distributions, variation, uncertainty, and small-sample limits once a controlled pilot produces observations.

**Where it appears:** Future analysis is defined in `kinder_signs_pilot_measurement.md`; no pilot-result dataset exists.

**Why it fits:** Assignment time, repeated use, and family engagement are likely to vary across educators and centres, so a single average would be misleading.

**Current evidence status:** **FUTURE**. Metric definitions and targets exist, but there is no real pilot dataset or statistical outcome.

**What it does not do:** No significance test, causal effect, adoption result, or product-market-fit conclusion is claimed.

## RAG

**What problem it solves:** Semantic retrieval can select relevant evidence from a large knowledge base for a model prompt.

**Where it appears:** It does not appear in the current product.

**Why it fits:** It does not fit the present six-sign library. Exact retrieval by sign ID is simpler and easier to govern. A larger approved multilingual library may justify evaluation later.

**Current evidence status:** **NOT NEEDED**.

**What it does not do:** KinderFlow makes no current RAG claim and does not need semantic retrieval to demonstrate the bounded MVP.

## Agentic AI

**What problem it solves:** Autonomous planning can choose tools and actions when a path cannot be defined in advance.

**Where it appears:** It does not appear in the customer-facing or runtime product.

**Why it fits:** It does not fit the bounded MVP. A fixed content workflow is easier to inspect and govern while publication requires explicit approval. Agentic orchestration should be considered only if future exception volume makes a bounded, reversible use case credible.

**Current evidence status:** **NOT NEEDED**.

**What it does not do:** No autonomous agent prepares, approves, publishes, assigns, or delivers current KinderFlow content.

## Decision summary

| Technology or method | Product role | Evidence status | Decisive boundary |
|---|---|---|---|
| MediaPipe | Pose and hand landmark evidence | CURRENT WORKING | No sign recognition or certification |
| OpenCV | Local frame and video processing | CURRENT WORKING | Not AI or sign validation |
| ffmpeg | Browser-compatible preview delivery | CURRENT WORKING when installed | Not AI or movement analysis |
| Python | Local service and deterministic logic | CURRENT WORKING | Not production operations |
| JavaScript, HTML, CSS | Interactive role-based prototype | CURRENT WORKING | Browser state is not a real account system |
| Open Peeps | Character and line grammar | VERSIONED EVIDENCE | Style does not determine the sign |
| Deterministic SVG | Repeatable visual candidates | PARTIAL | All 18 candidates require review |
| Gemini FX | Illustrative motion preview | DEMO ONLY | Separate from the current run and landmarks |
| n8n | Visible workflow orchestration | VERSIONED EVIDENCE | Exact export plus historical successful execution; not production or later-adapter proof |
| LangSmith | Optional LLM trace and evaluation | PARTIAL | Local dry-run, no live trace |
| Optional LLM | Bounded family-copy draft | PARTIAL | No sign mechanics or publication authority |
| JSON Schema | Structured handoffs | CURRENT WORKING | Valid shape does not prove content correctness |
| Quality gates | Objective readiness rules | CURRENT WORKING | Passing is not professional approval |
| Human review | Content and release control | CURRENT WORKING locally | No authenticated production ledger |
| Provenance and hashes | Identity and silent-change detection | CURRENT WORKING locally | Not ownership or security proof |
| Git and GitHub | Version and evidence history | CURRENT WORKING locally | Versioning does not validate a claim |
| Tableau | Round 1 opportunity view | VERSIONED EVIDENCE | Not a production or pilot dashboard |
| Statistical analysis | Future pilot interpretation | FUTURE | No real pilot outcome |
| RAG | Large-library retrieval | NOT NEEDED | Exact sign-ID retrieval is sufficient |
| Agentic AI | Open-ended orchestration | NOT NEEDED | Fixed workflow is safer for this scope |

## Related evidence

- [POC documentation](../poc/poc_documentation.md)
- [MVP documentation](../mvp/mvp_documentation.md)
- [Workflow documentation](../workflow/kinder_signs_n8n_workflow.md)
- [System one-page summary](kinder_signs_system_one_page.md)
- [Final claims matrix](final_claims_matrix.md)
- [Responsible AI audit](audits/responsible_ai_audit.md)
- [Dashboard documentation](../dashboard/dashboard_documentation.md)

The smallest defensible system is a controlled reference, Computer Vision evidence, deterministic checks, human approval, and reusable family material. Course technologies extend that centre only where evidence and operating need justify them.
