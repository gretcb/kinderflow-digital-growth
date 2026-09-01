# Round 1 Decision — Kinder Signs

## Feedback summary

Round 1 was reviewed with teaching staff and all mandatory deliverables were confirmed as covered.

The strongest feedback was to **continue with Kinder Signs and move from a well-developed static concept to a small working MVP**.

Key feedback:

* Keep Kinder Signs as the selected use case.
* The market framing, use case, dashboard, POC, business concept and static prototype are sufficiently developed to continue into Round 2.
* The priority is no longer additional concept development; it is proving the technically differentiating capability in a working MVP.
* The MVP should make the video upload and Computer Vision pipeline dynamic:
  validated reference video → MediaPipe → landmarks / skeleton → technical metrics.
* Human review must remain part of the workflow before a sign is published.
* The project should prioritise a small, reliable MVP rather than adding many production features.
* Computer Vision was identified as a distinctive aspect of the project compared with more common text-based AI capstones.
* A mid-project technical review with Isabella was recommended because of the Computer Vision complexity.
* The final MVP, documentation and presentation should be completed by Thursday evening; Friday should be treated as presentation time rather than additional build time.

No feedback suggested that the sector or selected use case should be changed.

## Decision

**KEEP — Kinder Signs**

Kinder Signs remains the first commercial validation use case for KinderFlow.

The initial market remains early-childhood education in Spain, with Madrid as the starting geographical focus.

The school-led B2B / B2B2C model also remains unchanged:

* nursery schools / school groups are the primary paying customers;
* educators operate the school-facing workflow;
* families are users and beneficiaries;
* children are beneficiaries and require particular privacy and safeguarding consideration.

The commercial proposition remains centred on school-home continuity rather than selling individual pieces of content directly to families.

## Why

Round 1 provided enough evidence to deepen the use case rather than pivot.

The problem is not a lack of Baby Sign resources. Free and paid resources already exist.

The opportunity identified is the lack of structured continuity between what an educator uses at nursery school and what the family can repeat at home.

Kinder Signs addresses this through a school-managed Signs & Flashcards Library:

educator selects the sign used that week
→ assigns it to a group or individual child
→ family receives the matching guidance and materials
→ the same communication cue can be repeated across school and home.

The school therefore acts as the trusted distribution and coordination layer.

The commercial model still requires validation through a real pilot. Round 1 supports continuing the concept; it does not prove willingness-to-pay, adoption or retention.

## Technical decision

The technical approach also remains appropriate.

Earlier generative-video experiments showed that general-purpose generative AI could produce unreliable signing motion, including problems with:

* finger configuration;
* hand orientation;
* hand position;
* bilateral movement;
* timing and movement consistency.

For that reason, Kinder Signs should not rely on generative video to invent or reproduce the underlying sign movement.

The current architecture uses Computer Vision to extract and represent movement from a validated reference video.

The product principle is:

**The character defines the look. The validated reference movement defines the sign.**

The intended content-production workflow is:

Approved sign video
→ Movement check
→ Movement data / skeleton
→ Visual layer
→ Avatar build / preview
→ Human review
→ Published in the Signs & Flashcards Library

Final production-ready avatar generation is not part of the current MVP and should not be presented as completed.

## Child-video decision

Child video has intentionally been removed from the core Kinder Signs workflow.

It is not necessary to solve the main business problem and would introduce additional:

* privacy risk;
* data-retention requirements;
* security exposure;
* operational complexity;
* regulatory complexity.

The core Computer Vision use case is therefore **content production from validated reference material**, not automated analysis of a child's signing performance.

The current MVP will not:

* assess whether a child signs correctly;
* score a child's performance;
* infer developmental ability;
* analyse emotion;
* make educational decisions about a child.

Any future child-video capability would require a separate product, necessity, privacy and regulatory assessment.

## Round 1 → Round 2 evolution

Round 1 established:

* sector and market context;
* opportunities and risks;
* three potential use cases;
* selection of Kinder Signs as the first validation wedge;
* public dataset and stakeholder dashboard;
* low-code POC;
* LangSmith monitoring sample;
* cost and timeline assumptions;
* initial commercial model;
* static product prototype;
* initial Computer Vision feasibility evidence.

Round 2 moves from **concept validation to functional validation**.

