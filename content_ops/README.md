# Kinder Signs content operations

This local module connects the existing KinderFlow evidence and prototype layers without replacing them.

## Reused architecture

```text
poc/                      real MediaPipe evidence and diagnostics
mvp/                      isolated local Create a Sign processing runs
prototype/data/signs.json structured family and flashcard source content
workflow/                 governed LLM draft, deterministic gate, n8n and LangSmith
assets/flashcards/        controlled character and sign-specific hand asset contract
content_ops/              states, policy, provenance, audit and packaging adapter
```

`content_ops` does not run Computer Vision, create artwork, call an LLM, approve content or publish automatically. It evaluates whether the outputs of those controlled processes are ready to move forward.

## Domain model

- **Sign:** identifier, labels, routine and source reference.
- **Sign version:** source and technical-evidence references plus a stable data hash.
- **Content package:** bilingual guidance, generation method, content version and content state.
- **Visual package:** character asset, hand-pose asset and separate illustration/hand-review states.
- **Review:** actor type, state, time and non-personal notes.
- **Publication package:** component versions, publication state and library readiness.

## Controlled states

- Technical: `NOT_RUN → PASS | REVIEW_NEEDED | FAIL`
- Content: `DRAFT → READY_FOR_REVIEW → APPROVED`
- Visual: `NEEDS_ARTWORK → NEEDS_HAND_REVIEW → READY`
- Publication: `DRAFT → READY_FOR_HUMAN_REVIEW → APPROVED → PUBLISHED`

Invalid jumps such as `DRAFT → PUBLISHED` are rejected. Deterministic publication policy also blocks a package when technical evidence, approved content, ready visual assets, hand review or explicit human approval is missing.

## Five-sign regression

Run from the repository root:

```bash
python -m content_ops
```

This evaluates MORE, EAT, WATER, ALL DONE and HELP, writes `content_ops/reports/golden_set_report.json`, refreshes the static admin data at `prototype/data/content_operations.json`, and idempotently rebuilds the structured MORE draft package under `build/publication/more/v1/`.

The report measures engineering and product readiness. It is not sign accuracy or linguistic certification.

## Provenance

The MORE manifest records local references and SHA-256 hashes for structured sign data and technical evidence. Hashes demonstrate change detection only; they are not a claim of legal authorship, cryptographic custody or source correctness.

The existing POC evidence is scoped as capture-pipeline evidence. Its identity is not treated here as professional linguistic evidence for MORE.

## Audit log

`events/audit_log.jsonl` is append-only local JSON Lines. Events contain synthetic/system identifiers and actor types, never reviewer names or child data. Duplicate event IDs are ignored to support idempotent operations.

## Current honest state

MORE reaches the furthest available local state, but publication remains blocked. Official character artwork, a reviewed sign-specific hand asset, content approval and explicit human publication approval are still missing. The other four signs intentionally remain earlier in the pipeline.
