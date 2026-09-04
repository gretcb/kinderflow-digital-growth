from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import urlsplit


REPO_ROOT = Path(__file__).resolve().parents[2]
PROTOTYPE_ROOT = REPO_ROOT / "prototype"
PACKAGE_PATH = PROTOTYPE_ROOT / "data/visual_sign_packages.json"
REGISTRY_PATH = REPO_ROOT / "assets/registry/sign_asset_registry.json"
PROVENANCE_PATH = REPO_ROOT / "assets/flashcards/open_peeps/provenance.json"

AUDITED_ROUTES = (
    "index.html",
    "kinder-signs.html",
    "admin.html",
    "content-studio.html",
    "create-sign.html",
    "library.html",
    "flashcards.html",
    "print-card.html",
    "create-story.html",
    "create-song.html",
    "school.html",
    "family.html",
)

ADMIN_ROUTES = {
    "admin.html",
    "content-studio.html",
    "create-sign.html",
    "library.html",
    "flashcards.html",
    "create-story.html",
    "create-song.html",
}

RAW_STATE_TERMS = (
    "MOTION_REPRESENTATION_FAIL",
    "KNOWLEDGE_REFERENCE_FALLBACK",
    "LANDMARK_KEY_POSE",
    "run_id",
    "schema_version",
    "DRY_RUN",
    "NOT_APPLICABLE",
    "LLM_ASSISTED",
)

PRIMARY_JARGON = RAW_STATE_TERMS + (
    "MediaPipe",
    "landmark extraction",
    "landmark preview",
    "dominant-hand coverage",
    "grounded fallback",
    "visual package",
    "generate candidate",
    "internal printable",
    "provenance",
    "deterministic quality gate",
    "LangSmith",
    "n8n",
    "Open Peeps",
    "Miroodles",
    "candidate",
    "candidates",
    "CV",
    "LLM",
)

SCHOOL_FAMILY_JARGON = (
    "MediaPipe",
    "landmark",
    "JSON",
    "schema",
    "model ID",
    "provenance",
    "entitlement",
    "LLM",
    "LangSmith",
    "n8n",
)

EXPECTED_HANDS = {
    "more": 2,
    "help": 2,
    "eat": 1,
    "sleep": 1,
    "milk": 1,
}


def term_pattern(term: str) -> re.Pattern[str]:
    return re.compile(r"(?<![A-Za-z0-9_]){0}(?![A-Za-z0-9_])".format(re.escape(term)), re.IGNORECASE)


class SurfaceParser(HTMLParser):
    """Collect the small set of static HTML semantics required by the UX audit."""

    def __init__(self) -> None:
        super().__init__()
        self.ids: List[str] = []
        self.labels_for: Set[str] = set()
        self.controls: List[Tuple[str, Dict[str, Optional[str]], bool]] = []
        self.references: List[Tuple[str, str, str]] = []
        self.headings: List[Tuple[str, str]] = []
        self.images: List[Dict[str, Optional[str]]] = []
        self.primary_text: List[str] = []
        self.details: List[Dict[str, List[str]]] = []
        self._details_stack: List[Dict[str, List[str]]] = []
        self._label_depth = 0
        self._summary_depth = 0
        self._hidden_text_depth = 0
        self._heading_tag: Optional[str] = None
        self._heading_text: List[str] = []

    def handle_starttag(
        self, tag: str, attrs: List[Tuple[str, Optional[str]]]
    ) -> None:
        attributes = dict(attrs)
        if tag in {"script", "style", "template"}:
            self._hidden_text_depth += 1
        if tag == "details":
            detail = {"summary": [], "text": []}
            self.details.append(detail)
            self._details_stack.append(detail)
        if tag == "summary" and self._details_stack:
            self._summary_depth += 1
        if tag == "label":
            self._label_depth += 1
            if attributes.get("for"):
                self.labels_for.add(str(attributes["for"]))
        element_id = attributes.get("id")
        if element_id:
            self.ids.append(str(element_id))
        if tag in {"input", "select", "textarea"}:
            self.controls.append((tag, attributes, self._label_depth > 0))
        if tag == "img":
            self.images.append(attributes)
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._heading_tag = tag
            self._heading_text = []
        for attribute_name in ("href", "src"):
            value = attributes.get(attribute_name)
            if value:
                self.references.append((tag, attribute_name, str(value)))

    def handle_startendtag(
        self, tag: str, attrs: List[Tuple[str, Optional[str]]]
    ) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag == self._heading_tag:
            self.headings.append((tag, " ".join(self._heading_text).strip()))
            self._heading_tag = None
            self._heading_text = []
        if tag == "label":
            self._label_depth = max(0, self._label_depth - 1)
        if tag == "summary" and self._details_stack:
            self._summary_depth = max(0, self._summary_depth - 1)
        if tag == "details" and self._details_stack:
            self._details_stack.pop()
        if tag in {"script", "style", "template"}:
            self._hidden_text_depth = max(0, self._hidden_text_depth - 1)

    def handle_data(self, data: str) -> None:
        if self._hidden_text_depth:
            return
        cleaned = " ".join(data.split())
        if not cleaned:
            return
        if self._heading_tag:
            self._heading_text.append(cleaned)
        if self._details_stack:
            self._details_stack[-1]["text"].append(cleaned)
            if self._summary_depth:
                self._details_stack[-1]["summary"].append(cleaned)
        else:
            self.primary_text.append(cleaned)


