"""Isolated Model Registry and controlled Model Lab runs."""

from __future__ import annotations

import json
import mimetypes
import sys
import time
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts.ada_paths import ADA_ROOT, COMFYUI_BASE_URL, EXPERIMENTAL_ROOT, MISSION_RUNS_ROOT

SCRIPTS_DIR = ADA_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.append(str(SCRIPTS_DIR))

from lmstudio_controller import LMStudioController
from model_scanner import PROFILES_DIR, REGISTRY_PATH, scan_models
from production_workflows import build_klein_workflow, workflow_generation_details
from run_specialist_mini_e2e import output_path, submit, wait_history


MODEL_LAB_ROOT = EXPERIMENTAL_ROOT / "model_lab"
KLEIN_BASELINE_PROMPT = (
    "Make it hyper-realistic while preserving the exact facial identity, facial proportions, expression, pose, "
    "framing, hairstyle and outfit of the source image. Keep her vivid golden-yellow eyes, tan skin and purple hair "
    "unchanged. Improve natural skin texture, facial detail, individual hair strands, realistic fabric and lighting. "
    "Do not soften or change her expression."
)


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _http_json(url: str) -> dict[str, Any]:
    with urllib.request.urlopen(url, timeout=10) as response:
        value = json.loads(response.read().decode("utf-8"))
    return value if isinstance(value, dict) else {}


def _vram_snapshot() -> dict[str, Any]:
    try:
        stats = _http_json(COMFYUI_BASE_URL + "/system_stats")
        devices = stats.get("devices", [])
        device = devices[0] if devices and isinstance(devices[0], dict) else {}
        return {
            "device": device.get("name"),
            "total_bytes": device.get("vram_total"),
            "free_bytes": device.get("vram_free"),
            "used_bytes": (device.get("vram_total") - device.get("vram_free")) if isinstance(device.get("vram_total"), int) and isinstance(device.get("vram_free"), int) else None,
        }
    except Exception as exc:
        return {"error": str(exc)}


def _upload(path: Path, name: str) -> str:
    boundary = ("----AdaModelLab" + uuid.uuid4().hex).encode("ascii")
    body = bytearray()
    body.extend(b"--" + boundary + b"\r\nContent-Disposition: form-data; name=\"image\"; filename=\"" + name.encode("utf-8") + b"\"\r\n")
    body.extend(b"Content-Type: " + (mimetypes.guess_type(name)[0] or "image/png").encode("ascii") + b"\r\n\r\n")
    body.extend(path.read_bytes())
    body.extend(b"\r\n--" + boundary + b"--\r\n")
    request = urllib.request.Request(
        COMFYUI_BASE_URL + "/upload/image", data=bytes(body), method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary.decode('ascii')}"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.loads(response.read().decode("utf-8"))
    return str(result.get("name", name))


def registry_view() -> dict[str, Any]:
    from ada_app.direct_generator_lab import recipe_catalog

    registry = _read(REGISTRY_PATH) if REGISTRY_PATH.is_file() else scan_models()
    recipes = recipe_catalog()
    models = []
    for model in registry.get("models", []):
        profile_path = PROFILES_DIR / f"{model.get('id')}.json"
        profile = _read(profile_path) if profile_path.is_file() else {}
        direct_recipes = [recipe for recipe in recipes if recipe.get("model_id") == model.get("id")]
        models.append({**model, "capability_profile": profile, "direct_generator_recipes": direct_recipes})
    return {
        **registry,
        "models": models,
        "runs": list_test_receipts(),
        "suggested_source": suggested_yoruichi_source(),
        "default_prompt": KLEIN_BASELINE_PROMPT,
        "direct_generator_recipes": recipes,
    }


def list_test_receipts() -> list[dict[str, Any]]:
    if not MODEL_LAB_ROOT.is_dir():
        return []
    receipts = []
    for path in MODEL_LAB_ROOT.glob("*/model_test_receipt.json"):
        try:
            value = _read(path)
            if isinstance(value, dict):
                receipts.append(value)
        except Exception:
            continue
    return sorted(receipts, key=lambda item: item.get("started_at", ""), reverse=True)


