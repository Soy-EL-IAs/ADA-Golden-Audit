"""Explicit Reinterpret requests and their background renderer execution."""
from __future__ import annotations

import hashlib
import json
import threading
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ada_app.semantic_contracts import build_character_contract, build_resolved_render_spec_v2
from ada_app.render_prompt_compilers import build_renderer_prompt_artifact
from scripts.ada_paths import ADA_ROOT, COMFYUI_BASE_URL, LOCKS_ROOT, RENDERER_RUNS_ROOT
from scripts.agent_contracts import validate_contract
from scripts.lmstudio_controller import LMStudioController
from scripts.production_workflows import (
    build_renderer_workflow,
    production_renderer_preset,
    renderer_generation_details,
    renderer_workflow_path,
)
from scripts.run_specialist_mini_e2e import submit, wait_history, output_path

REQUEST_ROOT = RENDERER_RUNS_ROOT / "reinterpretations"
_START_LOCK = threading.Lock()
_ACTIVE: set[str] = set()


def _record_path(request_id: str) -> Path:
    if not request_id or Path(request_id).name != request_id:
        raise ValueError("Invalid reinterpretation request id")
    return REQUEST_ROOT / f"{request_id}.json"


def _write_record(record: dict[str, Any]) -> dict[str, Any]:
    REQUEST_ROOT.mkdir(parents=True, exist_ok=True)
    path = _record_path(record["request_id"])
    temp = path.with_suffix(".json.tmp")
    temp.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)
    return record


def get_reinterpretation(request_id: str) -> dict[str, Any]:
    path = _record_path(request_id)
    if not path.is_file():
        raise FileNotFoundError(request_id)
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Invalid reinterpretation record")
    return value


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def scene_template_from_asset(asset: dict[str, Any]) -> dict[str, Any]:
    spec = asset.get("resolved_render_spec", {}) if isinstance(asset.get("resolved_render_spec"), dict) else {}
    hook = spec.get("hook_premise", spec.get("concept", {})) if isinstance(spec, dict) else {}
    template = {"schema_version":"scene_template_spec_v1", "template_id":f"scene-template:{asset['asset_id']}:v1", "source_asset_id":asset["asset_id"], "hook_type":_text(hook.get("hook_type")) or "asset_scene", "snapshot":_text(hook.get("snapshot")) or _text(asset.get("concept_snapshot")), "core_action":_text(hook.get("core_action")) or _text(hook.get("provocative_mechanism")), "visual_hook":_text(hook.get("visual_hook")), "object_interaction":_text(hook.get("object_interaction")), "setting":_text(hook.get("setting")), "composition":_text(hook.get("composition_intent")) or _text(spec.get("composition_intent")), "expression":_text(hook.get("expression")), "preserve_from_source":["pose", "scene type", "object layout", "framing"], "must_not_preserve":["original character identity", "original franchise-specific face", "source-specific outfit identity if incompatible"]}
    return validate_contract("scene_template_spec_v1", template)


def create_reinterpretation(asset: dict[str, Any], target_name: str, target_entry: dict[str, Any], *, renderer: str, render_intent: str, template_mode: str) -> dict[str, Any]:
    if renderer not in {"lustify", "miaomiao"}: raise ValueError("Renderer must be Lustify or Miaomiao")
    if template_mode not in {"strict_composition", "balanced", "loose_inspiration"}: raise ValueError("Unknown template mode")
    target_profile = {"requested_character": target_name, "name": target_name, "matched_tag": target_entry.get("canonical_tag", ""), "characteristics": target_entry.get("characteristics", []), "clothing": target_entry.get("clothing", []), "copyright": target_entry.get("copyright", []), "version": target_entry.get("version", "")}
    contract = build_character_contract(target_profile, target_entry)
    template = scene_template_from_asset(asset)
    proposal = {"hook_type":template["hook_type"], "snapshot":template["snapshot"], "core_action":template["core_action"], "visual_hook":template["visual_hook"], "provocative_mechanism":template["visual_hook"], "object_interaction":template["object_interaction"], "setting":template["setting"], "composition_intent":template["composition"], "expression":template["expression"]}
    base = build_resolved_render_spec_v2(contract, f"reinterpret:{asset['asset_id']}", proposal, render_intent=render_intent)
    reinterpreted = {"schema_version":"reinterpreted_render_spec_v1", "spec_id":f"reinterpret-spec:{asset['asset_id']}:{contract['character_id']}:v1", "source_asset_id":asset["asset_id"], "scene_template_id":template["template_id"], "target_character_contract_id":contract["contract_id"], "target_character":base["character"], "render_intent":render_intent, "render_mode":"DIRECT_T2I", "template_mode":template_mode, "resolved_scene":base}
    validate_contract("reinterpreted_render_spec_v1", reinterpreted)
    preset = "lustify_krea2_primary_v1" if renderer == "lustify" else "miaomiao_anima16_secondary_v1"
    prompt = build_renderer_prompt_artifact(base, renderer=renderer, recipe_id=preset)
    request_id = f"reinterpret_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}_{contract['character_id']}"
    record = {"request_id":request_id, "status":"READY_FOR_RENDER", "created_at":datetime.now(timezone.utc).isoformat(), "mode":"direct_reinterpret", "source_asset_id":asset["asset_id"], "source_generation_id":asset.get("generation_id", ""), "target_character":target_name, "renderer":renderer, "render_intent":render_intent, "template_mode":template_mode, "scene_template_spec":template, "target_character_contract":contract, "reinterpreted_render_spec":reinterpreted, "renderer_prompt_artifact":prompt, "capability_note":"DIRECT_T2I uses the persisted semantic scene template. No source pixels or unvalidated image adapter are injected."}
    return _write_record(record)


