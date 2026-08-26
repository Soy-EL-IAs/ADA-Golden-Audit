#!/usr/bin/env python3
"""Benchmark the configured LM Studio Vision Worker on existing pipeline outputs only."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import statistics
import sys
import time
from pathlib import Path
from typing import Any

if __package__:
    from .ada_paths import COMFYUI_ROOT, CONFIG_ROOT, KLEIN_BATCH_RUNS_ROOT, VISUAL_REVIEW_RUNS_ROOT, resolve_legacy_path
    from .character_profile import CharacterProfileDatabase
    from .lmstudio_controller import LMStudioController
    from .visual_reviewer import review_image
else:
    from ada_paths import COMFYUI_ROOT, CONFIG_ROOT, KLEIN_BATCH_RUNS_ROOT, VISUAL_REVIEW_RUNS_ROOT, resolve_legacy_path
    from character_profile import CharacterProfileDatabase
    from lmstudio_controller import LMStudioController
    from visual_reviewer import review_image


DEFAULT_CONFIG = CONFIG_ROOT.parent / "legacy" / "config" / "reviews" / "visual_review_benchmark_v1.json"
OUTPUT_ROOT = VISUAL_REVIEW_RUNS_ROOT
if COMFYUI_ROOT is None:
    raise RuntimeError("COMFYUI_ROOT is not configured")
COMFY_ROOT = COMFYUI_ROOT


def descriptor_path(descriptor: dict[str, Any]) -> Path:
    folder = {"output": "output", "input": "input", "temp": "temp"}.get(descriptor.get("type", "output"))
    if folder is None:
        raise ValueError(f"Unsupported image descriptor: {descriptor}")
    return COMFY_ROOT / folder / descriptor.get("subfolder", "") / descriptor["filename"]


def load_cases(path: Path) -> list[dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("schema_version") != 1 or not isinstance(value.get("cases"), list):
        raise ValueError(f"{path}: expected schema_version 1 with cases")
    return value["cases"]


def resolve_case(case: dict[str, Any], profiles: CharacterProfileDatabase) -> dict[str, Any]:
    batch_id = case["batch_id"]
    record_id = case["record_id"]
    manifest_path = KLEIN_BATCH_RUNS_ROOT / batch_id / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    record = next((item for item in manifest.get("records", []) if item.get("id") == record_id), None)
    if not isinstance(record, dict) or record.get("status") != "complete":
        raise ValueError(f"{batch_id}/{record_id}: no completed record")
    dataset_path = resolve_legacy_path(manifest["dataset"])
    dataset = [json.loads(line) for line in dataset_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    source = next((item for item in dataset if item.get("id") == record_id), {})
    character = source.get("character", case.get("character", ""))
    version = case.get("version")
    profile_name = character.split(" / ", 1)[0].strip()
    profile = profiles.get_character_profile(profile_name, version)
    context = {
        "record_id": record_id,
        "character": character,
        "version": version,
        "category": source.get("category"),
        "premise": source.get("premise"),
        "illustrious_prompt": source.get("illustrious_prompt"),
        "klein_prompt": source.get("klein_prompt"),
        "character_profile": profile.get("character_profile") if profile.get("character_profile_used") else None,
        "expected_observations": case.get("expected_observations", []),
    }
    return {
        "case_id": case["case_id"], "batch_id": batch_id, "record_id": record_id,
        "expectation": case.get("expectation", "exploratory"), "context": context,
        "klein_image": descriptor_path(record["klein"][0]),
        "illustrious_image": descriptor_path(record["illustrious"][0]),
        "comparison_image": descriptor_path(record["compare"][0]),
    }


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--benchmark-id", default=dt.datetime.now().strftime("worker_vision_v1_%Y%m%d_%H%M%S"))
    args = parser.parse_args()
    config_path = args.config.resolve()
    cases = load_cases(config_path)
    run_dir = OUTPUT_ROOT / args.benchmark_id
    if run_dir.exists():
        raise FileExistsError(f"Refusing to overwrite benchmark: {run_dir}")
    resolved = [resolve_case(case, CharacterProfileDatabase()) for case in cases]
    missing = [str(item["klein_image"]) for item in resolved if not item["klein_image"].is_file()]
    missing += [str(item["illustrious_image"]) for item in resolved if not item["illustrious_image"].is_file()]
    missing += [str(item["comparison_image"]) for item in resolved if not item["comparison_image"].is_file()]
    if missing:
        raise FileNotFoundError("Benchmark images missing:\n" + "\n".join(missing))

    controller = LMStudioController()
    inventory_before = controller.list_models()
    master_was_loaded = any(item.get("model") == controller.role("master").model for item in inventory_before["loaded"])
    run_dir.mkdir(parents=True)
    write_json(run_dir / "input_cases.json", {
        "config": str(config_path),
        "cases": [{
            **{key: item[key] for key in ("case_id", "batch_id", "record_id", "expectation", "context")},
            "klein_image": str(item["klein_image"]),
            "illustrious_image": str(item["illustrious_image"]),
            "comparison_image": str(item["comparison_image"]),
        } for item in resolved],
    })
    load_started = time.perf_counter()
    role = controller.begin_review(deep=False)
    load_seconds = round(time.perf_counter() - load_started, 3)
    results: list[dict[str, Any]] = []
    restore: dict[str, Any] | None = None
    try:
        for item in resolved:
            row = {key: item[key] for key in ("case_id", "batch_id", "record_id", "expectation")}
            row["klein_image"] = str(item["klein_image"])
            row["illustrious_image"] = str(item["illustrious_image"])
            row["comparison_image"] = str(item["comparison_image"])
            try:
                row["review"] = review_image(
                    item["klein_image"], illustrious_image=item["illustrious_image"], comparison_image=item["comparison_image"], context=item["context"],
                    model=role.model, base_url=controller.base_url, ttl_seconds=role.ttl_seconds,
                )
                row["status"] = "complete"
            except Exception as exc:
                row.update(status="error", error=str(exc))
            results.append(row)
            write_jsonl(run_dir / "results.jsonl", results)
    finally:
        controller.unload_role("worker")
        controller.wait_for_vram_release()
        if master_was_loaded:
            restore = controller.ensure_loaded("master")
        controller.finish_work()

    complete = [item["review"] for item in results if item["status"] == "complete"]
    verdicts = {name: sum(item["verdict"] == name for item in complete) for name in ("PASS", "REVIEW", "REJECT")}
    elapsed = [item["elapsed_seconds"] for item in complete]
    summary = {
        "benchmark_id": args.benchmark_id, "status": "complete", "model": role.model,
        "count": len(results), "completed": len(complete), "errors": len(results) - len(complete),
        "worker_load_seconds": load_seconds, "total_review_seconds": round(sum(elapsed), 3),
        "mean_seconds_per_image": round(statistics.mean(elapsed), 3) if elapsed else None,
        "verdicts": verdicts, "master_was_loaded": master_was_loaded, "master_restored": restore is not None,
    }
    write_json(run_dir / "summary.json", summary)
    lines = [
        "# Worker Vision v1 benchmark", "", f"- Model: `{role.model}`", f"- Cases: {len(results)}",
        f"- Worker load: {load_seconds}s", f"- Mean review: {summary['mean_seconds_per_image']}s",
        f"- Verdicts: PASS {verdicts['PASS']}, REVIEW {verdicts['REVIEW']}, REJECT {verdicts['REJECT']}", "",
        "## Results", "",
    ]
    for item in results:
        if item["status"] == "complete":
            review = item["review"]
            lines.append(f"- `{item['case_id']}` — **{review['verdict']}**; identity {review['identity']}/10, anatomy {review['anatomy']}/10, appeal {review['visual_appeal']}/10, viral {review['viral_hook']}/10. {review['reason']}")
        else:
            lines.append(f"- `{item['case_id']}` — **ERROR**: {item['error']}")
    (run_dir / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"run_dir": str(run_dir.resolve()), **summary}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
