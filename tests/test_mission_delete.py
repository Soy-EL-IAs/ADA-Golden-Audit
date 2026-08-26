from __future__ import annotations

import asyncio
import json
import shutil
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

from ada_app import main
from ada_app.mission import MissionStore, ProductionMission


ROOT = Path(__file__).resolve().parents[1]


class MissionDeleteTests(unittest.TestCase):
    def setUp(self) -> None:
        test_tmp = ROOT / "data" / "tmp" / "tests"
        test_tmp.mkdir(parents=True, exist_ok=True)
        self.temporary = test_tmp / f"ada-mission-delete-{uuid.uuid4().hex}"
        self.temporary.mkdir()
        self.addCleanup(shutil.rmtree, self.temporary, True)
        self.missions_dir = self.temporary / "missions"

    def save_mission(self, status: str) -> ProductionMission:
        mission = ProductionMission(character="Ghislaine Dedoldia")
        mission.status = status
        with patch("ada_app.mission.MISSIONS_DIR", self.missions_dir):
            MissionStore().save(mission)
        return mission

    def test_delete_removes_only_terminal_mission_state(self) -> None:
        library_asset = self.temporary / "library" / "approved.png"
        character_ref = self.temporary / "character_refs" / "ghislaine" / "ref.jpg"
        library_asset.parent.mkdir(parents=True)
        character_ref.parent.mkdir(parents=True)
        library_asset.write_bytes(b"approved")
        character_ref.write_bytes(b"reference")

        for status in ("FAILED", "COMPLETE", "CANCELLED"):
            with self.subTest(status=status):
                mission = self.save_mission(status)
                mission_path = self.missions_dir / f"{mission.mission_id}.json"

                with patch("ada_app.mission.MISSIONS_DIR", self.missions_dir):
                    response = asyncio.run(main.delete_mission(mission.mission_id))

                self.assertEqual(response["status"], "deleted")
                self.assertFalse(mission_path.exists())
                self.assertTrue(library_asset.is_file())
                self.assertTrue(character_ref.is_file())

    def test_active_mission_cannot_be_deleted(self) -> None:
        mission = self.save_mission("GENERATING_CONCEPTS")
        mission_path = self.missions_dir / f"{mission.mission_id}.json"

        with patch("ada_app.mission.MISSIONS_DIR", self.missions_dir):
            response = asyncio.run(main.delete_mission(mission.mission_id))

        self.assertEqual(response.status_code, 409)
        body = json.loads(response.body)
        self.assertEqual(body["error"], "mission_not_deletable")
        self.assertEqual(body["status"], "GENERATING_CONCEPTS")
        self.assertTrue(mission_path.is_file())

    def test_delete_button_requires_confirmation_and_returns_home(self) -> None:
        javascript = (ROOT / "ada_app" / "static" / "app.js").read_text(encoding="utf-8")
        template = (ROOT / "ada_app" / "templates" / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="btn-delete-mission"', template)
        self.assertIn("window.confirm(", javascript)
        self.assertIn("method: 'DELETE'", javascript)
        self.assertIn("switchTab('home')", javascript)


if __name__ == "__main__":
    unittest.main()
