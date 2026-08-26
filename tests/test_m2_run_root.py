from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

from ada_app import mission_runner
from scripts.ada_paths import MISSION_RUNS_ROOT


class M2RunRootTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        lab_root = Path(__file__).resolve().parents[1] / "experimental" / "m1_creative_expansion_lab"
        sys.path.insert(0, str(lab_root))
        try:
            spec = importlib.util.spec_from_file_location("ada_m2_run_root_test", lab_root / "run_m2.py")
            if spec is None or spec.loader is None:
                raise RuntimeError("Could not load run_m2.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            cls.run_m2 = module
        finally:
            sys.path.remove(str(lab_root))

    def test_child_and_caller_share_authoritative_mission_runs_root(self) -> None:
        self.assertEqual(self.run_m2.RUNS_ROOT, MISSION_RUNS_ROOT)
        self.assertEqual(mission_runner.RUNS_DIR, MISSION_RUNS_ROOT)

    def test_missing_manifest_failure_is_durable_and_structured(self) -> None:
        run_dir = MISSION_RUNS_ROOT / "golden_missing_manifest_test"
        completed = SimpleNamespace(returncode=0, stdout="child completed", stderr="")
        detail = mission_runner.m2_missing_manifest_detail(run_dir, completed)
        self.assertEqual(detail["error_type"], "M2ManifestMissing")
        self.assertEqual(detail["run_id"], run_dir.name)
        self.assertEqual(detail["exit_code"], 0)
        self.assertEqual(detail["expected_manifest"], str(run_dir / "manifest.json"))
        self.assertIn(str(run_dir), detail["message"])

    def test_compact_parser_accepts_only_matching_concept_id_mapping(self) -> None:
        payload = {
            "concept_01": {"concept_id": "concept_01", "action": "pose"},
            "concept_02": {"concept_id": "concept_02", "action": "turn"},
        }
        parsed = self.run_m2.parse_compact_concepts(json.dumps(payload))
        self.assertEqual([item["concept_id"] for item in parsed["concepts"]], ["concept_01", "concept_02"])

        mismatched = {"concept_01": {"concept_id": "different"}}
        with self.assertRaises(self.run_m2.ExperimentError):
            self.run_m2.parse_compact_concepts(json.dumps(mismatched))

    def test_twelve_concepts_receive_proportional_config_bounded_budget(self) -> None:
        transport = {
            "max_output_tokens": 8000,
            "output_tokens_per_concept": 256,
            "minimum_output_tokens": 1024,
        }
        self.assertEqual(self.run_m2.creative_output_token_budget(12, transport), 3072)
        self.assertEqual(self.run_m2.creative_output_token_budget(40, transport), 8000)

    def test_malformed_response_at_budget_is_explicit_truncation_without_retry(self) -> None:
        response = {
            "output": [{"type": "message", "content": '[{"concept_id":"m1_01"'}],
            "stats": {"total_output_tokens": 3072},
        }
        with self.assertRaisesRegex(
            self.run_m2.CreativeOutputTruncated,
            r"3072/3072 output tokens; no creative retry was attempted",
        ):
            self.run_m2.parse_and_validate_creative_response(
                response, budget=3072, character="Shihouin Yoruichi",
            )


if __name__ == "__main__":
    unittest.main()
