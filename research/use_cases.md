# Use Cases — KinderFlow

## 1. Decision context

KinderFlow is being evaluated as a digital growth platform for Chleo's early-childhood education business.

Round 1 considers three opportunities:

1. **Kinder Signs** — early communication across school and home
2. **Kinder Daily** — school-family information and shared context
3. **Kinder Food** — continuity between school meals and family routines

The objective is not to decide which idea sounds most attractive.

The objective is to identify which use case has the strongest combination of:

- customer relevance;
- evidence;
- differentiation;
- school-home integration;
- commercial potential;
- technical feasibility;
- credible AI value;
- and manageable risk.

> **Round 1 question**
>
> Which use case is worth learning about first?

---

## 2. The customer is not just the parent

KinderFlow operates in a multi-sided environment.

The person who uses the service may not be the person who chooses it or pays for it.

| Role | Primary actor | What matters most |
|---|---|---|
| **Decision maker** | School owner / director | Family value, differentiation, cost, implementation |
| **Professional user** | Educator | Simplicity, credibility, low workload |
| **Consumer user** | Parent / caregiver | Relevance, trust, convenience |
| **Influencer** | Educator / specialist / other parents | Confidence in the service |
| **Payer** | School, family or both | Clear value for money |
| **Beneficiary** | Child and family | Better continuity across routines |

This distinction matters because a product can fail even when parents like the idea.

For example:

- parents may value a feature that creates too much work for educators;
- educators may value a tool that the school will not pay for;
- a director may buy software that families barely use.

### Implication

> **KinderFlow needs fit across buyer, user and workflow — not just parent interest.**

---

# 3. The shared customer problem

The three use cases address different routines, but the underlying problem is similar.

Families already have access to large amounts of information through:

- educators;
- school apps;
- professionals;
- Google;
- YouTube;
- social media;
- specialist apps;
- and generative AI.

The problem is therefore not simply lack of information.

The stronger hypothesis is:

> **Useful guidance becomes fragmented when a child's routine moves between school and home.**

KinderFlow explores whether the school's existing position of trust can make that transition more useful.

### Shared Job to Be Done

> **When an important routine continues from school into home, help me understand what matters and what I should do next without making me search across disconnected sources.**

---

# 4. UC1 — Kinder Signs

## The problem

Baby Sign content already exists in Spanish through courses, instructors, apps, websites and free video.

This means Kinder Signs cannot rely on:

- being in Spanish;
- having a large sign library;
- or using AI-generated video.

Those are not strong differentiators.

The more specific problem is continuity:

> A sign may be introduced by an educator or professional, but the family still needs to remember which sign is being used, how it is performed and when to use it naturally at home.

## Job to Be Done

> **When my child's school introduces a sign, help me continue the same validated sign at home without having to search for or compare different versions myself.**

## Parent value

**Jobs**

- remember the sign;
- see how it is performed;
- understand when to use it;
- revisit it quickly.

**Pains**

- searching online;
- different versions of the same idea;
- forgetting the movement;
- long-form content for a small immediate need;
- uncertainty about the source.

**Gains**

- one approved reference;
- short contextual guidance;
- easy mobile access;
- consistency with school;
- greater confidence in the content.

## Value proposition

> **Professionally validated early-communication content that makes it easy for families to continue at home what is being introduced in the educational setting.**

---

## What the experience could look like

A lightweight first workflow could be:

1. The educator selects the sign being introduced.
2. The family receives the corresponding approved Kinder Sign.
3. The parent sees:
   - a clear original demonstration;
   - a short explanation;
   - a realistic usage context.
4. The content remains available for later reference.

The educator should not need to produce the content.

### Important design principle

> **The service should reduce explanation, not create another teaching task.**

---

## AI role

Computer Vision has a specific role in Kinder Signs:

### Primary role — content production

Initial experimentation showed that generative video can produce visually realistic people while still getting detailed hand movement wrong.

Relevant errors include:

- finger configuration;
- hand orientation;
- trajectory;
- positioning;
- timing;
- bilateral movement.

The proposed architecture is therefore:

> **validated movement → Computer Vision extraction → structured motion data → original KinderFlow visual asset → expert validation**

The validated movement remains the source of truth.

Generative AI may help create the final presentation, but it should not decide the sign movement.

### AI vs non-AI baseline

KinderFlow could simply film every sign manually with a performer.

That remains a valid baseline.

The AI question is therefore:

