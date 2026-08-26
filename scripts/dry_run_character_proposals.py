#!/usr/bin/env python3
"""Generate exactly 20 premise proposals locally without staging or ComfyUI."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

if __package__:
    from .ada_paths import ADA_ROOT, LMSTUDIO_BASE_URL, PREMISES_ROOT
    from .character_dataset import CharacterDatasetBuilder
    from .lmstudio_controller import LMStudioController
    from .prompt_guides import PromptGuideLibrary
else:
    from ada_paths import ADA_ROOT, LMSTUDIO_BASE_URL, PREMISES_ROOT
    from character_dataset import CharacterDatasetBuilder
    from lmstudio_controller import LMStudioController
    from prompt_guides import PromptGuideLibrary


def request_json(url: str, payload: dict[str, Any], timeout: int = 300) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            value = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"LM Studio proposal request failed: {exc}") from exc
    if not isinstance(value, dict):
        raise RuntimeError("LM Studio returned a non-object response")
    return value


def parse_proposals(
    content: str,
    expected_count: int,
    expected_distribution: dict[str, int],
) -> list[dict[str, Any]]:
    try:
        proposals = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError("Master response is not a JSON array") from exc
    if not isinstance(proposals, list) or len(proposals) != expected_count:
        raise ValueError(f"Master must return exactly {expected_count} proposals")
    required = {"id", "category", "premise"}
    ids: set[str] = set()
    actual_distribution = {category: 0 for category in expected_distribution}
    for number, proposal in enumerate(proposals, 1):
        if not isinstance(proposal, dict) or set(proposal) != required:
            raise ValueError(f"proposal {number} must contain only id, category and premise")
        if not all(isinstance(proposal[key], str) and proposal[key].strip() for key in required):
            raise ValueError(f"proposal {number} fields must be non-empty text")
        if proposal["id"] in ids:
            raise ValueError(f"proposal {number} repeats id {proposal['id']!r}")
        if proposal["category"] not in actual_distribution:
            raise ValueError(f"proposal {number} has an unplanned category")
        ids.add(proposal["id"])
        actual_distribution[proposal["category"]] += 1
    if actual_distribution != expected_distribution:
        raise ValueError(f"proposal category distribution must be {expected_distribution}, got {actual_distribution}")
    return proposals


def proposal_generation_brief(full_brief: dict[str, Any], category_plan: list[str]) -> dict[str, Any]:
    """Keep the dry-run premise call to Viral guidance and its requested categories."""
    viral_guides = [
        guide for guide in full_brief["proposal_guidance"]["guides"]
        if guide.get("name") == "viral_premise"
    ]
    if len(viral_guides) != 1:
        raise ValueError("The proposal phase requires exactly one active Viral guide")
    distribution = {category: category_plan.count(category) for category in full_brief["distribution"]}
    return {
        "character": full_brief["character"],
        "version": full_brief["version"],
        "count": len(category_plan),
        "categories_plan": category_plan,
        "distribution": distribution,
        "character_profile_used": full_brief["character_profile_used"],
        "character_profile": full_brief["character_profile"],
        "category_rules": [
            "Use each requested category exactly the prescribed number of times.",
            "Vary situations, actions, expressions, viewpoints and visual hooks across proposals.",
            "Describe composition with viewpoint and framing only; never use physical camera or lens language.",
        ],
        "proposal_guidance": {"phase": "proposal", "guides": viral_guides},
        "prompt_guide_manifest": full_brief["prompt_guide_manifest"],
    }


def proposal_request_payload(
    model: str,
    brief: dict[str, Any],
    batch_number: int,
) -> dict[str, Any]:
    count = int(brief["count"])
    instruction = (
        "Generate premise proposals only. Do not call tools, do not create prompts, do not stage a dataset, and do not render. "
        f"This is batch {batch_number} of 4. Return one JSON array with exactly {count} objects and no markdown. "
        "Each object must contain only id, category and premise. Use the prescribed category distribution exactly. "
        "Use the local character profile only as identity facts, and use proposal_guidance. "
        f"Prefix every id with b{batch_number:02d}_ so IDs remain unique across the final 20-proposal set.\n\n"
        + json.dumps(brief, ensure_ascii=False)
    )
    return {
        "model": model,
        "input": [{"type": "text", "content": instruction}],
        "temperature": 0.7,
        "max_output_tokens": 1600,
        "reasoning": "off",
        "store": False,
    }


def native_content(response: dict[str, Any]) -> str:
    """Extract only the final text from LM Studio's native reasoning-off endpoint."""
    for item in response.get("output", []):
        if isinstance(item, dict) and item.get("type") == "message":
            content = item.get("content", "")
            if isinstance(content, str):
                return content
    raise RuntimeError("LM Studio native response did not contain message content")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--character", default="2B")
    parser.add_argument("--version", default="NieR:Automata")
    parser.add_argument("--output", type=Path, default=PREMISES_ROOT / "dry_run_2b_nier_automata_20.json")
    parser.add_argument("--viral-guide", type=Path, help="Use one isolated Viral guide for this dry run only")
    parser.add_argument("--model", default=os.environ.get("LM_STUDIO_MODEL", LMStudioController().role("master").model))
    args = parser.parse_args()

    count = 20
    batches = 4
    batch_size = count // batches
    viral_guide = args.viral_guide.resolve() if args.viral_guide else None
    if viral_guide is not None and not viral_guide.is_file():
        raise FileNotFoundError(f"Viral guide is unavailable: {viral_guide}")
    guide_library = PromptGuideLibrary(viral_override=viral_guide) if viral_guide else PromptGuideLibrary()
    full_brief = CharacterDatasetBuilder(prompt_guides=guide_library).proposal_brief(args.character, args.version, count)
    output = args.output if args.output.is_absolute() else ADA_ROOT / args.output
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise FileExistsError(f"Dry-run output already exists and will not be overwritten: {output}")
    attempt = 1
    while any(
        output.with_name(f"{output.stem}_raw_batch_{number:02d}_attempt_{attempt:02d}.json").exists()
        for number in range(1, batches + 1)
    ):
        attempt += 1
    raw_paths = [
        output.with_name(f"{output.stem}_raw_batch_{number:02d}_attempt_{attempt:02d}.json")
        for number in range(1, batches + 1)
    ]

    collected: list[dict[str, Any]] = []
    batch_details: list[dict[str, Any]] = []
    category_plan = list(full_brief["categories_plan"])
    for index in range(batches):
        batch_number = index + 1
        batch_plan = category_plan[index * batch_size:(index + 1) * batch_size]
        brief = proposal_generation_brief(full_brief, batch_plan)
        response = request_json(
            f"{LMSTUDIO_BASE_URL}/api/v1/chat",
            proposal_request_payload(args.model, brief, batch_number),
        )
        raw_path = raw_paths[index]
        raw_path.write_text(json.dumps(response, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        content = native_content(response)
        batch_proposals = parse_proposals(str(content), batch_size, brief["distribution"])
        collected.extend(batch_proposals)
        batch_details.append({
            "batch": batch_number,
            "categories_plan": batch_plan,
            "raw_response": str(raw_path),
            "count": len(batch_proposals),
        })

    proposals = parse_proposals(json.dumps(collected, ensure_ascii=False), count, full_brief["distribution"])
    output.write_text(
        json.dumps({
            "dry_run": True,
            "comfyui_executed": False,
            "brief": proposal_generation_brief(full_brief, category_plan),
            "batches": batch_details,
            "proposals": proposals,
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": "valid", "count": len(proposals), "batches": batches,
        "comfyui_executed": False, "output": str(output), "raw_responses": [str(path) for path in raw_paths],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"dry-run failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1)
