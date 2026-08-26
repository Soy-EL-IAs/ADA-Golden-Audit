#!/usr/bin/env python3
"""One-shot Worker review and VRAM exclusion smoke check for ADA migration."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ada_paths import VISUAL_REVIEW_RUNS_ROOT, resolve_legacy_path  # noqa: E402
from lmstudio_controller import LMStudioController  # noqa: E402
from visual_reviewer import review_image  # noqa: E402


def loaded_models(controller: LMStudioController) -> list[str]:
    return [str(item.get("model")) for item in controller.list_models()["loaded"]]


def main() -> int:
    target = ROOT / "migration" / "lmstudio_smoke_results.json"
    if target.exists():
        raise FileExistsError(f"Refusing to overwrite smoke result: {target}")
    controller = LMStudioController()
    master = controller.role("master").model
    worker = controller.role("worker").model
    result = {
        "created_at": datetime.now(timezone.utc).isoformat(), "comfyui_executed": False,
        "review_attempts": 1, "inventories": {},
    }
    exit_code = 1
    try:
        result["inventories"]["initial"] = loaded_models(controller)
        role = controller.begin_review(deep=False)
        during = loaded_models(controller)
        result["inventories"]["worker_loaded"] = during
        if during != [worker]:
            raise RuntimeError(f"VRAM exclusion failed before Worker review: {during}")

        cases_path = VISUAL_REVIEW_RUNS_ROOT / "worker_vision_v1_20260821_003" / "input_cases.json"
        cases = json.loads(cases_path.read_text(encoding="utf-8"))["cases"]
        case = next(item for item in cases if item["case_id"] == "tifa_camera_and_back_drift")
        review = review_image(
            resolve_legacy_path(case["klein_image"]),
            illustrious_image=resolve_legacy_path(case["illustrious_image"]),
            comparison_image=resolve_legacy_path(case["comparison_image"]),
            context=case["context"], model=role.model, base_url=controller.base_url, ttl_seconds=None,
        )
        result["worker_review"] = {"case_id": case["case_id"], "model": role.model, "review": review}
        result["tests"] = {
            "D_visual_reviewer": "pass",
            "E_vram_orchestration": "pass",
        }
        exit_code = 0
    except Exception as exc:
        result["tests"] = {
            "D_visual_reviewer": "fail",
            "E_vram_orchestration": "fail",
        }
        result["error"] = str(exc)
    finally:
        controller.unload_all()
        controller.wait_for_vram_release()
        controller.load("master")
        final = loaded_models(controller)
        result["inventories"]["final"] = final
        result["master_restored"] = final == [master]
        if not result["master_restored"]:
            result["tests"]["E_vram_orchestration"] = "fail"
            exit_code = 1
        with target.open("x", encoding="utf-8") as output:
            json.dump(result, output, ensure_ascii=False, indent=2)
            output.write("\n")
    print(json.dumps({"tests": result["tests"], "master_restored": result["master_restored"],
                      "final_loaded": result["inventories"]["final"],
                      "verdict": result.get("worker_review", {}).get("review", {}).get("verdict")}))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
