# KinderFlow - Early Childhood Digital Growth

## Executive summary

KinderFlow is a market-validation and AI consulting project for an early-childhood education business in Madrid.

The project evaluates **Kinder Signs** as a potential first opportunity: a trusted early-communication service that connects approved sign guidance between school and home.

The recommendation is:

> **Proceed with further market validation before scaling.**

The evidence supports a focused validation phase. It does not yet prove product-market fit, willingness to pay or scalable adoption.

---

## Project question

Can a small early-childhood education business use its existing school-family trust relationship to create a credible digital growth opportunity?

For Kinder Signs, the specific question is:

> Can professionally bounded Baby Sign guidance become more useful when it is connected to the real routines that happen across school and home?

---

## Why Kinder Signs

Three use cases were assessed:

| Use case | Role |
|---|---|
| **Kinder Signs** | Early communication across school and home |
| **Kinder Daily** | School-family context and daily communication |
| **Kinder Food** | Food continuity between school and home |

Kinder Signs was selected as the first validation opportunity because it combines:

- a clear school-home continuity hypothesis;
- differentiation beyond a generic Baby Sign dictionary;
- a credible Computer Vision feasibility test;
- low need for child personal data in the first experiment;
- and strong fit with the existing early-childhood education context.

This does not mean Kinder Signs is already a proven business. It means it is the strongest first validation step.

---

## Repository structure

```text
.
├── cost_timeline/       # Validation budget and timeline
├── dashboard/           # Tableau dashboard documentation and workbook assets
├── data/                # Tableau-ready datasets and source register
├── feedback/            # Decision notes after review / feedback
├── poc/                 # Computer Vision motion-representation POC
├── research/            # Sector research, opportunities, risks and use-case analysis
└── workflow/            # n8n and LangSmith governed LLM workflow
````

---

## Market and dashboard evidence

The Tableau dashboard evaluates whether there is enough market, digital and competitive evidence to justify further validation of Kinder Signs.

It supports three conclusions:

1. Spain provides a meaningful early-years education audience.
2. Madrid is a credible initial market environment.
3. Existing Baby Sign alternatives validate the category, but Spanish-language content alone is not a moat.

The dashboard supports market access and positioning. It does **not** prove demand, willingness to pay or product-market fit.

Relevant files:

```text
dashboard/
data/
```

---

## Computer Vision POC

The technical POC tests whether a validated sign video can be converted into structured motion data.

The POC uses MediaPipe to extract hand and pose landmarks from an adult reference video.

Current observed results:

| Metric                               |                  Result |
| ------------------------------------ | ----------------------: |
| Frames analysed                      |                     332 |
| Pose detection                       |                    100% |
| Dominant hand detection              |                  93.98% |
| Missing hand frames                  |                      20 |
| Overall motion-representation status | Proceed with conditions |

The POC demonstrates that movement can be captured as structured data for further experimentation.

It does **not** prove:

* Baby Sign correctness;
* ASL or LSE correctness;
* clinical or developmental benefit;
* avatar generation;
* motion retargeting;
* synthetic-video fidelity;
* or product-market fit.

Relevant files:

```text
poc/
```

---

## Governed AI workflow

The workflow layer demonstrates how approved sign content and a CV motion summary can be transformed into a parent-facing draft while preserving quality controls.

Workflow logic:

```text
approved sign content + CV motion summary
→ LLM-generated family draft
→ deterministic quality checks
→ LangSmith trace/evaluation
→ draft pending professional approval
```

Important boundary:

> LangSmith evaluates the LLM content-transformation step. It does not validate the MP4 video, sign movement, Baby Sign correctness or Computer Vision quality.

Relevant files:

```text
workflow/
```

---

## Cost and timeline

The next validation phase is estimated at:

| Item              |     Estimate |
| ----------------- | -----------: |
| Timeline          |    8-9 weeks |
| Validation budget | €5.5k-€17.8k |

This is a validation budget, not a product-launch budget.

The main cost drivers are:

* expert review;
* user research;
* original content production;
* educator workflow testing;
* and technical refinement across more signs.

Relevant file:

```text
cost_timeline/estimate.md
```

---

## Key limitations

KinderFlow is not ready to scale.

The main open questions are:

* parent willingness to pay;
* school willingness to pay;
* educator adoption and workload;
* engagement and retention;
* professional validation process;
* scalable acquisition economics;
* and motion reliability across more signs, performers and capture conditions.

---

## Recommended next step

Run a focused validation phase for Kinder Signs:

1. Test 3-5 approved signs.
2. Interview parents and educators.
3. Measure whether school-home continuity creates enough additional value.
4. Validate willingness to pay.
5. Decide whether to continue, change direction or stop.

The next investment should buy evidence, not features.
