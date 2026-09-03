# KinderFlow — GDPR Documentation & Privacy-by-Design Assessment

**Project:** KinderFlow — Early Childhood Digital Growth  
**Use case assessed:** Kinder Signs  
**Assessment date:** 2 September 2026  
**Jurisdiction:** European Union / Spain  
**Assessment scope:** Current local MVP, proposed controlled pilot, and foreseeable production deployment

> This document is a capstone privacy assessment and implementation plan, not formal legal advice. The final controller/processor allocation and lawful bases should be confirmed against the actual pilot contracts, school type and data flows before real personal data are processed.

---

# 1. Executive takeaway

## Executive question

**Can Kinder Signs move from a local MVP to a real-school pilot without introducing disproportionate privacy risk?**

## Current conclusion

**PROCEED WITH CONDITIONS**

Privacy-by-design evidence exists in the current MVP because:

- child video is deliberately excluded;
- the Computer Vision pipeline processes adult reference material;
- the local MVP uses fictional school/child/family records;
- the core product does not need health data, developmental diagnoses or child-performance scores;
- Computer Vision does not identify people;
- there is no automated decision-making about children;
- LLM-assisted content can operate on approved sign/context data rather than personal data.

Operational GDPR readiness remains incomplete. A real pilot would introduce personal data for school staff, caregivers and, if individual assignment is used, children. The pilot therefore requires a documented data model, lawful-basis analysis, controller/processor allocation, Article 28 agreements where applicable, retention rules, security controls, transparency notices, rights procedures and a DPIA before real deployment.

The privacy objective should be:

> **Use the minimum personal data needed to connect approved KinderFlow content with the correct school group or family — and keep personal data out of AI processing whenever it is not necessary.**

---

# 2. Regulatory framework

The main framework is:

- Regulation (EU) 2016/679 — General Data Protection Regulation (GDPR);
- Spanish Organic Law 3/2018 (LOPDGDD);
- AEPD guidance on risk management and Data Protection Impact Assessments;
- EDPB guidance on children's data and DPIAs.

Key GDPR principles relevant to KinderFlow include:

- lawfulness, fairness and transparency;
- purpose limitation;
- data minimisation;
- accuracy;
- storage limitation;
- integrity and confidentiality;
- accountability;
- data protection by design and by default.

Children require particular protection because they are a vulnerable group.

---

# 3. Privacy scope by product stage

KinderFlow must not treat the current local MVP, a real-school pilot and production deployment as if they were the same processing activity.

| Stage | Personal-data reality | GDPR position |
|---|---|---|
| **Current local MVP** | Adult reference material + local technical run data; school/family/child records are fictional | Limited real-data processing |
| **Controlled pilot** | Real school staff, caregiver and limited child-assignment data | Full GDPR governance required before launch |
| **Production** | Persistent accounts, access, assignments, security logs, support and potentially broader analytics | Full operational privacy programme required |

---

# 4. Current MVP — data inventory

## 4.1 Adult reference video

The Create a Sign MVP accepts an adult reference MP4.

Potential data:

- identifiable image of adult performer;
- movement / pose data;
- hand / body landmarks;
- source filename;
- technical video metadata;
- processing timestamp;
- run identifier;
- processing diagnostics.

### Classification

If the adult is identifiable, the source video is personal data.

Pose and hand landmarks can also be personal data when linked to an identifiable person.

### Article 9 biometric-data boundary

The GDPR treats biometric data as special-category data when it results from specific technical processing relating to physical, physiological or behavioural characteristics **and is used to allow or confirm unique identification**.

KinderFlow's current MediaPipe purpose is:

> movement extraction and representation.

It is not:

> identification or identity verification.

Therefore the current landmark use should not automatically be described as Article 9 biometric identification.

### Control

KinderFlow must preserve this purpose boundary.

If future functionality uses movement, face or body data to identify a person, the Article 9 analysis changes.

---

# 5. Current MVP — other data

## Sign/content records

Examples:

- sign ID;
- sign label;
- language;
- approved routine/context;
- source/provenance ID;
- content-review state;
- Flashcard copy.

These are normally **not personal data** unless the source/provenance field contains identifiable contributor information.

---

## Technical run data

Examples:

- run ID;
- processing status;
- frame metrics;
- missing-landmark counts;
- processing duration;
- error logs.

These may become personal data if linked to an identifiable operator or identifiable reference performer.

