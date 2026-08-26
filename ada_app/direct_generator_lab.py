"""Single-image direct generator runner isolated inside Model Lab."""

from __future__ import annotations

import copy
import json
import time
import traceback
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts.ada_paths import ADA_ROOT, COMFYUI_BASE_URL, COMFYUI_ROOT

from ada_app.model_lab import (
    LMStudioController,
    MODEL_LAB_ROOT,
    _vram_snapshot,
    output_path,
    submit,
    wait_history,
)


RECIPES_ROOT = MODEL_LAB_ROOT / "recipes"
DIRECT_ROLE = "direct_anime_generator"


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, value: Any, *, exclusive: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x" if exclusive else "w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def _project_path(relative: str) -> Path:
    path = (ADA_ROOT / relative).resolve()
    lab_root = MODEL_LAB_ROOT.resolve()
    if path != lab_root and lab_root not in path.parents:
        raise ValueError("Direct generator recipes may only reference Model Lab artifacts")
    return path


def recipe_catalog() -> list[dict[str, Any]]:
    recipes: list[dict[str, Any]] = []
    if not RECIPES_ROOT.is_dir():
        return recipes
    for path in sorted(RECIPES_ROOT.glob("*.json")):
        try:
            recipe = _read(path)
            if recipe.get("schema_version") != "model_benchmark_recipe_v1":
                continue
            recipe["manifest_path"] = str(path.resolve())
            recipe["availability"] = _recipe_availability(recipe)
            recipes.append(recipe)
        except Exception as exc:
            recipes.append({"recipe_id": path.stem, "status": "blocked", "availability": {"ready": False, "reason": str(exc)}})
    return recipes


def recipe_by_id(recipe_id: str) -> dict[str, Any]:
    recipe = next((item for item in recipe_catalog() if item.get("recipe_id") == recipe_id), None)
    if recipe is None:
        raise ValueError("Unknown direct generator recipe")
    availability = recipe.get("availability", {})
    if recipe.get("status") != "benchmark_ready" or availability.get("ready") is not True:
        raise ValueError(f"Recipe is not benchmark-ready: {availability.get('reason', recipe.get('status'))}")
    return recipe


def _recipe_availability(recipe: dict[str, Any]) -> dict[str, Any]:
    if recipe.get("status") != "benchmark_ready":
        return {"ready": False, "reason": f"recipe status is {recipe.get('status')}"}
    workflow = recipe.get("workflow", {})
    try:
        template = _project_path(str(workflow.get("api_template", "")))
    except ValueError as exc:
        return {"ready": False, "reason": str(exc)}
    if not template.is_file():
        return {"ready": False, "reason": "API workflow template is missing"}
    missing: list[str] = []
    models_root = COMFYUI_ROOT / "models"
    installed = {path.name for path in models_root.rglob("*.safetensors")} if models_root.is_dir() else set()
    for dependency in recipe.get("dependencies", []):
        filename = dependency.get("file") if isinstance(dependency, dict) else None
        if isinstance(filename, str) and filename not in installed:
            missing.append(filename)
    if missing:
        return {"ready": False, "reason": "missing ComfyUI dependencies", "missing": missing}
    return {"ready": True, "reason": "manual workflow evidence and all declared dependencies are present"}


def _bind(workflow: dict[str, Any], recipe: dict[str, Any], *, prompt: str, seed: int, prefix: str) -> None:
    values = {"prompt": prompt, "seed": int(seed), "output_prefix": prefix}
    for name, value in values.items():
        binding = recipe["bindings"][name]
        node = str(binding["node"])
        input_name = str(binding["input"])
        try:
            workflow[node]["inputs"][input_name] = value
        except KeyError as exc:
            raise ValueError(f"Invalid {name} binding in recipe {recipe['recipe_id']}") from exc


def _inference_seconds(history: dict[str, Any]) -> float | None:
    timestamps: dict[str, int] = {}
    for message in history.get("status", {}).get("messages", []):
        if not isinstance(message, list) or len(message) != 2 or not isinstance(message[1], dict):
            continue
        timestamp = message[1].get("timestamp")
        if isinstance(timestamp, int):
            timestamps[str(message[0])] = timestamp
    start = timestamps.get("execution_start")
    end = timestamps.get("execution_success")
    return round((end - start) / 1000, 3) if start is not None and end is not None and end >= start else None