def parse_surface(path: Path) -> SurfaceParser:
    parser = SurfaceParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser


def class_tokens(root: ET.Element) -> Set[str]:
    tokens: Set[str] = set()
    for element in root.iter():
        tokens.update((element.attrib.get("class") or "").split())
    return tokens


def elements_with_class(root: ET.Element, class_name: str) -> List[ET.Element]:
    return [
        element
        for element in root.iter()
        if class_name in (element.attrib.get("class") or "").split()
    ]


def elements_with_semantic_class(root: ET.Element, marker: str) -> List[ET.Element]:
    return [
        element
        for element in root.iter()
        if any(marker in token for token in (element.attrib.get("class") or "").split())
    ]


class Prompt2BVisualAcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(PACKAGE_PATH.read_text(encoding="utf-8"))
        cls.packages = {item["sign_id"]: item for item in cls.payload["signs"]}
        cls.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    @staticmethod
    def candidates(package: dict) -> List[dict]:
        return package.get("candidates", []) + package.get("regeneration_candidates", [])

    def svg_records(self, sign_id: str) -> List[Tuple[dict, Path, str, ET.Element]]:
        records = []
        for candidate in self.candidates(self.packages[sign_id]):
            path = PROTOTYPE_ROOT / candidate["asset"]
            source = path.read_text(encoding="utf-8")
            records.append((candidate, path, source, ET.fromstring(source)))
        return records

    def combined_svg(self, sign_id: str) -> str:
        if sign_id not in self.packages:
            self.fail("missing visual package for {0}".format(sign_id))
        return "\n".join(record[2] for record in self.svg_records(sign_id)).lower()

    def test_all_six_signs_have_ready_source_grounded_visual_packages(self) -> None:
        expected = {"more", "help", "eat", "sleep", "milk", "water"}
        self.assertEqual(set(self.packages), expected)
        for sign_id in expected:
            package = self.packages[sign_id]
            self.assertGreaterEqual(len(package.get("candidates", [])), 2, sign_id)
            self.assertGreaterEqual(len(package.get("regeneration_candidates", [])), 1, sign_id)
            self.assertEqual(package["publication_status"], "DRAFT", sign_id)
            self.assertNotIn("APPROVED", package["review_status"], sign_id)
        self.assertEqual(self.packages["water"]["review_status"], "READY_FOR_HUMAN_REVIEW")

    def test_bust_is_the_only_base_and_both_open_peeps_grammar_sources_are_recorded(self) -> None:
        provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))
        expected_hierarchy = [
            "FUNCTIONAL_SIGN_ILLUSTRATION",
            "CURATED_SIGN_KNOWLEDGE",
            "REFERENCE_VIDEO_FRAME_LANDMARKS",
            "OPEN_PEEPS_VISUAL_GRAMMAR",
            "HUMAN_REVIEW",
        ]
        self.assertEqual(provenance["source_hierarchy"], expected_hierarchy)
        components = provenance.get("selected_components", [])
        component_text = json.dumps(components, ensure_ascii=False)
        self.assertIn("/Separate Atoms/a person/bust.svg", component_text)
        self.assertIn("/pose/standing/pointing_finger-1.svg", component_text)
        self.assertIn("/Templates/Bust/peep-4.svg", component_text)
        self.assertNotIn("mid-2.svg", component_text)

        for sign_id in self.packages:
            for candidate, path, source, _root in self.svg_records(sign_id):
                with self.subTest(sign_id=sign_id, candidate=candidate["id"]):
                    self.assertTrue("bust.svg" in source, path)
                    self.assertTrue("pointing_finger-1.svg" in source, path)
                    self.assertTrue("peep-4.svg" in source, path)
                    self.assertTrue("mid-2.svg" not in source, path)
                    self.assertTrue("open-peeps-bust" in source, path)
                    self.assertNotRegex(source, r"<use[^>]+(?:peep-4|pointing_finger)")
                    self.assertTrue(path.is_file())

    def test_composer_replaces_neutral_arms_with_split_integrated_limbs(self) -> None:
        for sign_id in self.packages:
            expected_masks = 2 if sign_id in {"more", "help"} else 1
            self.assertEqual(self.packages[sign_id]["source_hierarchy"], [
                "FUNCTIONAL_SIGN_ILLUSTRATION",
                "CURATED_SIGN_KNOWLEDGE",
                "REFERENCE_VIDEO_FRAME_LANDMARKS",
                "OPEN_PEEPS_VISUAL_GRAMMAR",
                "HUMAN_REVIEW",
            ])
            for candidate, _path, _source, root in self.svg_records(sign_id):
                with self.subTest(sign_id=sign_id, candidate=candidate["id"]):
                    masks = elements_with_class(root, "neutral-arm-mask")
                    panel_count = 2 if candidate["asset"].endswith("-b.svg") else 1
                    self.assertEqual(len(masks), expected_masks * panel_count)
                    limbs = elements_with_class(root, "complete-upper-limb")
                    self.assertTrue(limbs)
                    for limb in limbs:
                        upper = elements_with_class(limb, "upper-arm-outline")
                        forearm = elements_with_class(limb, "forearm-outline")
                        self.assertEqual(len(upper), 1)
                        self.assertEqual(len(forearm), 1)
                        self.assertNotEqual(upper[0].attrib.get("d"), forearm[0].attrib.get("d"))

    def test_movement_arrows_use_fixed_size_heads_and_flat_o_digits_stay_separated(self) -> None:
        for sign_id in self.packages:
            for candidate, _path, source, root in self.svg_records(sign_id):
                with self.subTest(sign_id=sign_id, candidate=candidate["id"]):
                    self.assertIn('markerUnits="userSpaceOnUse"', source)
                    self.assertNotIn('markerUnits="strokeWidth"', source)
                    for hand in elements_with_class(root, "flat-o-hand"):
                        self.assertEqual(hand.attrib.get("data-profile"), "horizontal-side")
                        digits = elements_with_class(hand, "finger-path")
                        self.assertEqual(len(digits), 4)
                        for digit in digits:
                            self.assertLessEqual(float(digit.attrib["stroke-width"]), 3.5)

    def test_every_candidate_has_verified_distinct_identity_path_and_hash(self) -> None:
        all_assets: Dict[str, str] = {}
        for sign_id, package in self.packages.items():
            records = self.candidates(package)
            identities = {(item["id"], item["asset"], item["content_hash"]) for item in records}
            self.assertEqual(len(identities), len(records), sign_id)
            initial_ids = {item["id"] for item in package["candidates"]}
            initial_paths = {item["asset"] for item in package["candidates"]}
            initial_hashes = {item["content_hash"] for item in package["candidates"]}
            for candidate in package["regeneration_candidates"]:
                self.assertNotIn(candidate["id"], initial_ids)
                self.assertNotIn(candidate["asset"], initial_paths)
                self.assertNotIn(candidate["content_hash"], initial_hashes)
            for candidate, path, _source, _root in self.svg_records(sign_id):
                actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
                self.assertEqual(candidate["content_hash"], actual_hash, candidate["id"])
                self.assertNotIn(candidate["asset"], all_assets, candidate["asset"])
                all_assets[candidate["asset"]] = sign_id

    def test_every_svg_is_valid_and_has_complete_arm_wrist_palm_thumb_finger_anatomy(self) -> None:
        forbidden_primitives = (
            "generic-hand",
            "hand-blob",
            "blob-hand",
            "mitten-hand",
            "pincher-hand",
            "clamp-hand",
            "floating-hand",
        )
        required_exact_tokens = {
            "complete-upper-limb",
            "shoulder-arm",
            "upper-arm",
            "elbow",
            "forearm",
            "wrist",
            "finger-path",
        }
        for sign_id in self.packages:
            for candidate, _path, source, root in self.svg_records(sign_id):
                with self.subTest(sign_id=sign_id, candidate=candidate["id"]):
                    tokens = class_tokens(root)
                    self.assertTrue(
                        required_exact_tokens.issubset(tokens),
                        required_exact_tokens - tokens,
                    )
                    self.assertTrue(any("palm" in token for token in tokens), "missing palm marker")
                    self.assertTrue(any("thumb" in token for token in tokens), "missing thumb marker")
                    data_hand_counts = {
                        element.attrib["data-hands"]
                        for element in root.iter()
                        if "data-hands" in element.attrib
                    }
                    self.assertTrue(data_hand_counts, "missing data-hands")
                    if sign_id in EXPECTED_HANDS:
                        expected_hands = EXPECTED_HANDS[sign_id]
                        self.assertIn(str(expected_hands), data_hand_counts)
                    else:
                        expected_hands = min(int(value) for value in data_hand_counts)
                        self.assertGreaterEqual(expected_hands, 1)
                    self.assertGreaterEqual(len(elements_with_class(root, "complete-upper-limb")), expected_hands)
                    self.assertGreaterEqual(len(elements_with_semantic_class(root, "palm")), expected_hands)
                    self.assertGreaterEqual(len(elements_with_semantic_class(root, "thumb")), expected_hands)
                    visible_fingers = [
                        element
                        for element in elements_with_class(root, "finger-path")
                        if not any(
                            "thumb" in token
                            for token in (element.attrib.get("class") or "").split()
                        )
                    ]
                    self.assertGreaterEqual(len(visible_fingers), expected_hands * 4)
                    lowered = source.lower()
                    for forbidden in forbidden_primitives:
                        self.assertNotIn(forbidden, lowered)

    def test_accents_and_arrows_declare_the_gesture_safe_contract(self) -> None:
        for sign_id in self.packages:
            for candidate, _path, source, root in self.svg_records(sign_id):
                with self.subTest(sign_id=sign_id, candidate=candidate["id"]):
                    self.assertTrue("gesture-safe-zone" in source, "missing gesture-safe-zone marker")
                    safe_zones = [
                        element for element in root.iter()
                        if element.attrib.get("data-gesture-safe-zone") == "true"
                    ]
                    self.assertTrue(safe_zones, "missing machine-checkable gesture-safe zone")
                    accents = elements_with_class(root, "peripheral-accent")
                    for accent in accents:
                        self.assertEqual(accent.attrib.get("data-outside-gesture-safe-zone"), "true")
                        self.assertEqual(accent.attrib.get("aria-hidden"), "true")
                    arrows = elements_with_class(root, "movement-arrow")
                    self.assertTrue(arrows, "missing movement cue")
                    for arrow in arrows:
                        self.assertEqual(arrow.attrib.get("data-avoids-hand-contours"), "true")

    def test_more_has_two_flat_o_hands_and_start_contact_repeat_semantics(self) -> None:
        source = self.combined_svg("more")
        for marker in ("flat-o", "upper-chest", "start", "contact", "repeat"):
            self.assertTrue(marker in source, "MORE is missing semantic marker: " + marker)
        self.assertNotIn("old-more-hand-primitive", source)

    def test_help_uses_two_asymmetric_supported_hands_moving_upward(self) -> None:
        source = self.combined_svg("help")
        for marker in (
            "asymmetric",
            "dominant-closed-a",
            "supporting-open-palm",
            "supported",
            "upward",
        ):
            self.assertTrue(marker in source, "HELP is missing semantic marker: " + marker)

    def test_eat_uses_one_flat_o_hand_and_reviewed_reference_fallback(self) -> None:
        package = self.packages["eat"]
        source = self.combined_svg("eat")
        self.assertEqual(package["evidence_routes"]["review"], "KNOWLEDGE_REFERENCE_FALLBACK")
        self.assertIn("one tap", package["knowledge"]["repetition"].lower())
        for marker in ("flat-o", "mouth", "reviewed-reference"):
            self.assertTrue(marker in source, "EAT is missing semantic marker: " + marker)

    def test_sleep_has_separate_spread_and_gathered_states_clear_of_the_face(self) -> None:
        source = self.combined_svg("sleep")
        for marker in (
            "start",
            "end",
            "fingers-spread",
            "fingers-gathered",
            "downward",
            "below-chin",
            "clear-of-face",
        ):
            self.assertTrue(marker in source, "SLEEP is missing semantic marker: " + marker)

    def test_milk_has_repeated_open_close_squeeze_release_without_vertical_trajectory(self) -> None:
        source = self.combined_svg("milk")
        for marker in ("open", "closed", "squeeze", "release", "repeat"):
            self.assertTrue(marker in source, "MILK is missing semantic marker: " + marker)
        self.assertNotIn("vertical-milking", source)

    def test_water_and_unknown_signs_never_resolve_to_more(self) -> None:
        water = self.packages["water"]
        self.assertEqual(water["review_status"], "READY_FOR_HUMAN_REVIEW")
        for candidate in self.candidates(water):
            self.assertTrue(candidate["id"].startswith("water"), candidate["id"])
            self.assertNotIn("more", candidate["asset"].lower())

        script = (PROTOTYPE_ROOT / "create-sign.js").read_text(encoding="utf-8")
        self.assertTrue(
            "This sign is not available in the current demo set." in script,
            "missing controlled unsupported-sign recovery copy",
        )
        self.assertNotRegex(script, r"(?:visualPackages|packages)\s*\[\s*0\s*\]")
        self.assertNotRegex(script, r"(?:activePackage|signPackage)\s*\|\|\s*[^;\n]*more")

    def test_local_visual_approval_remains_draft_and_never_publishes(self) -> None:
        script = (PROTOTYPE_ROOT / "create-sign.js").read_text(encoding="utf-8")
        self.assertIn('visual_review_status: "APPROVED_FOR_INTERNAL_PRINTABLE"', script)
        self.assertIn('publication_status: "DRAFT"', script)
        self.assertNotIn('publication_status: "PUBLISHED"', script)
        for package in self.packages.values():
            self.assertEqual(package["publication_status"], "DRAFT")

    def test_visual_composer_has_no_paid_or_network_generation_client(self) -> None:
        generator = (REPO_ROOT / "tools/build_sign_vectors.py").read_text(encoding="utf-8")
        for forbidden in (
            "import requests",
            "import httpx",
            "urllib.request",
            "from openai",
            "import openai",
            "image_gen",
            "replicate.com",
            "api.openai.com",
        ):
            self.assertNotIn(forbidden, generator.lower())
        browser = (PROTOTYPE_ROOT / "create-sign.js").read_text(encoding="utf-8")
        self.assertNotRegex(browser, r"fetch\(\s*[\"']https?://")


