# KinderFlow — EU AI Act Preliminary Internal Assessment

**Project:** KinderFlow — Early Childhood Digital Growth  
**Use case assessed:** Kinder Signs  
**Assessment date:** 2 September 2026  
**Assessment scope:** Current local MVP, proposed controlled pilot, and foreseeable production deployment  
**Regulatory basis:** Regulation (EU) 2024/1689 (Artificial Intelligence Act), consolidated version current in 2026

> This document is a capstone compliance assessment, not formal legal advice. Final production classification and contractual roles should be confirmed before a real-school deployment.

---

# 1. Executive takeaway

## Executive question

**How should Kinder Signs be classified under the EU AI Act, and what must KinderFlow do before a controlled pilot?**

## Current conclusion

**Preliminary internal assessment: the current intended use does not appear to match the Annex III high-risk education uses.**

Kinder Signs operates in an educational context, but the current system does not perform the education functions listed as high-risk in Annex III. It does not determine access or admission to education, evaluate learning outcomes, decide educational level, or monitor prohibited behaviour during tests.

The current product also does not perform emotion recognition, biometric identification, biometric categorisation, child scoring, developmental assessment or automated educational decision-making.

This working conclusion depends on the **intended purpose remaining narrow**. Final classification should be confirmed against the actual pilot design and deployment roles before launch.

If KinderFlow later adds child-performance assessment, developmental scoring, emotion inference, educational placement or other decision-making functions, the classification must be reassessed before those features are deployed.

## Pilot recommendation

**PROCEED WITH CONDITIONS**

Before a real-school pilot, KinderFlow should:

1. document the intended purpose and excluded uses;
2. formalise provider/deployer roles;
3. implement role-appropriate AI literacy;
4. complete the GDPR pilot assessment;
5. preserve human review and content-governance controls;
6. confirm which Article 50 transparency duties apply to any live AI-generated content;
7. maintain technical documentation and change-control records;
8. reassess classification if the pilot scope changes.

---

# 2. Why this matters for KinderFlow

KinderFlow works with nursery schools and supports content used around very young children.

That does **not automatically make every AI component high-risk**, but the context requires careful boundaries.

The most important regulatory design choice is therefore not simply choosing a risk label.

It is making sure KinderFlow does not quietly evolve from:

> content production and school-home support

into:

> automated assessment or decision-making about children.

The current architecture already reduces this risk by keeping child video, child scoring and developmental assessment outside the core product.

---

# 3. System assessed

## 3.1 KinderFlow platform

KinderFlow is the wider platform.

The current capstone develops **Kinder Signs** as the first product.

Other roadmap concepts, such as Kinder Daily and Kinder Food, are outside this classification unless they later introduce their own AI functionality.

---

## 3.2 Current Kinder Signs AI components

### A. Computer Vision / MediaPipe

Current function:

```text
Validated adult reference video
→ MediaPipe processing
→ pose / hand landmarks
→ normalization
→ movement diagnostics
→ landmark / skeleton preview
→ technical result
→ human review
```

The current MVP can process real MP4 input and generate run-specific movement evidence.

The Computer Vision component does **not**:

- identify the person in the video;
- classify sensitive traits;
- infer emotion;
- assess a child;
- determine linguistic sign correctness;
- make an educational decision.

The current MVP documentation explicitly separates technical movement evidence from sign correctness.

---

### B. Content Engine

The current content layer supports:

- stored human wording;
- LLM-assisted wording where configured;
- strict structured input/output contracts;
- deterministic quality checks;
- review states;
- human approval;
- dry-run / live-mode distinction.

Generated content cannot autonomously publish itself.

---

### C. LangSmith / observability

LangSmith is relevant only to the LLM-assisted content-transformation layer.

It does not evaluate:

- MediaPipe performance;
- movement correctness;
- sign-language correctness;
- child development.

The current repository distinguishes LIVE, DRY_RUN and NOT_APPLICABLE states. DRY_RUN is evidenced, and NOT_APPLICABLE is used for human-only content. Provider-path tests exist, but real external LIVE LLM execution and a LIVE LangSmith trace/evaluation are not evidenced.

A recorded trace would show observability evidence; it would not by itself prove that an evaluation was completed or that content was approved.

---

### D. Flashcard Studio

Flashcard Studio uses deterministic templates.

It does not require Generative AI for layout.

