# Kinder Signs EU AI Act Facts

**Frozen baseline:** 8eb0742
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
| Optional model path | Can draft bounded wording; repository evidence is local and dry-run, not a live provider run |
| LangSmith | Dry-run evidence covers the optional wording step only |
| n8n | Importable workflow and documentation exist; final target-runtime execution is unclaimed |
| Open Peeps | Supplies the CC0-recorded character and line grammar only; reviewed references determine sign mechanics |
| Gemini FX | MORE maps to mas.mp4, HELP to ayuda.mp4, and MILK to leche.mp4; EAT, SLEEP, and WATER have no current output |
| Nursery and Family Views | Local prototype with synthetic and session-based state; personalised family delivery is pending |

The Gemini videos were prepared separately as illustrative motion previews. They are not generated automatically from the current MediaPipe run or its landmarks. Rights, external display, sign review, and Article 50 decisions remain open.

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
- A family guidance preview exists. A personalised assignment-driven family library does not.

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
- [LangSmith dry-run](../workflow/langsmith_dry_run_summary.json)
- [Official consolidated EU AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689)
