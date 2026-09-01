# Use Case Definition — Kinder Signs

## 1. Round 2 Decision

**Kinder Signs remains the selected use case for Round 2.**

Round 1 established enough market, product and technical evidence to continue. Round 2 now moves Kinder Signs from opportunity validation into product and business validation.

The focus is to prove that Kinder Signs can work as a real school-led digital service with a repeatable content-production process, a usable school and family experience, a credible commercial model and a clear path to responsible deployment.

---

## 2. The Business Problem

Some early-years centres already introduce Baby Sign in the classroom. The problem is what happens afterwards.

Families may know that a sign was used at school, but they do not always receive the same short, contextual guidance for using it at home. They may turn to YouTube, Instagram, PDFs or other free resources, creating a fragmented experience that is disconnected from the school routine.

This creates three practical gaps:

### Fragmented learning

The sign used at school and the content found at home may not match.

### Limited context

A video may show how a sign looks, but not when or how to use it naturally in a daily routine.

### Weak school-home continuity

The school has the trusted relationship with the family, but that trust is not yet translated into a structured digital experience.

Kinder Signs tests whether the school can become the trusted distribution channel for the same sign, routine and family guidance.

---

## 3. Customer and Market

**Platform:** KinderFlow — Early Childhood Digital Growth

**First product:** Kinder Signs — a school-led Signs & Flashcards Library

**Primary customer:** Early-years centre

**Primary users:** Educators and families

**Primary beneficiary:** Child aged 0–3

**Initial market:** Community of Madrid

**Business model:** School-led B2B / B2B2C

The school is the main paying customer and distribution channel. Families receive the experience through the school relationship.

---

## 4. Product Proposition

Kinder Signs is not another Baby Sign dictionary.

The core product flow is:

```text
Kinder Signs creates the Signs & Flashcards Library
→ the educator selects this week’s sign
→ the sign is assigned to a group or child
→ families receive matching guidance at home
```

The educator does not create content, upload production videos or manage AI.

The school-facing experience should stay simple:

```text
Select group or child
→ choose this week’s sign
→ send to families
```

The value is not more content. The value is trusted continuity across school and home.

---

## 5. Kinder Signs Content Studio

The internal content-production engine is the heart of Kinder Signs.

The production flow is:

```text
Approved sign video
→ MediaPipe / Computer Vision movement check
→ movement data + skeleton
→ visual layer
→ avatar build / preview
→ human review
→ published sign in the Signs & Flashcards Library
```

The sign video comes first. The family card and flashcard are outputs created once the sign becomes a published library item.

Core principle:

> **The character defines the look. The reference movement defines the sign.**

This keeps the visual layer separate from the source movement and gives KinderFlow a clearer path to controlled avatar generation.

---

## 6. AI and Technology Roles

Kinder Signs separates responsibilities across different technical layers.

| Capability | Role |
|---|---|
| **Computer Vision** | Extract and represent movement from reference sign video |
| **Skeleton / movement layer** | Make the captured movement visible and reviewable |
| **Avatar layer** | Recreate the visual presentation from the captured movement |
| **LLM** | Support family-facing guidance and structured content drafting |
| **LangSmith** | Monitor and evaluate the LLM content step |
| **Human review** | Control publication before content becomes available to schools |

None of these components automatically certifies sign correctness.

Human review remains the publication control.

---

## 7. Stakeholders

| Stakeholder | Role | Main interest |
|---|---|---|
| **School owner / director** | B2B buyer and decision maker | Differentiation, adoption, family value, commercial return |
| **Educator** | Professional user | Very low weekly effort, simple sign selection |
| **Family / caregiver** | Family user | Clear guidance that matches the school routine |
| **Child aged 0–3** | Primary beneficiary | Consistent communication across school and home |
| **Sign / content expert** | Human reviewer | Quality and consistency of published sign content |
| **KinderFlow operations** | Platform operator | Reliable content production and low operational friction |
| **Legal / compliance** | Governance function | Privacy, data minimisation and responsible deployment |

---

## 8. Round 2 MVP

Round 2 focuses on three product capabilities and one supporting content layer.

### Capability 1 — Functional Computer Vision Flow

```text
reference sign video
→ MediaPipe processing
→ hand and pose landmarks
→ skeleton preview
→ technical metrics
```