> **Can Computer Vision make original validated content easier and more consistent to produce at scale?**

This is the key technical hypothesis for Round 1.

---

## Main alternatives

- Baby Sign Spain
- HCLM / Háblame Con Las Manos
- BabySignLanguage.com
- Baby Sign and Learn
- Baby Sign apps
- instructors and coaches
- YouTube
- Instagram / TikTok
- Google
- generic GenAI

### Differentiation hypothesis

Not:

> more content + Spanish + AI

But:

> **validated content + school-home continuity + contextual microlearning + original content infrastructure**

---

## What still needs to be proven

- Do families value using the same signs as the school?
- Will educators participate in a very lightweight workflow?
- Is Kinder Signs better enough than sending a free video?
- Who would pay?
- Can Computer Vision capture the required movement reliably?
- Can original content be produced at a sustainable cost?

---

# 5. UC2 — Kinder Daily

## The problem

The school-family software market is already established.

Current products provide combinations of:

- messaging;
- daily diaries;
- meals;
- naps;
- attendance;
- photos;
- video;
- billing;
- surveys;
- permissions;
- and administration.

Provider-reported installed bases reviewed in the sector research confirm that this is an existing paid B2B category.

Therefore, the problem is not:

> Schools need a communication app.

That has already been validated by the market.

The real question is:

> **Is there an important part of the school-family workflow that existing tools still handle poorly?**

---

## Jobs to Be Done

### Parent

> **When the school sends me information, help me quickly understand what matters and whether I need to do anything at home.**

### Educator

> **When I need to keep families informed, help me communicate what matters without repeating myself or duplicating administrative work.**

### Director

> **Help my school provide a high-quality family experience without increasing staff workload or replacing working systems unnecessarily.**

---

## Value proposition hypothesis

> **A shared school-family context layer that makes existing information more useful instead of simply collecting more data.**

That distinction is important.

Kinder Daily should not become another diary unless it solves something materially better.

---

## Potential platform role

Daily may be more valuable as infrastructure than as a standalone product.

For example:

> **Daily:** what happened  
> **Food:** what does it mean for home?

or:

> **Daily:** which communication activity is being used  
> **Signs:** the corresponding approved learning content

This suggests a possible architecture:

> **shared context → specialised KinderFlow services**

---

## AI role

Potential uses include:

- summarisation;
- categorisation;
- retrieval;
- translation;
- transformation of approved information;
- structured extraction.

But AI is not automatically necessary.

> **If a deterministic workflow solves the problem better, Kinder Daily should use the simpler solution.**

---

## Main alternatives

- Pequebook
- TokApp
- KinderUp
- Dinantia
- Alexia
- WhatsApp
- email
- paper
- verbal communication

---

## What still needs to be proven

- Is there a meaningful unsolved workflow?
- Is integration more attractive than replacement?
- Would educators save time?
- Would parents notice a meaningful improvement?
- Is Daily valuable independently?
- Or is its strongest role supporting Signs and Food?

---

# 6. UC3 — Kinder Food

## The problem

Food is a routine that naturally crosses school and home.

Parents may receive:

- the school menu;
- information about what was eaten;
- allergen information;
- professional advice;
- feeding guidance;
- and content from specialist platforms.

These sources are often disconnected.

Official Community of Madrid guidance reinforces the school-home logic: families need sufficient information about school meals to complement children's food intake outside the centre.

The opportunity is therefore not another food database.

It is:

> **turning school food context into useful, trusted continuity at home.**

---

## Job to Be Done

> **When I know what my child was offered or ate at school, help me understand the relevant context for home without making me interpret menus or search across multiple sources.**

---

## Parent value

**Jobs**

- understand school meals;
- organise the rest of the day;
- manage food exposure and routines;
- remember trusted guidance;
- coordinate between caregivers.

**Pains**

- menus without enough context;
- fragmented information;
- contradictory online advice;
- uncertainty about what matters;
- repeated searching.

**Gains**

- relevant context;
- trusted sources;
- simpler next steps;
- continuity between caregivers;
- less information searching.

---

## Value proposition

> **A trusted school-home food layer that connects what happens during the school day with useful approved guidance for the family.**

---

## Competitive reality

Solid Starts is an important benchmark because it already provides:

- structured food information;
- age/development guidance;
- allergen and safety information;
- tracking;
- professional review;
- Spanish-language material;
- caregiver/daycare guidance.

