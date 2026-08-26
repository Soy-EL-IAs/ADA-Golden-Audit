from __future__ import annotations

import unittest

from scripts.character_tag_resolver import CharacterTagResolver
from scripts.character_taxonomy import classify_tag


class CharacterTagResolverTests(unittest.TestCase):
    def setUp(self) -> None:
        self.resolver = CharacterTagResolver()

    def test_regression_set_resolves_taxonomy_before_discovery(self) -> None:
        cases = {
            "android_18": "android_18",
            "hyuuga_hinata": "hyuuga_hinata",
            "chun-li": "chun-li",
            "kamado_nezuko": "kamado_nezuko",
            "nanally de NTE": "nanally_(nte)",
        }
        for requested, expected in cases.items():
            with self.subTest(requested=requested):
                identity = self.resolver.resolve(requested)
                self.assertIsNotNone(identity)
                self.assertEqual(identity.canonical_tag, expected)
                self.assertTrue(identity.franchise)

    def test_contextual_tags_do_not_become_canonical_outfit(self) -> None:
        self.assertEqual(classify_tag("blonde_hair"), "IDENTITY")
        self.assertEqual(classify_tag("earrings"), "ACCESSORY")
        self.assertEqual(classify_tag("sitting"), "IGNORE")
        self.assertEqual(classify_tag("bikini", group="clothing"), "CONTEXTUAL")


if __name__ == "__main__":
    unittest.main()
