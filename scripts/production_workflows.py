#!/usr/bin/env python3
"""Build and guard ADA's two isolated production ComfyUI workflows."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from ada_paths import WORKFLOWS_ROOT
from ada_paths import ADA_ROOT


ILLUSTRIOUS_ONLY_WORKFLOW = WORKFLOWS_ROOT / "legacy" / "specialist" / "illustrious_only_api.json"
KLEIN_ONLY_WORKFLOW = WORKFLOWS_ROOT / "legacy" / "specialist" / "klein_only_api.json"
LUSTIFY_PRIMARY_WORKFLOW = WORKFLOWS_ROOT / "production" / "lustify_krea2_primary_v1_api.json"
LUSTIFY_IMG2IMG_WORKFLOW = WORKFLOWS_ROOT / "production" / "lustify_krea2_img2img_v1_api.json"
MIAOMIAO_SECONDARY_WORKFLOW = WORKFLOWS_ROOT / "production" / "miaomiao_anima16_secondary_v1_api.json"
PRODUCTION_RENDER_CONFIG = ADA_ROOT / "config" / "pipeline.json"

def _term(*fragments: str) -> str:
    """Keep incident literals out of active prompt/template source text."""
    return "".join(fragments)


ILLUSTRIOUS_FORBIDDEN = (
    "flux-2-klein", "qwen_3_8b", "referencelatent", "loadimage",
    _term("ch", "el"), _term("the road to ", "el dorado"), _term("water", "fall"), "imageconcat",
)
KLEIN_FORBIDDEN = (
    "waiillustrious", "emptylatentimage", _term("ch", "el"),
    _term("the road to ", "el dorado"), _term("water", "fall"), "imageconcat",
)
DANGEROUS_DEFAULTS = (
    _term("ch", "el"),
    _term("the road to ", "el dorado"),
    _term("golden ", "idol"),
    _term("treasure ", "chamber"),
    _term("gold ", "coins"),
    _term("temple ", "water", "fall"),
    _term("wet ", "skin"),
    _term("wet ", "clothes"),
    _term("playful seductive ", "smile"),
)


def load_workflow(path: Path) -> dict[str, dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not value:
        raise ValueError(f"Production workflow must be a non-empty API graph: {path}")
    return value


def production_render_config() -> dict[str, Any]:
    """The production config is the sole mutable source for render settings."""
    value = json.loads(PRODUCTION_RENDER_CONFIG.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("illustrious"), dict) or not isinstance(value.get("klein"), dict):
        raise ValueError("Invalid production render configuration")
    return value


def production_renderer_preset(preset_id: str) -> dict[str, Any]:
    """Return one frozen current renderer preset from pipeline.json."""
    presets = production_render_config().get("renderers", {}).get("presets", {})
    preset = presets.get(preset_id) if isinstance(presets, dict) else None
    if not isinstance(preset, dict):
        raise ValueError(f"Unknown production renderer preset: {preset_id}")
    return preset


def configured_renderers(include_secondary: bool = False, *, renderer_choice: str | None = None) -> list[tuple[str, dict[str, Any]]]:
    renderers = production_render_config().get("renderers", {})
    primary = renderers.get("primary")
    if not isinstance(primary, str):
        raise ValueError("Production primary renderer is not configured")
    if renderer_choice is not None:
        if renderer_choice == "lustify":
            return [(primary, production_renderer_preset(primary))]
        if renderer_choice == "miaomiao":
            secondary = renderers.get("secondary", {})
            preset_id = secondary.get("id") if isinstance(secondary, dict) else None
            if not isinstance(preset_id, str):
                raise ValueError("Production Miaomiao renderer is not configured")
            return [(preset_id, production_renderer_preset(preset_id))]
        raise ValueError(f"Unsupported renderer choice: {renderer_choice}")
    result = [(primary, production_renderer_preset(primary))]
    secondary = renderers.get("secondary", {})
    if include_secondary and isinstance(secondary, dict) and isinstance(secondary.get("id"), str):
        result.append((secondary["id"], production_renderer_preset(secondary["id"])))
    return result


def renderer_workflow_path(preset_id: str) -> Path:
    relative = production_renderer_preset(preset_id).get("workflow")
    if not isinstance(relative, str) or not relative:
        raise ValueError(f"Renderer preset {preset_id} has no workflow")
    path = (ADA_ROOT / relative).resolve()
    production_root = (WORKFLOWS_ROOT / "production").resolve()
    if not path.is_relative_to(production_root):
        raise ValueError(f"Production renderer workflow must stay under {production_root}: {path}")
    return path


def build_renderer_workflow(*, preset_id: str, positive_prompt: str, seed: int, output_prefix: str) -> dict[str, dict[str, Any]]:
    """Bind only runtime values into an immutable production renderer template."""
    preset = production_renderer_preset(preset_id)
    renderer = preset.get("renderer")
    workflow = copy.deepcopy(load_workflow(renderer_workflow_path(preset_id)))
    if renderer == "lustify":
        workflow["1"]["inputs"]["unet_name"] = preset["checkpoint"]
        workflow["3"]["inputs"].update({"clip_name": preset["text_encoder"], "type": preset["text_encoder_type"]})
        workflow["16"]["inputs"]["vae_name"] = preset["vae"]
        workflow["21"]["inputs"]["shift"] = float(preset["model_sampling"]["shift"])
        workflow["11"]["inputs"].update({"width": int(preset["width"]), "height": int(preset["height"]), "batch_size": int(preset["batch_size"])})
        workflow["6"]["inputs"].update({"seed": int(seed), "steps": int(preset["steps"]), "cfg": float(preset["cfg"]), "sampler_name": preset["sampler"], "scheduler": preset["scheduler"], "denoise": float(preset["denoise"])})
        workflow["8"]["inputs"]["text"] = positive_prompt
        workflow["14"]["inputs"]["filename_prefix"] = output_prefix
    elif renderer == "miaomiao":
        workflow["1"]["inputs"]["ckpt_name"] = preset["checkpoint"]
        workflow["9"]["inputs"].update({"clip_name": preset["text_encoder"], "type": preset["text_encoder_type"]})
        workflow["10"]["inputs"]["vae_name"] = preset["vae"]
        workflow["6"]["inputs"].update({"width": int(preset["width"]), "height": int(preset["height"]), "batch_size": int(preset["batch_size"])})
        workflow["5"]["inputs"].update({"seed": int(seed), "steps": int(preset["steps"]), "cfg": float(preset["cfg"]), "sampler_name": preset["sampler"], "scheduler": preset["scheduler"], "denoise": float(preset["denoise"])})
        workflow["3"]["inputs"]["text"] = positive_prompt
        workflow["4"]["inputs"]["text"] = preset["negative_prompt"]
        workflow["8"]["inputs"]["filename_prefix"] = output_prefix
    else:
        raise ValueError(f"Unsupported production renderer: {renderer}")
    return workflow


def build_lustify_img2img_workflow(*, source_image: str, positive_prompt: str, seed: int, output_prefix: str) -> dict[str, dict[str, Any]]:
    """Bind a trusted Miaomiao image into Lustify's verified latent Img2Img recipe."""
    preset_id = "lustify_krea2_img2img_v1"
    preset = production_renderer_preset(preset_id)
    workflow = copy.deepcopy(load_workflow(renderer_workflow_path(preset_id)))
    workflow["1"]["inputs"]["unet_name"] = preset["checkpoint"]
    workflow["3"]["inputs"].update({"clip_name": preset["text_encoder"], "type": preset["text_encoder_type"]})
    workflow["4"]["inputs"]["image"] = source_image
    workflow["5"]["inputs"].update({"width": int(preset["width"]), "height": int(preset["height"])})
    workflow["16"]["inputs"]["vae_name"] = preset["vae"]
    workflow["21"]["inputs"]["shift"] = float(preset["model_sampling"]["shift"])
    workflow["6"]["inputs"].update({
        "seed": int(seed), "steps": int(preset["steps"]), "cfg": float(preset["cfg"]),
        "sampler_name": preset["sampler"], "scheduler": preset["scheduler"], "denoise": float(preset["denoise"]),
    })
    workflow["8"]["inputs"]["text"] = positive_prompt
    workflow["14"]["inputs"]["filename_prefix"] = output_prefix
    return workflow


