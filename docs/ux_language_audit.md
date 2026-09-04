# KinderFlow plain-language UX audit

Date: 4 September 2026

## Scope

The prototype contains 12 HTML routes. The local MVP service maps its root route to create-sign.html. A basic static server maps its root to index.html.

The audit distinguishes visible product language from internal stored values. Exact UI labels take priority in user instructions. Raw statuses and provenance remain available through Technical and source details where the interface exposes them.

## Route map

### index.html

Role: platform overview for prospective schools and reviewers.

Primary heading: Bring nursery learning home.

Boundary: the statement that families receive active materials describes the intended experience. Real assignment delivery is not implemented.

### kinder-signs.html

Role: Kinder Signs product overview.

Primary heading: Turn Baby Sign knowledge into content families can use.

Boundary: this route explains the proposition. It does not prove that content is published or commercially available.

### admin.html

Role: KinderFlow Team operations overview.

Primary heading: KinderFlow Admin.

Boundary: activity and access values are explicitly example data. No live accounts, permissions, or analytics are connected.

### content-studio.html

Role: internal product and workspace selector.

Primary heading: KinderFlow Content Studio.

Boundary: Kinder Signs is the active prototype. Kinder Daily and Kinder Food are future products.

### create-sign.html

Role: internal sign operator and reviewer.

Primary heading: Create a sign.

The five visible steps are:

1. Sign & reference.
2. Review reference.
3. Choose poses.
4. Approve visual.
5. Family materials.

Exact source labels are Upload a video, Use a direct video URL, and Use demo reference. The submission action is Review the sign reference.

The evidence choices are Use tracked poses, Choose reference frames, and Use reviewed references. The decision action is Create family materials.

Visual actions are Create visual options, Choose different pose, Create another visual option, Reject visual, and Approve selected visual.

Technical terms, run IDs, source paths, and raw status values remain under Technical and source details. The visible Reviewed reference label maps to the internal request value Validated reference.

### library.html

Role: internal Content Library and wording-readiness demonstration.

Primary heading: Content Library.

Boundary: the five-record Content Operations set is separate from the six-sign visual registry. Every governed publication record remains blocked.

### flashcards.html

Role: internal printable reviewer.

Primary heading: Create a printable.

Exact output choices are Flashcard and Routine Card. Exact language choices are Bilingual and Spanish. The approved visual cannot be changed on this route.

Boundary: the route creates a local proof only.

### print-card.html

Role: internal print-proof reviewer.

Primary heading: Review before printing.

Boundary: the only export action is browser Print or Save as PDF. No PNG or server PDF action exists.

### create-story.html

Role: internal story author and reviewer.

Primary heading: Turn a reviewed sign into a simple story.

Boundary: the current script produces deterministic English or Spanish text for MORE only. No live LLM, n8n, or LangSmith call occurs.

### create-song.html

Role: future-format explanation.

Primary heading: Song.

Boundary: Coming soon and Not available yet are the current status labels.

### school.html

Role: Little Steps Nursery educator or administrator.

Primary heading: Share Kinder Signs with your families.

The interface supports selecting a sign, group, materials, and audience. The audience can be everyone in the group or one child. It blocks an exact duplicate and supports edit and removal for active assignments.

Boundary: synthetic data and browser session storage only. Share is demonstration copy, not proof of real delivery.

### family.html

Role: family-facing preview.

Primary heading: Your Kinder Signs.

The page labels its collection Your mini-library and Signs shared with you. It can filter and combine assignments from the current browser session. If no stored assignment exists, it inserts a synthetic MORE example.

Boundary: a family-facing guidance prototype exists. A personalised assignment-driven family library remains a next product iteration.

## Presentation mappings

- MediaPipe processing appears as Reference review.
- Landmark extraction appears as Find the reference poses.
- Dominant-hand landmark coverage appears as Main-hand visibility in summary copy.
- KNOWLEDGE_REFERENCE_FALLBACK appears as Reviewed references.
- Visual package appears as Sign visual.
- Candidate appears as Visual option.
- APPROVED_FOR_INTERNAL_PRINTABLE appears as Ready for family materials.
- LLM_ASSISTED appears as AI-assisted draft.
- HUMAN appears as Approved source copy.
- Deterministic quality gate appears as Quality checks.
- DRY_RUN appears as Demo mode in technical details.
- NOT_APPLICABLE appears as Not used for this step in technical details.

## Accessibility and responsive evidence

- Native labelled controls remain in place.
- Status changes use live regions.
- Visual choices remain keyboard-operable radio controls.
- Details summaries have visible focus styles.
- The five-step flow reflows across desktop, tablet, and mobile layouts.
- Tests cover headings, duplicate IDs, labels, local links, JavaScript syntax, story languages, and the 18 visual candidates.

These checks support interface quality. They do not replace assistive-technology testing with users.
