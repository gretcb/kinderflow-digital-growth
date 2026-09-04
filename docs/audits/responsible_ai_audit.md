# KinderFlow Responsible AI Audit

**Audit date:** 4 September 2026
**Frozen repository baseline:** 8eb0742, Freeze connected KinderFlow capstone demo
**Scope:** Kinder Signs local MVP, documented workflow, assets, and proposed controlled pilot

This audit reports evidence states. It is not a safety certificate, professional sign-language approval, legal advice, or proof that the product is ready for production.

## Executive assessment

Kinder Signs has a defensible narrow purpose: help a human content team turn an adult sign reference into reviewable technical evidence and reusable family material. Computer Vision is the strongest active AI evidence. The repository also contains an optional model-assisted wording path, but only local and dry-run evaluation is evidenced. It does not prove a live external model run.

The product includes meaningful controls: local processing, bounded inputs, deterministic validation, explicit review routes, source registries, versioned assets, and no autonomous publication. It also has material gaps: no production reviewer identity or approval ledger, no qualified sign approval for the current draft visuals, incomplete source and Gemini usage rights, no production correction process, no secure family-account system, and a mismatch between the six-sign registry and the older five-sign content package.

The evidence supports controlled pilot preparation. It does not support external pilot launch until the stated gates close.

| Dimension | Evidence state | Current conclusion |
| --- | --- | --- |
| Narrow intended purpose | Evidence present | Adult-reference content support, not child assessment |
| Human oversight | Partial evidence | Review routes exist; production accountability does not |
| Technical explainability | Evidence present | Landmarks, coverage, missing frames, plots, and previews are inspectable |
| Sign and visual correctness | Operational gap | All current visual options require qualified review |
| Provenance and rights | Partial evidence | Strong identity records; several usage rights remain unresolved |
| Privacy | Evidence present for local MVP; pilot control required | No real child data or live personal-data model transfer is evidenced |
| Fail-closed behaviour | Partial evidence | Many validation states block progress; Gemini display rights are not fully fail-closed |
| Accessibility and inclusion | Partial evidence | Spanish and bilingual formats exist; user testing and accessibility conformance are absent |
| Complaints and corrections | Operational gap | No production intake, service level, recall, or notification process |
| Environmental evidence | Measurement gap | Design choices are documented; energy and carbon are unmeasured |

## People, purpose, and potential harm

### People in scope

- adult reference performers;
- KinderFlow content operators and reviewers;
- nursery owners, administrators, and educators;
- families and caregivers; and
- children as beneficiaries and potentially affected persons.

Children are not buyers or reference-video subjects in the intended core workflow.

### Intended purpose

The operator supplies an adult reference video and declares that it is suitable for the selected input path. That declaration does not itself prove authority, consent, or sign correctness. MediaPipe extracts pose and hand landmarks, and the service creates technical evidence. A human reviews the reference, selects or reviews a pose, reviews draft visuals and family material, and controls publication.

The product does not assess a child. It does not recognise emotion, establish biometric identity, categorise a person, diagnose development, score learning, or make an educational decision.

### Current Family View boundary

The Little Steps Nursery assignment experience uses synthetic records and local or session-based state. Family View displays a basic guidance prototype.

A family-facing guidance prototype exists. A personalised assignment-driven family library remains a next product iteration. Current screens do not prove real delivery, account identity, access control, or cross-session persistence.

### Foreseeable harms

- a technically measurable pose is described as a correct sign;
- an incorrect hand shape, palm direction, contact point, or movement reaches a family;
- a source is used without performer authority or distribution rights;
- a generated or rewritten claim sounds clinical or developmental;
- a Gemini demo is mistaken for current landmark-generated output;
- one family sees another child's assignment;
- technical metrics become a child score after scope expansion;
- missing or partial landmarks are hidden from the reviewer;
- a correction cannot reach every copy of an asset; or
- reviewers approve content without adequate training or independence.

## AI and automation inventory