This challenges several easy differentiation claims.

Kinder Food cannot realistically win by offering:

- more food content;
- Spanish localisation;
- recipes;
- or generic complementary-feeding guidance.

### Differentiation hypothesis

> **The opportunity is the two-way connection between school context and trusted home guidance.**

---

## AI role

The appropriate AI architecture is constrained:

> **structured school input → retrieval from approved knowledge → family-friendly explanation**

Potential techniques:

- RAG;
- menu parsing;
- classification;
- structured retrieval;
- summarisation.

AI should not independently:

- diagnose allergies;
- prescribe therapeutic diets;
- diagnose feeding disorders;
- or replace clinical judgement.

---

## What still needs to be proven

- Do families actually value this continuity?
- Can the school provide useful information without additional workload?
- Does Food provide enough value beyond Daily?
- What level of professional review is needed?
- Who pays?
- Can the product remain clearly educational rather than clinical?

---

# 7. Jobs to Be Done comparison

| Use case | Core Job to Be Done |
|---|---|
| **Kinder Signs** | Help me continue the same validated early-communication learning at home |
| **Kinder Daily** | Help me understand what matters in the information exchanged between school and home |
| **Kinder Food** | Help me turn school food context into useful continuity at home |

### Insight

All three jobs involve **continuity**, but they solve different levels of the problem:

- Signs → learning
- Daily → information
- Food → routine guidance

This is what makes the KinderFlow umbrella coherent.

---

# 8. Strategyzer view — where is the actual value?

A useful way to assess each proposition is to separate the **existing customer job** from the **proposed value**.

| Use case | Existing job | Current workaround | KinderFlow hypothesis |
|---|---|---|---|
| **Signs** | Remember and use a sign | Search, course, video, instructor | School-linked validated microlearning |
| **Daily** | Understand school information | Existing app, WhatsApp, verbal communication | More useful shared context |
| **Food** | Coordinate meals across settings | Menu + searching + professional advice | School context connected to trusted guidance |

### Strategyzer implication

The highest-risk assumptions are not technical.

They are:

1. whether customers perceive enough additional value;
2. whether the workflow fits existing behaviour;
3. whether someone is willing to pay.

These assumptions should be tested before scaling product development.

---

# 9. Design Thinking view

## Empathise

The problem must be understood separately for:

- directors;
- educators;
- parents.

Desk research gives context, but it cannot replace interviews or observed behaviour.

## Define

The current problem definition is:

> **Families already have information. What is missing may be trusted continuity between school context and home action.**

## Ideate

KinderFlow explores three responses:

- Signs → communication learning
- Daily → shared context
- Food → feeding continuity

## Prototype

Round 1 prototypes the most distinctive technical uncertainty:

> **Can validated sign movement be extracted into structured motion data?**

## Test

The next customer tests should focus on:

- usefulness;
- educator effort;
- trust;
- behaviour;
- willingness to pay;
- preference versus existing alternatives.

### Design Thinking implication

> **The POC proves technical learning, not customer desirability. Both need separate evidence.**

---

# 10. Desirability, feasibility and viability

| Dimension | Kinder Signs | Kinder Daily | Kinder Food |
|---|---|---|---|
| **Problem evidence** | Medium | High | High |
| **Desirability** | Promising, not validated | Category validated; Kinder proposition not | Promising, not validated |
| **Technical feasibility** | Medium–High for narrow POC | High | High for baseline |
| **Credible AI role** | **High** | Medium | Medium–High |
| **Commercial evidence** | Medium | **High** | Medium–High |
| **Differentiation potential** | **High** | Low–Medium | Medium–High |
| **Adoption risk** | Medium | **High** | Medium |
| **Privacy exposure in first MVP** | Low–Medium | **High** | Medium |
| **Professional governance** | High | Medium | **High** |
| **Fit with Chleo's business** | **High** | High | High |
| **Round 1 learning value** | **High** | Medium | Medium–High |

> **NOTE**
>
> These are strategic assessments based on the evidence currently available. They are not statistical measurements or forecasts.

---

# 11. Marketing view

## Segment

The initial segment is not "all parents".

The most defensible starting segment is:

> **Families of children in first-cycle Early Childhood Education, initially reached through an existing nursery-school relationship in Madrid.**

The official Spanish education statistics show a substantial institutional 0–3 population, while INE data supports high digital readiness in Spain and Madrid.

Those figures establish access potential.

