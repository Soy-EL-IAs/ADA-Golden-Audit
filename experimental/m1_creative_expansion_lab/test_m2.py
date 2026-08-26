from __future__ import annotations

import unittest

from .run_m1 import validate_structure
from .run_m2 import proposal_records, supports_reasoning_parameter


def concept(identifier: str, snapshot: str) -> dict:
    return {
        "concept_id": identifier,
        "snapshot": snapshot,
        "visual_hook": "hook",
        "provocative_mechanism": "mechanism",
        "composition_intent": "composition",
        "diversity_signature": {
            "setting": identifier,
            "framing": identifier,
            "attitude": identifier,
            "visual_emphasis": identifier,
        },
    }


class M2Tests(unittest.TestCase):
    def test_records_semantic_fail_without_discarding_raw_proposal(self) -> None:
        value = {"concepts": [concept(f"m1_2b_{index:02d}", "One frozen visible action.") for index in range(1, 13)]}
        value["concepts"][0]["snapshot"] = "2B adjusts her dress after it caught on equipment."
        validate_structure(value)
        records = proposal_records(value, character="2B", model="fast")
        self.assertEqual("FAIL", records[0]["status"])
        self.assertEqual("PASS", records[1]["status"])
        self.assertEqual(value["concepts"][0], records[0]["proposal"])

    def test_reasoning_parameter_capability_detection(self) -> None:
        inventory = {"models": [{"key": "fast", "capabilities": {}}, {"key": "strong", "capabilities": {"reasoning": {"allowed_options": ["off", "on"]}}}]}
        self.assertFalse(supports_reasoning_parameter(inventory, "fast"))
        self.assertTrue(supports_reasoning_parameter(inventory, "strong"))


if __name__ == "__main__":
    unittest.main()
