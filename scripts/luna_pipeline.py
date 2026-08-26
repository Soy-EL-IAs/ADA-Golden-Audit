#!/usr/bin/env python3
"""Run the Illustrious -> Krea2 pipeline through the local ComfyUI API."""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import shutil
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any

if __package__:
    from .ada_paths import ADA_ROOT, COMFYUI_BASE_URL, COMFYUI_ROOT, CONFIG_ROOT, PREMISES_ROOT, RENDER_ONLY_RUNS_ROOT, RUNS_ROOT, WORKFLOWS_ROOT, resolve_legacy_path
else:
    from ada_paths import ADA_ROOT, COMFYUI_BASE_URL, COMFYUI_ROOT, CONFIG_ROOT, PREMISES_ROOT, RENDER_ONLY_RUNS_ROOT, RUNS_ROOT, WORKFLOWS_ROOT, resolve_legacy_path


PACKAGE_ROOT = ADA_ROOT  # compatibility for existing helper scripts
DEFAULT_PREMISES = PREMISES_ROOT / "pilot_10.jsonl"
DEFAULT_CONFIG = CONFIG_ROOT / "pipeline.json"
RUBRIC_PATH = CONFIG_ROOT / "scoring_rubric.json"
ILLUSTRIOUS_WORKFLOW = WORKFLOWS_ROOT / "legacy" / "specialist" / "illustrious_4x_api.json"
KREA_WORKFLOW = WORKFLOWS_ROOT / "legacy" / "specialist" / "krea_convert_1x_api.json"
RENDER_ONLY_ROOT = RENDER_ONLY_RUNS_ROOT

FRAMING_PROFILES: dict[str, dict[str, str]] = {
    "medium_close_up": {
        "positive": "medium close-up, waist-up framing, active interaction with the premise action and its required key prop clearly visible, cinematic depth",
        "negative": "full body, head-to-toe, centered standing pose, posing beside the bar",
    },
    "head_to_waist": {
        "positive": "(head and face fully visible:1.5), (framed from top of head to waist:1.5), face in the upper third, waist at the bottom edge",
        "negative": "cropped head, face out of frame, chest-only crop, torso-only composition, hips-centered framing, thighs visible, knees visible, legs visible, full body, head-to-toe, seated pose, hands outside frame",
    },
}


BASE_NEGATIVE = [
    "worst quality",
    "low quality",
    "lowres",
    "blurry",
    "jpeg artifacts",
    "bad anatomy",
    "bad hands",
    "extra fingers",
    "missing fingers",
    "extra limbs",
    "duplicate",
    "multiple girls",
    "two people",
    "collage",
    "split screen",
    "comic panels",
    "text",
    "watermark",
    "logo",
    "camera",
    "handheld camera",
    "photography equipment",
    "filming equipment",
    "visible lens",
    "cropped head",
    "young-looking",
    "gigantic hips",
    "extreme low angle",
    "fisheye",
    "explicit nudity",
]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_premises(path: Path) -> list[dict[str, Any]]:
    premises: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            premises.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc
    return premises


def find_premise(path: Path, premise_id: str) -> dict[str, Any]:
    matches = [item for item in read_premises(path) if item.get("id") == premise_id]
    if not matches:
        raise ValueError(f"Premise {premise_id!r} was not found in {path}")
    if len(matches) > 1:
        raise ValueError(f"Premise id {premise_id!r} is duplicated in {path}")
    return matches[0]


