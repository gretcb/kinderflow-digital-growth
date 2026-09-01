# KinderFlow: Early Childhood Digital Growth

KinderFlow explores how an early-years centre in Madrid can turn its trusted relationship with families into a digital service.

The first opportunity is **Kinder Signs**: a school-led **Signs and Flashcards Library** that helps families repeat at home the same sign used in class that week.

## Round 1 recommendation

**Proceed with a focused 8 to 9 week commercial validation phase before scaling.**

The project has enough evidence to justify the next validation phase. The next step is to test demand, educator adoption, family engagement, willingness to pay and technical reliability with a small set of signs.

## The product idea

Kinder Signs is not another Baby Sign dictionary.

The core flow is simple:

```text
Kinder Signs creates the Signs and Flashcards Library
→ the educator selects this week's sign
→ the sign is assigned to a group or child
→ families receive matching guidance at home
```

The educator does not create content, upload videos or manage AI. The school uses a ready-to-use library and keeps the classroom workflow simple.

The school-facing action is:

```text
Select group or child
→ choose this week's sign
→ send to families
```

The internal Kinder Signs content-production workflow is separate:

```text
Approved sign video
→ movement check
→ movement data and skeleton
→ visual layer
→ avatar build / preview
→ human review
→ published in the Signs and Flashcards Library
```

Core principle:

```text
The character defines the look.
The validated reference movement defines the sign.
```

Computer Vision is used to preserve and represent movement from validated reference material. It is not used to automatically certify sign-language correctness.

## Why Kinder Signs

Three use cases were compared.

| Use case         | Role                                          |
| ---------------- | --------------------------------------------- |
| **Kinder Signs** | Early communication across school and home    |
| **Kinder Daily** | School-family communication and daily context |
| **Kinder Food**  | Food routines and family guidance             |

Kinder Signs was selected as the first commercial validation wedge because it brings together:

| Reason                 | Why it matters                                                     |
| ---------------------- | ------------------------------------------------------------------ |
| School-home continuity | The same routine can continue from classroom to home               |
| Simple educator action | The educator only selects the sign used that week                  |
| Differentiation        | The value is not more content, but trusted continuity              |
| Reusable library       | One Signs and Flashcards Library can serve more schools and groups |
| Technical feasibility  | Computer Vision can test the movement-capture layer                |
| School-led model       | The school is the main customer and distribution channel           |

## What was built for Round 1

### 1. Research and use-case framing

The research covers the early-childhood education context in Spain, Madrid as a first entry market, opportunity and risk analysis, competitor evidence, and the comparison of Kinder Signs, Kinder Daily and Kinder Food.

Relevant folder:

```text
research/
```

### 2. Tableau dashboard

The dashboard supports a commercial validation decision. It is designed to answer:

**Is the market reachable enough to justify an 8 to 9 week validation phase?**

The dashboard uses public datasets and 7 stakeholder metrics.

| Metric                             | Why it matters                            |
| ---------------------------------- | ----------------------------------------- |
| Children in first-cycle education  | Market access                             |
| Enrolment rate at age 2            | Early routine access                      |
| Enrolment rate at age 3            | Continuity into the next stage            |
| Early-childhood centres in Madrid  | Local entry market                        |
| Private and concerted centre share | Potential commercial channel              |
| Internet and digital readiness     | Family reachability                       |
| GenAI adoption context             | Digital readiness for AI-enabled services |

Sources include the Spanish Ministry of Education, Comunidad de Madrid and INE public datasets.

Relevant folders:

```text
data/
dashboard/
```

### 3. Static product prototype

The prototype shows how Kinder Signs could work as a product.

| View                   | Purpose                                      |
| ---------------------- | -------------------------------------------- |
| `prototype/index.html` | School-family experience                     |
| `prototype/admin.html` | Kinder Signs internal and school/admin logic |

The mock shows:

* the Signs and Flashcards Library;
* the school, group, teacher and child hierarchy;
* assignment to a whole group or an individual child;
* family access and active packs;
* prepared family outputs;
* the internal reference-video-to-published-library-item workflow.

The school does not create, upload or validate reference sign videos. Kinder Signs manages the validated library, while educators select the sign used that week.

Run locally:

```bash
cd prototype
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/index.html
http://localhost:8000/admin.html
```

Relevant folder:

```text
prototype/
```

### 4. Computer Vision POC

The Computer Vision POC tests whether a validated reference sign video can be converted into structured movement data.

| Metric                   |                  Result |
| ------------------------ | ----------------------: |
| Frames analysed          |                     332 |
| Pose detection           |                    100% |
| Dominant hand detection  |                  93.98% |
| Missing hand frames      |                      20 |
| Overall technical status | Proceed with conditions |

The POC supports the first technical step:

```text
validated reference video
→ landmarks
→ movement data
→ motion diagnostics
```

These metrics describe the technical processing quality of the reference video. They do not certify that the sign itself is linguistically correct.

The POC provides a technical basis for testing whether a future visual layer or avatar preview can follow validated reference movement without redefining the sign.

Relevant folder:

