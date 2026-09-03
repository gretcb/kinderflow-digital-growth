from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch

import cv2
import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
MVP_ROOT = REPO_ROOT / "mvp"
sys.path.insert(0, str(MVP_ROOT))

import pipeline  # noqa: E402
from app import regenerate_visual_candidate, response_schema_ok  # noqa: E402


class IdCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids = []

    def handle_starttag(self, _tag, attrs) -> None:
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.append(attributes["id"])


class InputSafetyTests(unittest.TestCase):
    def test_valid_mp4_extension_is_accepted(self) -> None:
        self.assertEqual(pipeline.validate_extension("reference.MP4"), "reference.mp4")

    def test_invalid_extension_is_rejected(self) -> None:
        with self.assertRaisesRegex(pipeline.InputError, "supported MP4"):
            pipeline.validate_extension("reference.mov")

    def test_optional_reference_source_url_is_validated_for_provenance_only(self) -> None:
        self.assertEqual(
            pipeline.validate_reference_source_url("https://example.org/sign/more"),
            "https://example.org/sign/more",
        )
        self.assertIsNone(pipeline.validate_reference_source_url(""))
        with self.assertRaisesRegex(pipeline.InputError, "complete http"):
            pipeline.validate_reference_source_url("example.org/sign")

    def test_filename_is_reduced_to_safe_provenance(self) -> None:
        self.assertEqual(
            pipeline.safe_filename("../../private/My sign (final).mp4"),
            "My_sign_final.mp4",
        )

    def test_empty_video_is_handled(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.mp4"
            path.touch()
            with self.assertRaisesRegex(pipeline.InputError, "Try another"):
                pipeline.inspect_video(path)

    def test_small_valid_video_is_inspected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "valid.mp4"
            writer = cv2.VideoWriter(
                str(path),
                cv2.VideoWriter_fourcc(*"mp4v"),
                10,
                (64, 64),
            )
            self.assertTrue(writer.isOpened())
            for _ in range(4):
                writer.write(np.zeros((64, 64, 3), dtype=np.uint8))
            writer.release()
            metadata = pipeline.inspect_video(path)
            self.assertEqual(metadata["frames_reported"], 4)
            self.assertEqual(metadata["resolution"], {"width": 64, "height": 64})

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg is unavailable")
    def test_overlay_is_transcoded_to_browser_h264(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            intermediate = Path(directory) / "overlay.mp4"
            writer = cv2.VideoWriter(
                str(intermediate),
                cv2.VideoWriter_fourcc(*"mp4v"),
                10,
                (64, 64),
            )
            for index in range(6):
                frame = np.full((64, 64, 3), 40 + index * 20, dtype=np.uint8)
                cv2.line(frame, (8, 8), (56, 56), (0, 255, 0), 3)
                writer.write(frame)
            writer.release()
            metadata = pipeline.finalize_browser_preview(intermediate)
            final_path = Path(metadata["path"])
            probe = subprocess.run(
                [
                    shutil.which("ffprobe"),
                    "-v",
                    "error",
                    "-select_streams",
                    "v:0",
                    "-show_entries",
                    "stream=codec_name,codec_tag_string,pix_fmt,nb_frames,duration",
                    "-of",
                    "json",
                    str(final_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            stream = json.loads(probe.stdout)["streams"][0]
            self.assertEqual(stream["codec_name"], "h264")
            self.assertEqual(stream["codec_tag_string"], "avc1")
            self.assertEqual(stream["pix_fmt"], "yuv420p")
            self.assertEqual(int(stream["nb_frames"]), 6)
            self.assertGreater(float(stream["duration"]), 0)


class PipelineStateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.run_dir = Path(self.temporary.name) / "run_test"
        (self.run_dir / "input").mkdir(parents=True)
        video = self.run_dir / "input" / "reference.mp4"
        writer = cv2.VideoWriter(
            str(video),
            cv2.VideoWriter_fourcc(*"mp4v"),
            10,
            (64, 64),
        )
        for _ in range(4):
            writer.write(np.zeros((64, 64, 3), dtype=np.uint8))
        writer.release()
        self.manifest = {
            "run_id": "run_test",
            "state": "queued",
            "created_at": pipeline.utc_now(),
            "sign": {
                "name": "MORE",
                "routine_context": "Snack time",
                "reference_status": "Validated reference",
            },
            "source": {
                "kind": "test",
                "reference_id": "reference",
                "display_filename": "reference.mp4",
                "child_video_used": False,
            },
            "stages": pipeline.initial_stages(),
            "technical_status": "Waiting",
            "content_status": "Draft",
            "warnings": [],
            "error": None,
            "artifacts": {},
            "processing": {},
        }

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_response_schema(self) -> None:
        payload = pipeline.public_run(self.manifest)
        self.assertTrue(response_schema_ok(payload))

    @patch.object(pipeline, "normalize_and_smooth")
    @patch.object(pipeline, "finalize_browser_preview")
    @patch.object(pipeline, "process_video")
    @patch.object(pipeline, "analyse_motion")
    def test_insufficient_coverage_is_controlled(
        self, mocked_analysis, mocked_extraction, mocked_preview, _mocked_normalize
    ) -> None:
        mocked_extraction.return_value = {
            "validation": {"status": "EXTRACTION_FAIL"},
            "preview_path": str(self.run_dir / "output/previews/reference_landmarks.mp4"),
        }
        mocked_preview.return_value = {
            "path": str(self.run_dir / "output/previews/reference_landmarks_browser.mp4"),
            "duration_seconds": 0.4,
            "frames_reported": 4,
        }
        mocked_analysis.return_value = {
            "technical_feasibility": {"decision": "Stop"},
            "extraction": {
                "frames_total": 4,
                "pose_detection_rate_percent": 100.0,
                "hand_detection_rate_percent": 0.0,
                "status": "EXTRACTION_FAIL",
            },
            "missing_data": {
                "missing_frames_total": 4,
                "gap_count": 1,
                "interpolated_frames": 0,
                "unresolved_frames": 4,
            },
            "status": "MOTION_REPRESENTATION_FAIL",
            "status_reasons": ["Hand coverage is insufficient."],
            "quality_assessment": [
                {"dimension": "A. Detection coverage", "status": "FAIL"},
                {"dimension": "B. Missing-data continuity", "status": "FAIL"},
                {"dimension": "C. Short-gap recoverability", "status": "FAIL"},
                {"dimension": "D. Body-relative stability", "status": "PASS"},
                {"dimension": "E. Temporal smoothness", "status": "PASS"},
                {"dimension": "F. Human-inspectable correspondence", "status": "PENDING_EXPERT_REVIEW"},
            ],
        }
        result = pipeline.run_pipeline(self.run_dir, self.manifest)
        self.assertEqual(result["state"], "insufficient_coverage")
        self.assertEqual(result["error"]["code"], "insufficient_coverage")
        self.assertEqual(result["content_status"], "Draft")
        self.assertEqual(result["technical_status"], "Fail")
        stage_statuses = {stage["key"]: stage["status"] for stage in result["stages"]}
        self.assertEqual(stage_statuses["technical_checks"], "Complete")
        self.assertEqual(stage_statuses["results_ready"], "Failed")

    def test_status_mapping_reuses_quality_dimensions(self) -> None:
        base = {
            "extraction": {
                "status": "EXTRACTION_PASS",
                "frames_total": 100,
                "hand_detection_rate_percent": 98.0,
            },
            "missing_data": {"unresolved_frames": 0},
            "status": "MOTION_REPRESENTATION_PARTIAL",
            "quality_assessment": [
                {"dimension": f"{letter}. Test", "status": "PASS"}
                for letter in "ABCDE"
            ],
        }
        self.assertEqual(pipeline.map_technical_status(base)[0], "Pass")
        base["missing_data"]["unresolved_frames"] = 2
        base["quality_assessment"][1] = {
            "dimension": "B. Missing-data continuity",
            "status": "PARTIAL",
        }
        self.assertEqual(pipeline.map_technical_status(base)[0], "Review needed")
        base["status"] = "MOTION_REPRESENTATION_FAIL"
        base["quality_assessment"][4] = {
            "dimension": "E. Temporal smoothness",
            "status": "FAIL",
        }
        self.assertEqual(pipeline.map_technical_status(base)[0], "Fail")

    def test_eat_partial_hand_coverage_is_sign_aware_review_not_fail(self) -> None:
        summary = {
            "extraction": {
                "status": "EXTRACTION_PARTIAL",
                "frames_total": 100,
                "pose_detection_rate_percent": 99.0,
                "hand_detection_rate_percent": 76.57,
            },
            "missing_data": {"unresolved_frames": 19},
            "status": "MOTION_REPRESENTATION_FAIL",
            "quality_assessment": [
                {"dimension": "A. Detection coverage", "status": "PARTIAL"},
                {"dimension": "B. Missing-data continuity", "status": "PARTIAL"},
                {"dimension": "C. Short-gap recoverability", "status": "FAIL"},
                {"dimension": "D. Body-relative stability", "status": "PASS"},
                {"dimension": "E. Temporal smoothness", "status": "FAIL"},
            ],
        }
        status, reasons, unresolved = pipeline.map_technical_status(summary, "EAT")
        self.assertEqual(status, "Review needed")
        self.assertEqual(unresolved, 19.0)
        self.assertTrue(any("reviewed reference" in reason.lower() for reason in reasons))
        self.assertEqual(pipeline.map_technical_status(summary, "MORE")[0], "Fail")

    def test_real_regeneration_returns_distinct_verified_candidate(self) -> None:
        packages = json.loads(
            (REPO_ROOT / "prototype/data/visual_sign_packages.json").read_text(encoding="utf-8")
        )["signs"]
        more = next(item for item in packages if item["sign_id"] == "more")
        current = more["candidates"]
        result = regenerate_visual_candidate(
            {"sign_id": "more", "existing_candidate_ids": [item["id"] for item in current]}
        )
        candidate = result["candidate"]
        self.assertEqual(result["generation_method"], "DETERMINISTIC_LOCAL_VECTOR_RECOMPOSITION")
        self.assertNotIn(candidate["id"], {item["id"] for item in current})
        self.assertNotIn(candidate["asset"], {item["asset"] for item in current})
        asset = REPO_ROOT / "prototype" / candidate["asset"]
        self.assertEqual(hashlib.sha256(asset.read_bytes()).hexdigest(), candidate["content_hash"])
        self.assertEqual(result["publication_status"], "DRAFT")

    def test_regeneration_failure_keeps_existing_candidates_honest(self) -> None:
        packages = json.loads(
            (REPO_ROOT / "prototype/data/visual_sign_packages.json").read_text(encoding="utf-8")
        )["signs"]
        more = next(item for item in packages if item["sign_id"] == "more")
        all_ids = [
            item["id"]
            for item in more.get("candidates", []) + more.get("regeneration_candidates", [])
        ]
        with self.assertRaisesRegex(pipeline.InputError, "No additional local candidate"):
            regenerate_visual_candidate(
                {"sign_id": "more", "existing_candidate_ids": all_ids}
            )

    def test_unknown_sign_never_falls_back_to_more(self) -> None:
        with self.assertRaisesRegex(pipeline.InputError, "not available|No reviewed visual package"):
            regenerate_visual_candidate(
                {"sign_id": "unsupported-sign", "existing_candidate_ids": []}
            )

    def test_water_regeneration_resolves_only_water_assets(self) -> None:
        packages = json.loads(
            (REPO_ROOT / "prototype/data/visual_sign_packages.json").read_text(encoding="utf-8")
        )["signs"]
        water = next(item for item in packages if item["sign_id"] == "water")
        current = water["candidates"]
        result = regenerate_visual_candidate(
            {"sign_id": "water", "existing_candidate_ids": [item["id"] for item in current]}
        )
        candidate = result["candidate"]
        self.assertNotIn("more", candidate["id"].lower())
        self.assertNotIn("more", candidate["asset"].lower())
        self.assertTrue(candidate["id"].lower().startswith("water"))
        self.assertEqual(result["publication_status"], "DRAFT")


class CreateSignPageTests(unittest.TestCase):
    def test_create_sign_page_has_unique_ids_and_governance_boundary(self) -> None:
        html = (REPO_ROOT / "prototype/create-sign.html").read_text(encoding="utf-8")
        parser = IdCollector()
        parser.feed(html)
        self.assertEqual(len(parser.ids), len(set(parser.ids)))
        self.assertIn("What the reference review helps with", html)
        self.assertIn("Find the clearest moments in the sign", html)
        self.assertIn("Final sign approval remains a human decision.", html)
        self.assertIn('src="create-sign.js"', html)

    def test_demo_reference_is_registered_as_more_not_water(self) -> None:
        registry = json.loads(
            (REPO_ROOT / "assets/registry/sign_asset_registry.json").read_text(encoding="utf-8")
        )
        signs = {item["sign_id"]: item for item in registry["signs"]}
        assets = registry["assets"]
        demo_hash = hashlib.sha256(pipeline.DEMO_VIDEO.read_bytes()).hexdigest()
        self.assertEqual(getattr(pipeline, "DEMO_SIGN_ID", None), "more")
        self.assertEqual(getattr(pipeline, "DEMO_SIGN_NAME", None), "MORE")
        self.assertEqual(pipeline.DEMO_VIDEO.name, "more.mp4")
        self.assertEqual(demo_hash, assets[signs["more"]["reference_video_input"]]["sha256"])
        self.assertNotEqual(demo_hash, assets[signs["water"]["reference_video_input"]]["sha256"])
        historical_water = REPO_ROOT / "poc/input/sign_reference.mp4"
        historical_water_hash = hashlib.sha256(historical_water.read_bytes()).hexdigest()
        self.assertEqual(
            historical_water_hash,
            assets[signs["water"]["reference_video_input"]]["sha256"],
        )
        self.assertNotEqual(historical_water_hash, demo_hash)
        self.assertEqual(signs["more"]["landmark_evidence"], [])
        self.assertEqual(
            set(signs["water"]["landmark_evidence"]),
            {
                "water_landmark_summary",
                "water_detection_timeline",
                "water_validation_summary",
            },
        )

        script = (REPO_ROOT / "prototype/create-sign.js").read_text(encoding="utf-8")
        self.assertRegex(script, r"(?s)source\s*===\s*[\"']demo[\"'].*MORE")

        app_source = (REPO_ROOT / "mvp/app.py").read_text(encoding="utf-8")
        demo_route = app_source.split('if route == "/api/runs/demo":', 1)[1].split(
            'elif route == "/api/runs/upload":', 1
        )[0]
        self.assertIn("DEMO_SIGN", demo_route)
        self.assertNotIn('payload.get("sign_name"', demo_route)


@unittest.skipUnless(
    os.environ.get("KINDERFLOW_RUN_INTEGRATION") == "1",
    "Set KINDERFLOW_RUN_INTEGRATION=1 to process the private local demo reference.",
)
class DemoIntegrationTest(unittest.TestCase):
    def test_demo_reference_runs_through_real_pipeline(self) -> None:
        run_dir, manifest = pipeline.prepare_run(
            pipeline.DEMO_SIGN_NAME,
            "Snack time / playtime",
            "Validated reference",
            "more.mp4",
            "demo_reference",
        )
        self.assertEqual(manifest["sign"]["name"], "MORE")
        self.assertEqual(manifest["sign"]["sign_id"], pipeline.DEMO_SIGN_ID)
        self.assertEqual(manifest["source"]["reference_id"], "demo_more_reference")
        pipeline.store_demo(run_dir)
        result = pipeline.run_pipeline(run_dir, manifest)
        self.assertEqual(result["state"], "complete")
        self.assertEqual(result["metrics"]["frames_analysed"], 285)
        self.assertTrue(
            (run_dir / "output/previews/reference_landmarks.mp4").exists()
        )
        self.assertTrue(
            (run_dir / "output/previews/reference_landmarks_browser.mp4").exists()
        )
        self.assertEqual(result["technical_status"], "Review needed")
        self.assertEqual(result["processing"]["preview"]["codec"], "H.264")


if __name__ == "__main__":
    unittest.main()
