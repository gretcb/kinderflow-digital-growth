# KinderFlow Use Case Definition

Document status: final capstone reconciliation
Decision status: PROCEED WITH CONDITIONS
Primary operating case: Little Steps Nursery, a pseudonymised founder-observed case
Evidence rule: each quantitative statement is labelled as a founder-observed fact, public evidence, calculated scenario, benchmark, project estimate, pilot hypothesis, or TBD.

## Executive decision

KinderFlow should proceed to a small, controlled pilot, subject to the gates in this document. The opportunity is not yet a proven software business. It is a supported service hypothesis for nursery schools that already use or want to use baby signs and need a clearer way to review signs, assign them to groups, and give families consistent guidance.

The first paying customer is expected to be a nursery school or small nursery group. The economic buyer is the owner or director. Educators and support staff are daily users. In the intended service, families receive reviewed guidance through the nursery; they are not the core payer. The current product provides only a basic family-facing guidance preview.

The immediate decision is whether a 2 to 3 nursery, 3 to 5 sign pilot can demonstrate:

- reliable and reviewable sign evidence;
- an educator workflow that fits nursery routines;
- a useful family-facing assignment experience;
- safe content operations with complete provenance;
- a credible willingness to pay for a per-centre service.

The final recommendation is PROCEED WITH CONDITIONS. No claim of product-market fit, production readiness, family adoption, time savings, or return on investment is made before pilot evidence exists.

## Client and operating context

### Little Steps operating case

This is a pseudonymised operating case. It is not audited client financial information.

Little Steps is a founder-led nursery. Cleo, the owner and director, combines economic-buyer, service, quality, teaching, parent-support, and commercial responsibilities. Her limited time makes workflow fit important, but her existing Baby Sign activity also gives the pilot a credible domain entry point.

Founder-observed operating facts include:

- 3 paid lead educators;
- 3 classroom assistants who are interns or practicum staff, with cost TBD;
- 1 paid operations and cleaning team member;
- 1 owner and administrative director, with remuneration TBD;
- 1 finance and operations support role, with remuneration TBD;
- 9 people involved in the operating model, which must not be treated as 9 market-salary full-time equivalents;
- three nursery groups with capacity of 8, 14, and 20 children, for 42 places in total;
- about 38 occupied places at 90% occupancy;
- an existing Baby Sign practice known to staff;
- one-off Baby Sign training and course sales, but no observed recurring structured digital sign service;
- parent requests for sign lists or materials;
- use of Pequebook for general nursery communications in this specific setting.

The selected nursery planning envelope is approximately EUR 195,000 to EUR 238,000 a year, from about 90% occupancy over 10 months to full capacity over 11 months. The 85% occupancy case is a lower sensitivity outside these selected endpoints. This is a calculated revenue envelope, not profit, audited revenue, cash flow, or proof that a software budget exists.

Company-size treatment:

- 9 people are involved in the operating model;
- this is a founder-led operating case with no dedicated digital team; its legal enterprise category remains TBD;
- the 9 people must not be treated as 9 market-salary full-time equivalents.

### Problem statement

Nursery educators and leaders lack one controlled workflow that links:

1. a submitted or selected sign reference;
2. reviewable visual evidence;
3. a professional interpretation with explicit status;
4. an educator assignment to a nursery group;
5. a reviewed family-facing guidance item;
6. an audit trail for approval, blocking, and reuse.

The current workaround is fragmented across staff knowledge, one-off training, requests for lists or materials, general communication tools, and manual quality judgement. This can create inconsistent wording, repeated questions, unclear provenance, and added coordination. These are observed or research-supported problem signals. Their frequency and cost have not yet been measured.

## Users, buyer, payer, and jobs to be done

### Cleo, owner and director

Economic buyer: nursery owner or director
Payer: nursery school or nursery group
Decision authority: approves pilot participation, price testing, operating policy, and continuation

Job to be done:

> When my educators use baby signs, help me maintain a reviewed and consistent nursery practice, give families clear guidance, and see what was assigned without adding an unmanageable review or support burden.

Evidence status: founder-observed role and current practice; willingness to pay, acceptable contract structure, and budget source remain pilot hypotheses.

