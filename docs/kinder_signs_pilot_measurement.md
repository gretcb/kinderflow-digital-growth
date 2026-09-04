# Kinder Signs Pilot Measurement Plan

Document status: final capstone reconciliation
Pilot length: 8 to 9 weeks total
Controlled service test: 3 to 4 weeks
Pilot scope: 2 to 3 nursery schools and 3 to 5 reviewed signs
Decision: GO, ITERATE, or STOP

## Measurement purpose

The pilot must determine whether Kinder Signs can operate as a safe, useful, and potentially paid nursery service.

It measures five perspectives:

1. Teacher use and workflow fit.
2. Family delivery and value.
3. Content review, rights, and reuse.
4. Technical reliability and data boundaries.
5. Buyer, price, and operating economics.

This is a small controlled pilot. Results are descriptive and decision-oriented. They must not be represented as causal proof, statistical market validation, or a production reliability guarantee.

## Product boundary

Current evidence:

- a local computer vision evidence path exists;
- a professional interpretation and explicit review status exist;
- a local nursery assignment flow exists;
- a family-facing guidance preview exists.

Required pilot iteration:

> A family-facing guidance prototype exists. A personalised assignment-driven family library remains a next product iteration.

The pilot must add and test a small assignment-driven family mini-library. It must not describe a static or session-based preview as a completed personalised delivery service.

The mini-library must:

- show only signs assigned to the relevant nursery group or authorised pilot family context;
- show reviewed family wording, source status, and correction state;
- prevent blocked or unreviewed content from appearing;
- support a minimal access, withdrawal, correction, and help route;
- record minimised delivery and access evidence;
- avoid child profiles, child scoring, and free-text family history.

## Measurement principles

- Define every metric before participant activity.
- Record numerator, denominator, exclusions, missing data, owner, and source.
- Keep product events separate from facilitator observations and interview evidence.
- Use synthetic or random identifiers where possible.
- Do not place names, contact details, child data, or open-ended family notes in model prompts or LangSmith traces.
- Report counts beside rates because the sample is small.
- Do not convert time release into financial savings without measured loaded cost and recoverability.
- Do not treat vendor prices as KinderFlow willingness to pay.
- Do not change thresholds after results are known without recording the change and reason.

## Evidence sources

### Product events

Use minimised events for:

- assignment task opened;
- assignment confirmed;
- assignment repeated;
- family item made available;
- family item first accessed;
- family item accessed again;
- review started;
- review decision recorded;
- correction published;
- withdrawal completed;
- runtime failure;
- fallback used;
- blocked-delivery attempt prevented.

### Structured observations

Use observation records for:

- facilitator help;
- educator error and recovery;
- workflow interruption;
- unclear wording;
- accessibility difficulty;
- support request;
- manual fallback;
- unexpected use.

### Content operations records

Use content records for:

- sign and asset identifier;
- source and rights basis;
- version;
- creation effort;
- provider or API cost;
- review effort;
- decision;
- exception rationale;
- rework effort;
- schools using the approved asset.

### Surveys and interviews

Use short consented instruments for:

- educator usefulness and fit;
- family clarity and usefulness;
- family questions and accessibility;
- owner value, budget, procurement, price, and continuation;
- reviewer burden and confidence.

Open-ended research notes must be stored outside model and tracing systems under the approved pilot research process.

## Identifier and event rules

Allowed identifiers:

- pilot school ID;
- nursery group ID;
- educator participant ID;
- family participant ID;
- sign ID;
- assignment ID;
- approved asset version;
- run or evidence ID.

Identifier rules:

- use random or synthetic values;
- keep the re-identification key, if required, under nursery or approved research control;
- do not encode names, dates of birth, diagnoses, contact details, or classroom notes;
- remove identifiers when their measurement purpose ends.

Minimum event fields:

- event name;
- event timestamp;
- pilot school ID;
- nursery group ID when relevant;
- participant-role ID when relevant;
- sign ID when relevant;
- assignment or review ID when relevant;
- status;
- duration when relevant;
- error or fallback category when relevant;
- evidence or asset version when relevant.

Prohibited event fields:

- child name or image;
- family name or contact detail;
- diagnosis or developmental judgement;
- free-text child notes;
- message content;
- raw model prompt containing participant data;
- authentication secret;
- exact location beyond the approved school identifier.

## Baseline capture

Baseline is collected before the controlled service test.

### Educator baseline

Capture:

- educator role and nursery group;
- current way of finding, explaining, and sharing a sign;
- time for one comparable current task, where observable;
- frequency of sign assignment or family explanation;
- help sources and interruptions;
- confidence with the current process.

Owner:

- research lead with nursery pilot lead.

### Family baseline

Capture:

- whether the family has previously requested or received sign material;
- current access route;
- known accessibility or language need relevant to the pilot;
- expected usefulness;
- valid participation, information, or consent status.

Owner:

- research lead and privacy owner.

### Content operations baseline

Capture:

- available reference;
- source and rights status;
- current wording;
- reviewer identity and qualification;
- current effort if a comparable manual review exists;
- unresolved variants or presentation issues.

Owner:

- content operations lead.

### Commercial baseline

Capture for every participating school:

- economic buyer;
- budget owner;
- present Baby Sign or family-communication spend if the school is willing to disclose it;
- procurement route;
- current alternative;
- initial response to EUR 600, EUR 1,200, and EUR 1,800 per centre per year.

Owner:

- commercial lead.

## Primary outcome metrics

### Outcome 1: Little Steps group activation

- Type: primary outcome.
- Definition: a nursery group has at least one completed assignment of an allowed sign during controlled service.
- Numerator: Little Steps groups with at least one completed assignment.
- Denominator: 3 Little Steps groups.
- Baseline: 0 of 3 in a real assignment-driven service.
- Target: 3 of 3 groups.
- Evidence: assignment event reconciled to the nursery activity log.
- Owner: nursery pilot lead.
- Cadence: daily during first-use week, then weekly.
- Decision use: required for GO.

For other participating nurseries, report activated groups and eligible groups separately. Do not merge them into the Little Steps 3 of 3 target.

### Outcome 2: repeat assignment

- Type: primary outcome.
- Definition: a completed assignment after the first completed assignment in the same Little Steps group.
- Numerator: qualifying repeat assignments.
- Denominator: each of the 3 Little Steps groups.
- Baseline: 0 measured.
- Target: at least 2 repeat assignments per group during the controlled service test.
- Evidence: assignment history.
- Owner: product lead and nursery pilot lead.
- Cadence: weekly.
- Decision use: required for GO.

Corrections to an existing assignment and duplicate event writes do not count as repeat assignments.

### Outcome 3: family access

- Type: primary outcome.
- Definition: an invited eligible pilot household opens at least one assigned family item after it is made available.
- Numerator: invited eligible households with at least one valid first-access event.
- Denominator: invited eligible households with a successfully made-available assignment.
- Baseline: 0 in an assignment-driven family service.
- Target: at least 60%.
- Evidence: family-item availability and first-access events.
- Owner: product lead, research lead, and privacy owner.
- Cadence: weekly.
- Decision use: required for GO; exact threshold is a pilot hypothesis to sign off before first activity.

Exclude only documented technical delivery failures from the access denominator, and report those failures separately.

### Outcome 4: family repeat use

- Type: primary outcome.
- Definition: a household with a first access returns on a different calendar day or accesses a second assigned sign.
- Numerator: accessing households with a qualifying repeat access.
- Denominator: households with at least one valid access.
- Baseline: 0 measured.
- Target: at least 40%.
- Evidence: minimised family-access events.
- Owner: product lead and research lead.
- Cadence: weekly.
- Decision use: required for GO; exact threshold is a pilot hypothesis to sign off before first activity.

### Outcome 5: paid-continuation intent

- Type: primary commercial outcome.
- Definition: a named budget owner selects a specific tested annual price, states willingness to continue at that price, and records material conditions or approval steps.
- Numerator: participating schools with credible paid-continuation intent.
- Denominator: participating schools that complete the end-of-pilot buyer interview.
- Baseline: 0 observed KinderFlow paying centres.
- Target: at least 2 participating schools, with buyer interviews completed for 100% of participating schools.
- Evidence: signed or recorded economic-buyer interview.
- Owner: commercial lead.
- Cadence: baseline and final week.
- Decision use: required for GO.

General interest, a free-pilot request, or a response without a named price does not count.

## Teacher driver metrics

### First-assignment time

- Type: workflow driver.
- Definition: seconds from opening the prepared assignment task to a confirmed assignment, excluding an externally caused interruption recorded by the observer.
- Numerator: total valid elapsed seconds.
- Denominator: valid observed first-assignment attempts.
- Baseline: not measured.
- Task target: 120 seconds or less.
- Programme target: at least 80% of valid first-assignment attempts meet the task target.
- Evidence: event timestamps and observation record.
- Owner: product lead and research lead.
- Cadence: every first-use session.
- Decision use: required for GO.