Current local runs do not implement authenticated user identities.

---

## School / child / family prototype records

The current prototype uses fictional records.

**No real child data should be inferred from prototype fields.**

The existing School Admin demonstrates product logic such as:

```text
Child
Group
Parents / caregivers
Active packs
```

These fields become personal data only when real individuals are introduced during pilot or production.

---

# 6. Proposed pilot data model

The pilot should start with the smallest possible dataset.

## 6.1 School / centre data

Recommended:

- centre ID;
- centre name;
- plan / entitlement;
- participating groups;
- pilot status.

Usually organisational data are not personal data, but contact details may identify individuals.

---

## 6.2 School staff

Minimum likely data:

- staff ID;
- name;
- work email;
- role;
- school;
- account/access status;
- relevant activity/security logs.

Avoid:

- unnecessary personal phone numbers;
- personal email where work email is available;
- demographic profiling;
- unrelated employment information.

---

## 6.3 Child data

### Proposed minimum if individual child assignment is included

- pseudonymous child ID;
- school/group association;
- content assigned;
- active content pack where needed.

### Prefer not to collect

- exact date of birth;
- home address;
- photographs;
- videos;
- voice recordings;
- health information;
- developmental diagnosis;
- disability information;
- detailed behavioural profiles.

Age band or classroom group should be preferred over exact date of birth where sufficient.

### Strong design recommendation

The reason why a sign was assigned should **not** be stored as a diagnosis or developmental label.

KinderFlow needs to know:

> what content should be available to this child/family

not:

> why the child may need communication support.

---

# 7. Caregiver / family data

Likely minimum:

- caregiver ID;
- name;
- contact email or secure access identifier;
- relationship/access link to child;
- school/group entitlement;
- content-access state.

Potentially useful but optional:

- preferred interface language.

Avoid collecting unnecessary family-profile information.

---

# 8. Engagement and analytics data

A pilot needs evidence of value, but analytics should be proportionate.

## Recommended pilot signals

- content assigned;
- content accessed;
- broad access timestamp;
- school/group aggregate engagement;
- completion of simple feedback survey.

## Avoid

- granular behavioural tracking;
- attention scoring;
- child-level engagement profiling;
- inferred developmental ability;
- emotion analytics;
- cross-service advertising profiles.

### Preferred commercial metric

Instead of:

> Child A accessed the MORE card 14 times at 20:42.

Prefer:

> 72% of participating families accessed the assigned material during the pilot period.

This gives KinderFlow useful commercial evidence while reducing privacy exposure.

---

# 9. Current and proposed data flows

## 9.1 Current Computer Vision flow

```text
Validated adult reference MP4
→ local KinderFlow MVP service
→ MediaPipe
→ raw landmarks
→ normalized landmarks
→ movement diagnostics
→ browser-safe movement overlay
→ human review
→ local run storage
```

### Current boundary

The MVP documentation states that reference video processing remains local.

The video is not sent to the LLM or LangSmith.

---

# 10. Pilot school-family flow

Recommended architecture:

```text
School / centre record
→ participating group
→ pseudonymous child record
→ caregiver access relationship
→ educator selects approved content
→ assignment record
→ family receives/accesses approved material
→ minimal aggregate engagement signal
```

The AI content-production workflow should remain separate:

```text
Approved sign/context
→ optional LLM-assisted wording
→ deterministic checks
→ human review
→ approved content asset
```

### Privacy principle

**School/family/child identifiers should not be required to generate the content.**

This is one of the strongest privacy-by-design opportunities in the architecture.

---

# 11. LLM and LangSmith data boundary

The current content system can generate family-facing wording from:

- structured sign data;
- approved routine/context;
- bounded content instructions.

It does not need:

- child name;
- child profile;
- caregiver email;
- diagnosis;
- school-family message history.

## Recommended hard rule

**Do not send real child, caregiver or school-user personal data to the LLM or LangSmith in the pilot.**

This materially simplifies:

- purpose limitation;
- processor governance;
- international transfer risk;
- data minimisation;
- incident impact.

If a future use case genuinely requires personal data in LLM processing, perform a separate privacy and processor review first.

---

# 12. Controller / processor assessment

The exact allocation is a working assumption that must be confirmed by purpose, actual data flow and contract before pilot launch.

## 12.1 School-controlled child/family records

