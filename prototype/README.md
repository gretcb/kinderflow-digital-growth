# KinderFlow static product prototype

This dependency-free prototype presents KinderFlow as the platform and Kinder Signs as its active demonstration module. The primary customer is a nursery school or school group; families receive school-linked guidance and published materials.

The product is intentionally role-separated:

- KinderFlow internal teams create, review, publish and entitle content;
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
├── Kinder Signs — Active demo
├── Kinder Daily — Concept
└── Kinder Food — Concept
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

Master Content Studio owns all content creation. The contextual Create menu contains:

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

A flashcard, story or future song must use an already-published sign. `MORE` is currently the only item connected to real CV evidence. Other library examples are explicitly illustrative.

## Technology decisions

| Content type | Technology | Reason | Prototype state |
| --- | --- | --- | --- |
| Sign | Computer Vision | Preserve and inspect validated movement | Existing local POC evidence |
| Flashcard | Deterministic template | Create reliable reusable formatting | Functional internal builder |
| Story | Generative AI + evaluation architecture | Create controlled original contextual content | Illustrative local prototype |
| Song | Future generative capability | Demonstrate platform extensibility | Concept only |

Not every problem needs generative AI.

## Create a sign

The internal flow remains:

`Validated reference sign video → MediaPipe processing → landmarks → movement preview → technical metrics → human review → publish`

The Create a Sign route becomes functional when it is served by the local MVP service. An operator can use the existing demo reference or select another MP4. Each run uses the real POC pipeline, produces its own movement overlay and diagnostics, and reports only metrics calculated for that input.

The browser preview is an H.264 MP4 created from the real OpenCV/MediaPipe overlay through a local ffmpeg transcode. Operator-facing outcomes are **Pass**, **Review needed**, or **Fail**. Only Pass and Review needed may be approved; Fail requires another reference.

Start it from the repository root:

~~~bash
python mvp/app.py
~~~

Then open [http://127.0.0.1:8000/create-sign.html](http://127.0.0.1:8000/create-sign.html).

No child video is required. Files remain local, every run is isolated under *mvp/runs/*, and canonical Round 1 evidence is not overwritten. Technical metrics are movement-processing signals, not linguistic correctness certification or system-wide accuracy. Human review remains the publication gate. Production-ready avatar generation is not complete.

## Kinder Signs Flashcard Studio

The Flashcard Studio belongs exclusively to KinderFlow internal content operations. Schools and families receive reviewed flashcards but do not design them. It is a reusable content system rather than five separate cards:

```text
structured published-sign data
→ deterministic template
→ modular character asset
→ Kinder Signs hand-pose asset
→ preview
→ browser print / Save as PDF
→ Signs & Flashcards Library
```

The source model is `prototype/data/signs.json`. It contains initial records for MORE, EAT, WATER, ALL DONE and HELP, including publication, artwork, hand-pose, review, visibility and export readiness. MORE is the first selectable published-source target. The other records remain visible as readiness examples and cannot be selected for production output.

The asset contract is documented under `assets/flashcards/`. It reserves separate locations for:

- untouched official Open Peeps monochrome SVG source files;
- a selected modular character base;
- sign-specific reference, landmark, arm/hand SVG and review files;
- optional owned or licensed contextual elements;
- template assets; and
- local exports.

Local Open Peeps and Miroodles source libraries have been audited but remain ignored, unmodified working sources. No licence or attribution record was found beside them, so no vendor asset has been copied into the runtime. Three inspected Open Peeps candidates are recorded for founder review; their use remains blocked by licence verification. The preview deliberately says **Open Peeps character + Kinder Signs hand pose pending**. Open Peeps will define the modular character look; it will not provide or validate sign-specific hand biomechanics.

The visual rule is:

`illustration + attached sign label → routine → one guidance sentence → Try it during…`

The sign name is part of the same visual unit as the illustration, not a detached page heading. Spanish is the default preview language; English uses the same component and structured content.

The operating flow is:

`Published sign → reviewed sign content → create flashcard → human review → published asset → print / export`

Controls remain intentionally limited to:

- published sign;
- output language: Spanish or English;
- card type: Flashcard or Routine card; and
- browser preview and print proof.

Browser-native Print → Save as PDF is the working export path. Print CSS places one 105 × 148 mm card on an A4 page, removes interface chrome, preserves selectable text and avoids splitting important card sections. PNG export is disabled and labelled as a next step; the prototype does not simulate an image file. The next implementation step is to compose the reviewed character and hand layers as inline SVG, serialize that controlled SVG at a fixed output size, render it to a browser canvas and download the resulting PNG with `canvas.toBlob()`. This should be added only after the official SVG source and reviewed MORE hand asset exist.

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

The static path does not call an LLM, n8n or LangSmith live. `AI-assisted draft` describes the intended origin; `DRY_RUN / NOT_SENT` is shown explicitly. LangSmith is relevant only to LLM-assisted wording. It does not assess movement or sign correctness. The Python input/output contracts and deterministic validation live under `content_ops/` and the n8n adapter boundary is documented under `workflow/`.

MORE is the deepest demonstration target, but final library readiness remains blocked by the character selection, contextual export and custom reviewed hand-pose asset. The other four signs prove the shared data contract and renderer without claiming final assets or publication readiness.

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

The school sees only entitled published assets and operational assignment tools. It does not see source/reference videos, MediaPipe, LangSmith, internal review, or content-production actions.

The assignment flow is deliberately simple:

`Select sign/content → Select one group → Optionally select one child in that group → Confirm → Assign another`

The child dropdown is derived from the selected group. Assign another preserves the group to make repetitive assignment faster.

The school-facing Family Overview shows broad distribution and engagement indicators plus a fictional child roster with:

`Child | Group | Parents / caregivers | Active packs`

No output-format column or sensitive individual behavior scoring is included.

## Family preview

The family route is labelled as a preview of what families receive. It contains one active sign, concise routine guidance and shared family materials. It is not an administrative dashboard and exposes no internal AI or content-production terminology.

## Boundaries

This prototype does not include authentication, billing, payments, databases, APIs, cloud persistence, production CMS capabilities, real school integrations, real child data, tracking, server-side PDF generation, production avatar fidelity or music generation.

KinderFlow controls product and published-asset availability. Schools control assignment and permitted add-ons. Families receive shared materials. Those responsibilities remain separate throughout the prototype.