### Lead educator or Baby Sign coordinator

Primary user: educator who reviews or assigns a sign
Supporting user: a designated Baby Sign coordinator or content reviewer

Job to be done:

> When I want a nursery group to practise a sign, help me find or submit a reference, understand its status, assign reviewed guidance quickly, and answer family questions consistently.

Evidence status: workflow problem supported by current nursery context and prototype testing; repeated use, support burden, and acceptable assignment time require pilot measurement.

### Family member or carer

Recipient: family invited by the nursery
Payment role: not the core payer in the initial model

Job to be done:

> When the nursery assigns a sign, show me the same reviewed guidance in a clear, accessible format so I can understand what the nursery is practising and use it consistently if I choose.

Evidence status: families have asked for materials in the operating case. Actual access, repeat use, clarity, and perceived value remain unvalidated.

### Content reviewer

Primary responsibility: confirm that a sign is suitable for nursery use and that family guidance does not overstate certainty

Job to be done:

> When a sign candidate reaches review, give me traceable evidence, source and rights information, model output, and a clear approve, revise, or block decision.

Evidence status: the repository implements review-state logic and records evidence. Real reviewer effort, throughput, exceptions, and rework remain unmeasured.

### Beneficiaries

Families are direct service beneficiaries. Children may benefit indirectly from consistent adult guidance, but KinderFlow does not profile, score, diagnose, or process video of children in the core scope.

## Business model hypothesis

The initial route to market is school-led B2B or B2B2C:

- the nursery or nursery group purchases a per-centre subscription;
- nursery staff review, select, and assign content;
- families receive the assigned guidance through the nursery;
- future paid add-ons may include onboarding, staff training, specialist review, or additional content packs;
- add-on revenue is set to zero in the current ROI scenarios until tested;
- a direct-to-family subscription is outside the initial model.

The annual price hypotheses are EUR 600, EUR 1,200, and EUR 1,800 per centre. These correspond to EUR 50, EUR 100, and EUR 150 per month. They are pilot hypotheses, not published prices or observed willingness to pay.

For Little Steps, those annual prices are about 0.25% to 0.31%, 0.50% to 0.62%, and 0.76% to 0.92% of the calculated nursery tuition envelope. This shows proportional scale only. It does not prove affordability, profitability, budget availability, or willingness to pay.

Public vendor evidence for self-guided family plans and educator training provides category context, not KinderFlow pricing validation. The source register records approximate self-guided plans at EUR 30 to EUR 50, educator training at about EUR 180, observed platform access for one year, live training with format-dependent pricing, and school training with some prices unavailable. Sources conflict on five versus six sessions, so the model excludes a precise session-count benchmark.

Paid Spanish-language content and training already exist. Spanish-language content alone is therefore not a defensible differentiation. Kinder Signs must test whether school-led continuity, governed and versioned content, sign-specific provenance, group or audience assignment, reusable family materials, and measured reuse create enough additional value.

## Why AI is used and where it is not used

AI is useful only where it creates inspectable evidence or reduces a specific drafting burden.

### Computer vision role

The computer vision path can process a controlled sign reference, extract pose and motion evidence, and produce a manifest that a human can inspect. It is an evidence aid, not an autonomous sign-language authority and not a child assessment system.

### Language model role

The language model path can draft a professional interpretation from constrained evidence. The draft remains subject to review, status controls, source checks, and rights checks. HUMAN mode provides a deterministic fallback when provider-backed generation is unavailable or inappropriate.

### Explicit non-use

KinderFlow does not:

- analyse child video;
- score a child's communication;
- diagnose development;
- make automated educational decisions;
- send personal child or family data to a language model or LangSmith;
- deliver unreviewed or blocked content to families.

AI is not required for nursery assignment, family access, review-state enforcement, or audit logging. Those functions should remain deterministic.

## Current evidence and product boundary

### Proof of concept

The proof of concept is a local evidence pipeline. It demonstrates that a controlled adult sign reference can produce:

- extracted visual and pose evidence;
- versioned manifests and audit artefacts;
- run-specific professional interpretation;
- explicit reviewed, review-recommended, or failed states;
- a HUMAN fallback and optional provider-backed paths.

