import unittest

from ada_app.asset_library import (
    collection_display_name,
    humanize_collection_id,
    is_visible_library_asset,
    summarize_visible_collections,
    visible_library_assets,
)


def _asset(asset_id, collection, character, **overrides):
    asset = {
        "asset_id": asset_id,
        "franchise": collection,
        "collection_id": collection,
        "character": character,
        "library_status": "UNREVIEWED",
        "hidden_from_default_gallery": False,
    }
    asset.update(overrides)
    return asset


class LibraryVisibilityTests(unittest.TestCase):
    def test_visible_library_assets_excludes_removed_states_without_touching_records(self):
        active = _asset("active", "neverness_to_everness", "Nanally")
        rejected = _asset("rejected", "neverness_to_everness", "Nanally", library_status="REJECTED")
        hidden = _asset("hidden", "neverness_to_everness", "Nanally", hidden_from_default_gallery=True)
        soft_deleted = _asset("soft", "neverness_to_everness", "Nanally", soft_deleted=True)
        removed = _asset("removed", "neverness_to_everness", "Nanally", removed_at="2026-08-25T00:00:00Z")
        assets = [active, rejected, hidden, soft_deleted, removed]

        self.assertEqual(visible_library_assets(assets), [active])
        self.assertTrue(is_visible_library_asset(active))
        self.assertEqual(len(assets), 5)

    def test_collection_summary_counts_only_visible_images_and_unique_visible_characters(self):
        assets = [
            _asset("n1", "neverness_to_everness", "Nanally"),
            _asset("n2", "neverness_to_everness", "Nanally"),
            _asset("n3", "neverness_to_everness", "Another Character"),
            _asset("n4", "neverness_to_everness", "Rejected Character", library_status="REJECTED"),
            _asset("m1", "mushoku_tensei", "Ghislaine", soft_deleted=True),
        ]
        summaries = summarize_visible_collections(assets)

        self.assertEqual(summaries["neverness_to_everness"]["display_name"], "Neverness to Everness")
        self.assertEqual(summaries["neverness_to_everness"]["character_count"], 2)
        self.assertEqual(summaries["neverness_to_everness"]["total_images"], 3)
        self.assertNotIn("Rejected Character", summaries["neverness_to_everness"]["characters"])
        self.assertNotIn("mushoku_tensei", summaries)

    def test_collection_names_prefer_metadata_and_humanize_slug_as_fallback(self):
        self.assertEqual(collection_display_name(
            "custom_slug", {"franchise_display_name": "Official Collection Name"}
        ), "Official Collection Name")
        self.assertEqual(humanize_collection_id("neverness_to_everness"), "Neverness to Everness")
        self.assertEqual(humanize_collection_id("naruto_(series)"), "Naruto (Series)")
        self.assertEqual(humanize_collection_id("kimetsu_no_yaiba"), "Kimetsu no Yaiba")
        self.assertEqual(humanize_collection_id("NieR:Automata"), "NieR:Automata")


if __name__ == "__main__":
    unittest.main()
