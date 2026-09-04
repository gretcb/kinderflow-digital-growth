# KinderFlow EU AI Act Preliminary Intended-Purpose Assessment

**Assessment date:** 4 September 2026
**Frozen repository baseline:** 8eb0742, Freeze connected KinderFlow capstone demo
**Assessment type:** Preliminary intended-purpose assessment
**Decision use:** Controlled pilot planning

This document is a product and governance assessment. It is not legal advice, a regulatory determination, or a compliance certificate. KinderFlow must repeat the assessment when the intended purpose, users, data, model providers, deployment design, or applicable law changes.

## Executive conclusion

Kinder Signs uses Computer Vision to turn an adult reference video into technical movement evidence for human review. It can also prepare bounded family wording through an optional model path, although the repository proves only deterministic and dry-run evaluation evidence, not a live external model run. The product prototype includes six sign records, draft sign visuals, nursery assignment interactions, and a basic family-facing guidance preview.

The current intended purpose does not:

- admit a child to education;
- determine access to education;
- assign an educational level;
- evaluate a child's learning outcome;
- assess, score, rank, or profile a child;
- monitor prohibited behaviour during a test;
- recognise emotion;
- identify or categorise a person biometrically; or
- make an automated educational decision.

On that intended-purpose evidence, Kinder Signs does not appear to perform an education or biometric function listed as high risk in Annex III. This conclusion depends on function, not on the product being used near children or in a nursery setting. It is preliminary and must not be shortened to a generic risk label.

The product is not ready for an external pilot on regulatory documentation alone. Rights, sign review, role allocation, transparency, data protection, security, audit logging, and the current registry-to-content-package mismatch remain pilot gates.

## Scope and evidence

The assessment covers the repository state at 8eb0742.

| Component | Current evidence | Evidence state |
| --- | --- | --- |
| Adult reference intake | Registered demo, local MP4 upload, or bounded public direct MP4 URL | Implemented local control |
| Computer Vision | MediaPipe pose and hand landmarks, OpenCV processing, normalization, diagnostics, and reviewer-facing previews | Functional technical evidence |
| Six-sign registry | MORE, HELP, EAT, SLEEP, MILK, and WATER | Evidence present |
| Static sign visuals | Three Open Peeps-derived SVG candidates for each of six signs | Draft evidence; human review pending |
| Optional family-copy model path | Structured prompt, schema checks, deterministic quality gate, n8n design, and LangSmith dry-run | Partial evidence; no live run claimed |
| Gemini FX motion previews | MORE maps to mas.mp4, HELP to ayuda.mp4, and MILK to leche.mp4 | Separate demo files; rights and fidelity gates open |
| Nursery assignment | Little Steps Nursery fixture with synthetic records and session-based state | Local prototype |
| Family View | Basic family-facing guidance preview | Local prototype; personalised library pending |

Primary repository evidence:

- [Local MVP service](../mvp/app.py)
- [Computer Vision pipeline](../mvp/pipeline.py)
- [Current MVP tests](../mvp/tests/test_prompt_3.py)
- [Canonical sign asset registry](../assets/registry/sign_asset_registry.json)
- [Generated asset inventory](../assets/registry/sign_asset_inventory.md)
- [Open Peeps provenance record](../assets/flashcards/open_peeps/provenance.json)
- [Visual sign packages](../prototype/data/visual_sign_packages.json)
- [Content operations manifests](../content_ops/signs/)
- [n8n workflow export](../workflow/kinder_signs_n8n_workflow.json)
- [LangSmith dry-run record](../workflow/langsmith_dry_run_summary.json)

## Intended purpose

### Current intended purpose

KinderFlow prepares and governs reusable early-childhood content. Kinder Signs is its first active AI-enabled product.

The current workflow is:

1. An operator supplies an adult reference video.
2. The local service extracts pose and hand landmarks.
3. The service creates technical metrics and previews.
4. A human reviews the reference and selects or reviews a pose.
5. A human reviews a draft static visual and family material.
6. The Little Steps Nursery prototype simulates assignment.
7. Family View displays a basic local guidance preview.

