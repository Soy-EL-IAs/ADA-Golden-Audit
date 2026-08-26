#!/usr/bin/env python3
"""Versioned JSON contracts shared by ADA specialist-agent boundaries."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

if __package__:
    from .ada_paths import ADA_ROOT
else:
    from ada_paths import ADA_ROOT


SCHEMAS_ROOT = ADA_ROOT / "schemas"
CONTRACT_FILES = {
    "character_contract_v1": "character_contract_v1.schema.json",
    "resolved_render_spec_v1": "resolved_render_spec_v1.schema.json",
    "stage_render_plan_v1": "stage_render_plan_v1.schema.json",
    "prompt_artifact_v1": "prompt_artifact_v1.schema.json",
    "render_receipt_v1": "render_receipt_v1.schema.json",
    "review_observation_v1": "review_observation_v1.schema.json",
    "routing_decision_v1": "routing_decision_v1.schema.json",
    "comparative_review_v1": "comparative_review_v1.schema.json",
    "final_stage_decision_v1": "final_stage_decision_v1.schema.json",
    "render_receipt_v2": "render_receipt_v2.schema.json",
    "comparative_review_v2": "comparative_review_v2.schema.json",
    "final_renderer_decision_v2": "final_renderer_decision_v2.schema.json",
    "hook_premise_v2": "hook_premise_v2.schema.json",
    "resolved_render_spec_v2": "resolved_render_spec_v2.schema.json",
    "resolved_render_spec_v3": "resolved_render_spec_v3.schema.json",
    "resolved_render_spec_stock_v1": "resolved_render_spec_stock_v1.schema.json",
    "scene_template_spec_v1": "scene_template_spec_v1.schema.json",
    "reinterpreted_render_spec_v1": "reinterpreted_render_spec_v1.schema.json",
    "renderer_prompt_artifact_v1": "renderer_prompt_artifact_v1.schema.json",
    "human_stage_override_v1": "human_stage_override_v1.schema.json",
    "human_stage_review_v1": "human_stage_review_v1.schema.json",
    "premise_spec_v1": "premise_spec_v1.schema.json",
    "premise_output_v1": "premise_output_v1.schema.json",
    "illustrious_result_v1": "illustrious_result_v1.schema.json",
    "illustrious_output_v1": "illustrious_output_v1.schema.json",
    "visual_review_v1": "visual_review_v1.schema.json",
    "visual_review_v2": "visual_review_v2.schema.json",
    "visual_review_v3": "visual_review_v3.schema.json",
    "visual_review_v4": "visual_review_v4.schema.json",
    "review_observation_v2": "review_observation_v2.schema.json",
    "klein_result_v1": "klein_result_v1.schema.json",
    "klein_output_v1": "klein_output_v1.schema.json",
    "minimax_result_v1": "minimax_result_v1.schema.json",
    "minimax_output_v1": "minimax_output_v1.schema.json",
}


class ContractError(ValueError):
    """Raised when an artifact crosses an agent boundary with invalid structure."""


def validate_visual_review(value: Any) -> Any:
    """Accept current reviews and persisted v1 evidence without rewriting either."""
    try:
        return validate_contract("visual_review_v2", value)
    except ContractError:
        return validate_contract("visual_review_v1", value)


def load_contract(name: str) -> dict[str, Any]:
    try:
        filename = CONTRACT_FILES[name]
    except KeyError as exc:
        raise ContractError(f"Unknown ADA contract: {name}") from exc
    try:
        schema = json.loads((SCHEMAS_ROOT / filename).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"Unavailable or invalid ADA contract: {filename}") from exc
    if not isinstance(schema, dict):
        raise ContractError(f"ADA contract must be an object: {filename}")
    return schema


def validate_contract(name: str, value: Any) -> Any:
    """Validate the JSON-Schema subset used by ADA and return the same value."""
    _validate(value, load_contract(name), path=name)
    return value


def response_format(name: str) -> dict[str, Any]:
    """Build LM Studio's OpenAI-compatible strict structured-output wrapper."""
    return {
        "type": "json_schema",
        "json_schema": {"name": name, "strict": True, "schema": load_contract(name)},
    }


def _validate(value: Any, schema: dict[str, Any], *, path: str, root_schema: dict[str, Any] | None = None) -> None:
    root_schema = root_schema or schema
    reference = schema.get("$ref")
    if isinstance(reference, str) and reference.startswith("#/"):
        target: Any = root_schema
        for part in reference[2:].split("/"):
            if not isinstance(target, dict) or part not in target:
                raise ContractError(f"Unresolved schema reference at {path}: {reference}")
            target = target[part]
        if not isinstance(target, dict):
            raise ContractError(f"Invalid schema reference at {path}: {reference}")
        _validate(value, target, path=path, root_schema=root_schema)
        return
    expected_type = schema.get("type")
    if expected_type == "object":
        if not isinstance(value, dict):
            raise ContractError(f"{path} must be an object")
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        missing = [key for key in required if key not in value]
        if missing:
            raise ContractError(f"{path} is missing required fields: {', '.join(missing)}")
        if schema.get("additionalProperties") is False:
            extra = sorted(set(value) - set(properties))
            if extra:
                raise ContractError(f"{path} has unexpected fields: {', '.join(extra)}")
        for key, item in value.items():
            if key in properties:
                _validate(item, properties[key], path=f"{path}.{key}", root_schema=root_schema)
    elif expected_type == "array":
        if not isinstance(value, list):
            raise ContractError(f"{path} must be an array")
        minimum = schema.get("minItems")
        if isinstance(minimum, int) and len(value) < minimum:
            raise ContractError(f"{path} must contain at least {minimum} items")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                _validate(item, item_schema, path=f"{path}[{index}]", root_schema=root_schema)
    elif expected_type == "string":
        if not isinstance(value, str):
            raise ContractError(f"{path} must be a string")
        minimum = schema.get("minLength")
        if isinstance(minimum, int) and len(value.strip()) < minimum:
            raise ContractError(f"{path} must be non-empty")
    elif expected_type == "integer":
        if isinstance(value, bool) or not isinstance(value, int):
            raise ContractError(f"{path} must be an integer")
        if "minimum" in schema and value < schema["minimum"]:
            raise ContractError(f"{path} must be >= {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            raise ContractError(f"{path} must be <= {schema['maximum']}")
    elif expected_type == "number":
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ContractError(f"{path} must be a number")
        if "minimum" in schema and value < schema["minimum"]:
            raise ContractError(f"{path} must be >= {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            raise ContractError(f"{path} must be <= {schema['maximum']}")
    elif expected_type == "boolean":
        if not isinstance(value, bool):
            raise ContractError(f"{path} must be boolean")
    elif expected_type is not None:
        raise ContractError(f"Unsupported schema type at {path}: {expected_type}")

    enum = schema.get("enum")
    if isinstance(enum, list) and value not in enum:
        raise ContractError(f"{path} must be one of {enum}")
