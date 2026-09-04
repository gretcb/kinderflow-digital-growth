# KinderFlow GDPR Data-Flow and Pilot Readiness Record

**Assessment date:** 4 September 2026
**Functional evidence baseline:** 8eb0742, Freeze connected KinderFlow capstone demo
**Round 2 closure context:** `release/capstone-demo` adds the deployment pin, reconciled documentation, and final submission evidence without changing the demonstrated product baseline
**Scope:** Current local MVP and proposed controlled pilot

This record supports product and pilot decisions. It is not legal advice, a completed record of processing activities for a legal entity, or a compliance certificate. The controller must confirm the real purposes, roles, legal bases, contracts, retention periods, recipients, transfers, and safeguards before processing pilot data.

## Executive conclusion

The current local MVP has a narrow data footprint. It processes an adult reference video locally and creates technical run artifacts. It uses synthetic Little Steps Nursery, family, and child records. Its assignment-driven Family Experience is implemented only in browser/session state; it has no real child or family accounts, no production family delivery, and no evidenced live transfer of personal data to an LLM or LangSmith.

The bounded direct MP4 route adds an external source to the current flow. The remote host receives network request data, and the local service receives the adult video. The service strips the query string from persisted provenance, but that control does not establish source rights or consent.

A pilot would introduce persistent nursery and user data. The safest design is group-first. A pseudonymous child assignment identifier should exist only when an individual assignment is necessary. Real pilot processing requires a completed data protection impact assessment, role and legal-basis decisions, notices, contracts, access controls, retention and deletion, recipient and transfer records, incident handling, and data-subject request operations.

## Data-protection principles

KinderFlow should apply the following design rule:

> Use the minimum personal data needed to connect approved content with the correct nursery group or authorised family account. Keep personal data out of Computer Vision, LLM, and LangSmith processing whenever the function does not require it.

| Principle | Current evidence | Pilot requirement |
| --- | --- | --- |
| Purpose limitation | Adult video is used for technical content review | Fix each account, assignment, support, and analytics purpose |
| Data minimisation | Core Computer Vision needs an adult reference, not a child | Prefer group assignment; create a child ID only if necessary |
| Accuracy | Synthetic fixtures can be corrected locally | Provide correction and relationship-verification processes |
| Storage limitation | Runs remain local until manually removed | Approve and automate a retention schedule |
| Integrity and confidentiality | Local bounds and direct-URL controls exist | Add identity, access, encryption, tenancy, monitoring, backup, and incident controls |
| Accountability | Versioned documentation and registries exist | Record controller decisions, reviews, contracts, training, and requests |

## Current local MVP

### Data subjects and data categories

| Data subject | Data | Personal-data assessment |
| --- | --- | --- |
| Adult reference performer | Image, movement, pose and hand landmarks, and possible voice in source video | Personal data when the person is identifiable or linkable |
| Operator | Local interaction and operator-declared reference status | Personal data only if linked to an identified operator; current app has no account |
| Remote video host or service user | Network address and request metadata | The remote host can receive the local service's public IP and user-agent string |
| Nursery staff, families, and children | Little Steps Nursery fixture, group labels, Child A to Child F, and family preview content | Synthetic prototype data, not real records |

File names, source type, a redacted source URL, run identifier, timestamps, warnings, and review choices may also become personal data if they can be linked to an individual.

### Video and landmark nuance

An identifiable adult video is personal data. Pose and hand landmarks can also be personal data when retained with identifiers or when they can reasonably be linked back to the person.

The current service does not use landmarks to uniquely identify anyone. It does not compare identity templates, infer emotion, estimate age, or assess a child. On the current purpose, the landmarks are not processed as special-category biometric data for unique identification. A later identity function would require a new Article 9 analysis and a new EU AI Act assessment.

### Current data flow

