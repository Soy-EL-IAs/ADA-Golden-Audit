from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from agent_contracts import ContractError, response_format, validate_contract


class AgentContractTests(unittest.TestCase):
    def test_premise_contract_accepts_arrays(self) -> None:
        value = {
            "id": "case_01",
            "category": "closeup",
            "premise": "A visible event.",
            "preserved_elements": ["identity", "trigger"],
            "risk_notes": ["The trigger may become unclear."],
        }
        self.assertIs(validate_contract("premise_spec_v1", value), value)

    def test_premise_contract_rejects_string_risk_notes(self) -> None:
        value = {
            "id": "case_01",
            "category": "closeup",
            "premise": "A visible event.",
            "preserved_elements": ["identity", "trigger"],
            "risk_notes": "This must be an array.",
        }
        with self.assertRaisesRegex(ContractError, "risk_notes must be an array"):
            validate_contract("premise_spec_v1", value)

    def test_response_format_is_strict(self) -> None:
        value = response_format("klein_result_v1")
        self.assertEqual(value["type"], "json_schema")
        self.assertTrue(value["json_schema"]["strict"])


if __name__ == "__main__":
    unittest.main()
