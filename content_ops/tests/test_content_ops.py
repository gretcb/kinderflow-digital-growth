from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from content_ops.content import resolve_content
from content_ops.content_engine import (
    approve_content_locally,
    build_demo_report,
    build_dry_run_candidate,
    content_input_from_sign,
    prepare_flashcard_handoff,
    validate_content_input,
    validate_generated_output,
)
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


class ContentEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        payload = load_json(Path(__file__).parents[2] / "prototype/data/signs.json")
        self.sign = payload["signs"][0]
        self.source = content_input_from_sign(self.sign)

    def test_valid_structured_input(self) -> None:
        self.assertTrue(validate_content_input(self.source)["passed"])

    def test_missing_approved_context_is_rejected(self) -> None:
        source = copy.deepcopy(self.source)
        source.pop("approved_context")
        result = validate_content_input(source)
        self.assertFalse(result["passed"])
        self.assertIn("approved_context", {item["check"] for item in result["failed_checks"]})

    def test_malformed_output_is_rejected_cleanly(self) -> None:
        candidate, result = validate_generated_output("{not-json", self.source)
        self.assertIsNone(candidate)
        self.assertFalse(result["passed"])
        self.assertEqual(result["failed_checks"][0]["check"], "valid_json")

    def test_movement_instructions_are_rejected(self) -> None:
        candidate = build_dry_run_candidate(self.sign)
        candidate["family_guidance"]["en"] = "Rotate the wrist before snack time."
        _, result = validate_generated_output(candidate, self.source)
        self.assertFalse(result["passed"])
        self.assertIn("biomechanics_content", {item["check"] for item in result["failed_checks"]})

    def test_nested_biomechanics_field_is_rejected(self) -> None:
        candidate = build_dry_run_candidate(self.sign)
        candidate["flashcard_copy"]["movement_steps"] = []
        _, result = validate_generated_output(candidate, self.source)
        self.assertFalse(result["passed"])
        self.assertIn("biomechanics_fields", {item["check"] for item in result["failed_checks"]})

    def test_unsupported_claim_is_rejected(self) -> None:
        candidate = build_dry_run_candidate(self.sign)
        candidate["family_message"]["en"] = "This will accelerate language development."
        _, result = validate_generated_output(candidate, self.source)
        self.assertFalse(result["passed"])
        self.assertIn("unsupported_claim", {item["check"] for item in result["failed_checks"]})

    def test_sign_correctness_claim_is_rejected(self) -> None:
        candidate = build_dry_run_candidate(self.sign)
        candidate["family_message"]["en"] = "This proves the sign is correct."
        _, result = validate_generated_output(candidate, self.source)
        self.assertFalse(result["passed"])
        self.assertIn("sign_correctness_claim", {item["check"] for item in result["failed_checks"]})

    def test_input_biomechanics_are_rejected(self) -> None:
        source = copy.deepcopy(self.source)
        source["approved_context"]["family_use"]["en"] = "Rotate both hands."
        result = validate_content_input(source)
        self.assertFalse(result["passed"])
        self.assertIn("input_biomechanics", {item["check"] for item in result["failed_checks"]})

    def test_extra_output_field_is_rejected(self) -> None:
        candidate = build_dry_run_candidate(self.sign)
        candidate["confidence"] = 0.99
        _, result = validate_generated_output(candidate, self.source)
        self.assertFalse(result["passed"])
        self.assertIn("unsupported_fields", {item["check"] for item in result["failed_checks"]})

    def test_gate_is_deterministic_and_dry_run_is_not_live(self) -> None:
        candidate = build_dry_run_candidate(self.sign)
        first = validate_generated_output(candidate, self.source)[1]
        second = validate_generated_output(candidate, self.source)[1]
        self.assertEqual(first, second)
        self.assertEqual(candidate["generation_mode"], "DRY_RUN")
        self.assertFalse(candidate["automatic_publication"])

    def test_generation_does_not_mutate_human_source(self) -> None:
        original = copy.deepcopy(self.sign)
        build_dry_run_candidate(self.sign)
        self.assertEqual(self.sign, original)

    def test_unreviewed_content_cannot_reach_flashcard_handoff(self) -> None:
        with self.assertRaises(ValueError):
            prepare_flashcard_handoff(build_dry_run_candidate(self.sign))

    def test_explicit_local_review_enables_limited_handoff(self) -> None:
        approved = approve_content_locally(build_dry_run_candidate(self.sign), "explicit_demo_approval")
        handoff = prepare_flashcard_handoff(approved)
        self.assertEqual(handoff["review_status"], "APPROVED")
        self.assertNotIn("automatic_publication", handoff)
        self.assertNotIn("teacher_message", handoff)

    def test_all_five_signs_use_same_operation_contract(self) -> None:
        report = build_demo_report(Path(__file__).parents[2] / "prototype/data/signs.json")
        self.assertEqual(report["operation"], "GENERATE_CONTENT_PACK")
        self.assertEqual(len(report["results"]), 5)
        self.assertTrue(all(item["deterministic_quality_gate"]["passed"] for item in report["results"]))
        self.assertTrue(all(item["langsmith"]["trace_status"] == "NOT_SENT" for item in report["results"]))


class FlashcardIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = Path(__file__).parents[2]

    def test_founder_selected_open_peeps_atoms_are_runtime_enabled_with_provenance(self) -> None:
        inventory = load_json(self.repo / "assets/flashcards/open_peeps/candidates.json")
        modular = load_json(self.repo / "assets/flashcards/open_peeps/modular_inventory.json")
        provenance = load_json(self.repo / "assets/flashcards/open_peeps/provenance.json")
        self.assertEqual(inventory["licence_status"], "FOUNDER_VERIFIED_CC0")
        self.assertTrue(inventory["source_library_runtime_use"])
        self.assertLessEqual(len(inventory["candidates"]), 3)
        self.assertTrue(all(item["status"] == "IN_USE_FOR_INTERNAL_VISUAL_REVIEW" for item in inventory["candidates"]))
        self.assertFalse(modular["compatibility_findings"]["direct_interchangeability"])
        self.assertTrue(modular["runtime_dependency"])
        self.assertEqual(provenance["licence"], "CC0")
        self.assertEqual(len(provenance["selected_components"]), 3)

    def test_runtime_does_not_reference_ignored_source_library(self) -> None:
        runtime_files = list((self.repo / "prototype").glob("*.html")) + list((self.repo / "prototype").glob("*.js")) + list((self.repo / "prototype").glob("*.css"))
        self.assertTrue(runtime_files)
        self.assertFalse(any("source_libraries" in path.read_text(encoding="utf-8") for path in runtime_files))

    def test_one_flashcard_renderer_and_attached_sign_lockup(self) -> None:
        html = (self.repo / "prototype/flashcards.html").read_text(encoding="utf-8")
        self.assertEqual(html.count('class="flashcard-output"'), 1)
        self.assertIn('class="flashcard-visual-unit"', html)
        self.assertIn('class="flashcard-sign-lockup"', html)
        builder_js = (self.repo / "prototype/flashcards.js").read_text(encoding="utf-8")
        print_js = (self.repo / "prototype/print-card.js").read_text(encoding="utf-8")
        self.assertIn("print-card.html", builder_js)
        self.assertIn("window.print()", print_js)

    def test_all_five_signs_have_one_bilingual_print_contract(self) -> None:
        signs = load_json(self.repo / "prototype/data/signs.json")["signs"]
        self.assertEqual(len(signs), 5)
        self.assertEqual({item["sign_id"] for item in signs}, {"more", "eat", "water", "all_done", "help"})
        for sign in signs:
            for field in ("routine", "short_family_guidance", "try_it_during"):
                self.assertTrue(sign[field]["en"].strip())
                self.assertTrue(sign[field]["es"].strip())
            self.assertIn("print_readiness", sign)

    def test_family_card_never_receives_governance_metadata(self) -> None:
        approved = approve_content_locally(build_dry_run_candidate(load_json(self.repo / "prototype/data/signs.json")["signs"][0]), "explicit_demo_approval")
        handoff = prepare_flashcard_handoff(approved)
        forbidden = {"human_review", "automatic_publication", "teacher_message", "family_message", "generation_mode"}
        self.assertFalse(forbidden.intersection(handoff))

    def test_more_pose_package_is_explicitly_blocked(self) -> None:
        package = load_json(self.repo / "assets/flashcards/hand_pose_references/more/reference_package.json")
        self.assertEqual(package["target_svg_slot"]["status"], "NOT_CREATED")
        self.assertEqual(package["library_readiness"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