The main question becomes:

> Can the technically differentiating part of Kinder Signs run reliably enough to support a credible pilot?

## POC evolution

The Round 1 POC demonstrated an AI-assisted content workflow and monitoring approach.

Round 2 must make the separation between AI capabilities explicit:

### Computer Vision

Used for:

* processing a validated reference sign video;
* detecting hand / pose landmarks;
* creating a movement / skeleton representation;
* producing technical processing metrics.

It does **not** certify linguistic sign correctness.

### LLM / content pipeline

Used for:

* structured family guidance;
* contextual Tips & Tricks;
* support content associated with a published sign.

### LangSmith

Used to:

* observe and monitor the LLM/content-generation pipeline;
* make prompts, outputs and failures more transparent.

LangSmith does **not** validate biomechanical or linguistic sign correctness.

### Human review

Remains the final control before content is published in the library.

## Core MVP capability

The smallest MVP that still proves the differentiating technical use case is:

Validated reference sign video
→ video upload
→ MediaPipe processing
→ hand / pose landmarks
→ skeleton / movement preview
→ technical metrics
→ review-ready result

Example technical outputs may include:

* frames analysed;
* pose detection rate;
* hand detection rate;
* processing status;
* technical warning / proceed status.

These are technical processing signals, not automated sign-language certification.

## Secondary MVP capability

If the core Computer Vision pipeline is stable, Round 2 will add a second small functional capability that connects the technical system to family value:

Published sign
→ family sign card
→ short guidance
→ Tips & Tricks
→ printable flashcard
→ Print / PDF-friendly output

This demonstrates how a validated library item becomes a practical school-home resource.

It is secondary to the Computer Vision MVP and must not jeopardise completion of the core capability.

## MVP scope limits

The current MVP will not include:

* real payments;
* production billing;
* login or authentication;
* production APIs;
* database implementation;
* cloud upload;
* real school integrations;
* real child data;
* child-video analysis;
* automatic sign correctness certification;
* automated developmental assessment;
* autonomous publishing without human review;
* production-ready avatar generation.

The school also does not create, upload or validate reference sign videos.

Kinder Signs creates and manages the validated Signs & Flashcards Library. Educators select existing published material for use with their groups or families.

## Highest-risk Round 2 areas

The main Round 2 risks are:

1. **MVP reliability**
   The Computer Vision workflow must actually run from video input to visible landmarks / skeleton and metrics.

2. **Scope expansion**
   Additional product features must not prevent completion of the core MVP.

3. **Technical claims**
   Detection metrics must not be presented as automatic validation of sign-language correctness.

4. **Privacy and child-data governance**
   The architecture should continue to minimise child data and avoid unnecessary child-video processing.

5. **EU AI Act / GDPR classification and obligations**
   Compliance conclusions must be evidence-based and distinguish the current MVP from potential future production functionality.

6. **Commercial assumptions**
   Adoption, willingness-to-pay, pricing and retention remain hypotheses that must be tested during the pilot.

7. **Movement fidelity and content governance**
   Human review and validated source material remain necessary before publication.

## Round 2 priorities

1. Build a small working MVP with reliable video upload and MediaPipe processing.
2. Display landmarks / skeleton and understandable technical metrics.
3. Keep human review explicit in the content-production workflow.
4. Add the printable family card only after the core Computer Vision capability is stable.
5. Strengthen and document the existing POC.
6. Create reproducible MVP and POC documentation.
7. Build a realistic ROI model with explicit 12- and 36-month assumptions and break-even.
8. Develop a risk matrix covering technical, regulatory, ethical, privacy, operational and commercial risks.
9. Complete EU AI Act and GDPR assessments using existing research and conservative claims.
10. Define an explicit POC → pilot → deployment strategy with measurable go / iterate / stop criteria.
11. Validate adoption, workflow, engagement, trust and willingness-to-pay during an approximately 8–9 week commercial pilot.
12. Prepare a concise final presentation centred on business value, working technical evidence, risk, compliance and the next commercial decision.

## Round 2 decision question

Round 2 is not intended to prove that Kinder Signs is ready for full deployment.

It is intended to provide enough technical, business, regulatory and user evidence for a client to make a credible decision:

**Proceed to pilot, iterate before pilot, or stop.**