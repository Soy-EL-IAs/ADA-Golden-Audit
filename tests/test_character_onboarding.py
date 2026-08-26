from __future__ import annotations

import json
import asyncio
import shutil
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

from ada_app.character_onboarding import (
    CharacterBootstrapError,
    CharacterBootstrapService,
    registered_character_name,
)
from ada_app.command_parser import parse_command

ROOT = Path(__file__).resolve().parents[1]


class FakeProfiles:
    def __init__(self, found: bool = True) -> None:
        self.found = found
        self.calls = 0

    def get_character_profile(self, character: str, version: str | None = None):
        self.calls += 1
        if not self.found:
            return {
                "character_profile_used": False,
                "matched_tag": None,
                "reason": "not_found",
            }
        return {
            "character_profile_used": True,
            "matched_tag": "ghislaine_dedoldia",
            "copyright": ["mushoku_tensei"],
            "characteristics": ["cat_ears", "red_eyes"],
            "clothing": ["jacket"],
        }


class FakeCache:
    def __init__(self, refs_root: Path, mode: str = "usable") -> None:
        self.refs_root = refs_root
        self.mode = mode
        self.calls = 0

    def cache(self, character: str, version: str | None = None):
        self.calls += 1
        if self.mode == "error":
            raise RuntimeError("SearXNG unavailable")
        if self.mode == "unusable":
            return {"usable": False, "status": "insufficient_refs"}

        directory = self.refs_root / "ghislaine_dedoldia" / "default"
        refs_dir = directory / "refs"
        refs_dir.mkdir(parents=True, exist_ok=True)
        refs = []
        for index in (1, 2):
            ref = refs_dir / f"ref_{index:02d}.jpg"
            ref.write_bytes(b"reference")
            refs.append({"file": f"refs/{ref.name}"})
        manifest_path = directory / "manifest.json"
        manifest_path.write_text(
            json.dumps({
                "character": character,
                "version": version,
                "usable": True,
                "refs": refs,
            }),
            encoding="utf-8",
        )
        return {"usable": True, "manifest": str(manifest_path)}


