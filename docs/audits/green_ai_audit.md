# KinderFlow Green AI Audit

**Audit date:** 4 September 2026
**Functional evidence baseline:** 8eb0742, Freeze connected KinderFlow capstone demo
**Round 2 closure context:** `release/capstone-demo` adds the deployment pin, reconciled documentation, and final submission evidence without changing the demonstrated product baseline
**Scope:** Current Kinder Signs local MVP and proposed controlled pilot

This audit distinguishes architecture choices from measured environmental results. KinderFlow has not measured energy use, carbon emissions, embodied hardware impact, water use, or avoided impact. No environmental-benefit claim is supported.

## Executive assessment

The current design limits unnecessary inference:

- Computer Vision runs during content preparation, not when a family opens material;
- a small approved library can use exact sign-ID retrieval rather than RAG;
- the workflow is fixed rather than agentic;
- most validation and visual composition are deterministic;
- the optional language-model step is bounded and is not required for the core product;
- reviewed content is designed for reuse across groups and nurseries; and
- Family View uses prepared material rather than live per-view generation.

These choices are evidence of a resource-conscious design direction. They do not prove lower energy or carbon impact. The repository contains no meter data, provider carbon data, hardware baseline, workload benchmark, or measured reuse benefit.

Three pre-generated Gemini FX videos also exist. Their generation energy, provider region, hardware, retry count, and carbon data are unknown. The current product has no integrated avatar-generation or landmark-to-video pipeline.

| Question | Evidence state | Finding |
| --- | --- | --- |
| Is live AI called when a family opens current content? | Evidence present | No |
| Does the current app use RAG? | Evidence present | No |
| Does the current app use autonomous agent loops? | Evidence present | No |
| Is Computer Vision processing local? | Evidence present | Yes |
| Is optional LLM use bounded? | Partial evidence | Later final adapter has design, mocked-provider tests, and dry-run only; a separate historical n8n POC execution exists without resource telemetry |
| Is content reused in production? | Measurement gap | Reuse is designed but published production signs equal zero |
| Are energy and carbon measured? | Measurement gap | No |
| Is Gemini generation impact known? | Measurement gap | No |

## System boundary

The audit includes:

1. receiving or loading an adult reference MP4;
2. local video decoding;
3. MediaPipe pose and hand inference;
4. OpenCV frame processing;
5. landmark normalization, plots, previews, and local artifacts;
6. deterministic SVG candidate creation and review;
7. optional family-copy drafting and evaluation;
8. pre-generated Gemini FX demo files;
9. local nursery and Family View interactions;
10. storage, network transfer, retries, and rework; and
11. potential reuse of one approved sign package.

The audit does not have measured data for upstream model training, MediaPipe model training, Open Peeps creation, device manufacture, data-centre cooling, employee travel, or end-user device production. These exclusions prevent a full life-cycle claim.

## Current workload inventory

| Workload | Current status | Main resource use | Current evidence | Measurement status |
| --- | --- | --- | --- | --- |
| Local MP4 upload | Implemented | Network loopback, storage, video decode | Local service and tests | Bytes known per file; energy unmeasured |
| Public direct MP4 URL | Implemented local control | External network transfer, temporary storage, video decode | Bounded fetch and tests | Transfer bytes bounded; energy unmeasured |
| MediaPipe extraction | Implemented | CPU or local acceleration, memory, runtime | Pipeline and WATER run evidence | Coverage measured; power unmeasured |
| OpenCV processing | Implemented | CPU, memory, file input and output | Pipeline | Power unmeasured |
| ffmpeg preview conversion | Implemented where available | CPU, storage, encode time | Pipeline | Power unmeasured |
| Landmark plots and previews | Implemented | CPU and local storage | Run artifacts and POC output | File size may be observed; energy unmeasured |
| Deterministic SVG composition | Implemented | Small local compute and file storage | 18 draft sign candidates | Energy unmeasured |
| Exact sign retrieval | Implemented | Small JSON read and browser work | Six-sign data and registry | Energy unmeasured |
| Optional LLM wording | Code, dry-run evidence, and separate historical n8n POC execution | Potential external inference and network | Schema, exact n8n export and execution screenshot, LangSmith dry-run | No token, energy, carbon, retry, or provider telemetry preserved |
| Story draft | Deterministic prototype | Browser compute | Prototype code | Not current GenAI |
| Gemini FX output generation | Performed separately before runtime | Unknown provider inference | Three local demo MP4 files | Provider impact unknown |
| Family View | Local/session-based MVP | Browser rendering and local assets | Assignment-driven mini-library using synthetic session state | No production traffic data |

## Architecture evidence

### Deterministic-first design

The service delegates stable rules to code:

- file and URL validation;
- address, redirect, MIME, byte, and time limits;
- landmark normalization;
- threshold and fallback routing;
- schema validation;
- banned-claim checks;
- sign-ID retrieval;
- registry and hash validation; and
- deterministic SVG composition.

This reduces uncontrolled retries and makes each decision inspectable. It may also reduce compute compared with using a generative model for every step. That comparison has not been measured.

