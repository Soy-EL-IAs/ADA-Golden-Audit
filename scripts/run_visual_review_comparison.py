#!/usr/bin/env python3
"""Compare the configured Worker and Master on identical existing visual-review inputs."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import statistics
import time
from pathlib import Path
from typing import Any

if __package__:
    from .ada_paths import CONFIG_ROOT, VISUAL_REVIEW_RUNS_ROOT, resolve_legacy_path
    from .lmstudio_controller import LMStudioController
    from .visual_reviewer import review_image, review_master_image
else:
    from ada_paths import CONFIG_ROOT, VISUAL_REVIEW_RUNS_ROOT, resolve_legacy_path
    from lmstudio_controller import LMStudioController
    from visual_reviewer import review_image, review_master_image


DEFAULT_CONFIG = CONFIG_ROOT.parent / "legacy" / "config" / "reviews" / "visual_review_comparison_v1.json"
OUTPUT_ROOT = VISUAL_REVIEW_RUNS_ROOT


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_cases(config_path: Path) -> list[dict[str, Any]]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(config, dict) or config.get("schema_version") != 1:
        raise ValueError(f"{config_path}: expected schema_version 1")
    source_path = resolve_legacy_path(config["source_benchmark"])
    source = json.loads(source_path.read_text(encoding="utf-8"))
    case_map = {case["case_id"]: case for case in source.get("cases", [])}
    missing = [case_id for case_id in config["case_ids"] if case_id not in case_map]
    if missing:
        raise ValueError(f"Comparison cases missing from source benchmark: {missing}")
    cases = [case_map[case_id] for case_id in config["case_ids"]]
    for case in cases:
        for key in ("klein_image", "illustrious_image", "comparison_image"):
            case[key] = str(resolve_legacy_path(case[key]))
            if not Path(case[key]).is_file():
                raise FileNotFoundError(case[key])
    return cases


def run_role(controller: LMStudioController, role_name: str, cases: list[dict[str, Any]]) -> dict[str, Any]:
    started = time.perf_counter()
    role = controller.begin_review(deep=role_name == "master")
    load_seconds = round(time.perf_counter() - started, 3)
    rows: list[dict[str, Any]] = []
    try:
        for case in cases:
            row = {"case_id": case["case_id"]}
            try:
                # Only `model` differs between roles. Context, images, prompt/schema,
                # decoding parameters and TTL omission are deliberately identical.
                review_fn = review_master_image if role_name == "master" else review_image
                row["review"] = review_fn(
                    Path(case["klein_image"]), illustrious_image=Path(case["illustrious_image"]),
                    comparison_image=Path(case["comparison_image"]), context=case["context"],
                    model=role.model, base_url=controller.base_url, ttl_seconds=None,
                )
                row["status"] = "complete"
            except Exception as exc:
                row.update(status="error", error=str(exc))
            rows.append(row)
    finally:
        controller.unload_role(role_name)
        controller.wait_for_vram_release()
        controller.finish_work()
    elapsed = [item["review"]["elapsed_seconds"] for item in rows if item["status"] == "complete"]
    return {
        "model": role.model, "worker_or_master": role_name, "load_seconds": load_seconds,
        "mean_seconds_per_image": round(statistics.mean(elapsed), 3) if elapsed else None,
        "total_review_seconds": round(sum(elapsed), 3), "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--comparison-id", default=dt.datetime.now().strftime("worker_vs_master_v1_%Y%m%d_%H%M%S"))
    args = parser.parse_args()
    run_dir = OUTPUT_ROOT / args.comparison_id
    if run_dir.exists():
        raise FileExistsError(f"Refusing to overwrite comparison: {run_dir}")
    cases = load_cases(args.config.resolve())
    controller = LMStudioController()
    before = controller.list_models()
    master_was_loaded = any(item.get("model") == controller.role("master").model for item in before["loaded"])
    run_dir.mkdir(parents=True)
    write_json(run_dir / "input_cases.json", {"config": str(args.config.resolve()), "cases": cases})
    worker = run_role(controller, "worker", cases)
    master = run_role(controller, "master", cases)
    if master_was_loaded:
        controller.ensure_loaded("master")
        restored = True
    else:
        controller.unload_role("master")
        controller.wait_for_vram_release()
        restored = False

    comparisons = []
    worker_rows = {item["case_id"]: item for item in worker["rows"]}
    master_rows = {item["case_id"]: item for item in master["rows"]}
    for case in cases:
        comparisons.append({"case_id": case["case_id"], "expectation": case["expectation"],
                            "worker": worker_rows[case["case_id"]], "master": master_rows[case["case_id"]]})
    result = {
        "comparison_id": args.comparison_id, "status": "complete", "cases": len(cases),
        "master_was_loaded": master_was_loaded, "master_restored": restored,
        "worker": worker, "master": master, "comparisons": comparisons,
    }
    write_json(run_dir / "results.json", result)
    lines = ["# Worker 8B vs Master 27B", "", f"- Cases: {len(cases)}",
             f"- Worker: `{worker['model']}` — {worker['mean_seconds_per_image']} s/image",
             f"- Master: `{master['model']}` — {master['mean_seconds_per_image']} s/image", "",
             "| Case | Worker | Master |", "|---|---|---|"]
    for item in comparisons:
        def brief(value: dict[str, Any]) -> str:
            if value["status"] != "complete":
                return "ERROR"
            review = value["review"]
            return f"{review['verdict']} (id {review['identity']}, an {review['anatomy']})"
        lines.append(f"| {item['case_id']} | {brief(item['worker'])} | {brief(item['master'])} |")
    (run_dir / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"run_dir": str(run_dir.resolve()), "worker_seconds": worker["mean_seconds_per_image"],
                      "master_seconds": master["mean_seconds_per_image"], "cases": len(cases)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
