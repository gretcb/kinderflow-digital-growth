# Course technologies applied to Kinder Signs

These are founder notes, not a claim that every repository component came from the bootcamp. The rule is simple:

> We use a technology because Kinder Signs has a problem that requires it, not because it appeared in the bootcamp.

## A. Course technologies currently used

### n8n

- **What it is:** A visual workflow-orchestration tool.
- **What we learned/used it for in the course:** Connecting structured steps, branching on results and passing outputs between tools.
- **How Kinder Signs uses it:** The workflow design loads MORE source data, adds bounded CV context, checks the schema, prepares optional LLM wording, runs a quality gate and routes the result to human review preparation.
- **Why Kinder Signs needs it:** It can make repeated content-preparation steps visible and reusable when operations move beyond local scripts.
- **Simple example:** `MORE → load source → check readiness → optional wording draft → quality gate → human-review package`.
- **Current implementation status:** Credential-free export and detailed specification exist. The content-operations adapter contract exists. Target n8n runtime execution is not evidenced in the repository.
- **What would happen without it:** The same steps could run in Python or be performed manually; the product would still work, but workflow ownership and hand-offs would be less visible.

n8n is not the product. It does not decide whether a sign is correct and must not approve publication autonomously.

### LLM

- **What it is:** A model that generates or edits text from instructions and context.
- **What we learned/used it for in the course:** Prompting, structured output, constraint setting and evaluation of generated text.
- **How Kinder Signs uses it:** Optionally turns supplied sign/routine content into concise family wording.
- **Why Kinder Signs needs it:** It may help produce controlled wording variants when the content volume justifies it.
- **Simple example:** Approved routine context becomes a short “Try it during snack time” draft.
- **Current implementation status:** Prompt, optional live script, sample output and deterministic gate exist. The current content manifests use human-authored copy, so LLM use is `not_applicable` there.
- **What would happen without it:** Human-authored family copy and deterministic templates would still support the core product.

The LLM is deliberately not used for hand shape, movement, sign correctness, professional validation or autonomous publication.

### LangSmith

- **What it is:** A tool for tracing and evaluating LLM behaviour.
- **What we learned/used it for in the course:** Seeing model inputs/outputs, attaching evaluation results and debugging a text workflow.
- **How Kinder Signs uses it:** It defines a trace for the optional family-copy step and evaluates source adherence, claims, movement-note fidelity, JSON structure and review-gate preservation.
- **Why Kinder Signs needs it:** If a model helps with wording, the team should be able to inspect what it received and produced.
- **Simple example:** `approved context → generated family wording → criterion-level evaluation result`.
- **Current implementation status:** **Dry-run:** functional without keys and writes a local summary. **Live:** script path exists, but no live repository trace is claimed.
- **What would happen without it:** The core sign and flashcard flows would still work; the team would lose dedicated trace/evaluation evidence for LLM-assisted copy.

A trace is simply a saved record of one model step: its input, configuration, output and associated checks. LangSmith does not evaluate MediaPipe, hands, movement fidelity or sign correctness.

### Deterministic quality gates

- **What it is:** Ordinary code that applies explicit true/false rules.
- **What we learned/used it for in the course:** Separating objective validation from subjective model judgement.
- **How Kinder Signs uses it:** Checks required labels/routines, known artwork status, hand review, banned claims, preserved identifiers and human approval.
- **Why Kinder Signs needs it:** A missing field or approval is a fact, not a question for an LLM.
- **Simple example:** If `hand_review_status` is not `REVIEWED`, publication remains blocked.
- **Current implementation status:** Functional and covered by workflow and content-operations tests.
- **What would happen without it:** Readiness would depend on informal checking and errors could pass silently.

### Human-in-the-loop / human review

- **What it is:** A person retains control of a decision after automated assistance.
- **What we learned/used it for in the course:** Designing systems where AI output is evidence or a draft, not an automatic final decision.
- **How Kinder Signs uses it:** Publication policy requires explicit human approval; CV and LLM results cannot set `PUBLISHED` directly.
- **Why Kinder Signs needs it:** The material is educational, sign correctness is professional judgement, and the intended beneficiaries are very young children.
- **Simple example:** A technically usable MORE capture moves to `Ready for human review`, not directly to the school library.
- **Current implementation status:** Enforced in local state/policy tests; reviewer UI is simulated and not authenticated.
- **What would happen without it:** Technical or generated output could be mistaken for approved educational content.

### AI governance / EU AI Act thinking

