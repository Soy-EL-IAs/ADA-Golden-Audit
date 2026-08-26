#!/usr/bin/env python3
"""MCP tools that expose the local Illustrious -> Klein pipeline to LM Studio."""

from __future__ import annotations

import contextlib
import sys
from typing import Any

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.utilities.types import Image

if __package__:
    from .lmstudio_operator import (
        image_path,
        manifest_path,
        tool_batch_status,
        tool_append_character_dataset_entries,
        tool_build_gallery,
        tool_cache_character_refs,
        tool_get_character_profile,
        tool_generate_character_dataset,
        tool_get_character_dataset_prompt_guidance,
        tool_comfy_status,
        tool_find_character_refs,
        tool_load_master,
        tool_load_worker,
        tool_orchestration_status,
        tool_finalize_character_dataset,
        tool_persist_character_dataset,
        tool_review_batch,
        tool_run_batch,
        tool_search_images,
        tool_search_web,
        tool_unload_all_llms,
        tool_unload_master,
        tool_unload_worker,
    )
else:
    from lmstudio_operator import (
        image_path,
        manifest_path,
        tool_batch_status,
        tool_append_character_dataset_entries,
        tool_build_gallery,
        tool_cache_character_refs,
        tool_get_character_profile,
        tool_generate_character_dataset,
        tool_get_character_dataset_prompt_guidance,
        tool_comfy_status,
        tool_find_character_refs,
        tool_load_master,
        tool_load_worker,
        tool_orchestration_status,
        tool_finalize_character_dataset,
        tool_persist_character_dataset,
        tool_review_batch,
        tool_run_batch,
        tool_search_images,
        tool_search_web,
        tool_unload_all_llms,
        tool_unload_master,
        tool_unload_worker,
    )


server = MCPServer(
    name="illustrious-klein-local",
    title="Illustrious → Klein Local",
    description="Safe local tools for the reusable ComfyUI Illustrious to Klein pipeline.",
    instructions=(
        "Speak Spanish. Always check comfy_status before rendering. Characters are JSONL data, not workflows. "
        "Never modify prompts, seeds, models, LoRAs, VAE, sampler, guidance, connections or workflow files. "
        "For future prompts express composition only as viewpoint and framing; never name physical camera, lens, photographer or filming equipment to indicate angle or crop. "
        "Use find_character_refs for curated reference candidates; do not ask the LLM to mechanically filter raw image results. "
        "When find_character_refs returns filtered and scored references, summarize them directly without prolonged reasoning or re-ranking. "
        "Use cache_character_refs only when the user explicitly asks to persist references; never retry a failed download automatically. "
        "generate_character_dataset provides a local booru-characters profile when there is an unequivocal match; "
        "treat its characteristics and clothing as identity facts without mechanically pasting tags into prompts. "
        "Do not call get_character_profile again after generate_character_dataset unless the user explicitly asks to inspect or debug the profile. "
        "For a new character dataset, call generate_character_dataset first and use its proposal_guidance for premises. "
        "Then call get_character_dataset_prompt_guidance before writing Illustrious and Klein prompts; append 5-10 entries at a time "
        "with append_character_dataset_entries, then call finalize_character_dataset. These tools do not render or search. "
        "For a new dataset run a small pilot JSONL, review every result, and only then run a larger approved dataset. "
        "Never retry a failed render automatically. With PIPELINE_ORCHESTRATION=1, run_batch unloads all LLMs and "
        "verifies VRAM release plus ComfyUI idle before rendering; no LLM inference is allowed while it waits/renders."
    ),
)


@server.tool(description="Check whether local ComfyUI is idle. This does not generate or modify anything.")
def comfy_status() -> dict[str, Any]:
    return tool_comfy_status()


@server.tool(description="Search the web with opt-in local SearXNG. Returns metadata and URLs only; downloads nothing.")
def search_web(query: str, limit: int = 10) -> dict[str, Any]:
    return tool_search_web(query, limit)


@server.tool(description="Search images with opt-in local SearXNG. Returns page/image/thumbnail URLs and metadata; downloads and renders nothing.")
def search_images(query: str, limit: int = 10) -> dict[str, Any]:
    return tool_search_images(query, limit)


@server.tool(description="Two-stage deterministic character-reference selection using trusted pages first and at most one image-search fallback. Mechanical scoring only; downloads no images.")
def find_character_refs(character: str, version: str | None = None, limit: int = 6) -> dict[str, Any]:
    return tool_find_character_refs(character, version, limit)


