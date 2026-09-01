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

The internal Kinder Signs workflow is separate:

```text
Kinder Signs library item
→ reference video registered
→ movement check
→ movement data and skeleton
→ visual guide brief
→ next build: avatar preview
→ expert review
```

Core principle:

```text
The character defines the look.
The reference movement defines the sign.
```

## Why Kinder Signs

Three use cases were compared.

| Use case | Role |
|---|---|
| **Kinder Signs** | Early communication across school and home |
| **Kinder Daily** | School-family communication and daily context |
| **Kinder Food** | Food routines and family guidance |

Kinder Signs was selected as the first commercial validation wedge because it brings together:

| Reason | Why it matters |
|---|---|
| School-home continuity | The same routine can continue from classroom to home |
| Simple educator action | The educator only selects the sign used that week |
| Differentiation | The value is not more content, but trusted continuity |
| Reusable library | One Signs and Flashcards Library can serve more schools and groups |
| Technical feasibility | Computer Vision can test the movement capture layer |
| School-led model | The school is the main customer and distribution channel |

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

| Metric | Why it matters |
|---|---|
| Children in first-cycle education | Market access |
| Enrolment rate at age 2 | Early routine access |
| Enrolment rate at age 3 | Continuity into the next stage |
| Early-childhood centres in Madrid | Local entry market |
| Private and concerted centre share | Potential commercial channel |
| Internet and digital readiness | Family reachability |
| GenAI adoption context | Digital readiness for AI-enabled services |

Sources include the Spanish Ministry of Education, Comunidad de Madrid and INE public datasets.

Relevant folders:

```text
data/
dashboard/
```

### 3. Static MVP mock

The prototype shows how Kinder Signs could work as a product.

| View | Purpose |
|---|---|
| `prototype/index.html` | School-family experience |
| `prototype/admin.html` | Kinder Signs internal and school/admin logic |

The mock shows the Signs and Flashcards Library, the school account structure, the group, teacher and child hierarchy, assignment to a whole group or individual child, family access and active packs, automatic family output preparation, and the reference-video-to-avatar preparation flow.

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

The Computer Vision POC tests whether a reference sign video can be converted into structured movement data.

| Metric | Result |
|---|---:|
| Frames analysed | 332 |
| Pose detection | 100% |
| Dominant hand detection | 93.98% |
| Missing hand frames | 20 |
| Overall status | Proceed with conditions |

The POC supports the first technical step:

```text
reference video
→ landmarks
→ movement data
→ motion diagnostics
```

This gives Kinder Signs a technical basis for the next build: testing whether a visual guide or avatar preview can follow reference movement without changing the sign.

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
→ draft pending expert review
```

LangSmith is used to evaluate the LLM content step. The workflow keeps AI as support for content operations, not as the authority on sign correctness.

Relevant folder:

```text
workflow/
```

### 6. Cost and timeline

The proposed next phase is a focused validation investment.

| Item | Estimate |
|---|---:|
| Timeline | 8 to 9 weeks |
| Validation investment | €5.5k to €17.8k |

This is a validation budget, not a full launch budget.

The main cost drivers are expert review, user research, a 3 to 5 sign content test, Computer Vision refinement, workflow testing and content production.

Relevant file:

```text
cost_timeline/estimate.md
```

## Business model hypothesis

Kinder Signs is designed as a **school-led B2B/B2B2C product**.

The school is the main customer. Families are users and beneficiaries.

| Layer | Product logic |
|---|---|
| **School account** | The centre subscribes to Kinder Signs |
| **Classroom group** | Signs and packs can be assigned by group |
| **Teacher** | The educator selects the sign used that week |
| **Child profile** | Outputs can be prepared for a group or a specific child |
| **Family access** | Parents and caregivers receive the guidance |
| **Premium packs** | Flashcards, routines, mini stories or songs can be activated by school or group |
| **Prepared output** | Kinder Signs prepares the right family material automatically |

The MVP supports two assignment levels:

```text
Assign to whole group
Assign to individual child
```

Premium content is positioned mainly as a school or classroom-group purchase.

## Repository structure

```text
.
├── cost_timeline/       Validation budget and timeline
├── dashboard/           Tableau dashboard documentation and assets
├── data/                Tableau-ready datasets and source register
├── feedback/            Round 1 decision after feedback
├── poc/                 Computer Vision movement POC
├── prototype/           Static MVP mock
├── research/            Market research, risks and use cases
└── workflow/            n8n and LangSmith workflow
```

## Round 1 status

| Requirement | Status |
|---|---|
| Sector and company size | Covered |
| Research and 2 to 3 use cases | Covered |
| Public dataset selected and justified | Covered |
| Dashboard with 5 to 7 stakeholder metrics | Covered |
| Simple POC | Covered |
| n8n or equivalent workflow | Covered |
| LangSmith sample | Covered |
| Cost and timeline | Covered |
| Presentation | Covered |
| `round1_decision.md` | To complete after feedback |

## Next validation phase

After Round 1 feedback, the next phase should focus on a small MVP.

```text
4 to 5 signs
→ Signs and Flashcards Library
→ school, group, teacher and child assignment
→ family card output
→ active packs logic
→ movement preview and avatar preview exploration
```

Expected decision after Round 1 feedback:

**KEEP Kinder Signs as the first commercial validation wedge**, unless feedback shows that another use case has stronger evidence.

The goal is to test whether Kinder Signs creates enough value for schools and families before scaling.