```text
poc/
```

### 5. Governed AI workflow

The workflow shows how Kinder Signs can use AI internally while keeping content controlled.

```text
approved sign content + CV motion summary
→ LLM-generated family draft
→ deterministic quality checks
→ LangSmith trace and evaluation
→ draft pending human review
```

LangSmith is used to observe and evaluate the LLM content-generation step.

It does **not** validate biomechanical or linguistic sign correctness.

The workflow keeps AI as support for content operations rather than as the authority on whether a sign is correct.

Relevant folder:

```text
workflow/
```

### 6. Cost and timeline

The proposed next phase is a focused validation investment.

| Item                  |        Estimate |
| --------------------- | --------------: |
| Timeline              |    8 to 9 weeks |
| Validation investment | €5.5k to €17.8k |

This is a validation budget, not a full launch budget.

The main cost drivers are:

* expert / human review;
* user research;
* a 3 to 5 sign content test;
* Computer Vision refinement;
* workflow testing;
* content production.

Relevant file:

```text
cost_timeline/estimate.md
```

## Business model hypothesis

Kinder Signs is designed as a **school-led B2B/B2B2C product**.

The school is the main customer. Families are users and beneficiaries.

| Layer               | Product logic                                                                   |
| ------------------- | ------------------------------------------------------------------------------- |
| **School account**  | The centre subscribes to Kinder Signs                                           |
| **Classroom group** | Signs and packs can be assigned by group                                        |
| **Teacher**         | The educator selects the sign used that week                                    |
| **Child profile**   | Outputs can be prepared for a group or a specific child                         |
| **Family access**   | Parents and caregivers receive the guidance                                     |
| **Premium packs**   | Flashcards, routines, mini stories or songs can be activated by school or group |
| **Prepared output** | Kinder Signs prepares the matching family material                              |

The product supports two assignment levels:

```text
Assign to selected group(s)
Assign to individual child
```

Premium content is positioned mainly as a school or classroom-group purchase rather than as the core direct-to-family business model.

## Product and privacy scope decision

The current Kinder Signs direction intentionally removes child video from the core workflow.

Child video is not required to solve the primary school-home continuity problem and would introduce additional privacy, security, operational and regulatory complexity.

The current Computer Vision use case therefore focuses on **validated reference sign content**, not on assessing a child's signing performance.

The current scope does not include:

* automated child-performance scoring;
* developmental assessment;
* emotion analysis;
* automated sign-language certification;
* autonomous publishing without human review.

Any future child-video capability would require a separate product, privacy, legal and technical assessment.

## Repository structure

```text
.
├── cost_timeline/       Validation budget and timeline
├── dashboard/           Tableau dashboard documentation and assets
├── data/                Tableau-ready datasets and source register
├── feedback/            Round 1 decision after feedback
├── poc/                 Computer Vision movement POC
├── presentation/        Round 1 presentation
├── prototype/           Static product prototype
├── research/            Market research, risks and use cases
└── workflow/            n8n and LangSmith workflow
```

## Round 1 status

| Requirement                               | Status    |
| ----------------------------------------- | --------- |
| Sector and company size                   | Covered   |
| Research and 2 to 3 use cases             | Covered   |
| Public dataset selected and justified     | Covered   |
| Dashboard with 5 to 7 stakeholder metrics | Covered   |
| Simple POC                                | Covered   |
| n8n or equivalent workflow                | Covered   |
| LangSmith sample                          | Covered   |
| Cost and timeline                         | Covered   |
| Presentation                              | Covered   |
| `round1_decision.md`                      | Completed |

## Round 1 decision

After the Round 1 presentation and teaching-staff feedback, the decision is:

**KEEP Kinder Signs as the first commercial validation wedge.**

Round 1 confirmed that the project has enough evidence to continue rather than change sector or use case.

The strongest next-step signal was to move from a well-developed static concept to a **small working MVP**, with particular focus on the Computer Vision capability.

The full decision and feedback summary are documented in:

```text
feedback/round1_decision.md
```

## Round 2 focus

Round 2 moves from **concept validation to functional validation**.

The core working MVP will focus on:

```text
validated reference sign video
→ video upload
→ MediaPipe processing
→ hand / pose landmarks
→ skeleton / movement preview
→ technical metrics
→ review-ready result
```

This is the technically differentiating capability that must work reliably.

A secondary functional feature will connect the published library item to practical family value:

```text
published sign
→ family sign card
→ family guidance
→ Tips & Tricks
→ printable flashcard
→ print / PDF-friendly output
```

Final production-ready avatar generation remains future exploration and is not part of the core Round 2 MVP.

The project will also deepen:

* POC and MVP documentation;
* ROI and break-even assumptions;
* technical, regulatory, ethical, operational and commercial risks;
* EU AI Act assessment;
* GDPR and data-flow documentation;
* pilot design;
* commercialisation and deployment planning.

Round 2 is not intended to prove full product-market fit or production readiness.

The goal is to gather enough technical, business, regulatory and user evidence to support a clear next decision:

**Proceed to pilot, iterate before pilot, or stop.**