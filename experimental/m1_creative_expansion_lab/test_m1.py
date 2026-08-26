from __future__ import annotations

import copy
import unittest

from .run_m1 import extract_sections, temporal_leakage, validate_output


def valid_output() -> dict:
    concepts = []
    for index in range(1, 13):
        concepts.append({
            "concept_id": f"m1_2b_{index:02d}",
            "snapshot": f"2B walks through distinct space {index}, holding one object in a frozen stride.",
            "visual_hook": f"Distinct silhouette {index}",
            "provocative_mechanism": f"Non-explicit wardrobe tension {index}",
            "composition_intent": f"Full-body diagonal framing {index}",
            "diversity_signature": {
                "setting": f"setting {index}",
                "framing": f"framing {index}",
                "attitude": f"attitude {index}",
                "visual_emphasis": f"emphasis {index}",
            },
        })
    return {"concepts": concepts}


class M1Tests(unittest.TestCase):
    def test_valid_exact_twelve_allows_action_verbs(self) -> None:
        value = valid_output()
        validate_output(value)
        self.assertEqual([], temporal_leakage(value))

    def test_rejects_wrong_count(self) -> None:
        value = valid_output()
        value["concepts"].pop()
        with self.assertRaisesRegex(RuntimeError, "exactly 12"):
            validate_output(value)

    def test_rejects_temporal_sequence(self) -> None:
        value = valid_output()
        value["concepts"][0]["snapshot"] += " Then she leaves."
        with self.assertRaisesRegex(RuntimeError, "Temporal/video leakage"):
            validate_output(value)

    def test_rejects_future_consequence(self) -> None:
        value = valid_output()
        value["concepts"][1]["visual_hook"] = "The fabric will fall later"
        findings = temporal_leakage(value)
        self.assertTrue(any(item["rule"] == "future" for item in findings))

    def test_rejects_bare_after_retrospective(self) -> None:
        value = valid_output()
        value["concepts"][0]["snapshot"] = "2B adjusts her dress after it caught on equipment."
        with self.assertRaisesRegex(RuntimeError, "Temporal/video leakage"):
            validate_output(value)

    def test_rejects_future_intent(self) -> None:
        value = valid_output()
        value["concepts"][0]["snapshot"] = "2B draws back her arm to strike a punching bag."
        with self.assertRaisesRegex(RuntimeError, "Temporal/video leakage"):
            validate_output(value)

    def test_rejects_id_drift(self) -> None:
        value = valid_output()
        value["concepts"][4]["concept_id"] = "wrong"
        with self.assertRaisesRegex(RuntimeError, "Concept IDs"):
            validate_output(value)

    def test_extracts_only_requested_markdown_section(self) -> None:
        source = "# Root\nintro\n## A\na\n### Child\nc\n## B\nb\n# End\ne"
        self.assertEqual("## A\na\n### Child\nc", extract_sections(source, ("## A",)))


if __name__ == "__main__":
    unittest.main()