def run_direct_generator_test(
    *, model_id: str, recipe_id: str, character: str, prompt: str,
    seed: int, character_contract: str, artifact_root: Path,
) -> dict[str, Any]:
    recipe = recipe_by_id(recipe_id)
    if recipe.get("model_id") != model_id:
        raise ValueError("Recipe does not belong to the selected model")
    if recipe.get("role") != DIRECT_ROLE:
        raise ValueError("Recipe is not a direct anime generator recipe")
    effective_prompt = str(prompt or "").strip()
    if not effective_prompt:
        raise ValueError("Direct generator prompt must not be empty")
    if recipe.get("resolution", {}).get("batch_size") != 1:
        raise ValueError("Direct Generator Benchmark only permits batch_size=1")

    now = datetime.now(timezone.utc)
    run_id = f"direct_{now.strftime('%Y%m%d_%H%M%S')}_{model_id}_{uuid.uuid4().hex[:6]}"
    artifact_root.mkdir(parents=True, exist_ok=False)
    template_path = _project_path(recipe["workflow"]["api_template"])
    workflow = copy.deepcopy(_read(template_path))
    output_prefix = f"ADA/MODEL_LAB/{run_id}/output"
    _bind(workflow, recipe, prompt=effective_prompt, seed=seed, prefix=output_prefix)
    effective_workflow_path = artifact_root / "effective_workflow.json"
    _write(effective_workflow_path, workflow, exclusive=True)

    loader = recipe.get("loader", {})
    sampling = recipe.get("sampling", {})
    receipt: dict[str, Any] = {
        "schema_version": "model_test_receipt_v1",
        "run_id": run_id,
        "model_id": model_id,
        "model_version": str(recipe["recipe_version"]),
        "recipe_id": recipe_id,
        "recipe_version": int(recipe["recipe_version"]),
        "checkpoint": loader.get("checkpoint"),
        "adapters": [loader["adapter"]] if isinstance(loader.get("adapter"), dict) else [],
        "workflow": str(effective_workflow_path.resolve()),
        "workflow_template": str(template_path.resolve()),
        "character": character,
        "character_contract": character_contract,
        "task": "direct_anime_generation",
        "status": "RUNNING",
        "started_at": now.isoformat(),
        "input_asset": "",
        "output_asset": None,
        "prompt": effective_prompt,
        "negative_prompt": recipe.get("negative_prompt"),
        "seed": int(seed),
        "configuration": {
            "role": DIRECT_ROLE,
            "prompt_style": recipe["prompt_style"],
            "loader": loader,
            "resolution": recipe["resolution"],
            "sampling": sampling,
            "dependencies": recipe["dependencies"],
        },
        "duration_seconds": None,
        "inference_seconds": None,
        "job_size": 1,
        "vram": {"before": _vram_snapshot(), "after": None},
        "result": {"score": None, "human_notes": None},
        "error": None,
    }
    receipt_path = artifact_root / "model_test_receipt.json"
    _write(receipt_path, receipt, exclusive=True)
    started = time.perf_counter()
    try:
        controller = LMStudioController()
        controller.prepare_for_comfy(lambda: controller.comfy_status(COMFYUI_BASE_URL))
        prompt_id = submit(COMFYUI_BASE_URL, workflow, run_id)
        receipt["prompt_id"] = prompt_id
        history = wait_history(COMFYUI_BASE_URL, prompt_id, timeout=1200)
        output = output_path(history, str(recipe["workflow"]["output_node"]))
        receipt.update({
            "status": "COMPLETE",
            "output_asset": str(output),
            "duration_seconds": round(time.perf_counter() - started, 3),
            "inference_seconds": _inference_seconds(history),
        })
    except Exception as exc:
        receipt.update({
            "status": "FAILED",
            "duration_seconds": round(time.perf_counter() - started, 3),
            "error": f"{type(exc).__name__}: {exc}",
            "error_details": {"type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc()},
        })
    receipt["vram"]["after"] = _vram_snapshot()
    receipt["completed_at"] = datetime.now(timezone.utc).isoformat()
    _write(receipt_path, receipt)
    return receipt
