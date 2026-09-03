# KinderFlow — Green AI & Sustainable Technology Audit

**Project:** KinderFlow — Early Childhood Digital Growth  
**Use case assessed:** Kinder Signs  
**Assessment date:** 2 September 2026  
**Repository baseline:** `661c027 — Build Round 2 KinderFlow MVP and UX`  
**Assessment approach:** Defend Your Stack / Carbon Story, aligned with Green Software Foundation principles and the Software Carbon Intensity (SCI) methodology

> This audit evaluates architecture and measurement readiness. KinderFlow does not yet have enough production energy, cloud-region or hardware-utilisation data to claim a measured carbon footprint or a quantified emissions reduction.

---

# 1. Executive takeaway

## Executive question

**Is KinderFlow using AI only where it creates meaningful product value, and is the architecture designed to avoid unnecessary computational cost before scale?**

## Current conclusion

**PROCEED — MEASUREMENT REQUIRED BEFORE ENVIRONMENTAL CLAIMS**

KinderFlow has a useful technology-selection principle:

> **Not every problem needs Generative AI.**

The current architecture uses different technologies for different jobs:

- **Computer Vision / MediaPipe** where movement representation is necessary;
- **deterministic templates** for Flashcards and Routine Cards;
- **deterministic quality gates** for predictable validation rules;
- **optional LLM assistance** only where natural-language transformation may add value;
- **human review** for approval rather than repeated model calls;
- **reusable central content** rather than generating new content separately for every school or family.

The architecture supports bounded computation and central reuse, but the environmental effect is not yet evidenced.

However, KinderFlow has **not measured actual energy consumption or carbon emissions** for the current MVP.

Therefore the project should not claim:

- “low-carbon AI”;
- a specific CO2 reduction;
- that deterministic processing is a measured percentage more efficient;
- that the current local runtime is environmentally optimal.

The correct current claim is:

> **KinderFlow is designed to minimise unnecessary AI computation, and the pilot should establish an energy/carbon baseline before environmental performance is quantified.**

---

# 2. Methodology

This audit follows the same logic used in the bootcamp's sustainable-stack exercises:

```text
Understand the stack
→ identify computational hotspots
→ challenge whether AI is necessary
→ reduce unnecessary work
→ reuse outputs
→ measure
→ optimise
→ only then make environmental claims
```

It is also aligned with the Green Software Foundation's emphasis on reducing impact at source.

The Foundation describes three broad ways to reduce software emissions:

1. use fewer physical resources;
2. use less energy;
3. use energy more intelligently.

---

# 3. Software Carbon Intensity framework

The Green Software Foundation's Software Carbon Intensity methodology expresses software emissions as a rate per functional unit.

```text
SCI = (E × I + M) / R
```

Where:

- **E** = energy consumed by the software system;
- **I** = carbon intensity of the electricity;
- **M** = embodied emissions allocated to the hardware used;
- **R** = functional unit.

The purpose is not simply to calculate a total.

It is to measure:

> **the carbon intensity of delivering one useful unit of software functionality.**

KinderFlow does not currently have the data required to calculate a defensible SCI score.

This audit therefore defines what should be measured during the pilot.

---

# 4. KinderFlow technology stack — sustainability view

| Capability | Current technology | AI? | Current evidence | Sustainability implication |
|---|---|---:|---|---|
| Reference movement processing | MediaPipe / Computer Vision | Yes | Working local MVP | Compute-intensive relative to ordinary UI; should run only when a sign asset is created/reprocessed |
| Landmark normalization / diagnostics | Python deterministic processing | No / algorithmic | Working | Reuse existing run outputs rather than recompute unnecessarily |
| Video overlay preparation | OpenCV + ffmpeg | No | Working local MVP | Additional CPU work; should be generated once per required review artifact |
| Family/content wording | Human or LLM-assisted | Optional AI | DRY_RUN evidenced; provider-path tests exist; LIVE external execution not evidenced | Model call should be optional and bounded |
| Quality gates | Deterministic Python/rules | No | Working | Appropriate for repeatable checks; no reason to replace with LLM judgment |
| Flashcard Studio | HTML/CSS/JS deterministic template | No | Working internal builder | Reusable rendering avoids per-card generative image calls |
| PDF output | Browser print | No | Browser Print / Save as PDF path implemented; final saved-PDF visual QA pending | Uses existing rendered card; no separate server render pipeline |
| School assignment | Standard application logic | No | Prototype | No AI required |
| Family display | Standard application logic | No | Prototype | No AI required |
| LangSmith | Observability for LLM step | Supporting service | DRY_RUN evidenced; LIVE external trace/evaluation not evidenced | Only relevant when LLM assistance is used |
| Avatar/video generation | Future | Potentially high-compute AI | Not implemented | Must be justified and measured before adoption |
| Story generation | GenAI concept/prototype | Yes | Illustrative | Should be generated/reviewed centrally and reused, not generated per family |
| Song generation | Future | Potential AI | Concept only | No current environmental claim |