For a typical school-led deployment, the school is likely to determine why its children/families are registered and why content is assigned.

### Likely role

**Working assumption: School as controller, subject to purpose and contract**

---

## 12.2 KinderFlow processing school data on instruction

If KinderFlow hosts:

- child identifiers;
- caregiver access;
- school assignments;
- engagement records;

only to provide the contracted service under school instructions:

### Likely role

**Working assumption: KinderFlow as processor for instructed school processing, subject to purpose and contract**

An Article 28 Data Processing Agreement would then be required.

---

## 12.3 KinderFlow's own operational purposes

KinderFlow may act as an independent controller for limited purposes such as:

- account administration;
- fraud/security prevention;
- contract/contact management;
- legal compliance;
- its own internal staff/reviewer records.

These purposes should be kept separate from school-controlled child/family processing.

---

## 12.4 Joint controllership

Joint controllership should **not** be assumed.

It arises where parties jointly determine purposes and essential means.

KinderFlow should prefer clear role separation rather than creating joint control unintentionally through vague product analytics or independent reuse of school data.

---

# 13. Lawful-basis assessment — Article 6

There is no single lawful basis for the entire platform.

It must be identified per processing activity.

| Processing activity | Likely basis to assess | Current decision |
|---|---|---|
| B2B account/contact administration | Contract and/or legitimate interests depending relationship | **TBD CONTRACTUALLY** |
| School staff login/security | Legitimate interests / contract context | **TBD** |
| Child/family service records | Determined by school controller according to school type and service purpose | **TBD BEFORE PILOT** |
| Family access/delivery | Determined by controller and actual service relationship | **TBD BEFORE PILOT** |
| Security logging | Legitimate interests / legal obligations where applicable | **TBD** |
| Optional product research | Consent or legitimate interests only after balancing and design review | **DO NOT BUNDLE** |
| Marketing to school contacts | Separate ePrivacy / LSSI + GDPR analysis | **OUTSIDE CORE PILOT** |

## Important

Consent should **not** be used as a catch-all solution simply because children are involved.

The correct legal basis depends on:

- school type;
- contractual relationship;
- educational purpose;
- national/legal obligations;
- whether the processing is necessary for the service.

---

# 14. Children's consent — Spain

Children are vulnerable data subjects generally. Under Spanish LOPDGDD Article 7, age 14 is specifically relevant when relying on the child's own consent: that consent can generally be relied on only when the child is **over 14**.

Where consent is the lawful basis for a child under 14, consent must come from the holder of parental responsibility or guardianship.

## KinderFlow relevance

Kinder Signs is designed for children aged approximately 0–3.

Therefore:

> **KinderFlow must never rely on the child's own consent.**

However, the pilot should also avoid assuming that parental consent is automatically the correct lawful basis for every school processing activity.

The school/controller must document the correct Article 6 basis for each purpose.

---

# 15. Article 8 — information-society services offered directly to children

The current product is:

- school-led;
- operated by adults;
- not directly contracted or operated by a 0–3-year-old child.

Article 8 is therefore not the main current design route.

If KinderFlow later introduces a child-facing account or service directly offered to children, the analysis must be reopened.

---

# 16. Special-category data — Article 9

The core pilot does not require:

- health data;
- disability data;
- diagnosis;
- genetic data;
- data revealing protected beliefs or identity characteristics.

## Risk

Because Kinder Signs relates to early communication, a school might be tempted to include notes such as:

- speech delay;
- developmental condition;
- therapy status;
- disability;
- clinical diagnosis.

These may constitute health/special-category data.

## Design rule

**Do not include these fields in the core Kinder Signs data model.**

If a future use case genuinely needs health or disability information:

1. establish an Article 6 basis;
2. establish an Article 9 condition;
3. complete a new DPIA/risk assessment;
4. implement stronger access/security controls;
5. update transparency and retention.

---

# 17. Automated decisions and profiling — Article 22

Current Kinder Signs:

- does not score children;
- does not rank children;
- does not determine educational placement;
- does not infer developmental readiness;
- does not automatically decide what services a child can access.

The educator chooses what approved content to assign.

## Current result

**No solely automated decision with legal or similarly significant effects is identified in the current described scope.**

## Hard boundary

Any future child scoring, recommendation or decision engine must be assessed separately.

---

# 18. Data minimisation assessment

