#!/usr/bin/env python3
"""Capture one unparsed Master Visual Review response for transport diagnosis."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

if __package__:
    from .ada_paths import VISUAL_REVIEW_RUNS_ROOT, resolve_legacy_path
    from .lmstudio_controller import LMStudioController
    from .visual_reviewer import REVIEW_SCHEMA, _content_text, _native_content_text, _request, _review_prompt, image_data_url, validate_review
else:
    from ada_paths import VISUAL_REVIEW_RUNS_ROOT, resolve_legacy_path
    from lmstudio_controller import LMStudioController
    from visual_reviewer import REVIEW_SCHEMA, _content_text, _native_content_text, _request, _review_prompt, image_data_url, validate_review


DEFAULT_CASES = VISUAL_REVIEW_RUNS_ROOT / "worker_vision_v1_20260821_003" / "input_cases.json"
DEFAULT_OUTPUT = VISUAL_REVIEW_RUNS_ROOT / "master_jsonschema_diagnostic_tifa_camera_002"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    source = json.loads(args.cases.read_text(encoding="utf-8"))
    case = next(item for item in source["cases"] if item["case_id"] == "tifa_camera_and_back_drift")
    case["comparison_image"] = str(resolve_legacy_path(case["comparison_image"]))
    controller = LMStudioController()
    inventory = controller.list_models()
    loaded_models = [item.get("model") for item in inventory["loaded"]]
    if controller.role("worker").model in loaded_models:
        controller.unload_role("worker")
        controller.wait_for_vram_release()
    if controller.role("master").model not in loaded_models:
        controller.load("master")

    payload = {
        "model": controller.role("master").model,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": _review_prompt(case["context"], True, True)},
            {"type": "image_url", "image_url": {"url": image_data_url(Path(case["comparison_image"]))}},
        ]}],
        "temperature": 0,
        "max_tokens": 400,
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": "visual_review", "strict": True, "schema": REVIEW_SCHEMA},
        },
    }
    started = time.perf_counter()
    response = _request(f"{controller.base_url}/v1/chat/completions", payload, timeout=600)
    elapsed = round(time.perf_counter() - started, 3)
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / "raw_response.json").write_text(json.dumps(response, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    message = response.get("choices", [{}])[0].get("message", {}) if isinstance(response.get("choices"), list) else {}
    summary = {
        "case_id": case["case_id"], "model": controller.role("master").model, "elapsed_seconds": elapsed,
        "choices_count": len(response.get("choices", [])) if isinstance(response.get("choices"), list) else None,
        "finish_reasons": [item.get("finish_reason") for item in response.get("choices", []) if isinstance(item, dict)],
        "message": message,
        "content": message.get("content") if isinstance(message, dict) else None,
        "reasoning": message.get("reasoning") if isinstance(message, dict) else None,
        "reasoning_content": message.get("reasoning_content") if isinstance(message, dict) else None,
        "tool_calls": message.get("tool_calls") if isinstance(message, dict) else None,
        "usage": response.get("usage"),
    }
    fallback_response = None
    fallback_review = None
    if not summary["content"]:
        fallback_payload = {
            "model": payload["model"],
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": _review_prompt(case["context"], True, True) +
                 " Return ONLY the JSON object now; do not provide analysis or reasoning text."},
                {"type": "image_url", "image_url": {"url": image_data_url(Path(case["comparison_image"]))}},
            ]}],
            "temperature": 0, "max_tokens": 1200, "reasoning": "off",
            "response_format": {"type": "text"},
        }
        native_payload = {
            "model": payload["model"],
            "input": [
                {"type": "text", "content": fallback_payload["messages"][0]["content"][0]["text"]},
                {"type": "image", "data_url": fallback_payload["messages"][0]["content"][1]["image_url"]["url"]},
            ],
            "temperature": 0, "max_output_tokens": 400, "reasoning": "off", "store": False,
        }
        fallback_response = _request(f"{controller.base_url}/api/v1/chat", native_payload, timeout=600)
        (args.output / "fallback_raw_response.json").write_text(
            json.dumps(fallback_response, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        fallback_review = validate_review(json.loads(_native_content_text(fallback_response)))
        (args.output / "review.json").write_text(
            json.dumps(fallback_review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary["fallback_used"] = fallback_response is not None
    summary["fallback_finish_reasons"] = [item.get("finish_reason") for item in fallback_response.get("choices", [])
                                           if isinstance(item, dict)] if fallback_response else None
    summary["fallback_message"] = next((item for item in fallback_response.get("output", [])
                                         if item.get("type") == "message"), None) if fallback_response else None
    summary["fallback_content"] = _native_content_text(fallback_response) if fallback_response else None
    summary["parsed_review"] = fallback_review
    (args.output / "diagnostic_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output.resolve()), **{key: summary[key] for key in ("elapsed_seconds", "finish_reasons", "content", "reasoning_content", "fallback_used", "fallback_finish_reasons", "fallback_content", "parsed_review")}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