| Component | What it does | Evidence | What it does not prove |
| --- | --- | --- | --- |
| MediaPipe | Extracts adult pose and hand landmarks | Local pipeline and versioned WATER evidence | Sign correctness, identity, emotion, or child ability |
| OpenCV | Reads and processes video frames | Local pipeline | AI intelligence or linguistic validity |
| Deterministic normalization and thresholds | Converts landmarks to body-relative evidence and review states | Code and tests | Professional approval |
| Optional language model | Can draft bounded family wording from supplied sign and routine content | Provider path, schema, samples, deterministic evaluation | Live execution, truth, publication approval, or CV quality |
| LangSmith path | Defines trace and evaluation for the optional wording step | Dry-run summary with network calls false | A live trace or evaluation of movement fidelity |
| n8n | Represents fixed orchestration and review preparation | Exact importable JSON and documentation | A proven final target-runtime run |
| Deterministic SVG composition | Creates repeatable visual candidates | Six sign packages and 18 files | Correct fingers, palms, contact, direction, or readability |
| Gemini FX files | Provide pre-generated illustrative motion direction | Three registered local MP4 files | Current-run output, landmark control, rights, or sign certification |
| Nursery and Family Views | Simulate product handoff | Local interfaces and synthetic data | Production assignment or secure family delivery |

## Technical evidence interpretation

### Versioned WATER evidence

The committed Round 1 WATER reference records:

- 332 processed frames;
- 100.00 percent pose coverage;
- 93.98 percent dominant right-hand coverage;
- 20 missing hand frames;
- extraction status pass; and
- motion representation partial.

Evidence:

- [WATER validation summary](../../poc/output/validation_summary.json)
- [WATER movement summary](../../poc/output/diagnostics/sign_reference_motion_summary.json)
- [POC documentation](../../poc/poc_documentation.md)

The 93.98 percent value is hand-detection coverage in that reference run. It is not 93.98 percent sign accuracy.

### Current MORE evidence boundary

The registered MORE reference input is present and hash-mapped. The canonical registry does not assign the versioned WATER diagnostics to MORE. A current MORE run with 285 frames, 100 percent pose coverage, and 91.93 percent dominant-hand coverage was observed only in an ignored local run directory. That local record must not be presented as versioned repository evidence.

The registry therefore describes MORE as having a reference input without a canonical analysed run. This separation prevents metrics from one sign being used to support another.

### Status vocabulary

Keep these decisions separate:

- extraction coverage;
- motion representation;
- content readiness;
- sign review;
- visual review;
- rights clearance; and
- publication status.

Extraction pass means that the system created usable technical evidence. It does not mean the sign, illustration, wording, or publication is approved.

## Human oversight

### Current evidence

The local workflow asks the operator to:

- declare the reference validated;
- review the source video;
- inspect coverage, missing-frame, movement, and preview evidence;
- use a tracked pose only when the technical threshold permits it;
- select a representative frame when tracking cannot support the next step;
- review sign-specific visual candidates;
- review generated family material; and
- control local publication actions.

The EAT flow has an explicit reviewed-reference fallback. Missing or partial evidence is visible rather than silently converted into a quality claim.

### Operational gaps

The frozen product does not evidence:

- authenticated reviewer identity;
- role separation between creator and approver;
- qualified sign-review credentials;
- timestamped approval and rationale;
- an immutable publication record;
- review sampling or second review for high-risk exceptions;
- a correction and withdrawal service; or
- review-time and disagreement measurement.

UI approval buttons simulate governance. They are not a production control by themselves.

### Required authority

| Decision | Required reviewer |
| --- | --- |
| Adult source is authorised and suitable | Content and rights owner |
| Technical run is interpretable | Trained Computer Vision operator |
| Sign mechanics are correct | Qualified sign or Baby Sign reviewer |
| Illustration is readable and faithful | Qualified sign reviewer and visual reviewer |
| Family wording is accurate and bounded | Content reviewer |
| Asset may be released | Publication owner after all prior approvals |
| Asset must be corrected or withdrawn | Product Owner with Content Operations |

No model or deterministic rule may replace these decisions.

## Source fidelity, visuals, and provenance

### Six-sign evidence chain

The canonical registry covers MORE, HELP, EAT, SLEEP, MILK, and WATER. Each sign has three current static candidates. All 18 candidates remain draft and blocked from printable or school use.