| Stage | Data movement | Storage | Current boundary |
| --- | --- | --- | --- |
| 1. Source selection | Operator selects registered MORE demo, uploads an MP4, or provides a public direct MP4 URL | Browser and local service | Visible `Reviewed reference` copy sends the internal `Validated reference` value; this operator declaration does not independently prove authority, consent, or licence |
| 2. Direct URL fetch | Remote host sends MP4 bytes to the local service | Temporary local staging file | Scheme, address, redirects, MIME, size, time, and cleanup are bounded |
| 3. Local processing | OpenCV and MediaPipe read frames and extract landmarks | Local run directory | No cloud Computer Vision service is evidenced |
| 4. Technical evidence | Service writes raw and normalized landmarks, summaries, plots, and previews | Local MVP run artifacts | Git ignores the run directory; that is not a retention or security control |
| 5. Review | Operator views evidence and chooses a route or pose | Local process and browser state | No authenticated reviewer ledger |
| 6. Product prototype | A synthetic group or fictional-child assignment moves from School Admin to the corresponding Family View | Browser/session state | Assignment-driven mini-library works locally; no real accounts, durable service, or production delivery |
| 7. Optional wording evaluation | Approved sign and routine content can enter deterministic checks or dry-run evaluation | Local JSON evidence | No live LLM or LangSmith personal-data transfer is evidenced |

The direct URL implementation:

- accepts HTTP or HTTPS public targets;
- rejects credentials, fragments, local names, private addresses, unsafe ports, and non-global resolved addresses;
- pins validated addresses and revalidates redirects;
- rejects an HTTPS-to-HTTP downgrade;
- enforces an MP4 content type, 100 MB cap, redirect limit, and total timeout;
- writes a generated local filename;
- removes partial files on failure; and
- removes the query string from persisted provenance.

The remote source still sees a request, public network address, and KinderFlow user-agent. HTTP remains permitted. The service validates transport and file shape, not the performer's identity, consent, source licence, sign meaning, or malware safety.

Evidence:

- [Direct URL and local processing code](../mvp/pipeline.py)
- [Local service routes](../mvp/app.py)
- [Current security and provenance tests](../mvp/tests/test_prompt_3.py)
- [MVP reality check](../docs/mvp_reality_check.md)

### Current synthetic product records

The nursery and Family View use fictional Little Steps Nursery records, group labels, and Child A to Child F examples. Assignment state is local or session-based. School Admin stores the selected sign, materials, and group or fictional child; Family View reads that state, and exact duplicate assignments are blocked. This proves the assignment-driven mini-library at local/session MVP scope only.

The current experience is not evidence of real delivery, family identity verification, authentication, authorisation, durable cross-session or cross-device persistence, account or nursery separation, notifications, or production correction and deletion operations.

### Current asset and model boundaries

The six-sign registry contains reference videos, functional illustrations, source records, hashes, and draft output assets. Hashes support identity and change detection. They do not prove ownership, consent, or lawful processing.

Open Peeps supplies a CC0-recorded character and line grammar. It does not provide personal-data evidence or sign mechanics.

The three Gemini FX files are local pre-generated demo outputs:

- MORE maps to mas.mp4;
- HELP maps to ayuda.mp4; and
- MILK maps to leche.mp4.

EAT, SLEEP, and WATER have no current Gemini FX output. The files were prepared separately and are not generated from current landmarks. Their original provider-side processing, source inputs, location, and retention are not evidenced in this repository. Do not use them externally until those facts and usage rights are recorded.

## Proposed pilot

### Minimum pilot data

| Category | Minimum data | Excluded by default |
| --- | --- | --- |
| Nursery account | Nursery ID, name, status, contract reference | Unrelated business records |
| Staff user | Name, work email, role, authentication and access events | Personal phone and free-text profile |
| Group assignment | Group ID, sign ID, material IDs, dates, state, creator | Child identity |
| Family access | Authorised contact or access credential only when required | Household profile, unrelated family history |
| Individual assignment | Pseudonymous child assignment ID only when group delivery cannot meet the purpose | Child name in AI inputs, health, development, diagnosis, media |
| Review and publication | Reviewer, source, rights record, version, decision, rationale, timestamp | Unnecessary performer or child details |
| Support | Contact, issue category, response, resolution | Open-ended sensitive notes |
| Security and audit | Actor, event, time, object, result, network and device data as justified | Content beyond the event purpose |
| Measurement | Aggregated or pseudonymous assignment, access, time, and reuse measures | Behavioural profiling or child scores |

The pilot should not collect child video, voice, photographs, health data, developmental data, diagnostic information, free-text educator observations, emotion data, or learning scores.

### Proposed pilot data flow