---

# 5. The strongest Green AI decision already made

## Do not use GenAI for deterministic tasks

Flashcard Studio is intentionally template-based.

The system already knows:

- sign;
- word;
- language;
- card type;
- approved routine/context.

A generative model is not required to decide the layout each time.

The controlled flow is:

```text
Reviewed sign
→ deterministic template
→ live preview
→ local approval
→ print / PDF
```

This is better architecture for several reasons:

- predictable output;
- easier testing;
- lower vendor dependency;
- no hallucination risk in layout;
- easier accessibility control;
- easier reuse;
- less unnecessary AI computation.

### Environmental claim boundary

It is reasonable to say this **avoids unnecessary model calls**.

It is **not yet reasonable** to claim a quantified carbon saving without measurement.

---

# 6. Computer Vision — justified AI use

KinderFlow uses Computer Vision where the information being processed is genuinely visual and temporal.

The question is:

> Can validated reference movement be represented in structured form?

MediaPipe therefore has a clear role:

```text
reference video
→ pose / hand landmarks
→ movement representation
→ human review
```

This cannot be replaced by a simple text template without losing the core movement information.

## Sustainability principle

Use Computer Vision:

- during central sign production;
- when a new/changed reference requires processing;
- when evidence must be regenerated.

Do **not** run Computer Vision:

- every time a family views a sign;
- every time a school assigns a sign;
- for every Flashcard render;
- continuously in the background;
- on child video in the current product.

This creates a potentially important scaling property:

> **AI processing occurs during asset production; approved assets can then be reused many times.**

The environmental benefit of this reuse should be measured during pilot rather than assumed.

---

# 7. LLM use — bounded by design

The Content Engine supports:

- HUMAN;
- LLM_ASSISTED.

It also distinguishes:

- LIVE;
- DRY_RUN;
- NOT_APPLICABLE.

This is useful environmentally as well as operationally.

## Current principle

Do not call an LLM simply because the product contains an AI capability.

A model call is justified only when it adds useful language-generation capability.

---

## Current examples

### Appropriate deterministic work

- ID validation;
- required-field validation;
- restricted-claim detection;
- schema checking;
- Flashcard layout;
- publication-state rules.

### Potentially appropriate LLM work

- transforming approved structured context into concise family-facing wording;
- future original stories.

---

## Recommended pilot rule

Before adding an LLM call, ask:

1. Can a stored human version solve the task?
2. Can a deterministic template solve the task?
3. Does generation materially improve user value?
4. Will the output be reused?
5. Is the selected model appropriately sized for the task?
6. Can the result be cached/versioned after human review?

If the first or second answer is yes, GenAI may not be necessary.

---

# 8. Central generation and reuse

One of KinderFlow's most important scale assumptions is central content reuse.

Potential flow:

```text
Create/review MORE once
→ approved sign asset
→ approved family copy
→ Flashcard
→ Routine Card
→ future Story
→ multiple schools
→ multiple groups
→ multiple families
```

The alternative would be:

```text
new AI generation for every user/request
```

KinderFlow should avoid the second model unless personalisation is proven to create enough value to justify the additional complexity and compute.

## Pilot metric

Track:

```text
Number of family/school uses
÷
Number of AI production runs
```

A higher reuse ratio is directionally desirable.

---

# 9. Current computational hotspots

## 9.1 MediaPipe processing

Likely current hotspot in the local MVP because it performs frame-by-frame processing.

Actual energy consumption:

**NOT MEASURED**

---

## 9.2 Video transcoding

OpenCV creates the movement overlay and ffmpeg converts it to a browser-compatible H.264 representation.

This is necessary for the current review experience.

Actual energy consumption:

**NOT MEASURED**

