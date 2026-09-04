# Kinder Signs Privacy Facts

**Functional evidence baseline:** 8eb0742; final closure evidence is recorded on `release/capstone-demo`
**Scope:** Current local MVP and proposed controlled pilot

This fact sheet is a repository writing control. It is not legal advice or a privacy certificate. Use the [full GDPR record](../compliance/gdpr_documentation.md) for the processing register, role analysis, retention, rights, recipients, transfers, security, and DPIA screen.

## Current local MVP

| Item | Current fact |
| --- | --- |
| Reference subject | Intended to be an adult |
| Input | Registered MORE demo, local MP4 upload, or bounded public direct MP4 URL |
| Processing | Local OpenCV and MediaPipe |
| Artifacts | Local video copy, landmarks, metrics, plots, and previews |
| Nursery data | Synthetic Little Steps Nursery fixture |
| Child and family data | Synthetic labels such as Child A to Child F; no real accounts |
| Assignment | Local or session-based prototype |
| Family View | Assignment-driven mini-library at local/session scope, not production delivery |
| LLM and LangSmith | No evidenced live transfer of personal data |
| Child media | None in intended core scope |
| Age estimation | Not implemented or claimed |

An identifiable adult video is personal data. Pose and hand landmarks can also be personal data when they remain linkable to that adult.

The current system does not use landmarks to identify a person. It does not infer emotion or estimate age. Special-category biometric treatment would require processing for unique identification, which is not the current purpose.

## Direct MP4 URL

The local service:

- accepts a public HTTP or HTTPS direct MP4;
- rejects local and private targets;
- validates resolved addresses and redirects;
- limits type, size, time, and redirects;
- writes a generated local file;
- cleans failed partial files; and
- strips the URL query from persisted provenance.

The remote host still receives request metadata such as the service's public IP and user-agent. The local service receives and stores the video. The control does not prove source rights, performer consent, sign correctness, or malware safety.

## Family View boundary

An assignment-driven Family Experience exists at local, session-based MVP scope. School Admin stores a synthetic group or fictional-child assignment in browser/session state, and Family View displays the corresponding sign and materials. This does not establish a real family identity, account, relationship, or entitlement.

The current screens do not prove:

- real caregiver identity;
- family-to-child relationship verification;
- nursery separation;
- persistent assignments;
- notifications; or
- secure delivery to family accounts.

## Proposed pilot minimum

Use group assignment by default.

Potential pilot data:

- nursery account;
- administrator and educator identity;
- role and access events;
- group ID;
- sign and material assignment;
- authorised family contact or access credential;
- pseudonymous child assignment ID only when individual assignment is necessary;
- review and publication log;
- minimal security, support, notice, and request records; and
- aggregated or pseudonymous pilot measures.

Exclude by default:

- child video, voice, or photograph;
- health, diagnosis, disability, or development data;
- emotion or behaviour inference;
- learning or ability scores;
- free-text child observations;
- family history; and
- personal data in LLM or LangSmith prompts and traces.

## Role and legal-basis questions

The nursery is likely controller for its child and family relationship records. KinderFlow may be processor when it stores assignments only on documented nursery instructions. KinderFlow may be controller for its own account administration, security, and adult-reference content production.

These are working assumptions. Contracts and actual purposes decide the roles.

Before pilot:

- assign a controller and processor for every purpose;
- select and document an Article 6 basis for every activity;
- complete Article 28 terms where KinderFlow is processor;
- avoid bundled consent;
- assess GDPR Article 8 only if a service is offered directly to a child and relies on consent;
- complete a vendor and international-transfer record; and
- complete the DPIA.

## Retention facts

Current local run artifacts remain until manually removed. Git ignore is not deletion.

Proposed pilot targets include:

- adult source: delete within 30 days after review closes;
- landmarks and technical previews: delete within 90 days after the final content decision unless a smaller approved evidence subset is required;
- account data: delete or anonymise within 30 days after the relationship ends, subject to legal records;
- assignments: delete within 90 days after the service need ends;
- security logs: 90 days unless an active incident requires longer;
- row-level pilot measures: aggregate and delete within 30 days after the pilot decision; and
- publication decisions: keep for the active life plus 12 months after withdrawal.

These are proposed design targets, not implemented policy. The controller must approve or replace them and test deletion across active stores, exports, temporary files, and backups.

## Rights, recipients, and incidents

The pilot needs an authenticated process for information, access, correction, deletion, restriction, portability where applicable, objection where applicable, and withdrawal where consent is used.

Current local processing has no evidenced live transfer of personal data to an LLM or LangSmith recipient. A public direct-video host sees the fetch request. Gemini FX files were prepared separately; their original provider-side source, location, retention, and transfer facts are not documented.

A separate [screenshot](../workflow/evidence/n8n_successful_execution_2026-08-31.png) evidences a successful historical n8n governed-draft execution on 31 August 2026 at 21:30:27 (execution #21441, 14.499 seconds). It does not evidence that adult, child, family, or nursery personal data was transferred, that the later final MVP adapter ran, or that n8n was deployed to production. The OpenAI course credential used at that time was removed or revoked; a fresh provider-backed rerun requires a new authorised credential, and the former key must not be reconstructed or exposed.

Every pilot vendor needs a recorded purpose, role, data, sub-processor list, location, retention, security, deletion, and transfer mechanism.

The pilot also needs a tested breach and content-withdrawal process. The controller must assess supervisory-authority and individual notification under GDPR Articles 33 and 34 for each qualifying incident.

## DPIA fact

The proposed persistent family-access flow concerns children as vulnerable data subjects and may combine new technology, account linkage, and targeted assignment. A complete DPIA is a pilot gate, even if the first design is group-first.

Stop before live data if:

- an individual child ID is not necessary;
- a wrong family can access an assignment;
- personal data can enter an AI or monitoring path;
- vendor locations or transfers are unknown;
- deletion cannot be demonstrated; or
- high residual risk remains unresolved.

## Evidence

- [Local processing and direct URL code](../mvp/pipeline.py)
- [Local routes](../mvp/app.py)
- [Current tests](../mvp/tests/test_prompt_3.py)
- [Prototype documentation](../prototype/README.md)
- [Canonical asset registry](../assets/registry/sign_asset_registry.json)
- [GDPR text](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