@server.tool(description="Find and cache 2-5 character references once. Reuses a valid cache, never overwrites existing content and performs no automatic retries.")
def cache_character_refs(
    character: str,
    version: str | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    return tool_cache_character_refs(character, version, limit)


@server.tool(description="Inspection/debug only: read the local booru-characters identity profile. generate_character_dataset already returns this profile during normal dataset creation. Returns only source tags, relationships and conservative candidates; it does not search, download or render.")
def get_character_profile(character: str, version: str | None = None) -> dict[str, Any]:
    return tool_get_character_profile(character, version)


@server.tool(
    description=(
        "Phase 1 of Master-authored dataset creation. Create a new empty staging plan with distribution, prompt rules, "
        "safe target paths, usable local-reference context and any available local character_profile. Use its returned profile directly, then append entries. Performs no search or rendering."
    )
)
def generate_character_dataset(
    character: str,
    version: str | None = None,
    count: int = 20,
    dataset_id: str | None = None,
    categories: list[str] | None = None,
) -> dict[str, Any]:
    return tool_generate_character_dataset(character, version, count, dataset_id, categories)


@server.tool(description="After premises are selected for an active dataset staging plan, return only the versioned Illustrious and Klein prompt guides. It does not write, render, search or download.")
def get_character_dataset_prompt_guidance(dataset_id: str) -> dict[str, Any]:
    return tool_get_character_dataset_prompt_guidance(dataset_id)


@server.tool(
    description=(
        "Append 1-10 Master-authored entries to an existing character-dataset staging plan. Checks basic structure "
        "and duplicate IDs/seeds against prior chunks. It does not render or create final outputs."
    )
)
def append_character_dataset_entries(
    dataset_id: str,
    entries: list[dict[str, Any]],
) -> dict[str, Any]:
    return tool_append_character_dataset_entries(dataset_id, entries)


@server.tool(
    description=(
        "Validate all staged chunks and, only when the complete dataset is valid, write its JSONL and Klein preset "
        "plan. On failure, staging remains unchanged for targeted correction. It never renders."
    )
)
def finalize_character_dataset(
    character: str,
    count: int,
    dataset_id: str,
    version: str | None = None,
) -> dict[str, Any]:
    return tool_finalize_character_dataset(character, count, dataset_id, version)


@server.tool(
    description=(
        "Phase 2 of Master-authored dataset creation. Validate and save the complete creative entries as a new "
        "JSONL and Klein preset plan. Never overwrites, searches, downloads or renders."
    )
)
def persist_character_dataset(
    character: str,
    count: int,
    dataset_id: str,
    entries: list[dict[str, Any]],
    version: str | None = None,
) -> dict[str, Any]:
    return tool_persist_character_dataset(character, count, dataset_id, entries, version)


@server.tool(description="Read the manifest and progress of a Klein batch without generating anything.")
def batch_status(batch_id: str) -> dict[str, Any]:
    return tool_batch_status(batch_id)


@server.tool(description="Read Master/Worker state and LM Studio model inventory without changing anything.")
def orchestration_status() -> dict[str, Any]:
    return tool_orchestration_status()


@server.tool(description="Load the configured Master using LM Studio v1. Do not use during a batch wait or generation.")
def load_master() -> dict[str, Any]:
    return tool_load_master()


@server.tool(description="Unload configured Master instances using LM Studio v1.")
def unload_master() -> dict[str, Any]:
    return tool_unload_master()


@server.tool(description="Load the configured Vision Worker using LM Studio v1. Do not use during a batch wait or generation.")
def load_worker() -> dict[str, Any]:
    return tool_load_worker()


@server.tool(description="Unload configured Vision Worker instances using LM Studio v1.")
def unload_worker() -> dict[str, Any]:
    return tool_unload_worker()


@server.tool(description="Unload every reported LLM and wait for deterministic VRAM-release confirmation. Does not launch ComfyUI.")
def unload_all_llms() -> dict[str, Any]:
    return tool_unload_all_llms()


@server.tool(
    description=(
        "Validate and run every record in one JSONL dataset under prompts/. The count comes from the file. "
        "It blocks locally until completion without consuming model inference tokens, never overwrites a batch, "
        "and never retries automatically. klein_preset_plan is optional and must name a JSON plan under config/."
    )
)
def run_batch(dataset: str, batch_id: str, klein_preset_plan: str | None = None) -> dict[str, Any]:
    # The runner prints progress; redirect it away from stdout because stdout is the MCP protocol channel.
    with contextlib.redirect_stdout(sys.stderr):
        return tool_run_batch(dataset, batch_id, klein_preset_plan)


@server.tool(description="Review completed side-by-side comparisons with the loaded LM Studio vision model and write review.json.")
def review_batch(batch_id: str, limit: int) -> dict[str, Any]:
    with contextlib.redirect_stdout(sys.stderr):
        return tool_review_batch(batch_id, limit)


@server.tool(description="Use the configured Master for a deeper second opinion. With orchestration enabled: Worker unload -> VRAM release -> Master load.")
def deep_review_batch(batch_id: str, limit: int) -> dict[str, Any]:
    with contextlib.redirect_stdout(sys.stderr):
        return tool_review_batch(batch_id, limit, deep=True)


@server.tool(description="Create a local HTML gallery for completed comparisons in a Klein batch.")
def build_gallery(batch_id: str) -> dict[str, Any]:
    return tool_build_gallery(batch_id)


@server.tool(
    description=(
        "Display up to 6 completed comparison images directly inside LM Studio chat. "
        "Use build_gallery for larger batches."
    )
)
def show_comparisons(batch_id: str, limit: int = 3) -> list[Any]:
    if limit < 1 or limit > 6:
        raise ValueError("limit must be between 1 and 6")
    path = manifest_path(batch_id)
    if not path.exists():
        raise FileNotFoundError(path)
    import json

    manifest = json.loads(path.read_text(encoding="utf-8"))
    images: list[Image] = []
    for record in manifest.get("records", []):
        if len(images) >= limit:
            break
        if record.get("status") == "complete" and record.get("compare"):
            images.append(Image(path=image_path(record["compare"][0])))
    if not images:
        raise ValueError("The batch has no completed comparison images")
    return images


if __name__ == "__main__":
    server.run(transport="stdio")