def _serialized(workflow: dict[str, dict[str, Any]]) -> str:
    return json.dumps(workflow, ensure_ascii=False).lower()


def _save_nodes(workflow: dict[str, dict[str, Any]]) -> list[str]:
    return [node_id for node_id, node in workflow.items() if node.get("class_type") == "SaveImage"]


def _reject_terms(workflow: dict[str, dict[str, Any]], terms: tuple[str, ...], stage: str) -> None:
    serialized = _serialized(workflow)
    found = [term for term in terms if term in serialized]
    if found:
        raise ValueError(f"{stage} workflow contains forbidden production content: {', '.join(found)}")


def validate_illustrious_workflow(
    workflow: dict[str, dict[str, Any]], *, inspect_prompt_text: bool = True,
) -> None:
    if inspect_prompt_text:
        _reject_terms(workflow, ILLUSTRIOUS_FORBIDDEN, "Illustrious")
    saves = _save_nodes(workflow)
    if saves != ["7"]:
        raise ValueError(f"Illustrious workflow must have exactly SaveImage node 7; found {saves}")
    classes = {node.get("class_type") for node in workflow.values()}
    required = {"CheckpointLoaderSimple", "CLIPTextEncode", "EmptyLatentImage", "KSampler", "VAEDecode", "SaveImage"}
    if not required.issubset(classes):
        raise ValueError(f"Illustrious workflow is missing required classes: {sorted(required - classes)}")
    settings = production_render_config()["illustrious"]
    sampler = workflow["5"]["inputs"]
    if workflow["1"]["inputs"].get("ckpt_name") != settings["checkpoint"]:
        raise ValueError("Illustrious workflow checkpoint differs from production configuration")
    for key in ("width", "height", "batch_size"):
        if workflow["4"]["inputs"].get(key) != settings[key]:
            raise ValueError(f"Illustrious workflow {key} differs from production configuration")
    for key, expected in (("steps", settings["steps"]), ("cfg", settings["cfg"]), ("sampler_name", settings["sampler"]), ("scheduler", settings["scheduler"])):
        if sampler.get(key) != expected:
            raise ValueError(f"Illustrious workflow {key} differs from production configuration")