---

## 9.3 Live LLM inference

If enabled, external model inference will add computation outside KinderFlow's local runtime.

Actual energy/carbon data:

**NOT AVAILABLE IN THE CURRENT MVP EVIDENCE**

---

## 9.4 LangSmith observability

Tracing creates:

- network transfer;
- processing;
- stored trace data.

It should therefore be used for a clear governance/evaluation purpose rather than indiscriminate logging.

Actual incremental impact:

**NOT MEASURED**

---

## 9.5 Browser/UI

Static HTML/CSS/JS and deterministic card rendering are unlikely to dominate the AI workload, but no measured comparison has been performed.

---

# 10. Future high-compute risk: generative video/avatar production

Production-ready avatar/video generation is **not part of the current MVP**.

This matters environmentally.

Generative video can involve substantially more computation than:

- static templates;
- standard image assets;
- deterministic animation;
- lightweight rendering.

KinderFlow should not select generative video simply because it appears more advanced.

## Decision gate

Before adding a generative-video model, compare:

### Option A

Deterministic / rigged character animation using reviewed movement data.

### Option B

Generative-video production.

Evaluate:

- movement fidelity;
- visual quality;
- review burden;
- inference cost;
- latency;
- reproducibility;
- energy/carbon evidence;
- rights/governance;
- ability to reuse the final asset.

### Rule

> Choose the simplest technology that reliably preserves the validated movement and meets the product requirement.

---

# 11. Avoid / Shift / Improve strategy

## A. AVOID unnecessary computation

Current or recommended controls:

- do not process child video;
- do not run CV during family consumption;
- do not generate every Flashcard with AI;
- do not regenerate approved copy unless content changes;
- do not generate personalised content by default;
- do not call LangSmith when the workflow is NOT_APPLICABLE;
- do not rerun successful CV jobs only to reproduce already stored evidence;
- do not use generative video unless it solves a validated requirement.

---

## B. SHIFT computation intelligently

Once a hosting architecture is selected:

- review cloud region carbon data;
- schedule non-urgent batch content processing when appropriate;
- avoid keeping oversized compute continuously provisioned for infrequent content-production jobs;
- consider batch/queue architecture for non-real-time production workloads.

The current local MVP does not provide enough evidence to choose a production region or hosting model.

---

## C. IMPROVE efficiency

Potential actions:

- right-size input video resolution where fidelity allows;
- avoid duplicate video transcodes;
- reuse normalized landmarks and generated overlays;
- cache reviewed content assets;
- select an appropriately sized language model for bounded copy tasks;
- keep prompts/context concise and structured;
- prevent retries caused by malformed output through schemas;
- monitor failed/repeated AI calls;
- version outputs so unchanged content is reused.

Any technical optimisation that might reduce movement fidelity must be tested before adoption.

---

# 12. Reliability is also a sustainability issue

Failed computation creates no product value.

Examples:

```text
invalid video
→ processing attempt
→ failure
→ repeat
```

or:

```text
poorly constrained LLM prompt
→ bad output
→ retry
→ another bad output
```

KinderFlow already reduces this risk through:

- file validation;
- controlled capture guidance;
- schema checks;
- quality gates;
- explicit failure states;
- deterministic fallback/human content.

## Green AI implication

Improving first-pass success can reduce wasted computation.

The actual saving has not yet been measured.

---

# 13. Model-selection principle

KinderFlow should not default to the largest available model.

For each AI task:

```text
Task requirement
→ quality threshold
→ smallest model meeting the threshold
→ measured cost / latency / energy
→ human-review outcome
```

## Pilot comparison

For bounded family copy, compare candidate models using:

- content quality;
- deterministic-gate pass rate;
- reviewer-edit rate;
- latency;
- financial cost;
- available energy/carbon evidence.

A larger model is justified only if the additional quality creates enough value.

---

# 14. Environmental measurement boundary

KinderFlow should define a measurement boundary before calculating environmental impact.

## Include where practical

### Local / server computation

- MediaPipe;
- Python processing;
- OpenCV;
- ffmpeg;
- application backend.

### AI providers

- LLM inference where provider data allow attribution.

### Supporting services

- LangSmith;
- storage;
- networking;
- hosted database/authentication once deployed.

### Client layer

- browser rendering;
- content delivery where material.

### Hardware allocation