Historical WATER evidence and the current MORE demo path are technical evidence only. They do not establish sign-language correctness across signs, environments, people, or camera conditions. All output remains subject to qualified review.

### Minimum viable workflow

The repository also contains a local nursery workflow that can:

- display a reviewed professional record;
- assign a sign to a nursery group in session state;
- show a family-facing guidance preview;
- preserve a local audit trail for the demonstrated flow.

This is a workflow prototype, not a hosted multi-tenant service. Authentication, durable accounts, production access control, persistent assignments, real delivery, notifications, and operational integrations are not complete.

### Family-facing boundary

A family-facing guidance prototype exists. A personalised assignment-driven family library remains a next product iteration.

The controlled pilot must therefore add and test a small assignment-driven family mini-library. It must not describe the current static or session-based preview as a completed personalised delivery product.

### Content inventory boundary

The pilot target is 3 to 5 reviewed signs. The repository contains more than one sign list for different purposes:

- a six-item visual inventory used in interface and presentation material;
- a five-sign regression set used for content-operations checks.

Neither list is an approved production library. Pilot selection requires source, rights, expert review, and status confirmation for every included sign.

## Three validation perspectives

### Teacher perspective

The teacher question is whether educators can select and assign reviewed content in the course of normal work.

Pilot evidence must cover:

- first-assignment time;
- completion without help;
- repeat assignment by each nursery group;
- error, clarification, and support events;
- perceived usefulness and workflow fit.

### Family perspective

The family question is whether assigned guidance is delivered, accessible, understandable, and useful.

Pilot evidence must cover:

- successful delivery or access;
- first and repeat access;
- clarity and usefulness responses;
- accessibility issues;
- questions or confusion caused by the guidance;
- opt-out, withdrawal, and complaint events.

### Organisation perspective

The organisation question is whether the service can be operated, reviewed, sold, and governed at a sustainable burden.

Pilot evidence must cover:

- review time and rework per sign;
- provenance and rights completeness;
- critical content, privacy, and trust incidents;
- onboarding and support burden;
- named budget owner and price response;
- paid-continuation intent at a stated price;
- recurring content-production and vendor dependencies.

## Success measures and hard boundaries

The controlled pilot must use the following exact initial targets:

- first assignment completed in 2 minutes or less;
- at least 80% of educators complete the first assignment without help;
- all 3 Little Steps nursery groups activated;
- at least 2 repeat assignments per nursery group during the controlled service test.

The following are hard boundaries:

- child video processed: 0;
- child scoring: 0;
- automated educational decisions: 0;
- unreviewed content delivered: 0;
- blocked content delivered: 0;
- personal child or family data sent to a language model or LangSmith: 0;
- pilot sign provenance complete: 100%;
- review exceptions documented with rationale: 100%.

Additional family, willingness-to-pay, review-throughput, and support thresholds in the pilot measurement plan are provisional pilot hypotheses. They must be signed off before the first nursery activity.

## Evidence confidence

### Market confidence: MEDIUM

Public competitors and training providers show an active category and paid alternatives. The evidence does not establish the addressable number of schools, KinderFlow demand, or acceptable recurring pricing.

### User confidence: LOW

The Little Steps case and prior research support the problem direction. Evidence is still concentrated in one founder-led setting, and family behaviour has not been tested through a real assignment-driven service.

### Competitive confidence: MEDIUM

Available sources support the category and different offer types. Pricing visibility is incomplete, feature comparisons are not uniformly verified, and competitor evidence cannot substitute for customer interviews.

### Feasibility confidence: MEDIUM

The local pipeline and nursery workflow demonstrate a credible technical direction. Production hosting, access control, delivery, privacy operations, reviewer throughput, and multi-site reliability remain incomplete.

## Round 1 to Round 2 bridge

Round 1 research and prototype work established a plausible problem, a review-first concept, a local evidence pipeline, and a nursery assignment flow. It also exposed material gaps: limited buyer evidence, no family delivery evidence, no paid pilot, uncertain rights, and no measured operating burden.

Round 2 is not a broader feature build. It is an evidence-focused pilot that must:

1. recruit 2 to 3 nursery schools;
2. select and clear 3 to 5 signs;
3. complete pilot readiness in 8 to 9 weeks overall;
4. run a controlled service test for 3 to 4 weeks within that period;
5. add the assignment-driven family mini-library;
6. collect teacher, family, content-operations, technical, and commercial evidence;
7. end with a GO, ITERATE, or STOP decision.

## Decision instrument

Each pilot decision applies the Tejal specificity pattern: client fact, baseline, action, target, owner, cost, and decision rule.

### Educator workflow

- Client fact: educators already use baby signs and Cleo coordinates the practice.
- Baseline: no measured digital assignment time or completion rate.
- Action: test the local assignment workflow with educators from all three Little Steps groups.
- Target: first assignment in 2 minutes or less, at least 80% without help, and at least 2 repeat assignments per group.
- Owner: product lead with the Little Steps pilot lead.
- Cost: included in user research and pilot coordination.
- Decision rule: ITERATE if time or completion misses while safety remains intact; STOP if the workflow cannot be made usable within the agreed pilot scope.

### Family value

- Client fact: families have asked for sign lists or materials.
- Baseline: no assignment-driven family library and no observed family access data.
- Action: deliver a reviewed mini-library linked to actual nursery assignments.
- Target: meet the signed family access, repeat-use, and clarity thresholds in the pilot measurement plan with no blocked or unreviewed delivery.
- Owner: product lead, nursery pilot lead, and privacy owner.
- Cost: included in workflow refinement, user research, and coordination.
- Decision rule: ITERATE if delivery works but engagement or clarity misses; STOP if safe, consented delivery cannot be operated.

### Content operations

- Client fact: Cleo currently carries quality and explanation responsibility.
- Baseline: repository review controls exist, but reviewer time and rework are unmeasured.
- Action: clear 3 to 5 pilot signs and record source, rights, review time, exceptions, and rework.
- Target: 100% provenance completeness, 100% exception rationale, and zero unreviewed or blocked deliveries.
- Owner: content operations lead and qualified reviewer.
- Cost: expert review and visual or content production are explicit pilot line items.
- Decision rule: ITERATE if the control works but burden is above target; STOP if rights or qualified review cannot be secured.

### Commercial validation

- Client fact: nursery schools and family training providers pay for adjacent offers.
- Baseline: zero observed KinderFlow paying centres, zero measured acquisition cost, and no retention history.
- Action: test EUR 600, EUR 1,200, and EUR 1,800 annual per-centre hypotheses with named budget owners.
- Target: at least 2 participating schools identify a budget owner and state credible paid-continuation intent at a specific tested price.
- Owner: Cleo as case sponsor and the commercial lead.
- Cost: included in user research and pilot coordination.
- Decision rule: GO only with credible paid-continuation evidence; ITERATE if value is supported but price or buyer process is unclear; STOP if no participating school can identify a viable paid path.

## Pilot gates

The pilot may start only when:

- scope is limited to 2 to 3 schools and 3 to 5 cleared signs;
- every sign has traceable source and rights status;
- a qualified reviewer and exception route are named;
- family delivery, consent, access, retention, and deletion procedures are approved;
- no child-video or child-scoring route exists in the pilot workflow;
- event definitions and baselines are documented;
- commercial interviews include a named budget owner and explicit price questions;
- production-like failure, rollback, and support procedures are rehearsed for the controlled service.

The pilot does not authorize a public production launch.

## Out of scope

The following remain outside the controlled pilot unless separately approved:

- child video analysis or child assessment;
- diagnostic, therapeutic, or educational decision automation;
- a national or international sign-language claim;
- an unrestricted user-upload marketplace;
- a broad production sign library;
- direct-to-family subscription billing;
- production multi-tenant scale;
- automated publication without qualified review;
- Kinder Daily and Kinder Food as active pilot products;
- replacement of nursery staff, specialists, or qualified reviewers.

## Final recommendation

PROCEED WITH CONDITIONS.

The current evidence is sufficient for a narrow, instrumented pilot, but not for production launch or an investment claim. The conditions are complete rights and review gates, an assignment-driven family mini-library, exact teacher and family measurement, explicit price testing, and zero breach of the stated hard boundaries.