def validate_klein_workflow(
    workflow: dict[str, dict[str, Any]], *, expected_input_image: str | None = None,
    inspect_prompt_text: bool = True,
) -> None:
    if inspect_prompt_text:
        _reject_terms(workflow, KLEIN_FORBIDDEN, "Klein")
    saves = _save_nodes(workflow)
    if saves != ["20"]:
        raise ValueError(f"Klein workflow must have exactly SaveImage node 20; found {saves}")
    load_nodes = [node for node in workflow.values() if node.get("class_type") == "LoadImage"]
    if len(load_nodes) != 1:
        raise ValueError(f"Klein workflow must have exactly one LoadImage; found {len(load_nodes)}")
    actual_input = load_nodes[0].get("inputs", {}).get("image")
    if expected_input_image is not None and actual_input != expected_input_image:
        raise ValueError(f"Klein LoadImage mismatch: expected {expected_input_image!r}, got {actual_input!r}")
    if workflow.get("40", {}).get("inputs", {}).get("pixels") != ["900", 0]:
        raise ValueError("Klein VAEEncode must consume the single approved LoadImage node")
    if workflow.get("51", {}).get("class_type") != "ReferenceLatent":
        raise ValueError("Klein production workflow is missing ReferenceLatent")
    settings = production_render_config()["klein"]
    if workflow.get("45", {}).get("inputs", {}).get("unet_name") != settings["model"]:
        raise ValueError("Klein workflow model differs from production configuration")
    if workflow.get("46", {}).get("inputs", {}).get("clip_name") != settings["text_encoder"]:
        raise ValueError("Klein workflow text encoder differs from production configuration")
    configured = settings.get("loras", [])
    lora_inputs = workflow.get("42", {}).get("inputs", {})
    if not isinstance(configured, list) or not configured:
        raise ValueError("Klein production LoRA configuration is invalid")
    for index, expected in enumerate(configured, start=1):
        lora = lora_inputs.get(f"lora_{index}")
        if not isinstance(lora, dict) or not lora.get("on"):
            raise ValueError(f"Klein production LoRA {index} is missing or disabled")
        if lora.get("lora", "").replace("\\", "/") != expected.get("lora") or lora.get("strength") != expected.get("strength"):
            raise ValueError(f"Klein workflow LoRA {index} differs from the production configuration")
    unexpected = [
        key for key, value in lora_inputs.items()
        if key.startswith("lora_") and key[len("lora_"):].isdigit()
        and int(key[len("lora_"):]) > len(configured)
        and isinstance(value, dict) and value.get("on")
    ]
    if unexpected:
        raise ValueError(f"Klein workflow has unexpected enabled LoRAs: {unexpected}")
    for node, key, expected in (("43", "steps", settings["steps"]), ("43", "width", settings["width"]), ("43", "height", settings["height"]), ("41", "sampler_name", settings["sampler"]), ("47", "guidance", settings["guidance"]), ("53", "cfg", settings["cfg"])):
        if workflow[node]["inputs"].get(key) != expected:
            raise ValueError(f"Klein workflow {key} differs from production configuration")