Include embodied emissions when enough deployment/hardware information exists to apply SCI credibly.

---

# 15. Recommended functional units

A single overall number is not enough to understand KinderFlow.

Measure separate workflows.

## Functional unit 1 — Create a Sign

```text
1 adult reference video processed
→ technical movement evidence produced
```

Potential metric:

**gCO2e / completed sign-processing run**

---

## Functional unit 2 — Content Pack

```text
1 reviewed content candidate generated
```

If LIVE external execution is enabled later, compare:

- HUMAN; and
- LLM_ASSISTED LIVE.

Potential metric:

**gCO2e / accepted content candidate**

Accepted is preferable to “per model call” because failed/rejected outputs create less business value.

---

## Functional unit 3 — Approved reusable sign asset

```text
production + review
→ reusable approved content package
```

Potential metric:

**gCO2e / approved reusable sign package**

---

## Functional unit 4 — School/family delivery

Potential later metric:

**gCO2e / 1,000 approved content views or deliveries**

---

## Functional unit 5 — School service

For production:

**gCO2e / active school / month**

This can help management compare architecture changes over time.

---

# 16. Pilot measurement plan

## Baseline first

Do not begin with a sustainability target that has no measured baseline.

During pilot, record:

| Workflow | Measure |
|---|---|
| MediaPipe run | duration, CPU/energy where available, success state |
| ffmpeg conversion | duration, energy where available |
| LLM call | provider/model, tokens, latency, result status |
| Content review | accepted/rejected/retry |
| LangSmith | traces created / retention |
| Asset reuse | schools/families served per approved asset |
| Infrastructure | region, instance/resource type, utilisation |
| Storage | raw/intermediate/final asset volume |

---

# 17. Proposed Green AI KPIs

| KPI | Why it matters |
|---|---|
| CV runs per approved sign | Reprocessing efficiency |
| Failed CV runs / total runs | Wasted computation |
| LLM calls per approved content asset | Generation efficiency |
| LLM retry rate | Wasted inference |
| Human-source vs LLM-assisted use | Shows whether AI is actually necessary |
| Reviewed assets reused across schools | Amortisation of production compute |
| Model tokens per accepted content asset | LLM efficiency |
| Median processing duration | Operational proxy |
| Storage per approved asset | Lifecycle efficiency |
| % Flashcards created without GenAI | Demonstrates deterministic-first architecture |
| gCO2e per functional unit | Environmental outcome once measurable |

---

# 18. Carbon Story — current state

## What KinderFlow can demonstrate now

### 1. Challenge the need for AI

KinderFlow does not treat GenAI as the default solution.

### 2. Use AI where modality requires it

Computer Vision addresses movement representation.

### 3. Use deterministic tools for predictable work

Flashcards and rule-based quality gates are deterministic.

### 4. Produce centrally and reuse

The architecture is designed around reusable approved content.

### 5. Keep AI out of high-frequency end-user interactions

The current school/family experience does not trigger CV/LLM inference on every interaction.

---

## What KinderFlow cannot demonstrate yet

- measured kWh;
- measured gCO2e;
- embodied-carbon allocation;
- production cloud-region intensity;
- model-provider inference emissions;
- quantified emissions avoided through templates/reuse;
- lifecycle water impact.

These should remain explicit measurement gaps.

---

# 19. Greenwashing / unsupported-claim audit

## Do not say

> KinderFlow is carbon neutral.

No evidence.

---

## Do not say

> KinderFlow's AI is sustainable.

Too broad and unmeasured.

---

## Do not say

> Deterministic Flashcards reduce emissions by X%.

No measurement.

---

## Do not say

> Our local CV processing is greener than cloud AI.

Not demonstrated.

---

## Safe statement

> KinderFlow uses a deterministic-first architecture and limits AI computation to tasks where it adds functional value. Environmental performance will be baselined during pilot before quantitative sustainability claims are made.

---

# 20. Sustainable-stack decision matrix

