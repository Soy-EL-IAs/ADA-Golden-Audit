import unittest
from unittest.mock import patch

from ada_app.character_capabilities import build_character_catalog


class CharacterCatalogTests(unittest.TestCase):
    def test_visible_stock_asset_becomes_cover_and_removed_hero_is_ignored(self):
        characters = {"Chun-Li": {"name": "Chun-Li", "franchise": "street_fighter"}}
        assets = [
            {
                "asset_id": "removed-hero",
                "character": "Chun-Li",
                "full_image_path": "removed.png",
                "is_visible_library_asset": False,
                "creation_mode": "scene",
            },
            {
                "asset_id": "stock-cover",
                "character": "Chun-Li",
                "full_image_path": "stock.png",
                "is_visible_library_asset": True,
                "creation_mode": "stock",
                "agent_rating": 8.0,
                "generated_at": "2026-08-25T13:00:00",
            },
        ]
        with patch("ada_app.character_capabilities._reference_from_manifest", return_value=""):
            catalog = build_character_catalog(characters, assets, {"Chun-Li": "removed-hero"})

        chun_li = next(item for item in catalog if item.get("registered"))
        self.assertEqual(chun_li["reference_asset_id"], "stock-cover")
        self.assertEqual(chun_li["cover_source"], "stock")
        self.assertEqual(chun_li["stock_image_count"], 1)
        self.assertTrue(chun_li["stale_hero"])

    def test_catalog_includes_recommended_characters_not_yet_registered(self):
        with patch("ada_app.character_capabilities._reference_from_manifest", return_value=""):
            catalog = build_character_catalog({"2B": {"name": "2B"}}, [], {})

        self.assertTrue(next(item for item in catalog if item["name"] == "2B")["registered"])
        self.assertFalse(next(item for item in catalog if item["name"] == "Ada Wong")["registered"])


if __name__ == "__main__":
    unittest.main()
