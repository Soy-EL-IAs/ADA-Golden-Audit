from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_full_pipeline import FullPipeline
from lmstudio_controller import LMStudioController
from ada_app.pilot_runner import prepare_comfy_handoff, prepare_review_handoff


class FakeController:
    def __init__(self, events: list[str]) -> None:
        self.events = events

    def prepare_for_lm(self, unload, status):
        self.events.append("comfy_unload")
        unload()
        self.events.append("comfy_vram_released")
        status()
        return {"vram": {"released": True}}

    def activate_role(self, role: str):
        self.events.append(f"lm_load:{role}")

    def list_models(self):
        return {"loaded": []}

    def prepare_for_comfy(self, status):
        self.events.append("lm_unload")
        self.events.append("lm_vram_released")
        status()
        return {"vram": {"released": True}}


class ResourceHandoffTests(unittest.TestCase):
    def pipeline(self, events: list[str]) -> FullPipeline:
        pipeline = FullPipeline.__new__(FullPipeline)
        pipeline.controller = FakeController(events)
        pipeline.evidence = {"model_events": [], "comfy_events": []}
        pipeline._request_comfy_unload = lambda: events.append("comfy_free_request") or {}
        pipeline._comfy_status = lambda: events.append("vram_poll") or {
            "idle": True, "vram_total": 100, "vram_free": 90,
        }
        return pipeline

    def test_comfy_unload_and_release_happen_before_lm_load(self) -> None:
        events: list[str] = []
        pipeline = self.pipeline(events)

        pipeline._activate_review("before_illustrious_review")

        self.assertLess(events.index("comfy_free_request"), events.index("comfy_vram_released"))
        self.assertLess(events.index("comfy_vram_released"), events.index("lm_load:visual_review_worker"))

    def test_lm_unload_and_release_happen_before_comfy_submit(self) -> None:
        events: list[str] = []
        pipeline = self.pipeline(events)

        with patch("run_full_pipeline.submit", side_effect=lambda *args: events.append("comfy_render") or "prompt-id"):
            prompt_id = pipeline._submit_comfy({}, "test", "before_klein_render")

        self.assertEqual(prompt_id, "prompt-id")
        self.assertLess(events.index("lm_unload"), events.index("lm_vram_released"))
        self.assertLess(events.index("lm_vram_released"), events.index("comfy_render"))

    def test_comfy_release_poll_uses_configured_threshold(self) -> None:
        controller = LMStudioController.__new__(LMStudioController)
        controller.config = {"vram_release": {
            "timeout_seconds": 1,
            "poll_seconds": 0,
            "comfy_min_free_ratio": 0.75,
        }}
        snapshots = iter([
            {"idle": True, "vram_total": 100, "vram_free": 20},
            {"idle": True, "vram_total": 100, "vram_free": 80},
        ])

        result = controller.wait_for_comfy_vram_release(lambda: next(snapshots))

        self.assertTrue(result["released"])
        self.assertEqual(result["free_ratio"], 0.8)

    def test_ada_app_pilot_uses_the_same_bidirectional_handoffs(self) -> None:
        events: list[str] = []

        class PilotController(FakeController):
            def comfy_status(self, base_url):
                self.events.append("comfy_status")
                return {"idle": True, "vram_total": 100, "vram_free": 90}

            def handoff_comfy_to_lm(self, base_url):
                self.events.extend(["comfy_unload", "comfy_vram_released"])
                return {"vram": {"released": True}}

        controller = PilotController(events)
        prepare_review_handoff(controller)
        controller.activate_role("visual_review_worker")
        prepare_comfy_handoff(controller)
        events.append("comfy_render")

        self.assertLess(events.index("comfy_vram_released"), events.index("lm_load:visual_review_worker"))
        self.assertLess(events.index("lm_vram_released"), events.index("comfy_render"))


if __name__ == "__main__":
    unittest.main()
