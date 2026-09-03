from __future__ import annotations

import hashlib
import json
import unittest
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
            "Technical review needed",
            "Continue with grounded fallback",
            "Choose reference frames",
            "Generate another candidate",
            "Approve selected visual",
            "Reject visual",
            "Approved for internal printable",
            "Create printable",
            "Reference source URL",
        ):
            self.assertIn(text, implementation)

    def test_actual_open_peeps_components_are_recorded_and_embedded(self) -> None:
        provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(provenance["licence"], "CC0")
        self.assertEqual(provenance["verification_basis"], "Founder-verified official CC0 reference")
        paths = [item["path"] for item in provenance["selected_components"]]
        self.assertTrue(any(path.endswith("/face/Smile.svg") for path in paths))
        self.assertTrue(any(path.endswith("/head/Bun 2.svg") for path in paths))
        self.assertTrue(any(path.endswith("/pose/sitting/mid-2.svg") for path in paths))
        output = (PROTOTYPE_ROOT / "assets/signs/more-a.svg").read_text(encoding="utf-8")
        for path in paths:
            self.assertIn(path, output)
        self.assertIn("Actual Open Peeps source geometry", output)

    def test_source_filenames_do_not_appear_in_primary_html(self) -> None:
        primary = "\n".join(
            (PROTOTYPE_ROOT / filename).read_text(encoding="utf-8")
            for filename in ("create-sign.html", "flashcards.html", "print-card.html")
        )
        for leak in ("Smile.svg", "Bun 2.svg", "mid-2.svg", "visual_sign_packages.json"):
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

    def test_print_route_is_one_a5_card_without_ui_chrome(self) -> None:
        html = (PROTOTYPE_ROOT / "print-card.html").read_text(encoding="utf-8")
        css = (PROTOTYPE_ROOT / "styles.css").read_text(encoding="utf-8")
        script = (PROTOTYPE_ROOT / "print-card.js").read_text(encoding="utf-8")
        self.assertEqual(html.count('class="a5-print-card"'), 1)
        self.assertNotIn("<nav", html)
        self.assertIn("size: A5 portrait", css)
        self.assertIn("width: 148mm", css)
        self.assertIn("height: 210mm", css)
        self.assertIn("routineArea.remove()", script)
        self.assertIn("flashcardArea.remove()", script)
        self.assertIn("await waitForImages()", script)
        self.assertIn("The approved visual cannot be found", script)
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