- **What it is:** Defining intended purpose, responsibility, limits, risk and oversight before deployment.
- **What we learned/used it for in the course:** Asking what each AI component is allowed to do and what controls remain human.
- **How Kinder Signs uses it:** The responsibility matrix separates Computer Vision, LLM, LangSmith, n8n and human review.
- **Why Kinder Signs needs it:** Several technical components touch one content chain; unclear boundaries create misleading claims and unsafe automation.
- **Simple example:** Computer Vision may set a technical status but cannot approve publication.
- **Current implementation status:** Responsibility matrix, state rules and documentation exist. No legal classification or certification has been completed.
- **What would happen without it:** The team could conflate hand coverage, text evaluation and professional sign approval.

### GDPR / privacy by design

- **What it is:** Limiting personal data and designing handling controls before collection.
- **What we learned/used it for in the course:** Data minimisation, purpose limitation, role/retention questions and human rights considerations.
- **How Kinder Signs uses it:** The core content-production workflow uses adult reference material and does not require child names, child photos/videos, health data or developmental profiles.
- **Why Kinder Signs needs it:** Children merit particular protection, and unnecessary data creates risk without improving the core use case.
- **Simple example:** Synthetic `school_id`, `group_id` and—only if necessary—`family_id` can support pilot measurement without child names.
- **Current implementation status:** No-child-video product decision, local processing, ignored media and a minimal pilot schema exist. No GDPR certification is claimed.
- **What would happen without it:** The MVP could collect sensitive child data simply because it was available, increasing risk and operating burden.

### Testing / evaluation

- **What it is:** Repeated checks that known behaviour still works and failures are controlled.
- **What we learned/used it for in the course:** Evaluating software and AI workflows across success and failure cases, not only one happy path.
- **How Kinder Signs uses it:** POC tests, MVP input/state/schema tests, content-operations policy/state/provenance tests and workflow quality checks.
- **Why Kinder Signs needs it:** Changes to processing or publishing rules must not silently weaken boundaries.
- **Simple example:** One test proves `DRAFT → PUBLISHED` is rejected; another proves invalid video extensions are rejected.
- **Current implementation status:** Automated local suites exist; the real demo-video integration test is opt-in because it runs MediaPipe.
- **What would happen without it:** A refactor could break upload safety, metric mapping or publication controls without warning.

### Evaluation / golden set concept

- **What it is:** A small, stable set rerun whenever the system changes.
- **What we learned/used it for in the course:** Comparing behaviour consistently rather than choosing a new example each time.
- **How Kinder Signs uses it:** MORE, EAT, WATER, ALL DONE and HELP are checked for schema, provenance and readiness.
- **Why Kinder Signs needs it:** It prevents the content-operations rules being designed only around the most complete example.
- **Simple example:** All five currently pass schema checks and all five remain blocked from publication for visible reasons.
- **Current implementation status:** Functional local regression harness and JSON report.
- **What would happen without it:** Rule changes could appear successful on MORE while breaking or ignoring the other planned items.

This is an engineering/product evaluation set. It is not linguistic certification and not a sign-accuracy benchmark.

### Data visualisation / Tableau

- **What it is:** Turning structured data into charts and dashboards for decisions.
- **What we learned/used it for in the course:** Building an evidence-backed view of a market or product question.
- **How Kinder Signs uses it:** Round 1 includes a Tableau market-opportunity workbook and image based on the project dataset.
- **Why Kinder Signs needs it:** It supported the decision to continue investigating Kinder Signs rather than replacing product judgement with intuition.
- **Simple example:** The Round 1 dashboard compares market/opportunity evidence; a future pilot dashboard could show adoption, educator activation, family engagement, content-operations time and asset use.
- **Current implementation status:** Round 1 dashboard artifact exists. No production/pilot dashboard is being built now.
- **What would happen without it:** The market decision would have less accessible quantitative support; the functional product would still run.

### Statistical analysis

- **What it is:** Methods for describing data, comparing groups and judging whether a pattern is credible.
- **What we learned/used it for in the course:** Looking at distributions and uncertainty instead of relying on anecdotes.
- **How Kinder Signs uses it:** It does not yet analyse real pilot behaviour because none exists. The future use is to inspect engagement, task time and variation across participants.
- **Why Kinder Signs needs it:** A pilot will produce small, uneven samples that must not be overinterpreted.
- **Simple example:** Compare the distribution of educator assignment times rather than reporting only the fastest example.
- **Current implementation status:** Future/partial: metric definitions exist; no pilot statistical result exists.
- **What would happen without it:** The team could make decisions from isolated stories or averages without understanding variation.

