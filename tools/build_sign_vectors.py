"""Build deterministic KinderFlow sign vectors from the selected Open Peeps atoms.

The generated SVGs embed the source atom geometry; they do not redraw or trace the
Open Peeps face, hair, or body. Only the sign-specific arms, hands, movement cues,
and small accent fields are custom KinderFlow layers.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "assets/flashcards/source_libraries/Flat Assets/Separate Atoms"
OUTPUT_ROOT = ROOT / "prototype/assets/signs"
PROVENANCE_PATH = ROOT / "assets/flashcards/open_peeps/provenance.json"
SOURCES = {
    "face": SOURCE_ROOT / "face/Smile.svg",
    "hair": SOURCE_ROOT / "head/Bun 2.svg",
    "body": SOURCE_ROOT / "pose/sitting/mid-2.svg",
}


def inner_svg(path: Path) -> str:
    source = path.read_text(encoding="utf-8")
    match = re.search(r"<svg\b[^>]*>(.*)</svg>\s*$", source, re.DOTALL)
    if not match:
        raise ValueError(f"Cannot read SVG root: {path}")
    return match.group(1).strip()


def character_symbol() -> str:
    body = inner_svg(SOURCES["body"])
    hair = inner_svg(SOURCES["hair"])
    face = inner_svg(SOURCES["face"])
    return f"""
    <symbol id="open-peeps-character" viewBox="0 0 800 800">
      <g id="actual-open-peeps-body" aria-label="Actual Open Peeps mid-2 geometry">
        <svg x="124" y="305" width="552" height="668" viewBox="0 0 1534 1856">{body}</svg>
      </g>
      <g id="actual-open-peeps-head" aria-label="Actual Open Peeps Bun 2 geometry">
        <svg x="180" y="-20" width="440" height="493" viewBox="-100 -105 673 754">{hair}</svg>
      </g>
      <g id="actual-open-peeps-face" aria-label="Actual Open Peeps Smile geometry">
        <svg x="296" y="168" width="208" height="211" viewBox="0 0 289 293">{face}</svg>
      </g>
      <path d="M170 532 Q400 454 630 532 L660 800 H140Z" fill="#fffdf8"/>
      <path d="M176 534 Q400 460 624 534" fill="none" stroke="#111" stroke-width="11" stroke-linecap="round"/>
    </symbol>"""


def metadata(asset_id: str, sign_id: str, version: int, layout: str) -> str:
    payload = {
        "derivative_asset_id": asset_id,
        "sign_id": sign_id,
        "version": version,
        "layout": layout,
        "character_foundation": "Actual Open Peeps source geometry",
        "source_components": [str(path.relative_to(ROOT)) for path in SOURCES.values()],
        "custom_layers": "KinderFlow sign-specific arms/hands, movement cues, and restrained accent fields",
        "licence_basis": "Founder-verified CC0",
        "publication_status": "DRAFT",
    }
    return json.dumps(payload, separators=(",", ":")).replace("&", "&amp;").replace("<", "&lt;")


def more_hands(variant: str = "contact") -> str:
    separation = 42 if variant == "apart" else 5
    left_x = 400 - separation
    right_x = 400 + separation
    arrow = (
        '<path d="M310 500 H360 M490 500 H440" fill="none" stroke="#dc725d" '
        'stroke-width="9" stroke-linecap="round" marker-end="url(#arrow-coral)"/>'
        if variant == "apart"
        else '<path d="M335 486 Q400 454 465 486" fill="none" stroke="#dc725d" stroke-width="9" stroke-linecap="round"/><path d="M465 506 Q400 538 335 506" fill="none" stroke="#dc725d" stroke-width="9" stroke-linecap="round" marker-end="url(#arrow-coral)"/>'
    )
    return f"""
      <ellipse cx="400" cy="576" rx="180" ry="126" fill="#dce9e4"/>
      <path d="M188 676 Q224 566 {left_x - 62} 566" fill="none" stroke="#111" stroke-width="54" stroke-linecap="round"/>
      <path d="M612 676 Q576 566 {right_x + 62} 566" fill="none" stroke="#111" stroke-width="54" stroke-linecap="round"/>
      <path d="M188 676 Q224 566 {left_x - 62} 566" fill="none" stroke="#fffdf8" stroke-width="34" stroke-linecap="round"/>
      <path d="M612 676 Q576 566 {right_x + 62} 566" fill="none" stroke="#fffdf8" stroke-width="34" stroke-linecap="round"/>
      <g fill="#fffdf8" stroke="#111" stroke-width="10" stroke-linejoin="round">
        <path d="M{left_x - 86} 579 Q{left_x - 80} 531 {left_x - 42} 516 Q{left_x - 12} 504 {left_x + 4} 530 Q{left_x + 17} 551 {left_x + 39} 559 Q{left_x + 56} 568 {left_x + 43} 585 Q{left_x + 21} 610 {left_x - 24} 620 Q{left_x - 72} 622 {left_x - 86} 579Z"/>
        <path d="M{right_x + 86} 579 Q{right_x + 80} 531 {right_x + 42} 516 Q{right_x + 12} 504 {right_x - 4} 530 Q{right_x - 17} 551 {right_x - 39} 559 Q{right_x - 56} 568 {right_x - 43} 585 Q{right_x - 21} 610 {right_x + 24} 620 Q{right_x + 72} 622 {right_x + 86} 579Z"/>
      </g>
      <g fill="none" stroke="#111" stroke-width="7" stroke-linecap="round">
        <path d="M{left_x - 55} 550 Q{left_x - 29} 561 {left_x - 9} 579"/><path d="M{left_x - 66} 570 Q{left_x - 38} 580 {left_x - 18} 596"/>
        <path d="M{right_x + 55} 550 Q{right_x + 29} 561 {right_x + 9} 579"/><path d="M{right_x + 66} 570 Q{right_x + 38} 580 {right_x + 18} 596"/>
      </g>{arrow}"""


def eat_hand(variant: str = "mouth") -> str:
    end_x, end_y = ((486, 365) if variant == "mouth" else (528, 532))
    arrow = '<path d="M540 512 Q530 430 486 390" fill="none" stroke="#dc725d" stroke-width="10" stroke-linecap="round" marker-end="url(#arrow-coral)"/>' if variant != "mouth" else '<path d="M534 456 Q518 405 491 382" fill="none" stroke="#dc725d" stroke-width="10" stroke-linecap="round" marker-end="url(#arrow-coral)"/>'
    return f"""
      <circle cx="477" cy="374" r="94" fill="#eedcd7"/>
      <path d="M630 684 Q598 558 {end_x + 48} {end_y + 38}" fill="none" stroke="#111" stroke-width="56" stroke-linecap="round"/>
      <path d="M630 684 Q598 558 {end_x + 48} {end_y + 38}" fill="none" stroke="#fffdf8" stroke-width="36" stroke-linecap="round"/>
      <path d="M{end_x + 65} {end_y + 32} Q{end_x + 42} {end_y - 8} {end_x + 8} {end_y - 27} Q{end_x - 25} {end_y - 45} {end_x - 42} {end_y - 17} Q{end_x - 59} {end_y + 10} {end_x - 26} {end_y + 32} Q{end_x + 9} {end_y + 58} {end_x + 65} {end_y + 32}Z" fill="#fffdf8" stroke="#111" stroke-width="10" stroke-linejoin="round"/>
      <path d="M{end_x - 34} {end_y - 13} Q{end_x - 5} {end_y - 7} {end_x + 27} {end_y + 17} M{end_x - 22} {end_y - 29} Q{end_x + 9} {end_y - 20} {end_x + 39} {end_y + 4}" fill="none" stroke="#111" stroke-width="7" stroke-linecap="round"/>
      {arrow}"""


def defs() -> str:
    return """<defs>
      <marker id="arrow-coral" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10Z" fill="#dc725d"/></marker>
    </defs>"""


def one_pose(asset_id: str, sign_id: str, version: int, hands: str, label: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 800 800" role="img" aria-labelledby="title description">
  <title id="title">{label}</title>
  <desc id="description">Actual Open Peeps character geometry with a KinderFlow sign-specific hand pose. Human review is required.</desc>
  <metadata>{metadata(asset_id, sign_id, version, 'single_pose')}</metadata>
  {defs()}
  {character_symbol()}
  <rect width="800" height="800" rx="48" fill="#f8f6ef"/>
  <path d="M54 158 Q116 81 203 112 Q164 171 93 197Z" fill="#dce9e4"/>
  <path d="M686 111 Q755 148 730 225 Q670 193 651 139Z" fill="#ead8ab"/>
  <use href="#open-peeps-character"/>
  <g id="sign-specific-hands">{hands}</g>
</svg>
"""


