#!/usr/bin/env python3
"""Local LM Studio agent for the reusable Illustrious -> Klein pipeline."""

from __future__ import annotations

import base64
import html
import json
import mimetypes
import os
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

if __package__:
    from .ada_paths import (
        ADA_ROOT, COMFYUI_BASE_URL, COMFYUI_ROOT, CONFIG_ROOT,
        KLEIN_BATCH_RUNS_ROOT, LMSTUDIO_BASE_URL, PROMPTS_ROOT, WORKFLOWS_ROOT,
    )
    from .character_dataset import CharacterDatasetBuilder
    from .character_ref_cache import CharacterReferenceCache
    from .character_refs import CharacterReferenceFinder
    from .lmstudio_controller import LMStudioController, PipelineState
    from .local_search import SearXNGClient
    from .run_klein_jsonl_batch import apply_klein_preset, bind_record, compile_api, load_dataset, load_klein_preset_plan
    from .visual_reviewer import review_image
else:
    from ada_paths import (
        ADA_ROOT, COMFYUI_BASE_URL, COMFYUI_ROOT, CONFIG_ROOT,
        KLEIN_BATCH_RUNS_ROOT, LMSTUDIO_BASE_URL, PROMPTS_ROOT, WORKFLOWS_ROOT,
    )
    from character_dataset import CharacterDatasetBuilder
    from character_ref_cache import CharacterReferenceCache
    from character_refs import CharacterReferenceFinder
    from lmstudio_controller import LMStudioController, PipelineState
    from local_search import SearXNGClient
    from run_klein_jsonl_batch import apply_klein_preset, bind_record, compile_api, load_dataset, load_klein_preset_plan
    from visual_reviewer import review_image

ROOT = ADA_ROOT
LM_BASE = LMSTUDIO_BASE_URL
CONTROLLER = LMStudioController()
LOCAL_SEARCH = SearXNGClient()
CHARACTER_REFS = CharacterReferenceFinder(LOCAL_SEARCH)
CHARACTER_REF_CACHE = CharacterReferenceCache(CHARACTER_REFS)
CHARACTER_DATASETS = CharacterDatasetBuilder(refs_root=CHARACTER_REF_CACHE.root)
MODEL = os.environ.get("LM_STUDIO_MODEL", CONTROLLER.role("master").model)
COMFY_URL = COMFYUI_BASE_URL
RUNNER = ROOT / "scripts" / "run_klein_jsonl_batch.py"
WORKFLOW: Path | None = None
RUNS_ROOT = KLEIN_BATCH_RUNS_ROOT
CONFIG = json.loads((CONFIG_ROOT / "pipeline.json").read_text(encoding="utf-8"))
COMFY_ROOT = COMFYUI_ROOT or Path(CONFIG["comfy_root"])