Report the median, range, count, and percentage meeting 120 seconds. Do not report only an average.

### Completion without help

- Type: workflow driver.
- Definition: educator confirms the first assignment without facilitator action, procedural instruction, or correction after the task begins.
- Numerator: valid first-assignment attempts completed without help.
- Denominator: all valid observed first-assignment attempts.
- Baseline: not measured.
- Target: at least 80%.
- Evidence: structured observation.
- Owner: research lead.
- Cadence: every first-use session.
- Decision use: required for GO.

An orientation completed before the timed task is not counted as help. Any prompt after the task starts is counted.

### Assignment error rate

- Type: diagnostic driver.
- Definition: valid assignment attempts containing wrong group, wrong sign, duplicate action, status confusion, or failed confirmation.
- Numerator: attempts with at least one defined error.
- Denominator: all observed assignment attempts.
- Baseline: not measured.
- Target: at most 10%.
- Evidence: event and observation reconciliation.
- Owner: product lead.
- Cadence: weekly.
- Decision use: supports GO or ITERATE; threshold is a pilot hypothesis.

### Nursery support burden

- Type: operating driver.
- Definition: product or process support time provided to a nursery, excluding scheduled research interviews and content-review work.
- Numerator: support minutes.
- Denominator: active school-weeks.
- Baseline: not measured.
- Target: median of 30 minutes or less per active school-week after onboarding.
- Evidence: support log.
- Owner: pilot manager.
- Cadence: weekly.
- Decision use: updates unit economics and can trigger ITERATE.

Onboarding is reported separately, with a target of 60 minutes or less per participating nursery.

## Family driver metrics

### Family delivery success

- Type: service driver.
- Definition: an intended reviewed family assignment becomes available through the approved pilot access route without error.
- Numerator: successfully made-available family assignments.
- Denominator: intended family assignments.
- Baseline: no real assignment-driven delivery.
- Target: at least 95%.
- Evidence: availability event plus delivery or access-route log.
- Owner: product lead.
- Cadence: daily and weekly.
- Decision use: required for GO; threshold is a pilot hypothesis.

Blocked and unreviewed items are not intended assignments and must never be made available. Attempts prevented by controls are recorded as guardrail evidence.

### Family clarity

- Type: experience driver.
- Definition: response of 4 or 5 on a 5-point statement that the assigned guidance was clear.
- Numerator: qualifying clarity responses.
- Denominator: valid clarity responses.
- Baseline: not measured.
- Target: at least 80%.
- Evidence: short family survey.
- Owner: research lead.
- Cadence: after first access and at pilot end.
- Decision use: required for GO; threshold is a pilot hypothesis.

### Family usefulness

- Type: experience driver.
- Definition: response of 4 or 5 on a 5-point statement that the assigned guidance was useful for understanding what the nursery was practising.
- Numerator: qualifying usefulness responses.
- Denominator: valid usefulness responses.
- Baseline: not measured.
- Target: at least 70%.
- Evidence: short family survey.
- Owner: research lead.
- Cadence: pilot end.
- Decision use: required for GO; threshold is a pilot hypothesis.

### Reported optional home use

- Type: experience driver.
- Definition: family respondent reports using at least one assigned sign at home during the controlled service test.
- Numerator: respondents reporting at least one use at home.
- Denominator: valid respondents who accessed an assigned item.
- Baseline: not measured.
- Target: at least 40%.
- Evidence: end-of-pilot family survey.
- Owner: research lead.
- Cadence: pilot end.
- Decision use: supports the family-value decision; threshold is a pilot hypothesis and is not a child outcome measure.

### Family response sufficiency

- Type: evidence-quality driver.
- Definition: completed family survey containing both clarity and usefulness items.
- Baseline: 0.
- Target: at least 10 valid family responses across at least 2 participating nurseries.
- Evidence: consented survey record.
- Owner: research lead.
- Cadence: weekly.
- Decision use: if not met, family conclusions remain inconclusive and the decision cannot be GO without an approved evidence exception.

This threshold supports a directional pilot assessment only. It does not create statistical representativeness.

### Family questions and accessibility

