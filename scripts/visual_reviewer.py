#!/usr/bin/env python3
"""Small, strict JSON visual reviewer for a Klein result and optional source image."""

from __future__ import annotations

import base64
import json
import mimetypes
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

if __package__:
    from .ada_paths import LMSTUDIO_BASE_URL
else:
    from ada_paths import LMSTUDIO_BASE_URL


REQUIRED_KEYS = (
    "verdict", "identity", "anatomy", "single_subject", "visual_appeal",
    "viral_hook", "animation_potential", "identity_issues", "visual_issues", "reason",
)
SCORE_KEYS = ("identity", "anatomy", "visual_appeal", "viral_hook", "animation_potential")
VALID_VERDICTS = {"PASS", "REVIEW", "REJECT"}


class MasterReviewTransportError(RuntimeError):
    """The Master produced no contract-valid review after controlled transports."""
REVIEW_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "verdict": {"type": "string", "enum": ["PASS", "REVIEW", "REJECT"]},
        "identity": {"type": "integer", "minimum": 0, "maximum": 10},
        "anatomy": {"type": "integer", "minimum": 0, "maximum": 10},
        "single_subject": {"type": "boolean"},
        "visual_appeal": {"type": "integer", "minimum": 0, "maximum": 10},
        "viral_hook": {"type": "integer", "minimum": 0, "maximum": 10},
        "animation_potential": {"type": "integer", "minimum": 0, "maximum": 10},
        "identity_issues": {"type": "array", "items": {"type": "string"}},
        "visual_issues": {"type": "array", "items": {"type": "string"}},
        "reason": {"type": "string"},
    },
    "required": list(REQUIRED_KEYS),
}