def build_illustrious_workflow(
    *,
    positive_prompt: str,
    seed: int,
    width: int,
    height: int,
    output_prefix: str,
    negative_prompt: str | None = None,
) -> dict[str, dict[str, Any]]:
    workflow = copy.deepcopy(load_workflow(ILLUSTRIOUS_ONLY_WORKFLOW))
    settings = production_render_config()["illustrious"]
    workflow["1"]["inputs"]["ckpt_name"] = settings["checkpoint"]
    workflow["4"]["inputs"].update({"width": int(settings["width"]), "height": int(settings["height"]), "batch_size": int(settings["batch_size"])})
    workflow["5"]["inputs"].update({"steps": int(settings["steps"]), "cfg": float(settings["cfg"]), "sampler_name": settings["sampler"], "scheduler": settings["scheduler"]})
    validate_illustrious_workflow(workflow)
    workflow["2"]["inputs"]["text"] = positive_prompt
    if negative_prompt is not None:
        workflow["3"]["inputs"]["text"] = negative_prompt
    if (int(width), int(height)) != (int(settings["width"]), int(settings["height"])):
        raise ValueError("Illustrious dimensions must come from production render configuration")
    workflow["5"]["inputs"]["seed"] = int(seed)
    workflow["7"]["inputs"]["filename_prefix"] = output_prefix
    validate_illustrious_workflow(workflow, inspect_prompt_text=False)
    return workflow


def build_klein_workflow(
    *, input_image: str, positive_prompt: str, seed: int, output_prefix: str,
) -> dict[str, dict[str, Any]]:
    workflow = copy.deepcopy(load_workflow(KLEIN_ONLY_WORKFLOW))
    settings = production_render_config()["klein"]
    workflow["45"]["inputs"]["unet_name"] = settings["model"]
    workflow["46"]["inputs"]["clip_name"] = settings["text_encoder"]
    workflow["37"]["inputs"]["vae_name"] = settings["vae"]
    lora_inputs = workflow["42"]["inputs"]
    for key in [key for key in lora_inputs if key.startswith("lora_") and key[len("lora_"):].isdigit()]:
        del lora_inputs[key]
    for index, lora in enumerate(settings["loras"], start=1):
        lora_inputs[f"lora_{index}"] = {"on": True, **lora}
    workflow["43"]["inputs"].update({"steps": int(settings["steps"]), "width": int(settings["width"]), "height": int(settings["height"])})
    workflow["41"]["inputs"]["sampler_name"] = settings["sampler"]
    workflow["47"]["inputs"]["guidance"] = float(settings["guidance"])
    workflow["53"]["inputs"]["cfg"] = float(settings["cfg"])
    validate_klein_workflow(workflow, expected_input_image="__ADA_APPROVED_ILLUSTRIOUS__")
    workflow["900"]["inputs"]["image"] = input_image
    workflow["39"]["inputs"]["text"] = positive_prompt
    workflow["38"]["inputs"]["noise_seed"] = int(seed)
    workflow["20"]["inputs"]["filename_prefix"] = output_prefix
    validate_klein_workflow(workflow, expected_input_image=input_image, inspect_prompt_text=False)
    return workflow


