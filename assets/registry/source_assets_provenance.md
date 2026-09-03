# Kinder Signs source-assets provenance

## Scope and authority

`sign_asset_registry.json` is the single canonical mapping for the six current Kinder Signs packages: MORE, HELP, EAT, SLEEP, MILK and WATER. The builder refreshes file facts (existence, media type, byte size and SHA-256) in that file and generates `sign_asset_inventory.md`; it does not maintain a second mapping and never copies external material.

All paths are repository-relative. `../resources` is founder-provided external reference storage and is not part of this repository. `.env`, `poc_env/`, `mvp/runs/` and `/tmp/` are local-only paths covered by repository ignore rules; the `.gitkeep` contract in `mvp/runs/` remains versioned. Previously committed preview images under `tmp/` are historical repository state and are not registry inputs.

## Open Peeps

- Library: Open Peeps
- Creator: Pablo Stanley / Pabs Stanley
- Official source: <https://www.openpeeps.com/>
- Licence basis: founder-verified CC0 from the official source
- Base identity reference: `../resources/Flat Assets/Separate Atoms/a person/bust.svg`
- Complementary arm/hand reference: `../resources/Flat Assets/Templates/Bust/peep-4.svg`
- Exact hand-style reference: `../resources/Flat Assets/Separate Atoms/pose/standing/pointing_finger-1.svg`

The registry resolves the exact `pointing_finger-1.svg` atom case-insensitively from the standing-pose atom directory and records its current SHA-256. It is used only to study Open Peeps hand/finger and arm-to-hand transitions. `../resources/Flat Assets/Separate Atoms/body/Pointing Up.svg` remains deliberately excluded as a substitute. Bust and Standing compositions are supplementary visual references, not final character poses and never sign-mechanics evidence.

## Functional sign references

The six sign-specific JPGs under `../resources/ilustraciones/` and the shared JPG/EPS illustration sheets are founder-provided references. They define mechanics and pose information, not KinderFlow character identity. Their underlying licence and redistribution rights have not been documented, so the registry fails closed for printable use.

The six MP4 files under `../resources/video_input/` are the canonical reference inputs. Their presence and SHA-256 values are validated independently from every output video. They support technical and human review but do not certify linguistic correctness. The local `poc/input/sign_reference.mp4` demo is byte-identical to the registered WATER input, so the demo flow fixes its operator-selected identity to WATER; this is explicit source identity, not automatic sign recognition.

The six PDFs under `../resources/flashcards/` are reference-only. The validator rejects any attempt to place one in `flashcard_outputs` or `routine_card_outputs`; they are never copied into production/runtime output.

The six PNGs under `../resources/iconos/` are vendor-artwork references only. They may inform routine context, but cannot become final KinderFlow icons or enter printable output.

## Gemini FX demo outputs

The files `mas.mp4`, `ayuda.mp4` and `leche.mp4` are classified as `PREGENERATED_DEMO_OUTPUT` and mapped to MORE, HELP and MILK respectively. Provider: Google Labs FX / Gemini FX.

These videos:

- were not generated from the current landmark run;
- are not the canonical reference input videos;
- are not linguistically certified; and
- require confirmation of presentation and redistribution rights.

EAT, SLEEP and WATER have no current Gemini FX output. This is an explicit valid state and does not block their static flow.

## KinderFlow evidence and derived assets

The committed diagnostic JSON/PNG files are `TECHNICAL_EVIDENCE` for the registered WATER demo run. They measure capture and movement representation only; they do not approve a sign, visual or publication. MORE keeps its own reference input but no longer claims these WATER-derived diagnostics.

The sign SVG files under `prototype/assets/signs/` are `KINDERFLOW_DERIVED_ASSET` visual options. They retain Open Peeps provenance plus KinderFlow custom layers. They are not marked printable because human visual review and publication approval remain incomplete.

The current contextual MORE image is classified as a `KINDERFLOW_RUNTIME_ASSET` because it is used by the existing prototype. Its production rights record is incomplete, so the registry does not approve redistribution or printable use.

## Refresh and validation

From the repository root in the validated environment:

```bash
poc_env/bin/python tools/build_sign_asset_registry.py --write
poc_env/bin/python tools/build_sign_asset_registry.py --check
poc_env/bin/python -m unittest discover -s tools/tests -v
```

`--write` only updates registry metadata and the generated Markdown inventory. `--check` fails for stale hashes, missing required files, duplicate mappings, unsafe paths, output/input confusion, reference-PDF output leakage or schema/semantic errors.