1. KinderFlow creates an approved, versioned sign package without child or family data.
2. An authorised nursery administrator selects an approved sign, group, material set, and audience.
3. The assignment service stores a nursery and group assignment.
4. If an individual assignment is necessary, the service stores a pseudonymous assignment ID separated from the nursery's identity record.
5. An authorised family account receives access to reviewed content through a production access-control layer.
6. The service records minimal delivery, access, correction, and security events.
7. Pilot reporting uses aggregated or pseudonymous measures.
8. No school, family, or child identifier enters the Computer Vision, LLM, or LangSmith content path.

The local/session assignment-driven family mini-library exists. The pilot plan must build and test the identity, access, durable persistence, tenant separation, notification, delivery, correction, and deletion layers before claiming production end-to-end family delivery.

## Controller and processor assumptions

Roles follow actual decisions and contracts, not product labels.

| Processing | Working assumption | Decision required |
| --- | --- | --- |
| KinderFlow's internal adult-reference production | KinderFlow may act as controller if it decides why and how to use the reference | Identify legal entity, source, rights, lawful basis, and retention |
| Nursery staff and child or family relationship records | Nursery is likely controller for its educational and family-communication purposes | Confirm school type, applicable law, and purpose |
| KinderFlow hosting school-directed assignments | KinderFlow may be processor when acting only on documented nursery instructions | Sign Article 28 terms and prohibit secondary use |
| KinderFlow product security and service administration | KinderFlow may be independent controller for limited security and business-account purposes | Separate those purposes in notices and RoPA |
| Model, hosting, monitoring, or support vendors | Processor or sub-processor status depends on service and data | Complete vendor and transfer review |
| Joint product or measurement decisions | Joint controllership may arise if purposes and essential means are decided together | Avoid or document allocation transparently |

The current repository does not settle these roles.

## Processing-activities register

### Current development activities

| Activity | Purpose | Data and subjects | Working role | Legal-basis question | Recipients or transfers | Retention state |
| --- | --- | --- | --- | --- | --- | --- |
| Adult reference intake | Create technical movement evidence | Adult image, movement, possible voice, source metadata | KinderFlow controller assumption | Consent, contract, or legitimate interests must be assessed against the actual relationship | Local operator and service; remote host supplies direct-URL file | Manual deletion; no automatic limit evidenced |
| Computer Vision run | Extract and review landmarks and previews | Adult video, landmarks, metrics, artifacts | Same as source activity | Same purpose and basis; necessity must be documented | Local process only | Manual deletion |
| Direct URL retrieval | Receive one public MP4 | Source URL, request metadata, adult video | KinderFlow controller assumption | Authority to retrieve and use content must be documented | Public source host sees request metadata | Query stripped in stored provenance; local video follows run retention |
| Synthetic product demonstration | Demonstrate assignment-driven nursery and Family View interactions | Fictional records only | Not a real personal-data activity on current evidence | Not applicable to synthetic fixtures | Local browser and service | Browser/session state |
| Optional family-copy dry-run | Test bounded output and quality rules | Approved sign and routine content | Internal development | No personal data should be used | Local files; no live LangSmith or LLM call evidenced | Versioned sample evidence |
| Asset registry | Preserve identity, mapping, provenance, and rights status | Asset metadata; may include creator attribution | KinderFlow controller assumption | Legitimate documentation purpose to confirm | Repository reviewers | Versioned while evidence is needed |

### Proposed pilot activities

| Activity | Purpose | Data and subjects | Expected role | Candidate Article 6 basis | Recipients | Transfer and retention status |
| --- | --- | --- | --- | --- | --- | --- |
| Nursery account and contract | Provide and administer service | Decision-maker and staff contact data | KinderFlow controller for account administration | Contract or legitimate interests, subject to final analysis | Authorised KinderFlow staff and hosting provider | Vendor and period TBD before pilot |
| User authentication and role access | Protect nursery and family content | User identity, credential metadata, access events | Controller or processor by context | Contract, legitimate interests, or legal obligation as applicable | Identity and hosting providers | Vendor, region, and period TBD |
| Group assignment | Make reviewed content available to a group | Nursery, group, sign, materials, actor, status | Nursery controller; KinderFlow processor assumption | Nursery must document its basis | Authorised staff, family users, service providers | Period TBD; no model transfer |
| Optional individual assignment | Deliver content when group assignment is insufficient | Pseudonymous child assignment ID and authorised family link | Nursery controller; KinderFlow processor assumption | Nursery must establish necessity and basis | Authorised nursery and linked family only | Separate identity mapping; period TBD |
| Family access | Let an authorised caregiver view reviewed material | Contact or credential, content access, language choice | Role depends on account design | Contract, public task, legitimate interests, or another applicable basis | Authorised user and service providers | Period TBD |
| Review and publication log | Prove content decision and support correction | Reviewer identity, asset, source, decision, rationale | KinderFlow controller | Legitimate interests and accountability may apply | Authorised operations, auditors, regulators where required | Proposed 12 months after withdrawal, subject to approval |
| Security logging | Detect misuse and investigate incidents | Account, event, time, network and device data | Each party for its security purpose | Legitimate interests or legal obligation, subject to balancing | Security and hosting providers | Proposed 90 days, longer only for an active incident |
| Support | Resolve service and rights issues | User contact, ticket, response | Role depends on issue | Contract or legitimate interests | Support provider if used | Proposed 90 days after closure |
| Pilot measurement | Decide whether to continue | Aggregated or pseudonymous use, time, reuse, and issue measures | Define before collection | Legitimate interests or agreed pilot purpose, subject to balancing | Pilot team and nursery | Delete row-level data after pilot decision; retain approved aggregate |

