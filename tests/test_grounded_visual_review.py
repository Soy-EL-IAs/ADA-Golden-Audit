import json
import unittest
from pathlib import Path

from scripts.specialist_visual_reviewer import COMPACT_REVIEW_LIMITS_INSTRUCTION, _rated_grounded_review


def _raw(identity_result="PASS", identity_score=9, actual_subjects=1, hard_failures=None):
    return {
        "id": "case_01",
        "stage": "lustify",
        "identity": {"result": identity_result, "score": identity_score, "confidence": 0.95},
        "subject_count": {"expected": 1, "actual": actual_subjects, "result": "PASS" if actual_subjects == 1 else "FAIL"},
        "scores": {"anatomy": 9, "prompt_adherence": 9, "composition": 9, "visual_quality": 9},
        "defects": [],
        "hard_constraint_failures": hard_failures or [],
        "outfit_design_adherence": "Canonical outfit is preserved.",
        "identity_comparison": "Candidate matches the supplied references.",
        "reference_observations": "Canonical identity anchors are visible.",
        "candidate_observations": "Single subject with coherent anatomy.",
        "summary": "Compact grounded review.",
    }


class GroundedVisualReviewTests(unittest.TestCase):
    spec = {"expected_subject_count": 1, "character": {"must_preserve": []}}

    def test_wrong_identity_is_a_hard_gate_even_for_high_quality(self):
        result = _rated_grounded_review(
            _raw(identity_result="FAIL", identity_score=2),
            identifier="case_01", stage="lustify", semantic_spec=self.spec,
        )
        self.assertEqual(result["verdict"], "FAIL")
        self.assertLessEqual(result["agent_rating"], 4.0)
        self.assertTrue(result["identity_failures"])

    def test_extra_subject_is_a_hard_gate(self):
        result = _rated_grounded_review(
            _raw(actual_subjects=2),
            identifier="case_01", stage="lustify", semantic_spec=self.spec,
        )
        self.assertEqual(result["subject_count"]["result"], "FAIL")
        self.assertEqual(result["verdict"], "FAIL")
        self.assertLessEqual(result["agent_rating"], 4.5)

    def test_textual_second_person_claim_cannot_coexist_with_actual_one(self):
        raw = _raw(actual_subjects=1)
        raw["summary"] = "The protagonist is sharing tea with a friend."
        result = _rated_grounded_review(
            raw, identifier="case_01", stage="lustify", semantic_spec=self.spec,
        )
        self.assertEqual(result["subject_count"]["actual"], 2)
        self.assertEqual(result["verdict"], "FAIL")

    def test_locked_requirement_failure_caps_rating(self):
        result = _rated_grounded_review(
            _raw(hard_failures=["Requested action is not visibly performed"]),
            identifier="case_01", stage="lustify", semantic_spec=self.spec,
        )
        self.assertEqual(result["verdict"], "FAIL")
        self.assertLessEqual(result["agent_rating"], 5.0)

    def test_good_grounded_review_remains_high(self):
        result = _rated_grounded_review(
            _raw(), identifier="case_01", stage="lustify", semantic_spec=self.spec,
        )
        self.assertEqual(result["verdict"], "PASS")
        self.assertEqual(result["agent_rating"], 9.0)
        self.assertEqual(result["applied_caps"], [])

    def test_v4_schema_and_prompt_are_strictly_compact(self):
        schema_path = Path(__file__).resolve().parents[1] / "schemas" / "visual_review_v4.schema.json"
        properties = json.loads(schema_path.read_text(encoding="utf-8"))["properties"]
        for name in ("candidate_observations", "reference_observations", "identity_comparison", "outfit_design_adherence", "summary"):
            self.assertGreater(properties[name]["maxLength"], 0)
        for name in ("defects", "hard_constraint_failures"):
            self.assertEqual(properties[name]["maxItems"], 6)
            self.assertEqual(properties[name]["items"]["maxLength"], 160)
        self.assertIn("never repeat", COMPACT_REVIEW_LIMITS_INSTRUCTION)
        self.assertIn("under 50 words", COMPACT_REVIEW_LIMITS_INSTRUCTION)
