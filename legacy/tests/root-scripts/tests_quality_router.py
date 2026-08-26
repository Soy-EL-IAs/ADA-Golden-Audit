import unittest
from ada_app.quality_router import QualityRouter

class TestQualityRouter(unittest.TestCase):

    def test_case_a_illustrious_approve(self):
        self.assertEqual(QualityRouter.route("illustrious", "PASS"), QualityRouter.ACTION_ADVANCE_TO_KLEIN)
        self.assertEqual(QualityRouter.route("illustrious", "MINOR_DEFECT"), QualityRouter.ACTION_ADVANCE_TO_KLEIN)

    def test_case_b_illustrious_retry(self):
        self.assertEqual(QualityRouter.route("illustrious", "RETRY_ILLUSTRIOUS"), QualityRouter.ACTION_RETRY_ILLUSTRIOUS)
        self.assertEqual(QualityRouter.route("illustrious", "REVIEW"), QualityRouter.ACTION_RETRY_ILLUSTRIOUS)

    def test_case_c_final_retry_klein(self):
        self.assertEqual(QualityRouter.route("klein", "REVIEW"), QualityRouter.ACTION_RETRY_KLEIN)

    def test_case_d_final_retry_illustrious(self):
        self.assertEqual(QualityRouter.route("klein", "RETRY_ILLUSTRIOUS"), QualityRouter.ACTION_RETRY_ILLUSTRIOUS)

    def test_case_e_final_approve(self):
        self.assertEqual(QualityRouter.route("klein", "PASS"), QualityRouter.ACTION_APPROVE)
        self.assertEqual(QualityRouter.route("klein", "MINOR_DEFECT"), QualityRouter.ACTION_APPROVE)

    def test_case_f_reject(self):
        self.assertEqual(QualityRouter.route("illustrious", "REJECT"), QualityRouter.ACTION_REJECT)
        self.assertEqual(QualityRouter.route("klein", "REJECT"), QualityRouter.ACTION_REJECT)

    def test_unknown_fallback(self):
        self.assertEqual(QualityRouter.route("illustrious", "GARBAGE"), QualityRouter.ACTION_REJECT)

if __name__ == '__main__':
    unittest.main()
