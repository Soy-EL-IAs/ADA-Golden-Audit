from __future__ import annotations

import json
import shutil
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

from ada_app.asset_library import AssetLibrary


ROOT = Path(__file__).resolve().parents[1]


class HardRatingHistoryTests(unittest.TestCase):
    def setUp(self) -> None:
        parent = ROOT / "data" / "tmp" / "tests"
        parent.mkdir(parents=True, exist_ok=True)
        self.temporary = parent / f"hard-rating-{uuid.uuid4().hex}"
        self.temporary.mkdir()
        self.addCleanup(shutil.rmtree, self.temporary, True)

    def test_failed_reevaluation_appends_history_without_replacing_last_success(self) -> None:
        review_path = self.temporary / "asset_review.json"
        review_path.write_text("{}\n", encoding="utf-8")
        library = AssetLibrary.__new__(AssetLibrary)
        library.index = [{"asset_id": "asset-1"}]
        library.reviews = {}
        first = {"evaluation_id": "hard-1", "final_score": 84}
        failed = {"evaluation_id": "hard-2", "error": "worker unavailable"}

        with patch("ada_app.asset_library.REVIEW_PATH", review_path):
            library.save_hard_rating("asset-1", first)
            result = library.save_hard_rating("asset-1", failed, failed=True)

        self.assertEqual(result["hard_rating"], first)
        self.assertEqual(result["hard_rating_history"], [first, failed])
        persisted = json.loads(review_path.read_text(encoding="utf-8"))
        self.assertEqual(persisted["asset-1"]["hard_rating_history"], [first, failed])


if __name__ == "__main__":
    unittest.main()
