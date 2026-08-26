#!/usr/bin/env python3
"""Validate specialist Visual Review transports and Klein context without rerendering."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Callable

if __package__:
    from .ada_paths import ADA_ROOT, COMFYUI_ROOT, CONFIG_ROOT
    from .ada_run_state import AdaRunState
    from .lmstudio_controller import LMStudioController
    from .specialist_agents import LMStudioSpecialistClient, klein_request
    from .specialist_orchestrator import SpecialistOrchestrator
    from . import specialist_visual_reviewer as svr
else:
    from ada_paths import ADA_ROOT, COMFYUI_ROOT, CONFIG_ROOT
    from ada_run_state import AdaRunState
    from lmstudio_controller import LMStudioController
    from specialist_agents import LMStudioSpecialistClient, klein_request
    from specialist_orchestrator import SpecialistOrchestrator
    import specialist_visual_reviewer as svr


from ada_paths import LEGACY_RUNS_ROOT
SOURCE_MANIFEST = LEGACY_RUNS_ROOT / "klein" / "batch" / "render_validation_001_master_full_001" / "manifest.json"
SOURCE_PREMISES = LEGACY_RUNS_ROOT / "evolution" / "directed_validation" / "render_validation_001" / "selected" / "premises.jsonl"
SOURCE_MASTER = LEGACY_RUNS_ROOT / "evolution" / "directed_validation" / "render_validation_001" / "master_full_run_001" / "master_records.jsonl"
DEFAULT_ROOT = LEGACY_RUNS_ROOT / "evolution" / "directed_validation" / "render_validation_001" / "specialist_review_validation_004"
KLEIN_GUIDE = CONFIG_ROOT / "prompt_guides" / "klein_prompt_guide_v1.md"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as output:
        json.dump(value, output, ensure_ascii=False, indent=2)
        output.write("\n")


def stage_to_rendered(run_dir: Path, premise: dict[str, Any], illustrious_result: dict[str, Any], image_path: Path) -> SpecialistOrchestrator:
    orchestrator = SpecialistOrchestrator(run_dir, client=NoopClient())
    orchestrator.create("review_validation", character="2B", version="NieR:Automata", review_policy="strict")
    orchestrator._write_json_new("premise_spec.json", premise)
    orchestrator._write_json_new("illustrious_result.json", illustrious_result)
    orchestrator.run.allocate_seeds([premise["id"]])
    orchestrator.run.advance("PREMISES_READY", artifacts={"premise_spec": "premise_spec.json"})
    orchestrator.run.advance("ILLUSTRIOUS_PROMPTS_READY", artifacts={"illustrious_result": "illustrious_result.json"})
    orchestrator.record_illustrious_render(image_path)
    return orchestrator


class NoopClient:
    def execute(self, request, *, raw_output=None):
        raise RuntimeError("NoopClient must not execute an LLM call during state setup")


def call_review(orchestrator: SpecialistOrchestrator, *, image_path: Path, premise: dict[str, Any], model: str, diagnostic_dir: Path, patch_request: Callable | None = None) -> dict[str, Any]:
    original = svr._request
    if patch_request is not None:
        svr._request = patch_request
    try:
        review = svr.review_stage_image(
            image_path,
            identifier=premise["id"],
            stage="illustrious",
            premise_spec=premise,
            model=model,
            diagnostic_dir=diagnostic_dir,
        )
    finally:
        svr._request = original
    orchestrator.record_illustrious_review(review)
    return review


def main() -> int:
    root = DEFAULT_ROOT.resolve()
    if root.exists():
        raise FileExistsError(f"Refusing to overwrite validation root: {root}")
    root.mkdir(parents=True)
    manifest = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    record = manifest["records"][0]
    premise_source = next(item for item in read_jsonl(SOURCE_PREMISES) if item["id"] == record["id"])
    master_source = next(item for item in read_jsonl(SOURCE_MASTER) if item["id"] == record["id"])
    descriptor = record["illustrious"][0]
    image_path = COMFYUI_ROOT / "output" / descriptor["subfolder"] / descriptor["filename"]
    if not image_path.is_file():
        raise FileNotFoundError(image_path)

    premise = {
        "id": premise_source["id"],
        "category": premise_source["category"],
        "premise": premise_source["premise"],
        "preserved_elements": master_source["preserved_elements"],
        "risk_notes": master_source["risk_notes"],
    }
    illustrious_result = {
        "id": master_source["id"],
        "illustrious_prompt": master_source["illustrious_prompt"],
        "resolved_risks": master_source["risk_notes"],
    }
    write_json(root / "source_context.json", {
        "source_manifest": str(SOURCE_MANIFEST),
        "source_image": str(image_path),
        "premise_spec": premise,
        "illustrious_result": illustrious_result,
        "rerendered": False,
    })

    controller = LMStudioController()
    controller.unload_all()
    controller.wait_for_vram_release()
    worker = controller.ensure_loaded("worker")
    worker_model = controller.role("worker").model
    evidence: dict[str, Any] = {
        "source_image": str(image_path), "rerendered": False,
        "worker_model": worker_model, "worker_load": worker,
        "runs": {},
    }

    success = stage_to_rendered(root / "success", premise, illustrious_result, image_path)
    success_review = call_review(
        success, image_path=image_path, premise=premise, model=worker_model,
        diagnostic_dir=root / "success" / "review_diagnostics",
    )
    evidence["runs"]["success"] = {
        "review": success_review,
        "state": success.run.read(),
        "diagnostics": str(root / "success" / "review_diagnostics"),
    }

    fallback = stage_to_rendered(root / "fallback", premise, illustrious_result, image_path)
    real_request = svr._request
    first = {"value": True}
    def fail_schema_then_use_lmstudio(url: str, payload: dict[str, Any], timeout: int = 300) -> dict[str, Any]:
        if first["value"] and url.endswith("/v1/chat/completions"):
            first["value"] = False
            return {"choices": [{"message": {"content": ""}}], "synthetic": "forced_schema_failure_for_fallback_test"}
        return real_request(url, payload, timeout=timeout)
    fallback_review = call_review(
        fallback, image_path=image_path, premise=premise, model=worker_model,
        diagnostic_dir=root / "fallback" / "review_diagnostics", patch_request=fail_schema_then_use_lmstudio,
    )
    evidence["runs"]["fallback"] = {
        "review": fallback_review,
        "state": fallback.run.read(),
        "diagnostics": str(root / "fallback" / "review_diagnostics"),
        "forced_first_transport_failure": True,
        "native_fallback_was_real_lm_studio": True,
    }

    failure = stage_to_rendered(root / "failure_resume", premise, illustrious_result, image_path)
    def always_empty(url: str, payload: dict[str, Any], timeout: int = 300) -> dict[str, Any]:
        return {"choices": [{"message": {"content": ""}}], "output": [], "synthetic": "forced_failure_for_boundary_test"}
    failure_error: dict[str, str] = {}
    try:
        call_review(
            failure, image_path=image_path, premise=premise, model=worker_model,
            diagnostic_dir=root / "failure_resume" / "review_diagnostics", patch_request=always_empty,
        )
    except Exception as exc:
        failure_error = {"type": type(exc).__name__, "message": str(exc)}
        failure.record_review_failure(exc, stage="illustrious", diagnostic_dir=root / "failure_resume" / "review_diagnostics")
    persisted_after_failure = AdaRunState(failure.run.run_dir).read()
    resumed_review = call_review(
        failure, image_path=image_path, premise=premise, model=worker_model,
        diagnostic_dir=root / "failure_resume" / "resume_review_diagnostics",
    )
    evidence["runs"]["failure_resume"] = {
        "forced_failure": failure_error,
        "state_after_failure": persisted_after_failure,
        "resume_review": resumed_review,
        "state_after_resume": failure.run.read(),
        "diagnostics": str(root / "failure_resume" / "review_diagnostics"),
        "resume_diagnostics": str(root / "failure_resume" / "resume_review_diagnostics"),
    }

    controller.unload_all()
    controller.wait_for_vram_release()
    master = controller.ensure_loaded("master")
    master_model = controller.role("master").model
    klein = klein_request(
        premise_spec=premise,
        illustrious_result=illustrious_result,
        visual_review=resumed_review,
        illustrious_image=str(image_path.resolve()),
        klein_guide=KLEIN_GUIDE.read_text(encoding="utf-8").strip(),
    )
    write_json(root / "failure_resume" / "klein_effective_context.json", {
        "role": klein.role,
        "contract": klein.contract,
        "system_prompt": klein.system_prompt,
        "task_prompt": json.loads(klein.task_prompt),
    })
    client = LMStudioSpecialistClient(base_url="http://127.0.0.1:1234", model=master_model, timeout_seconds=900)
    klein_result = client.execute(klein, raw_output=root / "failure_resume" / "klein_raw_response.json")
    write_json(root / "failure_resume" / "klein_result.json", klein_result)
    failure.run.attach_artifact("klein_result", "klein_result.json")
    failure.run.advance("KLEIN_PROMPTS_READY", artifacts={"klein_result": "klein_result.json", "klein_context": "klein_effective_context.json"})
    evidence["klein"] = {
        "model": master_model, "load": master,
        "context": str(root / "failure_resume" / "klein_effective_context.json"),
        "raw_response": str(root / "failure_resume" / "klein_raw_response.json"),
        "result": str(root / "failure_resume" / "klein_result.json"),
        "state_after_klein_prompt": failure.run.read(),
    }
    write_json(root / "evidence.json", evidence)
    print(json.dumps({"status": "complete", "root": str(root), "source_image": str(image_path), "klein_model": master_model}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
