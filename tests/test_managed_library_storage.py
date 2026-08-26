from __future__ import annotations

import hashlib
import shutil
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

from ada_app import managed_assets


ROOT = Path(__file__).resolve().parents[1]


class ManagedLibraryStorageTests(unittest.TestCase):
    def setUp(self) -> None:
        parent = ROOT / "data" / "tmp" / "tests"
        parent.mkdir(parents=True, exist_ok=True)
        self.temporary = parent / f"managed-library-{uuid.uuid4().hex}"
        self.temporary.mkdir()
        self.addCleanup(shutil.rmtree, self.temporary, True)

    def test_adoption_owns_and_deduplicates_pixels_with_original_provenance(self) -> None:
        source = self.temporary / "raw.png"
        source.write_bytes(b"representative-image-bytes")
        assets = self.temporary / "library" / "assets"
        records = self.temporary / "library" / "records"
        with patch.multiple(
            managed_assets,
            ADA_ROOT=self.temporary,
            LIBRARY_ASSETS_ROOT=assets,
            LIBRARY_RECORDS_ROOT=records,
        ):
            first = managed_assets.adopt_library_record({
                "asset_id": "asset::one", "character": "2B",
                "full_image_path": str(source), "thumbnail_path": str(source),
            })
            second = managed_assets.adopt_library_record({
                "asset_id": "asset::two", "character": "2B",
                "full_image_path": str(source), "thumbnail_path": str(source),
            })

        self.assertEqual(first["full_image_path"], second["full_image_path"])
        self.assertEqual(len(list((assets / "sha256").rglob("*.png"))), 1)
        self.assertEqual(len(list(records.glob("*.json"))), 2)
        self.assertEqual(first["storage_provenance"]["original_source_path"], str(source.resolve()))
        self.assertEqual(
            first["storage_provenance"]["sha256"],
            hashlib.sha256(source.read_bytes()).hexdigest(),
        )


if __name__ == "__main__":
    unittest.main()