def suggested_yoruichi_source() -> str:
    root = MISSION_RUNS_ROOT
    candidates = sorted(root.glob("m2_*/pilot_candidates.json"), key=lambda path: path.stat().st_mtime, reverse=True) if root.is_dir() else []
    for path in candidates:
        try:
            for candidate in _read(path):
                if candidate.get("character") != "Shihouin Yoruichi":
                    continue
                receipt = candidate.get("illustrious_render_receipt", {})
                source = receipt.get("output_asset") if isinstance(receipt, dict) else None
                if isinstance(source, str) and Path(source).is_file():
                    return source
        except Exception:
            continue
    return ""


def run_model_test(
    *, model_id: str, source_image: str, character: str,
    prompt: str | None = None, seed: int = 20260824,
    artifact_root: Path | None = None, adopted_from: str | None = None,
) -> dict[str, Any]:
    registry = registry_view()
    model = next((item for item in registry["models"] if item.get("id") == model_id), None)
    if model is None:
        raise ValueError("Unknown Model Lab model")
    recipe = model.get("capability_profile", {}).get("test_recipe", {})
    if recipe.get("status") != "ready" or recipe.get("runner") != "klein_production_baseline_v1":
        raise ValueError(f"Model is discovered but not runnable: {recipe.get('reason', 'test recipe is not confirmed')}")
    source = Path(source_image)
    if not source.is_file():
        raise ValueError("Model Lab source image does not exist")
    effective_prompt = (prompt or KLEIN_BASELINE_PROMPT).strip()
    if not effective_prompt:
        raise ValueError("Model Lab prompt must not be empty")

    now = datetime.now(timezone.utc)
    run_id = f"model_lab_{now.strftime('%Y%m%d_%H%M%S')}_{model_id}_{uuid.uuid4().hex[:6]}"
    run_dir = artifact_root or (MODEL_LAB_ROOT / run_id)
    run_dir.mkdir(parents=True, exist_ok=False)
    receipt: dict[str, Any] = {
        "schema_version": "model_test_receipt_v1",
        "run_id": run_id,
        "model_id": model_id,
        "model_file": model.get("file"),
        "model_version": model.get("version"),
        "character": character,
        "task": "anime_to_realistic_conversion",
        "status": "RUNNING",
        "started_at": now.isoformat(),
        "input_asset": str(source.resolve()),
        "output_asset": None,
        "prompt": effective_prompt,
        "seed": int(seed),
        "configuration": {},
        "checkpoint": model.get("file"),
        "adapters": [],
        "workflow": None,
        "duration_seconds": None,
        "vram": {"before": _vram_snapshot(), "after": None},
        "result": {"score": None, "human_notes": None},
        "error": None,
        "adopted_from": adopted_from,
    }
    _write(run_dir / "model_test_receipt.json", receipt)
    started = time.perf_counter()
    try:
        controller = LMStudioController()
        controller.prepare_for_comfy(lambda: controller.comfy_status(COMFYUI_BASE_URL))
        uploaded = _upload(source, f"{run_id}_source{source.suffix or '.png'}")
        workflow = build_klein_workflow(
            input_image=uploaded,
            positive_prompt=effective_prompt,
            seed=int(seed),
            output_prefix=f"ADA/MODEL_LAB/{run_id}/output",
        )
        receipt["configuration"] = workflow_generation_details("klein", workflow)
        receipt["checkpoint"] = receipt["configuration"].get("checkpoint")
        receipt["adapters"] = receipt["configuration"].get("loras", [])
        receipt["workflow"] = receipt["configuration"].get("workflow")
        prompt_id = submit(COMFYUI_BASE_URL, workflow, run_id)
        receipt["prompt_id"] = prompt_id
        history = wait_history(COMFYUI_BASE_URL, prompt_id, timeout=300)
        output = output_path(history, "20")
        receipt.update({
            "status": "COMPLETE",
            "output_asset": str(output),
            "duration_seconds": round(time.perf_counter() - started, 3),
        })
    except Exception as exc:
        receipt.update({"status": "FAILED", "duration_seconds": round(time.perf_counter() - started, 3), "error": f"{type(exc).__name__}: {exc}"})
    receipt["vram"]["after"] = _vram_snapshot()
    receipt["completed_at"] = datetime.now(timezone.utc).isoformat()
    _write(run_dir / "model_test_receipt.json", receipt)
    return receipt