## B. Additional engineering introduced for Kinder Signs

These elements were added because the product needed them, not because the bootcamp required them.

### Computer Vision / MediaPipe

- **What it is:** MediaPipe converts video frames into structured body and hand landmarks.
- **What we learned/used it for in the course:** It was not part of the core bootcamp curriculum; it was introduced because movement is central to this product.
- **How Kinder Signs uses it:** `video → joint points → time-ordered movement evidence`.
- **Why it is needed:** Movement is central to the product and general text/image tools cannot preserve it reliably.
- **Simple example:** The reference run detected the dominant hand in 312 of 332 frames.
- **Current status:** Functional POC and local upload MVP using the legacy MediaPipe Solutions API.
- **Without it:** Kinder Signs would lose its structured movement evidence and differentiating technical MVP.

It measures capture structure. It does not certify sign correctness.

### Landmark / skeleton representation

- **What it is:** Landmarks are detected points; a skeleton connects selected points into an inspectable view.
- **What we learned/used it for in the course:** This is product-specific CV engineering rather than a course requirement.
- **How Kinder Signs uses it:** Produces raw/normalized coordinates, trajectories, plots and an overlay preview.
- **Why it is needed:** A reviewer needs evidence between the original pixels and any future visual output.
- **Simple example:** The wrist path can be measured while unresolved frames remain visible rather than guessed.
- **Current status:** Functional locally.
- **Without it:** The technical result would be a black box with no clear movement representation.

### State machine

- **What it is:** A list of allowed status changes.
- **What we learned/used it for in the course:** The course supplied governance and workflow ideas; the explicit state-machine implementation was added for Kinder Signs.
- **How Kinder Signs uses it:** Controls technical, content, visual and publication states.
- **Why it is needed:** It prevents important review steps being skipped.
- **Simple example:** `DRAFT → READY FOR HUMAN REVIEW → APPROVED → PUBLISHED`; `DRAFT → PUBLISHED` is blocked.
- **Current status:** Functional and tested.
- **Without it:** Any UI or workflow could jump directly to an unsupported state.

### Provenance

- **What it is:** Knowing where an item and its evidence came from.
- **What we learned/used it for in the course:** Traceability was a course theme; this file-level provenance model is product engineering.
- **How Kinder Signs uses it:** Records the reference, CV evidence, content version, visual version, review and package.
- **Why it is needed:** A commercial library must know which exact sources support an item.
- **Simple example:** MORE points to a POC summary but states that the source identity still needs confirmation.
- **Current status:** Functional local manifests with bounded claims.
- **Without it:** The team could not reliably explain or audit an item’s origin.

### SHA-256 hash

- **What it is:** A digital fingerprint that changes when the file/data changes.
- **What we learned/used it for in the course:** This was not added to demonstrate a course tool; it supports Kinder Signs change detection.
- **How Kinder Signs uses it:** Verifies that referenced sign data and technical evidence still match the manifest.
- **Why it is needed:** It detects silent changes between review/package runs.
- **Simple example:** Editing `signs.json` would make its stored fingerprint fail the provenance check.
- **Current status:** Functional and tested.
- **Without it:** A path could still exist even though its content changed.

It is not blockchain, proof of ownership or a complete security guarantee.

### Audit log

- **What it is:** An ordered record of important events.
- **What we learned/used it for in the course:** Observability/auditability informed the need; the local JSONL helper is additional engineering.
- **How Kinder Signs uses it:** Appends local events such as a quality-gate result with a sign/version and actor type.
- **Why it is needed:** Operations need to reconstruct what happened.
- **Simple example:** `content prepared → artwork attached → hand reviewed → human approved → package built`.
- **Current status:** Local append/idempotency helper and JSONL evidence; not a tamper-proof service.
- **Without it:** Investigating a failed or disputed content change would be harder.

### Idempotency

- **What it is:** Repeating the same operation does not create accidental duplicates or corrupt state.
- **What we learned/used it for in the course:** Reliable workflow retries are an engineering concern; the implementation was added for the product.
- **How Kinder Signs uses it:** The same package inputs produce the same package ID; duplicate event IDs are not appended twice.
- **Why it is needed:** Workflow retries are normal and should be safe.
- **Simple example:** Running “prepare MORE v1 for review” twice should reuse/update one review package, not create two versions.
- **Current status:** Functional and tested locally.
- **Without it:** Retries could create confusing duplicate assets and audit events.

### Versioned publication package

