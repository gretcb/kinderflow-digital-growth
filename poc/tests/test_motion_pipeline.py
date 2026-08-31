"""Regression checks for the Kinder Signs motion-representation POC."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "poc" / "src"
sys.path.insert(0, str(SRC_DIR))

from normalize_landmarks import classify_gap, contiguous_runs  # noqa: E402
from validate_output import evaluate_extraction_status  # noqa: E402


class ThresholdTests(unittest.TestCase):
    def test_extraction_status_boundaries(self) -> None:
        self.assertEqual(evaluate_extraction_status(90.0, 95.0)[0], "EXTRACTION_PASS")
        self.assertEqual(evaluate_extraction_status(89.99, 100.0)[0], "EXTRACTION_PARTIAL")
        self.assertEqual(evaluate_extraction_status(69.99, 100.0)[0], "EXTRACTION_FAIL")
        self.assertEqual(evaluate_extraction_status(95.0, 94.99)[0], "EXTRACTION_PARTIAL")

    def test_gap_detection_and_classification(self) -> None:
        self.assertEqual(contiguous_runs([0, 1, 4, 7, 8]), [(0, 1), (4, 4), (7, 8)])
        self.assertEqual(classify_gap(0, 2, 10), "leading")
        self.assertEqual(classify_gap(4, 4, 10), "internal")
        self.assertEqual(classify_gap(8, 9, 10), "trailing")


class GeneratedEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.hand_path = REPO_ROOT / "poc/output/normalized/sign_reference_hand_normalized.csv"
        cls.raw_hand_path = REPO_ROOT / "poc/output/landmarks/sign_reference_hand_landmarks.csv"
        cls.summary_path = REPO_ROOT / "poc/output/diagnostics/sign_reference_motion_summary.json"
        if not all(path.exists() for path in (cls.hand_path, cls.raw_hand_path, cls.summary_path)):
            raise unittest.SkipTest("Local private/raw pipeline outputs are unavailable")
        cls.hand = pd.read_csv(cls.hand_path)
        cls.raw_hand = pd.read_csv(cls.raw_hand_path)
        cls.summary = json.loads(cls.summary_path.read_text(encoding="utf-8"))

    def test_complete_expected_hand_index(self) -> None:
        self.assertEqual(len(self.hand), 332 * 21)
        self.assertTrue((self.hand.groupby("frame").size() == 21).all())
        self.assertFalse(self.hand.duplicated(["frame", "hand", "landmark_id"]).any())

    def test_gap_flags_are_conservative(self) -> None:
        by_frame = self.hand.groupby("frame").agg(
            detected=("is_detected", "all"),
            interpolated=("is_interpolated", "all"),
            unresolved=("is_unresolved", "any"),
        )
        self.assertTrue(by_frame.loc[320, "interpolated"])
        self.assertFalse(by_frame.loc[320, "unresolved"])
        self.assertTrue(by_frame.loc[list(range(0, 9)), "unresolved"].all())
        self.assertTrue(by_frame.loc[list(range(322, 332)), "unresolved"].all())
        self.assertEqual(int(by_frame["interpolated"].sum()), 1)
        self.assertEqual(int(by_frame["unresolved"].sum()), 19)

    def test_raw_coordinates_are_preserved_in_derived_rows(self) -> None:
        detected = self.hand.loc[self.hand["is_detected"]]
        merged = detected.merge(
            self.raw_hand,
            on=["frame", "hand", "landmark_id"],
            how="left",
            validate="one_to_one",
        )
        for axis in ("x", "y", "z"):
            pd.testing.assert_series_equal(
                merged[f"raw_{axis}"],
                merged[axis],
                check_names=False,
                check_exact=False,
                rtol=0,
                atol=1e-15,
            )

    def test_summary_is_bounded(self) -> None:
        self.assertEqual(self.summary["extraction"]["status"], "EXTRACTION_PASS")
        self.assertEqual(self.summary["status"], "MOTION_REPRESENTATION_PARTIAL")
        self.assertEqual(
            self.summary["technical_feasibility"]["decision"], "Proceed with conditions"
        )


if __name__ == "__main__":
    unittest.main()
