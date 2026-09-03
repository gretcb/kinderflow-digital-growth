from __future__ import annotations

import hashlib
import json
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from typing import List, Optional, Tuple


REPO_ROOT = Path(__file__).resolve().parents[2]
PROTOTYPE_ROOT = REPO_ROOT / "prototype"
PROVENANCE_PATH = REPO_ROOT / "assets/flashcards/open_peeps/provenance.json"


class IdCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: List[str] = []

    def handle_starttag(self, _tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        element_id = dict(attrs).get("id")
        if element_id:
            self.ids.append(element_id)


class VisualWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(
            (PROTOTYPE_ROOT / "data/visual_sign_packages.json").read_text(encoding="utf-8")
        )

    def package(self, sign_id: str) -> dict:
        return next(item for item in self.payload["signs"] if item["sign_id"] == sign_id)

    def test_workflow_pages_have_unique_ids(self) -> None:
        for filename in ("create-sign.html", "flashcards.html", "print-card.html"):
            parser = IdCollector()
            parser.feed((PROTOTYPE_ROOT / filename).read_text(encoding="utf-8"))
            self.assertEqual(len(parser.ids), len(set(parser.ids)), filename)

    def test_create_sign_includes_explicit_states_routes_and_actions(self) -> None:
        html = (PROTOTYPE_ROOT / "create-sign.html").read_text(encoding="utf-8")
        implementation = html + (PROTOTYPE_ROOT / "create-sign.js").read_text(encoding="utf-8")
        for text in (
            "Reference review complete",
            "Use reviewed references",
            "Choose one or two reference poses",
            "Create another visual option",
            "Approve selected visual",
            "Reject visual",
            "Create family materials",
            "Add to library or use later",
            "Sources and permissions",
        ):
            self.assertIn(text, implementation)

    def test_actual_open_peeps_components_are_recorded_and_embedded(self) -> None:
        provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(provenance["licence"], "CC0")
        self.assertEqual(provenance["verification_basis"], "Founder-verified official CC0 reference")
        components = {item["role"]: item for item in provenance["selected_components"]}
        self.assertTrue(components["base_character"]["path"].endswith("/Separate Atoms/a person/bust.svg"))
        self.assertTrue(components["hand_finger_style_grammar"]["path"].endswith("/pose/standing/pointing_finger-1.svg"))
        self.assertTrue(components["shoulder_arm_style_grammar"]["path"].endswith("/Templates/Bust/peep-4.svg"))
        output = (PROTOTYPE_ROOT / "assets/signs/more-a.svg").read_text(encoding="utf-8")
        for role in ("base_character", "hand_finger_style_grammar", "shoulder_arm_style_grammar"):
            self.assertIn(components[role]["path"], output)
        bust_path = REPO_ROOT / components["base_character"]["path"]
        bust_source = bust_path.read_text(encoding="utf-8")
        bust_inner = bust_source[bust_source.index(">", bust_source.index("<svg")) + 1:bust_source.rindex("</svg>")].strip()
        self.assertIn(bust_inner, output)
        self.assertIn("Exact registered Open Peeps bust geometry", output)

    def test_more_composer_excludes_seated_pose_and_constructs_full_upper_limbs(self) -> None:
        generator = (REPO_ROOT / "tools/build_sign_vectors.py").read_text(encoding="utf-8")
        provenance = PROVENANCE_PATH.read_text(encoding="utf-8")
        outputs = "\n".join(
            (PROTOTYPE_ROOT / f"assets/signs/more-{suffix}.svg").read_text(encoding="utf-8")
            for suffix in ("a", "b", "c")
        )
        self.assertNotIn("mid-2.svg", generator + provenance + outputs)
        for token in (
            "sign-specific-upper-limbs",
            "complete-upper-limb",
            "shoulder-arm",
            "upper-arm",
            "elbow",
            "forearm",
            "wrist",
            "flat-o-hand",
            "finger-path",
            'data-hands="2"',
            'data-location="upper-chest"',
        ):
            self.assertIn(token, outputs)
        self.assertGreaterEqual(outputs.count('class="finger-path'), 20)
        for leak in ("stump", "placeholder"):
            self.assertNotIn(leak, outputs.lower())

    def test_more_svg_candidates_are_valid_xml(self) -> None:
        for suffix in ("a", "b", "c"):
            ET.parse(PROTOTYPE_ROOT / f"assets/signs/more-{suffix}.svg")

    def test_source_filenames_do_not_appear_in_primary_html(self) -> None:
        primary = "\n".join(
            (PROTOTYPE_ROOT / filename).read_text(encoding="utf-8")
            for filename in ("create-sign.html", "flashcards.html", "print-card.html")
        )
        for leak in ("bust.svg", "peep-4.svg", "pointing_finger-1.svg", "more.jpg", "mid-2.svg", "visual_sign_packages.json"):
            self.assertNotIn(leak, primary)

    def test_more_and_eat_packages_resolve_distinct_assets_and_bilingual_copy(self) -> None:
        for sign_id, labels in (("more", {"en": "MORE", "es": "MÁS"}), ("eat", {"en": "EAT", "es": "COMER"})):
            package = self.package(sign_id)
            self.assertEqual(package["labels"], labels)
            self.assertTrue(package["routine"]["en"])
            self.assertTrue(package["routine"]["es"])
            identities = set()
            for candidate in package["candidates"] + package["regeneration_candidates"]:
                path = PROTOTYPE_ROOT / candidate["asset"]
                self.assertTrue(path.is_file())
                actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
                self.assertEqual(candidate["content_hash"], actual_hash)
                identities.add((candidate["id"], candidate["asset"], candidate["content_hash"]))
            self.assertEqual(len(identities), 3)

    def test_eat_fallback_and_rationale_are_persisted_without_publication(self) -> None:
        package = self.package("eat")
        self.assertEqual(package["evidence_routes"]["review"], "KNOWLEDGE_REFERENCE_FALLBACK")
        self.assertEqual(package["knowledge"]["repetition"], "One tap for this reviewed teaching distinction")
        script = (PROTOTYPE_ROOT / "create-sign.js").read_text(encoding="utf-8")
        for token in (
            "ACCEPT_WITH_FALLBACK",
            "technical_review_rationale",
            "KNOWLEDGE_REFERENCE_FALLBACK",
            'publication_status: "DRAFT"',
        ):
            self.assertIn(token, script)

    def test_regeneration_calls_local_service_and_does_not_reorder(self) -> None:
        script = (PROTOTYPE_ROOT / "create-sign.js").read_text(encoding="utf-8")
        self.assertIn("/api/visual-candidates/regenerate", script)
        self.assertIn("candidate.content_hash", script)
        self.assertNotIn("candidates.reverse()", script)
        self.assertNotIn("generationRevision", script)

    def test_more_recommendation_and_review_criteria_are_honest(self) -> None:
        package = self.package("more")
        self.assertFalse(package["candidates"][0]["recommended"])
        self.assertTrue(package["candidates"][1]["recommended"])
        self.assertEqual(package["review_status"], "READY_FOR_HUMAN_REVIEW")
        self.assertEqual(package["publication_status"], "DRAFT")
        implementation = (PROTOTYPE_ROOT / "create-sign.js").read_text(encoding="utf-8")
        html = (PROTOTYPE_ROOT / "create-sign.html").read_text(encoding="utf-8")
        self.assertIn("Recommended for this sign", implementation)
        for copy in (
            "Hands are easy to read",
            "Body position is clear",
            "Movement is understandable",
            "Visual matches the reviewed sign reference",
            "Final sign approval remains a human decision",
        ):
            self.assertIn(copy, html)

    def test_local_visual_approval_never_publishes(self) -> None:
        script = (PROTOTYPE_ROOT / "create-sign.js").read_text(encoding="utf-8")
        self.assertIn('publication_status: "DRAFT"', script)
        self.assertIn('visual_review_status: "APPROVED_FOR_INTERNAL_PRINTABLE"', script)
        self.assertNotIn('publication_status: "PUBLISHED"', script)

    def test_print_route_is_one_a5_card_without_ui_chrome(self) -> None:
        html = (PROTOTYPE_ROOT / "print-card.html").read_text(encoding="utf-8")
        css = (PROTOTYPE_ROOT / "styles.css").read_text(encoding="utf-8")
        script = (PROTOTYPE_ROOT / "print-card.js").read_text(encoding="utf-8")
        self.assertEqual(html.count('class="a5-print-card"'), 1)
        self.assertNotIn("<nav", html)
        self.assertIn("size: A5 portrait", css)
        self.assertIn("width: 148mm", css)
        self.assertIn("height: 210mm", css)
        for selector in (
            "body.flashcard-page .print-sheet .flashcard-output:not([hidden])",
            "body.flashcard-page .print-sheet .flashcard-output[hidden]",
            "body.print-card-page .a5-print-card:not([hidden])",
            "body.print-card-page .print-card-stage .a5-print-card[hidden]",
        ):
            self.assertIn(selector, css)
        self.assertIn("routineArea.remove()", script)
        self.assertIn("flashcardArea.remove()", script)
        self.assertIn("await waitForImages()", script)
        self.assertIn("sign visual", script.lower())
        self.assertIn("cannot be found", script.lower())
        self.assertNotIn("position: absolute", css[css.index(".a5-guidance-row"):css.index(".a5-card-footer")])

    def test_flashcard_contract_retains_context_and_routine_icon(self) -> None:
        html = (PROTOTYPE_ROOT / "flashcards.html").read_text(encoding="utf-8")
        self.assertIn("data-context-image", html)
        self.assertIn("data-sign-illustration", html)
        self.assertIn("data-routine-icon", html)
        self.assertIn('name="language" value="en"', html)
        self.assertIn('name="language" value="es"', html)
        self.assertNotIn("Character and reviewed hand pose go here", html)


if __name__ == "__main__":
    unittest.main()
