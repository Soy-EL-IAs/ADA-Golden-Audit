#!/usr/bin/env python3
"""Run a small Klein-only LoRA A/B test from existing Illustrious outputs."""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import re
import shutil
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any

if __package__:
    from .lmstudio_controller import LMStudioController
    from .run_klein_jsonl_batch import compile_api, descriptors, http_json, load_dataset, wait_history
else:
    from lmstudio_controller import LMStudioController
    from run_klein_jsonl_batch import compile_api, descriptors, http_json, load_dataset, wait_history


if __package__:
    from .ada_paths import ADA_ROOT, COMFYUI_BASE_URL, COMFYUI_ROOT, CONFIG_ROOT, KLEIN_AB_TESTS_ROOT, KLEIN_BATCH_RUNS_ROOT, resolve_legacy_path
else:
    from ada_paths import ADA_ROOT, COMFYUI_BASE_URL, COMFYUI_ROOT, CONFIG_ROOT, KLEIN_AB_TESTS_ROOT, KLEIN_BATCH_RUNS_ROOT, resolve_legacy_path


ROOT = ADA_ROOT
CONFIG = json.loads((CONFIG_ROOT / "pipeline.json").read_text(encoding="utf-8"))
COMFY_ROOT = COMFYUI_ROOT or Path(CONFIG["comfy_root"])
COMFY_URL = COMFYUI_BASE_URL
RUNS_ROOT = KLEIN_BATCH_RUNS_ROOT
TESTS_ROOT = KLEIN_AB_TESTS_ROOT
DEFAULT_PLAN = CONFIG_ROOT / "klein_ab_tifa_remake_001.json"
TARGET_SAVE_NODE = "20"
LOAD_IMAGE_NODE = "900"


def safe_id(value: Any, field: str) -> str:
    text = str(value or "")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", text):
        raise ValueError(f"{field} may contain only letters, digits, underscores and hyphens")
    return text


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return value


def descriptor_path(descriptor: dict[str, Any]) -> Path:
    folder = {"output": "output", "input": "input", "temp": "temp"}.get(descriptor.get("type"))
    if folder is None:
        raise ValueError(f"Unsupported source image type: {descriptor.get('type')}")
    return COMFY_ROOT / folder / descriptor.get("subfolder", "") / descriptor["filename"]


def lora_path(relative: str) -> Path:
    root = (COMFY_ROOT / "models" / "loras").resolve()
    candidate = (root / Path(relative)).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"LoRA must remain inside {root}") from exc
    if not candidate.is_file():
        raise FileNotFoundError(candidate)
    return candidate


def ancestors(prompt: dict[str, Any], target: str) -> set[str]:
    keep: set[str] = set()

    def visit(node_id: str) -> None:
        if node_id in keep:
            return
        if node_id not in prompt:
            raise ValueError(f"Prompt references missing node {node_id}")
        keep.add(node_id)
        for value in prompt[node_id].get("inputs", {}).values():
            if isinstance(value, list) and len(value) == 2 and str(value[0]) in prompt:
                visit(str(value[0]))

    visit(target)
    return keep


def build_klein_prompt(
    base_workflow: dict[str, Any],
    input_name: str,
    record: dict[str, Any],
    condition: dict[str, Any],
    output_prefix: str,
) -> dict[str, Any]:
    prompt = compile_api(copy.deepcopy(base_workflow))
    prompt[LOAD_IMAGE_NODE] = {
        "class_type": "LoadImage",
        "inputs": {"image": input_name, "upload": "image"},
        "_meta": {"title": "Existing Illustrious source"},
    }
    # Node 40 is the actual Klein reference encode. Replacing its pixels input
    # disconnects the complete Illustrious generation branch.
    prompt["40"]["inputs"]["pixels"] = [LOAD_IMAGE_NODE, 0]
    prompt["38"]["inputs"]["noise_seed"] = int(record["klein_seed"])
    prompt["39"]["inputs"]["text"] = record["klein_prompt"]
    prompt[TARGET_SAVE_NODE]["inputs"]["filename_prefix"] = output_prefix

    lora = condition.get("lora")
    if lora is None:
        # Bypass the base workflow's existing klein_snofs LoRA completely.
        prompt["50"]["inputs"]["model"] = prompt["42"]["inputs"]["model"]
        prompt.pop("42")
    else:
        prompt["42"]["inputs"]["lora_1"] = {
            "on": True,
            "lora": str(lora).replace("/", "\\"),
            "strength": float(condition["weight"]),
        }

    keep = ancestors(prompt, TARGET_SAVE_NODE)
    klein_only = {node_id: prompt[node_id] for node_id in keep}
    if "2" in klein_only or "7" in klein_only:
        raise RuntimeError("Klein-only graph unexpectedly retained the Illustrious branch")
    return klein_only