def http_json(url: str, method: str = "GET", payload: Any | None = None) -> Any:
    data = None
    headers: dict[str, str] = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def upload_input_image(
    server_url: str,
    source_path: Path,
    desired_name: str,
    subfolder: str,
) -> str:
    """Upload an input image through ComfyUI instead of writing to its input folder.

    The API process owns ComfyUI/input. This keeps the runner usable when its own
    filesystem permissions do not include that installation directory.
    """
    boundary = f"----LunaPipeline{uuid.uuid4().hex}"
    crlf = b"\r\n"

    def field(name: str, value: str) -> bytes:
        return (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
            f"{value}\r\n"
        ).encode("utf-8")

    image_header = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="image"; filename="{desired_name}"\r\n'
        "Content-Type: image/png\r\n\r\n"
    ).encode("utf-8")
    body = b"".join(
        [
            field("overwrite", "false"),
            field("subfolder", subfolder),
            image_header,
            source_path.read_bytes(),
            crlf,
            f"--{boundary}--\r\n".encode("utf-8"),
        ]
    )
    request = urllib.request.Request(
        f"{server_url}/upload/image",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        uploaded = json.loads(response.read().decode("utf-8"))

    name = uploaded.get("name")
    uploaded_subfolder = str(uploaded.get("subfolder") or "")
    if not name:
        raise RuntimeError(f"ComfyUI did not confirm the input upload: {uploaded}")
    return f"{uploaded_subfolder}/{name}" if uploaded_subfolder else str(name)


def ensure_server(server_url: str) -> None:
    try:
        http_json(f"{server_url}/system_stats")
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(
            f"ComfyUI is not reachable at {server_url}. Start it before running Luna."
        ) from exc


def submit_prompt(server_url: str, prompt: dict[str, Any], client_id: str) -> str:
    response = http_json(
        f"{server_url}/prompt",
        method="POST",
        payload={"prompt": prompt, "client_id": client_id},
    )
    node_errors = response.get("node_errors") or {}
    if node_errors:
        raise RuntimeError(f"ComfyUI rejected workflow nodes: {json.dumps(node_errors, indent=2)}")
    prompt_id = response.get("prompt_id")
    if not prompt_id:
        raise RuntimeError(f"ComfyUI did not return a prompt id: {response}")
    return str(prompt_id)


def wait_for_history(
    server_url: str,
    prompt_id: str,
    timeout_seconds: int,
    poll_seconds: float,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        history = http_json(f"{server_url}/history/{prompt_id}")
        item = history.get(prompt_id)
        if item:
            status = item.get("status", {})
            if status.get("status_str") == "error":
                raise RuntimeError(f"ComfyUI execution failed: {json.dumps(status, indent=2)}")
            if item.get("outputs"):
                return item
        time.sleep(poll_seconds)
    raise TimeoutError(f"Prompt {prompt_id} did not finish within {timeout_seconds} seconds")


def output_images(history_item: dict[str, Any], node_id: str) -> list[dict[str, Any]]:
    images = history_item.get("outputs", {}).get(node_id, {}).get("images", [])
    if not images:
        raise RuntimeError(f"SaveImage node {node_id} returned no images")
    return sorted(images, key=lambda item: (item.get("subfolder", ""), item.get("filename", "")))


def image_absolute_path(comfy_root: Path, descriptor: dict[str, Any]) -> Path:
    image_type = descriptor.get("type", "output")
    root_name = {"output": "output", "input": "input", "temp": "temp"}.get(image_type)
    if root_name is None:
        raise ValueError(f"Unsupported ComfyUI image type: {image_type}")
    path = comfy_root / root_name / descriptor.get("subfolder", "") / descriptor["filename"]
    return path.resolve()


def join_tags(values: list[str]) -> str:
    return ", ".join(value.strip() for value in values if value.strip())


def weighted_tags(values: list[str], weight: float) -> str:
    return ", ".join(f"({value.strip()}:{weight:g})" for value in values if value.strip())


def framing_profile(name: str | None) -> dict[str, str] | None:
    if name is None:
        return None
    try:
        return FRAMING_PROFILES[name]
    except KeyError as exc:
        raise ValueError(f"Unknown framing profile: {name}") from exc


def illustrious_positive(
    premise: dict[str, Any], style_note: str | None = None, framing: str | None = None,
) -> str:
    profile = framing_profile(framing)
    composition = profile["positive"] if profile else (
        "cinematic scene, funny visual storytelling, three-quarter view, full body, strong depth, dynamic composition"
    )
    parts = [
        "masterpiece, best quality, newest, very aesthetic",
        f"1girl, solo, {premise['character']}, {premise['franchise']}, mature woman",
        join_tags(premise["identity"]),
        premise["premise"],
        join_tags(premise["must_include"]),
        join_tags(premise["environment"]),
        composition,
        style_note or "",
        "(adult voluptuous athletic figure:0.95), (fuller bust:0.9), (defined waist:0.9), (wider hips:0.9), (thick toned thighs:0.9), anatomically coherent proportions, visible neckline and cleavage only where the garment design permits, confident sensual pose",
        weighted_tags(premise["sexual_direction"], 0.9),
    ]
    return ",\n".join(part for part in parts if part)


def illustrious_negative(premise: dict[str, Any], framing: str | None = None) -> str:
    profile = framing_profile(framing)
    composition_negative = [profile["negative"]] if profile else []
    return join_tags(BASE_NEGATIVE + list(premise.get("avoid", [])) + composition_negative)


def krea_prompt(premise: dict[str, Any]) -> str:
    identity = join_tags(premise["identity"])
    essentials = join_tags(premise["must_include"])
    environment = join_tags(premise["environment"])
    return (
        "transform the image to realistic photograph, "
        f"{premise['krea_direction']}, preserve {premise['character']} identity, "
        f"{identity}, preserve the source body proportions, sensual pose and expression, "
        f"preserve {essentials}, {environment} and the original composition, "
        "realistic skin and fabric materials, detailed hair, cinematic lighting, polished modern game-render quality"
    )


def render_only_krea_prompt(premise: dict[str, Any], preservation_note: str | None = None) -> str:
    """Fixed strict preservation prompt for render-only mode; never expands the premise."""
    if preservation_note:
        return preservation_note
    return (
        "Preserve the source image exactly as an image-to-image conversion. "
        "Preserve identity, facial expression, silhouette, proportions, clothing, hand position, action, viewpoint, crop and framing. "
        "Do not reconstruct, reframe, zoom out, zoom in, relocate objects or invent missing composition."
    )


def queue_is_idle(server_url: str) -> bool:
    queue = http_json(f"{server_url}/queue")
    return not queue.get("queue_running") and not queue.get("queue_pending")


def require_idle_queue(server_url: str) -> None:
    if not queue_is_idle(server_url):
        raise RuntimeError("ComfyUI still has an active or pending generation")


def copy_output(comfy_root: Path, descriptor: dict[str, Any], destination: Path) -> Path:
    source = image_absolute_path(comfy_root, descriptor)
    if not source.exists():
        raise FileNotFoundError(f"ComfyUI output is missing: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return destination.resolve()


def render_only_one(
    premise: dict[str, Any], config: dict[str, Any], run_dir: Path,
    sequence: int, batch_id: str, illustrious_style_note: str | None,
    framing: str | None, illustrious_width: int | None, illustrious_height: int | None,
    illustrious_seed: int | None, illustrious_prefix: str | None,
    illustrious_negative_addition: str | None, stop_after_illustrious: bool,
    crop_waist_up: bool, krea_preservation_note: str | None,
) -> dict[str, Any]:
    """Generate one Illustrious image and one Krea conversion, with no review artifacts."""
    server_url = config["server_url"].rstrip("/")
    comfy_root = Path(config["comfy_root"])
    run_id = run_dir.name
    manifest_path = run_dir / "manifest.json"
    run_dir.mkdir(parents=True, exist_ok=True)
    write_json(run_dir / "premise.json", premise)
    manifest = read_json(manifest_path) if manifest_path.exists() else {
        "run_id": run_id, "batch_id": batch_id, "sequence": sequence,
        "premise_id": premise["id"], "mode": "render-only-fast",
        "review_status": "unreviewed_render_only", "status": "generating_illustrious",
        "created_at": dt.datetime.now().astimezone().isoformat(),
        "illustrious_candidates": [], "krea_candidates": [],
    }
    if illustrious_style_note:
        manifest["illustrious_style_note"] = illustrious_style_note
    if framing:
        manifest["framing_profile"] = framing
    if illustrious_seed is not None:
        manifest["illustrious_seed_override"] = illustrious_seed
    write_json(manifest_path, manifest)
    if manifest.get("status") == "unreviewed_render_only":
        return manifest

    if not manifest.get("illustrious_candidates"):
        require_idle_queue(server_url)
        settings = config["illustrious"]
        prompt = copy.deepcopy(read_json(ILLUSTRIOUS_WORKFLOW))
        prompt["1"]["inputs"]["ckpt_name"] = settings["checkpoint"]
        positive = illustrious_positive(premise, illustrious_style_note, framing)
        prompt["2"]["inputs"]["text"] = f"{illustrious_prefix}, {positive}" if illustrious_prefix else positive
        negative = illustrious_negative(premise, framing)
        prompt["3"]["inputs"]["text"] = join_tags([negative, illustrious_negative_addition or ""])
        prompt["4"]["inputs"].update(width=settings["width"], height=settings["height"], batch_size=1)
        if illustrious_width is not None:
            prompt["4"]["inputs"]["width"] = illustrious_width
        if illustrious_height is not None:
            prompt["4"]["inputs"]["height"] = illustrious_height
        prompt["5"]["inputs"].update(
            seed=illustrious_seed if illustrious_seed is not None else premise["seed_base"], steps=settings["steps"], cfg=settings["cfg"],
            sampler_name=settings["sampler"], scheduler=settings["scheduler"],
        )
        prompt["7"]["inputs"]["filename_prefix"] = f"LunaRenderOnly/{batch_id}/{run_id}/illustrious/candidate_01"
        write_json(run_dir / "illustrious_workflow_submitted.json", prompt)
        prompt_id = submit_prompt(server_url, prompt, f"luna-fast-{run_id}-illustrious")
        history = wait_for_history(server_url, prompt_id, config["timeouts"]["illustrious_seconds"], config["timeouts"]["poll_seconds"])
        images = output_images(history, "7")
        if len(images) != 1:
            raise RuntimeError(f"Expected one Illustrious image, received {len(images)}")
        local_path = copy_output(comfy_root, images[0], run_dir / "illustrious" / "candidate_01.png")
        manifest["illustrious_prompt_id"] = prompt_id
        manifest["illustrious_candidates"] = [{
            "candidate_id": "candidate_01", "seed": illustrious_seed if illustrious_seed is not None else premise["seed_base"],
            "image_path": str(local_path), "comfy_descriptor": images[0],
        }]
        manifest["status"] = "awaiting_render_only_krea" if stop_after_illustrious else "generating_krea"
        write_json(manifest_path, manifest)

    if stop_after_illustrious:
        return manifest

    if not manifest.get("krea_candidates"):
        require_idle_queue(server_url)
        source_path = resolve_legacy_path(manifest["illustrious_candidates"][0]["image_path"])
        if crop_waist_up and not manifest.get("krea_source_image_path"):
            try:
                from PIL import Image
            except ImportError as exc:
                raise RuntimeError("Generic waist-up crop requires Pillow") from exc
            crop_path = run_dir / "illustrious" / "candidate_01_waist_up_crop.png"
            with Image.open(source_path) as image:
                width, height = image.size
                image.crop((0, 0, width, round(height * 0.65))).save(crop_path)
            manifest["krea_source_image_path"] = str(crop_path.resolve())
            manifest["krea_source_fallback"] = "generic_waist_up_crop"
            write_json(manifest_path, manifest)
        if manifest.get("krea_source_image_path"):
            source_path = resolve_legacy_path(manifest["krea_source_image_path"])
        uploaded = upload_input_image(server_url, source_path, f"{run_id}_candidate_01.png", f"LunaRenderOnly/inputs/{batch_id}/{run_id}")
        settings = config["krea"]
        prompt = copy.deepcopy(read_json(KREA_WORKFLOW))
        prompt["1"]["inputs"]["unet_name"] = settings["model"]
        prompt["2"]["inputs"]["clip_name"] = settings["text_encoder"]
        prompt["3"]["inputs"]["vae_name"] = settings["vae"]
        prompt["4"]["inputs"]["image"] = uploaded
        prompt["5"]["inputs"].update(width=settings["width"], height=settings["height"])
        prompt["6"]["inputs"].update(vl_size=settings["vl_size"], prompt=render_only_krea_prompt(premise, krea_preservation_note))
        prompt["9"]["inputs"]["kv_cache"] = settings["kv_cache"]
        prompt["10"]["inputs"].update(
            seed=premise["krea_seed_base"], steps=settings["steps"], cfg=settings["cfg"],
            sampler_name=settings["sampler"], scheduler=settings["scheduler"],
        )
        prompt["12"]["inputs"]["filename_prefix"] = f"LunaRenderOnly/{batch_id}/{run_id}/krea/candidate_01"
        write_json(run_dir / "krea_workflow_submitted.json", prompt)
        prompt_id = submit_prompt(server_url, prompt, f"luna-fast-{run_id}-krea")
        history = wait_for_history(server_url, prompt_id, config["timeouts"]["krea_seconds"], config["timeouts"]["poll_seconds"])
        images = output_images(history, "12")
        if len(images) != 1:
            raise RuntimeError(f"Expected one Krea image, received {len(images)}")
        local_path = copy_output(comfy_root, images[0], run_dir / "krea" / "candidate_01.png")
        manifest["krea_prompt_id"] = prompt_id
        manifest["krea_candidates"] = [{
            "candidate_id": "candidate_01", "seed": premise["krea_seed_base"],
            "source_image_path": str(source_path), "image_path": str(local_path),
            "comfy_descriptor": images[0],
        }]

    manifest["status"] = "unreviewed_render_only"
    manifest["review_status"] = "unreviewed_render_only"
    manifest["completed_at"] = dt.datetime.now().astimezone().isoformat()
    write_json(manifest_path, manifest)
    return manifest


def run_render_only_batch(
    premises_path: Path, config: dict[str, Any], expected_count: int,
    progress_every: int, batch_id: str | None, dry_run: bool, take: int | None,
    premise_ids: list[str] | None, illustrious_style_note: str | None, framing: str | None,
    illustrious_width: int | None, illustrious_height: int | None, illustrious_seed: int | None,
    illustrious_prefix: str | None, illustrious_negative_addition: str | None,
    stop_after_illustrious: bool, crop_waist_up: bool, krea_preservation_note: str | None,
) -> Path | None:
    source_premises = read_premises(premises_path)
    if premise_ids:
        requested = set(premise_ids)
        premises = [item for item in source_premises if item.get("id") in requested]
        if len(premises) != len(requested):
            missing = requested - {item.get("id") for item in premises}
            raise ValueError(f"Requested premise ids were not found: {sorted(missing)}")
    else:
        premises = source_premises[:take] if take is not None else source_premises
    if expected_count < 1 or progress_every < 1 or (take is not None and take < 1):
        raise ValueError("expected-count, progress-every, and take must be positive")
    ids = [str(item.get("id")) for item in premises]
    if len(ids) != len(set(ids)):
        raise ValueError("The premise list contains duplicate ids")
    if len(premises) != expected_count:
        raise ValueError(f"Expected {expected_count} premises, found {len(premises)} in {premises_path}")
    command_validate(config)
    server_url = config["server_url"].rstrip("/")
    require_idle_queue(server_url)
    if dry_run:
        print(json.dumps({"status": "ready", "premises": len(premises), "queue": "idle"}))
        return None

    batch_id = batch_id or f"{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}_render_only_fast"
    batch_dir = RENDER_ONLY_ROOT / batch_id
    batch_dir.mkdir(parents=True, exist_ok=True)
    batch_manifest_path = batch_dir / "batch_manifest.json"
    batch_manifest = read_json(batch_manifest_path) if batch_manifest_path.exists() else {
        "batch_id": batch_id, "mode": "render-only-fast",
        "premises_source": str(premises_path.resolve()), "expected_count": expected_count,
        "started_at": dt.datetime.now().astimezone().isoformat(), "runs": [],
    }
    indexed = {item["premise_id"]: item for item in batch_manifest["runs"]}
    for sequence, premise in enumerate(premises, 1):
        run_dir = batch_dir / f"{sequence:03d}_{premise['id']}"
        try:
            result = render_only_one(
                premise, config, run_dir, sequence, batch_id, illustrious_style_note, framing,
                illustrious_width, illustrious_height, illustrious_seed, illustrious_prefix,
                illustrious_negative_addition, stop_after_illustrious, crop_waist_up,
                krea_preservation_note,
            )
            record = {"sequence": sequence, "premise_id": premise["id"], "status": result["status"], "run_dir": str(run_dir.resolve())}
        except Exception as exc:
            error = {"sequence": sequence, "premise_id": premise["id"], "error": str(exc), "recorded_at": dt.datetime.now().astimezone().isoformat()}
            write_json(run_dir / "error.json", error)
            failed_manifest_path = run_dir / "manifest.json"
            failed_manifest = read_json(failed_manifest_path) if failed_manifest_path.exists() else {
                "run_id": run_dir.name, "batch_id": batch_id, "sequence": sequence,
                "premise_id": premise["id"], "mode": "render-only-fast",
                "review_status": "unreviewed_render_only", "illustrious_candidates": [],
                "krea_candidates": [],
            }
            failed_manifest["status"] = "render_only_error"
            failed_manifest["error"] = str(exc)
            write_json(failed_manifest_path, failed_manifest)
            record = {**error, "status": "render_only_error", "run_dir": str(run_dir.resolve())}
            if not queue_is_idle(server_url):
                indexed[premise["id"]] = record
                batch_manifest["runs"] = sorted(indexed.values(), key=lambda item: item["sequence"])
                write_json(batch_manifest_path, batch_manifest)
                raise RuntimeError(f"Premise {premise['id']} failed and ComfyUI is not idle; batch stopped") from exc
        indexed[premise["id"]] = record
        batch_manifest["runs"] = sorted(indexed.values(), key=lambda item: item["sequence"])
        write_json(batch_manifest_path, batch_manifest)
        if sequence % progress_every == 0:
            failures = sum(item["status"] == "render_only_error" for item in indexed.values())
            print(json.dumps({"progress": f"{sequence}/{expected_count}", "failures": failures}), flush=True)
    batch_manifest["status"] = "awaiting_render_only_krea" if stop_after_illustrious else "render_only_complete"
    batch_manifest["completed_at"] = dt.datetime.now().astimezone().isoformat()
    write_json(batch_manifest_path, batch_manifest)
    return batch_dir


def score_template(
    premise_id: str,
    stage: str,
    candidates: list[dict[str, Any]],
    rubric: dict[str, Any],
) -> dict[str, Any]:
    categories = list(rubric[stage].keys())
    return {
        "premise_id": premise_id,
        "stage": stage,
        "candidates": [
            {
                "candidate_id": item["candidate_id"],
                "image_path": item["image_path"],
                "hard_fail": False,
                "hard_fail_reasons": [],
                "scores": {category: None for category in categories},
                "weighted_total": None,
                "summary": None,
            }
            for item in candidates
        ],
        "winner": None,
        "runner_up": None,
        "selection_reason": None,
        "reviewed_at": None,
    }


def score_file_complete(path: Path, rubric: dict[str, Any], stage: str) -> bool:
    if not path.exists():
        return False
    score_data = read_json(path)
    expected = set(rubric[stage].keys())
    for candidate in score_data.get("candidates", []):
        scores = candidate.get("scores", {})
        if set(scores.keys()) != expected:
            return False
        if any(not isinstance(value, (int, float)) for value in scores.values()):
            return False
        if not candidate.get("summary"):
            return False
    return len(score_data.get("candidates", [])) == 4


def make_run_id(premise_id: str) -> str:
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}_{premise_id}"


def run_illustrious(
    premise: dict[str, Any],
    config: dict[str, Any],
    run_id: str | None = None,
) -> Path:
    server_url = config["server_url"].rstrip("/")
    ensure_server(server_url)
    comfy_root = Path(config["comfy_root"])
    run_id = run_id or make_run_id(premise["id"])
    run_dir = RUNS_ROOT / run_id
    if run_dir.exists():
        raise FileExistsError(f"Run directory already exists: {run_dir}")
    run_dir.mkdir(parents=True)

    settings = config["illustrious"]
    prompt = copy.deepcopy(read_json(ILLUSTRIOUS_WORKFLOW))
    prompt["1"]["inputs"]["ckpt_name"] = settings["checkpoint"]
    prompt["2"]["inputs"]["text"] = illustrious_positive(premise)
    prompt["3"]["inputs"]["text"] = illustrious_negative(premise)
    prompt["4"]["inputs"].update(
        width=settings["width"],
        height=settings["height"],
        batch_size=settings["batch_size"],
    )
    prompt["5"]["inputs"].update(
        seed=premise["seed_base"],
        steps=settings["steps"],
        cfg=settings["cfg"],
        sampler_name=settings["sampler"],
        scheduler=settings["scheduler"],
    )
    prompt["7"]["inputs"]["filename_prefix"] = (
        f"LunaPipeline/{run_id}/illustrious/candidate"
    )

    write_json(run_dir / "premise.json", premise)
    write_json(run_dir / "illustrious_workflow_submitted.json", prompt)
    prompt_id = submit_prompt(server_url, prompt, f"luna-{run_id}-illustrious")
    history = wait_for_history(
        server_url,
        prompt_id,
        config["timeouts"]["illustrious_seconds"],
        config["timeouts"]["poll_seconds"],
    )
    images = output_images(history, "7")
    if len(images) != 4:
        raise RuntimeError(f"Expected four Illustrious images, received {len(images)}")
    candidates = [
        {
            "candidate_id": f"candidate_{index:02d}",
            "image_path": str(image_absolute_path(comfy_root, image)),
            "comfy_descriptor": image,
        }
        for index, image in enumerate(images, 1)
    ]
    manifest = {
        "run_id": run_id,
        "premise_id": premise["id"],
        "status": "awaiting_illustrious_scores",
        "created_at": dt.datetime.now().astimezone().isoformat(),
        "illustrious_prompt_id": prompt_id,
        "illustrious_candidates": candidates,
        "krea_candidates": [],
    }
    write_json(run_dir / "manifest.json", manifest)
    rubric = read_json(RUBRIC_PATH)
    write_json(
        run_dir / "scores_illustrious.json",
        score_template(premise["id"], "illustrious", candidates, rubric),
    )
    return run_dir


def run_krea(run_dir: Path, config: dict[str, Any], allow_unscored: bool = False) -> Path:
    run_dir = run_dir.resolve()
    manifest_path = run_dir / "manifest.json"
    manifest = read_json(manifest_path)
    premise = read_json(run_dir / "premise.json")
    rubric = read_json(RUBRIC_PATH)
    scores_path = run_dir / "scores_illustrious.json"
    if not allow_unscored and not score_file_complete(scores_path, rubric, "illustrious"):
        raise RuntimeError(
            "Illustrious scoring is incomplete. Luna must score all four candidates before Krea."
        )

    server_url = config["server_url"].rstrip("/")
    ensure_server(server_url)
    comfy_root = Path(config["comfy_root"])
    settings = config["krea"]
    krea_candidates: list[dict[str, Any]] = []

    for index, source in enumerate(manifest["illustrious_candidates"], 1):
        source_path = resolve_legacy_path(source["image_path"])
        if not source_path.exists():
            raise FileNotFoundError(f"Illustrious source image is missing: {source_path}")
        input_name = f"luna_{manifest['run_id']}_candidate_{index:02d}.png"
        uploaded_image = upload_input_image(
            server_url,
            source_path,
            input_name,
            f"LunaPipeline/inputs/{manifest['run_id']}",
        )

        prompt = copy.deepcopy(read_json(KREA_WORKFLOW))
        prompt["1"]["inputs"]["unet_name"] = settings["model"]
        prompt["2"]["inputs"]["clip_name"] = settings["text_encoder"]
        prompt["3"]["inputs"]["vae_name"] = settings["vae"]
        prompt["4"]["inputs"]["image"] = uploaded_image
        prompt["5"]["inputs"].update(width=settings["width"], height=settings["height"])
        prompt["6"]["inputs"].update(vl_size=settings["vl_size"], prompt=krea_prompt(premise))
        prompt["9"]["inputs"]["kv_cache"] = settings["kv_cache"]
        prompt["10"]["inputs"].update(
            seed=premise["krea_seed_base"] + index - 1,
            steps=settings["steps"],
            cfg=settings["cfg"],
            sampler_name=settings["sampler"],
            scheduler=settings["scheduler"],
        )
        prompt["12"]["inputs"]["filename_prefix"] = (
            f"LunaPipeline/{manifest['run_id']}/krea/candidate_{index:02d}"
        )
        write_json(run_dir / f"krea_workflow_candidate_{index:02d}.json", prompt)
        prompt_id = submit_prompt(
            server_url,
            prompt,
            f"luna-{manifest['run_id']}-krea-{index:02d}",
        )
        history = wait_for_history(
            server_url,
            prompt_id,
            config["timeouts"]["krea_seconds"],
            config["timeouts"]["poll_seconds"],
        )
        images = output_images(history, "12")
        if len(images) != 1:
            raise RuntimeError(f"Expected one Krea image for candidate {index}, got {len(images)}")
        krea_candidates.append(
            {
                "candidate_id": f"candidate_{index:02d}",
                "source_image_path": str(source_path),
                "image_path": str(image_absolute_path(comfy_root, images[0])),
                "comfy_descriptor": images[0],
                "prompt_id": prompt_id,
            }
        )

    manifest["status"] = "awaiting_krea_scores"
    manifest["krea_candidates"] = krea_candidates
    manifest["krea_completed_at"] = dt.datetime.now().astimezone().isoformat()
    write_json(manifest_path, manifest)
    write_json(
        run_dir / "scores_krea.json",
        score_template(premise["id"], "krea", krea_candidates, rubric),
    )
    return run_dir


def calculate_weighted(candidate: dict[str, Any], weights: dict[str, float]) -> float:
    scores = candidate["scores"]
    if set(scores) != set(weights):
        raise ValueError(f"Score categories do not match rubric: {set(scores)} vs {set(weights)}")
    for key, value in scores.items():
        if not isinstance(value, (int, float)) or not 0 <= value <= 10:
            raise ValueError(f"Invalid score {key}={value!r}; expected 0..10")
    return round(sum(float(scores[key]) * weights[key] for key in weights), 3)


def finalize_run(run_dir: Path) -> Path:
    run_dir = run_dir.resolve()
    rubric = read_json(RUBRIC_PATH)
    illustrious_path = run_dir / "scores_illustrious.json"
    krea_path = run_dir / "scores_krea.json"
    if not score_file_complete(illustrious_path, rubric, "illustrious"):
        raise RuntimeError("Illustrious scores are incomplete")
    if not score_file_complete(krea_path, rubric, "krea"):
        raise RuntimeError("Krea scores are incomplete")

    illustrative = read_json(illustrious_path)
    krea = read_json(krea_path)
    illustrative_map = {item["candidate_id"]: item for item in illustrative["candidates"]}
    krea_map = {item["candidate_id"]: item for item in krea["candidates"]}
    combined: list[dict[str, Any]] = []

    for candidate_id in sorted(illustrative_map):
        source = illustrative_map[candidate_id]
        final = krea_map[candidate_id]
        source_total = calculate_weighted(source, rubric["illustrious"])
        final_total = calculate_weighted(final, rubric["krea"])
        source["weighted_total"] = source_total
        final["weighted_total"] = final_total
        hard_fail = bool(source.get("hard_fail") or final.get("hard_fail"))
        combined_total = round(
            source_total * rubric["final_formula"]["illustrious_total"]
            + final_total * rubric["final_formula"]["krea_total"],
            3,
        )
        combined.append(
            {
                "candidate_id": candidate_id,
                "illustrious_total": source_total,
                "krea_total": final_total,
                "combined_total": combined_total,
                "hard_fail": hard_fail,
                "source_image_path": source["image_path"],
                "final_image_path": final["image_path"],
            }
        )

    eligible = [item for item in combined if not item["hard_fail"]]
    if not eligible:
        raise RuntimeError("Every candidate is marked as hard-fail; there is no winner")
    eligible.sort(key=lambda item: item["combined_total"], reverse=True)
    winner = eligible[0]
    runner_up = eligible[1] if len(eligible) > 1 else None
    result = {
        "run_id": read_json(run_dir / "manifest.json")["run_id"],
        "premise_id": illustrative["premise_id"],
        "winner": winner,
        "runner_up": runner_up,
        "ranking": eligible,
        "finalized_at": dt.datetime.now().astimezone().isoformat(),
    }
    illustrative["winner"] = max(
        (item for item in illustrative["candidates"] if not item.get("hard_fail")),
        key=lambda item: item["weighted_total"],
    )["candidate_id"]
    krea["winner"] = max(
        (item for item in krea["candidates"] if not item.get("hard_fail")),
        key=lambda item: item["weighted_total"],
    )["candidate_id"]
    write_json(illustrious_path, illustrative)
    write_json(krea_path, krea)
    write_json(run_dir / "winner.json", result)
    manifest = read_json(run_dir / "manifest.json")
    manifest["status"] = "complete"
    manifest["winner"] = winner["candidate_id"]
    write_json(run_dir / "manifest.json", manifest)
    return run_dir / "winner.json"


def command_validate(config: dict[str, Any]) -> None:
    server_url = config["server_url"].rstrip("/")
    ensure_server(server_url)
    comfy_root = Path(config["comfy_root"])
    required_files = [
        comfy_root / "models" / "checkpoints" / config["illustrious"]["checkpoint"],
        comfy_root / "models" / "diffusion_models" / config["krea"]["model"],
        comfy_root / "models" / "text_encoders" / config["krea"]["text_encoder"],
        comfy_root / "models" / "vae" / config["krea"]["vae"],
        comfy_root / "custom_nodes" / "ComfyUI-Krea2-Ostris-Edit" / "__init__.py",
        comfy_root / "custom_nodes" / "easy_qwenEdit_2509" / "__init__.py",
    ]
    missing = [str(path) for path in required_files if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing required pipeline files:\n" + "\n".join(missing))
    print(json.dumps({"status": "ok", "server": server_url, "required_files": len(required_files)}))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--premises", type=Path, default=DEFAULT_PREMISES)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate", help="Check ComfyUI and required files")
    subparsers.add_parser("list", help="List available premise ids")

    illustrious_parser = subparsers.add_parser("illustrious", help="Generate four Illustrious candidates")
    illustrious_parser.add_argument("--premise-id", required=True)
    illustrious_parser.add_argument("--run-id")

    krea_parser = subparsers.add_parser("krea", help="Convert the four candidates through Krea")
    krea_parser.add_argument("--run-dir", type=Path, required=True)
    krea_parser.add_argument("--allow-unscored", action="store_true")

    full_parser = subparsers.add_parser("full", help="Validation mode: run both stages without score gate")
    full_parser.add_argument("--premise-id", required=True)
    full_parser.add_argument("--run-id")

    finalize_parser = subparsers.add_parser("finalize", help="Calculate combined ranking after Luna scores")
    finalize_parser.add_argument("--run-dir", type=Path, required=True)
    fast_parser = subparsers.add_parser("render-only-fast", help="Render one Illustrious and one Krea image per premise without review")
    fast_parser.add_argument("--expected-count", type=int, default=100)
    fast_parser.add_argument("--progress-every", type=int, default=10)
    fast_parser.add_argument("--batch-id")
    fast_parser.add_argument("--dry-run", action="store_true")
    fast_parser.add_argument("--take", type=int, help="Render only the first N premises, in source order")
    fast_parser.add_argument("--premise-id", action="append", help="Render only this premise id; may be repeated")
    fast_parser.add_argument("--illustrious-style-note", help="Additional global Illustrious style direction for this batch")
    fast_parser.add_argument("--framing-profile", choices=sorted(FRAMING_PROFILES), help="Replace the default Illustrious composition direction")
    fast_parser.add_argument("--illustrious-width", type=int, help="Override Illustrious output width for this batch")
    fast_parser.add_argument("--illustrious-height", type=int, help="Override Illustrious output height for this batch")
    fast_parser.add_argument("--illustrious-seed", type=int, help="Override the original Illustrious seed for this technical batch")
    fast_parser.add_argument("--illustrious-prefix", help="Prefix placed at the very start of the Illustrious prompt")
    fast_parser.add_argument("--illustrious-negative-addition", help="Additional generic Illustrious negative prompt terms")
    fast_parser.add_argument("--stop-after-illustrious", action="store_true", help="Create only Illustrious output, for composition review before Krea")
    fast_parser.add_argument("--crop-waist-up", action="store_true", help="Use a generic top 65 percent crop as Krea source")
    fast_parser.add_argument("--krea-preservation-note", help="Strict Krea image-to-image preservation text for this batch")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    config = read_json(args.config)
    config["server_url"] = COMFYUI_BASE_URL
    if COMFYUI_ROOT is not None:
        config["comfy_root"] = str(COMFYUI_ROOT)
    try:
        if args.command == "validate":
            command_validate(config)
        elif args.command == "list":
            for premise in read_premises(args.premises):
                print(f"{premise['id']}\t{premise['character']}\t{premise['premise']}")
        elif args.command == "illustrious":
            premise = find_premise(args.premises, args.premise_id)
            run_dir = run_illustrious(premise, config, args.run_id)
            print(json.dumps({"status": "awaiting_illustrious_scores", "run_dir": str(run_dir.resolve())}))
        elif args.command == "krea":
            run_dir = run_krea(args.run_dir, config, args.allow_unscored)
            print(json.dumps({"status": "awaiting_krea_scores", "run_dir": str(run_dir.resolve())}))
        elif args.command == "full":
            premise = find_premise(args.premises, args.premise_id)
            run_dir = run_illustrious(premise, config, args.run_id)
            run_krea(run_dir, config, allow_unscored=True)
            print(json.dumps({"status": "awaiting_scores", "run_dir": str(run_dir.resolve())}))
        elif args.command == "finalize":
            winner_path = finalize_run(args.run_dir)
            print(json.dumps({"status": "complete", "winner_file": str(winner_path)}))
        elif args.command == "render-only-fast":
            batch_dir = run_render_only_batch(
                args.premises, config, args.expected_count, args.progress_every,
                args.batch_id, args.dry_run, args.take, args.premise_id,
                args.illustrious_style_note, args.framing_profile, args.illustrious_width,
                args.illustrious_height, args.illustrious_seed, args.illustrious_prefix,
                args.illustrious_negative_addition, args.stop_after_illustrious,
                args.crop_waist_up, args.krea_preservation_note,
            )
            if batch_dir is not None:
                print(json.dumps({"status": "render_only_complete", "batch_dir": str(batch_dir.resolve())}))
        else:
            parser.error(f"Unknown command: {args.command}")
    except Exception as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