- Type: diagnostic driver.
- Definition: count and category of questions, confusion, access barriers, language barriers, and requested accommodations linked to an assigned item.
- Baseline: not measured.
- Target: 100% of reported issues categorised and assigned an owner within 1 working day.
- Evidence: minimised help and issue log.
- Owner: nursery pilot lead and product lead.
- Cadence: daily.
- Decision use: informs correction, accessibility scope, and ITERATE.

Do not store sensitive detail in the metric record. Keep necessary case handling under the nursery's approved process.

## Content operations metrics

### Provenance completeness

- Type: guardrail.
- Definition: pilot sign has source, rights basis, attribution requirement, reference version, evidence link, review decision, reviewer, and family-presentation status.
- Numerator: pilot signs with every required field.
- Denominator: all 3 to 5 pilot signs.
- Baseline: current repository lists are not approved production libraries.
- Target: 100%.
- Evidence: content registry and review record.
- Owner: content operations lead.
- Cadence: before service and after every change.
- Decision use: mandatory gate; any incomplete sign is excluded.

### Review exception rationale

- Type: guardrail.
- Definition: every override, exception, revision, or conditional approval records the decision, reason, owner, and version.
- Numerator: exceptions with complete rationale.
- Denominator: all review exceptions.
- Baseline: not measured in service.
- Target: 100%.
- Evidence: review record.
- Owner: qualified reviewer.
- Cadence: every decision.
- Decision use: mandatory gate.

If there are no exceptions, report zero exceptions and mark the rate not applicable rather than claiming 100% from an empty denominator.

### Review turnaround

- Type: operating driver.
- Definition: elapsed working time from a complete review package becoming available to an approve, revise, or block decision.
- Numerator: review packages decided within 2 working days.
- Denominator: complete review packages.
- Baseline: not measured.
- Target: at least 80% within 2 working days and 100% within 5 working days, excluding a documented external rights hold.
- Evidence: review timestamps.
- Owner: content operations lead and qualified reviewer.
- Cadence: per sign.
- Decision use: updates operating plan; miss can trigger ITERATE.

### Rework burden

- Type: operating driver.
- Definition: number of revision cycles and active rework time between first review and final approved or blocked status.
- Baseline: not measured.
- Target: at least 80% of approved pilot signs require no more than 1 revision cycle.
- Evidence: version and time records.
- Owner: content operations lead.
- Cadence: per sign.
- Decision use: updates content cost and reuse case; threshold is a pilot hypothesis.

### Reuse evidence

- Type: economic driver.
- Definition: the same approved asset version is used by more than one pilot nursery without new source creation, while any adaptation and review are recorded.
- Baseline: 0 observed multi-school reuse.
- Target: at least 2 approved sign assets used by at least 2 pilot nurseries.
- Evidence: asset-version and assignment records.
- Owner: content operations lead.
- Cadence: pilot end.
- Decision use: tests the reuse hypothesis; miss triggers cost-model revision.

Cost formula:

> Allocated content cost per school = (creation + API + review + rework) / schools using the approved asset

Every pilot sign must record creation, API, review, and rework separately. HUMAN mode may have EUR 0 provider API cost but still has staff and review cost.

### Content cost and throughput record

- Type: economic driver.
- Definition: complete active-time and direct-cost record for source preparation, processing, review, rework, and approval.
- Numerator: pilot signs with complete component records.
- Denominator: all pilot signs reaching a final approved or blocked decision.
- Baseline: not measured in service.
- Target: 100%.
- Evidence: content operations and cost logs.
- Owner: content operations lead.
- Cadence: per sign.
- Decision use: calculates time per sign, reviewer time, candidates per approved visual, rework rate, and cost per approved sign.

## Technical metrics

### Pilot-sign evidence readiness

- Type: readiness gate.
- Definition: sign candidate has a traceable run or documented manual fallback, evidence package, version, status, and reviewer route.
- Numerator: ready pilot sign candidates.
- Denominator: selected pilot sign candidates.
- Baseline: technical examples exist, but pilot set is not cleared.
- Target: 100%.
- Evidence: run manifest, evidence package, fallback record, and content registry.
- Owner: technical lead.
- Cadence: before service and after any version change.
- Decision use: mandatory gate.

### Runtime completion

- Type: technical driver.
- Definition: planned processing run reaches a terminal reviewable or documented failed state and writes its required evidence.
- Numerator: planned runs reaching a traceable terminal state.
- Denominator: planned processing runs.
- Baseline: local development evidence only.
- Target: 100%; failed runs may count only when failure is explicit, evidence is preserved, and manual fallback is invoked before use.
- Evidence: run manifest and operations log.
- Owner: technical lead.
- Cadence: every run.
- Decision use: unresolved or silent failure blocks the affected sign.