Candidate bases are decision prompts, not final conclusions. The controller must document necessity, reasonable expectations, balancing, and national education law. Consent should not be used as a default when it is not freely given or when another basis better reflects the service.

## Lawful-basis and special-category questions

### Adult reference performer

Before using a real adult reference, record:

- who the person is in relation to KinderFlow;
- who supplied the recording;
- what uses were explained;
- whether the recording can be adapted, reviewed, displayed, or redistributed;
- the selected Article 6 basis and its rationale;
- withdrawal or objection handling where relevant; and
- the deletion date.

The visible `Reviewed reference` copy maps to the internal `Validated reference` value. That operator statement is not consent evidence, a licence, professional validation, or proof of source authority.

### Children and family accounts

The nursery must identify the legal basis for service and family communication under its real educational context. If an information-society service is offered directly to a child and relies on consent, GDPR Article 8 and Spain's national age rule require a separate analysis. The current product has no child-directed account.

KinderFlow should not infer a child's age. No automated minor-age estimation appears in the frozen code.

### Special-category data

The pilot design should exclude health, diagnosis, disability, and other Article 9 data. Adult landmarks are not processed for unique identification in the current workflow.

If identity verification, health tailoring, or another special-category purpose is proposed, stop design work until an Article 9 condition, necessity analysis, DPIA, security design, and EU AI Act reassessment are complete.

### Automated decisions

The current system makes no solely automated decision with legal or similarly significant effects on a child or adult. It does not score or assess children.

If a future recommendation affects access, placement, support, or another significant outcome, KinderFlow must reassess GDPR Article 22, transparency, contestability, human intervention, and the EU AI Act before implementation.

## Retention and deletion

The frozen MVP has no automatic run-retention control. Git ignore rules do not delete or secure local artifacts.

The following limits are proposed pilot targets, not implemented policy:

| Record | Proposed maximum | Trigger and action | Owner |
| --- | --- | --- | --- |
| Raw adult source and temporary direct-URL file | 30 days after review closes | Delete earlier when no longer needed | Content Operations |
| Raw and normalized landmarks and technical previews | 90 days after final content decision | Retain only the approved evidence subset afterward | Content Operations |
| Rejected or abandoned draft visual | 30 days after decision | Delete unless needed for an active complaint | Content Operations |
| Published content decision and source record | Active life plus 12 months after withdrawal | Preserve correction and accountability evidence | Product Owner |
| Nursery and staff account | Contract life plus 30 days | Delete or anonymise except required finance or legal records | Account owner |
| Group or individual assignment | Active service need plus 90 days | Delete relationship data; retain approved aggregate only | Nursery controller |
| Family credential or contact | Account life plus 30 days | Revoke immediately on relationship change | Nursery controller |
| Security event | 90 days | Extend only for an active investigation | Security owner |
| Support ticket | 90 days after closure | Remove sensitive attachments earlier | Support owner |
| Row-level pilot measurement | Until pilot decision plus 30 days | Aggregate and delete row-level identifiers | Pilot lead |

The controller must approve or replace these values after checking legal obligations, school calendars, complaint periods, backup behaviour, and technical feasibility. Deletion must cover active systems, local exports, temporary files, and scheduled backup expiry.

## Recipients, processors, and transfers