This is relevant to the AI Act assessment because not every KinderFlow function is an AI system or AI-driven decision.

---

# 4. Does Kinder Signs contain an “AI system”?

## Assessment

**YES — the broader Kinder Signs solution contains AI-system components.**

The AI Act defines an AI system as a machine-based system that operates with varying levels of autonomy and infers from input how to generate outputs such as predictions, content, recommendations or decisions.

Kinder Signs currently includes:

- machine-learning-based Computer Vision for pose/hand landmark extraction; and
- an optional LLM-assisted content-generation component.

The deterministic Flashcard renderer, static school assignment interface and ordinary rule-based checks should not be treated as separate AI systems merely because they are part of the same product.

## What this means for KinderFlow

Compliance should be based on the **specific AI functions and intended purpose**, not on describing the whole platform as “AI” without distinction.

---

# 5. Operator-role assessment

The final contractual allocation must be confirmed before a live pilot.

## Working role assumption: KinderFlow

**Likely provider, subject to the final system and placing-on-the-market model**

The AI Act defines a provider as the entity that develops, or has developed, an AI system and places it on the market or puts it into service under its own name or trademark.

If KinderFlow supplies Kinder Signs to schools under the KinderFlow name, KinderFlow is likely to act as the provider of the Kinder Signs AI system.

Where KinderFlow integrates a third-party general-purpose model, the original model provider remains responsible for its own GPAI-model obligations, while KinderFlow remains responsible for how its downstream system is designed and used.

---

## Working role assumption: nursery school / school group

**Role requires feature-level and contractual confirmation**

A school operating an AI-enabled Kinder Signs function professionally under its authority may act as a deployer. A school that only receives reviewed static content may instead be a customer or recipient of the service rather than a deployer of KinderFlow's internal AI system. The role must be assessed per feature and contract before pilot launch.

The exact role should be confirmed in the pilot agreement because the school currently interacts mainly with reviewed content rather than the internal CV/content-production pipeline.

---

## Families

Families are primarily recipients/users of the resulting content in the current design.

They do not operate the internal AI system.

---

# 6. Prohibited-practices audit — Article 5

| Article 5 area | Kinder Signs current use | Status | Reason |
|---|---|---|---|
| Subliminal/manipulative techniques causing significant harm | Not intended | **Evidence present** | Product provides school-linked content; no hidden behavioural manipulation feature is designed |
| Exploitation of vulnerability due to age/disability causing significant harm | Not intended | **Pilot control required** | Children are a vulnerable population; design and marketing must avoid manipulative or harmful use |
| Social scoring | Not used | **Not present in current scope** | No social score or cross-context treatment |
| Criminal-risk prediction | Not used | **Not applicable to current scope** | Outside product purpose |
| Untargeted facial-image scraping | Not used | **Not applicable to current scope** | No facial database creation |
| Emotion recognition in education | Not used | **Hard boundary** | No emotion inference is included |
| Sensitive biometric categorisation | Not used | **Not present in current scope** | No sensitive-trait inference |
| Prohibited biometric identification use | Not used | **Not present in current scope** | MediaPipe movement extraction is not person identification |

## Key control

**Emotion recognition must remain out of scope.**

The AI Act prohibits emotion-recognition systems in education institutions except for narrow medical or safety reasons.

KinderFlow should therefore treat any future “emotion”, “engagement from facial expression” or similar feature as a regulatory red flag requiring a new legal assessment before development.

---

# 7. High-risk classification — Article 6 and Annex III

## 7.1 Annex I product-safety route

Kinder Signs is not currently:

- a safety component of a product regulated under the Annex I product-safety legislation; or
- itself a regulated product that requires third-party conformity assessment under that route.

**Preliminary internal view: the Article 6(1) high-risk route does not appear to apply to the current described scope. Legal confirmation remains required for the final pilot design.**

---

## 7.2 Annex III — education and vocational training

Annex III identifies specific educational AI uses as high-risk.

### A. Access, admission or assignment to educational institutions

Kinder Signs does not decide:

- whether a child may access a nursery;
- admission;
- placement in an educational institution.

**NOT APPLICABLE**

---

### B. Evaluation of learning outcomes

Kinder Signs does not:

- grade children;
- score sign performance;
- assess learning outcomes;
- use AI output to steer a child's educational process.

**NOT APPLICABLE**

---

### C. Assessment of the appropriate level of education

Kinder Signs does not decide:

- educational level;
- programme placement;
- educational pathway;
- eligibility for a particular level of education.

**NOT APPLICABLE**

---

### D. Monitoring prohibited behaviour during tests

Kinder Signs is not an exam-proctoring or behaviour-monitoring system.

**NOT APPLICABLE**

---

## 7.3 Education-sector conclusion

**Kinder Signs is not high-risk merely because it is used around nursery schools.**

The high-risk education category applies to the specific decision-making and assessment purposes listed in Annex III.

Kinder Signs currently performs content production, movement representation and school-home content distribution support.

It does not perform the listed high-risk educational decisions.

### Preliminary internal classification

**The current intended use does not appear to match the Annex III high-risk education uses. Final classification remains subject to the actual pilot design and deployment roles.**

---

# 8. Biometric-risk screening

MediaPipe processes hand and pose landmarks from a validated adult reference video.

The current use does not seek to establish or verify identity.

It also does not infer:

- race;
- political beliefs;
- religion;
- trade-union membership;
- sex life;
- sexual orientation;
- emotion.

The movement representation should therefore not be described as biometric identification or sensitive biometric categorisation merely because body landmarks are processed.

## Control

The intended purpose must remain documented as:

> movement extraction and representation from validated reference content.

If future functionality identifies people, profiles children, infers traits or analyses emotion, a new classification is required.

---

# 9. Transparency obligations — Article 50

Article 50 became particularly relevant from August 2026 for certain AI interactions and synthetic content.

KinderFlow should assess transparency at the level of each feature.

---

## 9.1 Direct interaction with AI

### Current product

Families and educators do not currently interact directly with a chatbot or autonomous AI assistant.

They receive reviewed content through the product interface.

**Current assessment: Article 50(1) chatbot-style disclosure is not triggered by the existing family experience.**

### Future change trigger

If KinderFlow introduces:

- an AI tutor;
- conversational assistant;
- chatbot;
- autonomous family coach;

the user must be informed that they are interacting with AI where Article 50 applies.

---

## 9.2 AI-generated content marking

The live LLM-assisted content path can generate text.

Article 50 includes technical transparency requirements for providers of systems generating synthetic text or other synthetic content.

### Current position

The local MVP distinguishes:

- HUMAN;
- LLM_ASSISTED;
- LIVE;
- DRY_RUN;
- NOT_APPLICABLE.

This is good internal provenance.

### Required action before live pilot

**REVIEW REQUIRED**

Before live LLM-assisted content is distributed, KinderFlow should confirm:

- whether KinderFlow is itself the relevant Article 50 provider for the generated output;
- what machine-readable marking is supplied by the upstream model provider;
- what additional marking KinderFlow must preserve or add;
- whether the human-review/editorial-control exception for certain published text is relevant to the specific content.

Do not assume that human review automatically removes all Article 50(2) technical-marking duties.

---

## 9.3 Public-interest text

Kinder Signs family guidance is not currently designed as text published to inform the general public about matters of public interest.

The Article 50 rule for AI-generated text published for that purpose is therefore not the core current use case.

Human review and editorial responsibility should nevertheless remain documented.

---

# 10. AI literacy — Article 4

AI literacy obligations already apply.

KinderFlow and relevant deployers must take measures to support appropriate AI literacy for staff and people operating AI systems on their behalf.

## KinderFlow staff should understand

- what MediaPipe metrics mean;
- what they do **not** mean;
- why hand-detection coverage is not sign accuracy;
- when human review is required;
- the difference between deterministic checks and semantic correctness;
- LIVE vs DRY_RUN LLM mode;
- LangSmith's actual scope;
- escalation and incident procedures.

## School staff should understand

At a minimum:

- KinderFlow centrally creates/reviews AI-supported content;
- educators do not validate the sign with AI;
- AI outputs do not assess the child;
- available school content should be used only for its intended purpose;
- unexpected or inappropriate content should be reported.

## Pilot action

Create a short role-based AI literacy briefing and retain evidence that it was delivered.

---

# 11. Human oversight

Human oversight is already a core KinderFlow design principle.

## Current controls

- Computer Vision produces technical status, not publication.
- `Pass` allows human approval.
- `Review needed` requires a human decision.
- `Fail` cannot be approved through the normal route.
- Generated family content requires review.
- Deterministic PASS does not equal publication.
- LangSmith evidence does not equal approval.

## Gap

