#!/usr/bin/env python3
"""Standalone, local-only overnight evolution loop for Ada's Viral guide.

The runner talks only to a loopback LM Studio native API. It never imports or
invokes OpenAI, Work, ComfyUI, Worker, or Ada's rendering pipeline.

This file is safe to import: no directories are created and no requests are
made until ``main()`` runs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
import time
import traceback
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse


ADA_ROOT = Path(__file__).resolve().parents[1]
CONFIG_ROOT = ADA_ROOT / "config"
ANALYSIS_ROOT = ADA_ROOT / "analysis"
from ada_paths import LEGACY_RUNS_ROOT
EVOLUTION_ROOT = LEGACY_RUNS_ROOT / "evolution"

BASELINE_V12 = CONFIG_ROOT / "prompt_guides" / "viral_premise_guide_v1.2.md"
EXTREME_TEST_V1 = CONFIG_ROOT / "prompt_guides" / "viral_premise_guide_extreme_test_v1.md"
INITIAL_REPORT_V1 = ANALYSIS_ROOT / "viral_guide_iteration_report_v1.md"
LOCAL_CONFIG = CONFIG_ROOT / "ada.local.json"
ORCHESTRATION_CONFIG = CONFIG_ROOT / "orchestration.json"

# Long-running local operation stops safely with Ctrl+C; this is only a
# guardrail, not a promise to run all cycles in one session.
DEFAULT_MAX_CYCLES = 999
DEFAULT_REQUEST_TIMEOUT_SECONDS = 900
DEFAULT_REQUEST_RETRIES = 2
DEFAULT_DELAY_SECONDS = 1.0
PROPOSAL_COUNT = 20
CANDIDATE_MAX_OUTPUT_TOKENS = 4200
PREMISE_BATCH_MAX_OUTPUT_TOKENS = 1600
ANALYSIS_MAX_OUTPUT_TOKENS = 3500
CATEGORY_PLAN = ["closeup", "medium", "fullbody", "dynamic", "cinematic"] * 4
EXPECTED_DISTRIBUTION = {
    "closeup": 4,
    "medium": 4,
    "fullbody": 4,
    "dynamic": 4,
    "cinematic": 4,
}

DEFAULT_CHARACTER = "2B"
DEFAULT_VERSION = "NieR:Automata"
DEFAULT_CHARACTER_PROFILE: dict[str, Any] = {
    "character": DEFAULT_CHARACTER,
    "version": DEFAULT_VERSION,
    "identity_facts": [
        "adult female android",
        "short white hair",
        "black blindfold",
        "hairband",
        "black dress with clothing cutout",
        "black gloves",
        "puffy feather-trimmed sleeves",
        "thigh-high boots and thigh-high stockings",
    ],
    "personality_guardrails": [
        "controlled and composed",
        "confident without becoming generically flirtatious",
        "emotion may appear through brief cracks in her restraint",
    ],
    "factual_rule": "Do not invent precise canon facts absent from this profile.",
}

ScoreValidator = Callable[[Any], Any]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json_object(path: Path, *, optional: bool = False) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        if optional:
            return {}
        raise
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON file: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return value


def read_required_text(path: Path) -> str:
    try:
        content = path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise FileNotFoundError(f"Required input is unavailable: {path}") from exc
    if not content:
        raise ValueError(f"Required input is empty: {path}")
    return content


def write_text_new(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(content.rstrip() + "\n")


def write_json_new(path: Path, value: Any) -> None:
    write_text_new(path, json.dumps(value, ensure_ascii=False, indent=2))


def write_text_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        temporary.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def write_json_atomic(path: Path, value: Any) -> None:
    write_text_atomic(path, json.dumps(value, ensure_ascii=False, indent=2))


def sha256_text(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def resolve_default_lm_studio_url() -> str:
    environment = os.environ.get("ADA_LMSTUDIO_URL") or os.environ.get("LM_STUDIO_URL")
    if environment:
        return environment.rstrip("/")
    local = read_json_object(LOCAL_CONFIG, optional=True)
    orchestration = read_json_object(ORCHESTRATION_CONFIG, optional=True)
    return str(
        local.get("lmstudio_base_url")
        or orchestration.get("lm_studio_url")
        or "http://127.0.0.1:1234"
    ).rstrip("/")


def resolve_default_model() -> str:
    environment = os.environ.get("LM_STUDIO_MODEL")
    if environment:
        return environment
    orchestration = read_json_object(ORCHESTRATION_CONFIG, optional=True)
    models = orchestration.get("models")
    if isinstance(models, dict):
        master = models.get("master")
        if isinstance(master, dict) and isinstance(master.get("model"), str):
            return master["model"]
    return "qwen3.8-27b-uncensored"


def require_loopback_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("LM Studio URL must use http or https")
    if parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError(
            "Local-only safety check failed: LM Studio URL must use localhost, 127.0.0.1, or ::1"
        )
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("LM Studio URL must not contain credentials, query parameters, or fragments")
    return url.rstrip("/")


def extract_native_content(response: dict[str, Any]) -> str:
    for item in response.get("output", []):
        if not isinstance(item, dict) or item.get("type") != "message":
            continue
        content = item.get("content")
        if isinstance(content, str) and content.strip():
            return content.strip()
        if isinstance(content, list):
            parts: list[str] = []
            for block in content:
                if isinstance(block, dict) and isinstance(block.get("text"), str):
                    parts.append(block["text"])
            joined = "\n".join(parts).strip()
            if joined:
                return joined
    raise ValueError("LM Studio response did not contain final message text")


def strip_markdown_fence(content: str) -> str:
    stripped = content.strip()
    match = re.fullmatch(r"```(?:markdown|md|json)?\s*\n?(.*?)\n?```", stripped, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else stripped


def compact_evidence(content: str, maximum_characters: int) -> str:
    """Keep prompt evidence within the configured local model context window."""
    if len(content) <= maximum_characters:
        return content
    head = maximum_characters * 2 // 3
    tail = maximum_characters - head
    omitted = len(content) - maximum_characters
    return (
        f"{content[:head].rstrip()}\n\n"
        f"[... {omitted} characters omitted for local context safety ...]\n\n"
        f"{content[-tail:].lstrip()}"
    )


def parse_json_content(content: str) -> Any:
    stripped = strip_markdown_fence(content)
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        starts = [index for index in (stripped.find("{"), stripped.find("[")) if index >= 0]
        if not starts:
            raise ValueError("Response contains no JSON object or array")
        start = min(starts)
        try:
            value, _ = json.JSONDecoder().raw_decode(stripped[start:])
        except json.JSONDecodeError as exc:
            raise ValueError(f"Response contains invalid JSON: {exc}") from exc
        return value


class LocalLMStudio:
    def __init__(
        self,
        base_url: str,
        model: str,
        timeout_seconds: int,
        retries: int,
        delay_seconds: float,
    ) -> None:
        self.base_url = require_loopback_url(base_url)
        self.model = model
        self.timeout_seconds = timeout_seconds
        self.retries = retries
        self.delay_seconds = delay_seconds
        self.token = os.environ.get("LM_STUDIO_API_TOKEN", "").strip()

    def _request_once(self, prompt: str, temperature: float, max_output_tokens: int) -> dict[str, Any]:
        payload = {
            "model": self.model,
            "input": [{"type": "text", "content": prompt}],
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
            "reasoning": "off",
            "store": False,
        }
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = urllib.request.Request(
            f"{self.base_url}/api/v1/chat",
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"LM Studio HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"LM Studio unavailable at {self.base_url}: {exc.reason}") from exc
        try:
            value = json.loads(body)
        except json.JSONDecodeError as exc:
            raise RuntimeError("LM Studio returned invalid response JSON") from exc
        if not isinstance(value, dict):
            raise RuntimeError("LM Studio returned a non-object response")
        return value

    def generate_text(
        self,
        prompt: str,
        raw_dir: Path,
        artifact_name: str,
        *,
        temperature: float,
        max_output_tokens: int,
        validator: Callable[[str], str],
    ) -> str:
        correction = ""
        errors: list[str] = []
        for attempt in range(1, self.retries + 2):
            attempt_prompt = prompt + correction
            try:
                response = self._request_once(attempt_prompt, temperature, max_output_tokens)
                write_json_new(raw_dir / f"{artifact_name}_attempt_{attempt:02d}.json", response)
                content = extract_native_content(response)
                write_text_new(raw_dir / f"{artifact_name}_attempt_{attempt:02d}.txt", content)
                result = validator(content)
                if self.delay_seconds:
                    time.sleep(self.delay_seconds)
                return result
            except Exception as exc:
                message = f"attempt {attempt}: {type(exc).__name__}: {exc}"
                errors.append(message)
                error_path = raw_dir / f"{artifact_name}_attempt_{attempt:02d}_error.txt"
                if not error_path.exists():
                    write_text_new(error_path, message)
                correction = (
                    "\n\nYour previous attempt failed local validation with this error:\n"
                    f"{message}\nReturn a corrected answer only, following the original output contract exactly."
                )
                if attempt <= self.retries and self.delay_seconds:
                    time.sleep(self.delay_seconds)
        raise RuntimeError(f"{artifact_name} failed after {self.retries + 1} attempts: {' | '.join(errors)}")

    def generate_json(
        self,
        prompt: str,
        raw_dir: Path,
        artifact_name: str,
        *,
        temperature: float,
        max_output_tokens: int,
        validator: ScoreValidator,
    ) -> Any:
        def validate_text(content: str) -> Any:
            return validator(parse_json_content(content))

        return self.generate_text(
            prompt,
            raw_dir,
            artifact_name,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            validator=validate_text,
        )


def validate_candidate_guide(content: str) -> str:
    guide = strip_markdown_fence(content)
    if len(guide) < 3500:
        raise ValueError("Candidate guide is too short to be a complete production candidate")
    lowered = guide.casefold()
    required_terms = (
        "identity",
        "visual",
        "micro-story",
        "diversity",
        "animation",
        "closeup",
        "medium",
        "fullbody",
        "dynamic",
        "cinematic",
    )
    missing = [term for term in required_terms if term not in lowered]
    if missing:
        raise ValueError(f"Candidate guide is missing required concepts: {missing}")
    if not guide.lstrip().startswith("#"):
        raise ValueError("Candidate guide must be a Markdown document with a title")
    return guide


def validate_proposals(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list) or len(value) != PROPOSAL_COUNT:
        raise ValueError(f"Expected exactly {PROPOSAL_COUNT} proposals")
    required = {"id", "category", "premise"}
    identifiers: set[str] = set()
    distribution = {name: 0 for name in EXPECTED_DISTRIBUTION}
    validated: list[dict[str, str]] = []
    for index, item in enumerate(value, 1):
        if not isinstance(item, dict) or set(item) != required:
            raise ValueError(f"Proposal {index} must contain only id, category, and premise")
        if not all(isinstance(item[key], str) and item[key].strip() for key in required):
            raise ValueError(f"Proposal {index} fields must be non-empty strings")
        identifier = item["id"].strip()
        category = item["category"].strip().casefold()
        premise = item["premise"].strip()
        if identifier in identifiers:
            raise ValueError(f"Duplicate proposal id: {identifier}")
        if category not in distribution:
            raise ValueError(f"Unknown category in proposal {index}: {category}")
        identifiers.add(identifier)
        distribution[category] += 1
        validated.append({"id": identifier, "category": category, "premise": premise})
    if distribution != EXPECTED_DISTRIBUTION:
        raise ValueError(f"Invalid category distribution: {distribution}")
    return validated


def validate_proposal_batch(value: Any, batch_number: int) -> list[dict[str, str]]:
    if not isinstance(value, list) or len(value) != 5:
        raise ValueError("Each proposal batch must contain exactly five proposals")
    required = {"id", "category", "premise"}
    categories: set[str] = set()
    identifiers: set[str] = set()
    validated: list[dict[str, str]] = []
    for index, item in enumerate(value, 1):
        if not isinstance(item, dict) or set(item) != required:
            raise ValueError(f"Batch proposal {index} must contain only id, category, and premise")
        if not all(isinstance(item[key], str) and item[key].strip() for key in required):
            raise ValueError(f"Batch proposal {index} fields must be non-empty strings")
        category = item["category"].strip().casefold()
        if category not in EXPECTED_DISTRIBUTION:
            raise ValueError(f"Unknown category: {category}")
        if category in categories:
            raise ValueError(f"Batch {batch_number} repeats category: {category}")
        identifier = item["id"].strip()
        if identifier in identifiers:
            raise ValueError(f"Batch {batch_number} repeats id: {identifier}")
        categories.add(category)
        identifiers.add(identifier)
        validated.append({"id": identifier, "category": category, "premise": item["premise"].strip()})
    if categories != set(EXPECTED_DISTRIBUTION):
        raise ValueError(f"Batch {batch_number} must contain one proposal per category")
    return validated


def validate_score(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be numeric")
    score = float(value)
    if not math.isfinite(score) or not 0 <= score <= 10:
        raise ValueError(f"{field} must be between 0 and 10")
    return score


def validate_string_list(value: Any, field: str, minimum: int = 1) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{field} must be an array")
    result = [item.strip() for item in value if isinstance(item, str) and item.strip()]
    if len(result) < minimum or len(result) != len(value):
        raise ValueError(f"{field} must contain at least {minimum} non-empty strings")
    return result


def validate_analysis(value: Any, proposal_ids: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("Analysis must be a JSON object")
    per_premise = value.get("per_premise")
    if not isinstance(per_premise, list) or len(per_premise) != PROPOSAL_COUNT:
        raise ValueError(f"per_premise must contain exactly {PROPOSAL_COUNT} rows")
    score_fields = ("identity", "visual_appeal", "micro_story", "animation_potential")
    normalized_rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, row in enumerate(per_premise, 1):
        if not isinstance(row, dict):
            raise ValueError(f"Analysis row {index} must be an object")
        identifier = row.get("id")
        if not isinstance(identifier, str) or identifier not in proposal_ids or identifier in seen:
            raise ValueError(f"Analysis row {index} has an invalid or duplicate id")
        notes = row.get("notes")
        if not isinstance(notes, str) or not notes.strip():
            raise ValueError(f"Analysis row {index} requires notes")
        normalized = {"id": identifier}
        for field in score_fields:
            normalized[field] = validate_score(row.get(field), f"per_premise.{identifier}.{field}")
        normalized["notes"] = notes.strip()
        normalized_rows.append(normalized)
        seen.add(identifier)
    if seen != proposal_ids:
        raise ValueError("Analysis rows do not cover every proposal id")

    set_scores = value.get("set_scores")
    if not isinstance(set_scores, dict):
        raise ValueError("set_scores must be an object")
    set_score_fields = (
        "identity",
        "visual_appeal",
        "diversity",
        "repetition_control",
        "micro_story",
        "animation_potential",
    )
    normalized_set_scores = {
        field: validate_score(set_scores.get(field), f"set_scores.{field}")
        for field in set_score_fields
    }

    clusters = value.get("repetition_clusters")
    if not isinstance(clusters, list):
        raise ValueError("repetition_clusters must be an array")
    normalized_clusters: list[dict[str, Any]] = []
    for index, cluster in enumerate(clusters, 1):
        if not isinstance(cluster, dict):
            raise ValueError(f"Repetition cluster {index} must be an object")
        pattern = cluster.get("pattern")
        ids = cluster.get("proposal_ids")
        if not isinstance(pattern, str) or not pattern.strip():
            raise ValueError(f"Repetition cluster {index} requires a pattern")
        if not isinstance(ids, list) or not all(isinstance(item, str) and item in proposal_ids for item in ids):
            raise ValueError(f"Repetition cluster {index} contains invalid proposal ids")
        normalized_clusters.append({"pattern": pattern.strip(), "proposal_ids": ids})

    verdict = value.get("verdict")
    if not isinstance(verdict, str) or not verdict.strip():
        raise ValueError("verdict must be non-empty text")
    return {
        "per_premise": normalized_rows,
        "set_scores": normalized_set_scores,
        "strengths": validate_string_list(value.get("strengths"), "strengths", 2),
        "failures": validate_string_list(value.get("failures"), "failures", 2),
        "desired_patterns": validate_string_list(value.get("desired_patterns"), "desired_patterns", 2),
        "undesired_patterns": validate_string_list(value.get("undesired_patterns"), "undesired_patterns", 2),
        "repetition_clusters": normalized_clusters,
        "recommendations_for_next_cycle": validate_string_list(
            value.get("recommendations_for_next_cycle"), "recommendations_for_next_cycle", 3
        ),
        "verdict": verdict.strip(),
    }


def candidate_prompt(
    cycle_number: int,
    baseline: str,
    extreme: str,
    initial_report: str,
    previous_report: str,
    previous_candidate: str | None,
) -> str:
    # The 8k local context must include both the evidence and the generated guide.
    # Keep the beginning and conclusion of each source, and never send the initial
    # report twice on the first cycle.
    baseline_section = compact_evidence(baseline, 7000)
    extreme_section = compact_evidence(extreme, 2500)
    initial_report_section = compact_evidence(initial_report, 4000)
    previous_report_section = (
        "The initial iteration report above is also the most recent evidence; no completed cycle exists yet."
        if previous_report == initial_report
        else compact_evidence(previous_report, 4000)
    )
    previous_candidate_section = (
        compact_evidence(previous_candidate, 4000)
        if previous_candidate
        else "No previous candidate exists; this is the first cycle."
    )
    return f"""You are evolving Ada's Viral Premise Guide using only the evidence provided below.