| Data | Necessary? | Recommendation |
|---|---|---|
| Child pseudonymous ID | Yes for individual assignment | Keep |
| Child name | Possibly | Avoid if pseudonymous ID is operationally sufficient |
| Exact date of birth | Usually no | Use age/group band |
| Child photo | No | Do not collect |
| Child video | No | Do not collect |
| Child voice | No | Do not collect |
| Health/diagnosis | No for core product | Do not collect |
| Parent/caregiver email | Yes if direct access requires it | Keep only while needed |
| Caregiver phone | Usually no | Avoid |
| Educator name/work email | Likely yes | Keep |
| Assignment history | Limited need | Define retention |
| Family access event | Useful for pilot | Minimise/aggregate |
| Fine-grained behaviour | No | Do not collect |
| LLM prompt containing child data | No | Prohibit |

---

# 19. Storage limitation and retention

The current local MVP has **no formal retention policy**.

This is a documented gap.

## Proposed pilot retention framework

Final periods must be agreed with the controller.

| Data type | Pilot recommendation | End-of-pilot action |
|---|---|---|
| Adult reference source | Only as long as production/review/provenance requires | Retain governed source or delete according to rights/licence policy |
| Raw CV landmarks | Keep only if needed for reproducibility/review | Review/delete or retain controlled version |
| Technical run logs | Pilot + short audit window | Delete or anonymise |
| Child assignment data | Active pilot/service period | Delete/return after agreed termination window |
| Caregiver contact/access | Active access period | Delete after termination window |
| Educator account | Active account | Disable then delete according to policy |
| Aggregate pilot metrics | May be retained if truly anonymised | Retain as non-personal evidence |
| Support tickets | Defined operational/legal period | Delete on schedule |
| Security logs | Defined security period | Automatically expire |

## Required before pilot

Define exact periods in a retention schedule.

“Keep indefinitely” is not acceptable.

---

# 20. Privacy by design and by default — Article 25

KinderFlow already has several strong design choices.

## Existing controls

### No child video

The largest unnecessary sensitive input was removed from scope.

### Central content production

Schools do not need to upload their own sign videos or personal child media.

### Separation of content and recipient

A sign can be produced without knowing which child will receive it.

### Deterministic Flashcards

Flashcard rendering does not require personal data or GenAI.

### Human review

AI output does not autonomously reach families as published content.

### No child assessment

Technical movement metrics apply to adult reference content, not children.

---

## Additional pilot controls

- pseudonymous child IDs;
- least-privilege access;
- school-level tenancy;
- secure caregiver access;
- no personal data in LLM/LangSmith;
- no unnecessary analytics;
- automatic retention/deletion rules;
- audit logs for sensitive administrative actions;
- default private visibility;
- separation of production/admin/family permissions.

---

# 21. Record of Processing Activities — proposed structure

A full Article 30 RoPA should be maintained by the relevant controller/processor where required.

## Proposed KinderFlow processing inventory

| Activity | Data subjects | Data categories | Purpose | Role | Recipients/subprocessors | Retention | Status |
|---|---|---|---|---|---|---|---|
| Adult reference processing | Adult performer | Video, landmarks, metadata | Create/review sign asset | Controller/TBD | Local processing initially | TBD | **MVP ACTIVE** |
| Staff account administration | Educators/admins | Name, work email, role | Access/service administration | Controller or processor depending activity | Hosting/auth provider | TBD | **PILOT** |
| Child assignment | Children | Pseudonymous ID, group, assignment | Deliver school-selected content | Likely processor | Hosting | TBD | **PILOT** |
| Family access | Caregivers | Name/contact/access relation | Provide assigned material | Likely processor | Email/auth/hosting | TBD | **PILOT** |
| Engagement measurement | Caregivers/school groups | Access/event data | Measure pilot adoption/value | Role depends purpose | Analytics/hosting | Short pilot period | **PILOT — MINIMISE** |
| Content generation | Internal content | Sign/context data | Draft family content | Controller for internal ops | LLM provider if LIVE | Content lifecycle | **MVP/PILOT** |
| AI observability | Internal content workflow | Prompt/output metadata | QA/traceability | Controller | LangSmith if LIVE | TBD | **OPTIONAL** |
| Security logging | Platform users | Account/IP/security events | Security | Controller/processor context | Hosting/security providers | TBD | **PRODUCTION** |
| Support | Staff/caregivers | Contact/support content | Resolve issues | Mixed/TBD | Support provider | TBD | **PILOT/PRODUCTION** |