- **What it is:** A fixed combination of source, content, visual and review records for one candidate release.
- **What we learned/used it for in the course:** The course reinforced governed outputs; this package structure is Kinder Signs-specific.
- **How Kinder Signs uses it:** Writes `content.json`, `visual.json`, `review.json`, `library_item.json` and a hash manifest.
- **Why it is needed:** Approval should apply to a known combination, not to a title that can change underneath it.
- **Simple example:** MORE v1 package ID is derived from its exact structured inputs.
- **Current status:** Functional local build; current package remains draft/blocked.
- **Without it:** A published label could point to mismatched or silently changed parts.

### Content Operations

- **What it is:** The operating layer coordinating source, technical evidence, content, artwork, review and publication.
- **What we learned/used it for in the course:** It was not a separate course technology. It was introduced after Flashcard Studio exposed a product need for coordinated readiness.
- **How Kinder Signs uses it:** Evaluates readiness and explains why each of five signs is blocked or can advance.
- **Why it is needed:** Flashcard Studio showed that rendering alone is not enough; a real library needs controlled inputs and approval.
- **Simple example:** MORE copy can be ready while its visual and hand review remain incomplete.
- **Current status:** Functional local rules/report/package; admin interactions remain prototype state.
- **Without it:** The team would have separate files and screens but no consistent definition of “ready.”

## C. Course technologies not currently needed

### RAG

- **What it is:** Retrieving relevant documents from a larger knowledge base and placing them into an LLM prompt.
- **What we learned/used it for in the course:** Grounding model responses in selected source material.
- **How Kinder Signs uses it:** It does not currently use RAG.
- **Why Kinder Signs needs it:** It does not today; a small structured source record is enough.
- **Simple example:** The MORE record is loaded directly by ID instead of searched semantically.
- **Current implementation status:** Not implemented. A large approved multilingual library might justify it later.
- **What would happen without it:** Nothing is lost in the current MVP.

### Airtable

- **What it is:** A hosted table/database interface often used for lightweight operations tools.
- **What we learned/used it for in the course:** Organising records and workflow-style content operations.
- **How Kinder Signs uses it:** It does not currently use Airtable.
- **Why Kinder Signs needs it:** It does not today; local JSON/manifests are sufficient and avoid a second source of truth.
- **Simple example:** The five sign manifests live in the repository rather than an Airtable base.
- **Current implementation status:** Deferred. Collaborative operations could justify it before a dedicated CMS.
- **What would happen without it:** The current local workflow continues unchanged.

### Agents / autonomous agents

- **What it is:** A system that chooses tools/actions across several steps with some autonomy.
- **What we learned/used it for in the course:** Delegating multi-step tasks where the path cannot be fully predetermined.
- **How Kinder Signs uses it:** It does not use an autonomous product agent.
- **Why Kinder Signs needs it:** It does not for the controlled content path; the sequence is known and publication needs explicit approval.
- **Simple example:** A deterministic gate—not an agent—decides whether required review evidence is missing.
- **Current implementation status:** Not implemented; only a bounded, reversible future support task might justify it.
- **What would happen without it:** The intended workflow remains clearer and more predictable.

### Subagents

- **What it is:** A software-development technique where coding agents split independent tasks.
- **What we learned/used it for in the course:** Parallel research, coding or review work.
- **How Kinder Signs uses it:** It is not a customer-facing or runtime capability.
- **Why Kinder Signs needs it:** The product does not need it; a development team might choose it for delivery work.
- **Simple example:** One coding agent could review tests while another edits documentation, without changing the customer architecture.
- **Current implementation status:** Not a product feature.
- **What would happen without it:** The product loses nothing.

### Hooks / dark-factory concept

- **What it is:** Automated checks/events around AI-assisted software delivery, intended to make actions observable and enforce rules.
- **What we learned/used it for in the course:** Improving visibility and control in highly automated engineering workflows.
- **How Kinder Signs uses it:** The repository uses tests, logs and Git checks, not a production dark-factory setup.
- **Why Kinder Signs needs it:** It does not at the current team/release scale.
- **Simple example:** `git diff --check` is a simple delivery check; it is not evidence of a production hooks platform.
- **Current implementation status:** Not implemented as a product or production engineering system.
- **What would happen without it:** Current manual/local release checks remain adequate for the capstone.

### Chaos / robustness testing

