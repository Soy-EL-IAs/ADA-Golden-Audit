import unittest
import json
from ada_app.pilot_runner import validate_integrity

class TestContamination(unittest.TestCase):
    def test_tifa_with_2b_contamination(self):
        char_profile = {"name": "Tifa Lockhart"}
        premise_spec = {
            "id": "m1_2b_01",
            "premise": "Tifa tries to pour a beer behind the Seventh Heaven bar.",
            "scene_requirements": ["2B is visibly wedged inside the open wardrobe"]
        }
        prop = {"concept_id": "m1_2b_01"}
        
        with self.assertRaises(ValueError) as ctx:
            validate_integrity("m1_2b_01", premise_spec, char_profile, prop)
        
        self.assertIn("CROSS_CANDIDATE_CONTAMINATION", str(ctx.exception))
        self.assertIn("2b", str(ctx.exception))

    def test_clean_tifa(self):
        char_profile = {"name": "Tifa Lockhart"}
        premise_spec = {
            "id": "tifa_001",
            "premise": "Tifa tries to pour a beer behind the Seventh Heaven bar.",
            "scene_requirements": ["bar counter", "expanding foam"]
        }
        prop = {"concept_id": "tifa_001"}
        
        # Should not raise
        validate_integrity("tifa_001", premise_spec, char_profile, prop)

if __name__ == '__main__':
    unittest.main()
