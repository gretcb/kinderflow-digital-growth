# Kinder Signs Flashcard Studio assets

This folder is the controlled asset layer for the reusable Kinder Signs flashcard template. Local Open Peeps and Miroodles source libraries were inspected on 2 September 2026, but they are excluded from Git and are not runtime assets.

## Source-library audit

| Source | Local evidence | Intended role | Rights evidence found | Current decision |
| --- | --- | --- | --- | --- |
| Open Peeps / Flat Assets | 358 SVG and 185 PNG files, including modular atoms and composed templates | Character base only | No licence, attribution or source record found in the local folder | **LICENCE VERIFICATION NEEDED**. Do not copy into runtime assets. |
| Miroodles | One `.fig`, one `.sketch` and one `.xd` design source; Sketch/XD previews can be inspected | Optional, visually secondary routine element | No licence, attribution or source record found in the local folder | **LICENCE VERIFICATION NEEDED**. Manual export only after rights are recorded. |
| Kinder Signs hand pose | No final MORE asset exists | Sign-specific arm and hand layer | Must come from a validated reference and recorded review | **BLOCKED** pending reference, drawing and human review. |

The local source folder is ignored by Git to reduce accidental redistribution risk. Candidate filenames are recorded in `open_peeps/candidates.json`; the files themselves stay in the local source library.

### Open Peeps format and composition findings

- Source location: `assets/flashcards/source_libraries/Flat Assets/`
- Formats found: 358 SVG and 185 PNG files.
- Structure found: Separate Atoms for accessories, faces, people, bodies, heads, standing/sitting poses and facial hair; composed Bust, Standing and Sitting templates are also present.
- SVG/PNG technical classification: **DIRECTLY USABLE** as file formats, but **REFERENCE ONLY** for this repository until licence verification is complete.
- Separate Atoms classification: **USABLE AFTER SIMPLE COMPOSITION**, subject to the same licence block.
- Three clean modular candidate recipes are recorded in `open_peeps/candidates.json`. They use shortlisted face, head/hair and clothing atoms with no accessory. `open_peeps/modular_inventory.json` records counts, viewBoxes and compatibility constraints. These are metadata-only recipes, not final compositions.

### Miroodles format findings

- Source location: `assets/flashcards/source_libraries/`
- Formats found: one Figma `.fig`, one Sketch `.sketch` and one Adobe XD `.xd` source.
- The Sketch and XD containers expose embedded preview images; the `.fig` file remains a proprietary design document in this environment.
- Classification: **MANUAL EXPORT NEEDED**. No selected runtime SVG/PNG exists.
- Intended role: a restrained routine cue only. It must not define the sign, the hand pose or movement.

## Composition model

```text
published sign data
+ official monochrome character base
+ reviewed Kinder Signs arm / hand pose
+ optional owned or licensed context element
+ deterministic flashcard template
= reviewed flashcard asset
```

The character defines the look. The validated reference movement defines the sign. A generic character pose must never be treated as evidence that a sign is correct.

## Folder contract

- `open_peeps/` — add the official monochrome SVG library and its licence/source notes here. Do not alter the downloaded originals.
- `character_base/` — add the selected, working SVG character composition and a short component map for replaceable body, clothing and arm layers.
- `hand_pose_references/<sign>/` — controlled, sign-specific working folders. Each may later contain a reference image, MediaPipe landmark snapshot, custom SVG arm/hand pose and review notes.
- `contextual_elements/` — optional owned or properly licensed routine objects. These must remain visually secondary to the hands.
- `templates/` — optional exported SVG template assets. The current working template is HTML/CSS in `prototype/flashcards.html` and `prototype/styles.css`.
- `exports/` — local review exports only. Generated files in this folder are ignored by Git.

## Hand-pose workflow

```text
validated sign reference
→ MediaPipe landmarks
→ pose reference
→ custom SVG arm / hand adaptation
→ human visual review
→ flashcard asset
```

MediaPipe supports pose reference and movement inspection. It does not certify linguistic sign correctness. Open Peeps supplies a modular visual base; Kinder Signs must supply and review the sign-specific arm and hand asset separately.

## Visual hierarchy

1. Illustration and sign label form one visual unit.
2. The sign label sits directly below or beside the illustration.
3. Routine context follows.
4. Family guidance is one short sentence.
5. A concise “Try it during…” cue closes the card.

The illustration safe area must keep both hands visible, separated from the body and clear of text. Start in monochrome, then add selective Kinder Signs colour only after the gesture reads clearly in grayscale.

## School and family output rule

Kinder Signs creates the flashcard from a published sign. Educators do not design it. When the Flashcards pack is active for a group or child, the matching reviewed flashcard is included automatically in prepared family output. When inactive, the school may see the asset as available, but families do not receive it. No billing is implemented here.

## Remaining manual asset work

1. Locate the official licence and provenance record for each selected source library and confirm the intended commercial use.
2. Select one character candidate and document its replaceable SVG groups under `character_base/`.
3. Open the Miroodles source in its native or compatible design tool, select one restrained routine element, and export SVG plus PNG into `contextual_elements/`. Do not use a contextual hand or sign pose.
4. Add a rights-cleared MORE reference still and a human-inspectable landmark snapshot under `hand_pose_references/more/`.
5. Draw the MORE arm/hand SVG against that reference without altering the movement.
6. Record independent human visual review in the supplied review template.
7. Replace the labelled placeholder in Flashcard Studio, then perform grayscale, small-size and print review.

No production illustration should be published until source rights and hand-pose review are recorded.
