from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_klein_jsonl_batch import compile_api
from split_klein_pipeline import compile_illustrious_stage, compile_klein_stage, validate_stage_separation


class SplitPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        workflow = json.loads((ROOT / "workflows" / "legacy" / "illustrious_to_klein_batch_base_ui.json").read_text(encoding="utf-8"))
        cls.prompt = compile_api(workflow)

    def test_workflow_can_pause_between_illustrious_and_klein(self) -> None:
        illustrious = compile_illustrious_stage(self.prompt)
        klein = compile_klein_stage(self.prompt, uploaded_image="AdaRuns/run_001/source.png")
        validate_stage_separation(illustrious, klein)
        self.assertIn("7", illustrious)
        self.assertNotIn("39", illustrious)
        self.assertNotIn("20", illustrious)
        self.assertNotIn("22", illustrious)
        self.assertNotIn("waterfall", json.dumps(illustrious).lower())
        self.assertIn("20", klein)
        self.assertNotIn("22", klein)
        self.assertEqual(klein["900"]["class_type"], "LoadImage")
        self.assertEqual(klein["40"]["inputs"]["pixels"], ["900", 0])
        self.assertNotIn("7", klein)

    def test_illus_retry_recompiles_only_illus_graph(self) -> None:
        attempts = [compile_illustrious_stage(self.prompt) for _ in range(2)]
        self.assertEqual(len(attempts), 2)
        for attempt in attempts:
            self.assertIn("7", attempt)
            self.assertNotIn("20", attempt)
            self.assertNotIn("22", attempt)


if __name__ == "__main__":
    unittest.main()