| Product need | Candidate approach | Decision | Reason |
|---|---|---|---|
| Capture movement | Text/manual description only | Reject as core method | Does not preserve structured visual movement evidence |
| Capture movement | Computer Vision | **Use** | Modality matches problem |
| Flashcard layout | Generative image/layout model | Avoid | No validated need |
| Flashcard layout | Deterministic template | **Use** | Predictable and reusable |
| Quality checks | LLM judge for every rule | Avoid where possible | Deterministic rules already cover known constraints |
| Quality checks | Deterministic checks + human review | **Use** | Controlled, testable |
| Family wording | Stored human text | **Use when sufficient** | No inference required |
| Family wording | Bounded LLM assistance | **Use selectively** | Adds language-generation value |
| School assignment | AI recommendation engine | Reject current scope | No need; increases risk/compute |
| School assignment | Educator selection | **Use** | Human-controlled and simple |
| Family viewing | Real-time AI generation | Reject current scope | Reusable approved material is sufficient |
| Final sign visual | Generative video | **TBD** | Must beat deterministic/rigged alternatives on fidelity, cost and sustainability |

---

# 21. Green AI risk matrix

| Risk | Likelihood | Impact | Current control | Remaining action |
|---|---:|---:|---|---|
| GenAI added to tasks that do not require it | 2 | 4 | Deterministic-first principle | Architecture review |
| Repeated CV processing wastes compute | 3 | 3 | Isolated stored runs | Cache/reuse policy |
| LLM retries caused by weak outputs | 2 | 3 | Schemas/quality gates | Measure retry rate |
| Largest model used by default | 3 | 3 | Configurable model | Benchmark right-sized options |
| Generative video adopted without business need | 3 | 5 | Outside MVP | Explicit build/buy/measure gate |
| Excess trace/storage retention | 2 | 3 | LangSmith optional | Retention policy |
| Sustainability claims made without measurements | 3 | 4 | Current docs are conservative | Claims review |
| Production infrastructure overprovisioned | 3 | 3 | Not yet deployed | Right-size pilot infrastructure |
| Cloud carbon intensity ignored | 3 | 2 | No region decision yet | Include sustainability in hosting decision |
| Fidelity sacrificed for efficiency | 2 | 5 | Human review | Quality threshold remains primary |

---

# 22. Green AI assessment matrix

| Area | Status | Evidence | Gap | Action |
|---|---|---|---|---|
| Challenge whether AI is necessary | **Architecture evidence present** | Deterministic-first architecture | Must preserve as scope grows | Architecture gate |
| AI/task fit | **Partial evidence** | CV used for movement | Broader sign evidence needed | Pilot validation |
| Reuse / caching | **Architecture supports reuse** | Central reusable-content model | No current sign is published; production cache policy not formal | Define version/reuse rules |
| Model right-sizing | **Measurement gap** | Model configurable | No comparative benchmark | Pilot test |
| Failed-work reduction | **Partial evidence** | Validation/error handling | No measured waste baseline | Measure |
| Energy measurement | **Measurement gap** | None | kWh not measured | Baseline pilot |
| Carbon measurement | **Measurement gap** | None | SCI inputs missing | Measure once infrastructure known |
| Embodied emissions | **Evidence not yet available** | No production hardware allocation | Deployment unknown | Add if SCI implemented |
| Carbon-aware hosting | **TBD** | No production region | Region/provider undecided | Include in deployment decision |
| Environmental claims governance | **Pilot control required** | No current quantitative claim | Formal claims review absent | Add sign-off |
| High-compute future features | **Pilot control required** | Gen video not implemented | Future pressure to add it | Require comparison gate |

---

# 23. Pilot Green AI gates

## Before pilot

1. Define the workloads to measure.
2. Record model/provider/version for all live AI calls.
3. Define cache/version/reuse rules.
4. Avoid personalisation that requires unnecessary per-user inference.
5. Define trace/log retention.
6. Select right-sized infrastructure.
7. Define one or more functional units.
8. Do not make quantitative sustainability claims without measurements.

---

## During pilot

Measure:

- CV run count;
- failed/repeated CV runs;
- LLM call count;
- LLM retry count;
- tokens;
- latency;
- accepted outputs;
- asset reuse;
- storage;
- infrastructure utilisation;
- energy/carbon where tools/provider data allow.

---

## After pilot

Decide:

### GO

If environmental intensity is measured, manageable and the architecture remains efficient.

### ITERATE

If excessive computation comes from:

- retries;
- repeated processing;
- overprovisioning;
- oversized models;
- unnecessary generation.

### STOP / REDESIGN FEATURE

If a high-compute feature provides insufficient user/business value relative to its cost, risk and environmental burden.

---

# 24. Relationship with ROI

Green AI and financial efficiency are partially aligned.

