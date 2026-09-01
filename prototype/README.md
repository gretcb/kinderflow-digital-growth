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

The UI shows the existing single-reference evidence: 332 frames, 100% pose detection, 93.98% dominant-hand detection and 20 missing hand frames. These metrics are technical signals, not linguistic correctness certification or system-wide accuracy.

No child video is required. The static page does not upload video or run the local CV scripts. Production-ready avatar generation is not complete.

## Internal Flashcard Builder

The Flashcard Builder belongs exclusively to KinderFlow internal content operations. Schools and families receive published flashcards but do not design them.

The flow is:

`Published sign → approved sign text → create flashcard → human review → published asset → print / export`

Controls are intentionally limited to:

- published sign;
- output language: English or Spanish;
- card type: Flashcard or Routine card; and
- output format: PDF or Image.

The application interface stays in English. Spanish appears only inside the printable preview when Spanish is selected.

A basic Flashcard contains the sign word and visual placeholder. A Routine card adds routine context and concise usage guidance. PDF uses browser-native print and Save as PDF. Image export is labelled illustrative and does not create a file. No freeform editor, page-packing controls, server-side PDF service or persistence is included.

## Story prototype

The story route accepts only a published sign and produces a short original English prototype draft. It demonstrates explicit deterministic checks, evaluator-style review dimensions, LangSmith observability boundaries and human review actions.

No live LLM, n8n or LangSmith call runs from the static page. LangSmith represents traceability for the content-transformation step; it does not validate sign biomechanics, MediaPipe output or linguistic sign correctness.

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