---

# 22. Transparency obligations — Articles 12–14

Before a real pilot, data subjects must receive clear information appropriate to their role.

## School staff notice

Explain:

- who controls the data;
- KinderFlow's role;
- account data processed;
- purposes;
- lawful bases;
- recipients;
- retention;
- rights;
- contact route;
- relevant international transfers.

---

## Parent / caregiver notice

Use clear, non-technical language.

Explain:

- school/KinderFlow roles;
- what family and child data are used;
- why;
- what is not collected;
- that KinderFlow does not assess the child with AI;
- that child video is not required;
- how long data are kept;
- how to exercise rights;
- whom to contact.

---

## Child-facing transparency

For the current 0–3 product, the meaningful transparency route is primarily through parents/guardians and the school.

If KinderFlow later creates a direct child-facing interface for older children, information must be age-appropriate and understandable.

---

# 23. Data-subject rights

Processes must support:

- access;
- rectification;
- erasure;
- restriction;
- portability where applicable;
- objection where applicable;
- rights related to automated decision-making where applicable.

## Operational design question

If the school is controller and KinderFlow processor:

```text
Parent request
→ school/controller
→ KinderFlow assists under Article 28
→ data located/exported/corrected/deleted
→ controller responds
```

The Article 28 agreement should define this assistance.

---

# 24. Processor requirements — Article 28

Where KinderFlow acts as processor, the school agreement should cover:

- subject matter and duration;
- nature and purpose;
- categories of personal data;
- data subjects;
- processing only on documented instructions;
- confidentiality;
- security;
- subprocessors;
- data-subject-right assistance;
- breach assistance;
- DPIA assistance;
- deletion/return after termination;
- audits/compliance evidence.

A generic SaaS contract is not enough unless it includes these processor terms.

---

# 25. Subprocessor and vendor register

The final register depends on the pilot architecture.

Potential vendors include:

- hosting provider;
- authentication provider;
- email/delivery provider;
- LLM provider;
- LangSmith;
- support/analytics tooling.

## Critical privacy architecture decision

If the LLM and LangSmith receive **no personal data**, their privacy exposure for child/family processing is greatly reduced.

This should be a deliberate technical control, not an informal assumption.

---

# 26. International transfers — Chapter V

The current local MVP does not send the adult MP4 to an external service.

A hosted pilot may introduce processors outside the EEA or international access.

Before pilot, for every relevant vendor:

1. identify processing location;
2. identify transfer mechanism;
3. check adequacy decision where applicable;
4. otherwise confirm Standard Contractual Clauses or other valid mechanism;
5. complete transfer-risk analysis where required;
6. document supplementary measures;
7. reflect the transfer in privacy information.

## Important

Do not claim:

> “No international transfers”

until the final production vendors and data routes have been audited.

---

# 27. Security of processing — Article 32

Current local MVP controls include:

- isolated run identifiers;
- sanitized filenames;
- no raw local paths in UI;
- no tracebacks exposed to users;
- ignored local run directories;
- serialized MediaPipe processing;
- no embedded credentials in workflow export.

These are useful MVP controls but are **not a production security programme**.

## Pilot minimum

- authenticated users;
- role-based access;
- tenant/school isolation;
- TLS in transit;
- encryption at rest where appropriate;
- secret management;
- secure password/authentication policy;
- access logging;
- backups;
- retention/deletion controls;
- vulnerability/patch process;
- incident response;
- least privilege;
- processor security review.

---

# 28. Personal-data breach process

Before pilot:

```text
Detect
→ contain
→ assess affected data/data subjects
→ document incident
→ determine controller/processor responsibilities
→ processor informs controller without undue delay
→ controller assesses Article 33 notification
→ notify supervisory authority within 72 hours where required
→ assess Article 34 communication to individuals
→ remediate
```

The school/KinderFlow contract must identify incident contacts and escalation paths.

---

# 29. DPIA screening — Article 35

## Current local MVP

A full DPIA is not necessary merely to run the current fictional/local demonstration.

However, the adult-reference processing still requires normal GDPR risk management if identifiable personal data are used.

---

## Real-school pilot

**DPIA: STRONGLY RECOMMENDED BEFORE PILOT AND LIKELY TO BE REQUIRED DEPENDING ON THE FINAL PROCESSING DESIGN.**

