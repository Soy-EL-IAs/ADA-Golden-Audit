from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from specialist_orchestrator import _character_name, _identity_tags, build_deterministic_klein_prompt


class KleinPromptCompilerTests(unittest.TestCase):
    def test_identity_data_adds_valid_preservation_sentence(self) -> None:
        profile = {"requested_character": "2B", "characteristics": ["short hair", "blindfold"]}
        premise = {"identity_elements": []}
        prompt = build_deterministic_klein_prompt(
            character_name=_character_name(profile, premise),
            identity_tags=_identity_tags(profile, premise),
            defects=[],
        )
        self.assertIn("hairstyle, outfit, short hair, blindfold.", prompt)

    def test_empty_identity_data_omits_identity_sentence(self) -> None:
        prompt = build_deterministic_klein_prompt(character_name=None, identity_tags=[], defects=[])
        self.assertNotIn("Preserve the character's .", prompt)
        self.assertNotIn("'s .", prompt)
        self.assertNotIn("identity details: .", prompt)

    def test_never_emits_empty_possessive_sentence(self) -> None:
        prompt = build_deterministic_klein_prompt(character_name="", identity_tags=["blindfold"], defects=[])
        self.assertIn("hairstyle, outfit, blindfold.", prompt)
        self.assertNotIn("'s ", prompt)


if __name__ == "__main__":
    unittest.main()
