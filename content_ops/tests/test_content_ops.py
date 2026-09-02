from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from content_ops.content import resolve_content
from content_ops.domain import InvalidTransition, transition_state
from content_ops.golden_set import build_domain_package, evaluate_golden_set, load_json, verify_manifest_provenance, CONTENT_ROOT
from content_ops.policy import check_content_quality, evaluate_package
from content_ops.provenance import append_event, build_publication_package, sha256_file


class StateMachineTests(unittest.TestCase):
    def test_valid_transitions(self) -> None:
        self.assertEqual(transition_state("publication", "DRAFT", "READY_FOR_HUMAN_REVIEW"), "READY_FOR_HUMAN_REVIEW")
        self.assertEqual(transition_state("publication", "APPROVED", "PUBLISHED"), "PUBLISHED")

    def test_invalid_transition_is_rejected(self) -> None:
        with self.assertRaises(InvalidTransition):
            transition_state("publication", "DRAFT", "PUBLISHED")


class PolicyFailureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.package = build_domain_package("more")

    def test_missing_hand_review_blocks_publication(self) -> None:
        result = evaluate_package(self.package)
        self.assertIn("Sign-specific hand pose has not completed human review.", result["blocking_reasons"])

    def test_pending_artwork_blocks_publication(self) -> None:
        result = evaluate_package(self.package)
        self.assertIn("Illustration artwork is not ready.", result["blocking_reasons"])

    def test_cv_fail_blocks_publication(self) -> None:
        self.package["technical"]["state"] = "FAIL"
        result = evaluate_package(self.package)
        self.assertIn("Technical state is not acceptable for human publication review.", result["blocking_reasons"])

    def test_missing_required_content_fails_gate(self) -> None:
        self.package["content_package"]["family_guidance"] = {}
        result = check_content_quality(self.package)
        self.assertFalse(result["passed"])

    def test_biomechanical_wording_fails_gate(self) -> None:
        self.package["content_package"]["family_guidance"] = {"en": "Rotate the wrist.", "es": "Gira la muñeca."}
        result = check_content_quality(self.package)
        self.assertFalse(result["passed"])

    def test_publication_without_human_approval_is_blocked(self) -> None:
        self.package["technical"]["state"] = "PASS"
        self.package["content_package"]["state"] = "APPROVED"
        self.package["visual_package"].update({"state": "READY", "illustration_status": "READY", "character_asset": "character.svg", "hand_pose_asset": "more.svg", "hand_review_status": "REVIEWED"})
        self.package["publication_package"]["publication_status"] = "APPROVED"
        result = evaluate_package(self.package)
        self.assertIn("Explicit human publication approval is missing.", result["blocking_reasons"])

    def test_llm_failure_does_not_corrupt_approved_human_content(self) -> None:
        existing = copy.deepcopy(self.package["content_package"])
        existing.update({"state": "APPROVED", "generation_method": "human"})
        resolved = resolve_content(existing, proposed={"family_guidance": "changed"}, llm_error="timeout")
        self.assertEqual(resolved, existing)


class ProvenanceAndIdempotencyTests(unittest.TestCase):
    def test_manifest_hashes_match_current_local_artifacts(self) -> None:
        manifest = load_json(CONTENT_ROOT / "signs/more/manifest.json")
        result = verify_manifest_provenance(manifest)
        self.assertTrue(result["passed"])

    def test_repeated_build_reuses_same_package_identity(self) -> None:
        package = build_domain_package("more")
        package["quality_gate"] = evaluate_package(package)
        with tempfile.TemporaryDirectory() as directory:
            first = build_publication_package(package, directory)
            second = build_publication_package(package, directory)
            self.assertEqual(first["package_id"], second["package_id"])
            self.assertEqual(sorted(path.name for path in Path(directory).iterdir()), ["content.json", "library_item.json", "manifest.json", "review.json", "visual.json"])

    def test_provenance_reference_remains_stable(self) -> None:
        package = build_domain_package("more")
        with tempfile.TemporaryDirectory() as directory:
            manifest = build_publication_package(package, directory)
            self.assertEqual(manifest["source_reference"], package["sign"]["source_reference"])
            self.assertEqual(manifest["technical_evidence_reference"], package["technical"]["evidence_reference"])

    def test_modifying_artifact_changes_hash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "artifact.txt"
            path.write_text("one", encoding="utf-8")
            first = sha256_file(path)
            path.write_text("two", encoding="utf-8")
            self.assertNotEqual(first, sha256_file(path))

    def test_audit_events_append_and_duplicate_id_is_idempotent(self) -> None:
        event = {"event_id": "evt_test", "timestamp": "2026-09-02T00:00:00Z", "sign_id": "more", "version": "v1", "event_type": "QUALITY_GATE_FAILED", "actor_type": "system", "metadata": {}}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            self.assertTrue(append_event(path, event))
            second = dict(event, event_id="evt_test_2")
            self.assertTrue(append_event(path, second))
            self.assertFalse(append_event(path, event))
            self.assertEqual(len(path.read_text().splitlines()), 2)


class GoldenSetTests(unittest.TestCase):
    def test_five_sign_set_has_blocked_library_states(self) -> None:
        report = evaluate_golden_set()
        self.assertEqual(len(report["results"]), 5)
        self.assertTrue(all(item["schema"] == "PASS" for item in report["results"]))
        self.assertTrue(all(item["library"] == "Blocked" for item in report["results"]))


if __name__ == "__main__":
    unittest.main()
