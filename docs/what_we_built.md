# What we built

These are working notes, not final Round 2 submission prose. They describe the repository as it exists on 2 September 2026.

## Kinder Signs in one sentence

Kinder Signs tests whether one controlled sign source can become reusable school-and-family material without asking each school to create or manage the content-production process.

## The product flow

### 1. Reference sign video

**What it does:** Provides the movement source for a sign-production run.

**Why we need it:** The movement must come from a known reference rather than be invented by a visual generator.

**What it does not do:** A video is not approved merely because it can be uploaded. Source rights, sign identity and professional suitability still need confirmation.

### 2. MediaPipe landmark extraction

**What it does:** Extracts body and hand points from each readable video frame.

**Why we need it:** Those points turn visible movement into structured data that software can inspect over time.

**What it does not do:** It does not certify linguistic sign correctness or assess a child.

### 3. Movement evidence and skeleton representation

**What it does:** Keeps the extracted points in time order and creates a landmark-overlay preview and diagnostic plots.

**Why we need it:** An operator can compare the reference video with the structured movement evidence.

**What it does not do:** The skeleton is not a finished avatar or family-facing sign asset.

### 4. Technical checks

**What it does:** Reports capture signals such as frames analysed, hand and pose coverage, gaps and abrupt transitions.

**Why we need it:** Weak or incomplete capture should be visible before content moves to human review.

**What it does not do:** A technical pass is not “sign accuracy.” The current reference produced 93.98% dominant-hand detection coverage, not 93.98% sign correctness.

### 5. Visual and flashcard layer

**What it does:** Keeps family-facing illustration and printable layout separate from the movement-processing layer.

**Why we need it:** The same approved source should be reusable in consistent materials without changing the movement evidence.

**What it does not do:** The repository does not contain final production avatar generation or a professionally reviewed MORE hand-pose asset.

### 6. Flashcard content

**What it does:** Combines a sign label, routine, short family guidance and a visual placeholder in predefined layouts.

**Why we need it:** Families need short material connected to a real school routine, not technical CV output.

**What it does not do:** It does not let the school create or validate the underlying sign. It is not a free-form design tool.

### 7. Deterministic checks

**What it does:** Normal code checks objective facts: required fields, allowed states, asset readiness, banned wording and the presence of human approval.

**Why we need it:** A true/false rule should not depend on a language model’s judgement.

**What it does not do:** Passing required-field checks does not prove that the educational content is professionally correct.

### 8. Optional LLM wording support

**What it does:** The workflow can ask a language model to turn supplied, approved source text into a short family draft.

**Why we need it:** It may reduce repetitive editing when several family-facing variants are needed.

**What it does not do:** It does not create hand shape, movement, sign correctness or publication approval. Current content-operations manifests use human-authored copy, so the LLM is not required for the core sign flow.

### 9. LangSmith evaluation

**What it does:** The dry-run shows what would be traced and which checks would apply to LLM-assisted wording.

**Why we need it:** If an LLM is used, the team needs to see its input, output and evaluation evidence.

**What it does not do:** It does not evaluate the video, MediaPipe, hands, movement fidelity or linguistic correctness. A live trace has not been run as repository evidence.

### 10. Human review

**What it does:** Keeps approval and publication under explicit human control.

**Why we need it:** Technical capture and generated wording cannot decide whether educational sign content is suitable for release.

**What it does not do:** The local buttons do not provide reviewer identity, authentication or a production audit trail.

### 11. Signs & Flashcards Library

**What it does:** Represents the intended destination for a reviewed, published sign and its family assets.

**Why we need it:** Kinder Signs can prepare one governed asset centrally and make it available to more than one entitled school.

**What it does not do:** The current repository does not contain a production database or a completed approved five-sign library. The five-sign regression report currently blocks all five from publication.

### 12. School assignment

**What it does:** The static school prototype shows selecting existing library items and assigning them to groups or a fictional child.

**Why we need it:** The school should operate a simple distribution flow, not CV, LLM or content production.

**What it does not do:** It does not save assignments, enforce permissions, contact families or integrate with a school platform.

### 13. Family output

**What it does:** Shows short guidance and printable material linked to the same routine used at school.

**Why we need it:** School-home continuity is the product proposition.

**What it does not do:** It is not clinical advice, a developmental assessment or a promise of faster development.

### 14. Pilot measurement

**What it does:** Defines future privacy-minimised events for assignment, viewing, printing and review operations.

**Why we need it:** A pilot must test actual use, effort and commercial interest rather than rely on prototype reactions.

**What it does not do:** The schema is not live instrumentation and contains no pilot results.

## How the parts fit

```text
Validated reference material
→ local CV processing
→ technical evidence
→ content + visual preparation
→ deterministic checks
→ human review
→ published library item
→ entitled school assignment
→ family output
→ future pilot evidence
```

The current repository proves parts of this chain. It does not prove the whole production service or the market.