Reasons include:

- use of new/AI-enabled technology;
- children under 14 are vulnerable data subjects;
- persistent school-family data would be introduced;
- the service may measure usage/engagement;
- multiple organisations may participate in the processing chain.

AEPD guidance states that a DPIA is generally mandatory where processing is likely to create high risk and notes that, in general, identifying two or more risk criteria points toward carrying one out.

AEPD's list explicitly includes processing involving vulnerable data subjects, including children under 14, as a risk criterion.

## Practical decision

Rather than debating whether the smallest pilot could avoid the legal threshold, KinderFlow should:

> **complete a pilot DPIA as a governance gate.**

This provides stronger evidence for both the capstone and a real commercial discussion.

---

# 30. Proposed DPIA structure

## A. Description

- system;
- purposes;
- stakeholders;
- data subjects;
- personal data;
- flows;
- recipients;
- retention;
- technologies.

## B. Necessity and proportionality

For each data field:

> Do we genuinely need this to deliver school-home continuity?

If not, remove it.

## C. Risks to individuals

Examples:

- child assignment exposed to wrong family;
- school-to-school data leakage;
- unauthorised access;
- excessive child profiling;
- accidental health-data collection;
- content/engagement data retained too long;
- personal data sent to LLM vendor;
- account takeover;
- incorrect parent-child association;
- sensitive inference from individual usage;
- breach affecting vulnerable data subjects.

## D. Controls

- minimisation;
- pseudonymisation;
- access control;
- tenant isolation;
- human oversight;
- LLM personal-data prohibition;
- retention;
- encryption;
- vendor governance;
- incident response.

## E. Residual risk

Decide:

- GO;
- GO WITH CONDITIONS;
- ITERATE;
- STOP / CONSULT AEPD where residual high risk cannot be reduced.

---

# 31. Privacy risk register

| Risk | Likelihood | Impact | Level | Control | Pilot gate |
|---|---:|---:|---|---|---|
| Wrong family receives child's assignment | 2 | 5 | High | Secure relationship mapping + access checks | **Must resolve** |
| Cross-school data exposure | 2 | 5 | High | Tenant isolation + RBAC + tests | **Must resolve** |
| Unnecessary child data collected | 3 | 4 | High | Minimal schema + prohibited fields | **Must resolve** |
| Health/developmental data entered informally | 3 | 5 | Critical | No free-text diagnosis field + policy/training | **Must resolve** |
| Personal data enters LLM/LangSmith | 2 | 5 | High | Technical/policy prohibition + redaction | **Must resolve** |
| Excessive engagement tracking | 3 | 4 | High | Aggregate metrics by default | **Pilot design control** |
| Data retained after pilot | 3 | 3 | Moderate | Retention schedule + deletion workflow | **Must resolve** |
| Weak reviewer/admin authentication | 3 | 4 | High | Production auth/RBAC | **Must resolve** |
| Vendor transfer not documented | 2 | 4 | Moderate | Vendor/SCC/transfer register | **Must resolve if applicable** |
| Parent cannot exercise rights efficiently | 2 | 4 | Moderate | Controller/processor rights workflow | **Must resolve** |

---

# 32. GDPR compliance matrix

| Requirement | Current status | Evidence | Gap | Action |
|---|---|---|---|---|
| Processing inventory | **Partial evidence** | MVP architecture documented | Pilot fields not frozen | Approve pilot schema |
| Lawful basis | **Legal confirmation required** | No real pilot yet | Must be mapped per purpose/controller | Legal review before pilot |
| Data minimisation | **Evidence present; operational control required** | Child video removed | Persistent pilot schema TBD | Use pseudonymous/minimal model where individual assignment is included |
| Special-category minimisation | **Design evidence present** | Not required by core use | Could enter via free text | Prohibit unnecessary health data |
| Article 22 | **Not identified in current scope** | No child scoring/automated decisions | Future scope risk | Maintain hard boundary |
| Controller/processor roles | **Legal confirmation required** | School-led model | Purposes and contracts not final | Confirm roles |
| Article 28 DPA | **Operational gap** | Not required for local MVP | Required where KinderFlow is processor | Draft before pilot |
| Transparency | **Operational gap** | Prototype copy only | Legal privacy notices missing | Draft school/caregiver notices |
| Rights handling | **Operational gap** | No real data | Workflow not implemented | Define process |
| Retention | **Operational gap** | Local MVP has no formal policy | Exact periods missing | Create retention schedule |
| Privacy by design | **Evidence present** | No child video; separated content generation | Must operationalise controls | Preserve through pilot |
| Security | **Local MVP evidence only** | Basic local safeguards | No auth/tenant isolation | Pilot security baseline |
| Subprocessors | **Partial evidence** | Vendors identifiable | Final architecture not fixed | Vendor register/DPA review |
| International transfers | **TBD** | Depends on vendors/data | No final transfer map | Complete before pilot |
| DPIA | **Operational gap** | Screening now completed | Full assessment not yet done | Complete before real pilot |
| Breach response | **Operational gap** | None operational | Contacts/process missing | Define before pilot |
| RoPA | **Draft structure** | This document | Formal record needed | Complete before pilot |