Create the complete candidate guide for evolution cycle {cycle_number:03d}. Write the guide in English as a standalone Markdown document. Return only the Markdown document, without a code fence or commentary.

The candidate is experimental and must remain inside this run directory. Do not claim to update production files. Preserve non-explicit boundaries. Improve identity, visual appeal, diversity, repetition control, micro-story, and animation potential together. Do not merely average the baseline and extreme guides: use the iteration evidence and correct the last cycle's weaknesses. Include explicit batch-level diversity enforcement, causal premise requirements, category rules, factual identity safeguards, hard anti-pattern rules, and an acceptance checklist.

=== PRODUCTION BASELINE v1.2 (READ-ONLY) ===
{baseline_section}

=== EXTREME DIAGNOSTIC GUIDE (READ-ONLY) ===
{extreme_section}

=== INITIAL ITERATION REPORT (READ-ONLY) ===
{initial_report_section}

=== REPORT FROM THE MOST RECENT SUCCESSFUL CYCLE ===
{previous_report_section}

=== CANDIDATE FROM THE MOST RECENT SUCCESSFUL CYCLE ===
{previous_candidate_section}
"""


def proposal_batch_prompt(
    cycle_number: int,
    batch_number: int,
    guide: str,
    character: str,
    version: str,
    profile: dict[str, Any],
    previous_proposals: list[dict[str, str]],
) -> str:
    prior = json.dumps(previous_proposals, ensure_ascii=False, indent=2) if previous_proposals else "[]"
    return f"""Generate premise proposals only for a local diagnostic. Do not create image prompts, do not render, and do not call tools.

