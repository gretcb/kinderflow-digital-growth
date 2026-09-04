# Kinder Signs EU AI Act Facts

**Functional evidence baseline:** 8eb0742; final closure evidence is recorded on `release/capstone-demo`
**Status:** Preliminary intended-purpose assessment

This fact sheet is a writing control for the KinderFlow repository. It is not legal advice or a compliance certificate. Use the [full EU AI Act assessment](../compliance/eu_ai_act_compliance.md) for reasoning and gates.

## Current intended purpose

Kinder Signs turns reference video into Computer Vision evidence for human content review. It supports preparation of reviewed sign visuals and family guidance.

The current intended purpose does not:

- admit students;
- determine access to education;
- assign an educational level;
- evaluate learning outcomes;
- proctor tests;
- assess, score, or profile children;
- recognise emotion;
- identify or categorise people biometrically; or
- make automated educational decisions.

The current use therefore does not appear to perform the education or biometric functions reviewed in Annex III. State the reasoning. Do not replace it with a generic risk label.

## Current component facts

| Component | Fact |
| --- | --- |
| MediaPipe | Extracts adult pose and hand landmarks for technical review |
| OpenCV and ffmpeg | Support video processing and previews; they are not treated as AI by themselves |
| Optional model path | Can draft bounded wording; current final MVP adapter evidence is local and dry-run, while the separate n8n POC has historical execution evidence |
| LangSmith | Separate observability/evaluation component; committed evidence is a dry-run for the optional wording step only, not a live trace or Computer Vision validation |
| n8n | Exact 12-node export plus screenshot of a successful historical governed-draft execution; complete at capstone low-code POC scope, not production deployment |
| Open Peeps | Supplies the CC0-recorded character and line grammar only; reviewed references determine sign mechanics |
| Gemini FX | MORE maps to mas.mp4, HELP to ayuda.mp4, and MILK to leche.mp4; EAT, SLEEP, and WATER have no current output |
| Nursery and Family Views | Assignment-driven mini-library implemented with synthetic browser/session state; production identity, access, persistence, tenancy, notifications, and delivery are pending |

The Gemini videos were prepared separately as illustrative motion previews. They are not generated automatically from the current MediaPipe run or its landmarks. Rights, external display, sign review, and Article 50 decisions remain open.

The [n8n execution screenshot](../workflow/evidence/n8n_successful_execution_2026-08-31.png) records **Kinder Signs — Governed Family Draft (Example)** succeeding on 31 August 2026 at 21:30:27, execution ID #21441, in 14.499 seconds. Status: **COMPLETE AT CAPSTONE LOW-CODE POC SCOPE**. This historical execution is not autonomous publication, production deployment, or proof that the later final MVP Content Pack adapter was exercised. The OpenAI course credential used at the time was removed or revoked shortly afterwards, so a fresh provider-backed rerun requires a new authorised credential; the former key must not be reconstructed, exposed, or committed.

LangSmith remains separate. Its committed dry-run does not validate hand movement, MediaPipe output, sign correctness, linguistic correctness, or professional approval.

## Human control

Computer Vision metrics measure extraction and representation. They do not certify a sign.

Humans must control:

- source and performer authority;
- technical exception review;
- sign mechanics;
- visual readability;
- family wording;
- rights;
- publication;
- correction; and
- withdrawal.

No AI output may publish autonomously.

## Current evidence limits

- A bounded direct MP4 URL is an intake route, not a webpage scraper.
- The direct URL controls transport and file shape, not rights, consent, or sign meaning.
- The six-sign registry has 18 draft static candidates, all awaiting human review.
- No current sign is registered as school-available or published.
- The older five-sign content package still assigns WATER evidence to MORE.
- Hashes prove identity and change detection, not ownership or complete security.
- An assignment-driven Family Experience exists at local, session-based MVP scope. It is not authenticated, durable, tenant-separated production family delivery.

## Reassessment triggers

Repeat the assessment before adding:

- child media or landmarks;
- age, emotion, identity, development, ability, or behaviour inference;
- scoring, ranking, profiling, or recommendations about children;
- admission, access, placement, level, testing, discipline, or support decisions;
- biometric identity or categorisation;
- autonomous generation or publication;
- live personalised family delivery;
- a new model, provider, actor, country, or intended purpose; or
- direct nursery operation of an AI component.

## Pilot gates

- approve intended purpose and prohibited uses;
- allocate provider, deployer, controller, and processor roles;
- train operators and reviewers;
- reconcile the registry and content package;
- complete sign, visual, rights, and publication reviews;
- assess Article 50 for model-assisted text and Gemini files;
- implement authenticated decisions, audit logs, correction, and withdrawal;
- close GDPR and DPIA actions; and
- complete production security review.

## Evidence

- [Local MVP](../mvp/)
- [Current tests](../mvp/tests/)
- [Canonical asset registry](../assets/registry/sign_asset_registry.json)
- [Asset inventory](../assets/registry/sign_asset_inventory.md)
- [Open Peeps provenance](../assets/flashcards/open_peeps/provenance.json)
- [n8n workflow](../workflow/kinder_signs_n8n_workflow.json)
- [n8n successful execution evidence](../workflow/evidence/n8n_successful_execution_2026-08-31.png)
- [LangSmith dry-run](../workflow/langsmith_dry_run_summary.json)
- [Official consolidated EU AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689)
