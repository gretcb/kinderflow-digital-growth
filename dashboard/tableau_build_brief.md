# KinderFlow — Tableau Build Brief

## Executive question

**Is there enough market, digital and competitive evidence to justify piloting Kinder Signs in Spain?**

## Dashboard title

**Kinder Signs — Market Opportunity & Pilot Readiness**

## Recommended layout

### 1. Market opportunity — KPI row
Use 4–5 KPI cards:
- **491,811** children enrolled in first-cycle Early Childhood Education
- **50.2%** 0–2 enrolment rate
- **76.4%** enrolment at age 2
- **12.2** average pupils per unit
- **+140** centres vs prior year

Keep the 50.2% label explicit: **0–2 enrolment rate**, not “0–3 penetration”.

### 2. Digital & AI readiness
Recommended chart: grouped bars or dot plot.

Show:
- Internet: Spain **96.3%** vs Madrid **98.0%**
- Ecommerce: Spain **59.6%** vs Madrid **65.0%**
- GenAI use: Spain 16–74 **37.9%**
- GenAI 25–34 **57.2%**
- GenAI 35–44 **43.8%**

Tooltip/source note:
INE Household ICT Survey 2025; theoretical sample **26,862 dwellings**; three-stage stratified survey. Age bands are proxies for plausible parent cohorts, not parent-specific results.

### 3. Competitive positioning — key visual
Scatter plot using `competitive_positioning.csv`.

- **X axis:** Content library (0) → Contextual learning programme (5)
- **Y axis:** Passive learning (0) → Guided / interactive practice (5)
- Label each point directly.
- Keep dots equal size.
- **Kinder Signs must be visibly labelled `TARGET POSITIONING — HYPOTHESIS`.**
- Do not imply market share.

Tooltip should include:
- evidence summary
- school-home integration score
- professional validation score
- source ID
- confidence

### 4. Executive takeaway
Use a short text block:

**Evidence supports a pilot — not product-market fit.**

Supporting lines:
- Spain provides meaningful institutional access through first-cycle education.
- Madrid is a digitally mature pilot environment.
- Spanish Baby Sign competition exists; Spanish-first is not a moat.
- Kinder Signs' hypothesis is school-home continuity + validated contextual learning.
- Demand, WTP and educator adoption still require primary validation.

## Visual principles

- One dashboard, not multiple pages.
- 5–7 decision metrics visible at first glance.
- Minimal chartjunk.
- Direct labels where possible.
- No rainbow palette.
- Do not use colour as the only differentiator.
- Keep source/methodology in tooltips or a compact source note.
- Bars should start at zero.
- Equal-size points on competitive map.
- Make `TARGET POSITIONING — HYPOTHESIS` explicit.

## Data files

1. `tableau_master.csv` — market/digital/AI metrics
2. `competitive_positioning.csv` — positioning map
3. `source_register.csv` — source, sample/methodology and limitations

## Important evidence boundary

The dashboard supports a **pilot decision** only.

It does not prove:
- product-market fit
- willingness to pay
- CAC
- retention
- market share
- causal benefits of Baby Sign
