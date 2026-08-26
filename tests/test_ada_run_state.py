from __future__ import annotations

import sys
import shutil
import unittest
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ada_run_state import AdaRunState


class AdaRunStateTests(unittest.TestCase):
    def workspace(self) -> Path:
        path = ROOT / "tests" / f"runtime_{uuid.uuid4().hex}"
        path.mkdir()
        self.addCleanup(shutil.rmtree, path, True)
        return path

    def test_persists_unique_runtime_seeds_and_stages(self) -> None:
        run = AdaRunState(self.workspace() / "run_001")
        run.create("run_001", character="2B", version="NieR:Automata", pipeline="specialist_image_v1")
        seeds = run.allocate_seeds(["a", "b"])
        flattened = [seed for pair in seeds.values() for seed in pair.values()]
        self.assertEqual(len(flattened), len(set(flattened)))
        run.advance("PREMISES_READY", artifacts={"premises": "premises.jsonl"})
        restored = AdaRunState(run.run_dir).read()
        self.assertEqual(restored["stage"], "PREMISES_READY")
        self.assertEqual(restored["artifacts"]["premises"], "premises.jsonl")

    def test_terminal_state_cannot_advance(self) -> None:
        run = AdaRunState(self.workspace() / "run_002")
        run.create("run_002", character="2B", version=None, pipeline="specialist_image_v1")
        run.advance("COMPLETE")
        with self.assertRaises(ValueError):
            run.advance("FAILED")


if __name__ == "__main__":
    unittest.main()