Computer Vision supports content review. It does not recognise a sign, certify linguistic correctness, evaluate a child, or approve publication.

### Current product boundary

A family-facing guidance prototype exists. A personalised assignment-driven family library remains a next product iteration.

The current prototype has no production nursery accounts, family accounts, notifications, persistent cross-session assignment service, or real delivery to caregivers. It uses fictional Little Steps Nursery records and synthetic child labels.

### Out-of-scope uses

The intended purpose excludes:

- processing child video in the core workflow;
- developmental, clinical, behavioural, or educational assessment;
- emotion inference;
- identity matching;
- biometric categorisation;
- automated admission, placement, progression, grading, or discipline;
- automated decisions about access to services;
- autonomous content publication; and
- professional sign-language certification.

These exclusions must appear in product requirements, operator training, contracts, and change control. A user interface disclaimer alone is not enough.

## System component classification

| Component | AI relevance | Current role | Boundary |
| --- | --- | --- | --- |
| MediaPipe landmark extraction | AI system component | Converts adult video frames into pose and hand landmarks | No identity, emotion, child assessment, or sign certification |
| OpenCV and ffmpeg | Supporting software | Frame processing and browser-compatible preview preparation | Not treated as AI by themselves |
| Normalization and thresholds | Deterministic logic | Produces body-relative technical evidence and routes review states | Technical coverage is not sign correctness |
| Optional language-model path | AI system component when used live | Drafts bounded family wording from approved sign and routine data | No live external run or personal-data transfer is evidenced |
| LangSmith path | Monitoring design | Describes evaluation of the optional wording step | Dry-run only; does not validate Computer Vision or sign fidelity |
| n8n workflow | Orchestration design | Defines steps, branching, quality gates, and review preparation | Importable export; final target-runtime execution is not evidenced |
| Open Peeps-derived SVGs | Deterministic visual composition | Supplies a consistent character and line grammar | Open Peeps does not determine sign mechanics |
| Gemini FX files | Pre-generated synthetic media | Illustrative motion direction for three signs | Separate from current landmarks; rights and professional review pending |
| Nursery and Family Views | Product interface | Simulates selection and basic family guidance | No production delivery or personalised family library |

## Actors and role allocation

Role allocation depends on who develops, places, operates, and controls each system.

| Actor | Working role | Question to settle before pilot |
| --- | --- | --- |
| KinderFlow | Likely provider of the Kinder Signs system if it places the system under its name | Confirm legal entity, intended purpose, instructions, monitoring, and post-market duties |
| KinderFlow content team | Operator of internal Computer Vision and content workflow | Define competence, approval authority, escalation, and logging |
| Nursery school | Potential deployer if it operates an AI-enabled feature; content recipient if it only uses reviewed static material | Fix the actual pilot architecture and contract |
| Educator or administrator | Authorised human user | Define training, allowed actions, and override or escalation route |
| Families and children | Affected persons or recipients of reviewed content, depending on the final flow | Provide clear notices and a correction route |
| Upstream model or tool provider | Third-party provider or processor depending on service and data flow | Record terms, instructions, location, transparency marks, and change notices |

KinderFlow is not shown to provide a general-purpose AI model. An upstream model provider's obligations do not replace KinderFlow's duties for the product it designs and operates.

## Prohibited-practices check

The review found no intended use for the following practices.

| Practice | Current finding | Control |
| --- | --- | --- |
| Harmful manipulation or exploitation | Not part of the intended purpose | Bounded family copy, review, and complaints route |
| Social scoring | No scoring or ranking | Prohibit child and family scores |
| Predictive criminal-risk assessment | Not relevant to the product | Keep outside product scope |
| Untargeted facial-image scraping | No facial-image database or scraper | Direct URL accepts a bounded MP4, not a generic webpage |
| Emotion recognition in education | No emotion model or emotion field | Prohibited-use rule and test coverage |
| Biometric categorisation | No sensitive-attribute categorisation | Do not add such fields or models |
| Real-time remote biometric identification | No identity matching | Do not create identity templates |

The direct MP4 URL does not change this result. It downloads one operator-supplied public video into an isolated local run. It is not a face-scraping or internet-crawling function. The operator must still have authority to use the video.