### Assignment evidence reconciliation

- Type: data-quality driver.
- Definition: sampled assignment and family-availability events match the approved manual activity record.
- Numerator: sampled records with complete agreement.
- Denominator: sampled records.
- Baseline: not measured.
- Target: at least 95% agreement, with 100% of discrepancies investigated.
- Evidence: weekly reconciliation.
- Owner: evaluation owner.
- Cadence: weekly.
- Decision use: miss triggers instrumentation correction and may make affected metrics inconclusive.

### Technical diagnostic rates

- Type: technical drivers.
- Successful processing rate: reviewable processing passes divided by planned processing runs; target at least 90%.
- Review-recommended or fail rate: review-recommended plus failed runs divided by planned runs; target is 100% explicit classification and investigation, not an artificially low status count.
- Repeated processing: process at least 2 pilot references twice under frozen configuration and record any material status or evidence variance.
- Preview availability: successful professional or family preview checks divided by planned checks; target at least 95%.
- Fallback rate: runs requiring manual or HUMAN fallback divided by planned runs; target at most 10%, with 100% of fallback outcomes recorded.
- Baseline: local development evidence only.
- Evidence: run manifest, status record, availability check, and operations log.
- Owner: technical lead and evaluation owner.
- Cadence: per run and weekly.
- Decision use: supports reliability and operating-cost decisions; silent failure blocks the affected sign.

## Commercial and economic metrics

### Price response

- Type: commercial driver.
- Definition: buyer response to each annual per-centre hypothesis, including value rationale, budget source, conditions, and approval route.
- Price points: EUR 600, EUR 1,200, and EUR 1,800.
- Baseline: no observed KinderFlow willingness to pay.
- Target: all participating economic buyers respond to all three price points.
- Evidence: structured buyer interview.
- Owner: commercial lead.
- Cadence: baseline and final week.
- Decision use: supports the paid-continuation outcome.

The interview also records preference for monthly or annual contracting and every material procurement condition.

### Time release

- Type: nursery-value driver.
- Definition: comparable monthly minutes no longer required for repeated coordination, sign-material preparation, or explanation, net of new KinderFlow tasks.
- Baseline hypothesis: Cleo 6 to 8 hours per month, classroom 5 to 7 hours per month, combined central case 13 hours per month.
- Target: measure actual baseline and change; no financial pass threshold is set.
- Evidence: task diary, observation, and end-of-pilot interview.
- Owner: research lead.
- Cadence: baseline, weekly diary, and final week.
- Decision use: informs value narrative only until loaded cost and recoverability are known.

Do not report the 30%, 40%, or 50% calculated scenarios as observed time release.

### Acquisition-cost inputs

- Type: provider-economic driver.
- Definition: founder and sales labour, demonstrations, travel, onboarding, and pilot conversion effort by prospect.
- Baseline: no measured CAC.
- Target: record 100% of in-scope acquisition effort and direct expense for participating schools.
- Evidence: time and expense log.
- Owner: commercial lead.
- Cadence: weekly.
- Decision use: enables a preliminary CAC calculation.

Formula:

> CAC = (sales labour + demonstrations + travel + onboarding) / new paying centres

If there are no new paying centres, report CAC as not yet calculable rather than EUR 0.

### Lifetime-value inputs

- Type: provider-economic driver.
- Definition: annual price, variable service cost, support cost, and stated retention or renewal evidence.
- Baseline: no measured retention or LTV.
- Target: capture price and variable-cost inputs; do not calculate observed LTV until paid retention exists.
- Evidence: buyer interview, cost log, and future renewal record.
- Owner: commercial lead and finance owner.
- Cadence: final week and future renewal.
- Decision use: prevents an unsupported CAC to LTV claim.

Formula:

> LTV = annual contribution per centre x expected retained years - incremental support cost

### Understanding of AI and human review

- Type: trust driver.
- Definition: participant correctly identifies that computer vision creates evidence, language-model output is a draft where used, and a human reviewer controls approval.
- Numerator: valid educator and owner responses containing all three elements.
- Denominator: valid responses.
- Baseline: not measured.
- Target: at least 80%.
- Evidence: short end-of-pilot comprehension check.
- Owner: research lead and governance owner.
- Cadence: after onboarding and at pilot end.
- Decision use: misunderstanding triggers revised disclosure and ITERATE; unsafe reliance triggers pause.

