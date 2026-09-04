# Kinder Signs motion-representation POC

This local, single-video experiment tests whether a validated adult reference video can be converted into a body-relative and temporally coherent structured motion representation. It does not test sign correctness, semantics, clinical value, avatar generation, retargeting, or rendering fidelity.

## Setup

Python 3.11 or 3.12 with the MediaPipe 0.10 legacy Solutions API is the target/recommended clean environment, but that exact setup has not yet been revalidated in the current evidence pass. The currently evidenced local `poc_env` uses Python 3.9.6 with MediaPipe 0.10.14. `poc/requirements.txt` separately pins MediaPipe 0.10.21 for deployment; that pin was not the environment used for the historical local measurements. The machine's default Python 3.13/MediaPipe 1.0.1 environment is incompatible with the legacy `solutions` API. From the repository root:

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