class Prompt2BPlainLanguageAcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.paths = {name: PROTOTYPE_ROOT / name for name in AUDITED_ROUTES}
        cls.parsers = {name: parse_surface(path) for name, path in cls.paths.items()}

    def test_all_audited_routes_have_one_clear_h1_and_main_landmark(self) -> None:
        for name, path in self.paths.items():
            source = path.read_text(encoding="utf-8")
            h1s = [heading for heading in self.parsers[name].headings if heading[0] == "h1"]
            with self.subTest(route=name):
                self.assertEqual(len(h1s), 1)
                self.assertIn("<main", source)
                levels = [int(tag[1]) for tag, _text in self.parsers[name].headings]
                jumps = [
                    (before, after)
                    for before, after in zip(levels, levels[1:])
                    if after > before + 1
                ]
                self.assertFalse(jumps, "heading levels skipped: {0}".format(jumps))

    def test_primary_surfaces_hide_raw_states_and_internal_jargon(self) -> None:
        for name, parser in self.parsers.items():
            primary = " ".join(parser.primary_text)
            for term in PRIMARY_JARGON:
                with self.subTest(route=name, term=term):
                    if term == "MediaPipe" and name in {"kinder-signs.html", "create-sign.html", "flashcards.html"}:
                        continue
                    self.assertNotRegex(primary, term_pattern(term))

            for detail in parser.details:
                detail_text = " ".join(detail["text"])
                leaked_terms = [term for term in PRIMARY_JARGON if term_pattern(term).search(detail_text)]
                if not leaked_terms:
                    continue
                summary = " ".join(detail["summary"])
                self.assertIn(name, ADMIN_ROUTES, (name, leaked_terms))
                self.assertRegex(summary, re.compile(r"technical|source|implementation", re.IGNORECASE))

    def test_school_and_family_never_expose_implementation_language(self) -> None:
        for name in ("school.html", "family.html"):
            parser = self.parsers[name]
            all_visible = " ".join(
                parser.primary_text
                + [item for detail in parser.details for item in detail["text"]]
            )
            for term in SCHOOL_FAMILY_JARGON:
                with self.subTest(route=name, term=term):
                    self.assertNotRegex(all_visible, term_pattern(term))

    def test_create_sign_uses_the_plain_language_operator_journey(self) -> None:
        source = "\n".join(
            (
                (PROTOTYPE_ROOT / "create-sign.html").read_text(encoding="utf-8"),
                (PROTOTYPE_ROOT / "create-sign.js").read_text(encoding="utf-8"),
            )
        )
        for phrase in (
            "Choose the sign",
            "Add the reference",
            "Review the sign reference",
            "Choose the clearest poses",
            "Create family materials",
            "Create visual options",
            "Choose the clearest visual",
            "Approve selected visual",
            "Supporting family materials",
            "Use reviewed references",
            "Create another visual option",
        ):
            self.assertIn(phrase, source)
        self.assertIn("Next product milestone", source)
        self.assertIn("reviewed MediaPipe hand and pose landmarks", source)
        self.assertNotIn("Add to library / use later", source)
        self.assertNotIn('title: "Landmark key poses"', source)
        self.assertNotIn('title: "Grounded fallback"', source)

    def test_flashcard_recovery_uses_sign_visual_language(self) -> None:
        source = "\n".join(
            (
                (PROTOTYPE_ROOT / "flashcards.html").read_text(encoding="utf-8"),
                (PROTOTYPE_ROOT / "flashcards.js").read_text(encoding="utf-8"),
            )
        )
        self.assertTrue(
            "Approve a sign visual before creating printable materials" in source,
            "missing plain-language flashcard blocked-state explanation",
        )
        self.assertTrue(
            "Back to visual options" in source,
            "missing plain-language flashcard recovery action",
        )
        self.assertNotIn("grounded visual package", source.lower())

    def test_content_library_uses_friendly_generation_and_check_labels(self) -> None:
        source = (PROTOTYPE_ROOT / "library.html").read_text(encoding="utf-8")
        self.assertIn("AI-assisted draft", source)
        self.assertIn("Approved source copy", source)
        self.assertIn("Quality checks", source)
        self.assertNotIn("LLM_ASSISTED", source)
        self.assertNotRegex(source, r">\s*HUMAN\s*(?:·|<)")

    def test_every_route_has_unique_ids_labelled_controls_and_valid_local_links(self) -> None:
        absolute_parsers = {path.resolve(): self.parsers[name] for name, path in self.paths.items()}
        for name, path in self.paths.items():
            parser = self.parsers[name]
            with self.subTest(route=name):
                self.assertEqual(len(parser.ids), len(set(parser.ids)), "duplicate id")
                for label_target in parser.labels_for:
                    self.assertIn(label_target, parser.ids, "label points to missing id")
                for tag, attrs, wrapped in parser.controls:
                    if tag == "input" and str(attrs.get("type") or "text").lower() == "hidden":
                        continue
                    element_id = attrs.get("id")
                    labelled = (
                        wrapped
                        or bool(attrs.get("aria-label"))
                        or bool(attrs.get("aria-labelledby"))
                        or bool(element_id and element_id in parser.labels_for)
                    )
                    self.assertTrue(labelled, "unlabelled {0}#{1}".format(tag, element_id))
                    for label_id in str(attrs.get("aria-labelledby") or "").split():
                        self.assertIn(label_id, parser.ids, "aria-labelledby points to missing id")
                for image in parser.images:
                    self.assertIn("alt", image, "image is missing alt text")
                for _tag, attribute, value in parser.references:
                    parsed = urlsplit(value)
                    if parsed.scheme or value.startswith("//") or value.startswith("data:"):
                        continue
                    target = (path.parent / parsed.path).resolve() if parsed.path else path.resolve()
                    if parsed.path:
                        self.assertTrue(target.is_file(), "broken {0}={1}".format(attribute, value))
                    if parsed.fragment and target in absolute_parsers:
                        self.assertIn(parsed.fragment, absolute_parsers[target].ids, "missing fragment " + value)

    def test_accessibility_and_responsive_basics_remain_present(self) -> None:
        css = (PROTOTYPE_ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn(":focus-visible", css)
        self.assertIn("prefers-reduced-motion: reduce", css)
        self.assertRegex(css, r"min-height\s*:\s*44px")
        self.assertRegex(css, r"@media\s*\(max-width:\s*(?:760|768)px\)")
        create_sign = (PROTOTYPE_ROOT / "create-sign.html").read_text(encoding="utf-8")
        self.assertIn('aria-live="polite"', create_sign)
        self.assertIn('type="radio"', create_sign)

    @unittest.skipUnless(shutil.which("node"), "Node is unavailable")
    def test_all_prototype_javascript_has_valid_syntax(self) -> None:
        scripts = sorted(PROTOTYPE_ROOT.glob("*.js"))
        self.assertTrue(scripts)
        for script in scripts:
            with self.subTest(script=script.name):
                result = subprocess.run(
                    [shutil.which("node") or "node", "--check", str(script)],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_story_has_english_spanish_output_and_language_change_resets_review(self) -> None:
        html = (PROTOTYPE_ROOT / "create-story.html").read_text(encoding="utf-8")
        script = (PROTOTYPE_ROOT / "story.js").read_text(encoding="utf-8")
        selector = re.search(
            r"<select\b[^>]*id=[\"']story-language[\"'][^>]*>(.*?)</select>",
            html,
            re.IGNORECASE | re.DOTALL,
        )
        self.assertIsNotNone(selector)
        selector_source = selector.group(1) if selector else ""
        self.assertRegex(selector_source, r"value=[\"']en[\"'][^>]*>\s*English")
        self.assertRegex(selector_source, r"value=[\"']es[\"'][^>]*>\s*Spanish")
        self.assertIn("Story language", html)

        self.assertRegex(script, re.compile(r"\ben\s*:", re.MULTILINE))
        self.assertRegex(script, re.compile(r"\bes\s*:", re.MULTILINE))
        self.assertIn("attribution.textContent = languageCopy.attribution", script)
        self.assertIn("Crea el borrador para ver el cuento completo en español.", script)
        self.assertRegex(script, re.compile(r"buildStory[\s\S]{0,500}language", re.IGNORECASE))
        self.assertRegex(script, re.compile(r"meta\.textContent[\s\S]{0,500}language", re.IGNORECASE))
        self.assertRegex(
            script,
            re.compile(
                r"(?:story-language|storyLanguage|language)[\s\S]*?addEventListener\(\s*[\"']change[\"'][\s\S]*?(?:setState\(\s*[\"']draft[\"']|reset[^\n{]*approval)",
                re.IGNORECASE,
            ),
        )
        spanish_markers = ("Papá", "papá", "más", "señal", "¿")
        self.assertTrue(any(marker in script for marker in spanish_markers))

    @unittest.skipUnless(shutil.which("node"), "Node is unavailable")
    def test_story_builder_returns_distinct_unmixed_english_and_spanish_output(self) -> None:
        story_path = PROTOTYPE_ROOT / "story.js"
        harness = r'''
const fs = require("fs");
const vm = require("vm");
const noop = () => {};
const element = {
  addEventListener: noop,
  classList: { toggle: noop },
  focus: noop,
  dataset: {},
  textContent: "",
  className: "",
  value: ""
};
const context = {
  document: {
    querySelector: () => element,
    querySelectorAll: () => []
  },
  console,
  FormData: function () { return []; }
};
vm.createContext(context);
const source = fs.readFileSync(process.argv[1], "utf8");
vm.runInContext(source + "\n;globalThis.__buildStory = buildStory;", context);
const input = { routine: "snack", length: "short", tone: "calm" };
const result = {
  en: context.__buildStory({ ...input, language: "en" }),
  es: context.__buildStory({ ...input, language: "es" })
};
process.stdout.write(JSON.stringify(result));
'''
        result = subprocess.run(
            [shutil.which("node") or "node", "-e", harness, str(story_path)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        variants = json.loads(result.stdout)
        self.assertNotEqual(variants["en"]["title"], variants["es"]["title"])
        self.assertNotEqual(variants["en"]["text"], variants["es"]["text"])

        spanish = json.dumps(variants["es"], ensure_ascii=False)
        for english_leak in (
            r"\bDad\b",
            r"\bWould\b",
            r"\basked\b",
            r"\bfinished\b",
            r"\blooked\b",
            r"\bsmiled\b",
            r"\bSnack time\b",
        ):
            self.assertNotRegex(spanish, re.compile(english_leak, re.IGNORECASE))
        self.assertTrue(any(marker in spanish for marker in ("Papá", "papá", "más", "señal", "¿")))

    def test_cross_route_sign_handoffs_fail_closed_and_primary_copy_stays_truthful(self) -> None:
        content_engine = (PROTOTYPE_ROOT / "content-engine.js").read_text(encoding="utf-8")
        story = (PROTOTYPE_ROOT / "story.js").read_text(encoding="utf-8")
        create_sign = (PROTOTYPE_ROOT / "create-sign.js").read_text(encoding="utf-8")

        self.assertIn('parameters.has("sign")', content_engine)
        self.assertIn("selectUnsupportedSign(requested)", content_engine)
        self.assertIn("renderUnsupportedSign(contentPackSign.value)", content_engine)
        self.assertIn("This sign is not available in the current demo set. Choose another sign.", content_engine)
        self.assertRegex(
            content_engine,
            re.compile(r"renderUnsupportedSign[\s\S]{0,1200}generateContentPack\.disabled\s*=\s*true"),
        )

        self.assertIn('parameters.has("sign")', story)
        self.assertIn('requestedSign !== "more"', story)
        self.assertIn("A story has not been prepared for this sign yet.", story)
        self.assertIn("No story was created", story)
        self.assertNotIn("continuó con ayudándola", story)
        self.assertIn("continuation: \"la rutina de vestirse\"", story)

        self.assertIn('STAGE_LABELS[active.key] || "Reference review"', create_sign)
        self.assertNotIn("`${active.label} is running", create_sign)

        studio = (PROTOTYPE_ROOT / "content-studio.html").read_text(encoding="utf-8")
        school = (PROTOTYPE_ROOT / "school.html").read_text(encoding="utf-8")
        print_surface = "\n".join(
            (
                (PROTOTYPE_ROOT / "print-card.html").read_text(encoding="utf-8"),
                (PROTOTYPE_ROOT / "print-card.js").read_text(encoding="utf-8"),
            )
        )
        self.assertNotRegex(studio, re.compile(r"published sign", re.IGNORECASE))
        school_primary = " ".join(self.parsers["school.html"].primary_text)
        self.assertNotRegex(school_primary, re.compile(r"publish", re.IGNORECASE))
        self.assertNotRegex(print_surface, re.compile(r"internal printable", re.IGNORECASE))
        self.assertNotIn("available candidate", print_surface.lower())

        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        limitation = registry["assets"]["visual_sign_packages"]["known_limitation"]
        self.assertIn("All six canonical signs", limitation)
        self.assertNotIn("Only MORE and EAT", limitation)


if __name__ == "__main__":
    unittest.main()
