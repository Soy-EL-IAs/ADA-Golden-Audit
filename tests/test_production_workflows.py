from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from production_workflows import (
    DANGEROUS_DEFAULTS,
    ILLUSTRIOUS_ONLY_WORKFLOW,
    KLEIN_ONLY_WORKFLOW,
    build_illustrious_workflow,
    build_klein_workflow,
    load_workflow,
    submission_provenance,
    validate_illustrious_workflow,
    validate_klein_workflow,
)
from run_klein_jsonl_batch import main as legacy_combined_main
from ada_app.run_index import RunIndex


class ProductionWorkflowTests(unittest.TestCase):
    def test_active_paths_have_no_incident_demo_defaults(self) -> None:
        active_roots = (ROOT / "workflows", ROOT / "config", ROOT / "ada_app", ROOT / "scripts", ROOT / "ada.py")
        files: list[Path] = []
        for root in active_roots:
            if root.is_file():
                files.append(root)
            elif root.is_dir():
                files.extend(path for path in root.rglob("*") if path.suffix.lower() in {".py", ".json", ".md"})
        for path in files:
            if "legacy" in {part.lower() for part in path.parts}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
            for forbidden in DANGEROUS_DEFAULTS:
                self.assertNotIn(forbidden, text, f"{forbidden!r} found in active path {path}")

    def test_a_illustrious_template_has_no_klein_nodes(self) -> None:
        workflow = load_workflow(ILLUSTRIOUS_ONLY_WORKFLOW)
        validate_illustrious_workflow(workflow)
        text = json.dumps(workflow).lower()
        for forbidden in ("flux-2-klein", "qwen_3_8b", "referencelatent", "loadimage"):
            self.assertNotIn(forbidden, text)

    def test_b_klein_template_has_no_illustrious_nodes(self) -> None:
        workflow = load_workflow(KLEIN_ONLY_WORKFLOW)
        validate_klein_workflow(workflow, expected_input_image="__ADA_APPROVED_ILLUSTRIOUS__")
        text = json.dumps(workflow).lower()
        self.assertNotIn("waiillustrious", text)
        self.assertNotIn("emptylatentimage", text)
        self.assertNotIn("ksampler\"", text)

    def test_c_illustrious_has_one_output_target(self) -> None:
        workflow = build_illustrious_workflow(
            positive_prompt="one adult character", seed=11, width=768, height=1376, output_prefix="test/a/illustrious",
        )
        self.assertEqual([n for n in workflow.values() if n["class_type"] == "SaveImage"], [workflow["7"]])

    def test_d_klein_has_one_output_target(self) -> None:
        workflow = build_klein_workflow(
            input_image="candidate-a.png", positive_prompt="preserve the source", seed=12, output_prefix="test/a/klein",
        )
        self.assertEqual([n for n in workflow.values() if n["class_type"] == "SaveImage"], [workflow["20"]])

    def test_e_no_production_template_has_dangerous_defaults(self) -> None:
        for path in (ILLUSTRIOUS_ONLY_WORKFLOW, KLEIN_ONLY_WORKFLOW):
            text = path.read_text(encoding="utf-8").lower()
            for forbidden in DANGEROUS_DEFAULTS:
                self.assertNotIn(forbidden, text, f"{forbidden!r} found in {path}")

    def test_f_klein_load_image_is_exact_approved_artifact(self) -> None:
        workflow = build_klein_workflow(
            input_image="uploads/run-a/candidate-a.png", positive_prompt="preserve", seed=13, output_prefix="test/a/klein",
        )
        validate_klein_workflow(workflow, expected_input_image="uploads/run-a/candidate-a.png")
        with self.assertRaisesRegex(ValueError, "LoadImage mismatch"):
            validate_klein_workflow(workflow, expected_input_image="uploads/run-b/candidate-b.png")

    def test_g_provenance_identity_is_stable_between_stages(self) -> None:
        identity = dict(mission_id="m1", run_id="r1", concept_id="c1", candidate_id="candidate-1", attempt_id="a1")
        illustrious = submission_provenance(
            **identity, stage="illustrious", workflow_path=ILLUSTRIOUS_ONLY_WORKFLOW, input_asset="prompt.json",
        )
        klein = submission_provenance(
            **identity, stage="klein", workflow_path=KLEIN_ONLY_WORKFLOW, input_asset="illustrious.png",
        )
        for key, value in identity.items():
            self.assertEqual(illustrious[key], value)
            self.assertEqual(klein[key], value)

    def test_h_concurrent_candidates_cannot_exchange_artifacts(self) -> None:
        a = build_klein_workflow(input_image="uploads/a.png", positive_prompt="a", seed=1, output_prefix="a/klein")
        b = build_klein_workflow(input_image="uploads/b.png", positive_prompt="b", seed=2, output_prefix="b/klein")
        self.assertEqual(a["900"]["inputs"]["image"], "uploads/a.png")
        self.assertEqual(b["900"]["inputs"]["image"], "uploads/b.png")
        self.assertNotEqual(a["900"]["inputs"]["image"], b["900"]["inputs"]["image"])

    def test_explicit_future_character_prompt_is_not_a_template_default(self) -> None:
        workflow = build_illustrious_workflow(
            positive_prompt="Chel, explicit user-requested character", seed=14,
            width=768, height=1376, output_prefix="test/explicit/illustrious",
        )
        self.assertIn("Chel", workflow["2"]["inputs"]["text"])
        self.assertNotIn("Chel", ILLUSTRIOUS_ONLY_WORKFLOW.read_text(encoding="utf-8"))

    def test_legacy_combined_runner_cannot_submit(self) -> None:
        with patch.object(sys, "argv", ["run_klein_jsonl_batch.py", "--workflow", "ignored.json"]):
            with self.assertRaisesRegex(RuntimeError, "quarantined"):
                legacy_combined_main()

    def test_library_run_index_excludes_legacy_adapters(self) -> None:
        self.assertEqual([type(adapter).__name__ for adapter in RunIndex().adapters], ["M2CreativeAdapter"])


if __name__ == "__main__":
    unittest.main()