## Annex III reasoning

### Step 1: Identify the relevant area

Nursery use makes the education area relevant for review. It does not decide classification by itself.

### Step 2: Compare actual functions with the listed education functions

| Annex III education concern | Kinder Signs current function |
| --- | --- |
| Admission or access | No |
| Assignment to an educational institution | No |
| Evaluation of learning outcomes | No |
| Determining educational level | No |
| Test monitoring or detection of prohibited behaviour | No |

Kinder Signs prepares reviewed communication material. The nursery prototype lets an educator select an available sign, group, material set, and audience. It does not use AI to decide who receives education or to evaluate a child.

### Step 3: Check biometric and emotion functions

MediaPipe produces body and hand landmarks from an adult reference. The service does not use them to establish or verify identity. It does not create a biometric identity template, compare a person against a database, categorise sensitive traits, or infer emotion.

Landmarks may still be personal data when linked to an identifiable adult. That GDPR issue does not make the current processing biometric identification under the AI Act.

### Step 4: Record the preliminary result

The current intended use does not appear to fall within the reviewed Annex III functions. A regulator, court, or qualified adviser may reach a different conclusion based on the final deployment facts. The product team must reopen this assessment before any material change.

## Transparency and AI-generated content

### Computer Vision disclosure

Operator documentation should say that MediaPipe extracts landmarks and that the output measures capture and movement representation. It should also say that a reviewer, not the metric, decides whether content can progress.

### Optional model-generated wording

The current Family View is not an autonomous chatbot. The repository shows a bounded drafting path and a dry-run quality evaluation, not a live conversation or live external trace.

If a live language model is introduced, KinderFlow must:

- disclose AI assistance where Article 50 or consumer expectations require it;
- identify the reviewed source and version;
- block unsupported developmental or clinical claims;
- keep personal child, family, and nursery data out of prompts and traces;
- retain reviewer identity, decision, rationale, and timestamp; and
- prevent unreviewed text from reaching a family.

### Gemini FX previews

The registry records:

| Sign | File | Status |
| --- | --- | --- |
| MORE | mas.mp4 | Pre-generated demo only |
| HELP | ayuda.mp4 | Pre-generated demo only |
| MILK | leche.mp4 | Pre-generated demo only |
| EAT | No file | Static flow remains available |
| SLEEP | No file | Static flow remains available |
| WATER | No file | Static flow remains available |

These videos were prepared separately as illustrative motion previews. They are not generated automatically from the current MediaPipe run or its landmarks.

The files are not certified sign videos. The registry records Google Labs FX or Gemini FX usage confirmation as pending, with external display and redistribution permission unresolved. The current code accepts a null display-rights value as locally available, so the permission boundary is not fully fail-closed.

Before any external display, KinderFlow must:

1. confirm display and redistribution rights;
2. obtain qualified motion and sign-fidelity review;
3. preserve any machine-readable provider mark;
4. decide whether visible synthetic-content disclosure is required; and
5. record the decision and evidence.

Article 50 applies by component and actor. The Commission states that Article 50 generally applies from 2 August 2026. A limited transition to 2 December 2026 applies only to the Article 50(2) marking and detection duty for providers of relevant systems placed on the market before 2 August 2026. KinderFlow must determine whether that narrow transition applies and verify the current rule before external use.

### AI literacy

Staff who operate or review AI components need role-specific literacy. Training should cover:

- what coverage metrics do and do not prove;
- missing-frame and partial-motion states;
- sign and visual review limits;
- source and usage rights;
- synthetic-content disclosure;
- prohibited child assessment and biometric uses;
- privacy and security escalation; and
- incident and correction handling.

The Commission's current Article 4 guidance describes an obligation to support AI literacy without guaranteeing a specific individual level. KinderFlow should keep training material and attendance evidence.

## Human oversight and publication control

No AI output should publish autonomously.

