from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from character_profile import CharacterProfileDatabase
from run_full_pipeline import FullPipeline


class CharacterProfileSafetyTests(unittest.TestCase):
    def test_known_local_character_resolves(self) -> None:
        profile = CharacterProfileDatabase().get_character_profile("2B", "NieR:Automata")
        self.assertTrue(profile["character_profile_used"])
        self.assertEqual(profile["matched_tag"], "2b_(nier:automata)")

    def test_missing_profile_fails_before_premise_or_comfy(self) -> None:
        test_tmp = ROOT / "data" / "tmp" / "tests"
        test_tmp.mkdir(parents=True, exist_ok=True)
        temporary = test_tmp / f"ada-profile-safety-{uuid.uuid4().hex}"
        temporary.mkdir()
        self.addCleanup(shutil.rmtree, temporary, True)
        run_dir = temporary / "missing_profile"
        pipeline = FullPipeline(
            run_dir,
            character="ADA_TEST_CHARACTER_DOES_NOT_EXIST_987654",
            version=None,
        )
        pipeline.orchestrator.create(
            "missing_profile",
            character=pipeline.character,
            version=None,
            review_policy="strict",
        )

        with patch.object(pipeline, "_premise", side_effect=AssertionError("premise must not run")), \
                patch("run_full_pipeline.submit", side_effect=AssertionError("ComfyUI must not run")):
            evidence = pipeline.run()

        state = evidence["state"]
        self.assertEqual(state["stage"], "FAILED")
        self.assertEqual(state["error"]["component"], "character_profile")
        self.assertIn("Generation was not started", state["error"]["message"])
        profile = json.loads((run_dir / "character_profile.json").read_text(encoding="utf-8"))
        self.assertFalse(profile["character_profile_used"])
        self.assertEqual(profile["reason"], "not_found")


if __name__ == "__main__":
    unittest.main()
