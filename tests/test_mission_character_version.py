from __future__ import annotations

import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from ada_app.mission import ProductionMission
from ada_app import mission_runner


class FakeMissionStore:
    def __init__(self, mission: ProductionMission) -> None:
        self.mission = mission
        self.updates: list[dict] = []

    def load(self, mission_id: str) -> ProductionMission:
        return self.mission

    def update(self, mission: ProductionMission, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(mission, key, value)
        self.updates.append(kwargs)


class FakeController:
    def activate_role(self, role: str) -> None:
        return None


class MissionCharacterVersionTests(unittest.TestCase):
    def test_create_mission_reaches_round_one_using_registered_character_version(self) -> None:
        created = ProductionMission(character="2B", requested_assets=2, max_rounds=1)
        persisted = created.to_dict()
        self.assertNotIn("version", persisted)
        mission = ProductionMission.from_dict(persisted)
        store = FakeMissionStore(mission)
        written_configs: list[dict] = []

        def fake_read_json(path: Path):
            if path == mission_runner.CHARACTERS_CONFIG:
                return {"2B": {"name": "2B", "universe": "NieR:Automata"}}
            return {"schema_version": 1}

        with patch.object(mission_runner, "MissionStore", return_value=store), \
                patch.object(mission_runner, "read_json", side_effect=fake_read_json), \
                patch.object(mission_runner, "write_json", side_effect=lambda path, value: written_configs.append(value.copy())), \
                patch("lmstudio_controller.LMStudioController", FakeController), \
                patch.object(mission_runner.subprocess, "run", return_value=SimpleNamespace(returncode=1, stdout="", stderr="test stop")) as subprocess_run, \
                patch.object(mission_runner, "RUNS_DIR", Path("D:/nonexistent-ada-test-runs")):
            mission_runner.run_mission(mission.mission_id)

        self.assertTrue(any(update.get("status") == "GENERATING_CONCEPTS" for update in store.updates))
        self.assertEqual(written_configs[0]["character"], "2B")
        self.assertEqual(written_configs[0]["version"], "NieR:Automata")
        subprocess_run.assert_called_once()
        self.assertNotIn("'ProductionMission' object has no attribute 'version'", mission.error_message)

    def test_explicit_registry_version_takes_precedence_over_universe(self) -> None:
        with patch.object(
            mission_runner,
            "read_json",
            return_value={"Character": {"version": "Exact Version", "universe": "Fallback Universe"}},
        ):
            self.assertEqual(mission_runner.character_version("Character"), "Exact Version")


if __name__ == "__main__":
    unittest.main()