def image_data_url(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def _request(url: str, payload: dict[str, Any], timeout: int = 300) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"LM Studio HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"LM Studio unavailable: {exc.reason}") from exc
    if not isinstance(result, dict):
        raise ValueError("LM Studio returned a non-object response")
    return result


def _review_prompt(context: dict[str, Any], has_source: bool, has_comparison: bool) -> str:
    details = {key: value for key, value in context.items() if value not in (None, "", [], {})}
    source_instruction = (
        "Image 1 is a side-by-side pair: Illustrious source is left and final Klein result is right. "
        "Evaluate subjects within each half; the expected source/final pair is not a duplicate."
        if has_comparison else
        "Image 1 is the final Klein result. Image 2 is the Illustrious source for continuity comparison."
        if has_source else "Image 1 is the final Klein result; no source image is available."
    )
    return (
        "You are a conservative visual QA reviewer for one fictional adult character image. "
        f"{source_instruction} Inspect pixels first and use the supplied record context only to resolve identity/outfit. "
        "Detect duplicate subjects or more than one woman when one subject is expected; wrong character, hair, outfit "
        "or canonical accessory; broken anatomy/hands/limbs; serious Klein-vs-source drift; and critical occlusion "
        "contradictions such as visible eyes through a required blindfold. Also assess visual appeal, scroll-stopping "
        "impact, and suitability as a first frame/reference for character video. These three are subjective heuristic "
        "scores, not measurements. Do not infer defects that are not visible. Return ONLY one JSON object, with exactly "
        "these keys: verdict, identity, anatomy, single_subject, visual_appeal, viral_hook, animation_potential, "
        "identity_issues, visual_issues, reason. verdict is PASS, REVIEW, or REJECT. Each numeric score is an integer "
        "from 0 to 10. single_subject is boolean. Issues are short string arrays. reason is brief. "
        f"Record context: {json.dumps(details, ensure_ascii=False, separators=(',', ':'))}"
    )


def _content_text(response: dict[str, Any]) -> str:
    try:
        text = response["choices"][0]["message"].get("content", "")
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError(f"LM Studio response has no chat content: {response}") from exc
    if not isinstance(text, str):
        raise ValueError("LM Studio response content is not text")
    text = text.strip()
    if text.startswith("```"):
        text = text[3:]
        if text.lstrip().startswith("json"):
            text = text.lstrip()[4:]
        text = text.strip().removesuffix("```").strip()
    return text


def _native_content_text(response: dict[str, Any]) -> str:
    """Extract the first text message from LM Studio's native REST response."""
    for item in response.get("output", []):
        if isinstance(item, dict) and item.get("type") == "message":
            text = item.get("content", "")
            if isinstance(text, str) and text.strip():
                return text.strip()
    return ""


def _parse_json_object(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped[3:].lstrip()
        if stripped.startswith("json"):
            stripped = stripped[4:].lstrip()
        stripped = stripped.removesuffix("```").strip()
    start = stripped.find("{")
    if start < 0:
        raise ValueError("review response contains no JSON object")
    value, _ = json.JSONDecoder().raw_decode(stripped[start:])
    if not isinstance(value, dict):
        raise ValueError("review response JSON must be an object")
    return value


def _save_diagnostic(directory: Path | None, name: str, value: Any) -> None:
    if directory is None:
        return
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / name
    if path.exists():
        raise FileExistsError(f"Review diagnostic already exists: {path}")
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_review(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != set(REQUIRED_KEYS):
        raise ValueError(f"review JSON must contain exactly {list(REQUIRED_KEYS)}")
    verdict = value["verdict"]
    if not isinstance(verdict, str) or verdict.upper() not in VALID_VERDICTS:
        raise ValueError("review verdict must be PASS, REVIEW or REJECT")
    result: dict[str, Any] = {"verdict": verdict.upper()}
    for key in SCORE_KEYS:
        score = value[key]
        if isinstance(score, bool) or not isinstance(score, int) or not 0 <= score <= 10:
            raise ValueError(f"review {key} must be an integer from 0 to 10")
        result[key] = score
    if not isinstance(value["single_subject"], bool):
        raise ValueError("review single_subject must be boolean")
    result["single_subject"] = value["single_subject"]
    for key in ("identity_issues", "visual_issues"):
        issues = value[key]
        if not isinstance(issues, list) or not all(isinstance(item, str) and item.strip() for item in issues):
            raise ValueError(f"review {key} must be an array of non-empty strings")
        result[key] = issues
    if not isinstance(value["reason"], str) or not value["reason"].strip() or len(value["reason"]) > 600:
        raise ValueError("review reason must be brief non-empty text")
    result["reason"] = value["reason"].strip()
    return result


def review_image(
    klein_image: Path,
    *,
    model: str,
    base_url: str = LMSTUDIO_BASE_URL,
    illustrious_image: Path | None = None,
    comparison_image: Path | None = None,
    context: dict[str, Any] | None = None,
    ttl_seconds: int | None = None,
) -> dict[str, Any]:
    """Review one existing output. Does not load models, render, retry, or write files."""
    if not klein_image.is_file():
        raise FileNotFoundError(klein_image)
    if illustrious_image is not None and not illustrious_image.is_file():
        raise FileNotFoundError(illustrious_image)
    if comparison_image is not None and not comparison_image.is_file():
        raise FileNotFoundError(comparison_image)
    review_image_path = comparison_image or klein_image
    content: list[dict[str, Any]] = [
        {"type": "text", "text": _review_prompt(context or {}, illustrious_image is not None, comparison_image is not None)},
        {"type": "image_url", "image_url": {"url": image_data_url(review_image_path)}},
    ]
    if illustrious_image is not None and comparison_image is None:
        content.append({"type": "image_url", "image_url": {"url": image_data_url(illustrious_image)}})
    payload: dict[str, Any] = {
        "model": model,
        "messages": [{"role": "user", "content": content}],
        "temperature": 0,
        "max_tokens": 400,
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": "visual_review", "strict": True, "schema": REVIEW_SCHEMA},
        },
    }
    if ttl_seconds is not None:
        payload["ttl"] = ttl_seconds
    started = time.perf_counter()
    response = _request(f"{base_url.rstrip('/')}/v1/chat/completions", payload)
    review = validate_review(json.loads(_content_text(response)))
    review["elapsed_seconds"] = round(time.perf_counter() - started, 3)
    return review


def review_master_image(
    klein_image: Path,
    *,
    model: str,
    base_url: str = LMSTUDIO_BASE_URL,
    illustrious_image: Path | None = None,
    comparison_image: Path | None = None,
    context: dict[str, Any] | None = None,
    ttl_seconds: int | None = None,
    diagnostic_dir: Path | None = None,
) -> dict[str, Any]:
    """Master-only review with native-first transport and one schema fallback.

    The native API honors ``reasoning=off`` for this model. If it returns empty
    or invalid content, one OpenAI-compatible strict-schema attempt is allowed.
    Both raw responses can be persisted. Failure remains a hard boundary.
    """
    if model != "qwen3.8-27b-uncensored":
        raise ValueError("review_master_image is only for qwen3.8-27b-uncensored")
    if not klein_image.is_file():
        raise FileNotFoundError(klein_image)
    if illustrious_image is not None and not illustrious_image.is_file():
        raise FileNotFoundError(illustrious_image)
    if comparison_image is not None and not comparison_image.is_file():
        raise FileNotFoundError(comparison_image)
    review_image_path = comparison_image or klein_image
    prompt = _review_prompt(context or {}, illustrious_image is not None, comparison_image is not None)
    content: list[dict[str, Any]] = [
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": image_data_url(review_image_path)}},
    ]
    if illustrious_image is not None and comparison_image is None:
        content.append({"type": "image_url", "image_url": {"url": image_data_url(illustrious_image)}})
    started = time.perf_counter()
    strict_prompt = prompt + " Return ONLY the JSON object now; do not provide analysis or reasoning text."
    native_input: list[dict[str, Any]] = [{"type": "text", "content": strict_prompt}]
    for item in content[1:]:
        native_input.append({"type": "image", "data_url": item["image_url"]["url"]})
    native_payload: dict[str, Any] = {
        "model": model, "input": native_input, "temperature": 0,
        "max_output_tokens": 1000, "reasoning": "off", "store": False,
    }
    if ttl_seconds is not None:
        native_payload["ttl"] = ttl_seconds
    native_response = _request(f"{base_url.rstrip('/')}/api/v1/chat", native_payload, timeout=600)
    _save_diagnostic(diagnostic_dir, "attempt_01_native.json", native_response)
    errors: list[str] = []
    try:
        review = validate_review(_parse_json_object(_native_content_text(native_response)))
        review["elapsed_seconds"] = round(time.perf_counter() - started, 3)
        review["master_fallback_used"] = False
        review["master_transport"] = "native_reasoning_off"
        return review
    except (ValueError, json.JSONDecodeError) as exc:
        errors.append(f"native: {type(exc).__name__}: {exc}")

    fallback_content = list(content)
    fallback_content[0] = {"type": "text", "text": strict_prompt}
    schema_payload: dict[str, Any] = {
        "model": model, "messages": [{"role": "user", "content": fallback_content}],
        "temperature": 0, "max_tokens": 1600, "reasoning": "off",
        "response_format": {"type": "json_schema", "json_schema": {
            "name": "visual_review", "strict": True, "schema": REVIEW_SCHEMA,
        }},
    }
    if ttl_seconds is not None:
        schema_payload["ttl"] = ttl_seconds
    schema_response = _request(f"{base_url.rstrip('/')}/v1/chat/completions", schema_payload, timeout=600)
    _save_diagnostic(diagnostic_dir, "attempt_02_schema.json", schema_response)
    try:
        review = validate_review(_parse_json_object(_content_text(schema_response)))
        review["elapsed_seconds"] = round(time.perf_counter() - started, 3)
        review["master_fallback_used"] = True
        review["master_transport"] = "openai_strict_schema"
        return review
    except (ValueError, json.JSONDecodeError) as exc:
        errors.append(f"schema: {type(exc).__name__}: {exc}")
    raise MasterReviewTransportError("Master visual review failed hard after controlled transports: " + " | ".join(errors))
