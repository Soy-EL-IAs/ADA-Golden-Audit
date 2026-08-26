"""Generic Illustrious -> FLUX.2 Klein -> Krea bridge runner.

The runner reads an unchanged premise from premises/pilot_10.jsonl. It never
contains character-specific prompt text and checkpoints progress after every
candidate so a safe retry resumes instead of regenerating completed work.
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import shutil
import sys
from pathlib import Path
from typing import Any


PACKAGE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACKAGE / "scripts"))
import luna_pipeline as lp  # noqa: E402


PREMISES_PATH = PACKAGE / "premises" / "pilot_10.jsonl"
CONFIG_PATH = PACKAGE / "config" / "pipeline.json"
KLEIN_STAGE = "flux2_klein"
EXPECTED_CANDIDATES = 4


def now() -> str:
    return dt.datetime.now().astimezone().isoformat()


def read_premise(premise_id: str) -> dict[str, Any]:
    for line in PREMISES_PATH.read_text(encoding="utf-8").splitlines():
        item = json.loads(line)
        if item["id"] == premise_id:
            return item
    raise RuntimeError(f"premise {premise_id!r} not found in {PREMISES_PATH}")


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else PACKAGE / path


def assert_four(items: list[Any], label: str) -> None:
    if len(items) != EXPECTED_CANDIDATES:
        raise RuntimeError(f"expected exactly four {label}, got {len(items)}")


def scores_complete(path: Path) -> bool:
    if not path.exists():
        return False
    payload = lp.read_json(path)
    candidates = payload.get("candidates", [])
    if len(candidates) != EXPECTED_CANDIDATES:
        return False
    for candidate in candidates:
        if candidate.get("hard_fail") is None or candidate.get("summary") in (None, ""):
            return False
        scores = candidate.get("scores", {})
        if not scores or any(value is None for value in scores.values()):
            return False
    return True


def queue_is_idle(server: str) -> bool:
    queue = lp.http_json(f"{server}/queue")
    return not queue.get("queue_running") and not queue.get("queue_pending")


def validate_install(config: dict[str, Any], check_nodes: bool = True) -> dict[str, Any]:
    server = config["server_url"].rstrip("/")
    lp.ensure_server(server)
    if not queue_is_idle(server):
        raise RuntimeError("ComfyUI queue is not idle")
    comfy_root = Path(config["comfy_root"])
    klein = config["klein"]
    required_files = [
        comfy_root / "models" / "diffusion_models" / klein["model"],
        comfy_root / "models" / "text_encoders" / klein["text_encoder"],
        comfy_root / "models" / "vae" / klein["vae"],
    ]
    missing_files = [str(path) for path in required_files if not path.exists()]
    if missing_files:
        raise RuntimeError(f"missing Klein model files: {missing_files}")
    if check_nodes:
        object_info = lp.http_json(f"{server}/object_info")
        required_nodes = {
            "UNETLoader", "CLIPLoader", "VAELoader", "LoadImage",
            "ImageScaleToTotalPixels", "VAEEncode", "CLIPTextEncode",
            "FluxGuidance", "ReferenceLatent", "ConditioningZeroOut",
            "CFGGuider", "RandomNoise", "KSamplerSelect", "Flux2Scheduler",
            "EmptyFlux2LatentImage", "SamplerCustomAdvanced", "VAEDecode",
            "SaveImage",
        }
        missing_nodes = sorted(required_nodes.difference(object_info))
        if missing_nodes:
            raise RuntimeError(f"missing ComfyUI nodes: {missing_nodes}")
    return {
        "status": "ok",
        "server": server,
        "queue_idle": True,
        "model": klein["model"],
        "text_encoder": klein["text_encoder"],
        "vae": klein["vae"],
    }


def klein_prompt(premise: dict[str, Any]) -> str:
    structured = {
        "instruction": (
            "Use the supplied image only as the appearance, identity, body, and outfit reference. "
            "Reconstruct a new scene using only the premise fields below. Ignore every reference-image "
            "background, prop, action, or character that is not explicitly present below."
        ),
        "style": "polished anime game-cinematic illustration with clear visual storytelling",
        "subject": {
            "count": 1,
            "character": premise["character"],
            "franchise": premise["franchise"],
            "identity": premise["identity"],
            "appearance_direction": premise["sexual_direction"],
        },
        "action": premise["premise"],
        "must_include": premise["must_include"],
        "environment": premise["environment"],
        "animation_hook": premise["animation_hook"],
        "avoid": premise["avoid"],
        "hard_constraints": [
            "exactly one main character unless the premise explicitly requires more",
            "do not add characters, props, objects, locations, or plot events",
            "do not import scene content from any prior prompt or reference image",
            "every must_include element must be visibly readable",
        ],
    }
    return json.dumps(structured, ensure_ascii=False)


def krea_prompt(premise: dict[str, Any]) -> str:
    # Deliberately excludes sexual_direction; Krea is a conservative finishing pass.
    return (
        f"Transform the reference into {premise['krea_direction']}. "
        f"Preserve {premise['character']} from {premise['franchise']} and these identity details: "
        f"{', '.join(premise['identity'])}. Preserve the exact action: {premise['premise']} "
        f"Preserve every required element: {', '.join(premise['must_include'])}. "
        f"Preserve the environment: {', '.join(premise['environment'])}. "
        "Keep the same composition and animation-ready interaction. Do not add or remove any character, "
        "prop, object, location, or event."
    )


def klein_workflow(
    reference_name: str,
    seed: int,
    prefix: str,
    text: str,
    settings: dict[str, Any],
) -> dict[str, Any]:
    width = settings["width"]
    height = settings["height"]
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": settings["model"], "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": settings["text_encoder"], "type": "flux2", "device": "cpu"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": settings["vae"]}},
        "4": {"class_type": "LoadImage", "inputs": {"image": reference_name}},
        "5": {"class_type": "ImageScaleToTotalPixels", "inputs": {
            "image": ["4", 0], "upscale_method": "area",
            "megapixels": settings["reference_megapixels"],
            "resolution_steps": settings["reference_resolution_steps"],
        }},
        "6": {"class_type": "VAEEncode", "inputs": {"pixels": ["5", 0], "vae": ["3", 0]}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"text": text, "clip": ["2", 0]}},
        "8": {"class_type": "FluxGuidance", "inputs": {"conditioning": ["7", 0], "guidance": settings["guidance"]}},
        "9": {"class_type": "ReferenceLatent", "inputs": {"conditioning": ["8", 0], "latent": ["6", 0]}},
        "10": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["7", 0]}},
        "11": {"class_type": "CFGGuider", "inputs": {"model": ["1", 0], "positive": ["9", 0], "negative": ["10", 0], "cfg": settings["cfg"]}},
        "12": {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}},
        "13": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": settings["sampler"]}},
        "14": {"class_type": "Flux2Scheduler", "inputs": {"steps": settings["steps"], "width": width, "height": height}},
        "15": {"class_type": "EmptyFlux2LatentImage", "inputs": {"width": width, "height": height, "batch_size": 1}},
        "16": {"class_type": "SamplerCustomAdvanced", "inputs": {"noise": ["12", 0], "guider": ["11", 0], "sampler": ["13", 0], "sigmas": ["14", 0], "latent_image": ["15", 0]}},
        "17": {"class_type": "VAEDecode", "inputs": {"samples": ["16", 0], "vae": ["3", 0]}},
        "18": {"class_type": "SaveImage", "inputs": {"images": ["17", 0], "filename_prefix": prefix}},
    }


def klein_score_template(
    premise_id: str,
    candidates: list[dict[str, Any]],
    weights: dict[str, float],
) -> dict[str, Any]:
    return {
        "premise_id": premise_id,
        "stage": KLEIN_STAGE,
        "weights": weights,
        "candidates": [
            {
                "candidate_id": item["candidate_id"],
                "image_path": item["local_image_path"],
                "hard_fail": False,
                "hard_fail_reasons": [],
                "scores": {name: None for name in weights},
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


def default_run_dir(source_run: Path) -> Path:
    return PACKAGE / "experimental_runs" / f"{source_run.name}_flux2_klein_bridge"


def initialize_manifest(
    run_dir: Path,
    premise_id: str,
    source_run: Path,
    config: dict[str, Any],
) -> dict[str, Any]:
    manifest_path = run_dir / "manifest.json"
    if manifest_path.exists():
        manifest = lp.read_json(manifest_path)
        if manifest.get("premise_id") != premise_id or Path(manifest.get("source_run", "")) != source_run:
            raise RuntimeError("existing run manifest does not match premise/source run")
        return manifest
    if run_dir.exists() and any(run_dir.iterdir()):
        raise RuntimeError(f"run directory exists without a resumable manifest: {run_dir}")
    for name in ("workflows", "inputs", "klein"):
        (run_dir / name).mkdir(parents=True, exist_ok=True)
    manifest = {
        "experiment": "flux2_klein_bridge",
        "run_id": run_dir.name,
        "premise_id": premise_id,
        "source_run": str(source_run),
        "created_at": now(),
        "status": "generating_klein",
        "klein_candidates": [],
        "krea_candidates": [],
    }
    lp.write_json(manifest_path, manifest)
    lp.write_json(run_dir / "config.json", {
        "experiment": "Illustrious -> FLUX.2 Klein -> Krea",
        "premise_id": premise_id,
        "source_run": str(source_run),
        "klein": config["klein"],
        "krea": config["krea"],
        "final_formula": config["bridge_final_formula"],
    })
    return manifest


def run_klein(premise_id: str, source_run_arg: str, run_dir_arg: str | None) -> Path:
    config = lp.read_json(CONFIG_PATH)
    validate_install(config)
    premise = read_premise(premise_id)
    source_run = resolve_path(source_run_arg).resolve()
    source_manifest = lp.read_json(source_run / "manifest.json")
    if source_manifest.get("premise_id") != premise_id:
        raise RuntimeError("source run premise does not match requested premise")
    sources = source_manifest.get("illustrious_candidates", [])
    assert_four(sources, "Illustrious candidates")
    source_scores = source_run / "scores_illustrious.json"
    if not scores_complete(source_scores):
        raise RuntimeError("Illustrious scores must be complete before Klein")
    run_dir = resolve_path(run_dir_arg).resolve() if run_dir_arg else default_run_dir(source_run).resolve()
    manifest = initialize_manifest(run_dir, premise_id, source_run, config)
    completed = {item["candidate_id"] for item in manifest.get("klein_candidates", [])}
    if len(completed) == EXPECTED_CANDIDATES:
        raise RuntimeError("all four Klein candidates already exist; refusing to regenerate")
    shutil.copy2(source_scores, run_dir / "scores_illustrious.json")
    server = config["server_url"].rstrip("/")
    comfy_root = Path(config["comfy_root"])
    settings = config["klein"]
    text = klein_prompt(premise)
    for index, source in enumerate(sources, 1):
        candidate_id = f"candidate_{index:02d}"
        if candidate_id in completed:
            continue
        if not queue_is_idle(server):
            raise RuntimeError("ComfyUI queue became busy; refusing to submit")
        source_path = Path(source["image_path"])
        if not source_path.exists():
            raise FileNotFoundError(source_path)
        reference_name = f"luna_bridge_{run_dir.name}_illustrious_{index:02d}.png"
        local_reference = run_dir / "inputs" / reference_name
        shutil.copy2(source_path, local_reference)
        uploaded = lp.upload_input_image(server, source_path, reference_name, f"LunaBridge/inputs/{run_dir.name}")
        seed = int(premise["seed_base"]) + index - 1
        prefix = f"LunaBridge/{run_dir.name}/klein/{candidate_id}"
        prompt = klein_workflow(uploaded, seed, prefix, text, settings)
        workflow_path = run_dir / "workflows" / f"klein_{candidate_id}_submitted.json"
        lp.write_json(workflow_path, prompt)
        prompt_id = lp.submit_prompt(server, prompt, f"luna-bridge-{run_dir.name}-klein-{index:02d}")
        history = lp.wait_for_history(
            server, prompt_id, settings["timeout_seconds"], config["timeouts"]["poll_seconds"]
        )
        images = lp.output_images(history, "18")
        if len(images) != 1:
            raise RuntimeError(f"expected one Klein image for candidate {index}, got {len(images)}")
        image_path = lp.image_absolute_path(comfy_root, images[0])
        local_path = run_dir / "klein" / images[0]["filename"]
        shutil.copy2(image_path, local_path)
        manifest["klein_candidates"].append({
            "candidate_id": candidate_id,
            "source_illustrious_path": str(source_path),
            "reference_input": str(local_reference),
            "image_path": str(image_path),
            "local_image_path": str(local_path),
            "comfy_descriptor": images[0],
            "prompt_id": prompt_id,
            "seed": seed,
        })
        lp.write_json(run_dir / "manifest.json", manifest)
    assert_four(manifest["klein_candidates"], "Klein candidates")
    manifest["status"] = "awaiting_klein_scores"
    manifest["klein_completed_at"] = now()
    lp.write_json(run_dir / "manifest.json", manifest)
    score_path = run_dir / "scores_klein.json"
    if not score_path.exists():
        lp.write_json(score_path, klein_score_template(
            premise_id, manifest["klein_candidates"], settings["score_weights"]
        ))
    return run_dir


def run_krea(run_dir_arg: str) -> Path:
    run_dir = resolve_path(run_dir_arg).resolve()
    config = lp.read_json(CONFIG_PATH)
    server = config["server_url"].rstrip("/")
    lp.ensure_server(server)
    if not queue_is_idle(server):
        raise RuntimeError("ComfyUI queue is not idle")
    manifest_path = run_dir / "manifest.json"
    manifest = lp.read_json(manifest_path)
    sources = manifest.get("klein_candidates", [])
    assert_four(sources, "Klein candidates")
    if not scores_complete(run_dir / "scores_klein.json"):
        raise RuntimeError("Klein scores must be complete before Krea")
    premise = read_premise(manifest["premise_id"])
    settings = config["krea"]
    completed = {item["candidate_id"] for item in manifest.get("krea_candidates", [])}
    if len(completed) == EXPECTED_CANDIDATES:
        raise RuntimeError("all four Krea candidates already exist; refusing to regenerate")
    manifest["status"] = "generating_krea"
    lp.write_json(manifest_path, manifest)
    for index, source in enumerate(sources, 1):
        candidate_id = f"candidate_{index:02d}"
        if candidate_id in completed:
            continue
        if not queue_is_idle(server):
            raise RuntimeError("ComfyUI queue became busy; refusing to submit")
        source_path = Path(source["local_image_path"])
        if not source_path.exists():
            raise FileNotFoundError(source_path)
        input_name = f"luna_bridge_{manifest['run_id']}_klein_{index:02d}.png"
        uploaded = lp.upload_input_image(server, source_path, input_name, f"LunaBridge/inputs/{manifest['run_id']}")
        prompt = copy.deepcopy(lp.read_json(lp.KREA_WORKFLOW))
        prompt["1"]["inputs"]["unet_name"] = settings["model"]
        prompt["2"]["inputs"]["clip_name"] = settings["text_encoder"]
        prompt["3"]["inputs"]["vae_name"] = settings["vae"]
        prompt["4"]["inputs"]["image"] = uploaded
        prompt["5"]["inputs"].update(width=settings["width"], height=settings["height"])
        prompt["6"]["inputs"].update(vl_size=settings["vl_size"], prompt=krea_prompt(premise))
        prompt["9"]["inputs"]["kv_cache"] = settings["kv_cache"]
        prompt["10"]["inputs"].update(
            seed=int(premise["krea_seed_base"]) + index - 1,
            steps=settings["steps"], cfg=settings["cfg"],
            sampler_name=settings["sampler"], scheduler=settings["scheduler"],
        )
        prompt["12"]["inputs"]["filename_prefix"] = f"LunaBridge/{manifest['run_id']}/krea/{candidate_id}"
        lp.write_json(run_dir / "workflows" / f"krea_{candidate_id}_submitted.json", prompt)
        prompt_id = lp.submit_prompt(server, prompt, f"luna-bridge-{manifest['run_id']}-krea-{index:02d}")
        history = lp.wait_for_history(
            server, prompt_id, config["timeouts"]["krea_seconds"], config["timeouts"]["poll_seconds"]
        )
        images = lp.output_images(history, "12")
        if len(images) != 1:
            raise RuntimeError(f"expected one Krea image for candidate {index}, got {len(images)}")
        manifest.setdefault("krea_candidates", []).append({
            "candidate_id": candidate_id,
            "source_klein_path": str(source_path),
            "image_path": str(lp.image_absolute_path(Path(config["comfy_root"]), images[0])),
            "comfy_descriptor": images[0],
            "prompt_id": prompt_id,
        })
        lp.write_json(manifest_path, manifest)
    assert_four(manifest["krea_candidates"], "Krea candidates")
    manifest["status"] = "awaiting_krea_scores"
    manifest["krea_completed_at"] = now()
    lp.write_json(manifest_path, manifest)
    score_path = run_dir / "scores_krea.json"
    if not score_path.exists():
        rubric = lp.read_json(lp.RUBRIC_PATH)
        lp.write_json(score_path, lp.score_template(
            manifest["premise_id"], "krea", manifest["krea_candidates"], rubric
        ))
    return run_dir


def weighted_total(candidate: dict[str, Any], weights: dict[str, float]) -> float:
    return round(sum(float(candidate["scores"][name]) * weight for name, weight in weights.items()), 3)


def finalize(run_dir_arg: str) -> Path:
    run_dir = resolve_path(run_dir_arg).resolve()
    config = lp.read_json(CONFIG_PATH)
    manifest_path = run_dir / "manifest.json"
    manifest = lp.read_json(manifest_path)
    klein_path = run_dir / "scores_klein.json"
    krea_path = run_dir / "scores_krea.json"
    if not scores_complete(klein_path) or not scores_complete(krea_path):
        raise RuntimeError("Klein and Krea scores must be complete before finalize")
    klein_scores = lp.read_json(klein_path)
    krea_scores = lp.read_json(krea_path)
    klein_map = {item["candidate_id"]: item for item in klein_scores["candidates"]}
    krea_map = {item["candidate_id"]: item for item in krea_scores["candidates"]}
    assert_four(list(klein_map), "Klein scores")
    assert_four(list(krea_map), "Krea scores")
    klein_weights = config["klein"]["score_weights"]
    krea_weights = lp.read_json(lp.RUBRIC_PATH)["krea"]
    formula = config["bridge_final_formula"]
    ranking = []
    hard_fails: dict[str, list[str]] = {}
    for candidate_id in sorted(klein_map):
        klein = klein_map[candidate_id]
        krea = krea_map[candidate_id]
        klein_total = weighted_total(klein, klein_weights)
        krea_total = weighted_total(krea, krea_weights)
        klein["weighted_total"] = klein_total
        krea["weighted_total"] = krea_total
        failed = bool(klein.get("hard_fail") or krea.get("hard_fail"))
        reasons = list(dict.fromkeys(
            list(klein.get("hard_fail_reasons", [])) + list(krea.get("hard_fail_reasons", []))
        ))
        if failed:
            hard_fails[candidate_id] = reasons
        ranking.append({
            "candidate_id": candidate_id,
            "klein_total": klein_total,
            "krea_total": krea_total,
            "combined_total": round(
                klein_total * formula["klein_total"] + krea_total * formula["krea_total"], 3
            ),
            "hard_fail": failed,
        })
    ranking.sort(key=lambda item: item["combined_total"], reverse=True)
    valid = [item for item in ranking if not item["hard_fail"]]
    result = {
        "experiment": "Illustrious -> FLUX.2 Klein 9B -> Krea",
        "run_id": manifest["run_id"],
        "premise_id": manifest["premise_id"],
        "weights": formula,
        "winner": valid[0] if valid else None,
        "runner_up": valid[1] if len(valid) > 1 else None,
        "ranking": ranking,
        "hard_fails": hard_fails,
        "valid_counts": {
            "klein": sum(not item.get("hard_fail", False) for item in klein_scores["candidates"]),
            "krea": sum(not item.get("hard_fail", False) for item in krea_scores["candidates"]),
            "final": len(valid),
            "total": EXPECTED_CANDIDATES,
        },
        "finalized_at": now(),
    }
    lp.write_json(klein_path, klein_scores)
    lp.write_json(krea_path, krea_scores)
    lp.write_json(run_dir / "winner.json", result)
    lp.write_json(run_dir / "experimental_result.json", result)
    manifest["status"] = "complete"
    manifest["result_file"] = "winner.json"
    manifest["finalized_at"] = result["finalized_at"]
    lp.write_json(manifest_path, manifest)
    return run_dir


def inspect_paths(run_dir_arg: str, stage: str) -> list[str]:
    run_dir = resolve_path(run_dir_arg).resolve()
    manifest = lp.read_json(run_dir / "manifest.json")
    key = "klein_candidates" if stage == "klein" else "krea_candidates"
    candidates = manifest.get(key, [])
    assert_four(candidates, f"{stage} candidates")
    field = "local_image_path" if stage == "klein" else "image_path"
    return [str(item[field]) for item in candidates]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate", help="validate fixed models, nodes, server, and idle queue")
    klein = sub.add_parser("klein", help="generate/resume four Klein references sequentially")
    klein.add_argument("--premise-id", required=True)
    klein.add_argument("--source-run", required=True)
    klein.add_argument("--run-dir")
    krea = sub.add_parser("krea", help="generate/resume four Krea conversions sequentially")
    krea.add_argument("--run-dir", required=True)
    inspect = sub.add_parser("inspect", help="print all four image paths for one-pass review")
    inspect.add_argument("--run-dir", required=True)
    inspect.add_argument("--stage", choices=("klein", "krea"), required=True)
    final = sub.add_parser("finalize", help="finalize completed score files")
    final.add_argument("--run-dir", required=True)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "validate":
        result: Any = validate_install(lp.read_json(CONFIG_PATH))
    elif args.command == "klein":
        result = {"status": "awaiting_klein_scores", "run_dir": str(run_klein(
            args.premise_id, args.source_run, args.run_dir
        ))}
    elif args.command == "krea":
        result = {"status": "awaiting_krea_scores", "run_dir": str(run_krea(args.run_dir))}
    elif args.command == "inspect":
        result = {"stage": args.stage, "images": inspect_paths(args.run_dir, args.stage)}
    else:
        run_dir = finalize(args.run_dir)
        result = lp.read_json(run_dir / "winner.json")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