They do not establish KinderFlow demand.

---

## Target

The first pilot should focus on Chleo's existing family-school ecosystem because it provides:

- immediate user access;
- existing trust;
- educator access;
- lower research cost;
- realistic workflow conditions.

This is a **pilot target**, not necessarily the final scalable market.

---

## Positioning

### KinderFlow

> **Trusted early-childhood guidance connected to the routines that move between school and home.**

### Kinder Signs

> **The same validated early-communication learning used at school, made simple to continue at home.**

### Kinder Daily

> **School-family information turned into useful shared context.**

### Kinder Food

> **Trusted food guidance connected to what happens during the school day.**

---

## Channels

| Channel | Role |
|---|---|
| **Existing school relationship** | Trust, pilot and B2B2C acquisition |
| **Educators / professionals** | Recommendation and credibility |
| **Google Search** | Intent-led discovery |
| **YouTube** | Educational discovery |
| **Instagram** | Awareness and consideration |
| **TikTok** | Experimental reach |
| **Direct B2B outreach** | Future school acquisition |

The digital-distribution research supports these as channel hypotheses.

It does **not** provide KinderFlow conversion rates or CAC.

---

# 12. Business-model hypotheses

The current evidence does not justify selecting one business model yet.

| Model | Potential fit | Main question |
|---|---|---|
| **School-paid B2B** | Daily / platform | Will schools pay? |
| **School-sponsored B2B2C** | Signs / Food | Is family value high enough for the school to fund it? |
| **Family subscription** | Signs / Food | Is value strong enough versus free substitutes? |
| **Freemium** | Family acquisition | What justifies the paid tier? |
| **Professional licence** | Signs / validated content | Is there professional demand? |
| **Hybrid** | Platform + premium modules | Does complexity improve economics or damage adoption? |

### Important distinction

Competitor pricing proves that people and organisations spend money in these categories.

It does not prove:

> **KinderFlow willingness to pay.**

---

# 13. Comparative Round 1 scoring

To make the decision explicit, the three use cases are scored against the criteria most relevant to Round 1.

### Scale

- **1 — weak**
- **2 — limited**
- **3 — moderate**
- **4 — strong**
- **5 — very strong**

| Criterion | Weight | Kinder Signs | Kinder Daily | Kinder Food |
|---|---:|---:|---:|---:|
| Problem clarity | 15% | 4 | 4 | 4 |
| Evidence strength | 15% | 3 | 5 | 4 |
| School-home integration | 15% | 5 | 5 | 5 |
| Differentiation potential | 15% | 5 | 2 | 4 |
| Commercial opportunity | 10% | 3 | 5 | 4 |
| Credible AI role | 10% | 5 | 3 | 4 |
| Round 1 feasibility | 10% | 4 | 4 | 4 |
| Risk profile | 5% | 4 | 2 | 3 |
| Platform fit | 5% | 5 | 5 | 5 |

### Weighted result

| Use case | Score / 5 | Interpretation |
|---|---:|---|
| **Kinder Signs** | **4.20** | Strongest combination of differentiation and learning value |
| **Kinder Food** | **4.05** | Strong problem and platform fit, with greater governance complexity |
| **Kinder Daily** | **3.95** | Strongest category evidence, but hardest to differentiate |

> **NOTE**
>
> The score does not mean Kinder Signs is already the best business. It means its next experiment provides the most useful Round 1 learning.

---

# 14. What is validated and what is still hypothesis

| Statement | Status |
|---|---|
| Spain has a substantial first-cycle education market | **Validated** |
| Madrid is highly digitally connected | **Validated** |
| Paid Baby Sign products exist | **Validated** |
| Schools already pay for school-family software | **Validated** |
| Families pay for specialist feeding products | **Validated** |
| Spanish-language alternatives already exist | **Validated** |
| Current CV tools can extract hand/pose landmarks | **Technically supported** |
| Families want Kinder Signs | **Hypothesis** |
| School-linked Signs creates more value than free content | **Hypothesis** |
| Educators will adopt the workflow | **Hypothesis** |
| Schools will pay for KinderFlow | **Hypothesis** |
| Families will pay | **Hypothesis** |
| Daily needs to become a new standalone platform | **Hypothesis** |
| Food provides enough value beyond Daily | **Hypothesis** |
| School distribution will reduce CAC | **Hypothesis** |

### Insight

> **Round 1 has enough evidence to justify experimentation, but not enough to justify scale.**

