# Kinder Signs manual QA checklist

Use `python mvp/app.py`, then open `http://127.0.0.1:8000/create-sign.html`. Use fictional records only.

## Create a Sign

- [ ] Select the demo reference and confirm its selected state.
- [ ] Run the movement check and watch all seven processing stages.
- [ ] Play the reference and skeleton/landmark previews side by side.
- [ ] Confirm frames, pose coverage, hand coverage and missing frames describe capture—not sign accuracy.
- [ ] Confirm Fail cannot be approved and Review needed explains its conditions.
- [ ] Record local human review and continue to Prepare family content.

## Content Engine

- [ ] Select MORE and confirm school and family source context appears.
- [ ] Select `LLM-assisted` and generate. Confirm `LIVE` or `DRY-RUN` is accurate.
- [ ] Inspect structured JSON, the deterministic gate and the separate LangSmith status.
- [ ] Confirm rejected output cannot be approved.
- [ ] Approve valid content and confirm Flashcard, school and family preview links unlock.
- [ ] Request changes and confirm those links lock again.
- [ ] Restore human copy and confirm it creates a separate human review candidate.

## Flashcard Studio

- [ ] In the first viewport, identify KinderFlow Admin, Flashcard Studio, the selected sign, the three configuration steps, the live preview and `Approve flashcard` without scrolling.
- [ ] Confirm MORE reads `Internal visual proof available`; confirm EAT, WATER, ALL DONE and HELP read `Not ready`.
- [ ] Select each ineligible sign and confirm a useful empty state replaces the card, approval is disabled and Master Content Studio is the recovery action.
- [ ] Create an English Flashcard for MORE. Confirm the output contains only KINDER SIGNS, the labelled visual placeholder and MORE.
- [ ] Switch to Spanish. Confirm the output changes to MÁS while the application interface remains English.
- [ ] Switch to Routine Card. Confirm only routine and one concise `How to use it` / `Cómo usarlo` section are added.
- [ ] Confirm changing sign, language or card type resets any local approval.
- [ ] Approve the proof. Confirm `Print as PDF` becomes the only primary action and the state reads `Approved locally`, not published or available to schools.
- [ ] Confirm `PNG export — prototype` remains disabled and its reason is visible.
- [ ] Confirm the illustration is visibly labelled as an internal placeholder and the final hand pose is not implied.
- [ ] Complete the main workflow by keyboard only; check focus order, selected states and visible focus rings.
- [ ] Use browser print preview and Save as PDF. Confirm only one card prints, with no navigation, controls, status, approval note or empty-state content.
- [ ] Check the PDF at normal scale and in grayscale for clipping, selectable text, visual hierarchy, margins and sign-label attachment.
- [ ] Test at 1440 × 900, 1280 × 800, 768 px and 390 px. Confirm no horizontal overflow, clipped card or hidden primary action.
- [ ] At 200% browser zoom, confirm all controls and output text remain readable and operable.

## Character and context

- [ ] Compare the three metadata-only Open Peeps recipes and save one local candidate.
- [ ] Confirm no third-party source SVG is loaded by the runtime.
- [ ] Confirm `LICENCE VERIFICATION NEEDED` is visible.
- [ ] Follow the Miroodles manual-export note; do not treat context artwork as the sign source.

## Library, school and family previews

- [ ] Confirm MORE says `Blocked by hand review`, not production-ready.
- [ ] Confirm the school surface is clearly labelled `School Admin` and does not expose internal review terminology.
- [ ] Confirm `What’s included for School A` explains the benefit of each available service.
- [ ] Confirm the school library shows only sign name, available formats and the assignment action—no routines or family guidance.
- [ ] Confirm `MORE — Sign + flashcard` describes the assignable item without internal delivery language.
- [ ] Change groups and verify the child list contains only children in that group.
- [ ] Leave `All children in group` selected and confirm both the summary and CTA name the selected group.
- [ ] Select a child and confirm both the summary and CTA name that child.
- [ ] Assign to a group and a child; confirm the concise success message uses the correct destination.
- [ ] Select `Assign another item`; confirm the group is preserved and the child resets to all children.
- [ ] Confirm reviewed family wording appears without MediaPipe, LangSmith or quality-gate metadata.
- [ ] Confirm the flashcard pack is conditional and the visual remains preview-only until hand review.
- [ ] From Family Preview, confirm `Return to School Admin` goes back to the school surface.

## UX freeze viewport review

Browser automation was unavailable during the source-level freeze pass. Confirm each item manually before declaring the UX frozen.

Test at 1440 × 900, 1280 × 800, 768 px wide and 390 px wide:

- [ ] KinderFlow Hub explains the school-to-home value before showing product structure.
- [ ] Product roadmap labels Kinder Signs as the first product and Daily/Food as future products.
- [ ] Role cards clearly distinguish KinderFlow operations, School A management and the family experience.
- [ ] Master Content Studio technology choices remain readable and explicitly state that not everything uses AI.
- [ ] Master Content Studio shows its purpose and the explicit sign/flashcard/story/song paths without a generic `+ Create` control.
- [ ] At least the next available action is visible in the first laptop viewport; there is no isolated button in empty space.
- [ ] School assignment fields align as three numbered steps; the CTA sits in a separate lower action area.
- [ ] At tablet and mobile widths, assignment fields stack in reading and tab order with no overlap.
- [ ] Headers and navigation remain usable without clipped text or horizontal page overflow.
- [ ] Hub, Admin, Studio, Create Sign, Master Library, School Admin and Family Preview each identify the current surface and a return/next path.
- [ ] Button focus indicators are visible with keyboard navigation and all select controls have associated labels.
- [ ] Flashcard controls remain usable in Spanish and English, and browser print preview still isolates the selected proof.
- [ ] Family Preview contains no administrative controls or internal AI/CV terminology.