Current approval is local/prototype behavior.

Before production, KinderFlow requires:

- reviewer role definition;
- reviewer competence requirements;
- versioned review criteria;
- reviewer identity;
- timestamp;
- change history;
- escalation route;
- audit evidence.

---

# 12. General AI Act controls recommended for the pilot

Even though the current system is not classified as high-risk, KinderFlow should voluntarily adopt several high-risk-style controls because the product operates in an early-childhood setting.

| Control | Current MVP | Pilot action |
|---|---|---|
| Intended-purpose documentation | Partial | Formalise and version |
| Risk management | Partial | Maintain pilot risk register |
| Data / input provenance | Partial | Record all reference sources |
| Technical documentation | Strong base | Consolidate |
| Logging / traceability | Local runs | Define pilot logging |
| Human oversight | Built into logic | Formalise reviewer role |
| Technical performance / robustness (AI Act terminology) | Coverage and motion diagnostics; not sign accuracy | Define pilot thresholds |
| Cybersecurity | Local only | Pilot security controls required |
| Change management | Git/versioning | Formal release process |
| Incident reporting | Not formal | Define process before pilot |

This is a voluntary governance decision for the current classification, not a claim that all Chapter III high-risk obligations legally apply.

---

# 13. Current applicability timeline

As of this assessment date:

- prohibited-practice rules and AI literacy obligations are already applicable;
- general-purpose AI governance obligations have already entered into application;
- new Article 50 transparency requirements are in application from August 2026;
- the amended enforcement timetable places Annex III high-risk-system rules from **2 December 2027**.

The timing does not remove the need to classify KinderFlow correctly today.

A pilot started before the Annex III high-risk date should still be designed so that a future feature change does not create a compliance cliff.

---

# 14. Change triggers requiring reclassification

The current non-high-risk conclusion is conditional.

Reassess immediately if KinderFlow adds any of the following:

## Child performance analysis

Examples:

- “Is the child signing correctly?”
- performance score;
- ranking;
- progression score.

---

## Educational assessment

Examples:

- learning-outcome evaluation;
- readiness assessment;
- programme placement;
- educational-level recommendation.

---

## Emotion recognition

Examples:

- detecting engagement, frustration, happiness or anxiety from face/voice in an educational setting.

This is particularly sensitive because emotion recognition in education is prohibited except in narrow medical/safety cases.

---

## Biometric identification or sensitive categorisation

Any identity or sensitive-trait inference requires separate assessment.

---

## Automated decisions affecting access or treatment

If AI output begins materially affecting:

- admission;
- access;
- placement;
- educational opportunities;
- services provided to a child;

the classification must be revisited.

---

# 15. Provider / deployer action matrix

This is a provisional planning matrix. School-column duties apply only where the final feature-level assessment and contract establish that the school is a deployer, rather than only a customer receiving reviewed static content.

| Action | KinderFlow | School | Pilot timing |
|---|---|---|---|
| Define intended purpose | Lead | Acknowledge | Before pilot |
| Define prohibited uses | Lead | Follow | Before pilot |
| AI literacy | Internal team | Role-appropriate staff | Before / at onboarding |
| Reference-content provenance | Lead | N/A | Before pilot |
| Human-review process | Lead | Report issues | Before pilot |
| Technical documentation | Lead | Receive relevant instructions | Before pilot |
| AI transparency assessment | Lead | Apply school-facing notices if needed | Before pilot |
| Monitor intended use | Lead | Use within scope | During pilot |
| Report incidents/issues | Receive / investigate | Report | During pilot |
| Reclassification trigger | Lead | Notify use-case change | Continuous |

---

# 16. Gap analysis

