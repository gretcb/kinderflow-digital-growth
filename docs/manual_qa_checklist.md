# Kinder Signs manual QA checklist

Use fictional records only. The application default remains port 8000: run `poc_env/bin/python mvp/app.py`, then open `http://127.0.0.1:8000/create-sign.html`.

For the final demonstrated route set, run `poc_env/bin/python mvp/app.py --port 8765` and check `http://127.0.0.1:8765/index.html`, `kinder-signs.html`, `create-sign.html`, `school.html?sign=more&focus=share`, and `family.html`.

## Create a Sign

- [ ] Confirm `Upload a video` and `Use a direct video URL` are the only two source modes; only the selected field is visible, enabled and submitted.
- [ ] Switch between both modes and confirm a stale file or URL cannot leak into the other request.
- [ ] Select the demo reference and confirm it remains a MORE shortcut, not a third source mode.
- [ ] Submit a valid public direct MP4 URL; confirm it runs through the same review flow, retains the explicit selected sign and stores no query string in displayed/restored provenance.
- [ ] Submit a normal webpage URL; confirm the controlled error explains that a direct MP4 is required and offers `Upload a video instead` without clearing the selected sign.
- [ ] Try `file:`, credential-bearing, localhost/private-address and oversized URL cases; confirm they fail closed without a partial or orphaned run.
- [ ] Run the reference review and watch all seven processing stages.
- [ ] Play the reference and skeleton/landmark previews side by side.
- [ ] Confirm frames, pose coverage, hand coverage and missing frames describe capture. They do not measure sign accuracy.
- [ ] Confirm Fail cannot be approved and Review needed explains its conditions.
- [ ] Confirm the practical value statement, the two decision charts and the collapsed technical/source details.
- [ ] Confirm tracked poses are offered at 90% tracked-hand coverage and disabled with a clear reason below 90%.
- [ ] Save one or two poses, create/approve a visual and open family materials.
- [ ] After pose approval, confirm MORE, HELP and MILK show only their registered illustrative video, and EAT, SLEEP and WATER show `Video preview not available for this sign yet.` with `Continue to family materials`.
- [ ] Confirm the available preview says it was prepared separately and the collapsed technical details identify Google Labs FX / Gemini FX, pre-generated status, no current-run or landmark control, demo-only use, human review and no certification.
- [ ] Confirm an unavailable or failed illustrative video clears any stale video/source and never blocks the ordinary visual preparation or family-material handoff.
- [ ] Choose `Different pose`; confirm the completed reference review, chart evidence, result state and run identity remain, MediaPipe does not rerun, and the illustrative preview resets until pose approval.

## Content Engine

- [ ] Select MORE and confirm school and family source context appears.
- [ ] Select `LLM-assisted` and generate. Confirm `LIVE` or `DRY-RUN` is accurate.
- [ ] Inspect structured JSON, the deterministic gate and the separate LangSmith status.
- [ ] Confirm rejected output cannot be approved.
- [ ] Approve valid content and confirm Flashcard, school and family preview links become available.
- [ ] Request changes and confirm those links lock again.
- [ ] Restore human copy and confirm it creates a separate human review candidate.

## Family printables

- [ ] Open Flashcard from an exactly approved sign visual; confirm an unmatched or stale handoff fails closed with a route back to visual review.
- [ ] Confirm the only language choices are `Bilingual` and `Spanish` and no PNG action or PNG copy is visible.
- [ ] In Bilingual, confirm English is primary and Spanish is secondary.
- [ ] In Spanish, confirm the word, labels, routine, guidance, movement text and accessibility descriptions are Spanish.
- [ ] Switch between Flashcard and Routine Card; confirm the reviewed sign visual, routine context and approved guidance remain consistent.
- [ ] Confirm `Finish your printable`, `Ready for approval` and the concise approval instructions appear before approval.
- [ ] Confirm approval stays disabled until the sign illustration is visibly loaded.
- [ ] Approve the printable; confirm `Printable ready`, `Print / Save as PDF`, `Create another format` and `Back to family materials` appear.
- [ ] Open the A5 proof, then return to family materials and visual options; confirm sign, run, candidate, language, type, routine and approved copy remain exact without re-running reference analysis.
- [ ] Complete the main workflow by keyboard only; check focus order, selected states and visible focus rings.
- [ ] Use browser print preview and Save as PDF. Confirm exactly one A5 card prints, with no navigation, controls, status or empty-state content.
- [ ] Check the PDF at normal scale and in grayscale for clipping, selectable text, visual hierarchy, margins and sign-label attachment.
- [ ] Test at 1440 × 900, 1280 × 800, 768 px and 390 px. Confirm no horizontal overflow, clipped card or hidden primary action.
- [ ] At 200% browser zoom, confirm all controls and output text remain readable and operable.

