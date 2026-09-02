# Kinder Signs Flashcard Studio assets

This folder is the controlled asset layer for the reusable Kinder Signs flashcard template. It intentionally contains no downloaded Open Peeps or Miroodles artwork yet.

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

## Add manually tomorrow

1. Download the official Open Peeps monochrome SVG library from its official source.
2. Save the untouched files and source/licence record under `open_peeps/`.
3. Choose one character base and document its replaceable SVG groups under `character_base/`.
4. Add the validated MORE reference still and landmark snapshot under `hand_pose_references/more/`.
5. Create the MORE arm/hand SVG without changing the validated movement.
6. Conduct human visual review and record the result in that sign folder.
7. Replace the labelled placeholder in the Flashcard Studio, then review and export the first card.

No production illustration should be published until source rights and hand-pose review are recorded.