Sign mechanics should follow this source order:

1. registered functional sign illustration;
2. curated sign knowledge;
3. registered reference video and relevant frames or movement evidence;
4. Open Peeps visual grammar; and
5. human sign and visual review.

### Open Peeps role

The provenance record identifies Open Peeps by Pablo Stanley, links to the official source, records CC0, and hashes the selected base components.

Open Peeps provides the base character and line grammar. It does not determine a sign's fingers, palm, contact, direction, or motion. KinderFlow adds deterministic, sign-specific anatomy from reviewed sources.

The character defines the look. The reviewed reference defines the sign.

Human review remains required because deterministic composition is repeatable, not self-validating.

### Hash meaning

Hashes support:

- exact asset identity;
- change detection;
- reproducible mapping; and
- linkage between evidence and a version.

A hash does not prove ownership, performer consent, lawful distribution, sign correctness, accessibility, or security.

### Rights gaps

Open Peeps provenance is recorded. Other founder-provided videos, functional illustrations, icons, reference PDFs, the current context image, and Gemini output need purpose-specific display, adaptation, and distribution decisions.

Reference flashcards and vendor icons are marked reference-only and cannot enter printable output. Current draft SVGs are marked non-printable until human review and publication approval.

### Registry and package drift

The current asset registry covers six signs and 18 visual candidates. The older content-operations manifests, golden-set report, prototype content-operations data, and built MORE package cover a five-sign wording workflow. MORE still points to WATER technical evidence there.

The golden-set report's passing result means schema and hash checks passed. It does not mean that rights, sign fidelity, visual quality, or publication readiness passed.

Required action:

1. reconcile canonical sign IDs;
2. assign technical evidence only to its source sign;
3. bind current visual and rights records;
4. regenerate the package;
5. complete qualified review; and
6. record explicit publication approval.

No current sign is registered as school-available or published.

## Gemini FX motion previews

The exact current mapping is:

| Sign | File | Current status |
| --- | --- | --- |
| MORE | mas.mp4 | Available as pre-generated demo only |
| HELP | ayuda.mp4 | Available as pre-generated demo only |
| MILK | leche.mp4 | Available as pre-generated demo only |
| EAT | None | Static workflow remains available |
| SLEEP | None | Static workflow remains available |
| WATER | None | Static workflow remains available |

These videos were prepared separately as illustrative motion previews. They are not generated automatically from the current MediaPipe run or its landmarks.

The registry records external-usage confirmation as pending. The files are not linguistically certified. The local service validates file identity and mapping, but it treats a null demo-display permission as available. This is a material rights-control gap.

Before external display, require:

- documented display and redistribution rights;
- confirmation of source inputs and permitted purpose;
- qualified sign and motion-fidelity review;
- clear separation from current-run evidence;
- a synthetic-content transparency assessment; and
- a withdrawal route.

## Direct MP4 intake

The direct URL path accepts one public HTTP or HTTPS MP4. It validates syntax, resolved address, redirects, type, time, and size. It pins the validated public destination, uses a generated local filename, removes partial files, and strips query parameters from stored provenance.

This supports safer local testing. It does not prove that the operator owns the video, that the adult agreed to the use, or that the sign is correct. It also is not a production fetch service.

Misuse controls still needed:

- authenticated and authorised operators;
- approved source or host policy;
- evidence of performer authority and licence;
- HTTPS-only production intake or a controlled object store;
- rate and concurrency limits;
- media decoder isolation;
- incident monitoring;
- deletion and access logs; and
- sanctions for prohibited child or third-party media.

## Privacy and child safeguards

### Current evidence

- the reference subject is intended to be an adult;
- the core workflow does not need a child's identity;
- the nursery and family records are synthetic;
- current processing is local;
- no real child account or production delivery exists;
- no live transfer of personal data to an LLM or LangSmith is evidenced;
- no age estimation, emotion recognition, identity matching, or child scoring exists; and
- the optional wording path can operate on sign and routine content without personal data.

### Pilot controls