def workflow_generation_details(stage: str, workflow: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Extract the effective submitted settings, never a parallel declaration."""
    if stage == "illustrious":
        return {
            "workflow": str(ILLUSTRIOUS_ONLY_WORKFLOW.resolve()), "checkpoint": workflow["1"]["inputs"]["ckpt_name"],
            "positive_prompt": workflow["2"]["inputs"]["text"], "negative_prompt": workflow["3"]["inputs"]["text"],
            "seed": workflow["5"]["inputs"]["seed"], "width": workflow["4"]["inputs"]["width"], "height": workflow["4"]["inputs"]["height"],
            "steps": workflow["5"]["inputs"]["steps"], "cfg": workflow["5"]["inputs"]["cfg"],
            "sampler": workflow["5"]["inputs"]["sampler_name"], "scheduler": workflow["5"]["inputs"]["scheduler"],
        }
    if stage == "klein":
        loras = [
            workflow["42"]["inputs"][f"lora_{index}"]
            for index in range(1, len(production_render_config()["klein"]["loras"]) + 1)
        ]
        return {
            "workflow": str(KLEIN_ONLY_WORKFLOW.resolve()), "checkpoint": workflow["45"]["inputs"]["unet_name"],
            "text_encoder": workflow["46"]["inputs"]["clip_name"], "vae": workflow["37"]["inputs"]["vae_name"],
            "positive_prompt": workflow["39"]["inputs"]["text"], "negative_prompt": None, "reference_source_image": workflow["900"]["inputs"]["image"],
            "seed": workflow["38"]["inputs"]["noise_seed"], "width": workflow["43"]["inputs"]["width"], "height": workflow["43"]["inputs"]["height"],
            "steps": workflow["43"]["inputs"]["steps"], "guidance": workflow["47"]["inputs"]["guidance"], "cfg": workflow["53"]["inputs"]["cfg"],
            "sampler": workflow["41"]["inputs"]["sampler_name"], "scheduler": "flux2",
            "loras": [{"lora": lora["lora"], "strength": lora["strength"]} for lora in loras],
        }
    raise ValueError(f"Unknown production stage: {stage}")


def renderer_generation_details(preset_id: str, workflow: dict[str, dict[str, Any]]) -> dict[str, Any]:
    preset = production_renderer_preset(preset_id)
    renderer = preset["renderer"]
    common = {"preset": preset_id, "renderer": renderer, "workflow": str(renderer_workflow_path(preset_id).resolve()), "checkpoint": preset["checkpoint"], "text_encoder": preset["text_encoder"], "vae": preset["vae"], "width": preset["width"], "height": preset["height"], "steps": preset["steps"], "cfg": preset["cfg"], "sampler": preset["sampler"], "scheduler": preset["scheduler"], "prompt_strategy": preset["prompt_strategy"]}
    if renderer == "lustify":
        details = {**common, "positive_prompt": workflow["8"]["inputs"]["text"], "negative_prompt": None, "seed": workflow["6"]["inputs"]["seed"], "shift": workflow["21"]["inputs"]["shift"], "denoise": workflow["6"]["inputs"]["denoise"]}
        if preset_id == "lustify_krea2_img2img_v1":
            details.update({"mode": "LATENT_IMG2IMG", "reference_source_image": workflow["4"]["inputs"]["image"]})
        else:
            details["mode"] = "DIRECT_T2I"
        return details
    return {**common, "positive_prompt": workflow["3"]["inputs"]["text"], "negative_prompt": workflow["4"]["inputs"]["text"], "seed": workflow["5"]["inputs"]["seed"]}


def submission_provenance(
    *,
    mission_id: str,
    run_id: str,
    concept_id: str,
    candidate_id: str,
    attempt_id: str,
    stage: str,
    workflow_path: Path,
    input_asset: str,
    prompt_id: str | None = None,
    output_asset: str | None = None,
    comfyui_input_name: str | None = None,
) -> dict[str, Any]:
    if stage not in {"illustrious", "klein"}:
        raise ValueError(f"Unknown production stage: {stage}")
    identity = {
        "mission_id": mission_id,
        "run_id": run_id,
        "concept_id": concept_id,
        "candidate_id": candidate_id,
        "attempt_id": attempt_id,
    }
    if not all(isinstance(value, str) and value for value in identity.values()):
        raise ValueError("Submission provenance identity fields must be non-empty strings")
    return {
        **identity,
        "stage": stage,
        "workflow": str(workflow_path.resolve()),
        "prompt_id": prompt_id,
        "input_asset": input_asset,
        "comfyui_input_name": comfyui_input_name,
        "output_asset": output_asset,
    }
