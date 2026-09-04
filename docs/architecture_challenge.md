# Architecture challenge

This is a pre-final architecture decision record. The Open Peeps defer decision was later superseded by 18 deterministic draft SVG options with versioned provenance. The current status and remaining review gates are recorded in `docs/mvp_reality_check.md` and `assets/registry/source_assets_provenance.md`; the row below remains as historical rationale.

This review asks whether each part earns its place now. The goal is a smaller, clearer product rather than maximum technical coverage.

| Decision | Element | Reason |
|---|---|---|
| KEEP | Existing MediaPipe POC reused by the MVP | It is the distinguishing functional evidence and avoids two sources of CV truth. |
| KEEP | Raw/normalized/diagnostic evidence separation | It protects the original extraction and makes transformations explainable. |
| KEEP | Technical status separate from content status | This prevents detection coverage becoming an approval claim. |
| KEEP | Deterministic publication rules | Objective readiness checks should be explicit and testable. |
| KEEP | Human publication gate | The core professional-quality and governance boundary depends on it. |
| KEEP | Flashcard templates and browser print | They turn controlled content into a useful family output without a design platform or AI layout. |
| KEEP | Run IDs, safe filenames and ignored run artifacts | These are small controls with direct reliability/privacy value. |
| KEEP | Five-sign regression set | It is cheap to rerun and prevents rules being tested only against MORE. |
| KEEP | Basic provenance and change-detection hashes | They support version awareness without requiring a CMS. |
| SIMPLIFY | Content Operations UI | Keep the readiness matrix and blocking reasons. Avoid adding editing, bulk actions or enterprise CMS features before a pilot. |
| SIMPLIFY | State model in presentations | The code can retain four domains; founder/panel explanations should lead with “technical result” and “publication decision.” |
| SIMPLIFY | n8n | Use it only if it removes repeated manual workflow steps. Do not add a second orchestration path alongside Python without a named operational owner. |
| SIMPLIFY | LLM use | Keep it optional. Approved human-written family copy already works; do not regenerate text merely to show AI. |
| SIMPLIFY | LangSmith | One small live evaluation set is enough when LLM use begins. Do not frame the dry-run as production monitoring. |
| SIMPLIFY | Local audit log | Keep event shape/idempotency tests, but do not present the JSONL file as an enterprise audit trail. |
| SIMPLIFY | Publication package | The five JSON files are useful evidence. Avoid adding signing, blockchain or release infrastructure before real publishing requirements exist. |
| DEFER | Production avatar/retargeting | It is technically and professionally high risk. First secure validated sources and reviewed hand/visual assets. |
| DEFER | Open Peeps integration | Add only after asset licensing, visual direction and hand-composition approach are confirmed. |
| DEFER | Real-time school assignment backend | A pilot can first test the workflow with controlled delivery and minimal records. |
| DEFER | Production analytics stack | Define events now; build collection only when a pilot question and data responsibilities are agreed. |
| DEFER | RAG, autonomous agents and multi-agent product behaviour | No current product problem requires them. |
| DEFER | Song generation | It is a future content concept, not evidence needed for the current wedge. |

## Reproducibility issue to fix, not defer

This pre-final review identified that the locally evidenced `poc_env` uses Python 3.9.6 and MediaPipe 0.10.14, while Python 3.11 or 3.12 is the clean future rebuild target. The separate deployment requirements now pin MediaPipe 0.10.21; that was not the environment used for the historical local measurements. The default Python 3.13 installation cannot load the required legacy MediaPipe Solutions API. Before a future production-oriented handoff, rebuild on a documented supported version, install the pinned requirements, and rerun the real demo integration test.

## Main cut recommendation

For the final demonstration, do not try to show every platform page. Lead with:

```text
reference video
→ real movement evidence
→ clear human-review boundary
→ deterministic flashcard output
```

Use Content Operations as supporting evidence for governance and repeatability. Treat school assignment, story and song surfaces as context, not equal proof points.

## Product-language issue to fix before presentation

Some static pages show “Published,” “Published demo,” schools reached and children reached. They are labelled as prototype/illustrative in places, but a fast viewer could still mistake them for real approval or traction. Either demonstrate them only after explaining the local simulation, or change the most prominent labels to “demo library state.”