Current technical evidence from one analysed reference video:

| Metric | Current result |
|---|---:|
| Frames analysed | 332 |
| Pose detection | 100% |
| Dominant-hand detection | 93.98% |
| Missing hand frames | 20 |
| Technical status | Proceed with conditions |

These figures describe detection coverage from one reference video. They are not an accuracy score for sign correctness.

### Capability 2 — Signs & Flashcards Library

The first MVP library should contain 4–5 signs, starting with:

```text
More
Eat
Water
All done
Help
```

Each published library item can include:

- sign video
- routine context
- family guidance
- flashcard
- PDF / image output
- publication status
- school visibility

### Capability 3 — School Delivery Experience

The school uses the published library rather than creating content.

The delivery flow is:

```text
School
→ group(s)
→ teacher
→ this week’s sign
→ assign to group or individual child
→ family output prepared
```

The assignment structure supports both full-group and individual-child use.

### Supporting Layer — Premium Content Packs

Premium content is primarily sold at school or group level.

Examples:

- Flashcards
- Routine packs
- Mini stories
- Songs

These packs can be linked to a group or individual child as part of the MVP logic, without implementing real billing.

---

## 9. Success Criteria

Success criteria are the signals that will tell us whether Kinder Signs is strong enough to keep investing in.

At the end of the pilot, we want to know:

### School adoption

Are educators actually using Kinder Signs as part of the weekly routine?

### Low operational effort

Can an educator select and send this week’s sign without creating additional production work?

### Family engagement

Are families opening and using the content sent by the school?

### Content-production reliability

Can Kinder Signs produce several signs through the same repeatable content workflow?

### Technical quality

Does the Computer Vision pipeline capture enough movement information for human review across 4–5 signs?

### Avatar quality

Can the avatar or visual guide reproduce the reference movement closely enough to support human review?

### Commercial signal

Do school decision makers see enough value to continue with a paid or expanded pilot?

Any numeric thresholds used in the pilot should be treated as **initial pilot targets**, not as industry benchmarks.

---

## 10. MVP Boundaries

Round 2 keeps the MVP focused so the core experience can run reliably.

The MVP focuses on:

- one content-production flow
- one Signs & Flashcards Library
- one school delivery flow
- 4–5 signs
- one controlled avatar / visual-guide path
- human publication control

The MVP does not depend on a full production billing system, live school-app integrations or automated sign certification.

---

## 11. Round 1 → Round 2 Evolution

### Round 1 — Opportunity Validation

Round 1 established:

- the market opportunity
- Madrid as the initial entry market
- the school-led business model
- the Kinder Signs positioning
- stakeholder metrics through the Tableau dashboard
- initial Computer Vision feasibility
- the n8n / LangSmith content workflow
- the first static product mock
- an initial cost and validation timeline

### Round 2 — Product and Business Validation

Round 2 converts the validated opportunity into a working product and commercial pilot proposition.

It will deepen Kinder Signs through five workstreams.

### 1. Kinder Signs Content Studio

Build the working content-production flow from approved sign video to movement representation, skeleton preview, controlled avatar rendering, human review and publication into the Signs & Flashcards Library.

### 2. Product Experience

Build the Signs & Flashcards Library, family guidance, printable flashcards and the school delivery experience around this week’s sign.

### 3. Business Case & Profitability

Define pricing, revenue model, production costs, operating economics, break-even and 12 / 36-month commercial scenarios.

### 4. Legal, Privacy & AI Compliance

Assess GDPR, EU AI Act, privacy by design, data flows, third-party processing, content governance and the deployment boundaries required for responsible use.

### 5. Commercial Pilot & Scale Gate

Define a real-world pilot with a small set of signs, participating educators and families, explicit KPIs and success criteria.

The pilot should end with a clear decision:

```text
Continue
Refine
Stop
Scale
```

---

## 12. Pilot Decision Gate

At the end of the pilot, KinderFlow should be able to answer three questions.

### Do schools want it?

Is Kinder Signs valuable enough for a school to keep using and paying for?

### Do families use it?

Does school-home continuity create enough engagement and practical value at home?

### Can Kinder Signs produce it reliably?

Can the content-production pipeline create and publish sign content with enough technical and operational consistency to scale?

The next decision should be based on evidence, not feature count.
