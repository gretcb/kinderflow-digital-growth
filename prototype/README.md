# KinderFlow static product prototype

This dependency-free prototype presents KinderFlow as a platform that helps nursery schools extend everyday learning and routines into the home. Kinder Signs is the first product. The primary customer is a nursery school or school group; families receive school-linked guidance and materials.

The product is intentionally role-separated:

- KinderFlow internal teams create, review, add content to the Master Content Library and control school access;
- schools assign available content and manage permitted add-ons; and
- families receive only the relevant guidance and assets shared by the school.

## How to open

No package installation is required.

Option 1:

```text
open prototype/index.html
```

Option 2:

```bash
cd prototype
python -m http.server 8000
```

Then open [http://localhost:8000](http://localhost:8000).

## Routes

- KinderFlow Hub: [http://localhost:8000/index.html](http://localhost:8000/index.html)
- KinderFlow Admin: [http://localhost:8000/admin.html](http://localhost:8000/admin.html)
- Master Content Studio: [http://localhost:8000/content-studio.html](http://localhost:8000/content-studio.html)
- Create a sign: [http://localhost:8000/create-sign.html](http://localhost:8000/create-sign.html)
- Create a flashcard: [http://localhost:8000/flashcards.html](http://localhost:8000/flashcards.html)
- Create a story: [http://localhost:8000/create-story.html](http://localhost:8000/create-story.html)
- Create a song concept: [http://localhost:8000/create-song.html](http://localhost:8000/create-song.html)
- Master Content Library: [http://localhost:8000/library.html](http://localhost:8000/library.html)
- School Admin: [http://localhost:8000/school.html](http://localhost:8000/school.html)
- Family preview: [http://localhost:8000/family.html](http://localhost:8000/family.html)

## Platform architecture

```text
KinderFlow
├── Kinder Signs — First product / active demo
├── Kinder Daily — On the roadmap
└── Kinder Food — On the roadmap
```

All modules use the same KinderFlow design system. They do not have separate logos or monograms.

KinderFlow Admin uses this primary navigation:

```text
KinderFlow Admin
├── Master Content Studio
├── Clients / Schools
├── Master Content Library
└── Metrics
```

## Master Content Studio

Master Content Studio owns all content creation. Its top-level navigation provides three task areas:

- Create a sign;
- Master Library; and
- Schools.

Flashcards, Routine Cards and Stories are derived family materials after visual review. Song is shown only as Coming soon.

Signs are foundational assets. The dependency is:

```text
Create a sign
→ Human review
→ Master Content Library
→ Make available to schools
→ Flashcard / Routine Card / Story
```

A Flashcard Studio proof requires the exact reviewed visual from the sign journey. It cannot become available to schools until the underlying sign and visual asset are added to the Master Content Library and approved for school use. The current app demo is MORE; the committed Round 1 POC evidence belongs to WATER and must never be relabelled. Other library examples are explicitly illustrative.

## Technology decisions

| Content type | Technology | Reason | Prototype state |
| --- | --- | --- | --- |
| Sign | Computer Vision / MediaPipe | Capture and preserve movement from a validated reference video | Existing local POC evidence |
| Flashcard | Template-based | Turn reviewed sign content into consistent printable proofs and, after publication, reusable cards | Functional internal builder |
| Story | Generative AI + quality checks + human review | Create original stories from signs added to the Master Content Library, with evaluation before use | Illustrative local prototype |
| Song | Future generative capability | Planned content format built from signs added to the Master Content Library | Concept only |

Not every problem needs generative AI.

## Create a sign

The internal MVP flow is:

`Choose the sign → add the reference → review the sign reference → choose one or two poses → create and approve a visual → family materials → Bilingual / Spanish → Print / Save as PDF`

The Create a Sign route becomes functional when it is served by the local MVP service. An operator can use the existing demo reference or select another MP4. Each run uses the real POC pipeline, produces its own movement overlay and diagnostics, and reports only metrics calculated for that input.

The browser preview is an H.264 MP4 created from the real OpenCV/MediaPipe overlay through a local ffmpeg transcode. Operator-facing outcomes are **Pass**, **Review needed**, or **Fail**. Evidence routing is explicit: landmark key poses, one or two operator-selected reference frames, or a knowledge/sign-reference fallback with a required rationale. EAT is sign-aware: partial hand tracking near the face does not automatically create a dead end.

MORE, HELP, EAT, SLEEP, MILK and WATER each have a controlled visual package grounded in the exact founder-selected Open Peeps bust plus the reviewed arm and hand-style references. Sign-specific arms, hands and restrained movement accents are custom layers. Local regeneration returns a different prebuilt vector composition with a new ID, path, version and verified hash; it never reorders the original options and calls no paid API.

Start it from the repository root:

~~~bash
source poc_env/bin/activate
python mvp/app.py
~~~

Then open [http://127.0.0.1:8000/create-sign.html](http://127.0.0.1:8000/create-sign.html).

Files remain local, every run is isolated under *mvp/runs/*, and canonical Round 1 evidence is not overwritten. Technical metrics are movement-processing signals, not linguistic correctness certification or system-wide accuracy. Reference review, visual approval and publication remain separate decisions. Production-ready avatar generation is not complete.

## Kinder Signs Flashcard Studio

The Flashcard Studio belongs exclusively to KinderFlow internal content operations. Schools and families receive reviewed flashcards but do not design them. It is a reusable content system rather than six separate sign-specific editors:

```text
reviewed sign data
→ deterministic template
→ modular character asset
→ Kinder Signs hand-pose asset
→ preview
→ browser print / Save as PDF
→ Signs & Flashcards Library
```

The source model is `prototype/data/signs.json`, and `prototype/data/visual_sign_packages.json` provides the deterministic visual-preparation package resolved by `sign_id`. It contains bilingual copy, the movement brief, internal routing data, character identity, candidate assets, context image and routine icon semantics needed by the renderer. Each canonical sign can enter printable creation only after its exact visual is approved; final library release is still blocked by qualified hand review and publication approval. Unknown signs fail closed instead of rendering a misleading card.

The asset contract is documented under `assets/flashcards/`. It reserves separate locations for:

- untouched official Open Peeps monochrome SVG source files;
- a selected modular character base;
- sign-specific reference, landmark, arm/hand SVG and review files;
- optional owned or licensed contextual elements;
- template assets; and
- local exports.

Local Open Peeps and Miroodles source libraries remain unmodified working references. The runtime candidates embed the unchanged registered `bust.svg` geometry as their sole character base; the registered hand/finger and shoulder/arm examples guide line grammar without supplying sign mechanics or a copied full pose. The sign-specific references define each pose, and every movement cue remains explicitly reviewable without claiming linguistic certification.

The two controlled visual rules are:

- Flashcard: `Kinder Signs identifier → visual → sign word`.
- Routine Card: `Kinder Signs identifier → visual → sign word → routine → one guidance sentence`.

The sign name is part of the same visual unit as the illustration, not a detached page heading. English is the initial preview language; the operator can switch the output to Spanish without changing the English interface.

The intended production flow is:

`Reviewed sign → controlled template → approve visual proof → add to Master Content Library → print / export`

The current local app demo is explicitly MORE. Historical POC diagnostics remain explicitly WATER supporting evidence. The visual workflow resolves each of the six canonical sign IDs to its own controlled visual options and continues through `local visual approval → Flashcard or Routine Card → Bilingual or Spanish → browser Print / Save as PDF`. This creates a printable proof; it does not add a family asset to the library.

Controls remain intentionally limited to:

- one reviewed-sign selector that resolves the six canonical signs by exact ID and shows a controlled unavailable state for unknown signs;
- output language: Bilingual or Spanish;
- card type: Flashcard or Routine Card; and
- local proof approval followed by browser print / Save as PDF.

The Flashcard uses an available routine context image plus the sign illustration; the sign remains the primary educational element. The Routine Card uses the same sign illustration, a KinderFlow-style routine icon, a routine label and one guidance sentence, with no contextual photo. Browser-native Print → Save as PDF is the only exposed export path. The dedicated A5 portrait print route removes interface chrome, preserves selectable text and avoids splitting important card sections.

When a school/group or child has the Flashcards pack active, the matching reviewed flashcard is included automatically in prepared family output. When the pack is inactive, the item can remain visible to the school as available content but is not sent to families. No billing, manual educator design, freeform editor, server-side PDF service or persistence is included.

Because the Studio loads its structured JSON source at runtime, use the local HTTP option rather than opening `flashcards.html` directly from the filesystem.

## Content Engine and reviewed handoff

The Master Content Library now demonstrates one reusable `GENERATE_CONTENT_PACK` operation for MORE, EAT, WATER, ALL DONE and HELP:

```text
approved structured context
→ human or AI-assisted review candidate
→ structured JSON
→ deterministic quality gate
→ LangSmith status (dry-run for the prototype)
→ explicit local content review
→ reviewed Flashcard Studio handoff
```

Run `python -m content_ops` before serving the prototype to regenerate `prototype/data/content_engine_demo.json`. In `library.html`, select a sign and content origin, generate the pack, inspect its JSON and gate result, then approve it locally. Only that reviewed copy can populate Flashcard Studio. Generation never edits the stored source record and never publishes content.

When served by `python mvp/app.py`, the Content Engine calls the local backend and records each run separately. Human mode uses the stored human source. LLM-assisted mode uses the configured provider when credentials and dependencies are available; otherwise it returns an explicit `DRY_RUN`. When served without the MVP backend, the page retains a clearly labelled static fallback.

LangSmith status is separate from generation mode. A live model call may still show LangSmith dry-run/unavailable if the tracing dependency is absent. LangSmith is relevant only to LLM-assisted wording and does not assess movement or sign correctness. The contracts and deterministic validation live under `content_ops/`; the service is under `mvp/`; and the n8n boundary is documented under `workflow/`.

The Content Engine remains a separate five-record wording demo. The six-sign visual system provides controlled options for MORE, HELP, EAT, SLEEP, MILK and WATER without claiming linguistic certification, printable approval or library availability. EAT uses the reviewed-reference route when movement evidence is incomplete, and unknown sign IDs fail closed.

## Story prototype

The story route currently accepts only MORE and produces a short original English or Spanish prototype draft. A non-MORE `?sign=` request shows an unavailable state instead of silently producing a MORE story. The route demonstrates explicit deterministic checks, evaluator-style review dimensions, LangSmith observability boundaries and human review actions.

No live LLM, n8n or LangSmith call runs from the static page. LangSmith represents traceability for the content-transformation step; it does not validate sign biomechanics, MediaPipe output or linguistic sign correctness.

## Content operations readiness

The Master Content Library includes a five-record content-readiness matrix generated by the local `content_ops` package. This wording demo is intentionally separate from the six canonical visual packages. It keeps source, CV, content, artwork, hand review, deterministic quality gate, human review and library state separate.

Run:

```bash
python -m content_ops
```

Then serve the prototype and open `library.html`. MORE exposes the furthest available review package, including honest blocking reasons. Approval cannot bypass missing artwork, missing hand review, unapproved content or missing human publication approval. Review-screen actions are illustrative and do not persist.

## School Admin

The School Admin route is a configured assignment-demo fixture for Little Steps Nursery. It can preview six signs, exercise assignment behavior, manage illustrative add-ons and review synthetic family access. It does not see source/reference videos, MediaPipe, LangSmith, internal review, or content-production actions. Every library card is labelled **Preview** because the canonical registry does not currently evidence any sign as published for school distribution.

The responsive school library stays concise: bilingual sign name, routine context, configured preview formats and one assignment action. The format chips model the demo plan; they are not production-availability claims.

The assignment flow is deliberately simple:

`Choose a sign → Choose a group → Choose materials → Choose everyone or one child → Review the summary → Share`

The summary and CTA name the selected sign and destination before the action. The child selector appears only for **One child** and is derived from the selected group. Exact duplicate assignments are blocked; a sign can still be shared with another group, child or material set. Active assignment cards show materials and support edit-in-place and removal. **Share another sign** preserves the group to make repetitive assignment faster. Changes persist only in the current browser session and are never sent to families.

The school-facing Family Overview shows broad distribution and engagement indicators plus a fictional child roster with:

`Child | Group | Parents / caregivers | Active packs`

No output-format column or sensitive individual behavior scoring is included.

## Family preview

The family route is labelled as a preview of what families receive. It contains one active sign, concise routine guidance and shared family materials. It is not an administrative dashboard and exposes no internal AI or content-production terminology.

## Boundaries

This prototype does not include authentication, billing, payments, databases, APIs, cloud persistence, production CMS capabilities, real school integrations, real child data, tracking, server-side PDF generation, production avatar fidelity or music generation.

KinderFlow controls what is added to the Master Content Library and made available to schools. Schools control assignment and permitted add-ons. Families receive shared materials. Those responsibilities remain separate throughout the prototype.
