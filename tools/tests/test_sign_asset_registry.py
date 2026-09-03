from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path

from tools import build_sign_asset_registry as builder


class SignAssetRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = builder.build(write=False)
        cls.assets = cls.registry["assets"]

    def sign(self, sign_id: str) -> dict:
        return builder.get_sign(self.registry, sign_id)

    def test_canonical_signs_include_water(self) -> None:
        self.assertEqual(
            self.registry["canonical_sign_ids"],
            ["more", "help", "eat", "sleep", "milk", "water"],
        )
        self.assertEqual(
            [sign["sign_id"] for sign in self.registry["signs"]],
            self.registry["canonical_sign_ids"],
        )

    def test_labels_are_correct_in_english_and_spanish(self) -> None:
        expected = {
            "more": ("MORE", "MÁS"),
            "help": ("HELP", "AYUDA"),
            "eat": ("EAT", "COMER"),
            "sleep": ("SLEEP", "DORMIR"),
            "milk": ("MILK", "LECHE"),
            "water": ("WATER", "AGUA"),
        }
        for sign_id, labels in expected.items():
            sign = self.sign(sign_id)
            self.assertEqual((sign["label_en"], sign["label_es"]), labels)

    def test_reference_input_video_exists_for_every_canonical_sign(self) -> None:
        for sign in self.registry["signs"]:
            asset = self.assets[sign["reference_video_input"]]
            self.assertTrue(asset["exists"], sign["sign_id"])
            self.assertIn("/video_input/", asset["path"])
            self.assertEqual(sign["reference_video_hash"], asset["sha256"])

    def test_gemini_demo_outputs_exist_only_for_more_help_and_milk(self) -> None:
        expected = {"more": "mas.mp4", "help": "ayuda.mp4", "milk": "leche.mp4"}
        for sign in self.registry["signs"]:
            asset_id = sign["gemini_demo_video"]
            if sign["sign_id"] in expected:
                self.assertIsNotNone(asset_id)
                asset = self.assets[asset_id]
                self.assertTrue(asset["exists"])
                self.assertEqual(Path(asset["path"]).name, expected[sign["sign_id"]])
                self.assertEqual(asset["asset_class"], "PREGENERATED_DEMO_OUTPUT")
            else:
                self.assertIsNone(asset_id)
                self.assertEqual(sign["gemini_demo_status"], "NOT_AVAILABLE_STATIC_FLOW_ALLOWED")

    def test_required_open_peeps_base_and_arm_reference_exist(self) -> None:
        base = self.assets["open_peeps_bust_base"]
        arm = self.assets["open_peeps_arm_reference"]
        self.assertTrue(base["exists"])
        self.assertTrue(base["path"].endswith("/Separate Atoms/a person/bust.svg"))
        self.assertTrue(arm["exists"])
        self.assertTrue(arm["path"].endswith("/Templates/Bust/peep-4.svg"))

    def test_exact_hand_style_reference_is_found_or_a_blocking_gap(self) -> None:
        asset = self.assets[builder.POINTING_ASSET_ID]
        if asset["exists"]:
            self.assertEqual(Path(asset["path"]).name.casefold(), "pointing_finger-1.svg")
            for sign in self.registry["signs"]:
                self.assertEqual(sign["open_peeps_reference_status"], "AVAILABLE_REFERENCE_ONLY")
        else:
            self.assertEqual(asset["path"], builder.POINTING_EXPECTED)
            self.assertIn("BLOCKING GAP", asset["known_limitation"])
            for sign in self.registry["signs"]:
                self.assertEqual(
                    sign["open_peeps_reference_status"],
                    "BLOCKED_MISSING_EXACT_HAND_STYLE_REFERENCE",
                )
                self.assertTrue(any(builder.POINTING_EXPECTED in gap for gap in sign["known_gaps"]))

    def test_all_functional_illustrations_exist(self) -> None:
        for sign in self.registry["signs"]:
            asset = self.assets[sign["functional_sign_illustration"]]
            self.assertTrue(asset["exists"], sign["sign_id"])
            self.assertEqual(Path(asset["path"]).name, "{0}.jpg".format(sign["sign_id"]))

    def test_water_supporting_evidence_and_more_demo_keep_distinct_identities(self) -> None:
        water = self.sign("water")
        for field in ("reference_video_input", "reference_flashcard", "functional_sign_illustration"):
            asset = self.assets[water[field]]
            self.assertTrue(asset["exists"], field)
            self.assertEqual(asset["sign_mapping"], ["water"])

        historical_water_reference = builder.REPO_ROOT / "poc/input/sign_reference.mp4"
        self.assertTrue(historical_water_reference.is_file())
        historical_water_hash = hashlib.sha256(historical_water_reference.read_bytes()).hexdigest()
        water_input = self.assets[water["reference_video_input"]]
        more_input = self.assets[self.sign("more")["reference_video_input"]]
        current_more_demo = builder.RESOURCE_ROOT / "video_input/more.mp4"
        self.assertTrue(current_more_demo.is_file())
        current_more_hash = hashlib.sha256(current_more_demo.read_bytes()).hexdigest()
        self.assertEqual(historical_water_hash, water_input["sha256"])
        self.assertNotEqual(historical_water_hash, more_input["sha256"])
        self.assertEqual(current_more_hash, more_input["sha256"])
        self.assertNotEqual(current_more_hash, water_input["sha256"])

    def test_water_assets_never_map_to_more(self) -> None:
        water = self.sign("water")
        water_asset_ids = {
            water["reference_video_input"],
            water["reference_flashcard"],
            water["functional_sign_illustration"],
        }
        for asset_id in water_asset_ids:
            self.assertNotIn("more", self.assets[asset_id]["sign_mapping"], asset_id)

    def test_all_reference_flashcards_exist_and_are_not_outputs(self) -> None:
        for sign in self.registry["signs"]:
            asset_id = sign["reference_flashcard"]
            asset = self.assets[asset_id]
            self.assertTrue(asset["exists"], sign["sign_id"])
            self.assertFalse(asset["printable_allowed"])
            self.assertNotIn(asset_id, sign["flashcard_outputs"])
            self.assertNotIn(asset_id, sign["routine_card_outputs"])

    def test_no_absolute_external_path_is_exposed_to_browser_data(self) -> None:
        for asset in self.assets.values():
            self.assertFalse(Path(asset["path"]).is_absolute())
        projection = builder.REPO_ROOT / "prototype/data/sign_asset_registry.json"
        if projection.exists():
            payload = projection.read_text(encoding="utf-8")
            self.assertNotIn(str(builder.RESOURCE_ROOT), payload)
            self.assertNotIn("/Users/", payload)

    def test_unknown_sign_fails_closed(self) -> None:
        with self.assertRaises(builder.RegistryValidationError):
            builder.get_sign(self.registry, "unsupported-sign")

    def test_registry_validates_against_committed_json_schema(self) -> None:
        schema = json.loads(builder.SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        builder.validate_against_schema(self.registry, schema)

    def test_every_asset_has_exactly_one_allowed_class(self) -> None:
        self.assertEqual(set(self.registry["asset_classes"]), builder.ASSET_CLASSES)
        for asset in self.assets.values():
            self.assertIn(asset["asset_class"], builder.ASSET_CLASSES)
            self.assertIsInstance(asset["asset_class"], str)

    def test_output_video_cannot_be_mapped_as_reference_input(self) -> None:
        invalid = copy.deepcopy(self.registry)
        more = builder.get_sign(invalid, "more")
        more["reference_video_input"] = "demo_more"
        more["reference_video_hash"] = invalid["assets"]["demo_more"]["sha256"]
        with self.assertRaises(builder.RegistryValidationError):
            builder.validate_registry(invalid)

    def test_optional_demo_output_may_be_absent(self) -> None:
        valid = copy.deepcopy(self.registry)
        more = builder.get_sign(valid, "more")
        demo = valid["assets"][more["gemini_demo_video"]]
        demo["exists"] = False
        demo["file_type"] = None
        demo["byte_size"] = None
        demo["sha256"] = None
        more["gemini_demo_status"] = "OPTIONAL_DEMO_FILE_MISSING_STATIC_FLOW_ALLOWED"
        builder.validate_registry(valid)

    def test_reference_flashcard_cannot_be_mapped_as_distributable_output(self) -> None:
        invalid = copy.deepcopy(self.registry)
        more = builder.get_sign(invalid, "more")
        more["flashcard_outputs"] = [more["reference_flashcard"]]
        with self.assertRaises(builder.RegistryValidationError):
            builder.validate_registry(invalid)

    def test_duplicate_sign_file_mapping_is_rejected(self) -> None:
        invalid = copy.deepcopy(self.registry)
        help_sign = builder.get_sign(invalid, "help")
        help_sign["reference_video_input"] = "input_more"
        help_sign["reference_video_hash"] = invalid["assets"]["input_more"]["sha256"]
        invalid["assets"]["input_more"]["sign_mapping"].append("help")
        with self.assertRaises(builder.RegistryValidationError):
            builder.validate_registry(invalid)


if __name__ == "__main__":
    unittest.main()