Examples:

- fewer unnecessary model calls → lower variable cost;
- asset reuse → lower repeated production cost;
- right-sized models → lower inference cost;
- fewer failed runs → less staff time and compute;
- deterministic templates → predictable operating cost.

However:

> **financial cost is not a reliable substitute for carbon measurement.**

A cheap service is not necessarily low-carbon.

The ROI model and Green AI audit should therefore use some shared operational metrics but keep financial and environmental conclusions separate.

---

# 25. Relationship with Responsible AI

The Green AI principle reinforces Responsible AI proportionality:

> Use AI only when the expected benefit justifies the additional complexity and resource use.

For KinderFlow this is particularly relevant because the product serves early childhood.

Technology should support the school-family routine, not add AI for novelty.

---

# 26. Slide-ready summary

| Question | Answer |
|---|---|
| Does every KinderFlow feature use GenAI? | **No** |
| Why use CV? | Movement is visual/temporal and needs structured representation |
| Why not GenAI for Flashcards? | Deterministic templates solve the task reliably |
| Is the family experience real-time AI? | **No** |
| Can content be reused after publication? | **The architecture supports reuse; no current sign has reached published library status** |
| Are actual carbon emissions measured? | **Not yet** |
| What is the pilot sustainability goal? | Establish a baseline and reduce unnecessary computation |
| Main future sustainability risk | High-compute generative video without validated need |
| Current Green AI decision | **PROCEED — MEASURE BEFORE CLAIMING** |

---

# 27. Bottom line

## Assessment

**PROCEED — MEASUREMENT REQUIRED BEFORE ENVIRONMENTAL CLAIMS**

KinderFlow has made a strong architectural choice by separating:

```text
AI that is functionally necessary
from
tasks that can be solved deterministically
```

The current design avoids several common sources of unnecessary AI computation:

- no child-video inference;
- no AI recommendation engine for school assignments;
- no generative Flashcard layout;
- no real-time LLM call whenever a family opens content;
- no automatic repeated generation after human approval;
- no production generative-video dependency.

The strongest sustainability opportunity is the same one that supports KinderFlow's business model:

> **Create reviewed content centrally, then reuse it.**

The next step is measurement.

KinderFlow should baseline energy/carbon per useful functional unit during the pilot and use that evidence to decide:

- whether workloads can be reduced;
- whether models can be right-sized;
- whether processing can be reused;
- whether future high-compute features create enough value.

Until then, the project's environmental strength should be presented as **sustainable architecture and measurement readiness**, not as a quantified carbon-performance claim.

---

# 28. Official sources

1. Green Software Foundation — Software Carbon Intensity (SCI)  
   https://greensoftware.foundation/standards/sci/

2. Green Software Foundation — Software standards  
   https://greensoftware.foundation/standards/

3. Green Software Foundation — What is Green Software?  
   https://greensoftware.foundation/articles/what-is-green-software/

4. Green Software Foundation — Software Energy Intensity (SEI)  
   https://greensoftware.foundation/standards/sei/

5. Green Software Foundation — SCI for AI Specification  
   https://greensoftware.foundation/articles/sci-ai-specification-ratified-standard-for-measuring-ai-emissions-across-the/

6. Green Software Foundation — Real Time Cloud standard  
   https://greensoftware.foundation/standards/rtc/

---

# 29. Repository evidence used

Assessment aligned to:

`661c027 — Build Round 2 KinderFlow MVP and UX`

Relevant evidence includes:

- `mvp/mvp_documentation.md`
- `mvp/app.py`
- `content_ops/`
- `workflow/kinder_signs_n8n_workflow.md`
- `prototype/README.md`
- `prototype/create-sign.*`
- `prototype/flashcards.*`

Key repository facts reflected in this audit:

- MediaPipe processing is local in the current MVP;
- CV runs produce reusable stored run artifacts;
- ffmpeg is used to create the browser-facing overlay;
- the Content Engine supports human and optional LLM-assisted modes;
- DRY_RUN is evidenced and LIVE external execution is not yet evidenced;
- quality gates are deterministic;
- Flashcards are template-based;
- browser Print / Save as PDF is implemented without a generative/export service; final saved-PDF visual QA remains pending;
- school/family use does not require live CV processing;
- production-ready avatar/generative video is not implemented;
- production infrastructure and environmental telemetry are not yet defined.
