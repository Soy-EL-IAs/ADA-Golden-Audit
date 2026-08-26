#!/usr/bin/env python3
"""Pixel-level Illustrious/Klein comparison, separate from stage PASS reviews."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

if __package__:
    from .agent_contracts import response_format, validate_contract
    from .visual_reviewer import _content_text, _native_content_text, _parse_json_object, _request, _save_diagnostic, image_data_url
else:
    from agent_contracts import response_format, validate_contract
    from visual_reviewer import _content_text, _native_content_text, _parse_json_object, _request, _save_diagnostic, image_data_url


class ComparativeReviewTransportError(RuntimeError):
    """No valid comparative review crossed the review boundary."""


def _prompt(
    *, concept_id: str, attempt: int, receipts: dict[str, dict[str, Any]],
    render_spec: dict[str, Any], observations: dict[str, dict[str, Any]],
) -> str:
    context = {
        "concept_id": concept_id,
        "attempt": attempt,
        "render_spec": render_spec,
        "stage_receipts": {
            stage: {"receipt_id": value.get("receipt_id", ""), "stage": value.get("stage", stage)}
            for stage, value in receipts.items()
        },
        "legacy_stage_observations": observations,
    }
    return (
        "Compare the two labeled images from the same ADA concept. This is a comparative review only, "
        "not a prompt and not an independent PASS/FAIL review. A stage PASS does not make that stage the winner. "
        "Inspect pixels and choose the stronger final asset relative to the Resolved Render Spec. Evaluate identity "
        "fidelity, anatomy/structure, face, outfit, composition preservation, scene/premise readability, visual "
        "polish, realism gain, unwanted drift, and overall preference. UNKNOWN or incomplete legacy observations "
        "must not block comparison. Distinguish a violated requirement from beneficial aesthetic deviation. "
        "Use HUMAN_REVIEW_REQUIRED only when pixels cannot support a responsible preference. Return only the exact "
        f"comparative_review_v1 JSON object. comparison_id must be 'comparative:{concept_id}:{attempt:02d}'. "
        "legacy_review_context_used must be true because the two existing Review Observations are supplied as secondary context. "
        "Do not repeat the render spec, observations, or instructions. Context: "
        + json.dumps(context, ensure_ascii=False, separators=(",", ":"))
    )


def review_stage_comparison(
    illustrious_image: Path, klein_image: Path, *, concept_id: str, attempt: int,
    receipts: dict[str, dict[str, Any]], render_spec: dict[str, Any],
    observations: dict[str, dict[str, Any]], model: str,
    base_url: str = "http://127.0.0.1:1234", diagnostic_dir: Path | None = None,
) -> dict[str, Any]:
    """Compare both stage outputs while keeping the two independent reviews intact."""
    for image in (illustrious_image, klein_image):
        if not image.is_file():
            raise FileNotFoundError(image)
    prompt = _prompt(
        concept_id=concept_id, attempt=attempt, receipts=receipts,
        render_spec=render_spec, observations=observations,
    )
    expected_stages = {
        "illustrious_receipt_id": receipts["illustrious"].get("receipt_id", ""),
        "klein_receipt_id": receipts["klein"].get("receipt_id", ""),
        "illustrious_observation_id": observations.get("illustrious", {}).get("observation_id", ""),
        "klein_observation_id": observations.get("klein", {}).get("observation_id", ""),
    }
    expected_comparison_id = f"comparative:{concept_id}:{attempt:02d}"
    if not all(expected_stages.values()):
        raise ValueError("Comparative review requires both receipt and observation ids")
    payload: dict[str, Any] = {
        "model": model,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": prompt + "\nIMAGE A — ILLUSTRIOUS:"},
            {"type": "image_url", "image_url": {"url": image_data_url(illustrious_image)}},
            {"type": "text", "text": "IMAGE B — KLEIN:"},
            {"type": "image_url", "image_url": {"url": image_data_url(klein_image)}},
        ]}],
        "temperature": 0,
        "max_tokens": 1400,
        "response_format": response_format("comparative_review_v1"),
    }
    if model != "qwen/qwen3-vl-8b":
        payload["reasoning"] = "off"
    errors: list[str] = []
    response = _request(f"{base_url.rstrip('/')}/v1/chat/completions", payload, timeout=600)
    _save_diagnostic(diagnostic_dir, "attempt_01_schema.json", response)
    try:
        value = _parse_json_object(_content_text(response))
        validate_contract("comparative_review_v1", value)
        if value["comparison_id"] != expected_comparison_id or value["concept_id"] != concept_id or value["attempt"] != attempt:
            raise ValueError("Comparative reviewer changed comparison identity")
        if value["stages"] != expected_stages:
            raise ValueError("Comparative reviewer changed receipt or observation lineage")
        if value["legacy_review_context_used"] is not True:
            raise ValueError("Comparative reviewer did not record its partial legacy observation dependency")
        return value
    except (ValueError, json.JSONDecodeError) as exc:
        errors.append(f"schema: {type(exc).__name__}: {exc}")

    native_payload = {
        "model": model,
        "input": [
            {"type": "text", "content": prompt + "\nThe next image is ILLUSTRIOUS."},
            {"type": "image", "data_url": image_data_url(illustrious_image)},
            {"type": "text", "content": "The next image is KLEIN. Return only contract JSON."},
            {"type": "image", "data_url": image_data_url(klein_image)},
        ],
        "temperature": 0,
        "max_output_tokens": 1400,
        "store": False,
    }
    native = _request(f"{base_url.rstrip('/')}/api/v1/chat", native_payload, timeout=600)
    _save_diagnostic(diagnostic_dir, "attempt_02_native.json", native)
    try:
        value = _parse_json_object(_native_content_text(native))
        validate_contract("comparative_review_v1", value)
        if value["comparison_id"] != expected_comparison_id or value["concept_id"] != concept_id or value["attempt"] != attempt:
            raise ValueError("Comparative reviewer changed comparison identity")
        if value["stages"] != expected_stages:
            raise ValueError("Comparative reviewer changed receipt or observation lineage")
        if value["legacy_review_context_used"] is not True:
            raise ValueError("Comparative reviewer did not record its partial legacy observation dependency")
        return value
    except (ValueError, json.JSONDecodeError) as exc:
        errors.append(f"native: {type(exc).__name__}: {exc}")
    raise ComparativeReviewTransportError("Comparative Review failed after controlled transports: " + " | ".join(errors))