---

# 15. Kill criteria

A good pilot must also define what evidence would make us stop or change direction.

## Kinder Signs

Reconsider the use case if:

- families do not value school-home consistency;
- educators reject even a lightweight workflow;
- free content is perceived as equally useful;
- Computer Vision cannot capture the movement reliably enough;
- professional validation makes production economics unrealistic.

## Kinder Daily

Reconsider if:

- no meaningful unsolved workflow emerges;
- schools strongly resist another system;
- integration creates duplicate work;
- the value can easily be reproduced by existing platforms.

## Kinder Food

Reconsider if:

- families do not value school-linked food context;
- the service is perceived as another menu feature;
- educator workload increases materially;
- professional governance becomes too expensive;
- safe educational boundaries cannot be maintained.

---

# 16. Round 1 recommendation

**Kinder Signs moves forward to the Round 1 technical POC.**

This is not because it has the strongest market evidence.

Kinder Daily has stronger evidence of an established B2B category.

Kinder Food has strong institutional support for the underlying school-home problem.

Kinder Signs is selected because it combines:

- a relevant school-home problem;
- stronger differentiation potential;
- fit with Chleo's existing educational context;
- a credible Computer Vision role;
- limited child-data requirements for the first experiment;
- and a technical uncertainty that can be tested quickly.

### POC question

> **Can validated sign movement be captured reliably as structured hand and pose data that could support future original KinderFlow content production?**

The POC does not need to prove:

- product-market fit;
- commercial demand;
- full sign recognition;
- automated linguistic correctness;
- hyperrealistic motion transfer;
- or large-scale content production.

It needs to answer one narrower question well.

---

# 17. What happens next

The next investment should reduce uncertainty rather than add features.

### Kinder Signs

**Technical test**

- MediaPipe landmark extraction
- tracking quality
- structured output

**Customer test**

- parent concept test
- educator workflow test
- comparison with free-video alternative

### Kinder Daily

**Customer/workflow test**

- current communication journey
- duplicated work
- switching/integration pain
- unmet workflow discovery

### Kinder Food

**Customer/workflow test**

- usefulness of school-home context
- educator effort
- professional boundaries
- incremental value over Daily

---

# 18. Decision

The evidence currently supports:

> **KEEP KinderFlow as the platform hypothesis.**

> **VALIDATE Kinder Signs first.**

> **KEEP Kinder Daily and Kinder Food active as complementary opportunities, but do not build them yet.**

The broader platform should only expand when evidence shows that shared infrastructure creates more value than separate focused services.

---

# 19. Evidence base

This assessment should be read together with:

- `research/sector_research.md`
- `research/opportunities_risks.md`

Key external evidence used across the analysis includes:

| Source | What it supports | URL |
|---|---|---|
| Ministerio de Educación, Formación Profesional y Deportes | Spanish first-cycle Early Childhood Education market | https://www.educacionfpydeportes.gob.es/servicios-al-ciudadano/estadisticas/no-universitaria/alumnado/matriculado/2025-2026-da.html |
| INE — Household ICT Survey 2025 | Spanish and Madrid digital readiness | https://www.ine.es/dyngs/Prensa/TICH2025.htm |
| INE — Enterprise ICT Survey | Business digitalisation context and methodology | https://www.ine.es/dynt3/metadatos/RespuestaDatos.html?oper=129 |
| Eurostat | Enterprise AI adoption context | https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises |
| Comunidad de Madrid | School-home nutrition continuity | Official regional education / nutrition guidance |
| MediaPipe / Google AI Edge | Hand and pose landmark extraction | https://ai.google.dev/edge/mediapipe/solutions/guide |
| Baby Sign Spain | Spanish Baby Sign category evidence | https://www.babysignspain.com/ |
| Solid Starts | Feeding-platform benchmark | https://solidstarts.com/ |
| GDPR | Privacy and children's data | https://eur-lex.europa.eu/eli/reg/2016/679/oj |
| Spanish LOPDGDD | Children's consent framework | https://www.boe.es/buscar/act.php?id=BOE-A-2018-16673 |
| Google Generative AI Prohibited Use Policy | AI-provider constraints | https://policies.google.com/terms/generative-ai/use-policy?hl=en |

> **NOTE**
>
> Vendor evidence is used to document competitors' own products, features, pricing or reported reach. It is not treated as audited market share or evidence of willingness to pay for KinderFlow.