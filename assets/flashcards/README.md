# Kinder Signs Flashcard Studio assets

This folder is the controlled asset layer for the reusable Kinder Signs flashcard template. Ignored local Open Peeps and Miroodles source libraries were inspected on 2 September 2026. Selected Open Peeps inputs now have a versioned provenance record, and KinderFlow-derived SVGs are runtime draft assets. The original source libraries remain excluded from Git.

## Source-library audit

| Source | Local evidence | Intended role | Rights evidence found | Current decision |
| --- | --- | --- | --- | --- |
| Open Peeps / Flat Assets | 358 SVG and 185 PNG files, including modular atoms and composed templates | Character and line grammar only | `open_peeps/provenance.json` records the official source, founder-verified CC0 basis and selected-input hashes | Use only for recorded style inputs. Derived sign assets remain drafts pending qualified sign and visual review. |
| Miroodles | One `.fig`, one `.sketch` and one `.xd` design source; Sketch/XD previews can be inspected | Optional, visually secondary routine element | No licence, attribution or source record found in the local folder | **LICENCE VERIFICATION NEEDED**. Manual export only after rights are recorded. |
| Kinder Signs hand pose | Six packages contain 18 deterministic draft SVG options | Sign-specific arm and hand layer | Functional references and asset hashes are recorded; qualified review and several usage rights remain open | **BLOCKED** for printable use and publication pending rights, sign, hand and visual review. |

The local source folder is ignored by Git to reduce accidental redistribution risk. Candidate filenames are recorded in `open_peeps/candidates.json`; selected identities and hashes are recorded in `open_peeps/provenance.json`; the source files remain in the local library. Derived draft SVGs live under `prototype/assets/signs/`.

### Open Peeps format and composition findings

- Source location: `assets/flashcards/source_libraries/Flat Assets/`
- Formats found: 358 SVG and 185 PNG files.
- Structure found: Separate Atoms for accessories, faces, people, bodies, heads, standing/sitting poses and facial hair; composed Bust, Standing and Sitting templates are also present.
- SVG/PNG technical classification: **DIRECTLY USABLE** as file formats. Only inputs covered by the versioned provenance record may inform the current visual system.
- Separate Atoms classification: **USABLE AFTER SIMPLE COMPOSITION** for character and line grammar, not sign mechanics.
- Candidate recipes are recorded in `open_peeps/candidates.json`. `open_peeps/modular_inventory.json` records counts, viewBoxes and compatibility constraints. The current fixed base and source hashes are recorded in `open_peeps/provenance.json`; the 18 derived SVG options remain review drafts.

### Miroodles format findings

- Source location: `assets/flashcards/source_libraries/`
- Formats found: one Figma `.fig`, one Sketch `.sketch` and one Adobe XD `.xd` source.
- The Sketch and XD containers expose embedded preview images; the `.fig` file remains a proprietary design document in this environment.
- Classification: **MANUAL EXPORT NEEDED**. No selected runtime SVG/PNG exists.
- Intended role: a restrained routine cue only. It must not define the sign, the hand pose or movement.

## Composition model

```text
approved sign data
+ official monochrome character base
+ reviewed Kinder Signs arm / hand pose
+ optional owned or licensed context element
+ deterministic flashcard template
= reviewed flashcard asset
```

The character defines the look. The reviewed reference defines the sign. A generic character pose must never be treated as evidence that a sign is correct.

## Folder contract

- `open_peeps/`: versioned candidate metadata, modular inventory and provenance. Downloaded originals remain external and unaltered.
- `character_base/`: reserved for an exported reusable base if a separate runtime file becomes necessary.
- `hand_pose_references/<sign>/`: controlled, sign-specific reference and review records.
- `contextual_elements/`: optional owned or properly licensed routine objects. These must remain visually secondary to the hands.
- `templates/`: optional exported SVG template assets. The current working template is HTML/CSS in `prototype/flashcards.html` and `prototype/styles.css`.
- `exports/`: local review exports only. Generated files in this folder are ignored by Git.

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

Kinder Signs is designed to create a flashcard from an approved sign package; educators do not design the asset. School Admin stores synthetic assignments in browser/session state, and Family View reads that state to display the corresponding sign and materials. This implements the assignment-driven mini-library at local/session-based MVP scope. It does not prove automatic delivery to real family identities or accounts, durable cross-session or cross-device persistence, authentication or authorisation, notifications, production school accounts, tenant isolation, production correction/deletion workflows, or external nursery-platform integration. No billing is implemented here.

## Remaining manual asset work

1. Confirm intended display, processing, adaptation, print and distribution rights for every non-Open Peeps reference, contextual asset and Gemini file used in the pilot.
2. Retain the Open Peeps source, CC0 basis, selected-input hashes and voluntary credit with every derived version.
3. Use Miroodles only if its licence is recorded and a restrained contextual element passes manual export and review.
4. Complete qualified sign, hand, contact, direction, movement and readability review for each selected pilot SVG.
5. Record reviewer identity, authority, decision, rationale, version and time in an approval system suitable for the pilot.
6. Perform grayscale, small-size, accessibility and saved-PDF checks with the final rights-cleared assets.

No production illustration should be published until source rights and qualified sign, hand, visual and publication review are recorded.