### Local Computer Vision

MediaPipe and OpenCV run on the local host in the evidenced MVP. The service produces reusable technical artifacts from one adult reference run.

Local processing avoids a required cloud video upload in the current flow. It does not make the run impact-free. Device efficiency, power source, runtime, frame count, decode and encode work, and reprocessing all affect impact.

The direct URL route adds an external transfer before local processing. It caps the video at 100 MB and limits total fetch time and redirects, but the repository does not measure network energy or source-host impact.

### Exact retrieval instead of RAG

The current canonical set has six sign IDs. Exact lookup is sufficient for that bounded library. No embedding store, vector database, semantic retrieval, retrieval evaluation, or RAG inference appears in the current product.

RAG should remain out of scope until a larger approved multilingual library creates a retrieval problem that exact IDs and metadata cannot solve. If that point arrives, measure quality gain and added compute before adoption.

### Fixed workflow instead of agentic loops

The current n8n design has explicit steps, branches, quality gates, and review preparation. The exact export and its separate successful historical execution evidence are versioned. It is not an autonomous planning agent or a production deployment.

This fixed structure limits repeated tool calls and makes retries easier to count. Agentic orchestration should remain out of scope unless content volume and exception handling create a measured need.

### Bounded optional language model

The optional model path transforms approved sign and routine data into concise family wording. The core Computer Vision and static family-material path do not depend on it.

Current evidence includes local samples, JSON Schema checks, deterministic quality gates, the exact 12-node n8n export, a screenshot of its successful historical governed-draft execution on 31 August 2026, and a LangSmith dry-run with network calls false. The historical n8n evidence does not preserve token count, provider telemetry, energy, carbon, or retry measurements; it is not production deployment or proof of the later final MVP adapter. A fresh provider-backed rerun requires a new authorised credential because the former OpenAI course credential is unavailable.

Before live use:

- test a human-authored and deterministic baseline;
- use the smallest model that meets approved quality criteria;
- cap prompt and output size;
- reject retries that cannot improve a defined failure;
- cache an approved output by content and prompt version;
- prevent per-family or per-view regeneration;
- record provider, model, region, tokens, latency, and errors; and
- obtain provider environmental data where available.

### Reusable content

The product is designed to create a reviewed sign package once and reuse it across groups, family materials, and nurseries. Family access should retrieve the prepared asset without rerunning Computer Vision or an LLM.

This is an architecture hypothesis, not a realised saving. The canonical registry records zero school-available signs, and no real nursery traffic or reuse count exists.

Measure:

- approved assets created;
- groups, family accounts, and nurseries served per asset;
- content views per approved generation;
- rework and withdrawal;
- storage copies; and
- compute per approved and actually used asset.

Unused or repeatedly rejected assets can erase the expected reuse advantage.

## Gemini FX boundary

The exact current mapping is:

| Sign | File | Generation relationship |
| --- | --- | --- |
| MORE | mas.mp4 | Prepared separately |
| HELP | ayuda.mp4 | Prepared separately |
| MILK | leche.mp4 | Prepared separately |
| EAT | None | Static flow only |
| SLEEP | None | Static flow only |
| WATER | None | Static flow only |

These videos were prepared separately as illustrative motion previews. They are not generated automatically from the current MediaPipe run or its landmarks.

The repository does not record:

- model version;
- provider region;
- input and output token or media units;
- generation count;
- failed attempts;
- compute hardware;
- electricity use;
- carbon intensity;
- storage before repository capture; or
- provider retention.

Do not describe the files as an efficient animation pipeline. If the pilot retains them, request available provider data, record every generation attempt, and compare the result with reviewed static or human-produced alternatives. Rights and sign-fidelity gates also apply.

## Data, storage, and network

### Current storage

The workflow can create:

- copied or downloaded reference video;
- raw landmarks;
- normalized landmarks;
- diagnostic summaries;
- plots;
- reference and overlay previews;
- visual candidates; and
- content package files.

Ignored local run directories are not automatically deleted. Duplicate runs and previews can increase storage without improving an approved asset.

### Storage controls

- delete raw and temporary files on an approved retention schedule;
- retain only evidence required for review, accountability, or correction;
- avoid duplicate renditions unless a client or browser requirement justifies them;
- record output size by run and approved asset;
- expire failed and abandoned runs quickly;
- deduplicate approved assets by content hash and version; and
- measure backup copies and deletion lag.

### Network controls

- prefer a registered local source when it meets the purpose;
- avoid repeated direct-URL downloads of the same authorised asset;
- cache only when rights, privacy, and freshness permit;
- prevent production requests to unapproved hosts;
- keep model prompts free of media and personal data;
- serve one approved family asset rather than regenerate it; and
- measure ingress and egress bytes.

These controls must not weaken privacy, security, or correction requirements to save compute.

## Measurement plan

### Functional units

Measure at least four units separately:

1. one adult reference processed into a reviewable technical run;
2. one sign package that receives qualified approval;
3. one bounded family-copy draft that receives approval; and
4. one hundred authorised views of an approved family asset.

A run that fails review still consumes resources and belongs in the denominator.

### Minimum telemetry

| Measure | Unit | Collection point |
| --- | --- | --- |
| Runtime | Seconds per stage and per run | Local service |
| Device utilisation | Average and peak CPU, GPU if used, and memory | Host monitor |
| Electricity | kWh per run and per approved asset | External power meter or supported device telemetry |
| Reference transfer | MB ingress per run | Direct URL or upload service |
| Artifact storage | MB retained per run and approved asset | Run and asset stores |
| Model use | Provider, model, region, input and output units, calls, retries | Optional model wrapper |
| Gemini generation | Attempts, duration, output size, provider metadata | Generation record if repeated |
| Review and rework | Attempts, rejected candidates, reruns, reviewer minutes | Content operations log |
| Reuse | Groups, nurseries, accounts, and views per approved asset | Delivery analytics |
| Carbon | gCO2e per functional unit | kWh and documented regional or provider factor |

Report both energy and carbon. A low-energy run in a high-carbon region and a higher-energy run in a lower-carbon region are not equivalent.

### Baseline comparison

Compare:

- current deterministic family copy with optional model-assisted copy;
- one approved central asset with repeated local preparation;
- tracked-pose route with avoidable reruns;
- static visual with Gemini motion preview where both meet the user need; and
- current file retention with the proposed deletion schedule.

Use the same quality threshold for each comparison. A cheaper or lower-energy output that fails sign review is not a valid substitute.

## Claims policy

Allowed current wording:

- Kinder Signs uses a deterministic-first, local content-preparation architecture.
- The small sign library uses exact retrieval and does not need RAG.
- The bounded workflow does not use agentic loops.
- Family View does not trigger live Computer Vision or LLM inference.
- Reviewed content is designed for reuse.
- Energy and carbon are not yet measured.

Unsupported wording:

- Kinder Signs reduces carbon emissions.
- Local processing is greener than cloud processing.
- Deterministic output is proven to use less energy.
- Reuse has already reduced cost or emissions.
- The Gemini previews are environmentally efficient.
- KinderFlow is carbon neutral or sustainable.

Every future environmental claim needs a defined baseline, functional unit, measurement period, calculation method, uncertainty, and reviewer.

## Pilot gates and decision rules

| Client fact | Action | Target | Owner | Decision rule |
| --- | --- | --- | --- | --- |
| No energy baseline exists | Instrument the agreed pilot hardware | Energy captured for at least 90 percent of technical runs | Engineering lead | Make no efficiency claim below coverage target |
| Published production signs equal zero | Measure creation, approval, use, and rework together | Compute reported per approved and used sign | Content Operations | Iterate if reruns or unused assets dominate |
| Live model use is not evidenced | Compare human, deterministic, and candidate model paths | Select only a path that meets quality and resource thresholds | Product Owner | Keep model optional if gain is not material |
| Gemini impact is unknown | Obtain provider data and log any new generation | Every generation attempt and output recorded | Product Owner | Do not make an environmental claim without data |
| Direct URL adds network work | Log bytes and avoid duplicate retrieval | Duplicate authorised downloads below an agreed pilot limit | Engineering lead | Change intake if transfer waste is material |
| Storage has no automated expiry | Apply GDPR-aligned retention and verify deletion | One hundred percent of test records expire as designed | Engineering and privacy owner | No pilot if deletion cannot be shown |
| Reuse is only a hypothesis | Measure approved asset use across groups and nurseries | Target fixed before pilot | Pilot lead | Continue only if reuse improves cost and resource use without quality loss |
| Carbon factors are undecided | Record provider and host regions and calculation source | One documented method per reporting period | Sustainability owner | Report energy only if carbon evidence is not credible |

## Evidence index

- [Local Computer Vision pipeline](../../mvp/pipeline.py)
- [Local service](../../mvp/app.py)
- [Current MVP tests](../../mvp/tests/)
- [WATER technical POC evidence](../../poc/output/)
- [Canonical asset registry](../../assets/registry/sign_asset_registry.json)
- [Asset inventory](../../assets/registry/sign_asset_inventory.md)
- [Visual sign packages](../../prototype/data/visual_sign_packages.json)
- [LangSmith dry-run](../../workflow/langsmith_dry_run_summary.json)
- [n8n workflow](../../workflow/kinder_signs_n8n_workflow.json)
- [Successful historical n8n execution](../../workflow/evidence/n8n_successful_execution_2026-08-31.png)
- [Family View prototype](../../prototype/family.html)
- [GDPR retention and data-flow record](../../compliance/gdpr_documentation.md)

## Audit conclusion

Architecture evidence is present. Environmental measurement is not.

The pilot should preserve exact retrieval, deterministic controls, central reuse, and no live per-view inference. It should also measure the full path from input transfer through review, rework, storage, approved reuse, and deletion. Until those measurements exist, KinderFlow should make no environmental-benefit claim.