| Decision | Required human authority | Evidence to retain |
| --- | --- | --- |
| Reference is suitable and lawfully usable | Content lead and rights owner | Source, rights record, reviewer, date |
| Technical run is reviewable | Trained operator | Run ID, metrics, warnings, exception |
| Sign mechanics are correct | Qualified sign reviewer | Decision, notes, version |
| Visual is readable and accurate | Sign reviewer and visual reviewer | Candidate ID, decision, rationale |
| Family wording is bounded and accurate | Content reviewer | Source version, draft, final text |
| Asset may be published | Publication owner | Rights, review approvals, release version |
| Correction or withdrawal | Product owner | Incident, affected versions, action |

The current interface demonstrates review actions, but it does not provide a production identity, timestamped approval ledger, immutable audit trail, or correction workflow. Those controls remain operational gaps.

## Technical and security controls

### Direct MP4 intake

The current direct URL path:

- accepts only a complete public HTTP or HTTPS URL;
- rejects credentials, fragments, local names, private addresses, unsafe ports, and non-global resolved addresses;
- pins the connection to validated public IP addresses;
- revalidates redirects and rejects an HTTPS-to-HTTP downgrade;
- limits redirects, total time, response type, and bytes;
- stores the file under a generated local run name;
- removes partial files on failure; and
- redacts the query string from persisted provenance.

Evidence appears in [the pipeline](../mvp/pipeline.py) and [direct URL tests](../mvp/tests/test_prompt_3.py).

This is a local bounded intake control. It does not prove source rights, performer consent, sign correctness, malware safety, or production network security. HTTP remains permitted. A production design still needs authentication, authorisation, tenant separation, rate limits, controlled egress, decoder isolation, retention, monitoring, and incident handling.

### Registries, provenance, and hashes

The registry records exact asset identity and detects silent file changes. A hash does not prove ownership, consent, lawful use, linguistic correctness, or complete security.

Open Peeps by Pablo Stanley supplies the base character and visual line grammar. The provenance record states CC0 and links to the official source. Functional sign references, curated sign knowledge, frames, and movement evidence determine sign mechanics. Human review remains required for fingers, palms, contact, direction, and readability.

The character defines the look. The reviewed reference defines the sign.

### Registry and content-package drift

The canonical registry contains six signs and 18 current draft visual candidates. The older content-operations manifests and golden-set report cover a five-sign package and still assign WATER technical evidence to a MORE record. Their passing result covers schema and hash checks only.

Before pilot, KinderFlow must reconcile sign IDs and evidence ownership, bind current rights and visual records into the content package, regenerate the package, and obtain explicit expert and publication approvals.

## Logging and documentation

### Current evidence

Current local runs record technical inputs, run identifiers, metrics, artifacts, and redacted provenance. Registry files preserve asset paths, classifications, hashes, sign mappings, and limitations. Git preserves versioned evidence.

### Production gaps

The repository does not evidence:

- authenticated reviewer identities;
- a tamper-evident approval log;
- production model and prompt version logging;
- production access logs;
- change approval;
- incident and withdrawal records;
- deployed monitoring;
- a live LangSmith trace; or
- a final n8n runtime execution.

These are not optional proof points if KinderFlow relies on them in pilot governance.

## Conformity assessment summary

| Question | Preliminary finding | Evidence state |
| --- | --- | --- |
| Is AI used? | Yes. MediaPipe is active; an optional language-model path exists; Gemini files are separate synthetic demo media. | Evidence present |
| Is a prohibited practice intended? | No prohibited practice was identified in the current intended purpose. | Intended-purpose evidence present |
| Does the current use appear to match Annex III education functions? | No. It does not admit, assess, score, place, proctor, or determine access or level. | Preliminary conclusion |
| Does it perform biometric identity, categorisation, or emotion recognition? | No. Adult landmarks support motion review only. | Evidence present in current code |
| Is a formal high-risk conformity procedure triggered by this assessment? | Not on the current intended-purpose finding. | Legal confirmation required before market placement |
| Are Article 50 questions closed? | No. Gemini output and any future live model use need actor-specific assessment and records. | Pilot control required |
| Are human controls complete? | No. The local workflow demonstrates gates, but production identity, audit, correction, and withdrawal controls are missing. | Operational gap |
| Are content and rights records complete? | No. Open Peeps provenance is recorded, but sign-source rights, Gemini rights, expert review, and package reconciliation remain open. | Pilot gate |

