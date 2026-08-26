from __future__ import annotations

import json
import sys
import shutil
import unittest
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from specialist_orchestrator import SpecialistOrchestrator


class FakeClient:
    def __init__(self) -> None:
        self.roles: list[str] = []

    def execute(self, request, *, raw_output=None):
        self.roles.append(request.role)
        if request.role == "premise":
            value = {"category": "closeup", "premise": "A visible event.",
                     "identity_elements": ["identity", "event"], "risk_notes": ["The event may become unclear."]}
        elif request.role == "illustrious":
            value = {"prompt": "identity, visible event, closeup framing",
                     }
        elif request.role == "klein":
            value = {"prompt": "Preserve identity and framing; correct the right hand."}
        else:
            value = {"video_prompt": "She completes the visible motion.",
                     "hook_contract": {"visual_hook": "A visible event.", "motion_trigger": "She moves.",
                                        "escalation": "The event intensifies.", "payoff": "The event resolves.",
                                        "end_state": "She holds the final pose."}}
        request.validate(value)
        if raw_output is not None:
            raw_output.parent.mkdir(parents=True, exist_ok=True)
            raw_output.write_text(json.dumps(value), encoding="utf-8")
        return value


class SpecialistOrchestratorTests(unittest.TestCase):
    def test_roles_have_separate_calls_and_persisted_boundaries(self) -> None:
        temporary = ROOT / "tests" / f"runtime_{uuid.uuid4().hex}"
        temporary.mkdir()
        self.addCleanup(shutil.rmtree, temporary, True)
        client = FakeClient()
        orchestrator = SpecialistOrchestrator(temporary / "run_001", client)
        orchestrator.create("run_001", character="2B", version="NieR:Automata")
        orchestrator.create_premise(task="Create one premise", character_profile={}, viral_guide="viral only")
        orchestrator.compile_illustrious(character_profile={}, illustrious_guide="illustrious only")
        source = temporary / "source.png"
        source.write_bytes(b"image")
        orchestrator.record_illustrious_render(source)
        orchestrator.record_illustrious_review({
            "id": "2b_run_001", "stage": "illustrious", "verdict": "REVIEW",
            "preserved_ok": ["identity"], "defects": ["right hand"], "drift": [], "summary": "Repair hand.",
        })
        orchestrator.compile_klein_legacy_agent(klein_guide="klein only")
        final = temporary / "final.png"
        final.write_bytes(b"image")
        orchestrator.record_klein_render(final)
        orchestrator.record_final_review({
            "id": "2b_run_001", "stage": "klein", "verdict": "PASS",
            "preserved_ok": ["identity"], "defects": [], "drift": [], "summary": "Ready.",
        })
        orchestrator.complete()
        orchestrator.compile_minimax(duration_seconds=5, workflow_mode="F2V", minimax_guide="video only")
        self.assertEqual(client.roles, ["premise", "illustrious", "klein", "minimax"])
        state = orchestrator.run.read()
        self.assertEqual(state["stage"], "COMPLETE")
        self.assertIn("minimax_result", state["artifacts"])


if __name__ == "__main__":
    unittest.main()