- use group assignment by default;
- create a pseudonymous child assignment ID only when necessary;
- keep child media, health data, development notes, and free text out of scope;
- keep all nursery, staff, family, and child identifiers out of LLM and LangSmith inputs;
- implement family relationship verification, role access, and nursery separation;
- complete notices, lawful-basis analysis, contracts, retention, rights, and DPIA;
- log access and deletion; and
- stop the pilot on any unauthorised personal-data model transfer.

Detailed requirements appear in [the GDPR record](../../compliance/gdpr_documentation.md).

## Model-assisted wording

### Current evidence

The repository contains:

- a structured content contract;
- an optional provider call;
- JSON Schema validation;
- banned-claim and source-adherence checks;
- an importable n8n workflow design;
- evaluation cases; and
- a LangSmith dry-run with network calls false.

LangSmith covers the optional wording step only. It does not validate MediaPipe, hand shape, movement fidelity, or sign correctness.

### Responsible-use rules

- supply only approved sign and routine content;
- send no personal data;
- constrain length, tone, and fields;
- block clinical, developmental, diagnostic, or guaranteed-outcome claims;
- show source and model version to the reviewer;
- require human editing and approval;
- retain the draft, final text, checks, reviewer, and rationale; and
- prevent any failed or unreviewed output from family delivery.

The current evidence does not prove a live provider's behaviour, model drift, data retention, or incident response.

## Fail-closed and fallback assessment

| Control | Evidence state | Finding |
| --- | --- | --- |
| Invalid local upload | Evidence present | Rejected |
| Unsafe or private direct URL | Evidence present | Rejected |
| Wrong response type, excessive size, redirect, or timeout | Evidence present | Rejected and partial file cleaned |
| Missing or weak tracking | Evidence present | Reviewer sees partial state or selects a frame |
| Missing Gemini file or false display permission | Evidence present | Static flow remains available |
| Null Gemini display permission | Operational gap | File remains locally available |
| Failed wording quality check | Partial evidence | Deterministic sample blocks progression; production enforcement is not evidenced |
| Missing publication approval | Partial evidence | Registry blocks current signs, but no production delivery layer exists to test |

Transparent fallback is preferable to invented certainty. A static reviewed asset or human-selected frame is acceptable when the interface explains why it was used.

## Explainability and transparency

The reviewer can inspect:

- source video;
- reference and overlay previews;
- representative frames;
- pose and hand coverage;
- missing-frame counts;
- motion paths;
- warnings and fallback state;
- source asset and hash;
- sign-specific visual candidates; and
- structured wording checks.

Families should receive a plain explanation that material was prepared and reviewed by KinderFlow. They do not need raw technical metrics. If AI assistance materially shapes content or synthetic video is displayed, provide the disclosure required for that context.

Never present detection coverage as accuracy. Never describe a separately prepared Gemini file as current-run output.

## Accessibility and inclusion

### Evidence present

- Spanish and bilingual material modes;
- visual and text formats;
- consistent sign labels and routine context;
- browser print or Save as PDF path; and
- a static fallback when no Gemini video exists.

### Evidence missing

- WCAG conformance test;
- keyboard and screen-reader test across all routes;
- contrast and zoom evidence;
- caption and transcript policy for motion media;
- comprehension testing with families;
- testing across literacy, language, disability, and device conditions; and
- qualified review that visual candidates remain legible when printed.

The existence of two languages does not prove cultural or accessibility fairness. The pilot should measure comprehension and correction patterns by language and access mode without profiling children.

## Complaints, corrections, and withdrawal

The production service needs one accountable route for:

- incorrect sign mechanics;
- misleading family wording;
- accessibility barriers;
- source-rights claims;
- privacy requests;
- wrong-recipient access; and
- harmful or confusing synthetic media.

For each issue, record intake time, affected sign and version, severity, owner, containment, reviewer decision, correction, affected recipients, notification, and closure.

Critical sign, rights, or privacy issues should block the affected asset immediately. The system must be able to identify and withdraw every active copy. The current prototype does not provide this service.

## Risk register