class CharacterOnboardingTests(unittest.TestCase):
    def setUp(self) -> None:
        # Keep test artifacts out of the workspace so a previous interrupted
        # bootstrap cannot leave an ACL-locked directory behind.
        test_tmp = ROOT / "data" / "tmp" / "tests"
        test_tmp.mkdir(parents=True, exist_ok=True)
        self.temporary = test_tmp / f"ada-character-onboarding-{uuid.uuid4().hex}"
        self.temporary.mkdir()
        self.addCleanup(shutil.rmtree, self.temporary, True)
        self.characters_path = self.temporary / "data" / "characters" / "catalog.json"
        self.characters_path.parent.mkdir(parents=True)
        self.characters_path.write_text("{}\n", encoding="utf-8")
        self.refs_root = self.temporary / "data" / "references"

    def service(self, profiles=None, cache=None) -> CharacterBootstrapService:
        return CharacterBootstrapService(
            characters_path=self.characters_path,
            refs_root=self.refs_root,
            profiles=profiles or FakeProfiles(),
            cache=cache or FakeCache(self.refs_root),
        )

    def test_success_registers_only_after_profile_and_usable_manifest(self) -> None:
        result = self.service().bootstrap("Ghislaine Dedoldia")

        self.assertEqual(result["status"], "registered")
        registered = json.loads(self.characters_path.read_text(encoding="utf-8"))
        entry = registered["Ghislaine Dedoldia"]
        self.assertEqual(entry["canonical_tag"], "ghislaine_dedoldia")
        self.assertEqual(entry["refs_manifest"], "data/references/ghislaine_dedoldia/default/manifest.json")
        self.assertEqual(registered_character_name("ghislaine_dedoldia", self.characters_path), "Ghislaine Dedoldia")

    def test_duplicate_does_not_profile_or_cache_again(self) -> None:
        profiles = FakeProfiles()
        cache = FakeCache(self.refs_root)
        service = self.service(profiles, cache)
        service.bootstrap("Ghislaine Dedoldia")

        result = service.bootstrap("ghislaine_dedoldia")

        self.assertEqual(result["status"], "already_registered")
        self.assertTrue(result["duplicate"])
        self.assertEqual(profiles.calls, 1)
        self.assertEqual(cache.calls, 1)
        self.assertEqual(len(json.loads(self.characters_path.read_text(encoding="utf-8"))), 1)

    def test_not_found_never_calls_cache_or_registers(self) -> None:
        cache = FakeCache(self.refs_root)
        service = self.service(FakeProfiles(found=False), cache)

        with self.assertRaises(CharacterBootstrapError) as raised:
            service.bootstrap("Missing Character")

        self.assertEqual(raised.exception.code, "character_not_found")
        self.assertEqual(cache.calls, 0)
        self.assertEqual(json.loads(self.characters_path.read_text(encoding="utf-8")), {})

    def test_searxng_or_cache_failure_never_registers(self) -> None:
        service = self.service(cache=FakeCache(self.refs_root, mode="error"))

        with self.assertRaises(CharacterBootstrapError) as raised:
            service.bootstrap("Ghislaine Dedoldia")

        self.assertEqual(raised.exception.code, "character_cache_failed")
        self.assertEqual(json.loads(self.characters_path.read_text(encoding="utf-8")), {})

    def test_unusable_cache_never_registers(self) -> None:
        service = self.service(cache=FakeCache(self.refs_root, mode="unusable"))

        with self.assertRaises(CharacterBootstrapError) as raised:
            service.bootstrap("Ghislaine Dedoldia")

        self.assertEqual(raised.exception.code, "character_cache_failed")
        self.assertEqual(json.loads(self.characters_path.read_text(encoding="utf-8")), {})

    def test_unknown_create_command_is_blocked(self) -> None:
        self.characters_path.write_text(json.dumps({"2B": {"name": "2B"}}), encoding="utf-8")
        with patch("ada_app.command_parser.CHARACTERS_PATH", self.characters_path):
            known = parse_command("create 2 images of 2B")
            unknown = parse_command("create 2 images of Ghislaine Dedoldia")

        self.assertEqual(known["intent"], "CREATE_IMAGES")
        self.assertEqual(unknown["intent"], "CHARACTER_NOT_REGISTERED")
        self.assertEqual(unknown["error"], "character_not_registered")

    def test_direct_mission_api_blocks_unregistered_character(self) -> None:
        from ada_app import main

        class FakeRequest:
            async def json(self):
                return {"character": "Ghislaine Dedoldia", "requested_assets": 2}

        with patch.object(main, "CHARACTERS_PATH", self.characters_path):
            response = asyncio.run(main.create_mission(FakeRequest()))

        self.assertEqual(response.status_code, 409)
        body = json.loads(response.body)
        self.assertEqual(body["error"], "character_not_registered")

    def test_missing_character_payload_does_not_fallback_to_2b(self) -> None:
        from ada_app import main

        class FakeRequest:
            async def json(self):
                return {"requested_assets": 2}

        response = asyncio.run(main.create_mission(FakeRequest()))

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.body)
        self.assertEqual(body["error"], "character_required")

    def test_bootstrap_ghislaine_selection_creates_ghislaine_mission(self) -> None:
        from ada_app import main

        service = self.service()

        class FakeRequest:
            def __init__(self, data):
                self.data = data

            async def json(self):
                return self.data

        saved_missions = []

        class CapturingMissionStore:
            def save(self, mission):
                saved_missions.append(mission)

        def local_bootstrap(character, version, characters_path):
            self.assertEqual(characters_path, self.characters_path)
            return service.bootstrap(character, version)

        with patch.object(main, "CHARACTERS_PATH", self.characters_path), \
                patch.object(main, "bootstrap_character", side_effect=local_bootstrap):
            bootstrap_result = asyncio.run(
                main.add_character(FakeRequest({"character": "Ghislaine Dedoldia"}))
            )
            characters = asyncio.run(main.get_characters())

            selected_value = bootstrap_result["character"] if bootstrap_result["character"] in characters else ""
            self.assertEqual(selected_value, "Ghislaine Dedoldia")

            with patch("ada_app.mission.MissionStore", CapturingMissionStore), \
                    patch("ada_app.mission_runner.start_mission_background"):
                response = asyncio.run(main.create_mission(FakeRequest({
                    "character": selected_value,
                    "requested_assets": 2,
                })))

        self.assertEqual(response["status"], "created")
        self.assertEqual(len(saved_missions), 1)
        self.assertEqual(saved_missions[0].character, "Ghislaine Dedoldia")

    def test_app_route_and_dynamic_selector_are_wired(self) -> None:
        from ada_app.main import app

        routes = {route.path for route in app.routes}
        self.assertIn("/api/characters/bootstrap", routes)
        javascript = (Path(__file__).parents[1] / "ada_app" / "static" / "app.js").read_text(encoding="utf-8")
        template = (Path(__file__).parents[1] / "ada_app" / "templates" / "index.html").read_text(encoding="utf-8")
        self.assertIn("fetch('/api/characters')", javascript)
        self.assertIn("const selected = await loadCharacters(result.character)", javascript)
        self.assertIn("body: JSON.stringify({", javascript)
        self.assertIn("character,", javascript)
        self.assertNotIn('<option value="2B">', template)
        self.assertNotIn('<option value="Tifa Lockhart">', template)
        self.assertNotIn('<option value="Jill Valentine">', template)


if __name__ == "__main__":
    unittest.main()
