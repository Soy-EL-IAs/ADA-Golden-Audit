"""Minimal resumable coordinator for ADA's specialist image pipeline."""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from ada_paths import ADA_ROOT, COMFYUI_BASE_URL
from character_profile import CharacterProfileDatabase
from lmstudio_controller import LMStudioController
from specialist_agents import LMStudioSpecialistClient
from specialist_orchestrator import SpecialistOrchestrator
from specialist_visual_reviewer import review_stage_image
from production_workflows import (
    ILLUSTRIOUS_ONLY_WORKFLOW,
    KLEIN_ONLY_WORKFLOW,
    build_illustrious_workflow,
    build_klein_workflow,
    submission_provenance,
    validate_klein_workflow,
)

from run_specialist_mini_e2e import (
    output_path, read_json, submit, upload, wait_history, write_json,
)
from run_klein_jsonl_batch import apply_klein_preset

from ada_paths import LEGACY_RUNS_ROOT
RUNS_ROOT = LEGACY_RUNS_ROOT / "full-pipeline"
CHARACTER = "2B"
VERSION = "NieR:Automata"
TASK = "Create one restrained strategic-censorship scene with a clear interruption, visible cause and consequence, and a strong animation hook."
KLEIN_PRESET_CONFIG = ADA_ROOT / "legacy" / "config" / "klein" / "klein_production_presets.json"