This is evolution cycle {cycle_number:03d}, proposal batch {batch_number} of 4. Return only one valid JSON array with exactly five objects. Each object must contain only: id, category, premise. Include exactly one proposal in each category: closeup, medium, fullbody, dynamic, cinematic.

Use IDs prefixed with e{cycle_number:03d}_b{batch_number:02d}_. Every premise must be distinct from the proposals already generated in this cycle. Apply the candidate guide's diversity ledger across batches, not just inside this batch.

Character: {character}
Version: {version}
Local identity profile (the only source of precise identity facts):
{json.dumps(profile, ensure_ascii=False, indent=2)}

Proposals already generated in this cycle:
{prior}

Candidate Viral guide:
{guide}
"""


def analysis_prompt(
    cycle_number: int,
    guide: str,
    proposals: list[dict[str, str]],
    profile: dict[str, Any],
) -> str:
    return f"""Audit evolution cycle {cycle_number:03d} rigorously. Do not rewrite the guide and do not generate image prompts. Evaluate the actual set of 20 premises against the candidate guide and local identity profile.

Analyze these dimensions: identity, visual appeal, diversity, repetition, micro-story, and animation potential. Penalize repeated conceptual families even when wording or framing changes. Penalize unsupported canon facts, atmosphere replacing events, generic gameplay, pure poses, direct gaze/smirk as a substitute for interaction, and motion without cause or consequence.

