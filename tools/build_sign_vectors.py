#!/usr/bin/env python3
"""Deterministically compose source-grounded KinderFlow sign illustrations.

The registered Open Peeps bust is the sole character base. Registered Open
Peeps pose files inform only the line grammar; sign mechanics come from each
sign's functional image, input video, and reference flashcard.
"""

from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence, Tuple


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "assets/registry/sign_asset_registry.json"
OUTPUT_ROOT = REPO_ROOT / "prototype/assets/signs"
PACKAGE_PATH = REPO_ROOT / "prototype/data/visual_sign_packages.json"
PROVENANCE_PATH = REPO_ROOT / "assets/flashcards/open_peeps/provenance.json"
CONTACT_SHEET_PATH = REPO_ROOT / "tmp/qa/sign-visual-contact-sheet.html"

SIGN_ORDER = ("more", "help", "eat", "sleep", "milk", "water")

SIGN_SPECS: Dict[str, Dict[str, Any]] = {
    "more": {
        "labels": {"en": "MORE", "es": "MÁS"},
        "usage": {
            "en": "Use during a familiar routine when a child asks for another portion, turn or repetition.",
            "es": "Úsalo durante una rutina habitual cuando un niño pida otra porción, turno o repetición.",
        },
        "routine": {"en": "Snack time", "es": "Hora de la merienda"},
        "routine_guidance": {
            "en": "Use the sign naturally just before offering more food.",
            "es": "Haz el signo de forma natural justo antes de ofrecer más comida.",
        },
        "hands": 2,
        "dominant": "Both hands participate independently",
        "non_dominant": "Both hands participate independently",
        "handshape": "Two grouped flat-O hands",
        "orientation": "Hands face one another",
        "location": "Upper chest",
        "movement": "The two grouped fingertip sets move inward, meet, separate and repeat.",
        "direction": "Inward",
        "repetition": "Small repeated contact",
        "contact": "The two grouped fingertip sets meet",
        "presentation": "A start/contact sequence preserves the inward meeting and repeated relationship.",
        "review": "HUMAN_SELECTED_FRAME",
        "checks": ["Two independent hands", "Grouped flat-O handshape", "Visible wrists, thumbs and four fingers", "Upper-chest location", "Meet, separate and repeat"],
    },
    "help": {
        "labels": {"en": "HELP", "es": "AYUDA"},
        "usage": {"en": "Use when offering or asking for help in a familiar activity.", "es": "Úsalo al ofrecer o pedir ayuda en una actividad habitual."},
        "routine": {"en": "Getting ready", "es": "Prepararse"},
        "routine_guidance": {"en": "Pair the sign with a calm offer of help.", "es": "Acompaña el signo con una oferta tranquila de ayuda."},
        "hands": 2,
        "dominant": "Closed A-like hand",
        "non_dominant": "Open supporting palm",
        "handshape": "Asymmetric closed hand supported by an open palm",
        "orientation": "Supporting palm faces upward",
        "location": "Upper chest",
        "movement": "The supported hands move upward together.",
        "direction": "Upward",
        "repetition": "One clear upward movement",
        "contact": "Closed dominant hand rests on supporting open palm",
        "presentation": "A start/end sequence makes the support and upward movement explicit.",
        "review": "HUMAN_SELECTED_FRAME",
        "checks": ["Two asymmetric hands", "Dominant closed-A hand", "Supporting open palm", "Supported contact", "Upward movement"],
    },
    "eat": {
        "labels": {"en": "EAT", "es": "COMER"},
        "usage": {"en": "Use when food is offered or a familiar meal begins.", "es": "Úsalo al ofrecer comida o al comenzar una comida habitual."},
        "routine": {"en": "Mealtime", "es": "Hora de comer"},
        "routine_guidance": {"en": "Use the sign naturally when a familiar meal begins.", "es": "Haz el signo de forma natural al comenzar una comida habitual."},
        "hands": 1,
        "dominant": "One dominant hand",
        "non_dominant": "Not used",
        "handshape": "Grouped flat-O hand",
        "orientation": "Toward the mouth",
        "location": "Mouth",
        "movement": "The grouped fingertips approach and contact the mouth.",
        "direction": "Toward the mouth",
        "repetition": "One tap for this reviewed teaching distinction",
        "contact": "Grouped fingertips meet the mouth",
        "presentation": "A start/contact sequence makes the approach and reviewed one-tap mouth location clear.",
        "review": "KNOWLEDGE_REFERENCE_FALLBACK",
        "checks": ["One hand", "Grouped flat-O handshape", "Mouth location", "One reviewed tap", "Clear approach path"],
    },
    "sleep": {
        "labels": {"en": "SLEEP", "es": "DORMIR"},
        "usage": {"en": "Use while settling into a familiar sleep routine.", "es": "Úsalo al comenzar una rutina habitual para dormir."},
        "routine": {"en": "Bedtime", "es": "Hora de dormir"},
        "routine_guidance": {"en": "Show the sign before the next calm bedtime step.", "es": "Haz el signo antes del siguiente paso tranquilo para dormir."},
        "hands": 1,
        "dominant": "One dominant hand",
        "non_dominant": "Not used",
        "handshape": "Fingers spread, then gathered",
        "orientation": "Palm faces the signer",
        "location": "In front of the face to below the chin",
        "movement": "A spread hand moves downward while the fingers gather below the chin.",
        "direction": "Downward",
        "repetition": "One downward movement",
        "contact": "No sustained face covering",
        "presentation": "Separate start and end states keep the face clear and show the gathering action.",
        "review": "HUMAN_SELECTED_FRAME",
        "checks": ["One hand", "Fingers-spread start", "Fingers-gathered end", "Downward path", "End below chin and clear of face"],
    },
    "milk": {
        "labels": {"en": "MILK", "es": "LECHE"},
        "usage": {"en": "Use when milk is offered in a familiar feeding routine.", "es": "Úsalo al ofrecer leche en una rutina habitual de alimentación."},
        "routine": {"en": "Milk time", "es": "Hora de la leche"},
        "routine_guidance": {"en": "Pair the sign with the milk choice before serving it.", "es": "Acompaña el signo con la elección de leche antes de servirla."},
        "hands": 1,
        "dominant": "One dominant hand",
        "non_dominant": "Not used",
        "handshape": "Open hand closes into a fist",
        "orientation": "Hand remains upright",
        "location": "In front of the upper torso",
        "movement": "The hand opens and closes in a repeated squeeze-and-release action without vertical travel.",
        "direction": "Open and closed in place",
        "repetition": "Repeat squeeze and release",
        "contact": "Fingers close into the palm",
        "presentation": "Open/closed states show the squeeze and release without implying a vertical path.",
        "review": "HUMAN_SELECTED_FRAME",
        "checks": ["One hand", "Open start", "Closed end", "Squeeze and release", "No vertical trajectory"],
    },
    "water": {
        "labels": {"en": "WATER", "es": "AGUA"},
        "usage": {"en": "Use when offering or asking for water in a familiar routine.", "es": "Úsalo al ofrecer o pedir agua en una rutina habitual."},
        "routine": {"en": "Drink break", "es": "Pausa para beber"},
        "routine_guidance": {"en": "Show the sign just before offering the water choice.", "es": "Haz el signo justo antes de ofrecer la opción de agua."},
        "hands": 1,
        "dominant": "One dominant hand",
        "non_dominant": "Not used",
        "handshape": "Three fingers extended with little finger and thumb folded",
        "orientation": "Palm faces across the body",
        "location": "Beside the lower face",
        "movement": "The three-finger hand moves a short distance to the lower face for contact.",
        "direction": "Toward the lower face",
        "repetition": "Short reviewed contact",
        "contact": "Extended index area approaches the lower face",
        "presentation": "A start/contact sequence follows the supplied WATER references and keeps the three-finger shape readable.",
        "review": "HUMAN_SELECTED_FRAME",
        "checks": ["One hand", "Three extended fingers", "Folded little finger and visible thumb", "Lower-face location", "Short contact path"],
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_registry() -> Dict[str, Any]:
    payload = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload.get("assets"), dict):
        raise ValueError("Registry has no assets mapping: {0}".format(REGISTRY_PATH))
    return payload


def load_asset(assets: Mapping[str, Any], asset_id: str) -> Dict[str, Any]:
    if asset_id not in assets:
        raise KeyError("Required registry asset is missing: {0}".format(asset_id))
    record = dict(assets[asset_id])
    source_path = (REPO_ROOT / record["path"]).resolve()
    if not source_path.is_file():
        raise FileNotFoundError("Registered asset does not exist: {0}".format(source_path))
    actual_hash = sha256(source_path)
    if actual_hash != record.get("sha256"):
        raise ValueError("Registered hash mismatch for {0}".format(asset_id))
    record.update({"asset_id": asset_id, "absolute_path": source_path})
    return record


def load_sources() -> Dict[str, Any]:
    assets = read_registry()["assets"]
    common = {
        "base": load_asset(assets, "open_peeps_bust_base"),
        "hand_grammar": load_asset(assets, "open_peeps_pointing_finger_reference"),
        "arm_grammar": load_asset(assets, "open_peeps_arm_reference"),
        "hand_sheet_jpg": load_asset(assets, "functional_hand_sheet_jpg"),
        "hand_sheet_eps": load_asset(assets, "functional_hand_sheet_eps"),
    }
    signs: Dict[str, Dict[str, Any]] = {}
    for sign_id in SIGN_ORDER:
        signs[sign_id] = {
            "functional": load_asset(assets, "functional_{0}".format(sign_id)),
            "video": load_asset(assets, "input_{0}".format(sign_id)),
            "flashcard": load_asset(assets, "flashcard_{0}_reference".format(sign_id)),
        }
    # The committed diagnostics describe WATER only. They must never ground MORE.
    signs["water"]["landmark_support"] = load_asset(assets, "water_landmark_summary")
    return {"common": common, "signs": signs}


def inner_svg(path: Path) -> str:
    source = path.read_text(encoding="utf-8")
    opening = source.index(">", source.index("<svg")) + 1
    closing = source.rindex("</svg>")
    return source[opening:closing].strip()


def xml_json(payload: Mapping[str, Any]) -> str:
    return html.escape(json.dumps(payload, ensure_ascii=False, sort_keys=True), quote=False)


def character_symbol(bust_inner: str) -> str:
    return (
        '<g class="open-peeps-bust base-character" data-base-character="exact-registered-bust" '
        'transform="translate(178 118) scale(.32)">\n'
        '  <!-- Exact registered Open Peeps bust geometry; sole character base. -->\n'
        + bust_inner
        + "\n</g>"
    )


def safe_contract(width: int, height: int) -> str:
    return """<g class="composition-contract">
  <rect class="gesture-safe-zone" data-gesture-safe-zone="true" data-decoration-exclusion="true" x="96" y="108" width="{w}" height="{h}" fill="none" stroke="none"/>
  <circle class="peripheral-accent" data-outside-gesture-safe-zone="true" aria-hidden="true" cx="48" cy="108" r="10" fill="#ee7f72"/>
  <path class="peripheral-accent" data-outside-gesture-safe-zone="true" aria-hidden="true" d="M58 {bottom} h28" fill="none" stroke="#efbd67" stroke-width="9" stroke-linecap="round"/>
</g>""".format(w=width - 192, h=height - 196, bottom=height - 68)


def neutral_arm_occlusion(sign_id: str) -> str:
    """Hide only the neutral bust arms that a sign-specific limb replaces."""
    masks = [
        '<path class="neutral-arm-mask dominant-arm-mask" data-replaces-neutral-arm="viewer-right" d="M434 438 L502 430 L508 558 L428 558 Z" fill="#fffdf9"/>',
    ]
    if SIGN_SPECS[sign_id]["hands"] == 2:
        masks.insert(
            0,
            '<path class="neutral-arm-mask supporting-arm-mask" data-replaces-neutral-arm="viewer-left" d="M218 430 L286 438 L292 558 L214 558 Z" fill="#fffdf9"/>',
        )
    return '<g class="neutral-arm-occlusion" aria-hidden="true">{0}</g>'.format("".join(masks))


def arm_tube(
    limb_id: str,
    upper_path_d: str,
    forearm_path_d: str,
    elbow: Tuple[int, int],
    wrist_d: str,
) -> str:
    return """<g id="{id}" class="complete-upper-limb shoulder-arm">
  <path class="arm-outline upper-arm-outline" d="{upper}" fill="none" stroke="#111111" stroke-width="44" stroke-linecap="round" stroke-linejoin="round"/>
  <path class="arm-outline forearm-outline" d="{forearm}" fill="none" stroke="#111111" stroke-width="44" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="{ex}" cy="{ey}" r="22" fill="#111111"/>
  <path class="upper-arm" d="{upper}" fill="none" stroke="#ffffff" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>
  <path class="forearm" d="{forearm}" fill="none" stroke="#ffffff" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>
  <circle class="elbow" cx="{ex}" cy="{ey}" r="15" fill="#ffffff" data-visible-as="curved-joint"/>
  <path class="wrist" d="{wrist}" fill="none" stroke="#111111" stroke-width="7" stroke-linecap="round"/>
</g>""".format(id=limb_id, upper=upper_path_d, forearm=forearm_path_d, ex=elbow[0], ey=elbow[1], wrist=wrist_d)


def arrow(path_d: str, cue: str) -> str:
    return '<path class="movement-arrow" data-avoids-hand-contours="true" data-cue="{0}" d="{1}" fill="none" stroke="#ee7f72" stroke-width="9" stroke-linecap="round" marker-end="url(#movement-arrowhead)"/>'.format(cue, path_d)


def finger(path_d: str, name: str, width: float = 8) -> str:
    return '<path class="finger-path {0}" d="{1}" fill="none" stroke="#111111" stroke-width="{2}" stroke-linecap="round" stroke-linejoin="round"/>'.format(name, path_d, width)


def flat_o_hand(hand_id: str, x: int, y: int, direction: str, rotation: int = 0, scale: float = 1.0) -> str:
    if direction == "right":
        fingers = (
            "M-5 -13 C8 -13 19 -10 28 -6",
            "M-4 -6 C10 -6 21 -4 30 -1",
            "M-4 1 C10 1 21 2 29 5",
            "M-5 8 C8 9 18 10 25 11",
        )
        palm = "M-34 -14 C-22 -22 -7 -22 3 -15 L4 14 C-8 20 -23 20 -34 12 Z"
        thumb = "M-12 13 C-2 25 13 24 27 12"
        wrist = "M-52 -14 L-34 -14 M-52 13 L-34 12"
    elif direction == "left":
        # Deliberately authored coordinates: no mechanical mirroring of the right hand.
        fingers = (
            "M5 -14 C-8 -14 -19 -10 -29 -6",
            "M4 -7 C-10 -7 -21 -4 -31 -1",
            "M4 0 C-10 0 -21 2 -30 5",
            "M5 8 C-8 9 -18 10 -26 11",
        )
        palm = "M34 -14 C22 -22 7 -22 -3 -15 L-4 14 C8 20 23 20 34 12 Z"
        thumb = "M12 13 C2 25 -13 24 -27 12"
        wrist = "M52 -14 L34 -14 M52 13 L34 12"
    else:
        raise ValueError("flat-O direction must be left or right")
    finger_markup = "\n".join(finger(path, "finger-{0}".format(index + 1), 3.5) for index, path in enumerate(fingers))
    return """<g id="{id}" class="flat-o-hand explicit-hand-anatomy" data-handshape="flat-o" data-profile="horizontal-side" data-authored-direction="{direction}" transform="translate({x} {y}) rotate({rotation}) scale({scale})">
  <path class="wrist hand-wrist" d="{wrist}" fill="none" stroke="#111111" stroke-width="7" stroke-linecap="round"/>
  <path class="palm hand-palm" d="{palm}" fill="#ffffff" stroke="#111111" stroke-width="6" stroke-linejoin="round"/>
  {fingers}
  <path class="thumb hand-thumb" d="{thumb}" fill="none" stroke="#111111" stroke-width="5.5" stroke-linecap="round"/>
</g>""".format(id=hand_id, direction=direction, x=x, y=y, rotation=rotation, scale=scale, wrist=wrist, palm=palm, fingers=finger_markup, thumb=thumb)


def open_hand(hand_id: str, x: int, y: int, rotation: int = 0, scale: float = 1.0, state: str = "open") -> str:
    fingers = (
        "M-23 -13 L-48 -48",
        "M-10 -22 L-23 -66",
        "M5 -23 L4 -70",
        "M19 -17 L30 -58",
    )
    return """<g id="{id}" class="open-hand explicit-hand-anatomy fingers-spread" data-handshape="open" data-state="{state}" transform="translate({x} {y}) rotate({rotation}) scale({scale})">
  <path class="wrist hand-wrist" d="M-20 34 L-18 55 M19 34 L20 55" fill="none" stroke="#111111" stroke-width="8" stroke-linecap="round"/>
  <path class="palm hand-palm" d="M-31 -15 Q-29 -35 -7 -39 Q18 -40 31 -19 L29 17 Q22 38 0 41 Q-23 38 -30 19 Z" fill="#ffffff" stroke="#111111" stroke-width="8" stroke-linejoin="round"/>
  {fingers}
  <path class="thumb hand-thumb" d="M-27 8 Q-48 2 -52 21 Q-43 31 -24 23" fill="#ffffff" stroke="#111111" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
</g>""".format(
        id=hand_id,
        state=state,
        x=x,
        y=y,
        rotation=rotation,
        scale=scale,
        fingers="\n  ".join(finger(path, "finger-{0}".format(index + 1)) for index, path in enumerate(fingers)),
    )


def gathered_hand(hand_id: str, x: int, y: int, rotation: int = 0, scale: float = 1.0) -> str:
    fingers = (
        "M-22 -12 Q-15 -39 -3 -45",
        "M-8 -17 Q-4 -43 2 -47",
        "M6 -16 Q7 -42 6 -46",
        "M19 -11 Q17 -35 10 -43",
    )
    return """<g id="{id}" class="gathered-hand explicit-hand-anatomy fingers-gathered" data-handshape="gathered" data-state="end" transform="translate({x} {y}) rotate({rotation}) scale({scale})">
  <path class="wrist hand-wrist" d="M-20 35 L-19 55 M18 35 L20 55" fill="none" stroke="#111111" stroke-width="8" stroke-linecap="round"/>
  <path class="palm hand-palm" d="M-30 -13 Q-27 -34 -6 -38 Q19 -38 30 -16 L28 20 Q18 39 -2 40 Q-24 36 -30 18 Z" fill="#ffffff" stroke="#111111" stroke-width="8"/>
  {fingers}
  <path class="thumb hand-thumb" d="M-26 9 Q-41 5 -43 20 Q-35 30 -20 24" fill="none" stroke="#111111" stroke-width="8" stroke-linecap="round"/>
</g>""".format(id=hand_id, x=x, y=y, rotation=rotation, scale=scale, fingers="\n  ".join(finger(path, "finger-{0}".format(index + 1)) for index, path in enumerate(fingers)))


def fist_hand(hand_id: str, x: int, y: int, rotation: int = 0, scale: float = 1.0, handshape: str = "closed") -> str:
    if handshape == "dominant-closed-a":
        fingers = (
            "M-24 -10 Q-19 -23 -10 -24",
            "M-12 -17 Q-6 -29 3 -28",
            "M1 -17 Q8 -27 17 -21",
            "M15 -10 Q24 -17 29 -6",
        )
        thumb = "M-23 8 Q-8 13 4 2 L3 -27 Q4 -42 13 -44 Q21 -42 20 -27 L19 6"
    else:
        fingers = (
            "M-23 -15 Q-18 -29 -5 -27",
            "M-8 -20 Q-2 -33 10 -28",
            "M6 -18 Q13 -29 24 -21",
            "M16 -8 Q27 -16 31 -3",
        )
        thumb = "M-23 8 Q-2 22 23 8"
    return """<g id="{id}" class="fist-hand explicit-hand-anatomy {handshape}" data-handshape="{handshape}" data-state="closed" transform="translate({x} {y}) rotate({rotation}) scale({scale})">
  <path class="wrist hand-wrist" d="M-19 30 L-17 52 M19 30 L19 52" fill="none" stroke="#111111" stroke-width="8" stroke-linecap="round"/>
  <path class="palm hand-palm" d="M-31 -12 Q-29 -31 -8 -36 Q19 -37 32 -14 L30 17 Q18 36 -4 37 Q-26 33 -31 15 Z" fill="#ffffff" stroke="#111111" stroke-width="8"/>
  {fingers}
  <path class="thumb hand-thumb" d="{thumb}" fill="none" stroke="#111111" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
</g>""".format(id=hand_id, handshape=handshape, x=x, y=y, rotation=rotation, scale=scale, fingers="\n  ".join(finger(path, "finger-{0}".format(index + 1), 5.5) for index, path in enumerate(fingers)), thumb=thumb)


def water_hand(hand_id: str, x: int, y: int, rotation: int = 0, scale: float = 1.0) -> str:
    fingers = (
        "M-19 -15 L-34 -67",
        "M-4 -23 L-7 -78",
        "M11 -20 L20 -70",
        "M22 -8 Q34 -16 32 2",
    )
    return """<g id="{id}" class="water-hand explicit-hand-anatomy three-fingers-extended little-finger-folded" data-handshape="three-fingers-extended" transform="translate({x} {y}) rotate({rotation}) scale({scale})">
  <path class="wrist hand-wrist" d="M-19 34 L-17 56 M19 34 L20 56" fill="none" stroke="#111111" stroke-width="8" stroke-linecap="round"/>
  <path class="palm hand-palm" d="M-30 -12 Q-28 -34 -7 -39 Q19 -38 31 -16 L29 20 Q19 39 -2 40 Q-25 36 -30 17 Z" fill="#ffffff" stroke="#111111" stroke-width="8"/>
  {fingers}
  <path class="thumb hand-thumb folded-thumb" d="M-26 8 Q-10 18 7 7" fill="none" stroke="#111111" stroke-width="9" stroke-linecap="round"/>
</g>""".format(id=hand_id, x=x, y=y, rotation=rotation, scale=scale, fingers="\n  ".join(finger(path, "finger-{0}".format(index + 1)) for index, path in enumerate(fingers)))


def more_pose(state: str, variant: str) -> str:
    apart = state == "start"
    left_x, right_x = ((300, 420) if apart else (331, 389))
    if variant == "c":
        left_x -= 12
        right_x += 12
    parts = [
        '<g class="sign-specific-upper-limbs more-pose {0}" data-sign-id="more" data-hands="2" data-location="upper-chest" data-handshape="flat-o" data-independent-left-right-anatomy="true" data-phase="{0}" data-contact="{1}" data-repeat="true">'.format(state, "separate" if apart else "fingertips-meet"),
        arm_tube("more-left-limb", "M238 440 Q226 469 250 478", "M250 478 Q274 474 {0} 437".format(left_x - 43), (250, 478), "M{0} 429 L{1} 442".format(left_x - 47, left_x - 31)),
        arm_tube("more-right-limb", "M482 440 Q494 469 470 478", "M470 478 Q446 474 {0} 437".format(right_x + 43), (470, 478), "M{0} 429 L{1} 442".format(right_x + 47, right_x + 31)),
        flat_o_hand("more-left-flat-o", left_x, 435, "right", 0, .9),
        flat_o_hand("more-right-flat-o", right_x, 435, "left", 0, .9),
        arrow("M{0} 390 Q{1} 380 {2} 390".format(left_x - 10, left_x + 8, left_x + 28), "inward-left"),
        arrow("M{0} 390 Q{1} 380 {2} 390".format(right_x + 10, right_x - 8, right_x - 28), "inward-right"),
        '<text x="360" y="529" text-anchor="middle" class="mechanics-caption" font-family="Arial,sans-serif" font-size="18" fill="#333333">MEET · SEPARATE · REPEAT</text>',
        "</g>",
    ]
    return "\n".join(parts)


def help_pose(state: str, variant: str) -> str:
    rise = 0 if state == "start" else -58
    if variant == "c":
        rise -= 12
    return "\n".join((
        '<g class="sign-specific-upper-limbs help-pose {0} asymmetric supported" data-sign-id="help" data-hands="2" data-location="upper-chest" data-asymmetric-hands="true" data-contact="supported" data-direction="upward" data-phase="{0}">'.format(state),
        arm_tube("help-support-limb", "M238 440 Q228 478 270 487", "M270 487 Q307 486 333 {0}".format(463 + rise), (270, 487), "M322 {0} L340 {1}".format(466 + rise, 455 + rise)),
        arm_tube("help-dominant-limb", "M482 440 Q493 476 457 482", "M457 482 Q421 469 386 {0}".format(423 + rise), (457, 482), "M398 {0} L382 {1}".format(429 + rise, 416 + rise)),
        open_hand("help-supporting-open-palm", 354, 448 + rise, 88, .78, "supporting-open-palm"),
        fist_hand("help-dominant-closed-a", 359, 395 + rise, 0, .72, "dominant-closed-a"),
        arrow("M445 {0} L445 {1}".format(430 + rise, 348 + rise), "upward"),
        '<text x="360" y="535" text-anchor="middle" class="mechanics-caption" font-family="Arial,sans-serif" font-size="18" fill="#333333">SUPPORTED · MOVE UP</text>',
        "</g>",
    ))


def eat_pose(state: str, variant: str) -> str:
    contact = state != "start"
    x, y = ((475, 360) if not contact else (430, 315))
    if variant == "c":
        x += 18
        y += 8
    return "\n".join((
        '<g class="sign-specific-upper-limbs eat-pose reviewed-reference {0}" data-sign-id="eat" data-hands="1" data-location="mouth" data-handshape="flat-o" data-contact="one-reviewed-tap" data-reviewed-reference="true" data-phase="{0}">'.format(state),
        arm_tube("eat-dominant-limb", "M482 440 Q507 433 492 405", "M492 405 Q483 354 {0} {1}".format(x + 43, y + 3), (492, 405), "M{0} {1} L{2} {3}".format(x + 48, y - 7, x + 31, y + 8)),
        flat_o_hand("eat-flat-o", x, y, "left", -4, .82),
        arrow("M535 352 Q511 302 450 286", "toward-mouth"),
        '<circle class="contact-marker" cx="400" cy="310" r="6" fill="#efbd67" data-contact="mouth"/>',
        '<text x="360" y="535" text-anchor="middle" class="mechanics-caption" font-family="Arial,sans-serif" font-size="18" fill="#333333">ONE REVIEWED TAP · MOUTH</text>',
        "</g>",
    ))


def sleep_pose(state: str, variant: str) -> str:
    start = state == "start"
    x, y = ((480, 250) if start else (425, 365))
    if variant == "c":
        x += 15
    hand = open_hand("sleep-spread-hand", x, y, 8, .76, "start") if start else gathered_hand("sleep-gathered-hand", x, y, -12, .78)
    state_marker = "fingers-spread" if start else "fingers-gathered below-chin"
    return "\n".join((
        '<g class="sign-specific-upper-limbs sleep-pose {0} {1} clear-of-face" data-sign-id="sleep" data-hands="1" data-location="below-chin" data-states="start end" data-direction="downward" data-clear-of-face="true" data-phase="{0}">'.format(state, state_marker),
        arm_tube("sleep-dominant-limb", "M482 440 Q502 433 488 405", "M488 405 Q492 349 {0} {1}".format(x + 4, y + 46), (488, 405), "M{0} {1} L{2} {3}".format(x + 17, y + 50, x + 7, y + 31)),
        hand,
        arrow("M540 270 Q550 337 493 393", "downward"),
        '<text x="360" y="535" text-anchor="middle" class="mechanics-caption" font-family="Arial,sans-serif" font-size="18" fill="#333333">SPREAD · GATHER BELOW CHIN</text>',
        "</g>",
    ))


def milk_pose(state: str, variant: str) -> str:
    open_state = state == "start"
    x = 411 + (15 if variant == "c" else 0)
    hand = open_hand("milk-open-hand", x, 384, 0, .78, "open") if open_state else fist_hand("milk-closed-hand", x, 384, 0, .82, "closed")
    return "\n".join((
        '<g class="sign-specific-upper-limbs milk-pose {0} {1}" data-sign-id="milk" data-hands="1" data-location="upper-torso" data-states="open closed" data-action="squeeze release repeat" data-trajectory="in-place-no-up-down" data-phase="{0}">'.format(state, "open release" if open_state else "closed squeeze"),
        arm_tube("milk-dominant-limb", "M482 440 Q490 460 469 447", "M469 447 Q447 432 {0} 421".format(x + 8), (469, 447), "M{0} 427 L{1} 408".format(x + 18, x + 8)),
        hand,
        arrow("M354 350 Q375 334 393 348", "squeeze-inward-left"),
        arrow("M468 350 Q448 334 430 348", "squeeze-inward-right"),
        '<text x="360" y="535" text-anchor="middle" class="mechanics-caption" font-family="Arial,sans-serif" font-size="18" fill="#333333">OPEN · CLOSE · REPEAT IN PLACE</text>',
        "</g>",
    ))


def water_pose(state: str, variant: str) -> str:
    contact = state != "start"
    x, y = ((480, 365) if not contact else (445, 335))
    if variant == "c":
        x += 16
        y += 5
    return "\n".join((
        '<g class="sign-specific-upper-limbs water-pose three-fingers-extended {0}" data-sign-id="water" data-hands="1" data-location="lower-face" data-handshape="three-fingers-extended" data-source-identity="water" data-phase="{0}" data-contact="{1}">'.format(state, "lower-face" if contact else "approach"),
        arm_tube("water-dominant-limb", "M482 440 Q502 433 488 405", "M488 405 Q484 366 {0} {1}".format(x + 8, y + 42), (488, 405), "M{0} {1} L{2} {3}".format(x + 17, y + 46, x + 7, y + 29)),
        water_hand("water-three-finger-hand", x, y, -18, .76),
        arrow("M540 375 Q518 326 468 302", "toward-lower-face"),
        '<circle class="contact-marker" cx="411" cy="327" r="6" fill="#efbd67" data-contact="lower-face"/>',
        '<text x="360" y="535" text-anchor="middle" class="mechanics-caption" font-family="Arial,sans-serif" font-size="18" fill="#333333">THREE FINGERS · LOWER FACE</text>',
        "</g>",
    ))


POSE_BUILDERS = {
    "more": more_pose,
    "help": help_pose,
    "eat": eat_pose,
    "sleep": sleep_pose,
    "milk": milk_pose,
    "water": water_pose,
}


def svg_defs() -> str:
    return """<defs>
  <marker id="movement-arrowhead" markerWidth="20" markerHeight="20" refX="18" refY="10" orient="auto" markerUnits="userSpaceOnUse">
    <path d="M2 2 L18 10 L2 18 Z" fill="#ee7f72"/>
  </marker>
  <filter id="panel-shadow" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="0" dy="5" stdDeviation="8" flood-color="#18232d" flood-opacity=".10"/>
  </filter>
</defs>"""


def source_descriptor(record: Mapping[str, Any]) -> Dict[str, str]:
    return {
        "asset_id": str(record["asset_id"]),
        "path": str(record["path"]),
        "sha256": str(record["sha256"]),
    }


def metadata_for(sign_id: str, candidate: str, sources: Mapping[str, Any]) -> str:
    common = sources["common"]
    sign_sources = sources["signs"][sign_id]
    mechanics = [source_descriptor(sign_sources[key]) for key in ("functional", "video", "flashcard")]
    if "landmark_support" in sign_sources:
        mechanics.append(source_descriptor(sign_sources["landmark_support"]))
    payload = {
        "candidate": candidate,
        "character_base": source_descriptor(common["base"]),
        "style_grammar": [source_descriptor(common["hand_grammar"]), source_descriptor(common["arm_grammar"])],
        "supplementary_hand_configuration": [source_descriptor(common["hand_sheet_jpg"]), source_descriptor(common["hand_sheet_eps"])],
        "sign_id": sign_id,
        "sign_mechanics": mechanics,
        "status": "DRAFT_REQUIRES_HUMAN_REVIEW",
    }
    return "<metadata>{0}</metadata>".format(xml_json(payload))


def single_svg(sign_id: str, variant: str, bust_inner: str, sources: Mapping[str, Any]) -> str:
    spec = SIGN_SPECS[sign_id]
    state = "start" if variant == "c" else ("contact" if sign_id in {"more", "eat", "water"} else "end")
    pose = POSE_BUILDERS[sign_id](state, variant)
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="720" height="760" viewBox="0 0 720 760" role="img" aria-labelledby="title desc" data-sign-id="{sign_id}" data-candidate="{variant}" data-publication-status="DRAFT">
  <title id="title">{label} sign — candidate {candidate}</title>
  <desc id="desc">Source-grounded Open Peeps teaching illustration. Human sign review is required.</desc>
  {metadata}
  {defs}
  <rect width="720" height="760" rx="38" fill="#fffdf9"/>
  <path d="M36 92 Q172 26 332 62 T684 74" fill="none" stroke="#b9ded4" stroke-width="18" opacity=".55" aria-hidden="true"/>
  {safe}
  <text x="360" y="66" text-anchor="middle" font-family="Arial,sans-serif" font-size="28" font-weight="700" letter-spacing="3" fill="#16242c">{label} · {label_es}</text>
  {character}
  {occlusion}
  {pose}
  <g transform="translate(135 592)">
    <rect width="450" height="112" rx="24" fill="#ffffff" stroke="#16242c" stroke-width="3"/>
    <text x="225" y="38" text-anchor="middle" font-family="Arial,sans-serif" font-size="15" font-weight="700" letter-spacing="2" fill="#16242c">{location}</text>
    <text x="225" y="69" text-anchor="middle" font-family="Arial,sans-serif" font-size="17" fill="#40505a">{direction}</text>
    <text x="225" y="94" text-anchor="middle" font-family="Arial,sans-serif" font-size="13" fill="#6b7479">DRAFT · HUMAN REVIEW REQUIRED</text>
  </g>
</svg>
""".format(
        sign_id=sign_id,
        variant=variant,
        label=spec["labels"]["en"],
        label_es=spec["labels"]["es"],
        candidate=variant.upper(),
        metadata=metadata_for(sign_id, variant, sources),
        defs=svg_defs(),
        safe=safe_contract(720, 760),
        character=character_symbol(bust_inner),
        occlusion=neutral_arm_occlusion(sign_id),
        pose=pose,
        location=spec["location"].upper(),
        direction=spec["direction"],
    )


def sequence_svg(sign_id: str, bust_inner: str, sources: Mapping[str, Any]) -> str:
    spec = SIGN_SPECS[sign_id]
    start = POSE_BUILDERS[sign_id]("start", "b")
    end = POSE_BUILDERS[sign_id]("contact" if sign_id in {"more", "eat", "water"} else "end", "b")
    character = character_symbol(bust_inner)
    occlusion = neutral_arm_occlusion(sign_id)
    panel = '<rect x="0" y="0" width="720" height="760" rx="34" fill="#fffdf9" stroke="#d7dedf" stroke-width="3" filter="url(#panel-shadow)"/>'
    return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="680" viewBox="0 0 1200 680" role="img" aria-labelledby="title desc" data-sign-id="{sign_id}" data-candidate="b" data-publication-status="DRAFT">
  <title id="title">{label} sign — start and end candidate</title>
  <desc id="desc">Two source-grounded Open Peeps states show the sign movement. Human sign review is required.</desc>
  {metadata}
  {defs}
  <rect width="1200" height="680" rx="38" fill="#f7f5ef"/>
  {safe}
  <text x="600" y="48" text-anchor="middle" font-family="Arial,sans-serif" font-size="27" font-weight="700" letter-spacing="3" fill="#16242c">{label} · {label_es}</text>
  <g transform="translate(28 72) scale(.75)">
    {panel}
    <rect x="38" y="32" width="112" height="42" rx="21" fill="#b9ded4"/>
    <text x="94" y="59" text-anchor="middle" font-family="Arial,sans-serif" font-size="17" font-weight="700" fill="#16242c">START</text>
    {character}
    {occlusion}
    {start}
  </g>
  <g transform="translate(632 72) scale(.75)">
    {panel}
    <rect x="38" y="32" width="102" height="42" rx="21" fill="#efbd67"/>
    <text x="89" y="59" text-anchor="middle" font-family="Arial,sans-serif" font-size="17" font-weight="700" fill="#16242c">END</text>
    {character}
    {occlusion}
    {end}
  </g>
  <text x="600" y="654" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" letter-spacing="1.4" fill="#5c676d">{direction} · DRAFT · HUMAN REVIEW REQUIRED</text>
</svg>
""".format(
        sign_id=sign_id,
        label=spec["labels"]["en"],
        label_es=spec["labels"]["es"],
        metadata=metadata_for(sign_id, "b", sources),
        defs=svg_defs(),
        safe=safe_contract(1200, 680),
        panel=panel,
        character=character,
        occlusion=occlusion,
        start=start,
        end=end,
        direction=spec["direction"],
    )


CANDIDATE_COPY: Dict[str, Dict[str, Tuple[str, str, str]]] = {
    "more": {
        "a": ("Clear contact pose", "Both independently drawn flat-O hands are readable at the upper chest.", "Single-pose handshape readability"),
        "b": ("Meet and repeat sequence", "Start and contact panels make the inward meeting relationship explicit.", "Mechanics and movement readability"),
        "c": ("Wider movement alternate", "The wider start state gives the inward arrows more separation.", "Alternate movement emphasis"),
    },
    "help": {
        "a": ("Supported-hand pose", "The closed dominant hand and open supporting palm stay visibly asymmetric.", "Single-pose support relationship"),
        "b": ("Supported upward sequence", "Start and end panels show both hands rising together.", "Upward movement readability"),
        "c": ("Higher end alternate", "A higher supported pose tests the clearest final location.", "Alternate end-state emphasis"),
    },
    "eat": {
        "a": ("Mouth-contact pose", "The one-hand flat-O contact is clear without covering the face.", "Single-pose mouth location"),
        "b": ("Approach and contact sequence", "Two panels distinguish approach from one reviewed mouth contact.", "Start/contact explanation"),
        "c": ("Approach-focused alternate", "A wider start pose emphasizes the path toward the mouth.", "Alternate movement emphasis"),
    },
    "sleep": {
        "a": ("Gathered end pose", "The gathered fingers finish below the chin and clear of the face.", "Single-pose end-state readability"),
        "b": ("Spread-to-gather sequence", "Separate panels show the spread start and gathered end.", "Handshape change readability"),
        "c": ("Spread-start alternate", "The offset start keeps every spread finger away from facial contours.", "Alternate start-state emphasis"),
    },
    "milk": {
        "a": ("Closed squeeze pose", "The fist reads as the closed state with no vertical path.", "Single-pose closed state"),
        "b": ("Open and close sequence", "Two panels explain squeeze and release in place.", "Open/closed mechanics"),
        "c": ("Open-hand alternate", "The offset open state keeps all fingers readable.", "Alternate open-state emphasis"),
    },
    "water": {
        "a": ("Lower-face contact pose", "Three extended fingers remain legible at the reviewed lower-face location.", "Single-pose reference readability"),
        "b": ("Approach and contact sequence", "Two panels retain WATER identity through the short contact path.", "Reference-grounded movement"),
        "c": ("Three-finger alternate", "The wider approach makes the three-finger shape easy to inspect.", "Alternate handshape emphasis"),
    },
}


def candidate_id(sign_id: str, variant: str) -> Tuple[str, int]:
    if sign_id == "more":
        return (("more-c-v4", 4) if variant == "c" else ("more-{0}".format(variant), 4))
    if sign_id == "eat":
        return (("eat-c-v2", 2) if variant == "c" else ("eat-{0}".format(variant), 2))
    return (("{0}-c-v2".format(sign_id), 2) if variant == "c" else ("{0}-{1}".format(sign_id, variant), 1))


def build_svgs(sources: Mapping[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    bust_inner = inner_svg(sources["common"]["base"]["absolute_path"])
    results: Dict[str, List[Dict[str, Any]]] = {}
    for sign_id in SIGN_ORDER:
        records: List[Dict[str, Any]] = []
        for variant in ("a", "b", "c"):
            target = OUTPUT_ROOT / "{0}-{1}.svg".format(sign_id, variant)
            source = sequence_svg(sign_id, bust_inner, sources) if variant == "b" else single_svg(sign_id, variant, bust_inner, sources)
            target.write_text(source, encoding="utf-8")
            asset_id, version = candidate_id(sign_id, variant)
            title, note, recommended_for = CANDIDATE_COPY[sign_id][variant]
            records.append({
                "id": asset_id,
                "version": version,
                "label": "Candidate {0}".format(variant.upper()) if variant != "c" else "New candidate",
                "title": title,
                "asset": "assets/signs/{0}-{1}.svg".format(sign_id, variant),
                "content_hash": sha256(target),
                "review_note": note,
                "recommended_for": recommended_for,
                "recommended": variant == "b",
                "review_checks": list(SIGN_SPECS[sign_id]["checks"]),
            })
        results[sign_id] = records
    return results


def grounding_sources(sign_id: str) -> List[Dict[str, str]]:
    geometry_role = "Reference video, selected frames and landmarks support broad geometry"
    geometry_status = "Supporting evidence"
    if sign_id == "eat":
        geometry_role = "Reviewed reference route supports the critical near-face approach and contact window"
        geometry_status = "Usable with conditions"
    if sign_id == "water":
        geometry_role = "WATER video and committed WATER landmarks support broad geometry only"
        geometry_status = "Review required"
    return [
        {"priority": "1", "label": "Functional sign illustration", "role": "Primary mechanics source for the selected sign", "status": "Applied"},
        {"priority": "2", "label": "Curated sign knowledge", "role": "Mechanics and usage for human confirmation", "status": "Applied"},
        {"priority": "3", "label": "Reference geometry", "role": geometry_role, "status": geometry_status},
        {"priority": "4", "label": "Open Peeps visual grammar", "role": "Character identity and line grammar only; never sign mechanics", "status": "Applied"},
        {"priority": "5", "label": "Human review", "role": "Required before the draft is relied on or shared as approved sign content", "status": "Required"},
    ]


def package_for(sign_id: str, records: Sequence[Dict[str, Any]], sources: Mapping[str, Any]) -> Dict[str, Any]:
    spec = SIGN_SPECS[sign_id]
    sign_sources = sources["signs"][sign_id]
    package: Dict[str, Any] = {
        "sign_id": sign_id,
        "labels": spec["labels"],
        "usage": spec["usage"],
        "routine": spec["routine"],
        "routine_guidance": spec["routine_guidance"],
        "knowledge": {
            "hands_used": spec["hands"],
            "dominant_hand": spec["dominant"],
            "non_dominant_hand": spec["non_dominant"],
            "broad_handshape": spec["handshape"],
            "palm_orientation": spec["orientation"],
            "body_location": spec["location"],
            "movement": spec["movement"],
            "direction": spec["direction"],
            "repetition": spec["repetition"],
            "contact_relationship": spec["contact"],
            "expected_key_pose_count": 2,
            "variants": "Human review required",
            "source_conflict": "No unresolved conflict recorded; human sign review still required",
        },
        "movement": {
            "hands": spec["hands"],
            "body_location": spec["location"],
            "description": spec["movement"],
            "presentation": spec["presentation"],
            "technical_evidence": "Registered local references; technical evidence does not certify linguistic correctness",
            "evidence_quality": "Use sign-aware human review",
        },
        "visual_identity": {
            "base_system": "Open Peeps visual system",
            "operator_description": "KinderFlow character identity · calm monochrome linework",
            "mood": "Calm, editorial and friendly",
        },
        "source_hierarchy": [
            "FUNCTIONAL_SIGN_ILLUSTRATION",
            "CURATED_SIGN_KNOWLEDGE",
            "REFERENCE_VIDEO_FRAME_LANDMARKS",
            "OPEN_PEEPS_VISUAL_GRAMMAR",
            "HUMAN_REVIEW",
        ],
        "grounding_sources": grounding_sources(sign_id),
        "evidence_routes": {
            "pass": "LANDMARK_KEY_POSE",
            "review": spec["review"],
            "fallback": "KNOWLEDGE_REFERENCE_FALLBACK",
            "last_resort": "INTERNAL_POSE_GUIDE",
        },
        "candidates": [dict(records[0]), dict(records[1])],
        "regeneration_candidates": [dict(records[2])],
        "contextual_image": ({"asset": "assets/context/more-snack-time.png", "alt": "A toddler reaching for another berry during a calm snack routine", "scope": "Flashcard only"} if sign_id == "more" else None),
        "routine_icon": {"more": "snack", "help": "help", "eat": "mealtime", "sleep": "bedtime", "milk": "milk", "water": "water"}[sign_id],
        "review_status": "GROUNDED_FALLBACK_AVAILABLE" if sign_id == "eat" else "READY_FOR_HUMAN_REVIEW",
        "publication_status": "DRAFT",
        "composer": {
            "method": "DETERMINISTIC_OPEN_PEEPS_UPPER_LIMB_GRAMMAR",
            "base_character_asset_id": "open_peeps_bust_base",
            "style_grammar_asset_ids": ["open_peeps_pointing_finger_reference", "open_peeps_arm_reference"],
            "mechanics_asset_ids": [sign_sources["functional"]["asset_id"], sign_sources["video"]["asset_id"], sign_sources["flashcard"]["asset_id"], "functional_hand_sheet_jpg", "functional_hand_sheet_eps"],
            "anatomy_contract": ["shoulder", "upper arm", "elbow", "forearm", "wrist", "palm", "thumb", "four fingers"],
            "gesture_safe_contract": "Decorative accents stay outside the gesture-safe zone; movement arrows declare contour avoidance.",
        },
    }
    if sign_id == "eat":
        package["sign_aware_review"] = {
            "coverage_floor_percent": 65,
            "coverage_ceiling_percent": 80,
            "reason": "Hand-to-face occlusion makes the critical approach/contact window more important than overall hand coverage.",
        }
    if sign_id == "water":
        package["composer"]["landmark_support"] = sign_sources["landmark_support"]["path"]
        package["source_identity"] = {
            "sign_id": "water",
            "input_asset_id": "input_water",
            "functional_asset_id": "functional_water",
            "flashcard_asset_id": "flashcard_water_reference",
            "default_substitution": None,
        }
    return package


def write_package(outputs: Mapping[str, Sequence[Dict[str, Any]]], sources: Mapping[str, Any]) -> Dict[str, Any]:
    payload = {
        "schema_version": "2.1",
        "purpose": "Exact local retrieval packages for six source-grounded KinderFlow sign illustration sets.",
        "governance_note": "These deterministic records support visual preparation and human review. They do not certify linguistic correctness or publish content.",
        "signs": [package_for(sign_id, outputs[sign_id], sources) for sign_id in SIGN_ORDER],
    }
    PACKAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    PACKAGE_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def selected_component(role: str, record: Mapping[str, Any]) -> Dict[str, str]:
    return {
        "role": role,
        "asset_id": str(record["asset_id"]),
        "path": str(record["path"]),
        "sha256": str(record["sha256"]),
    }


def write_provenance(outputs: Mapping[str, Sequence[Dict[str, Any]]], sources: Mapping[str, Any]) -> Dict[str, Any]:
    common = sources["common"]
    derivatives = []
    for sign_id in SIGN_ORDER:
        for record in outputs[sign_id]:
            derivatives.append({
                "derivative_asset_id": record["id"],
                "sign_id": sign_id,
                "version": record["version"],
                "path": "prototype/{0}".format(record["asset"]),
                "sha256": record["content_hash"],
                "publication_status": "DRAFT",
            })
    sign_sources: Dict[str, List[Dict[str, str]]] = {}
    for sign_id in SIGN_ORDER:
        entries = [source_descriptor(sources["signs"][sign_id][key]) for key in ("functional", "video", "flashcard")]
        if sign_id == "water":
            entries.append(source_descriptor(sources["signs"][sign_id]["landmark_support"]))
        sign_sources[sign_id] = entries
    payload = {
        "schema_version": "3.0",
        "scope": "Six-sign KinderFlow Open Peeps upper-limb illustration grammar",
        "library_name": "Open Peeps",
        "creator": "Pablo Stanley / Pabs Stanley",
        "official_source_url": "https://www.openpeeps.com/",
        "licence": "CC0",
        "verification_basis": "Founder-verified official CC0 reference",
        "date_recorded": "2026-09-03",
        "source_hierarchy": [
            "FUNCTIONAL_SIGN_ILLUSTRATION",
            "CURATED_SIGN_KNOWLEDGE",
            "REFERENCE_VIDEO_FRAME_LANDMARKS",
            "OPEN_PEEPS_VISUAL_GRAMMAR",
            "HUMAN_REVIEW",
        ],
        "selected_components": [
            selected_component("base_character", common["base"]),
            selected_component("hand_finger_style_grammar", common["hand_grammar"]),
            selected_component("shoulder_arm_style_grammar", common["arm_grammar"]),
            {
                "role": "functional_pose_mechanics",
                "scope": "one registered source per canonical sign",
                "asset_ids": [sources["signs"][sign_id]["functional"]["asset_id"] for sign_id in SIGN_ORDER],
                "paths": [sources["signs"][sign_id]["functional"]["path"] for sign_id in SIGN_ORDER],
            },
            selected_component("supplementary_hand_configuration", common["hand_sheet_jpg"]),
            {
                "role": "movement_reference",
                "scope": "one registered source per canonical sign",
                "asset_ids": [sources["signs"][sign_id]["video"]["asset_id"] for sign_id in SIGN_ORDER],
                "paths": [sources["signs"][sign_id]["video"]["path"] for sign_id in SIGN_ORDER],
            },
            dict(selected_component("landmark_support", sources["signs"]["water"]["landmark_support"]), sign_id="water"),
        ],
        "supplementary_configuration_sources": [source_descriptor(common["hand_sheet_jpg"]), source_descriptor(common["hand_sheet_eps"])],
        "sign_sources": sign_sources,
        "derivatives": derivatives,
        "composition": "Exact bust.svg inner geometry is embedded as the sole character base. Reusable KinderFlow layers add sign-specific shoulder-to-finger anatomy; the two Open Peeps pose files supply line grammar only.",
        "mechanics": "Each sign uses its own registered functional image, reference video and flashcard. WATER diagnostics are recorded only under WATER and are not MORE evidence.",
        "colour_treatment": "Monochrome character with coral, mint and muted ochre restricted to peripheral and motion accents outside the gesture zone.",
        "voluntary_credit": "Character foundation: Open Peeps by Pablo Stanley.",
        "review_status": "READY_FOR_HUMAN_REVIEW",
        "publication_status": "DRAFT",
    }
    PROVENANCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROVENANCE_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def write_contact_sheet(outputs: Mapping[str, Sequence[Dict[str, Any]]], sources: Mapping[str, Any]) -> None:
    cards = []
    for sign_id in SIGN_ORDER:
        for variant, record in zip(("a", "b", "c"), outputs[sign_id]):
            cards.append("""<article><h2>{label} — {variant}</h2><img src="../../prototype/{asset}" alt="{label} candidate {variant}"><p>{title}</p><code>{hash}</code></article>""".format(
                label=SIGN_SPECS[sign_id]["labels"]["en"], variant=variant.upper(), asset=record["asset"], title=html.escape(record["title"]), hash=record["content_hash"][:16]))
    source_cards = []
    for label, source_key in (
        ("Exact character base", "base"),
        ("Hand and finger grammar", "hand_grammar"),
        ("Shoulder and arm grammar", "arm_grammar"),
    ):
        record = sources["common"][source_key]
        source_cards.append(
            """<article><h2>{label}</h2><img src="../../{path}" alt="{label} source example"><p>{asset_id}</p><code>{hash}</code></article>""".format(
                label=label,
                path=html.escape(record["path"], quote=True),
                asset_id=record["asset_id"],
                hash=record["sha256"][:16],
            )
        )
    document = """<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>KinderFlow sign visual QA contact sheet</title>
<style>body{{margin:0;padding:32px;font:15px/1.4 system-ui;background:#eef2ef;color:#17232b}}header{{max-width:960px;margin:auto auto 28px}}main,.source-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:24px}}.source-review{{margin:0 0 42px}}article{{background:white;border-radius:18px;padding:18px;box-shadow:0 8px 28px #18303a18}}h2{{font-size:18px}}img{{display:block;width:100%;aspect-ratio:1/1;object-fit:contain;background:#faf9f5;border-radius:12px}}code{{font-size:11px;color:#68747a}}</style>
<header><h1>KinderFlow visual sign QA</h1><p>18 deterministic DRAFT candidates. Exact Open Peeps bust is the sole base; pointing-finger and peep-4 sources provide line grammar only. Human sign review is required.</p></header>
<section class="source-review" aria-labelledby="source-review-title"><h2 id="source-review-title">Registered Open Peeps source examples</h2><p>These are visual-grammar references, not sign-mechanics sources.</p><div class="source-grid">{source_cards}</div></section>
<main>{cards}</main></html>
""".format(source_cards="\n".join(source_cards), cards="\n".join(cards))
    CONTACT_SHEET_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONTACT_SHEET_PATH.write_text(document, encoding="utf-8")


def main() -> int:
    sources = load_sources()
    outputs = build_svgs(sources)
    write_package(outputs, sources)
    write_provenance(outputs, sources)
    write_contact_sheet(outputs, sources)
    print("Built {0} sign SVGs for {1} canonical signs.".format(sum(len(records) for records in outputs.values()), len(outputs)))
    print(PACKAGE_PATH.relative_to(REPO_ROOT))
    print(PROVENANCE_PATH.relative_to(REPO_ROOT))
    print(CONTACT_SHEET_PATH.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
