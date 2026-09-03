# KinderFlow static product prototype

This dependency-free prototype presents KinderFlow as a platform that helps nursery schools extend everyday learning and routines into the home. Kinder Signs is the first product. The primary customer is a nursery school or school group; families receive school-linked guidance and materials.

The product is intentionally role-separated:

- KinderFlow internal teams create, review, publish and control school access to content;
- schools assign available published content and manage permitted add-ons; and
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

Master Content Studio owns all content creation. Its landing page provides four explicit paths:

- Create a sign;
- Create a flashcard;
- Create a story; and
- Create a song.

Signs are foundational assets. The dependency is:

```text
Create a sign
→ Human review
→ Published sign
→ Master Content Library
→ Flashcard / Story / Song
```

A Flashcard Studio proof can begin from reviewed sign content, but it cannot become available to schools until the underlying sign and visual asset are published. `MORE` is currently the only item connected to real CV evidence. Other library examples are explicitly illustrative.

## Technology decisions

| Content type | Technology | Reason | Prototype state |
| --- | --- | --- | --- |
| Sign | Computer Vision / MediaPipe | Capture and preserve movement from a validated reference video | Existing local POC evidence |
| Flashcard | Template-based | Turn reviewed sign content into consistent printable proofs and, after publication, reusable cards | Functional internal builder |
| Story | Generative AI + quality checks + human review | Create original stories from published signs, with evaluation before use | Illustrative local prototype |
| Song | Future generative capability | Planned content format built from published signs | Concept only |

Not every problem needs generative AI.

## Create a sign

The internal MVP flow is:

`Validated reference sign video → MediaPipe processing → movement evidence → technical review → grounded visual preparation → candidate review → approved printable → Flashcard / Routine Card → EN / ES → Print as PDF`

The Create a Sign route becomes functional when it is served by the local MVP service. An operator can use the existing demo reference or select another MP4. Each run uses the real POC pipeline, produces its own movement overlay and diagnostics, and reports only metrics calculated for that input.

The browser preview is an H.264 MP4 created from the real OpenCV/MediaPipe overlay through a local ffmpeg transcode. Operator-facing outcomes are **Pass**, **Review needed**, or **Fail**. Pass uses MediaPipe key poses, Review needed uses representative reference frames, and Fail can still create a controlled review-needed pose guide from the local sign package instead of ending in an empty state.

Start it from the repository root:

~~~bash
python mvp/app.py
~~~