## Hard guardrails

The following targets are absolute:

- child video processed: 0;
- child scoring: 0;
- automated educational decisions: 0;
- unreviewed content delivered: 0;
- blocked content delivered: 0;
- personal child or family data sent to a language model or LangSmith: 0;
- pilot sign provenance complete: 100%;
- review exceptions with rationale: 100%;
- critical content, privacy, rights, or safeguarding incidents: 0.

Any suspected breach is reported immediately, affected processing or delivery is paused, evidence is preserved, and the incident owner decides containment and participant communication.

## Pilot cadence

### Before service

- approve scope, owners, definitions, and thresholds;
- complete baseline capture;
- clear 3 to 5 signs;
- rehearse assignment, access, correction, withdrawal, failure, and incident paths;
- confirm that instrumentation contains no prohibited data;
- freeze the measurement specification.

### Daily during first-use periods

- reconcile assignment and family-availability events;
- review help, failure, blocked-attempt, and incident records;
- respond to family access or clarity issues;
- check that only approved versions are available.

### Weekly

- teacher activation and repeat-use readout;
- family delivery, access, repeat-use, and response readout;
- content review, rework, and reuse readout;
- runtime, fallback, and data-quality readout;
- support and acquisition-effort readout;
- guardrail review;
- action owner and due date for each variance.

### End of pilot

- close buyer interviews at explicit prices;
- reconcile all metric denominators and exclusions;
- calculate validation cost and preliminary recurring inputs;
- report sample limits and missing data;
- compare results with GO, ITERATE, and STOP rules;
- issue a signed decision record.

## Decision hierarchy

Decisions are made in this order:

1. Hard guardrails.
2. Evidence completeness and data quality.
3. Teacher workflow and repeat use.
4. Family delivery and value.
5. Content-review and operating burden.
6. Paid-continuation evidence.
7. Updated economics and production scope.

A commercial signal cannot offset a safety, privacy, rights, or review failure.

## GO rule

Choose GO only when all of the following hold:

- every hard guardrail target is met;
- Little Steps activation is 3 of 3 groups;
- each Little Steps group records at least 2 repeat assignments;
- at least 80% of valid first assignments finish in 120 seconds or less;
- at least 80% of valid first assignments complete without help;
- family delivery success is at least 95%;
- family access is at least 60%;
- family repeat use is at least 40%;
- family clarity is at least 80% and usefulness at least 70%;
- at least 10 valid family responses represent at least 2 nurseries;
- review, rework, support, and data-quality targets are met or have a documented low-risk variance accepted by the decision owner;
- at least 2 participating schools identify a budget owner and state credible paid-continuation intent at a specific tested price;
- production build, privacy, security, support, and content-operation work is scoped before the next investment approval.

GO means scope the next phase. It does not mean public launch.

## ITERATE rule

Choose ITERATE when:

- every hard guardrail holds;
- evidence is sufficient to locate the gap;
- there is material teacher, family, or buyer value;
- one or more non-guardrail targets miss;
- a bounded correction has a named owner, cost, metric, and decision date.

Examples include:

- assignment requires too much help but repeat use is strong;
- safe family delivery works but access or clarity is below target;
- schools value the service but price or procurement needs revised packaging;
- review works but turnaround, rework, or support burden exceeds target;
- instrumentation is incomplete but underlying safe operation is evidenced manually.

Do not extend an iteration indefinitely or change the original threshold without retaining both the original and revised decision record.

## STOP rule

Choose STOP, or stop the affected scope, when:

- any child-video, child-scoring, or automated-decision boundary is introduced;
- personal child or family data is sent to a model provider or LangSmith;
- blocked or unreviewed content reaches a family;
- sign rights, provenance, or qualified review cannot be secured;
- a critical privacy, rights, content, or safeguarding incident cannot be fully contained;
- educator workflow remains unusable after a bounded correction;
- family guidance remains unclear or unsafe after a bounded correction;
- no participating school identifies a credible paid path;
- review, content, support, or production economics remain incompatible with tested pricing.

## Reporting template

The final pilot report must include:

- metric name and version;
- target;
- numerator and denominator;
- result;
- baseline;
- evidence source;
- exclusions and missing data;
- variance reason;
- owner response;
- cost effect;
- decision effect;
- confidence;
- GO, ITERATE, or STOP status.

The report must separate observed results from calculated scenarios and future estimates.