def ab_invariant_signature(prompt: dict[str, Any]) -> str:
    """Normalize the one intended variable and verify everything else matches."""
    normalized = copy.deepcopy(prompt)
    normalized[TARGET_SAVE_NODE]["inputs"]["filename_prefix"] = "<condition-output>"
    if "42" in normalized:
        normalized["50"]["inputs"]["model"] = normalized["42"]["inputs"]["model"]
        normalized.pop("42")
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"))


def preflight(plan_path: Path) -> dict[str, Any]:
    plan = read_json(plan_path)
    test_id = safe_id(plan.get("test_id"), "test_id")
    source_batch_id = safe_id(plan.get("source_batch_id"), "source_batch_id")
    test_dir = TESTS_ROOT / test_id
    input_stage = COMFY_ROOT / "input" / "LunaKleinAB" / test_id
    if test_dir.exists():
        raise FileExistsError(f"A/B test directory already exists and will not be overwritten: {test_dir}")
    if input_stage.exists():
        raise FileExistsError(f"ComfyUI input staging directory already exists: {input_stage}")

    workflow_path = (ROOT / plan["workflow"]).resolve()
    if not workflow_path.is_file():
        raise FileNotFoundError(workflow_path)
    base_workflow = read_json(workflow_path)
    source_manifest_path = RUNS_ROOT / source_batch_id / "manifest.json"
    source_manifest = read_json(source_manifest_path)
    if source_manifest.get("status") != "complete":
        raise ValueError(f"Source batch is not complete: {source_manifest_path}")

    dataset_path = resolve_legacy_path(source_manifest["dataset"])
    records = {item["id"]: item for item in load_dataset(dataset_path, take=None)}
    batch_records = {
        item["id"]: item for item in source_manifest.get("records", []) if item.get("status") == "complete"
    }

    cases: list[dict[str, Any]] = []
    seen_cases: set[str] = set()
    for raw_case in plan.get("cases", []):
        case_id = safe_id(raw_case.get("id"), "case id")
        if case_id in seen_cases:
            raise ValueError(f"Duplicate case id: {case_id}")
        seen_cases.add(case_id)
        if case_id not in records or case_id not in batch_records:
            raise ValueError(f"Case is missing from dataset or completed source batch: {case_id}")
        images = batch_records[case_id].get("illustrious") or []
        if len(images) != 1:
            raise ValueError(f"Case must have exactly one Illustrious source: {case_id}")
        source_path = descriptor_path(images[0]).resolve()
        if not source_path.is_file():
            raise FileNotFoundError(source_path)
        cases.append({
            "id": case_id,
            "category": raw_case.get("category"),
            "record": records[case_id],
            "source_path": source_path,
        })

    conditions: list[dict[str, Any]] = []
    seen_conditions: set[str] = set()
    for raw_condition in plan.get("conditions", []):
        condition = dict(raw_condition)
        name = safe_id(condition.get("name"), "condition name")
        if name in seen_conditions:
            raise ValueError(f"Duplicate condition name: {name}")
        seen_conditions.add(name)
        if condition.get("trigger"):
            raise ValueError(f"No trigger is configured/required for the installed LoRA: {name}")
        if condition.get("lora") is not None:
            lora_path(str(condition["lora"]))
            condition["weight"] = float(condition["weight"])
        conditions.append(condition)

    if not cases or not conditions:
        raise ValueError("Plan must contain cases and conditions")

    for case in cases:
        input_name = f"LunaKleinAB/{test_id}/{case['id']}.png"
        signatures: set[str] = set()
        for condition in conditions:
            prompt = build_klein_prompt(
                base_workflow,
                input_name,
                case["record"],
                condition,
                f"LunaKleinAB/{test_id}/{condition['name']}/{case['id']}",
            )
            signatures.add(ab_invariant_signature(prompt))
        if len(signatures) != 1:
            raise RuntimeError(f"A/B conditions differ by more than the Klein LoRA: {case['id']}")

    return {
        "plan": plan,
        "test_id": test_id,
        "test_dir": test_dir,
        "input_stage": input_stage,
        "workflow_path": workflow_path,
        "base_workflow": base_workflow,
        "source_manifest_path": source_manifest_path,
        "dataset_path": dataset_path,
        "cases": cases,
        "conditions": conditions,
        "jobs": len(cases) * len(conditions),
    }


