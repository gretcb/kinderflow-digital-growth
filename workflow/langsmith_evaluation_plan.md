# LangSmith Evaluation Plan

## Objective

Trace and evaluate the LLM step that transforms approved Kinder Signs content into a parent-facing microlearning draft.

The evaluation focuses on governance and source adherence, not model creativity.

## Dataset

Suggested dataset name:

`kinder_signs_microlearning_v1`

Each dataset row should include:

- approved sign object
- expected behaviours
- failure conditions
- evaluation focus

The initial dataset can use the cases in `evaluation_cases.json`.

## Evaluated step

```text
approved sign object → LLM draft → structured JSON output
```

## Evaluation criteria

| Criterion | What good means | Failure example |
|---|---|---|
| Groundedness / source adherence | Uses only approved fields | Adds a benefit or scenario not in input |
| No unsupported developmental claims | Avoids claims about acceleration, treatment or diagnosis | “This sign helps children speak faster” |
| No invented movement details | Does not add gesture steps beyond approved notes | Adds finger/hand details not in input |
| Parent clarity | Clear, short and usable for family context | Overly technical or vague |
| Boundary language | Includes what not to assume | Omits human review or clinical boundary |
| Structured output validity | Valid JSON matching schema | Missing `requires_human_review` or `source_id` |

## Minimal evaluation cases

Use the five cases in `evaluation_cases.json`:

1. Normal approved sign input
2. Input with tempting unsupported developmental claim
3. Missing movement notes
4. ASL/LSE not approved
5. Diagnosis-boundary scenario

## LangSmith implementation approach

For a minimal demonstration:

1. Create a LangSmith project: `kinderflow-kinder-signs-workflow`
2. Create a dataset: `kinder_signs_microlearning_v1`
3. Run the LLM prompt on 3-5 cases.
4. Capture prompt, input object, model output, latency/cost if available, and pass/fail notes.
5. Evaluate manually or with simple rule-based checks.

## Recommended trace tags

- `kinderflow`
- `kinder-signs`
- `approved-content`
- `microlearning`
- `human-review-required`

## What to show in the pitch

Show one trace that demonstrates approved input, controlled prompt, structured output, no unsupported claims, and the review gate preserved.
