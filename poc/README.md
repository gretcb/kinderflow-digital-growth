# Kinder Signs motion-representation POC

This local, single-video experiment tests whether a validated adult reference video can be converted into a body-relative and temporally coherent structured motion representation. It does not test sign correctness, semantics, clinical value, avatar generation, retargeting, or rendering fidelity.

## Setup

Use Python 3.11 or 3.12 with the MediaPipe 0.10 legacy Solutions API. From the repository root:

```bash
python -m venv poc_env
source poc_env/bin/activate
python -m pip install -r poc/requirements.txt
```

Keep the adult reference video local at `poc/input/sign_reference.mp4`. The video, raw CSVs, normalized CSVs, and preview videos are excluded from Git.

## Reproduce

```bash
python poc/src/extract_landmarks.py \
  --video poc/input/sign_reference.mp4

python poc/src/normalize_landmarks.py \
  --video-name sign_reference

python poc/src/analyse_motion.py \
  --video-name sign_reference
```

To regenerate the extraction coverage summary without rerunning MediaPipe:

```bash
python poc/src/validate_output.py --video-name sign_reference
```

The normalization defaults are a maximum three-frame internal gap and a centered three-frame rolling mean. Configure them with `--max-gap-frames` and `--smoothing-window`. No leading or trailing extrapolation is performed.

## Evidence outputs

- Raw evidence: `poc/output/landmarks/`
- Derived normalized data: `poc/output/normalized/`
- Missing-data, transition, summary, and plot evidence: `poc/output/diagnostics/`
- Detailed method and decision: `poc/poc_documentation.md`

Run regression checks after generating the local CSV outputs:

```bash
python -m unittest discover -s poc/tests -v
```

Current evidence status: `EXTRACTION_PASS`; `MOTION_REPRESENTATION_PARTIAL`. This means the representation supports further controlled experimentation subject to the documented conditions. It does not mean that the sign or product is validated.