| Check | Status | Evidence | Gap | Required action |
|---|---|---|---|---|
| AI system inventory | **Partial evidence** | CV + LLM components documented | Final inventory should be versioned | Add to technical documentation |
| Intended purpose | **Evidence present** | Product docs and MVP boundaries | Cross-document reconciliation required | Maintain one versioned statement |
| Prohibited-practice screening | **Preliminary internal screening** | Current feature set | Must prevent future scope creep | Add prohibited-use list and obtain legal confirmation |
| Annex III education screening | **Preliminary internal screening** | No admission/scoring/assessment/proctoring | Final pilot design may alter the analysis | Legal confirmation and change-control trigger |
| Biometric screening | **Preliminary internal screening** | Adult movement landmarks only | Future identity/trait features would change assessment | Maintain boundary and confirm final use |
| Emotion recognition | **Hard boundary** | Not implemented | Future feature would be highly problematic | Explicitly prohibit |
| Article 50 direct-interaction disclosure | **Not applicable to current scope** | No direct AI conversation | Reassess if AI tutor/chat added | Change trigger |
| Article 50 synthetic-content marking | **Legal confirmation required** | LLM-assisted text path exists | Final technical marking responsibility unresolved | Confirm before live LLM pilot |
| AI literacy | **Operational gap** | No formal training evidence yet | Article 4 operational evidence needed | Create role-based briefing |
| Human oversight | **Partial evidence** | Logical local gate exists | No production reviewer/audit identity | Formalise before pilot |
| Technical documentation | **Partial evidence** | Repository evidence exists | Needs consolidated final ToC | Complete before submission/pilot |
| Incident process | **Operational gap** | No formal process | Production/pilot issue escalation missing | Define before pilot |
| Post-market monitoring | **Not applicable to current local scope** | No production deployment | Future operational process | Design before full deployment |

---

# 17. Conformity Assessment Summary

## Legal trigger

**Under the preliminary internal classification, a formal high-risk conformity assessment does not appear to be triggered by the current described intended purpose. This is not a certification or final legal conclusion.**

Therefore KinderFlow should not:

- claim high-risk conformity certification;
- claim CE marking for this AI use;
- perform a fictitious conformity procedure merely for the capstone.

## Internal readiness assessment

For capstone and pilot-readiness purposes, KinderFlow should nevertheless maintain an internal conformity-style evidence pack covering:

1. intended purpose;
2. system description;
3. AI components;
4. known limitations;
5. risk assessment;
6. human oversight;
7. performance evidence;
8. error handling;
9. data/provenance;
10. technical documentation;
11. transparency;
12. AI literacy;
13. incident/change procedures.

## Current internal result

**PARTIAL EVIDENCE — LEGAL AND OPERATIONAL CONFIRMATION REQUIRED**

The repository already provides strong technical evidence and unusually clear separation between technical processing and human approval.

The main gaps are operational and governance-related rather than core MVP feasibility.

---

# 18. Technical Documentation Outline

The following structure should be maintained for pilot and production readiness.

## 1. System identification

- Product name
- Version
- Provider
- Intended purpose
- Intended users
- Deployment context

## 2. Product architecture

- KinderFlow Hub
- KinderFlow Admin
- Kinder Signs School Admin
- Family experience
- Internal vs external responsibilities

## 3. AI component inventory

### Computer Vision

- MediaPipe version
- input format
- landmark extraction
- normalization
- technical metrics
- status mapping
- known limitations

### LLM-assisted content

- provider/model
- prompt version
- structured contract
- output fields
- quality gate
- LIVE / DRY_RUN behavior
- LangSmith boundary

## 4. Non-AI components

- deterministic quality rules
- Flashcard templates
- ordinary UI/business logic

## 5. Data and content inputs

- validated adult reference material
- sign metadata
- routines/context
- generated/reviewed family wording
- provenance

## 6. Outputs

- movement representation
- technical metrics
- content review candidate
- Flashcard / Routine Card proof
- school/family preview

## 7. Performance evidence

- test results
- MediaPipe run evidence
- run-specific metrics
- known failure cases
- error handling

## 8. Human oversight

- reviewer role
- approval criteria
- Review needed handling
- Fail handling
- publication boundary

## 9. Risk management

- technical
- regulatory
- ethical
- operational
- commercial

## 10. Transparency

- AI role explanation
- direct-interaction analysis
- generated-content marking
- family/school notices

## 11. Security

- runtime architecture
- credentials
- local vs production storage
- access control
- logging
- incident management

## 12. Change management

- version control
- model changes
- prompt changes
- threshold changes
- new features
- classification review trigger

## 13. Third parties

- MediaPipe / Google
- LLM provider
- LangSmith
- hosting/infrastructure
- visual source libraries where relevant

## 14. Compliance links

- GDPR assessment
- DPIA
- AI Act assessment
- asset/content provenance
- contractual roles

---

# 19. What KinderFlow should say publicly

## Safe description

> KinderFlow uses Computer Vision to turn validated adult reference movement into structured technical evidence for human review. AI-assisted content can help prepare family wording, but publication remains under human control.