---

# 33. MVP → Pilot → Production privacy gates

## Current MVP

### Acceptable for demonstration

- local adult-reference processing;
- fictional child/family data;
- no personal data in LLM workflow;
- no persistent real accounts.

### Remaining MVP housekeeping

- document retention/deletion of local demo runs;
- confirm reference-performer rights/provenance.

---

## Before controlled pilot

### Must have

1. final personal-data schema;
2. controller/processor allocation;
3. lawful-basis matrix;
4. Article 28 DPA;
5. DPIA;
6. parent/caregiver and staff privacy information;
7. retention schedule;
8. rights procedure;
9. subprocessor register;
10. transfer assessment;
11. authentication/RBAC;
12. school tenancy isolation;
13. incident/breach procedure;
14. LLM/LangSmith no-personal-data rule;
15. data deletion/return procedure.

---

## Before full production

Add:

- scalable security monitoring;
- formal vendor review cycle;
- production audit logging;
- tested backup/recovery;
- periodic access review;
- privacy/security incident exercises;
- product-change DPIA trigger;
- data lifecycle automation;
- formal privacy governance ownership.

---

# 34. Pilot-ready data architecture recommendation

The preferred architecture is deliberately simple.

```text
CONTENT DOMAIN
Validated adult reference
→ CV processing
→ reviewed sign
→ approved content

IDENTITY / DELIVERY DOMAIN
School
→ group
→ pseudonymous child ID
→ caregiver access
→ assignment

OUTPUT
Approved content + entitlement
→ family receives content
```

These domains should remain separated.

The Content Engine should not need a child's identity to write a Flashcard or family guidance.

---

# 35. Recommended pilot schema

## Child

```text
child_id
school_id
group_id
active_content_entitlements
```

Add a display name only if user research proves it is operationally necessary.

---

## Caregiver

```text
caregiver_id
contact_identifier
child_access_relationship
preferred_language (optional)
access_status
```

---

## Educator

```text
staff_id
school_id
name
work_email
role
account_status
```

---

## Assignment

```text
assignment_id
content_id
school_id
group_id
child_id (nullable)
assigned_by
assigned_at
```

Avoid storing an explanation such as:

```text
reason_for_assignment = speech delay
```

The product does not need it.

---

# 36. Pilot privacy KPIs

Privacy controls should be measurable.

| KPI | Target |
|---|---|
| Child videos processed | **0** |
| Child health/developmental fields in core schema | **0** |
| Personal-data fields sent to LLM | **0** |
| Personal-data fields sent to LangSmith | **0** |
| Unauthorised cross-school access incidents | **0** |
| Open high-risk DPIA actions at pilot start | **0** |
| Staff completing privacy/AI onboarding | **100% of pilot operators** |
| Data-subject requests within required deadline | **100%** |
| Pilot data deleted/returned according to schedule | **100%** |

---

# 37. What KinderFlow should say

## Safe

> KinderFlow uses only the personal data needed to connect school-approved content with the correct families. The core Computer Vision workflow uses adult reference material and does not require child video or child-performance analysis.

## Avoid

> KinderFlow does not process personal data.

False once real staff/family/child accounts are introduced.

---

## Avoid

> KinderFlow is GDPR compliant.

Too broad before pilot contracts, DPIA, vendor configuration, security controls and operational procedures are complete.

Use:

> KinderFlow has been designed with data minimisation and privacy-by-design controls. A real-school pilot requires the additional GDPR controls documented in the pilot plan.

---

# 38. Slide-ready summary