| Risk | Evidence state | Current control | Required pilot control |
| --- | --- | --- | --- |
| Technical coverage becomes a quality claim | Present risk | Metric labels and documentation | Review every presentation surface and sales claim |
| Wrong sign mechanics | Present risk | Source hierarchy and draft state | Qualified sign approval for every asset |
| Rights or consent missing | Present risk | Registry status and hashes | Written authority, usage scope, expiry, and withdrawal |
| Gemini file mistaken for pipeline output | Present risk | Separate registry class and local disclosure | Rights, fidelity, and transparency gate |
| Child data enters AI path | Current evidence shows zero; future risk | Synthetic data and local flow | Field blocks, monitoring, contracts, and stop rule |
| Wrong family access | Not testable in current prototype | Session-only fixture | Production identity, tenant, relationship, and access tests |
| Unreviewed publication | Current registry blocks all signs | Human review UX | Authenticated approval ledger and delivery enforcement |
| Reviewer inconsistency | Measurement gap | Review prompts | Training, rubric, second review, disagreement measure |
| Unsupported family claim | Partial evidence | Banned-claim checks | Live-provider evaluation and human approval |
| Accessibility exclusion | Measurement gap | Basic bilingual formats | Formal test and family comprehension study |
| Correction fails to propagate | Operational gap | None | Version recall and recipient notification |
| Content package uses wrong evidence | Present contradiction | Canonical registry identifies WATER correctly | Regenerate and validate package before release |

## Pilot controls and decision rules

| Client fact | Action | Target | Owner | Decision rule |
| --- | --- | --- | --- | --- |
| Published production signs equal zero | Qualify and approve the pilot set | Three to five signs with complete source, rights, sign, visual, and publication records | Content Operations and sign reviewer | Stop if any sign lacks evidence |
| Registry and package disagree | Rebuild from the canonical six-sign registry | Zero cross-sign evidence links | Engineering and Content Operations | Block an unreconciled package |
| Human decisions lack identity and time | Implement approval logging | One hundred percent of decisions attributable with rationale | Product Owner | Unattributed approval cannot publish |
| Gemini rights and fidelity are unresolved | Close rights, review, and transparency decisions | Written decision for each displayed file | Rights owner and sign reviewer | No external display while unknown |
| Family access is only a preview | Build and security-test group-first delivery | Zero cross-family or cross-nursery access in tests | Engineering and privacy owner | Stop on any wrong-recipient access |
| Child and family data are unnecessary for content generation | Enforce separated data paths | Zero personal child or family data sent to LLM or LangSmith | Engineering and privacy owner | Stop on first transfer |
| Review quality is unmeasured | Calibrate reviewers and measure disagreement | One hundred percent exceptions include rationale; threshold agreed before pilot | Content lead | Iterate if review cannot be consistent |
| Complaints and recall are absent | Exercise correction and withdrawal | Complete drill before launch | Product Owner | No pilot until every active version can be found and withdrawn |

Hard pilot boundaries:

- child video processed in core scope equals zero;
- child scoring equals zero;
- automated educational decisions equal zero;
- unreviewed content delivered equals zero;
- blocked content delivered equals zero;
- personal child or family data sent to LLM or LangSmith equals zero;
- pilot sign provenance, including rights and review, equals 100 percent; and
- review exceptions with rationale equals 100 percent.

## Evidence index

- [Current MVP reality check](../mvp_reality_check.md)
- [Local MVP code](../../mvp/)
- [Current MVP tests](../../mvp/tests/)
- [Canonical sign asset registry](../../assets/registry/sign_asset_registry.json)
- [Generated asset inventory](../../assets/registry/sign_asset_inventory.md)
- [Source and asset provenance](../../assets/registry/source_assets_provenance.md)
- [Open Peeps provenance](../../assets/flashcards/open_peeps/provenance.json)
- [Visual sign packages](../../prototype/data/visual_sign_packages.json)
- [Content operations reports](../../content_ops/reports/)
- [LangSmith dry-run](../../workflow/langsmith_dry_run_summary.json)
- [n8n workflow documentation](../../workflow/kinder_signs_n8n_workflow.md)
- [GDPR record](../../compliance/gdpr_documentation.md)
- [EU AI Act assessment](../../compliance/eu_ai_act_compliance.md)