Return only one valid JSON object with this exact structure:
{{
  "per_premise": [
    {{"id": "...", "identity": 0-10, "visual_appeal": 0-10, "micro_story": 0-10, "animation_potential": 0-10, "notes": "..."}}
  ],
  "set_scores": {{
    "identity": 0-10,
    "visual_appeal": 0-10,
    "diversity": 0-10,
    "repetition_control": 0-10,
    "micro_story": 0-10,
    "animation_potential": 0-10
  }},
  "strengths": ["..."],
  "failures": ["..."],
  "desired_patterns": ["..."],
  "undesired_patterns": ["..."],
  "repetition_clusters": [{{"pattern": "...", "proposal_ids": ["..."]}}],
  "recommendations_for_next_cycle": ["..."],
  "verdict": "..."
}}

There must be exactly one per_premise row for every proposal ID. Scores may be integers or decimals from 0 to 10.

Local identity profile:
{json.dumps(profile, ensure_ascii=False, indent=2)}

Candidate guide:
{guide}

Premises:
{json.dumps(proposals, ensure_ascii=False, indent=2)}
"""


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def bullet_section(title: str, items: list[str]) -> list[str]:
    lines = [f"## {title}", ""]
    lines.extend(f"- {item}" for item in items)
    lines.append("")
    return lines


def build_cycle_report(
    cycle_number: int,
    model: str,
    proposals: list[dict[str, str]],
    analysis: dict[str, Any],
) -> str:
    proposal_by_id = {item["id"]: item for item in proposals}
    scores = analysis["set_scores"]
    overall = sum(scores.values()) / len(scores)
    lines = [
        f"# Ada Viral Guide Evolution — Cycle {cycle_number:03d}",
        "",
        f"- Model: `{model}` via local LM Studio",
        f"- Premises: {len(proposals)}",
        "- Rendering: not executed",
        f"- Overall diagnostic mean: {overall:.2f}/10",
        "",
        "## Set scores",
        "",
        "| Dimension | Score |",
        "|---|---:|",
    ]
    for field, score in scores.items():
        lines.append(f"| {markdown_cell(field.replace('_', ' ').title())} | {score:.2f} |")
    lines.extend(["", "## Verdict", "", analysis["verdict"], ""])
    lines.extend(bullet_section("Strengths", analysis["strengths"]))
    lines.extend(bullet_section("Failures", analysis["failures"]))
    lines.extend(bullet_section("Desired patterns", analysis["desired_patterns"]))
    lines.extend(bullet_section("Undesired patterns", analysis["undesired_patterns"]))
    lines.extend(["## Repetition clusters", ""])
    if analysis["repetition_clusters"]:
        for cluster in analysis["repetition_clusters"]:
            identifiers = ", ".join(f"`{item}`" for item in cluster["proposal_ids"])
            lines.append(f"- **{cluster['pattern']}**: {identifiers or 'no IDs supplied'}")
    else:
        lines.append("- No material repetition cluster was identified.")
    lines.append("")
    lines.extend(bullet_section("Recommendations for the next cycle", analysis["recommendations_for_next_cycle"]))
    lines.extend([
        "## Per-premise audit",
        "",
        "| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |",
        "|---|---|---:|---:|---:|---:|---|",
    ])
    for row in analysis["per_premise"]:
        proposal = proposal_by_id[row["id"]]
        lines.append(
            f"| `{markdown_cell(row['id'])}` | {markdown_cell(proposal['category'])} | "
            f"{row['identity']:.1f} | {row['visual_appeal']:.1f} | {row['micro_story']:.1f} | "
            f"{row['animation_potential']:.1f} | {markdown_cell(row['notes'])} |"
        )
    lines.extend(["", "## Premises", ""])
    for proposal in proposals:
        lines.extend([
            f"### {proposal['id']} — {proposal['category']}",
            "",
            proposal["premise"],
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def next_run_number(root: Path) -> int:
    highest = 0
    if root.exists():
        for child in root.iterdir():
            match = re.fullmatch(r"run_(\d{3,})", child.name) if child.is_dir() else None
            if match:
                highest = max(highest, int(match.group(1)))
    return highest + 1


def latest_successful_artifacts(root: Path) -> tuple[Path | None, Path | None]:
    candidates: list[tuple[int, Path, Path]] = []
    if not root.exists():
        return None, None
    for child in root.iterdir():
        match = re.fullmatch(r"run_(\d{3,})", child.name) if child.is_dir() else None
        if not match:
            continue
        state_path = child / "state.json"
        report_path = child / "cycle_report.md"
        guide_path = child / "candidate_guide.md"
        try:
            state = read_json_object(state_path)
        except (OSError, ValueError):
            continue
        if state.get("status") == "completed" and report_path.is_file() and guide_path.is_file():
            candidates.append((int(match.group(1)), report_path, guide_path))
    if not candidates:
        return None, None
    _, report, guide = max(candidates, key=lambda item: item[0])
    return report, guide


def write_last_completed_checkpoint(state: dict[str, Any]) -> None:
    """Atomically record the newest completed cycle for overnight recovery."""
    write_json_atomic(
        EVOLUTION_ROOT / "last_completed_cycle.json",
        {
            "run": state["run"],
            "completed_at": state["ended_at"],
            "model": state["model"],
            "lm_studio_url": state["lm_studio_url"],
            "set_scores": state["set_scores"],
            "files": state["files"],
        },
    )


def snapshot_inputs(
    run_dir: Path,
    baseline: str,
    extreme: str,
    initial_report: str,
    previous_report: str,
    previous_report_source: Path,
    previous_candidate: str | None,
    previous_candidate_source: Path | None,
) -> dict[str, Any]:
    inputs_dir = run_dir / "inputs"
    snapshots = [
        ("baseline_v1.2.md", BASELINE_V12, baseline),
        ("extreme_test_v1.md", EXTREME_TEST_V1, extreme),
        ("initial_iteration_report_v1.md", INITIAL_REPORT_V1, initial_report),
        ("previous_cycle_report.md", previous_report_source, previous_report),
    ]
    if previous_candidate is not None and previous_candidate_source is not None:
        snapshots.append(("previous_candidate_guide.md", previous_candidate_source, previous_candidate))
    manifest: dict[str, Any] = {"captured_at": utc_now(), "files": {}}
    for snapshot_name, source, content in snapshots:
        write_text_new(inputs_dir / snapshot_name, content)
        manifest["files"][snapshot_name] = {
            "source": str(source.resolve()),
            "sha256": sha256_text(content),
            "bytes": len(content.encode("utf-8")),
        }
    write_json_new(run_dir / "input_manifest.json", manifest)
    return manifest


def load_character_profile(path: Path | None, character: str, version: str) -> dict[str, Any]:
    if path is None:
        if character != DEFAULT_CHARACTER or version != DEFAULT_VERSION:
            raise ValueError("A custom --character-profile JSON is required when changing character or version")
        return dict(DEFAULT_CHARACTER_PROFILE)
    profile = read_json_object(path)
    if not profile:
        raise ValueError("Character profile cannot be empty")
    return profile


def run_one_cycle(
    run_number: int,
    client: LocalLMStudio,
    character: str,
    version: str,
    profile: dict[str, Any],
) -> dict[str, Any]:
    run_dir = EVOLUTION_ROOT / f"run_{run_number:03d}"
    run_dir.mkdir(parents=False, exist_ok=False)
    raw_dir = run_dir / "raw_responses"
    raw_dir.mkdir(exist_ok=False)
    state = {
        "schema_version": 1,
        "run": run_number,
        "status": "started",
        "started_at": utc_now(),
        "ended_at": None,
        "model": client.model,
        "lm_studio_url": client.base_url,
        "character": character,
        "version": version,
        "openai_used": False,
        "work_used": False,
        "comfyui_used": False,
        "worker_used": False,
    }
    write_json_atomic(run_dir / "state.json", state)

    try:
        # Re-read all three required sources during every cycle.
        baseline = read_required_text(BASELINE_V12)
        extreme = read_required_text(EXTREME_TEST_V1)
        initial_report = read_required_text(INITIAL_REPORT_V1)
        previous_report_path, previous_candidate_path = latest_successful_artifacts(EVOLUTION_ROOT)
        if previous_report_path is None:
            previous_report_path = INITIAL_REPORT_V1
        previous_report = read_required_text(previous_report_path)
        previous_candidate = read_required_text(previous_candidate_path) if previous_candidate_path else None

        manifest = snapshot_inputs(
            run_dir,
            baseline,
            extreme,
            initial_report,
            previous_report,
            previous_report_path,
            previous_candidate,
            previous_candidate_path,
        )

        guide = client.generate_text(
            candidate_prompt(
                run_number,
                baseline,
                extreme,
                initial_report,
                previous_report,
                previous_candidate,
            ),
            raw_dir,
            "candidate_guide",
            temperature=0.55,
            max_output_tokens=CANDIDATE_MAX_OUTPUT_TOKENS,
            validator=validate_candidate_guide,
        )
        write_text_new(run_dir / "candidate_guide.md", guide)

        proposals: list[dict[str, str]] = []
        for batch_number in range(1, 5):
            batch = client.generate_json(
                proposal_batch_prompt(
                    run_number,
                    batch_number,
                    guide,
                    character,
                    version,
                    profile,
                    proposals,
                ),
                raw_dir,
                f"premises_batch_{batch_number:02d}",
                temperature=0.75,
                max_output_tokens=PREMISE_BATCH_MAX_OUTPUT_TOKENS,
                validator=lambda value, number=batch_number: validate_proposal_batch(value, number),
            )
            existing_ids = {item["id"] for item in proposals}
            duplicate_ids = existing_ids.intersection(item["id"] for item in batch)
            if duplicate_ids:
                raise ValueError(f"Proposal IDs repeat across batches: {sorted(duplicate_ids)}")
            proposals.extend(batch)
        proposals = validate_proposals(proposals)
        premise_document = {
            "schema_version": 1,
            "run": run_number,
            "character": character,
            "version": version,
            "count": len(proposals),
            "distribution": EXPECTED_DISTRIBUTION,
            "candidate_guide": "candidate_guide.md",
            "lm_studio_only": True,
            "rendering_executed": False,
            "proposals": proposals,
        }
        write_json_new(run_dir / "premises.json", premise_document)

        analysis = client.generate_json(
            analysis_prompt(run_number, guide, proposals, profile),
            raw_dir,
            "analysis",
            temperature=0.25,
            max_output_tokens=ANALYSIS_MAX_OUTPUT_TOKENS,
            validator=lambda value: validate_analysis(value, {item["id"] for item in proposals}),
        )
        write_json_new(run_dir / "analysis.json", analysis)
        report = build_cycle_report(run_number, client.model, proposals, analysis)
        write_text_new(run_dir / "cycle_report.md", report)

        state.update({
            "status": "completed",
            "ended_at": utc_now(),
            "input_manifest_sha256": sha256_text(json.dumps(manifest, sort_keys=True)),
            "set_scores": analysis["set_scores"],
            "files": {
                "candidate_guide": "candidate_guide.md",
                "premises": "premises.json",
                "analysis": "analysis.json",
                "report": "cycle_report.md",
            },
        })
        write_json_atomic(run_dir / "state.json", state)
        write_last_completed_checkpoint(state)
        return state
    except KeyboardInterrupt:
        state.update({"status": "interrupted", "ended_at": utc_now()})
        write_json_atomic(run_dir / "state.json", state)
        write_text_new(run_dir / "error.md", "# Cycle interrupted\n\nThe operator interrupted this cycle.")
        raise
    except Exception as exc:
        error = {
            "run": run_number,
            "failed_at": utc_now(),
            "exception_type": type(exc).__name__,
            "message": str(exc),
            "traceback": traceback.format_exc(),
        }
        write_json_new(run_dir / "error.json", error)
        write_text_new(
            run_dir / "error.md",
            f"# Cycle {run_number:03d} failed\n\n- Type: `{type(exc).__name__}`\n- Message: {exc}\n\nSee `error.json` for the traceback.",
        )
        state.update({"status": "failed", "ended_at": utc_now(), "error": "error.json"})
        write_json_atomic(run_dir / "state.json", state)
        return state


def overall_score(scores: dict[str, Any]) -> float | None:
    values = [float(value) for value in scores.values() if isinstance(value, (int, float)) and not isinstance(value, bool)]
    return sum(values) / len(values) if values else None


def collect_run_states(root: Path) -> list[dict[str, Any]]:
    states: list[dict[str, Any]] = []
    if not root.exists():
        return states
    run_dirs: list[tuple[int, Path]] = []
    for child in root.iterdir():
        match = re.fullmatch(r"run_(\d{3,})", child.name) if child.is_dir() else None
        if match:
            run_dirs.append((int(match.group(1)), child))
    for run_number, run_dir in sorted(run_dirs):
        try:
            state = read_json_object(run_dir / "state.json")
        except (OSError, ValueError) as exc:
            state = {"run": run_number, "status": "unreadable", "error": str(exc)}
        state["run_dir"] = str(run_dir.resolve())
        states.append(state)
    return states


def build_evolution_summary(states: list[dict[str, Any]], model: str, base_url: str) -> str:
    completed = [state for state in states if state.get("status") == "completed"]
    failed = [state for state in states if state.get("status") == "failed"]
    ranked: list[tuple[float, int]] = []
    for state in completed:
        score = overall_score(state.get("set_scores", {}))
        if score is not None:
            ranked.append((score, int(state["run"])))
    best = max(ranked) if ranked else None
    lines = [
        "# Ada Viral Guide Evolution Summary",
        "",
        f"- Updated: {utc_now()}",
        f"- Local LM Studio URL: `{base_url}`",
        f"- Model: `{model}`",
        f"- Runs recorded: {len(states)}",
        f"- Completed: {len(completed)}",
        f"- Failed: {len(failed)}",
        "- OpenAI / Work / ComfyUI / Worker used: no",
        "",
    ]
    if best:
        lines.extend([
            f"Best completed run by unweighted diagnostic mean: `run_{best[1]:03d}` ({best[0]:.2f}/10).",
            "",
        ])
    lines.extend([
        "## Runs",
        "",
        "| Run | Status | Overall | Identity | Appeal | Diversity | Repetition | Micro-story | Animation |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|",
    ])
    for state in states:
        scores = state.get("set_scores") if isinstance(state.get("set_scores"), dict) else {}
        mean = overall_score(scores)
        display = lambda field: f"{float(scores[field]):.2f}" if isinstance(scores.get(field), (int, float)) else "—"
        lines.append(
            f"| {int(state.get('run', 0)):03d} | {markdown_cell(state.get('status', 'unknown'))} | "
            f"{f'{mean:.2f}' if mean is not None else '—'} | {display('identity')} | "
            f"{display('visual_appeal')} | {display('diversity')} | {display('repetition_control')} | "
            f"{display('micro_story')} | {display('animation_potential')} |"
        )
    if failed:
        lines.extend(["", "## Failures", ""])
        for state in failed:
            lines.append(f"- `run_{int(state['run']):03d}`: see `run_{int(state['run']):03d}/error.json`.")
    lines.extend([
        "",
        "## Interpretation",
        "",
        "Each completed cycle's `cycle_report.md` is the evidence supplied to the next cycle. "
        "Scores are local-model diagnostics, not ground truth; inspect the winning guide and premises before promoting anything to production.",
        "",
        "No candidate is automatically copied into `config/prompt_guides`. Promotion remains a manual decision.",
        "",
    ])
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-cycles", type=int, default=DEFAULT_MAX_CYCLES)
    parser.add_argument("--model", default=resolve_default_model())
    parser.add_argument("--lm-studio-url", default=resolve_default_lm_studio_url())
    parser.add_argument("--timeout-seconds", type=int, default=DEFAULT_REQUEST_TIMEOUT_SECONDS)
    parser.add_argument("--request-retries", type=int, default=DEFAULT_REQUEST_RETRIES)
    parser.add_argument("--delay-seconds", type=float, default=DEFAULT_DELAY_SECONDS)
    parser.add_argument("--character", default=DEFAULT_CHARACTER)
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument("--character-profile", type=Path)
    return parser


def validate_args(args: argparse.Namespace) -> None:
    if not 1 <= args.max_cycles <= DEFAULT_MAX_CYCLES:
        raise ValueError(f"--max-cycles must be between 1 and {DEFAULT_MAX_CYCLES}")
    if args.timeout_seconds < 30:
        raise ValueError("--timeout-seconds must be at least 30")
    if not 0 <= args.request_retries <= 10:
        raise ValueError("--request-retries must be between 0 and 10")
    if not 0 <= args.delay_seconds <= 300:
        raise ValueError("--delay-seconds must be between 0 and 300")
    if not args.model.strip():
        raise ValueError("--model cannot be empty")
    require_loopback_url(args.lm_studio_url)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    validate_args(args)
    profile_path = args.character_profile.resolve() if args.character_profile else None
    profile = load_character_profile(profile_path, args.character, args.version)
    client = LocalLMStudio(
        args.lm_studio_url,
        args.model.strip(),
        args.timeout_seconds,
        args.request_retries,
        args.delay_seconds,
    )

    EVOLUTION_ROOT.mkdir(parents=True, exist_ok=True)
    first_run = next_run_number(EVOLUTION_ROOT)
    interrupted = False
    for offset in range(args.max_cycles):
        run_number = first_run + offset
        print(json.dumps({"event": "cycle_started", "run": run_number, "at": utc_now()}), flush=True)
        try:
            state = run_one_cycle(run_number, client, args.character, args.version, profile)
        except KeyboardInterrupt:
            interrupted = True
            print(json.dumps({"event": "interrupted", "run": run_number, "at": utc_now()}), flush=True)
            break
        print(
            json.dumps(
                {"event": "cycle_finished", "run": run_number, "status": state["status"], "at": utc_now()},
                ensure_ascii=False,
            ),
            flush=True,
        )

    states = collect_run_states(EVOLUTION_ROOT)
    summary = build_evolution_summary(states, client.model, client.base_url)
    write_text_atomic(EVOLUTION_ROOT / "evolution_summary.md", summary)
    print(
        json.dumps(
            {
                "event": "evolution_finished",
                "interrupted": interrupted,
                "summary": str((EVOLUTION_ROOT / 'evolution_summary.md').resolve()),
                "at": utc_now(),
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    return 130 if interrupted else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"evolution runner failed before or after cycle isolation: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1)
