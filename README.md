# KinderFlow — Early Childhood Digital Growth

KinderFlow is an early-stage school-led digital platform concept for extending nursery-school routines into the home. Its first developed product is **Kinder Signs**.

Kinder Signs is a centrally managed **Signs & Flashcards Library**. KinderFlow prepares and governs the content; an educator selects an available sign and assigns it to a group or child; families receive the corresponding guidance. The school does not create sign videos or operate Computer Vision, LLM, n8n or LangSmith workflows.

## Product boundary

The current internal content flow is:

```text
Validated/reference adult sign video
→ Computer Vision movement check
→ movement data and human-inspectable evidence
→ content and visual preparation
→ human review
→ publication only when every gate is satisfied
→ eligible school library
→ group or child assignment
→ family output
```

Computer Vision measures whether movement landmarks were captured sufficiently for review. It does not certify linguistic sign correctness. No child video, child-performance scoring, developmental assessment, emotion recognition or automated educational decision is part of the current product scope.

## What works now

- A local Python MVP accepts an MP4 reference, runs the existing MediaPipe pipeline and returns run-specific movement evidence and controlled technical states.
- The committed reference evidence contains 332 analysed frames, 100% pose coverage, 93.98% dominant-hand coverage and 20 missing hand frames. Its motion-representation status is `PARTIAL`, leading to `Proceed with conditions`; these values apply only to that run.
- A logical human-review gate separates technical processing from publication.
- Content Operations provides shared records, provenance, state transitions, deterministic publication checks, an audit log and a five-sign engineering regression set.
- The Content Engine supports `HUMAN` and `LLM_ASSISTED` methods. `DRY_RUN` is evidenced; `NOT_APPLICABLE` is used for human-only content. Real external `LIVE` LLM execution and a live LangSmith trace are not yet evidenced.
- Flashcard Studio provides deterministic English/Spanish previews for Flashcard and Routine Card outputs. Browser Print / Save as PDF is implemented; final saved-PDF visual QA remains pending. PNG export is disabled and labelled as a prototype.
- Local School Admin and Family Preview pages demonstrate the intended experience without real delivery or personal data.

## Current MORE state

MORE is an **internal visual and content proof**, not a published school asset.

| State | Current evidence |
|---|---|
| Source | Review Needed; confirmation pending |
| Technical | Review Needed / Proceed with conditions |
| Artwork | Needs Artwork; internal proof only |
| Hand review | Needs Review |
| Quality gate | Blocked where publication requirements are unmet |
| Human review | Pending |
| Library | Blocked |
| Publication | Draft; not available to schools |

The final character, reviewed hand pose and production avatar are not complete. The product principle remains:

> The character defines the look. The validated reference movement defines the sign.

## Prototype and planned work

The following are not production capabilities:

- persistent publication and reviewer identity;
- real school accounts, authentication or tenant isolation;
- real school/family delivery or integrations;
- production analytics and security operations;
- final reviewed character/avatar rendering;
- live LangSmith evidence;
- real PNG export;
- commercial billing or payment;
- production infrastructure.

The n8n file is an **importable reference workflow / orchestration design**. Current-version execution in an n8n runtime is not evidenced here.

## Business model and validation programme

The business hypothesis is school-led B2B/B2B2C: the nursery school or school group is the intended payer; educators are operational users; families and children are beneficiaries.

The evidence supports further validation, not commercial validation or product-market fit. The reconciled plan is an **8–9 week validation programme**, including approximately **3–4 weeks of controlled service testing**. A proposed starting scale is **2–3 nursery schools**, with **3–5 signs** as a pilot assumption. Neither scale is empirically validated.

The reconciled validation-budget estimate is **€5.5k–€17.3k**. Pricing, willingness to pay, operating cost and ROI remain `TBD` until pilot assumptions are agreed and measured.

## Run the local MVP

The environment evidenced in this repository is:

- Python 3.9.6;
- MediaPipe 0.10.14 legacy Solutions API;
- local `poc_env`.

Python 3.11/3.12 remains the target/recommended clean environment but has not been revalidated in this evidence pass. The current default Python 3.13 environment is not equivalent: its MediaPipe 1.0.1 installation does not expose the legacy `solutions` API.

From the repository root, using the evidenced local environment:

```bash
poc_env/bin/python mvp/app.py
```

Open:

- [Create a Sign](http://127.0.0.1:8000/create-sign.html)
- [KinderFlow Hub](http://127.0.0.1:8000/index.html)
- [Master Content Studio](http://127.0.0.1:8000/content-studio.html)
- [Flashcard Studio](http://127.0.0.1:8000/flashcards.html)
- [School Admin](http://127.0.0.1:8000/school.html)
- [Family Preview](http://127.0.0.1:8000/family.html)

The demo reference is private local material and is not committed. Confirm its source rights, sign identity and presentation permission before external use.

## Repository structure

```text
assets/          Visual-source inventories and hand-pose review evidence
build/           Versioned demo publication packages; current MORE package is blocked
compliance/      Preliminary internal GDPR and EU AI Act assessments
content_ops/     Shared state, provenance, quality gates and regression set
cost_timeline/   Validation timeline and reconciled planning budget
dashboard/       Round 1 Tableau evidence
data/            Dashboard datasets and source register
docs/            Product, architecture, evidence and audit notes
feedback/        Round 1 feedback and decision
mvp/             Local Create a Sign and Content Engine service
poc/             Reproducible Computer Vision feasibility evidence
presentation/    Capstone presentation assets
prototype/       Static and local-service product interfaces
research/        Round 1 market and use-case research
workflow/        n8n reference workflow, quality gate and LangSmith dry-run
```

## Evidence and tests

Run from the repository root with a compatible environment:

```bash
poc_env/bin/python -m unittest discover -s content_ops/tests -v
poc_env/bin/python -m unittest discover -s mvp/tests -v
poc_env/bin/python -m unittest discover -s poc/tests -v
```

The real demo-video integration test is opt-in because it processes private local media:

```bash
KINDERFLOW_RUN_INTEGRATION=1 poc_env/bin/python -m unittest mvp.tests.test_mvp.DemoIntegrationTest -v
```

See `mvp/README.md`, `mvp/mvp_documentation.md`, `prototype/README.md` and `workflow/kinder_signs_n8n_workflow.md` for component-level instructions and limitations.