| Question | Answer |
|---|---|
| Does the core MVP require child video? | **No** |
| Does CV assess the child? | **No** |
| Does the LLM need child data? | **No** |
| Are prototype child records real? | **No — fictional** |
| Would a real pilot process child data? | **Yes, limited assignment/access data** |
| Proposed child identifier if individual assignment is used | **Pseudonymous ID, subject to final data design** |
| Should diagnoses be stored? | **No, not for the core service** |
| Should personal data go to LLM/LangSmith? | **No** |
| Is Article 22 automated decision-making present? | **No** |
| Is a DPIA recommended? | **Yes — before pilot** |
| Current decision | **PROCEED WITH CONDITIONS** |

---

# 39. Bottom line

## Assessment

**PROCEED WITH CONDITIONS**

KinderFlow's current architecture contains a strong privacy-by-design decision: the product can create and distribute Kinder Signs content **without analysing child video or child performance**.

This substantially reduces privacy, security and regulatory complexity.

The current local MVP does not prove production GDPR compliance because the real-school data-processing layer does not yet exist.

A pilot should introduce only the minimum identity and assignment data necessary to connect a school, group, child and caregiver.

The most important privacy design principle is:

> **Keep content intelligence separate from personal identity.**

If KinderFlow maintains that separation, avoids unnecessary child/health data, prevents personal data from entering LLM/LangSmith workflows, uses pseudonymous child identifiers and implements the required contractual/security controls, a limited school pilot can be designed with materially lower privacy risk.

The final gate before real personal data are used should be a completed DPIA with no unresolved high-risk actions.

---

# 40. Official sources

1. Regulation (EU) 2016/679 — General Data Protection Regulation (GDPR)  
   https://eur-lex.europa.eu/eli/reg/2016/679/oj

2. Spanish Organic Law 3/2018 (LOPDGDD), including Article 7 on minors' consent  
   https://www.boe.es/buscar/act.php?id=BOE-A-2018-16673

3. AEPD — Data Protection Impact Assessments  
   https://www.aepd.es/derechos-y-deberes/cumple-tus-deberes/medidas-de-cumplimiento/realizacion-de-evaluaciones-de

4. AEPD — When a DPIA is required  
   https://www.aepd.es/preguntas-frecuentes/2-tus-obligaciones-como-responsable-del-tratamiento/10-evaluacion-de-impacto/FAQ-0226-en-que-supuestos-es-necesario-realizar-una-evaluacion-de-impacto

5. AEPD — Article 35.4 DPIA risk list  
   https://www.aepd.es/documento/listas-dpia-es-35-4.pdf

6. AEPD — Risk management and DPIA guidance  
   https://www.aepd.es/prensa-y-comunicacion/notas-de-prensa/aepd-publica-nueva-guia-gestionar-riesgos-y-evaluciones-impacto

7. AEPD — Consent age for minors  
   https://www.aepd.es/preguntas-frecuentes/10-menores-y-educacion/FAQ-1001-cual-es-la-edad-para-que-los-menores-puedan-prestar-consentimiento-para-tratar-sus-datos-personales

8. European Data Protection Board — Children  
   https://www.edpb.europa.eu/topics/key-gdpr-concepts/children_en

9. European Data Protection Board — DPIA template / guidance (2026)  
   https://www.edpb.europa.eu/public-consultations/template-for-data-protection-impact-assessment_en

---

# 41. Repository evidence used

This assessment was reconciled against the committed Round 2 baseline:

`661c027 — Build Round 2 KinderFlow MVP and UX`

Relevant repository evidence includes:

- `mvp/mvp_documentation.md`
- `prototype/README.md`
- `prototype/school.html`
- `prototype/school.js`
- `prototype/family.html`
- `prototype/create-sign.html`
- `prototype/create-sign.js`
- `content_ops/`
- `workflow/kinder_signs_n8n_workflow.md`

## Repository facts carried into this assessment

- no child video is required;
- adult reference video is processed locally in the current MVP;
- school/child/family prototype records are fictional;
- the school assignment layer is prototype-stage;
- real authentication/persistence is not implemented;
- local run storage has no formal retention policy;
- content-generation inputs do not require child identity;
- LangSmith applies to LLM content observability, not CV;
- production security, identity and school integration remain future deployment requirements.

## Documentation gap still open

The root `README.md` retains some older Round 1 product wording and should be reconciled with the frozen Round 2 architecture before final submission.
