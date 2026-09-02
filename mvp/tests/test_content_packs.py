from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[2]
MVP_ROOT = REPO_ROOT / "mvp"
sys.path.insert(0, str(MVP_ROOT))
sys.path.insert(0, str(REPO_ROOT))

import content_packs  # noqa: E402
from content_ops.content_engine import build_dry_run_candidate  # noqa: E402


class ContentPackServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.runs_patch = patch.object(content_packs, "CONTENT_RUNS_ROOT", Path(self.temporary.name))
        self.env_patch = patch.object(content_packs, "load_local_environment", lambda: None)
        self.runs_patch.start()
        self.env_patch.start()
        self.addCleanup(self.runs_patch.stop)
        self.addCleanup(self.env_patch.stop)
        self.addCleanup(self.temporary.cleanup)
        self.source = content_packs.build_content_request("more")
        self.request = {"operation": "GENERATE_CONTENT_PACK", "generation_method": "llm_assisted", "input": self.source}

    def test_dry_run_uses_backend_contract_and_is_not_live(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            result = content_packs.generate_content_pack(self.request)
        self.assertTrue({"schema_version", "run_id", "operation", "state", "source", "generation", "quality_gate", "langsmith", "review", "automatic_publication", "content_pack", "flashcard_handoff", "error"}.issubset(result))
        self.assertEqual(result["state"], "READY_FOR_REVIEW")
        self.assertEqual(result["generation"]["mode"], "DRY_RUN")
        self.assertEqual(result["content_pack"]["generation_mode"], "DRY_RUN")
        self.assertEqual(result["langsmith"]["mode"], "DRY_RUN")
        self.assertTrue(result["quality_gate"]["passed"])
        self.assertFalse(result["automatic_publication"])

    def test_invalid_input_and_missing_context_are_rejected(self) -> None:
        invalid = json.loads(json.dumps(self.request))
        invalid["input"].pop("approved_context")
        with self.assertRaisesRegex(content_packs.ContentPackError, "input failed validation"):
            content_packs.generate_content_pack(invalid)

    def test_modified_source_context_is_rejected(self) -> None:
        invalid = json.loads(json.dumps(self.request))
        invalid["input"]["approved_context"]["family_use"]["en"] = "Invented context"
        with self.assertRaisesRegex(content_packs.ContentPackError, "does not match"):
            content_packs.generate_content_pack(invalid)

    def test_live_mode_records_model_usage_and_trace_state(self) -> None:
        sign = content_packs.find_sign("more")

        def provider(prompt: str, model: str):
            run_id = next(line.split('"')[3] for line in prompt.splitlines() if '"run_id"' in line)
            candidate = build_dry_run_candidate(sign, "llm_assisted", run_id)
            candidate["generation_mode"] = "LIVE"
            return json.dumps(candidate), {"input_tokens": 120, "output_tokens": 80, "total_tokens": 200}, True

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-only", "OPENAI_MODEL": "configured-model"}, clear=True):
            result = content_packs.generate_content_pack(self.request, live_provider=provider)
        self.assertEqual(result["generation"]["mode"], "LIVE")
        self.assertEqual(result["generation"]["model_configuration"], "configured-model")
        self.assertEqual(result["generation"]["token_usage"]["total_tokens"], 200)
        self.assertEqual(result["langsmith"]["mode"], "LIVE")
        self.assertEqual(result["langsmith"]["evaluation_status"], "TRACE_RECORDED_EVALUATION_PENDING")

    def test_missing_live_dependency_uses_labelled_dry_run(self) -> None:
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-only"}, clear=True), patch.object(content_packs, "_live_dependency_available", return_value=False):
            result = content_packs.generate_content_pack(self.request)
        self.assertEqual(result["generation"]["mode"], "DRY_RUN")
        self.assertTrue(any("dependency unavailable" in warning for warning in result["quality_gate"]["warnings"]))

    def test_malformed_live_output_fails_safely(self) -> None:
        def provider(_prompt: str, _model: str):
            return "{bad-json", {}, False

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-only"}, clear=True):
            result = content_packs.generate_content_pack(self.request, live_provider=provider)
        self.assertEqual(result["state"], "REJECTED")
        self.assertFalse(result["quality_gate"]["passed"])
        self.assertEqual(result["error"]["code"], "malformed_model_output")

    def test_unreviewed_run_cannot_create_flashcard_handoff(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            run = content_packs.generate_content_pack(self.request)
        self.assertIsNone(run["flashcard_handoff"])

    def test_approval_is_explicit_idempotent_and_records_generic_actor(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            run = content_packs.generate_content_pack(self.request)
        approved = content_packs.approve_content_pack(run["run_id"])
        repeated = content_packs.approve_content_pack(run["run_id"])
        self.assertEqual(approved, repeated)
        self.assertEqual(approved["review"]["actor_type"], "human_reviewer")
        self.assertEqual(approved["state"], "APPROVED_LOCALLY")
        self.assertIsNotNone(approved["flashcard_handoff"])
        self.assertFalse(approved["automatic_publication"])

    def test_request_changes_removes_flashcard_handoff(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            run = content_packs.generate_content_pack(self.request)
        content_packs.approve_content_pack(run["run_id"])
        changed = content_packs.request_content_changes(run["run_id"])
        self.assertEqual(changed["state"], "CHANGES_REQUESTED")
        self.assertIsNone(changed["flashcard_handoff"])

    def test_restore_creates_new_human_run_without_overwriting_ai_run(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            original = content_packs.generate_content_pack(self.request)
            restored = content_packs.restore_human_copy(original["run_id"])
        self.assertNotEqual(original["run_id"], restored["run_id"])
        self.assertEqual(restored["generation"]["method"], "human")
        self.assertEqual(restored["generation"]["mode"], "NOT_APPLICABLE")
        self.assertEqual(restored["langsmith"]["mode"], "NOT_APPLICABLE")
        self.assertEqual(content_packs.load_content_run(original["run_id"])["generation"]["method"], "llm_assisted")

    def test_run_id_rejects_path_traversal(self) -> None:
        with self.assertRaises(content_packs.ContentPackError):
            content_packs.load_content_run("../../private")


if __name__ == "__main__":
    unittest.main()