Then open [http://127.0.0.1:8000/create-sign.html](http://127.0.0.1:8000/create-sign.html).

No child video is required. Files remain local, every run is isolated under *mvp/runs/*, and canonical Round 1 evidence is not overwritten. Technical metrics are movement-processing signals, not linguistic correctness certification or system-wide accuracy. Technical review, visual approval and publication remain separate decisions. Production-ready avatar generation is not complete.

## Kinder Signs Flashcard Studio

The Flashcard Studio belongs exclusively to KinderFlow internal content operations. Schools and families receive reviewed flashcards but do not design them. It is a reusable content system rather than five separate cards:

```text
reviewed sign data
→ deterministic template
→ modular character asset
→ Kinder Signs hand-pose asset
→ preview
→ browser print / Save as PDF
→ Signs & Flashcards Library
```

The source model is `prototype/data/signs.json`, and `prototype/data/visual_sign_packages.json` provides the deterministic visual-preparation package resolved by `sign_id`. It contains the bilingual copy, movement brief, evidence route, character identity, candidate assets, context image and routine icon semantics needed by the renderer. MORE is the only complete end-to-end printable proof; final library release is still blocked by qualified hand review and publication approval. Selecting another record shows why it is not ready instead of rendering a misleading card.

The asset contract is documented under `assets/flashcards/`. It reserves separate locations for:

- untouched official Open Peeps monochrome SVG source files;
- a selected modular character base;
- sign-specific reference, landmark, arm/hand SVG and review files;
- optional owned or licensed contextual elements;
- template assets; and
- local exports.

Local Open Peeps and Miroodles source libraries remain unmodified working references. The runtime candidates are original controlled SVG proofs that apply the approved character direction (smile, bun2 and mid-2) without treating a generic Open Peeps pose as sign evidence. The MORE hand relationship and movement cue remain explicitly reviewable and do not claim linguistic certification.

The two controlled visual rules are:

- Flashcard: `Kinder Signs identifier → visual → sign word`.
- Routine Card: `Kinder Signs identifier → visual → sign word → routine → one guidance sentence`.

The sign name is part of the same visual unit as the illustration, not a detached page heading. English is the initial preview language; the operator can switch the output to Spanish without changing the English interface.

The intended production flow is:

`Reviewed sign → controlled template → approve visual proof → published asset → print / export`

The current MORE demo completes the local operator path: `movement evidence → controlled visual candidates → local visual approval → Flashcard or Routine Card → EN or ES → browser Print / Save as PDF`. This creates a printable proof, not a published family asset.

Controls remain intentionally limited to:

- one reviewed-sign selector, with MORE identified as the available internal proof and the other shared records clearly marked as not ready;
- output language: English or Spanish;
- card type: Flashcard or Routine Card; and
- local proof approval followed by browser print / Save as PDF.

The Flashcard uses a calm, realistic snack-time context image plus the sign illustration; the sign remains the primary educational element. The Routine Card uses the same sign illustration, a KinderFlow-style snack icon, a routine label and one guidance sentence, with no contextual photo. Browser-native Print → Save as PDF is the working export path. Print CSS places one 105 × 148 mm card on an A4 page, removes interface chrome, preserves selectable text and avoids splitting important card sections. PNG export remains disabled and honestly labelled.

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

MORE is the deepest demonstration target. Character candidates are ready for founder review and the optional contextual export path is documented. Final library readiness remains blocked by the custom reviewed hand-pose asset. The other four signs prove the shared data contract and renderer without claiming final visual assets or publication readiness.

## Story prototype

The story route accepts only a published sign and produces a short original English prototype draft. It demonstrates explicit deterministic checks, evaluator-style review dimensions, LangSmith observability boundaries and human review actions.

No live LLM, n8n or LangSmith call runs from the static page. LangSmith represents traceability for the content-transformation step; it does not validate sign biomechanics, MediaPipe output or linguistic sign correctness.

## Content operations readiness

The Master Content Library includes a five-sign readiness matrix generated by the local `content_ops` package. It keeps source, CV, content, artwork, hand review, deterministic quality gate, human review and library state separate.

Run:

```bash
python -m content_ops
```

Then serve the prototype and open `library.html`. MORE exposes the furthest available review package, including honest blocking reasons. Approval cannot bypass missing artwork, missing hand review, unapproved content or missing human publication approval. Review-screen actions are illustrative and do not persist.

## School Admin

The school sees only the content and services made available to it. It can assign available content, manage permitted add-ons and review family access. It does not see source/reference videos, MediaPipe, LangSmith, internal review, or content-production actions.

The school library overview deliberately stays concise: sign name, available formats and assignment action. Routine guidance and family wording belong in the content detail or family view, not in the library card.

The assignment flow is deliberately simple:

`Select content → Select one group → Optionally select one child in that group → Review the assignment summary → Assign`

The summary and CTA name the selected sign and destination before the action. The child dropdown is derived from the selected group. Assign another item preserves the group to make repetitive assignment faster.

The school-facing Family Overview shows broad distribution and engagement indicators plus a fictional child roster with:

`Child | Group | Parents / caregivers | Active packs`

No output-format column or sensitive individual behavior scoring is included.

## Family preview

The family route is labelled as a preview of what families receive. It contains one active sign, concise routine guidance and shared family materials. It is not an administrative dashboard and exposes no internal AI or content-production terminology.

## Boundaries

This prototype does not include authentication, billing, payments, databases, APIs, cloud persistence, production CMS capabilities, real school integrations, real child data, tracking, server-side PDF generation, production avatar fidelity or music generation.

KinderFlow controls product and published-asset availability. Schools control assignment and permitted add-ons. Families receive shared materials. Those responsibilities remain separate throughout the prototype.
