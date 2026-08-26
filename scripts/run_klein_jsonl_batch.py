#!/usr/bin/env python3
"""Inspect historical combined Illustrious/Klein JSONL workflows.

Submission is intentionally disabled: ADA production uses two isolated jobs.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import math
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any

if __package__:
    from .ada_paths import COMFYUI_BASE_URL, KLEIN_BATCH_RUNS_ROOT, PROMPTS_ROOT
else:
    from ada_paths import COMFYUI_BASE_URL, KLEIN_BATCH_RUNS_ROOT, PROMPTS_ROOT


DEFAULT_DATASET = PROMPTS_ROOT / "klein_batch_100.jsonl"
RUNS_ROOT = KLEIN_BATCH_RUNS_ROOT
TARGET_NODES = {2, 5, 7, 20, 22, 38, 39}
KLEIN_LORA_NODE = "42"
KLEIN_SCHEDULER_NODE = "43"
KLEIN_MODEL_CONSUMER_NODE = "50"


def http_json(url: str, method: str = "GET", payload: Any | None = None, timeout: int = 30) -> Any:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"ComfyUI HTTP {exc.code}: {body}") from exc


def load_dataset(path: Path, take: int | None) -> list[dict[str, Any]]:
    required = ("id", "character", "illustrious_prompt", "klein_prompt", "illustrious_seed", "klein_seed")
    records: list[dict[str, Any]] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        record = json.loads(raw)
        if not isinstance(record, dict):
            raise ValueError(f"{path}:{line_number}: each line must be a JSON object")
        missing = [key for key in required if key not in record]
        if missing:
            raise ValueError(f"{path}:{line_number}: missing {', '.join(missing)}")
        for key in ("id", "character", "illustrious_prompt", "klein_prompt"):
            if not isinstance(record[key], str) or not record[key].strip():
                raise ValueError(f"{path}:{line_number}: {key} must be non-empty text")
        for key in ("illustrious_seed", "klein_seed"):
            if not isinstance(record[key], int) or isinstance(record[key], bool) or record[key] < 0:
                raise ValueError(f"{path}:{line_number}: {key} must be a non-negative integer")
        records.append(record)
    if take is not None:
        records = records[:take]
    ids = [record["id"] for record in records]
    if not records or len(ids) != len(set(ids)):
        raise ValueError("Dataset must be non-empty and contain unique ids")
    return records


def set_first_widget(nodes: dict[int, dict[str, Any]], node_id: int, value: Any) -> None:
    widgets = nodes[node_id].get("widgets_values")
    if not isinstance(widgets, list) or not widgets:
        raise ValueError(f"Node {node_id} has no first widget")
    widgets[0] = value


def illustrious_positive_with_subject_token(prompt: str) -> str:
    """Guarantee the Illustrious subject token once without changing other prompt text."""
    tags = [tag.strip().lower() for tag in prompt.split(",")]
    return prompt if "1girl" in tags else f"1girl, {prompt}"


def bind_record(base: dict[str, Any], record: dict[str, Any], output_root: str) -> dict[str, Any]:
    workflow = copy.deepcopy(base)
    nodes = {int(node["id"]): node for node in workflow["nodes"]}
    missing = TARGET_NODES - set(nodes)
    if missing:
        raise ValueError(f"Template is missing dynamic nodes: {sorted(missing)}")
    record_id = record["id"]
    set_first_widget(nodes, 2, illustrious_positive_with_subject_token(record["illustrious_prompt"]))
    set_first_widget(nodes, 39, record["klein_prompt"])
    set_first_widget(nodes, 5, int(record["illustrious_seed"]))
    set_first_widget(nodes, 38, int(record["klein_seed"]))
    set_first_widget(nodes, 7, f"{output_root}/{record_id}/illustrious")
    set_first_widget(nodes, 20, f"{output_root}/{record_id}/klein")
    set_first_widget(nodes, 22, f"{output_root}/{record_id}/compare")
    return workflow


WIDGET_INPUTS: dict[int, tuple[tuple[str, int], ...]] = {
    1: (("ckpt_name", 0),),
    2: (("text", 0),),
    3: (("text", 0),),
    4: (("width", 0), ("height", 1), ("batch_size", 2)),
    5: (("seed", 0), ("steps", 2), ("cfg", 3), ("sampler_name", 4), ("scheduler", 5), ("denoise", 6)),
    7: (("filename_prefix", 0),),
    13: (("upscale_method", 0), ("width", 1), ("height", 2), ("crop", 3)),
    20: (("filename_prefix", 0),),
    21: (("direction", 0), ("match_image_size", 1)),
    22: (("filename_prefix", 0),),
    37: (("vae_name", 0),),
    38: (("noise_seed", 0),),
    39: (("text", 0),),
    41: (("sampler_name", 0),),
    43: (("steps", 0), ("width", 1), ("height", 2)),
    45: (("unet_name", 0), ("weight_dtype", 1)),
    46: (("clip_name", 0), ("type", 1), ("device", 2)),
    47: (("guidance", 0),),
    50: (("sage_attention", 0), ("allow_compile", 1)),
    52: (("enable_fp16_accumulation", 0),),
    53: (("cfg", 0),),
}


def compile_api(workflow: dict[str, Any]) -> dict[str, Any]:
    links = {int(link[0]): (str(link[1]), int(link[2])) for link in workflow["links"]}
    prompt: dict[str, Any] = {}
    for node in workflow["nodes"]:
        node_id = int(node["id"])
        inputs: dict[str, Any] = {}
        for item in node.get("inputs", []):
            if item.get("link") is not None:
                inputs[item["name"]] = list(links[int(item["link"])])
        widgets = node.get("widgets_values") or []
        for name, index in WIDGET_INPUTS.get(node_id, ()):
            inputs[name] = widgets[index]
        if node_id == 42:
            lora = dict(widgets[2])
            lora.pop("strengthTwo", None)
            inputs["lora_1"] = lora
        prompt[str(node_id)] = {"class_type": node["type"], "inputs": inputs, "_meta": {"title": node.get("title", node["type"])}}
    return prompt


def load_klein_preset_plan(path: Path, records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Read a small external per-record Klein preset plan without changing JSONL."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or raw.get("schema_version") != 1:
        raise ValueError(f"{path}: expected schema_version 1")
    presets = raw.get("presets")
    assignments = raw.get("records")
    if not isinstance(presets, dict) or not isinstance(assignments, dict):
        raise ValueError(f"{path}: presets and records must be objects")

    record_ids = {record["id"] for record in records}
    assigned_ids = set(assignments)
    if record_ids != assigned_ids:
        missing = sorted(record_ids - assigned_ids)
        extra = sorted(assigned_ids - record_ids)
        details = []
        if missing:
            details.append(f"missing assignments: {missing}")
        if extra:
            details.append(f"unexpected assignments: {extra}")
        raise ValueError(f"{path}: " + "; ".join(details))

    resolved: dict[str, dict[str, Any]] = {}
    for record_id, preset_name in assignments.items():
        if not isinstance(preset_name, str) or preset_name not in presets:
            raise ValueError(f"{path}: {record_id} names an unknown preset")
        preset = presets[preset_name]
        if not isinstance(preset, dict):
            raise ValueError(f"{path}: preset {preset_name} must be an object")
        steps = preset.get("steps")
        loras = preset.get("loras")
        if not isinstance(steps, int) or isinstance(steps, bool) or steps < 1:
            raise ValueError(f"{path}: preset {preset_name} has invalid steps")
        if not isinstance(loras, list) or not loras:
            raise ValueError(f"{path}: preset {preset_name} needs at least one LoRA")
        normalized_loras: list[dict[str, Any]] = []
        for lora in loras:
            if not isinstance(lora, dict) or not isinstance(lora.get("lora"), str) or not lora["lora"].strip():
                raise ValueError(f"{path}: preset {preset_name} has an invalid LoRA name")
            strength = lora.get("strength")
            if isinstance(strength, bool) or not isinstance(strength, (int, float)) or not math.isfinite(strength):
                raise ValueError(f"{path}: preset {preset_name} has an invalid LoRA strength")
            normalized_loras.append({"lora": lora["lora"].replace("/", "\\"), "strength": float(strength)})
        resolved[record_id] = {"name": preset_name, "steps": steps, "loras": normalized_loras}
    return resolved


def apply_klein_preset(prompt: dict[str, Any], preset: dict[str, Any]) -> None:
    """Apply a validated LoRA chain and scheduler steps to a compiled API prompt."""
    for node_id in (KLEIN_LORA_NODE, KLEIN_SCHEDULER_NODE, KLEIN_MODEL_CONSUMER_NODE):
        if node_id not in prompt:
            raise ValueError(f"Workflow API prompt is missing Klein node {node_id}")

    prompt[KLEIN_SCHEDULER_NODE]["inputs"]["steps"] = preset["steps"]
    loras = preset["loras"]
    first = loras[0]
    prompt[KLEIN_LORA_NODE]["inputs"]["lora_1"] = {"on": True, **first}
    previous_node = KLEIN_LORA_NODE
    next_node_id = 1000
    for lora in loras[1:]:
        while str(next_node_id) in prompt:
            next_node_id += 1
        node_id = str(next_node_id)
        chained = copy.deepcopy(prompt[KLEIN_LORA_NODE])
        chained["inputs"]["model"] = [previous_node, 0]
        chained["inputs"]["lora_1"] = {"on": True, **lora}
        prompt[node_id] = chained
        previous_node = node_id
        next_node_id += 1
    prompt[KLEIN_MODEL_CONSUMER_NODE]["inputs"]["model"] = [previous_node, 0]


def sync_klein_preset_workflow(workflow: dict[str, Any], preset: dict[str, Any]) -> None:
    """Mirror the API LoRA chain in the UI workflow stored in PNG metadata."""
    nodes = {int(node["id"]): node for node in workflow["nodes"]}
    loader_id = int(KLEIN_LORA_NODE)
    scheduler_id = int(KLEIN_SCHEDULER_NODE)
    consumer_id = int(KLEIN_MODEL_CONSUMER_NODE)
    for node_id in (loader_id, scheduler_id, consumer_id):
        if node_id not in nodes:
            raise ValueError(f"Workflow metadata is missing Klein node {node_id}")

    loras = preset["loras"]
    loader = nodes[loader_id]
    widgets = loader.get("widgets_values")
    if not isinstance(widgets, list) or len(widgets) < 3 or not isinstance(widgets[2], dict):
        raise ValueError("Workflow metadata has no editable Klein LoRA widget")
    widgets[2] = {**widgets[2], "on": True, **loras[0]}

    scheduler_widgets = nodes[scheduler_id].get("widgets_values")
    if not isinstance(scheduler_widgets, list) or not scheduler_widgets:
        raise ValueError("Workflow metadata has no editable Klein scheduler widget")
    scheduler_widgets[0] = preset["steps"]

    if len(loras) == 1:
        return

    consumer_model_input = next(
        (item for item in nodes[consumer_id].get("inputs", []) if item.get("name") == "model"), None
    )
    if not isinstance(consumer_model_input, dict) or consumer_model_input.get("link") is None:
        raise ValueError("Workflow metadata has no Klein model-consumer link")
    final_link_id = int(consumer_model_input["link"])
    links = workflow.get("links")
    if not isinstance(links, list):
        raise ValueError("Workflow metadata has no links")
    final_link = next((link for link in links if int(link[0]) == final_link_id), None)
    if not isinstance(final_link, list) or int(final_link[1]) != loader_id:
        raise ValueError("Workflow metadata Klein model link does not start at the LoRA loader")

    next_node_id = 1000
    next_link_id = max(int(link[0]) for link in links) + 1
    previous_node = loader
    previous_node_id = loader_id
    for index, lora in enumerate(loras[1:], 2):
        while next_node_id in nodes:
            next_node_id += 1
        chained = copy.deepcopy(loader)
        chained["id"] = next_node_id
        chained["title"] = f"Klein LoRA {index}"
        chained["order"] = max(int(node.get("order", 0)) for node in workflow["nodes"]) + 1
        if isinstance(chained.get("pos"), list):
            chained["pos"] = [chained["pos"][0] + 380 * (index - 1), chained["pos"][1]]
        chained_widgets = chained["widgets_values"]
        chained_widgets[2] = {**chained_widgets[2], "on": True, **lora}
        model_input = next(item for item in chained["inputs"] if item.get("name") == "model")
        model_input["link"] = next_link_id
        model_output = next(item for item in chained["outputs"] if item.get("name") == "MODEL")
        model_output["links"] = [final_link_id]
        previous_output = next(item for item in previous_node["outputs"] if item.get("name") == "MODEL")
        previous_output["links"] = [next_link_id]
        links.append([next_link_id, previous_node_id, 0, next_node_id, 0, "MODEL"])
        workflow["nodes"].append(chained)
        nodes[next_node_id] = chained
        previous_node = chained
        previous_node_id = next_node_id
        next_node_id += 1
        next_link_id += 1
    final_link[1] = previous_node_id


def queue_state(server: str) -> tuple[int, int]:
    queue = http_json(f"{server}/queue")
    return len(queue.get("queue_running", [])), len(queue.get("queue_pending", []))


def submit(server: str, prompt: dict[str, Any], workflow: dict[str, Any], record_id: str) -> str:
    payload = {
        "prompt": prompt,
        "client_id": f"luna-klein-batch-{uuid.uuid4().hex}",
        "extra_data": {"extra_pnginfo": {"workflow": workflow, "batch_record_id": record_id}},
    }
    response = http_json(f"{server}/prompt", "POST", payload, timeout=60)
    if response.get("node_errors"):
        raise RuntimeError(json.dumps(response["node_errors"], ensure_ascii=False, indent=2))
    if not response.get("prompt_id"):
        raise RuntimeError(f"ComfyUI returned no prompt_id: {response}")
    return str(response["prompt_id"])


def wait_history(server: str, prompt_id: str, timeout_seconds: int) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        history = http_json(f"{server}/history/{prompt_id}")
        item = history.get(prompt_id)
        if item:
            status = item.get("status", {})
            if status.get("status_str") == "error":
                raise RuntimeError(json.dumps(status, ensure_ascii=False, indent=2))
            if item.get("outputs"):
                return item
        time.sleep(2)
    raise TimeoutError(f"Prompt {prompt_id} exceeded {timeout_seconds}s")


def descriptors(history: dict[str, Any], node_id: int) -> list[dict[str, Any]]:
    return history.get("outputs", {}).get(str(node_id), {}).get("images", [])


def write_manifest(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workflow", type=Path, required=True)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--server", default=COMFYUI_BASE_URL)
    parser.add_argument("--take", type=int)
    parser.add_argument("--expected-count", type=int)
    parser.add_argument("--batch-id")
    parser.add_argument("--progress-every", type=int, default=10)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--klein-preset-plan", type=Path,
                        help="Optional schema-v1 JSON plan that maps every record ID to Klein steps and LoRAs.")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    if not args.validate_only:
        raise RuntimeError(
            "Combined Illustrious/Klein submission is quarantined. "
            "Use ADA's isolated illustrious_only and klein_only production runtime."
        )
    records = load_dataset(args.dataset, args.take)
    if args.expected_count is not None and len(records) != args.expected_count:
        raise ValueError(f"Expected {args.expected_count} records, got {len(records)}")
    base = json.loads(args.workflow.read_text(encoding="utf-8"))
    presets = load_klein_preset_plan(args.klein_preset_plan, records) if args.klein_preset_plan else {}
    batch_id = args.batch_id or dt.datetime.now().strftime("%Y%m%d_%H%M%S_klein_batch")
    output_root = f"LunaKleinBatch/{batch_id}"
    # Fully compile every record before touching ComfyUI or creating a run directory.
    prepared: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    for record in records:
        bound = bind_record(base, record, output_root)
        prompt = compile_api(bound)
        if record["id"] in presets:
            apply_klein_preset(prompt, presets[record["id"]])
            sync_klein_preset_workflow(bound, presets[record["id"]])
        prepared[record["id"]] = (bound, prompt)
    if args.validate_only:
        print(json.dumps({"status": "valid", "count": len(records), "nodes": len(next(iter(prepared.values()))[1]), "batch_id": batch_id,
                          "klein_preset_plan": str(args.klein_preset_plan) if args.klein_preset_plan else None}))
        return 0
    running, pending = queue_state(args.server)
    if running or pending:
        raise RuntimeError(f"ComfyUI is busy: running={running}, pending={pending}")
    run_dir = RUNS_ROOT / batch_id
    manifest_path = run_dir / "manifest.json"
    if run_dir.exists():
        raise FileExistsError(f"Batch directory already exists and will not be overwritten: {run_dir}")
    manifest: dict[str, Any] = {
        "batch_id": batch_id,
        "status": "running",
        "workflow": str(args.workflow.resolve()),
        "dataset": str(args.dataset.resolve()),
        "count": len(records),
        "output_root": output_root,
        "klein_preset_plan": str(args.klein_preset_plan.resolve()) if args.klein_preset_plan else None,
        "records": [],
    }
    write_manifest(manifest_path, manifest)
    for index, record in enumerate(records, 1):
        bound, prompt = prepared[record["id"]]
        entry: dict[str, Any] = {"index": index, "id": record["id"], "status": "running"}
        if record["id"] in presets:
            entry["klein_preset"] = presets[record["id"]]
        manifest["records"].append(entry)
        write_manifest(manifest_path, manifest)
        try:
            prompt_id = submit(args.server, prompt, bound, record["id"])
            entry["prompt_id"] = prompt_id
            history = wait_history(args.server, prompt_id, args.timeout_seconds)
            entry.update(
                status="complete",
                illustrious=descriptors(history, 7),
                klein=descriptors(history, 20),
                compare=descriptors(history, 22),
            )
            if not entry["illustrious"] or not entry["klein"] or not entry["compare"]:
                raise RuntimeError(f"Missing outputs for {record['id']}")
        except Exception as exc:
            entry.update(status="failed", error=str(exc))
            manifest["status"] = "failed"
            write_manifest(manifest_path, manifest)
            raise
        write_manifest(manifest_path, manifest)
        if index % args.progress_every == 0 or index == len(records):
            print(json.dumps({"progress": index, "total": len(records), "id": record["id"]}, ensure_ascii=False), flush=True)
    manifest["status"] = "complete"
    manifest["completed_at"] = dt.datetime.now().astimezone().isoformat()
    write_manifest(manifest_path, manifest)
    print(json.dumps({"status": "complete", "batch_dir": str(run_dir.resolve())}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