This summary is not an EU declaration of conformity or CE-marking decision.

## Technical documentation outline

KinderFlow should maintain one controlled technical file with:

1. legal entity, system name, version, owner, and release status;
2. intended purpose, excluded uses, affected persons, and operating context;
3. component inventory, including MediaPipe, optional model, Gemini files, deterministic logic, and interfaces;
4. data and asset flow, including direct URL intake and deletion;
5. model, library, provider, prompt, schema, and dependency versions;
6. six-sign registry, source rights, hashes, provenance, and sign mappings;
7. Open Peeps source and style-only role;
8. Computer Vision metrics, thresholds, missing-data handling, and known limits;
9. sign, visual, language, and publication review procedures;
10. Article 50 assessment and marking or disclosure decisions;
11. role allocation and user instructions;
12. privacy, security, retention, recipient, and transfer controls;
13. logging, monitoring, incidents, corrections, and withdrawal;
14. tests, validation evidence, known failures, and residual risks;
15. change history and reassessment record; and
16. pilot acceptance and stop criteria.

## Reassessment triggers

Reopen the assessment before any of these changes:

- child video, voice, image, or landmarks enter the workflow;
- the system estimates age, emotion, development, behaviour, ability, or learning;
- a score, ranking, recommendation, or prediction affects a child;
- an AI output affects admission, access, placement, level, progress, discipline, or support;
- identity matching or biometric categorisation is added;
- test or behaviour monitoring is added;
- family delivery becomes personalised and persistent;
- a live model or new model provider is introduced;
- the system generates or publishes video, images, or text automatically;
- a nursery operates an AI component directly;
- source, sign, rights, or review policy changes;
- deployment expands to a new country, user group, or material purpose; or
- a serious incident, complaint, or material model change occurs.

## Pilot gates

| Client fact | Action | Target | Owner | Decision rule |
| --- | --- | --- | --- | --- |
| Intended purpose is narrow but only documented in the repository | Approve a versioned intended-purpose and prohibited-use statement | Signed before pilot configuration | Product Owner and legal reviewer | Do not pilot if scope permits child assessment, emotion, biometric identity, or automated education decisions |
| Roles depend on the final service design | Allocate provider, deployer, controller, processor, and reviewer roles | Contracts and responsibility matrix complete | Product Owner and privacy lead | Do not process real data until roles and instructions agree |
| Six-sign registry and older package disagree | Rebuild package from the canonical registry and verify ownership of evidence | Six of six sign records reconcile | Content Operations | Block every unreconciled sign |
| No sign is published | Complete rights, sign, visual, and publication reviews | Every pilot sign has all approvals and a rationale | Content lead and qualified sign reviewer | Unreviewed content delivered equals zero |
| Gemini rights and fidelity remain open | Confirm rights and complete Article 50 and sign review | Written evidence for every displayed file | Product Owner and rights owner | No external display without evidence |
| Production oversight logs do not exist | Implement authenticated, timestamped decisions and correction or withdrawal records | Every decision attributable and reversible | Engineering and Content Operations | Stop if an unreviewed or blocked asset can reach a user |
| Direct URL is a local control | Complete production security design and testing | Approved threat model and test record | Security owner | No public intake until authentication, egress, isolation, logging, and retention gates close |
| AI literacy is not yet evidenced | Train each role on limits and escalation | Attendance and materials recorded before access | Product Owner | No operator access without training |

## Official legal references

- [Regulation (EU) 2024/1689, consolidated text](https://eur-lex.europa.eu/eli/reg/2024/1689)
- [European Commission AI Act implementation overview](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
- [European Commission enforcement framework](https://digital-strategy.ec.europa.eu/en/policies/enforcement-ai-act)
- [European Commission Article 50 transparency FAQ](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act)
- [European Commission AI literacy questions and answers](https://digital-strategy.ec.europa.eu/en/faqs/ai-literacy-questions-answers)

Legal timing and guidance can change. Check the current consolidated law and regulator guidance at each release decision.