## Character and context

- [ ] Compare the current Open Peeps-derived draft options and save one distinct local candidate.
- [ ] Confirm the runtime uses versioned KinderFlow-derived SVGs rather than an ignored third-party source file.
- [ ] Confirm the Open Peeps provenance record states the official source and founder-verified CC0 basis, while unrelated source and Gemini rights remain visibly unresolved.
- [ ] Follow the Miroodles manual-export note; do not treat context artwork as the sign source.

## Library, school and family previews

- [ ] Confirm MORE says `Blocked by hand review`, not production-ready.
- [ ] Confirm the school surface is branded `Little Steps Nursery` with `Kinder Signs workspace` context and no internal review terminology.
- [ ] Confirm `Your Kinder Signs plan` explains the services configured for the nursery.
- [ ] Confirm the responsive library shows six bilingual sign cards with routine context, truthful `Preview` state, configured format chips and one assignment action.
- [ ] Open `Demo details`; confirm it distinguishes the assignment-demo fixture from canonical school-distribution availability.
- [ ] Change groups and verify the child list contains only children in that group.
- [ ] Leave `Everyone in the group` selected and confirm both the summary and CTA name the selected group.
- [ ] Select a child and confirm both the summary and CTA name that child.
- [ ] Share to a group and a child; confirm the concise success message uses the correct destination.
- [ ] Submit an exact duplicate; confirm no record is added, the message `This exact sign, audience and material combination is already active.` appears, and `View active assignment` / `Change materials` are offered.
- [ ] Share the same sign with another group or material set; confirm a distinct record is added.
- [ ] Edit an active assignment’s materials, then remove it; confirm the same record is updated before removal.
- [ ] Select `Share another sign`; confirm the group is preserved and the child resets to everyone in the group.
- [ ] Confirm reviewed family wording appears without MediaPipe, LangSmith or quality-gate metadata.
- [ ] Confirm the flashcard pack is conditional and the visual remains preview-only until hand review.
- [ ] From Family View, confirm the synthetic browser/session assignment is filtered to the selected group or fictional child, the corresponding sign and materials form the local mini-library, and `Return to School Admin` goes back to the school surface.

## UX freeze viewport review

Browser automation was unavailable during the source-level freeze pass. Confirm each item manually before declaring the UX frozen.

Test at 1440 × 900, 1280 × 800, 768 px wide and 390 px wide:

- [ ] KinderFlow Hub explains the school-to-home value before showing product structure.
- [ ] Product roadmap labels Kinder Signs as the first product and Daily/Food as future products.
- [ ] Role cards clearly distinguish KinderFlow operations, Little Steps Nursery management and the family experience.
- [ ] Master Content Studio technology choices remain readable and explicitly state that not everything uses AI.
- [ ] Master Content Studio shows its purpose and the explicit sign/flashcard/story/song paths without a generic `+ Create` control.
- [ ] At least the next available action is visible in the first laptop viewport; there is no isolated button in empty space.
- [ ] School assignment fields align as four numbered decisions; the CTA sits in a separate lower action area.
- [ ] At tablet and mobile widths, assignment fields stack in reading and tab order with no overlap.
- [ ] Headers and navigation remain usable without clipped text or horizontal page overflow.
- [ ] Hub, Admin, Studio, Create Sign, Master Library, School Admin and Family Preview each identify the current surface and a return/next path.
- [ ] Button focus indicators are visible with keyboard navigation and all select controls have associated labels.
- [ ] Flashcard controls remain usable in Spanish and English, and browser print preview still isolates the selected proof.
- [ ] Family Preview contains no administrative controls or internal AI/CV terminology.