def _execute_reinterpretation(request_id: str) -> None:
    try:
        record = get_reinterpretation(request_id)
        record.update({"status":"PREPARING_RENDER", "started_at":datetime.now(timezone.utc).isoformat()})
        _write_record(record)
        renderer = record["renderer"]
        preset_id = record["renderer_prompt_artifact"]["recipe_id"]
        preset = production_renderer_preset(preset_id)
        if preset.get("renderer") != renderer:
            raise ValueError("Reinterpretation renderer and preset do not match")
            
        import filelock
        LOCKS_ROOT.mkdir(parents=True, exist_ok=True)
        lock = filelock.FileLock(str(LOCKS_ROOT / "gpu_execution.lock"))
        
        with lock.acquire(timeout=86400):
            controller = LMStudioController()
            handoff = controller.prepare_for_comfy(lambda: controller.comfy_status(COMFYUI_BASE_URL))
            seed = int.from_bytes(hashlib.sha256(request_id.encode("utf-8")).digest()[:8], "big") & 0x7fffffff
            workflow = build_renderer_workflow(
                preset_id=preset_id,
                positive_prompt=record["renderer_prompt_artifact"]["prompt"],
                seed=seed,
                output_prefix=f"AdaReinterpret/{request_id}/{renderer}",
            )
            artifact_dir = REQUEST_ROOT / request_id
            artifact_dir.mkdir(parents=True, exist_ok=True)
            workflow_path = artifact_dir / "workflow.json"
        workflow_path.write_text(json.dumps(workflow, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        prompt_id = submit(COMFYUI_BASE_URL, workflow, request_id)
        record.update({"status":"RENDERING", "prompt_id":prompt_id, "seed":seed, "resource_handoff":handoff, "workflow_artifact":str(workflow_path.resolve())})
        _write_record(record)
        history = wait_history(COMFYUI_BASE_URL, prompt_id)
        image = output_path(history, str(preset["output_node"]))
        generation = renderer_generation_details(preset_id, workflow)
        receipt = {
            "schema_version":"render_receipt_v2", "receipt_id":f"render:{request_id}",
            "renderer":renderer, "preset":preset_id, "attempt":1,
            "render_spec_id":record["reinterpreted_render_spec"]["spec_id"],
            "stage_render_plan_id":f"reinterpret-plan:{request_id}",
            "prompt_artifact_id":record["renderer_prompt_artifact"]["prompt_id"],
            "workflow":str(renderer_workflow_path(preset_id).resolve()),
            "generation":generation,
            "submission":{"prompt_id":prompt_id, "request_id":request_id, "source_asset_id":record["source_asset_id"]},
            "output_asset":str(image.resolve()),
        }
        validate_contract("render_receipt_v2", receipt)
        receipt_path = artifact_dir / "render_receipt.json"
        receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        record.update({"status":"REGISTERING", "output_asset":str(image.resolve()), "render_receipt":receipt, "render_receipt_artifact":str(receipt_path.resolve())})
        _write_record(record)
        from ada_app.asset_library import AssetLibrary
        library_asset = AssetLibrary().register_reinterpretation({**record, "status":"COMPLETE"})
        record["library_asset_id"] = library_asset["asset_id"]
        record["status"] = "RELEASING_RESOURCES"
        _write_record(record)
        try:
            release = controller.request_comfy_unload(COMFYUI_BASE_URL)
            released = controller.wait_for_comfy_vram_release(lambda: controller.comfy_status(COMFYUI_BASE_URL))
            record["comfy_release"] = {"request":release, "vram":released}
        except Exception as release_exc:
            record["comfy_release_warning"] = f"{type(release_exc).__name__}: {release_exc}"
        record["status"] = "COMPLETE"
        record["completed_at"] = datetime.now(timezone.utc).isoformat()
        _write_record(record)
    except Exception as exc:
        try:
            record = get_reinterpretation(request_id)
        except Exception:
            record = {"request_id":request_id}
        record.update({"status":"FAILED", "failed_at":datetime.now(timezone.utc).isoformat(), "error":{"exception_type":type(exc).__name__, "message":str(exc), "traceback":traceback.format_exc()}})
        _write_record(record)
    finally:
        with _START_LOCK:
            _ACTIVE.discard(request_id)


def start_reinterpretation(request_id: str) -> dict[str, Any]:
    with _START_LOCK:
        record = get_reinterpretation(request_id)
        if record.get("status") not in {"READY_FOR_RENDER", "FAILED"}:
            return record
        if request_id in _ACTIVE:
            return record
        record["status"] = "QUEUED"
        record.pop("error", None)
        _write_record(record)
        _ACTIVE.add(request_id)
        thread = threading.Thread(target=_execute_reinterpretation, args=(request_id,), name=f"reinterpret-{request_id}", daemon=True)
        thread.start()
        return record