class FullPipeline:
    def __init__(self, run_dir: Path, *, character: str, version: str | None, video: bool = False) -> None:
        self.run_dir = run_dir
        self.character = character
        self.version = version
        self.video = video
        self.controller = LMStudioController()
        self.orchestrator = SpecialistOrchestrator(run_dir, client=None)
        self.evidence: dict[str, Any] = {"run_dir": str(run_dir), "video": video, "model_events": [], "comfy_events": []}

    def run(self) -> dict[str, Any]:
        profile = CharacterProfileDatabase().get_character_profile(self.character, self.version)
        if not (self.run_dir / "character_profile.json").exists():
            write_json(self.run_dir / "character_profile.json", profile)

        if not profile.get("character_profile_used", False):
            self.orchestrator.run.fail(
                RuntimeError(
                    f'Character profile not found locally for "{self.character}". Generation was not started.'
                ),
                component="character_profile",
            )

        while True:
            state = self.orchestrator.run.read()
            stage = state["stage"]

            if stage in {"COMPLETE", "FAILED"}:
                break

            if stage == "CREATED":
                self._premise(profile)
            elif stage == "PREMISES_READY":
                self._illustrious(profile)
            elif stage == "ILLUSTRIOUS_PROMPTS_READY":
                self._illustrious_render()
            elif stage == "ILLUSTRIOUS_RENDERED":
                self._illustrious_review()
            elif stage == "ILLUSTRIOUS_REVIEWED":
                self._klein(profile)
            elif stage == "KLEIN_PROMPTS_READY":
                self._klein_render()
            elif stage == "KLEIN_RENDERED":
                self._final_review()
            elif stage == "FINAL_REVIEWED":
                self.orchestrator.complete()
        final = self.orchestrator.run.read()
        self.evidence["state"] = final
        write_json(self.run_dir / "pipeline_evidence.json", self.evidence)
        if final["stage"] not in {"COMPLETE", "FAILED"}:
            raise RuntimeError(f"Pipeline stopped at {final['stage']}")
        return self.evidence

    def _activate(self, role: str, agent: str) -> LMStudioSpecialistClient:
        started = time.perf_counter()
        client = LMStudioSpecialistClient.for_role(self.controller, role)
        self.evidence["model_events"].append({"agent": agent, "role": role, "activate_seconds": round(time.perf_counter() - started, 3), "unload": self.controller.last_unload_diagnostic})
        return client

    def _premise(self, profile: dict[str, Any]) -> None:
        self.orchestrator.client = self._activate("premise_agent", "premise")
        self.orchestrator.create_premise(task=TASK, character_profile=profile, viral_guide="runtime")

    def _illustrious(self, profile: dict[str, Any]) -> None:
        self.orchestrator.client = self._activate("illustrious_agent", "illustrious")
        self.orchestrator.compile_illustrious(character_profile=profile, illustrious_guide="runtime")

    def _illustrious_render(self) -> None:
        state = self.orchestrator.run.read(); result = self.orchestrator._read_artifact(state, "illustrious_result")
        node_out = "7"
        workflow = build_illustrious_workflow(
            positive_prompt=result["illustrious_prompt"],
            seed=state["seeds"][result["id"]]["illustrious"],
            width=768,
            height=1376,
            output_prefix=f"AdaFullPipeline/{self.run_dir.name}/{result['id']}/illustrious",
        )
        write_json(self.run_dir / "illustrious_workflow.json", workflow)
        started = time.perf_counter()
        prompt_id = self._submit_comfy(workflow, f"full-ill-{result['id']}", "before_illustrious_render")
        attempt = state.get("retries_PREMISES_READY", 0) + 1
        provenance = submission_provenance(
            mission_id=f"standalone:{self.run_dir.name}", run_id=self.run_dir.name,
            concept_id=result["id"], candidate_id=result["id"], attempt_id=f"{result['id']}:attempt:{attempt:02d}",
            stage="illustrious", workflow_path=ILLUSTRIOUS_ONLY_WORKFLOW,
            input_asset=str((self.run_dir / "illustrious_result.json").resolve()), prompt_id=prompt_id,
        )
        submission_path = self.run_dir / "submissions" / f"illustrious_attempt_{attempt:02d}.json"
        write_json(submission_path, provenance)
        self.orchestrator.run.attach_artifact("illustrious_prompt_id", prompt_id)
        history = wait_history(COMFYUI_BASE_URL, prompt_id)
        if len(history.get("outputs", {}).get(node_out, {}).get("images", [])) != 1:
            raise RuntimeError("Illustrious submission did not produce exactly one image")
        path = output_path(history, node_out)
        provenance["output_asset"] = str(path.resolve())
        write_json(submission_path, provenance)
        self.evidence["comfy_events"].append({"stage": "illustrious_render", "prompt_id": prompt_id, "seconds": round(time.perf_counter() - started, 3), "path": str(path)})
        self.orchestrator.record_illustrious_render(path)
        self.orchestrator.run.attach_artifact("illustrious_output_path", str(path.resolve()))

    def _illustrious_review(self) -> None:
        from specialist_visual_reviewer import review_stage_image
        print("  Running Visual Review [Illustrious]...")
        state = self.orchestrator.run.read()
        if state["stage"] != "ILLUSTRIOUS_RENDERED":
            return
        artifacts = state["artifacts"]
        image = Path(artifacts["illustrious_image"])
        if not image.is_absolute():
            image = self.run_dir / image
        premise = json.loads((self.run_dir / artifacts["premise_spec"]).read_text(encoding="utf-8"))
        attempt = state.get("retries_PREMISES_READY", 0) + 1
        diag_dir = self.run_dir / "diagnostics" / f"review_illustrious_attempt_{attempt:02d}"
        diag_dir.mkdir(parents=True, exist_ok=True)
        try:
            started = time.perf_counter()
            self._activate_review("before_illustrious_review")
            try:
                review = review_stage_image(
                    image, identifier=premise["id"], stage="illustrious", premise_spec=premise,
                    model=self.controller.role("visual_review_worker").model, diagnostic_dir=diag_dir,
                )
            finally:
                self._release_lm("after_illustrious_review")
            self.evidence["comfy_events"].append({"stage": "visual_review", "seconds": round(time.perf_counter() - started, 3)})
            self.orchestrator.record_illustrious_review(review)

            if review["verdict"] in {"RETRY_RENDER", "RETRY_ILLUSTRIOUS"}:
                print("  [Illustrious Review] Renderer retry requested. Retrying...")
                self.orchestrator.run.retry_stage("PREMISES_READY", reason="Illustrious review requested a structural retry", max_retries=3)
        except Exception as exc:
            from specialist_visual_reviewer import VisualReviewTransportError
            if isinstance(exc, VisualReviewTransportError):
                print(f"  [Illustrious Review] Review format error: {exc}. Retrying review...")
                self.orchestrator.run.retry_stage("ILLUSTRIOUS_RENDERED", reason=f"Visual Review schema failure: {exc}", max_retries=3)
            else:
                self.orchestrator.record_review_failure(exc, stage="illustrious", diagnostic_dir=diag_dir)
                raise

    def _klein(self, profile: dict[str, Any]) -> None:
        # We skip activating the 27B model for the standard path
        self.orchestrator.compile_klein_deterministic(character_profile=profile)

    def _klein_render(self) -> None:
        state = self.orchestrator.run.read(); result = self.orchestrator._read_artifact(state, "klein_result")
        source = Path(state["artifacts"]["illustrious_image"]).resolve()
        if not source.is_file():
            raise FileNotFoundError(f"Approved Illustrious artifact is missing: {source}")
        node_out = "20"
        uploaded = upload(COMFYUI_BASE_URL, source, f"ada_full_{result['id']}.png")
        workflow = build_klein_workflow(
            input_image=uploaded,
            positive_prompt=result["klein_prompt"],
            seed=state["seeds"][result["id"]]["klein"],
            output_prefix=f"AdaFullPipeline/{self.run_dir.name}/{result['id']}/klein",
        )
        preset_config = read_json(KLEIN_PRESET_CONFIG)
        preset_name = preset_config["default"]
        preset = preset_config["presets"][preset_name]
        apply_klein_preset(workflow, preset)
        validate_klein_workflow(workflow, expected_input_image=uploaded)
        self.evidence["klein_preset"] = {"source": str(KLEIN_PRESET_CONFIG), "name": preset_name, "steps": preset["steps"], "loras": preset["loras"], "sampler": workflow["41"]["inputs"].get("sampler_name"), "scheduler": "Flux2Scheduler node 43", "guidance": workflow["47"]["inputs"].get("guidance"), "cfg": workflow["53"]["inputs"].get("cfg"), "model": workflow["45"]["inputs"].get("unet_name"), "text_encoder": workflow["46"]["inputs"].get("clip_name"), "vae": workflow["37"]["inputs"].get("vae_name")}
        write_json(self.run_dir / "klein_workflow.json", workflow)
        started = time.perf_counter()
        prompt_id = self._submit_comfy(workflow, f"full-klein-{result['id']}", "before_klein_render")
        attempt = state.get("retries_ILLUSTRIOUS_REVIEWED", 0) + 1
        provenance = submission_provenance(
            mission_id=f"standalone:{self.run_dir.name}", run_id=self.run_dir.name,
            concept_id=result["id"], candidate_id=result["id"], attempt_id=f"{result['id']}:attempt:{attempt:02d}",
            stage="klein", workflow_path=KLEIN_ONLY_WORKFLOW, input_asset=str(source),
            prompt_id=prompt_id, comfyui_input_name=uploaded,
        )
        submission_path = self.run_dir / "submissions" / f"klein_attempt_{attempt:02d}.json"
        write_json(submission_path, provenance)
        self.orchestrator.run.attach_artifact("klein_prompt_id", prompt_id)
        history = wait_history(COMFYUI_BASE_URL, prompt_id)
        if len(history.get("outputs", {}).get(node_out, {}).get("images", [])) != 1:
            raise RuntimeError("Klein submission did not produce exactly one image")
        path = output_path(history, node_out)
        provenance["output_asset"] = str(path.resolve())
        write_json(submission_path, provenance)
        self.evidence["comfy_events"].append({"stage": "klein_render", "prompt_id": prompt_id, "input": str(source), "seconds": round(time.perf_counter() - started, 3), "path": str(path)})
        self.orchestrator.record_klein_render(path)
        self.orchestrator.run.attach_artifact("klein_output_path", str(path.resolve()))

    def _prepare_comfy(self, block: str) -> None:
        started = time.perf_counter()
        loaded_before = self.controller.list_models().get("loaded", [])
        release = self.controller.prepare_for_comfy(self._comfy_status)
        loaded_after = self.controller.list_models().get("loaded", [])
        self.evidence.setdefault("comfy_model_events", []).append({"block": block, "seconds": round(time.perf_counter() - started, 3), "release": release, "loaded_instances_before_render": loaded_before, "loaded_instances_after_unload": loaded_after})

    def _submit_comfy(self, workflow: dict[str, Any], label: str, block: str) -> str:
        self._prepare_comfy(block)
        return submit(COMFYUI_BASE_URL, workflow, label)

    def _comfy_status(self) -> dict[str, Any]:
        return self.controller.comfy_status(COMFYUI_BASE_URL)

    def _request_comfy_unload(self) -> dict[str, Any]:
        return self.controller.request_comfy_unload(COMFYUI_BASE_URL)

    def _prepare_lm(self, block: str) -> None:
        started = time.perf_counter()
        release = self.controller.prepare_for_lm(self._request_comfy_unload, self._comfy_status)
        self.evidence.setdefault("comfy_model_events", []).append({
            "block": block,
            "seconds": round(time.perf_counter() - started, 3),
            "release": release,
        })

    def _activate_review(self, block: str) -> None:
        self._prepare_lm(block)
        self.controller.activate_role("visual_review_worker")

    def _release_lm(self, block: str) -> None:
        started = time.perf_counter()
        unloaded = self.controller.unload_all()
        released = self.controller.wait_for_vram_release()
        self.evidence.setdefault("model_events", []).append({
            "agent": "visual_review",
            "block": block,
            "seconds": round(time.perf_counter() - started, 3),
            "unloaded": unloaded,
            "vram": released,
        })

    def _final_review(self) -> None:
        state = self.orchestrator.run.read(); premise = self.orchestrator._read_artifact(state, "premise_spec")
        path = Path(state["artifacts"]["klein_image"]); started = time.perf_counter()

        attempt = state.get("retries_KLEIN_RENDERED", 0) + 1
        diag_dir = self.run_dir / "diagnostics" / f"final_review_attempt_{attempt:02d}"
        diag_dir.mkdir(parents=True, exist_ok=True)

        try:
            self._activate_review("before_final_review")
            try:
                from specialist_visual_reviewer import review_stage_image, VisualReviewTransportError
                review = review_stage_image(path, identifier=premise["id"], stage="klein", premise_spec=premise, model=self.controller.role("visual_review_worker").model, diagnostic_dir=diag_dir, context_length=8192)
            finally:
                self._release_lm("after_final_review")
            self.evidence["comfy_events"].append({"stage": "final_review", "seconds": round(time.perf_counter() - started, 3)})
            self.orchestrator.record_final_review(review)
        except Exception as exc:
            from specialist_visual_reviewer import VisualReviewTransportError
            if isinstance(exc, VisualReviewTransportError):
                print(f"  [Final Review] Review format error: {exc}. Retrying review...")
                self.orchestrator.run.retry_stage("KLEIN_RENDERED", reason=f"Visual Review schema failure: {exc}", max_retries=3)
            else:
                self.orchestrator.record_review_failure(exc, stage="klein", diagnostic_dir=diag_dir)
                raise


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="specialist_full_001")
    parser.add_argument("--character", default=CHARACTER)
    parser.add_argument("--version", default=VERSION)
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--video", action="store_true")
    args = parser.parse_args()
    if args.count not in {1, 3} or args.video:
        raise ValueError("Supported executions are --count 1 or --count 3 with --video false")
    results = []
    version = args.version if args.version else None
    for index in range(1, args.count + 1):
        run_id = args.run_id if args.count == 1 else f"{args.run_id}_{index:02d}"
        run_dir = RUNS_ROOT / run_id
        if not (run_dir / "ada_run.json").exists():
            FullPipeline(run_dir, character=args.character, version=version, video=False).orchestrator.create(run_id, character=args.character, version=version, review_policy="strict")
        evidence = FullPipeline(run_dir, character=args.character, version=version, video=False).run()
        results.append({"run_dir": str(run_dir), "stage": evidence["state"]["stage"]})
    print(json.dumps({"status": "complete", "runs": results}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