def two_pose(asset_id: str, sign_id: str, version: int, first: str, second: str, label: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="720" viewBox="0 0 1000 720" role="img" aria-labelledby="title description">
  <title id="title">{label}</title>
  <desc id="description">Two-pose sequence built on exact Open Peeps components with custom sign-specific hands. Human review is required.</desc>
  <metadata>{metadata(asset_id, sign_id, version, 'two_pose_sequence')}</metadata>
  {defs()}
  {character_symbol()}
  <rect width="1000" height="720" rx="48" fill="#f8f6ef"/>
  <rect x="34" y="34" width="444" height="652" rx="34" fill="#fff" stroke="#d3d8d0" stroke-width="3"/>
  <rect x="522" y="34" width="444" height="652" rx="34" fill="#fff" stroke="#d3d8d0" stroke-width="3"/>
  <g transform="translate(42 96) scale(.52)"><use href="#open-peeps-character"/><g>{first}</g></g>
  <g transform="translate(530 96) scale(.52)"><use href="#open-peeps-character"/><g>{second}</g></g>
  <circle cx="478" cy="360" r="28" fill="#1f6f6b"/><path d="M468 360h20m-8-8 8 8-8 8" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="256" y="74" text-anchor="middle" font-family="Arial,sans-serif" font-size="20" font-weight="700" fill="#52605a">POSE A</text>
  <text x="744" y="74" text-anchor="middle" font-family="Arial,sans-serif" font-size="20" font-weight="700" fill="#52605a">POSE B</text>
</svg>
"""


def build_assets() -> dict:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    assets = {
        "more-a": one_pose("more-a", "more", 2, more_hands("contact"), "MORE single teaching pose"),
        "more-b": two_pose("more-b", "more", 2, more_hands("apart"), more_hands("contact"), "MORE start and contact sequence"),
        "more-c-v3": one_pose("more-c-v3", "more", 3, more_hands("apart"), "MORE alternate movement-focused pose"),
        "eat-a": one_pose("eat-a", "eat", 1, eat_hand("mouth"), "EAT mouth-contact teaching pose"),
        "eat-b": two_pose("eat-b", "eat", 1, eat_hand("start"), eat_hand("mouth"), "EAT start and mouth-contact sequence"),
        "eat-c-v2": one_pose("eat-c-v2", "eat", 2, eat_hand("start"), "EAT alternate approach pose"),
    }
    records = []
    for asset_id, content in assets.items():
        path = OUTPUT_ROOT / f"{asset_id.replace('-v3', '').replace('-v2', '')}.svg"
        path.write_text(content, encoding="utf-8")
        records.append(
            {
                "derivative_asset_id": asset_id,
                "path": str(path.relative_to(ROOT)),
                "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
            }
        )
    return {record["derivative_asset_id"]: record for record in records}


def write_provenance(derivatives: dict) -> None:
    payload = {
        "schema_version": "1.0",
        "library_name": "Open Peeps",
        "creator": "Pablo Stanley / Pabs Stanley",
        "official_source_url": "https://www.openpeeps.com/",
        "licence": "CC0",
        "verification_basis": "Founder-verified official CC0 reference",
        "date_recorded": str(date.today()),
        "selected_components": [
            {
                "role": role,
                "path": str(path.relative_to(ROOT)),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
            for role, path in SOURCES.items()
        ],
        "pose_reference_pool": [25, 34, 38, 42, 43, 44, 45, 46, 52, 57, 60, 62, 64, 67, 68, 71, 74, 77, 78, 90],
        "derivatives": list(derivatives.values()),
        "composition": "Exact selected SVG atom geometry embedded in a reusable character symbol; only sign arms/hands and accents are custom.",
        "voluntary_credit": "Character foundation: Open Peeps by Pablo Stanley.",
        "publication_status": "DRAFT",
    }
    PROVENANCE_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    built = build_assets()
    write_provenance(built)
    for record in built.values():
        print(f"{record['derivative_asset_id']} {record['sha256']} {record['path']}")
