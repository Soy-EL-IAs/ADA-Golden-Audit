#!/usr/bin/env python3
"""Split the quarantined legacy combined graph for migration tests only."""

from __future__ import annotations

from typing import Any, Iterable


def dependency_closure(prompt: dict[str, dict[str, Any]], outputs: Iterable[str]) -> set[str]:
    """Return output nodes and every upstream node referenced by their inputs."""
    needed: set[str] = set()
    pending = [str(item) for item in outputs]
    while pending:
        node_id = pending.pop()
        if node_id in needed:
            continue
        if node_id not in prompt:
            raise ValueError(f"Workflow references missing node {node_id}")
        needed.add(node_id)
        for value in prompt[node_id].get("inputs", {}).values():
            if isinstance(value, list) and len(value) == 2 and isinstance(value[0], str) and value[0] in prompt:
                pending.append(value[0])
    return needed


def prune_to_outputs(prompt: dict[str, dict[str, Any]], outputs: Iterable[str]) -> dict[str, dict[str, Any]]:
    needed = dependency_closure(prompt, outputs)
    return {node_id: node for node_id, node in prompt.items() if node_id in needed}


def compile_illustrious_stage(prompt: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Keep only the Illustrious SaveImage branch (node 7 and dependencies)."""
    return prune_to_outputs(prompt, ("7",))


def compile_klein_stage(
    prompt: dict[str, dict[str, Any]], *, uploaded_image: str, load_node_id: str = "900",
) -> dict[str, dict[str, Any]]:
    """Replace the in-memory Illustrious dependency with a persisted ComfyUI input image."""
    if load_node_id in prompt:
        raise ValueError(f"Reserved LoadImage node already exists: {load_node_id}")
    if "13" not in prompt or "40" not in prompt:
        raise ValueError("Reusable workflow is missing source-image consumers 13 and 40")
    stage = {node_id: {**node, "inputs": dict(node.get("inputs", {}))} for node_id, node in prompt.items()}
    stage[load_node_id] = {
        "class_type": "LoadImage",
        "inputs": {"image": uploaded_image},
        "_meta": {"title": "ADA persisted Illustrious source"},
    }
    stage["13"]["inputs"]["image"] = [load_node_id, 0]
    stage["40"]["inputs"]["pixels"] = [load_node_id, 0]
    return prune_to_outputs(stage, ("20",))


def validate_stage_separation(
    illustrious: dict[str, dict[str, Any]], klein: dict[str, dict[str, Any]], *, load_node_id: str = "900",
) -> None:
    if "7" not in illustrious or "20" in illustrious or "22" in illustrious:
        raise ValueError("Illustrious stage contains invalid output nodes")
    if "20" not in klein or "22" in klein or load_node_id not in klein:
        raise ValueError("Klein stage is missing final outputs or persisted source")
    if any(node_id in klein for node_id in ("1", "2", "3", "4", "5", "6", "7", "8")):
        raise ValueError("Klein stage still depends on the Illustrious generation branch")
    if klein["40"]["inputs"].get("pixels") != [load_node_id, 0]:
        raise ValueError("Klein latent does not use the persisted Illustrious image")