## Avoid

> AI validates the sign.

> KinderFlow verifies that a child signs correctly.

> KinderFlow assesses child development.

> The system is certified as EU AI Act compliant.

> The system is minimal-risk because it is only educational content.

---

# 20. Pilot controls

## Must resolve before pilot

1. Finalise intended-purpose statement.
2. Document prohibited uses.
3. Confirm provider/deployer roles.
4. Complete GDPR / DPIA screening.
5. Confirm reference-content rights.
6. Formalise reviewer responsibilities.
7. Create AI literacy briefing.
8. Resolve Article 50 generated-text marking responsibilities for any live LLM path.
9. Define incident/escalation process.
10. Reconcile README, MVP docs and demonstrated product state.

## Operate during pilot

- track technical failures;
- track Review needed frequency;
- track content-review issues;
- log scope changes;
- monitor school misuse or misunderstanding;
- collect staff feedback about AI transparency.

## Production requirement

- persistent audit records;
- authentication / permissions;
- production security;
- formal release management;
- post-market monitoring;
- vendor governance;
- classification reassessment when functionality changes.

---

# 21. Slide-ready summary

| Question | Answer |
|---|---|
| Is Kinder Signs an AI-enabled system? | **Yes** |
| Does the current intended use appear to match Annex III high-risk education uses? | **No, under the preliminary internal assessment; final pilot confirmation required** |
| Why not? | It does not make admissions, learning-outcome, educational-level or exam-monitoring decisions |
| Does it use child video? | **No** |
| Does it score children? | **No** |
| Does it recognise emotions? | **No — explicit boundary** |
| Does CV certify sign correctness? | **No** |
| Is human review required? | **Yes** |
| What is the main AI Act gap before pilot? | AI literacy, final transparency assessment, documented roles and governance |
| Could classification change? | **Yes, if future child-assessment or decision-making features are added** |

---

# 22. Bottom line

## Assessment

**PROCEED WITH CONDITIONS**

Kinder Signs is an AI-enabled product operating in an educational setting. Under the preliminary internal assessment, its current described intended purpose does not appear to match the high-risk education uses listed in Annex III.

This is a meaningful distinction: **education context alone does not make the system high-risk.**

The current product architecture also avoids several particularly sensitive areas by design:

- no child video;
- no emotion recognition;
- no biometric identification;
- no learning-outcome scoring;
- no developmental assessment;
- no automated educational decisions;
- no autonomous publication.

Before a controlled pilot, KinderFlow should close the remaining governance gaps, particularly AI literacy, provider/deployer role documentation, Article 50 transparency analysis for any live LLM output, human-review procedures and GDPR pilot readiness.

A future feature that begins assessing children or materially influencing educational decisions must trigger a fresh AI Act classification before development or deployment proceeds.

---

# 23. Official sources

1. Regulation (EU) 2024/1689 — Artificial Intelligence Act, consolidated version current in 2026  
   https://eur-lex.europa.eu/eli/reg/2024/1689

2. EUR-Lex — Annex III high-risk AI systems, including education and vocational training  
   https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:02024R1689-20260727

3. European Commission — Navigating the AI Act / application timetable  
   https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act

4. European Commission — AI literacy Q&A  
   https://digital-strategy.ec.europa.eu/en/faqs/ai-literacy-questions-answers

5. European Commission — AI Act enforcement framework  
   https://digital-strategy.ec.europa.eu/en/policies/enforcement-ai-act

6. European Commission — High-risk AI-system guidelines and updated application timeline  
   https://digital-strategy.ec.europa.eu/en/policies/guidelines-ai-high-risk-systems

---

# 24. Repository evidence used

The assessment was checked against the committed repository baseline, including:

- `mvp/mvp_documentation.md`
- `poc/`
- `content_ops/`
- `workflow/kinder_signs_n8n_workflow.md`
- `prototype/README.md`
- `prototype/create-sign.*`
- `prototype/flashcards.*`
- `prototype/school.*`
- `prototype/family.html`

Current committed Round 2 baseline:

`661c027 — Build Round 2 KinderFlow MVP and UX`

## Documentation gap identified

The root `README.md` still contains some Round 1 / older product wording, including cadence-specific school assignment language and an older repository overview.

The more recent `prototype/README.md` and MVP documentation better reflect the current product architecture.

**Action before final submission:** reconcile the root README with the final frozen Round 2 state.