def comfy_status() -> dict[str, Any]:
    queue = http_json(f"{COMFY_URL}/queue")
    running = len(queue.get("queue_running", []))
    pending = len(queue.get("queue_pending", []))
    return {"idle": running == 0 and pending == 0, "running": running, "pending": pending}


def submit(prompt: dict[str, Any], test_id: str, case_id: str, condition: str) -> str:
    payload = {
        "prompt": prompt,
        "client_id": f"klein-ab-{uuid.uuid4().hex}",
        "extra_data": {"extra_pnginfo": {
            "klein_ab_test": test_id,
            "case_id": case_id,
            "condition": condition,
        }},
    }
    response = http_json(f"{COMFY_URL}/prompt", "POST", payload, timeout=60)
    if response.get("node_errors"):
        raise RuntimeError(json.dumps(response["node_errors"], ensure_ascii=False, indent=2))
    if not response.get("prompt_id"):
        raise RuntimeError(f"ComfyUI returned no prompt_id: {response}")
    return str(response["prompt_id"])


def copy_exclusive(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with source.open("rb") as source_file, target.open("xb") as target_file:
        shutil.copyfileobj(source_file, target_file)


def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def workflow_settings(base_workflow: dict[str, Any]) -> dict[str, Any]:
    nodes = {str(node["id"]): node for node in base_workflow["nodes"]}
    return {
        "sampler": nodes["41"]["widgets_values"][0],
        "scheduler": nodes["43"]["type"],
        "steps": nodes["43"]["widgets_values"][0],
        "width": nodes["43"]["widgets_values"][1],
        "height": nodes["43"]["widgets_values"][2],
        "guidance": nodes["47"]["widgets_values"][0],
        "cfg": nodes["53"]["widgets_values"][0],
        "reference_input": "existing Illustrious PNG encoded directly by VAEEncode node 40",
    }


def run(prepared: dict[str, Any]) -> dict[str, Any]:
    controller = LMStudioController()
    restore_master: dict[str, Any] | None = None
    if controller.enabled:
        try:
            controller.prepare_for_comfy(comfy_status)
        except Exception as preflight_error:
            controller.finish_work()
            try:
                controller.ensure_loaded("master")
            except Exception as restore_error:
                raise RuntimeError(
                    f"A/B preflight failed ({preflight_error}); Master restore also failed ({restore_error})"
                ) from preflight_error
            raise
    else:
        status = comfy_status()
        if not status["idle"]:
            raise RuntimeError(f"ComfyUI is busy: {status}")

    test_dir: Path = prepared["test_dir"]
    input_stage: Path = prepared["input_stage"]
    manifest_path = test_dir / "manifest.json"
    try:
        test_dir.mkdir(parents=True, exist_ok=False)
        input_stage.mkdir(parents=True, exist_ok=False)
        for condition in prepared["conditions"]:
            (test_dir / condition["name"]).mkdir()
        (test_dir / "source").mkdir()

        sources: list[dict[str, Any]] = []
        for case in prepared["cases"]:
            source_copy = test_dir / "source" / f"{case['id']}.png"
            staged_copy = input_stage / f"{case['id']}.png"
            copy_exclusive(case["source_path"], source_copy)
            copy_exclusive(case["source_path"], staged_copy)
            sources.append({
                "id": case["id"],
                "category": case["category"],
                "original_illustrious": str(case["source_path"]),
                "file": source_copy.relative_to(test_dir).as_posix(),
            })

        manifest: dict[str, Any] = {
            "schema_version": 1,
            "test_id": prepared["test_id"],
            "status": "running",
            "created_at": dt.datetime.now().astimezone().isoformat(),
            "source_batch_id": prepared["plan"]["source_batch_id"],
            "source_manifest": str(prepared["source_manifest_path"]),
            "dataset": str(prepared["dataset_path"]),
            "workflow": str(prepared["workflow_path"]),
            "settings": workflow_settings(prepared["base_workflow"]),
            "sources": sources,
            "conditions": prepared["conditions"],
            "jobs": [],
        }
        write_manifest(manifest_path, manifest)

        for case in prepared["cases"]:
            input_name = f"LunaKleinAB/{prepared['test_id']}/{case['id']}.png"
            for condition in prepared["conditions"]:
                job = {
                    "case_id": case["id"],
                    "category": case["category"],
                    "source": f"source/{case['id']}.png",
                    "condition": condition["name"],
                    "lora": condition.get("lora"),
                    "weight": condition["weight"],
                    "trigger": condition.get("trigger"),
                    "seed": case["record"]["klein_seed"],
                    "klein_prompt": case["record"]["klein_prompt"],
                    "status": "running",
                }
                manifest["jobs"].append(job)
                write_manifest(manifest_path, manifest)
                try:
                    prompt = build_klein_prompt(
                        prepared["base_workflow"],
                        input_name,
                        case["record"],
                        condition,
                        f"LunaKleinAB/{prepared['test_id']}/{condition['name']}/{case['id']}",
                    )
                    prompt_id = submit(prompt, prepared["test_id"], case["id"], condition["name"])
                    job["prompt_id"] = prompt_id
                    history = wait_history(COMFY_URL, prompt_id, int(CONFIG["klein"]["timeout_seconds"]))
                    outputs = descriptors(history, int(TARGET_SAVE_NODE))
                    if len(outputs) != 1:
                        raise RuntimeError(f"Expected one Klein output, got {len(outputs)}")
                    generated = descriptor_path(outputs[0])
                    suffix = generated.suffix.lower() or ".png"
                    local_output = test_dir / condition["name"] / f"{case['id']}{suffix}"
                    copy_exclusive(generated, local_output)
                    job.update(
                        status="complete",
                        output=local_output.relative_to(test_dir).as_posix(),
                        comfy_output=str(generated),
                    )
                except Exception as exc:
                    job.update(status="failed", error=str(exc))
                    manifest["status"] = "failed"
                    write_manifest(manifest_path, manifest)
                    raise
                write_manifest(manifest_path, manifest)

        manifest["status"] = "complete"
        manifest["completed_at"] = dt.datetime.now().astimezone().isoformat()
        write_manifest(manifest_path, manifest)
        return {"status": "complete", "test_dir": str(test_dir), "jobs": len(manifest["jobs"])}
    finally:
        if controller.enabled:
            controller.finish_work()
            restore_master = controller.ensure_loaded("master")
            if manifest_path.exists():
                manifest = read_json(manifest_path)
                manifest["master_after_test"] = restore_master
                write_manifest(manifest_path, manifest)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    plan_path = args.plan.resolve()
    prepared = preflight(plan_path)
    if args.validate_only:
        print(json.dumps({
            "status": "valid",
            "test_id": prepared["test_id"],
            "cases": [item["id"] for item in prepared["cases"]],
            "conditions": [item["name"] for item in prepared["conditions"]],
            "jobs": prepared["jobs"],
            "output": str(prepared["test_dir"]),
        }, ensure_ascii=False))
        return 0
    result = run(prepared)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