- **What it is:** Deliberately introducing failures to see how a system behaves.
- **What we learned/used it for in the course:** Testing recovery and failure handling beyond the happy path.
- **How Kinder Signs uses it:** It uses controlled invalid-file, insufficient-coverage and policy-failure cases, not a chaos system.
- **Why Kinder Signs needs it:** Controlled failure tests are useful now; broad chaos testing is not.
- **Simple example:** An empty MP4 returns a controlled error instead of a traceback.
- **Current implementation status:** Partial through focused tests. No Chaos Agent exists or is needed.
- **What would happen without it:** The team would know less about basic failure messages, but a full chaos platform would add little today.

### Telegram

- **What it is:** A messaging transport/interface.
- **What we learned/used it for in the course:** Triggering or receiving workflow messages.
- **How Kinder Signs uses it:** It does not.
- **Why Kinder Signs needs it:** No current school/family requirement points to Telegram.
- **Simple example:** The prototype prepares a family card but does not send it to a Telegram chat.
- **Current implementation status:** Not implemented.
- **What would happen without it:** Nothing is lost; Kinder Signs remains channel-neutral until customer evidence supports an integration.

## D. Technology map

| Technology | From bootcamp? | Used in product today? | What problem it solves | Status |
|---|---|---|---|---|
| n8n | Yes | Partial | Repeatable workflow routing | Design/export; runtime proof pending |
| LLM | Yes | Partial | Optional family-copy drafting | Optional script/sample |
| LangSmith | Yes | Partial | LLM trace and evaluation | Dry-run |
| Deterministic gates | Yes | Yes | Objective readiness checks | Functional |
| Human-in-the-loop | Yes | Yes | Publication control | Policy functional; UI local |
| AI governance | Yes | Yes | Responsibility boundaries | Documented/encoded |
| Privacy by design | Yes | Yes | Avoid unnecessary child data | Current architecture decision |
| Testing/evaluation | Yes | Yes | Detect regressions/failures | Functional suites |
| Golden set | Yes | Yes | Stable five-item readiness regression | Functional |
| Tableau | Yes | Yes | Round 1 market evidence | Completed Round 1 artifact |
| Statistical analysis | Yes | No | Future pilot interpretation | Future; no pilot data |
| MediaPipe CV | No | Yes | Structured movement evidence | Functional local MVP |
| State machine | No | Yes | Controlled status transitions | Functional |
| Provenance/hashes | No | Yes | Source/version change detection | Functional local |
| Audit log/idempotency | No | Yes | Traceable, retry-safe operations | Functional local helper |
| Publication package | No | Yes | Bind one release candidate | Functional, currently blocked |
| RAG | Yes | No | Large-knowledge retrieval | Not needed |
| Airtable | Yes | No | Collaborative lightweight CMS | Deferred |
| Autonomous agents | Yes | No | Open-ended tool/action selection | Not needed |
| Subagents | Yes | No | Development-task delegation | Not a product feature |
| Hooks/dark factory | Yes | No | Automated development controls | No production evidence |
| Chaos testing | Yes | Partial | Failure behaviour | Controlled cases only |
| Telegram | Yes | No | Messaging transport | Not needed |

## E. If I removed this technology, what would Kinder Signs lose?

- **MediaPipe:** We would lose the structured movement evidence used to inspect a reference video.
- **Movement representation:** We would lose the visible bridge between video and a future controlled visual output.
- **Deterministic gates:** We would lose repeatable checks for objective readiness facts.
- **State machine:** We would lose enforced separation between draft, review, approval and publication.
- **Human review:** We would lose the control preventing technical/AI output from becoming educational content automatically.
- **Flashcard templates:** We would lose consistent printable output and return to manual layout work.
- **Provenance and hashes:** We would lose a simple way to link and detect changes in source evidence and versions.
- **Audit log/idempotency:** We would lose basic event traceability and safe repeated operations.
- **n8n:** We would lose the reusable visual orchestration layer, but Python/manual steps could still run the product.
- **LLM:** We would lose optional wording assistance, but approved human copy could still operate Kinder Signs.
- **LangSmith:** We would lose trace/evaluation of LLM-assisted copy, but the core sign workflow would still function.
- **Tableau:** We would lose an accessible Round 1 market-evidence view, not the product runtime.
- **Testing/golden set:** We would lose early warning when changes break known behaviours across the five planned signs.

## F. Do not force course technology into the product

RAG, Airtable, autonomous agents, subagents, Telegram and a Chaos Agent would currently add architecture without solving the highest-priority problem. Live LLM/LangSmith/n8n should also remain conditional: use them only when actual content volume and operations justify them.

The core product can be explained without pretending every course tool is required:

```text
controlled reference
→ Computer Vision evidence
→ deterministic content and asset checks
→ human approval
→ reusable family material
```

That is the smallest defensible centre of the current system.