### Current recipients

Current identifiable adult content remains on the local machine in the evidenced flow. The local operator and operating-system processes can access it. A direct video host receives the fetch request and network metadata. The repository does not evidence a live upload of the adult video, landmarks, or school or family data to OpenAI, LangSmith, Google, or another model provider.

A separate [screenshot](../workflow/evidence/n8n_successful_execution_2026-08-31.png) evidences a successful historical n8n governed-family-draft execution on 31 August 2026 at 21:30:27 (execution #21441, 14.499 seconds). It does not evidence that adult, child, family, or nursery personal data was transferred, that the later final MVP Content Pack adapter was exercised, or that n8n was deployed to production. The OpenAI course credential used at that time was removed or revoked shortly afterwards; a new authorised credential would be required for a fresh provider-backed rerun, and the former key must not be reconstructed or exposed.

The Gemini FX output files were prepared before or outside the current runtime. Their provider-side source, account, processing location, retention, and transfer history are not documented here.

### Pilot due diligence

Before selecting a hosting, identity, analytics, support, model, or monitoring service, record:

1. legal entity and service;
2. data categories and purposes;
3. controller, processor, or sub-processor role;
4. processing and support locations;
5. sub-processor list and change notice;
6. retention and deletion behaviour;
7. security measures and incident notification;
8. training or secondary-use settings;
9. international transfer mechanism;
10. transfer impact assessment and supplementary measures where required; and
11. exit, export, and deletion process.

No personal child, family, nursery, or staff data should enter an LLM or LangSmith during the pilot. If that rule changes, update the RoPA, notice, contracts, DPIA, transfer assessment, and EU AI Act record before the change.

## Security controls

### Current evidence

- local loopback service;
- controlled upload validation;
- bounded direct MP4 retrieval;
- private and local target rejection;
- pinned public address and redirect revalidation;
- response type, byte, and time limits;
- generated run names and failed-run cleanup;
- query-redacted direct-URL provenance;
- same-origin check when an Origin header is present; and
- registry hashes and path validation.

### Production gaps

- authentication and multi-factor options;
- role-based authorisation;
- family-to-child relationship verification;
- nursery tenant separation;
- encryption in transit and at rest;
- key and secret management;
- host allowlist or controlled object-store intake;
- rate, quota, and concurrency controls;
- isolated and patched media decoding;
- malware and content-safety handling;
- central audit and anomaly logging;
- tested backup and deletion;
- vulnerability and dependency management;
- incident response and data-breach workflow; and
- availability and disaster recovery.

The pilot must use a production security design. The local direct-URL controls cannot be treated as that design.

## Data-subject rights

Before pilot, the controller must provide a route for:

- transparent information;
- access;
- correction;
- deletion;
- restriction;
- portability where applicable;
- objection where applicable;
- withdrawal of consent where consent is used;
- information about recipients and transfers; and
- human contact about any automated process.

The operating procedure should:

1. authenticate the requester without collecting excessive evidence;
2. record the request and deadline;
3. search active systems, local exports, support records, and processor systems;
4. coordinate controller and processor duties;
5. apply a documented exception where lawful;
6. respond in accessible language; and
7. preserve a minimal accountability record.

The current prototype has no rights-request interface or operating process.

## Incident handling

Before pilot, KinderFlow and each nursery should agree:

- how staff report a suspected incident;
- who contains and investigates it;
- who decides controller notifications;
- how processors notify the controller without undue delay;
- how affected records, users, and versions are identified;
- when the supervisory authority notification under Article 33 is required;
- when communication to affected people under Article 34 is required;
- how an incorrect sign or rights breach is withdrawn; and
- how lessons and corrective actions enter change control.

The incident register should include facts, impact, containment, notification decision, timing, owner, and follow-up. The 72-hour GDPR notification period applies to a controller's supervisory-authority notice when the legal threshold is met. It is not a general deadline for every event.

## Short data protection impact assessment

### Proposed processing assessed

The highest-risk proposed flow is a persistent family mini-library in which an authorised caregiver sees content selected for a nursery group or, only when necessary, a pseudonymous child assignment.

### Necessity and proportionality

The service goal can usually be met with a group ID, approved sign ID, material ID, and authorised family access. Child identity, media, health information, developmental notes, and free text are not necessary for content preparation. Individual linkage should be an exception.

### Risk screen

| Risk | Potential impact | Initial level | Required control | Residual decision |
| --- | --- | --- | --- | --- |
| Wrong family accesses an individual assignment | Confidentiality and trust harm involving a child | High | Verified relationship, tenant isolation, deny-by-default access, access tests, rapid revocation | Must be reassessed after testing |
| Child identity spreads into AI or monitoring tools | Loss of control and unexpected processing | High | Architectural separation, blocked fields, provider configuration, logs, contract prohibition | Pilot must stop on any transfer |
| Persistent use enables profiling | Unfair inference or pressure on a child or family | High | No scores, no behavioural profile, aggregate measurement, purpose checks | Accept only if tests prove absence |
| Adult reference lacks authority or consent | Rights and reputational harm | High | Source contract, purpose notice, rights record, expiry and deletion | No source enters production without evidence |
| Incorrect sign or visual reaches a family | Safety, trust, and communication harm | High | Qualified sign review, publication gate, version withdrawal, complaints route | Unreviewed delivery must remain zero |
| Account or support data is exposed | Identity and relationship disclosure | High | Authentication, authorisation, encryption, monitoring, incident process | Security test required |
| Data is kept too long | Unnecessary exposure | Medium | Approved schedule, automated deletion, backup expiry tests | Measure deletion completion |
| Vendor or international transfer is unknown | Loss of control and unlawful transfer risk | High | Vendor register, DPA, location, SCC or other mechanism, transfer assessment | No vendor until closed |

### DPIA conclusion

Children are vulnerable data subjects, and the proposed service may combine new technology, persistent accounts, and targeted family access. A complete DPIA is a pilot gate even if the first pilot uses group assignments. The AEPD states that a DPIA is required when processing is likely to create high risk and notes that two or more risk criteria generally indicate that one is expected.

The DPIA is not complete until the actual architecture, controllers, vendors, countries, data fields, retention, security test evidence, and residual-risk acceptance are fixed. Consult the supervisory authority if high residual risk remains and Article 36 requires it.

## Pilot gates

| Client fact | Action | Target | Owner | Decision rule |
| --- | --- | --- | --- | --- |
| Current nursery and family data are synthetic | Approve a minimum pilot data dictionary | No child media, health, development, emotion, or score fields | Privacy lead and nursery controller | Reject any unapproved field |
| Individual identity is not needed for most assignments | Implement group-first assignment | Pseudonymous child ID only for documented necessity | Product Owner | Stop if the design defaults to named children |
| Roles are assumptions | Sign controller, processor, and sub-processor allocation | All purposes assigned before data collection | Legal and privacy owners | No real data until complete |
| Legal bases remain undecided | Complete purpose-by-purpose Article 6 analysis | Decision and rationale recorded for every activity | Controller | Do not rely on bundled consent |
| Retention is manual | Implement and test deletion | One hundred percent of test records follow approved schedule | Engineering and privacy owner | No pilot if deletion cannot be demonstrated |
| Production family identity and delivery are not implemented | Build secure access, durable persistence, tenant isolation, and relationship verification around the local/session mini-library | Cross-family and cross-nursery access tests pass | Engineering and security owner | Zero wrong-recipient access |
| Vendor and transfer map is empty | Complete DPA, sub-processor, location, and transfer review | Written evidence for every vendor | Privacy and procurement owners | No undeclared recipient |
| DPIA is only a short screen | Complete the DPIA and residual-risk decision | Signed before live pilot | Controller and DPO or adviser | Stop if high residual risk lacks a lawful resolution |
| Rights and incident processes do not exist | Test requests, revocation, breach handling, correction, and withdrawal | Exercise completed before launch | Privacy, security, and Content Operations | No pilot without accountable owners |

## Official references

- [General Data Protection Regulation, Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- [AEPD guidance on when a DPIA is required](https://www.aepd.es/preguntas-frecuentes/2-tus-obligaciones-como-responsable-del-tratamiento/10-evaluacion-de-impacto/FAQ-0226-en-que-supuestos-es-necesario-realizar-una-evaluacion-de-impacto)
- [AEPD risk and DPIA resources](https://www.aepd.es/derechos-y-deberes/cumple-tus-deberes/medidas-de-cumplimiento/realizacion-de-evaluaciones-de)
- [European Data Protection Board guidelines](https://www.edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en)

These sources do not replace purpose-specific advice for the actual legal entities and pilot design.
