from __future__ import annotations

import json
import unittest
from html.parser import HTMLParser
from pathlib import Path


PROTOTYPE_ROOT = Path(__file__).resolve().parents[1]


class IdCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []

    def handle_starttag(self, _tag: str, attrs: list[tuple[str, str | None]]) -> None:
        element_id = dict(attrs).get("id")
        if element_id:
            self.ids.append(element_id)


class VisualWorkflowTests(unittest.TestCase):
    def test_workflow_pages_have_unique_ids(self) -> None:
        for filename in ("create-sign.html", "flashcards.html"):
            parser = IdCollector()
            parser.feed((PROTOTYPE_ROOT / filename).read_text(encoding="utf-8"))
            self.assertEqual(len(parser.ids), len(set(parser.ids)), filename)

    def test_create_sign_includes_required_operator_states_and_ctas(self) -> None:
        html = (PROTOTYPE_ROOT / "create-sign.html").read_text(encoding="utf-8")
        for text in (
            "Technical review needed",
            "Ready to prepare visual",
            "Generate visual candidates",
            "Visual review",
            "Approve visual",
            "Approved for printable",
            "Create printable",
        ):
            self.assertIn(text, html)

    def test_more_visual_package_resolves_existing_assets(self) -> None:
        payload = json.loads(
            (PROTOTYPE_ROOT / "data/visual_sign_packages.json").read_text(encoding="utf-8")
        )
        more = next(item for item in payload["signs"] if item["sign_id"] == "more")
        self.assertEqual(more["labels"], {"en": "MORE", "es": "MÁS"})
        self.assertEqual(more["movement"]["hands"], 2)
        self.assertGreaterEqual(len(more["candidates"]), 2)
        for candidate in more["candidates"]:
            self.assertTrue((PROTOTYPE_ROOT / candidate["asset"]).is_file())
        self.assertTrue((PROTOTYPE_ROOT / more["contextual_image"]["asset"]).is_file())

    def test_printable_has_real_visual_slots_and_bilingual_controls(self) -> None:
        html = (PROTOTYPE_ROOT / "flashcards.html").read_text(encoding="utf-8")
        self.assertIn("data-context-image", html)
        self.assertIn("data-sign-illustration", html)
        self.assertIn("data-routine-icon", html)
        self.assertIn('name="language" value="en"', html)
        self.assertIn('name="language" value="es"', html)
        self.assertNotIn("Character and reviewed hand pose go here", html)


if __name__ == "__main__":
    unittest.main()