SYSTEM_PROMPT = """You are the local operator for one reusable ComfyUI Illustrious -> Klein pipeline.
Speak Spanish and keep answers concise. Use tools instead of inventing status.
The characters are JSONL data; never create a workflow per character.
Never modify existing prompts, seeds, models, LoRAs, VAE, sampler, guidance, graph connections or workflow files.
For future prompts, describe composition only as viewpoint and framing; never name a physical camera, lens, photographer or filming equipment to express an angle or crop.
Before a heavy batch, call comfy_status. Never start when ComfyUI is busy.
For a new dataset, run a small pilot JSONL first, review every result, and only then run a larger approved dataset.
run_batch waits locally without further model inference; do not repeatedly poll while it runs.
Do not retry a failed render automatically. Report the exact error.
Never claim an image was reviewed unless review_batch returned a result.
For curated character references use find_character_refs; do not replace its mechanical filtering with LLM judgment.
When find_character_refs returns filtered and scored references, summarize them directly; do not re-rank them or spend prolonged reasoning on mechanical selection.
Use cache_character_refs only when the user explicitly asks to persist references. Never retry failed downloads automatically.
generate_character_dataset reads the local booru-characters profile before the Master writes prompts. When
character_profile_used is true, use its characteristics and clothing as identity facts; do not invent
contradictory basics and do not mechanically paste its tags into prompts.
The returned character_profile is already the local lookup result. Do not call get_character_profile again
unless the user explicitly asks to inspect or debug that profile.
When the user asks for a new character dataset, call generate_character_dataset first. It creates a local
staging plan with the distribution, prompt rules and available local-reference context. You, the Master,
must author 5-10 semantic entries at a time and call append_character_dataset_entries after each chunk.
When the exact total is staged, call finalize_character_dataset. Do not use persist_character_dataset for
new datasets because a complete entry list does not scale.
Do not search for or download references automatically. Do not replace creative prompts with rigid templates.
After persistence, report the returned run_batch arguments; never start rendering unless separately requested.
When PIPELINE_ORCHESTRATION=1, run_batch explicitly unloads every LLM and waits
for VRAM release before ComfyUI. During GENERATING/WAITING, do not request LLM inference.
"""


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "find_character_refs",
            "description": "Two-stage deterministic character-reference selection: trusted web pages and their image metadata first, one general image-search fallback at most. Separates provenance, relevance and technical quality; downloads no images.",
            "parameters": {
                "type": "object",
                "properties": {
                    "character": {"type": "string"},
                    "version": {"type": ["string", "null"]},
                    "limit": {"type": "integer", "minimum": 1, "maximum": 12},
                },
                "required": ["character"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_character_profile",
            "description": "Inspection/debug only: read a conservative local identity profile from booru-characters. generate_character_dataset already performs this lookup for normal dataset creation. Returns raw tag categories and candidates only; no web search, download or rendering.",
            "parameters": {
                "type": "object",
                "properties": {
                    "character": {"type": "string"},
                    "version": {"type": ["string", "null"]}
                },
                "required": ["character"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "append_character_dataset_entries",
            "description": "Append one small Master-authored chunk (maximum 10 entries) to an existing dataset staging plan. Checks basic structure and duplicate IDs/seeds across all staged chunks. Does not render or finalize.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dataset_id": {"type": "string"},
                    "entries": {
                        "type": "array",
                        "minItems": 1,
                        "maxItems": 10,
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "category": {"type": "string", "enum": ["closeup", "medium", "fullbody", "dynamic", "cinematic"]},
                                "premise": {"type": "string"},
                                "illustrious_prompt": {"type": "string"},
                                "klein_prompt": {"type": "string"},
                                "illustrious_seed": {"type": "integer", "minimum": 0},
                                "klein_seed": {"type": "integer", "minimum": 0}
                            },
                            "required": ["id", "category", "premise", "illustrious_prompt", "klein_prompt", "illustrious_seed", "klein_seed"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["dataset_id", "entries"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "finalize_character_dataset",
            "description": "Validate all staged chunks and, only if the full dataset is valid, create the final JSONL and Klein preset plan. Keeps staging unchanged on failure. Never renders.",
            "parameters": {
                "type": "object",
                "properties": {
                    "character": {"type": "string"},
                    "version": {"type": ["string", "null"]},
                    "count": {"type": "integer", "minimum": 1, "maximum": 100},
                    "dataset_id": {"type": "string"}
                },
                "required": ["character", "count", "dataset_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cache_character_refs",
            "description": "Find and download 2-5 reusable character references once. Reuses an existing valid cache, never overwrites prior content and never retries failed downloads.",
            "parameters": {
                "type": "object",
                "properties": {
                    "character": {"type": "string"},
                    "version": {"type": ["string", "null"]},
                    "limit": {"type": ["integer", "null"], "minimum": 2, "maximum": 5},
                },
                "required": ["character"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_character_dataset",
            "description": "Phase 1: create a new empty staging plan with automatic distribution by default, or an explicit valid category plan when categories is supplied. Includes prompt rules, safe local-reference context and any available local character_profile.",
            "parameters": {
                "type": "object",
                "properties": {
                    "character": {"type": "string"},
                    "version": {"type": ["string", "null"]},
                    "count": {"type": "integer", "minimum": 1, "maximum": 100, "default": 20},
                    "dataset_id": {"type": ["string", "null"]},
                    "categories": {"type": ["array", "null"], "items": {"type": "string"}},
                },
                "required": ["character"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_character_dataset_prompt_guidance",
            "description": "After premises are selected for an active staging dataset, return the versioned Illustrious and Klein guides needed to write their prompts. This does not render or modify entries.",
            "parameters": {
                "type": "object",
                "properties": {"dataset_id": {"type": "string"}},
                "required": ["dataset_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "persist_character_dataset",
            "description": "Legacy compatibility only: persist a complete small dataset in one call. New datasets must use append_character_dataset_entries and finalize_character_dataset.",
            "parameters": {
                "type": "object",
                "properties": {
                    "character": {"type": "string"},
                    "version": {"type": ["string", "null"]},
                    "count": {"type": "integer", "minimum": 1, "maximum": 100},
                    "dataset_id": {"type": "string"},
                    "entries": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "category": {"type": "string", "enum": ["closeup", "medium", "fullbody", "dynamic", "cinematic"]},
                                "premise": {"type": "string"},
                                "illustrious_prompt": {"type": "string"},
                                "klein_prompt": {"type": "string"},
                                "illustrious_seed": {"type": "integer", "minimum": 0},
                                "klein_seed": {"type": "integer", "minimum": 0},
                            },
                            "required": [
                                "id", "category", "premise", "illustrious_prompt", "klein_prompt",
                                "illustrious_seed", "klein_seed"
                            ],
                            "additionalProperties": False,
                        },
                    },
                },
                "required": ["character", "count", "dataset_id", "entries"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web through opt-in local SearXNG and return metadata/URLs only. Does not download or render content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "minimum": 1, "maximum": 30},
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_images",
            "description": "Search images through opt-in local SearXNG and return source page, image/thumbnail URLs and metadata only. Does not download or render images.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "minimum": 1, "maximum": 30},
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "comfy_status",
            "description": "Check whether local ComfyUI is idle.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "orchestration_status",
            "description": "Read the Master/Worker orchestration state and LM Studio model inventory. Does not load, unload, generate, or review.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "load_master",
            "description": "Load the configured Qwen3.8 Master through LM Studio v1. Manual/diagnostic action; do not use during GENERATING or WAITING.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "unload_master",
            "description": "Unload configured Master instances through LM Studio v1.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "load_worker",
            "description": "Load the configured Qwen3-VL Vision Worker through LM Studio v1. Manual/diagnostic action; do not use during GENERATING or WAITING.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "unload_worker",
            "description": "Unload configured Vision Worker instances through LM Studio v1.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "unload_all_llms",
            "description": "Unload every LLM known to LM Studio through its v1 API, then wait until none are reported loaded. Does not start ComfyUI.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "batch_status",
            "description": "Read a Klein batch manifest without generating anything.",
            "parameters": {
                "type": "object",
                "properties": {"batch_id": {"type": "string"}},
                "required": ["batch_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_batch",
            "description": "Validate and run every record in a JSONL dataset under prompts/. The record count is read from the file. This tool waits locally until completion without consuming model tokens.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dataset": {"type": "string", "description": "JSONL filename in prompts/, or a path contained within prompts/."},
                    "batch_id": {"type": "string", "description": "New unique batch identifier using letters, digits, underscores or hyphens."},
                    "klein_preset_plan": {
                        "type": ["string", "null"],
                        "description": "Optional JSON filename in config/, or a path contained within config/."
                    },
                },
                "required": ["dataset", "batch_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "review_batch",
            "description": "Use this same local vision model to review completed side-by-side comparisons and write review.json.",
            "parameters": {
                "type": "object",
                "properties": {
                    "batch_id": {"type": "string"},
                    "limit": {"type": "integer", "minimum": 1, "maximum": 100},
                },
                "required": ["batch_id", "limit"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "deep_review_batch",
            "description": "Run a deeper review with the configured Master. With orchestration enabled it unloads Worker, waits for VRAM release, then loads Master.",
            "parameters": {
                "type": "object",
                "properties": {"batch_id": {"type": "string"}, "limit": {"type": "integer", "minimum": 1, "maximum": 100}},
                "required": ["batch_id", "limit"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "build_gallery",
            "description": "Create a local HTML gallery from a completed or partial Klein batch manifest.",
            "parameters": {
                "type": "object",
                "properties": {"batch_id": {"type": "string"}},
                "required": ["batch_id"],
                "additionalProperties": False,
            },
        },
    },
]


def http_json(url: str, method: str = "GET", payload: Any | None = None, timeout: int = 120) -> Any:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {body}") from exc


def safe_batch_id(value: str) -> str:
    if not value or len(value) > 80 or any(not (char.isalnum() or char in "_-") for char in value):
        raise ValueError("batch_id may contain only letters, digits, underscores and hyphens")
    return value


def manifest_path(batch_id: str) -> Path:
    return RUNS_ROOT / safe_batch_id(batch_id) / "manifest.json"


def summarize_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    records = manifest.get("records", [])
    return {
        "batch_id": manifest.get("batch_id"),
        "status": manifest.get("status"),
        "expected": manifest.get("count"),
        "records": len(records),
        "complete": sum(item.get("status") == "complete" for item in records),
        "failed": sum(item.get("status") == "failed" for item in records),
        "last_id": records[-1].get("id") if records else None,
        "manifest": str(manifest_path(str(manifest.get("batch_id"))).resolve()),
    }


def tool_comfy_status() -> dict[str, Any]:
    queue = http_json(f"{COMFY_URL}/queue", timeout=10)
    running = len(queue.get("queue_running", []))
    pending = len(queue.get("queue_pending", []))
    return {"idle": running == 0 and pending == 0, "running": running, "pending": pending}


def tool_search_web(query: str, limit: int = 10) -> dict[str, Any]:
    return LOCAL_SEARCH.web(query, limit)


def tool_search_images(query: str, limit: int = 10) -> dict[str, Any]:
    return LOCAL_SEARCH.images(query, limit)


def tool_find_character_refs(character: str, version: str | None = None, limit: int = 6) -> dict[str, Any]:
    return CHARACTER_REFS.find(character, version, limit)


def tool_cache_character_refs(
    character: str,
    version: str | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    return CHARACTER_REF_CACHE.cache(character, version, limit)


def tool_get_character_profile(character: str, version: str | None = None) -> dict[str, Any]:
    return CHARACTER_DATASETS.get_character_profile(character, version)


def tool_generate_character_dataset(
    character: str,
    version: str | None = None,
    count: int = 20,
    dataset_id: str | None = None,
    categories: list[str] | None = None,
) -> dict[str, Any]:
    return CHARACTER_DATASETS.prepare(character, version, count, dataset_id, categories)


def tool_get_character_dataset_prompt_guidance(dataset_id: str) -> dict[str, Any]:
    return CHARACTER_DATASETS.get_prompt_guidance(dataset_id)


def tool_persist_character_dataset(
    character: str,
    count: int,
    dataset_id: str,
    entries: list[dict[str, Any]],
    version: str | None = None,
) -> dict[str, Any]:
    return CHARACTER_DATASETS.persist(character, entries, version, count, dataset_id)


def tool_append_character_dataset_entries(
    dataset_id: str,
    entries: list[dict[str, Any]],
) -> dict[str, Any]:
    return CHARACTER_DATASETS.append(dataset_id, entries)


def tool_finalize_character_dataset(
    character: str,
    count: int,
    dataset_id: str,
    version: str | None = None,
) -> dict[str, Any]:
    return CHARACTER_DATASETS.finalize(character, version, count, dataset_id)


def tool_orchestration_status() -> dict[str, Any]:
    return {
        "enabled": CONTROLLER.enabled,
        "state": CONTROLLER.state.value,
        "master": CONTROLLER.role("master").model,
        "worker": CONTROLLER.role("worker").model,
        "models": CONTROLLER.list_models(),
    }


def _guard_manual_model_action() -> None:
    if CONTROLLER.state in {PipelineState.GENERATING, PipelineState.WAITING}:
        raise RuntimeError(f"LLM model action is prohibited while state is {CONTROLLER.state.value}")


def tool_load_master() -> dict[str, Any]:
    _guard_manual_model_action()
    return CONTROLLER.load("master")


def tool_unload_master() -> dict[str, Any]:
    return {"role": "master", "unloaded": CONTROLLER.unload_role("master")}


def tool_load_worker() -> dict[str, Any]:
    _guard_manual_model_action()
    return CONTROLLER.load("worker")


def tool_unload_worker() -> dict[str, Any]:
    return {"role": "worker", "unloaded": CONTROLLER.unload_role("worker")}


def tool_unload_all_llms() -> dict[str, Any]:
    _guard_manual_model_action()
    unloaded = CONTROLLER.unload_all()
    return {"unloaded": unloaded, "vram": CONTROLLER.wait_for_vram_release()}


def tool_batch_status(batch_id: str) -> dict[str, Any]:
    path = manifest_path(batch_id)
    if not path.exists():
        return {"exists": False, "batch_id": batch_id}
    return {"exists": True, **summarize_manifest(json.loads(path.read_text(encoding="utf-8")))}


def safe_dataset_path(value: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("dataset must be a JSONL filename or path under prompts/")
    requested = Path(value.strip())
    if requested.is_absolute():
        candidate = requested
    elif requested.parts and requested.parts[0].lower() == "prompts":
        candidate = ROOT / requested
    else:
        candidate = PROMPTS_ROOT / requested
    resolved = candidate.resolve()
    try:
        resolved.relative_to(PROMPTS_ROOT.resolve())
    except ValueError as exc:
        raise ValueError("dataset must remain inside the prompts directory") from exc
    if resolved.suffix.lower() != ".jsonl":
        raise ValueError("dataset must be a .jsonl file")
    if not resolved.is_file():
        raise FileNotFoundError(resolved)
    return resolved


def safe_klein_preset_plan_path(value: str | None) -> Path | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError("klein_preset_plan must be a JSON filename or path under config/")
    requested = Path(value.strip())
    candidate = ROOT / requested if requested.parts and requested.parts[0].lower() == "config" else CONFIG_ROOT / requested
    resolved = candidate.resolve()
    try:
        resolved.relative_to(CONFIG_ROOT.resolve())
    except ValueError as exc:
        raise ValueError("klein_preset_plan must remain inside the config directory") from exc
    if resolved.suffix.lower() != ".json" or not resolved.is_file():
        raise ValueError("klein_preset_plan must be an existing .json file")
    return resolved


def validate_batch_inputs(dataset: Path, batch_id: str, klein_preset_plan: Path | None = None) -> int:
    if WORKFLOW is None:
        raise RuntimeError("Legacy combined batch validation is disabled; use the isolated production pipeline.")
    records = load_dataset(dataset, take=None)
    base = json.loads(WORKFLOW.read_text(encoding="utf-8"))
    output_root = f"LunaKleinBatch/{batch_id}"
    presets = load_klein_preset_plan(klein_preset_plan, records) if klein_preset_plan else {}
    for record in records:
        prompt = compile_api(bind_record(base, record, output_root))
        if record["id"] in presets:
            apply_klein_preset(prompt, presets[record["id"]])
    return len(records)


def tool_run_batch(dataset: str, batch_id: str, klein_preset_plan: str | None = None) -> dict[str, Any]:
    raise RuntimeError("Legacy combined batch execution is disabled; use the isolated production pipeline.")
    batch_id = safe_batch_id(batch_id)
    dataset_path = safe_dataset_path(dataset)
    preset_plan_path = safe_klein_preset_plan_path(klein_preset_plan)
    target_dir = RUNS_ROOT / batch_id
    if target_dir.exists():
        raise FileExistsError(f"Batch already exists and will not be overwritten: {target_dir}")

    # All local input validation happens before any LLM unload, state change or
    # ComfyUI request. The runner repeats these checks before creating a run.
    count = validate_batch_inputs(dataset_path, batch_id, preset_plan_path)
    restore_master: dict[str, Any] | None = None
    if CONTROLLER.enabled:
        try:
            CONTROLLER.prepare_for_comfy(tool_comfy_status)
        except Exception as preflight_error:
            # The MCP host still needs the Master to turn the tool error into a
            # final chat response. PREPARING/WAITING is over before restoring it.
            CONTROLLER.finish_work()
            try:
                CONTROLLER.ensure_loaded("master")
            except Exception as restore_error:
                raise RuntimeError(
                    f"Batch preflight failed ({preflight_error}); Master restore also failed ({restore_error})"
                ) from preflight_error
            raise
    else:
        status = tool_comfy_status()
        if not status["idle"]:
            raise RuntimeError(f"ComfyUI is busy: {status}")
    command = [
        sys.executable,
        str(RUNNER),
        "--workflow", str(WORKFLOW),
        "--dataset", str(dataset_path),
        "--expected-count", str(count),
        "--batch-id", batch_id,
        "--progress-every", str(max(1, min(10, count))),
    ]
    if preset_plan_path:
        command.extend(["--klein-preset-plan", str(preset_plan_path)])
    print(f"\n[operador] Iniciando {count} registros. El modelo queda en espera...", flush=True)
    output: list[str] = []
    code = -1
    try:
        process = subprocess.Popen(
            command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace",
        )
        assert process.stdout is not None
        for line in process.stdout:
            line = line.rstrip()
            output.append(line)
            print(f"[runner] {line}", flush=True)
        code = process.wait()
    finally:
        if CONTROLLER.enabled:
            # At this point the runner has exited: GENERATING/WAITING is over.
            # Restore Master before returning the MCP tool result so LM Studio
            # can safely produce the post-tool response without relying on JIT.
            CONTROLLER.finish_work()
            restore_master = CONTROLLER.ensure_loaded("master")
    result = tool_batch_status(batch_id)
    result.update(dataset=str(dataset_path), count=count, klein_preset_plan=str(preset_plan_path) if preset_plan_path else None,
                  exit_code=code, tail=output[-10:])
    if restore_master is not None:
        result["master_after_batch"] = restore_master
    if code != 0:
        result["error"] = "Runner stopped; no automatic retry was attempted."
    return result


def image_path(descriptor: dict[str, Any]) -> Path:
    folder = {"output": "output", "input": "input", "temp": "temp"}.get(descriptor.get("type", "output"))
    if folder is None:
        raise ValueError(f"Unsupported image type: {descriptor.get('type')}")
    return COMFY_ROOT / folder / descriptor.get("subfolder", "") / descriptor["filename"]


def image_data_url(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def vision_review(record_id: str, path: Path, model: str, ttl_seconds: int | None) -> dict[str, Any]:
    review = review_image(
        path, comparison_image=path, context={"record_id": record_id}, model=model,
        base_url=LM_BASE, ttl_seconds=ttl_seconds,
    )
    return {"id": record_id, "compare": str(path.resolve()), **review}


def tool_review_batch(batch_id: str, limit: int, deep: bool = False) -> dict[str, Any]:
    path = manifest_path(batch_id)
    if not path.exists():
        raise FileNotFoundError(path)
    manifest = json.loads(path.read_text(encoding="utf-8"))
    review_model = MODEL
    review_role = CONTROLLER.role("master" if deep else "worker")
    if CONTROLLER.enabled:
        review_role = CONTROLLER.begin_review(deep=deep)
        review_model = review_role.model
    reviews: list[dict[str, Any]] = []
    try:
        for record in manifest.get("records", []):
            if len(reviews) >= limit:
                break
            if record.get("status") != "complete" or not record.get("compare"):
                continue
            compare_path = image_path(record["compare"][0])
            print(f"[visión] Revisando {record['id']}...", flush=True)
            reviews.append(vision_review(record["id"], compare_path, review_model, review_role.ttl_seconds))
    finally:
        if CONTROLLER.enabled:
            CONTROLLER.finish_work()
    output = path.parent / "review.json"
    report = {
        "batch_id": batch_id,
        "model": review_model,
        "reviewed_at": datetime.now().astimezone().isoformat(),
        "count": len(reviews),
        "pass": sum(item.get("verdict") == "PASS" for item in reviews),
        "review": sum(item.get("verdict") == "REVIEW" for item in reviews),
        "reject": sum(item.get("verdict") == "REJECT" for item in reviews),
        "reviews": reviews,
    }
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {key: report[key] for key in ("batch_id", "model", "count", "pass", "review", "reject")} | {"report": str(output.resolve())}


def relative_file_uri(path: Path, gallery_dir: Path) -> str:
    try:
        return os.path.relpath(path.resolve(), gallery_dir.resolve()).replace("\\", "/")
    except ValueError:
        # Windows cannot form a relative path across drives (for example C: -> D:).
        return path.resolve().as_uri()


def tool_build_gallery(batch_id: str) -> dict[str, Any]:
    path = manifest_path(batch_id)
    if not path.exists():
        raise FileNotFoundError(path)
    manifest = json.loads(path.read_text(encoding="utf-8"))
    cards: list[str] = []
    for record in manifest.get("records", []):
        if record.get("status") != "complete" or not record.get("compare"):
            continue
        compare = image_path(record["compare"][0])
        cards.append(
            '<article><h2>' + html.escape(record["id"]) + '</h2>'
            + '<a href="' + html.escape(relative_file_uri(compare, path.parent)) + '">'
            + '<img loading="lazy" src="' + html.escape(relative_file_uri(compare, path.parent)) + '"></a></article>'
        )
    output = path.parent / "gallery.html"
    document = f"""<!doctype html><meta charset="utf-8"><title>{html.escape(batch_id)}</title>
<style>body{{font-family:system-ui;background:#111;color:#eee;margin:24px}}main{{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:18px}}article{{background:#1d1d1d;padding:12px;border-radius:12px}}img{{width:100%;height:auto;border-radius:8px}}h1,h2{{margin:.3rem 0 .7rem}}</style>
<h1>{html.escape(batch_id)} — {len(cards)} comparaciones</h1><main>{''.join(cards)}</main>"""
    output.write_text(document, encoding="utf-8")
    return {"batch_id": batch_id, "images": len(cards), "gallery": str(output.resolve())}


TOOL_FUNCTIONS: dict[str, Callable[..., Any]] = {
    "find_character_refs": tool_find_character_refs,
    "cache_character_refs": tool_cache_character_refs,
    "get_character_profile": tool_get_character_profile,
    "generate_character_dataset": tool_generate_character_dataset,
    "get_character_dataset_prompt_guidance": tool_get_character_dataset_prompt_guidance,
    "persist_character_dataset": tool_persist_character_dataset,
    "append_character_dataset_entries": tool_append_character_dataset_entries,
    "finalize_character_dataset": tool_finalize_character_dataset,
    "search_web": tool_search_web,
    "search_images": tool_search_images,
    "orchestration_status": tool_orchestration_status,
    "load_master": tool_load_master,
    "unload_master": tool_unload_master,
    "load_worker": tool_load_worker,
    "unload_worker": tool_unload_worker,
    "unload_all_llms": tool_unload_all_llms,
    "comfy_status": tool_comfy_status,
    "batch_status": tool_batch_status,
    "run_batch": tool_run_batch,
    "review_batch": tool_review_batch,
    "deep_review_batch": lambda batch_id, limit: tool_review_batch(batch_id, limit, deep=True),
    "build_gallery": tool_build_gallery,
}


def chat_completion(messages: list[dict[str, Any]]) -> dict[str, Any]:
    payload = {
        "model": MODEL,
        "messages": messages,
        "tools": TOOLS,
        "tool_choice": "auto",
        "temperature": 0.1,
        "max_tokens": int(CHARACTER_DATASETS.config.get("master_max_output_tokens", 4096)),
    }
    response = http_json(f"{LM_BASE}/v1/chat/completions", "POST", payload, timeout=300)
    return response["choices"][0]["message"]


def agent_turn(messages: list[dict[str, Any]], user_text: str) -> str:
    messages.append({"role": "user", "content": user_text})
    for _ in range(12):
        message = chat_completion(messages)
        messages.append(message)
        calls = message.get("tool_calls") or []
        if not calls:
            return message.get("content") or "Listo."
        for call in calls:
            name = call["function"]["name"]
            try:
                arguments = json.loads(call["function"].get("arguments") or "{}")
                if name not in TOOL_FUNCTIONS:
                    raise ValueError(f"Unknown tool: {name}")
                result = TOOL_FUNCTIONS[name](**arguments)
            except Exception as exc:
                result = {"error": f"{type(exc).__name__}: {exc}"}
            messages.append({"role": "tool", "tool_call_id": call["id"], "content": json.dumps(result, ensure_ascii=False)})
    raise RuntimeError("The local model exceeded the tool-call limit")


def main() -> int:
    print("Operador local Illustrious -> Klein")
    print(f"Modelo: {MODEL} | LM Studio: {LM_BASE}")
    print("Escribí 'salir' para cerrar.\n")
    messages: list[dict[str, Any]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    while True:
        try:
            user_text = input("Vos> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if user_text.lower() in {"salir", "exit", "quit"}:
            return 0
        if not user_text:
            continue
        try:
            print(f"Operador> {agent_turn(messages, user_text)}\n")
        except Exception as exc:
            print(f"Error local: {type(exc).__name__}: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
