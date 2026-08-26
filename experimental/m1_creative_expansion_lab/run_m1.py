#!/usr/bin/env python3
"""Run the isolated, text-only M1 Creative Expansion Lab exactly once."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ADA_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_ROOT = ADA_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from character_profile import CharacterProfileDatabase  # noqa: E402
from lmstudio_controller import LMStudioController  # noqa: E402
from prompt_guides import PromptGuideLibrary  # noqa: E402


LAB_ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = LAB_ROOT / "concept_proposals_v1.schema.json"
RUNS_ROOT = ADA_ROOT / "experimental_runs" / "m1_creative_expansion_lab"
EXPECTED_MODEL = "qwen3.8-27b-uncensored"
EXPECTED_COUNT = 12
EXTREME_GUIDE_PATH = ADA_ROOT / "config" / "prompt_guides" / "viral_premise_guide_extreme_test_v1.md"
PREMISE_RUNTIME_PATH = ADA_ROOT / "config" / "runtime_instructions" / "premise_runtime_v1.md"

# These names route small, relevant excerpts from the existing source-of-truth
# guides into an 8k context. The text itself remains owned by those guide files.
VIRAL_SECTIONS = (
    "## Role",
    "# Character Identity Priority",
    "# Visual Appeal Philosophy",
    "# Body As A Hook, Not The Entire Premise",
    "# Sensuality Balance",
    "# Erotic Non-Explicit Direction",
    "# Strategic Censorship And Suggestion",
    "# Scene Variety",
    "# Composition Priority",
    "# Avoid Repetition",
    "# Scroll-Stopping Test",
)
ILLUSTRIOUS_SECTIONS = (
    "## Core Principle",
    "## Clothing State",
    "## Pose",
    "## Action",
    "## Expression and Attitude",
    "## Provocative Presentation",
    "## Pure Visual Appeal",
    "## Situational Appeal",
    "## Strategic / Convenient Censorship",
    "## Strong Erotic Implication",
    "## Framing and Body Hook",
    "## One Dominant Visual Idea",
)

TEMPORAL_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("then", re.compile(r"\bthen\b", re.IGNORECASE)),
    (
        "retrospective leakage",
        re.compile(
            r"\b(?:before|after|afterwards?|subsequently|following|having\s+just|having\s+finished|"
            r"just\s+(?:finished|completed)|previously|earlier)\b",
            re.IGNORECASE,
        ),
    ),
    ("future", re.compile(r"\b(?:will|would|later|eventually|next)\b", re.IGNORECASE)),
    (
        "future-intent leakage",
        re.compile(
            r"\b(?:about\s+to|preparing\s+to|ready\s+to|going\s+to|poised\s+to|set\s+to|"
            r"on\s+the\s+verge\s+of|to\s+(?:strike|attack|punch|kick|leap|jump|launch|flee))\b",
            re.IGNORECASE,
        ),
    ),
    ("sequence", re.compile(r"\b(?:followed by|leads? to|escalat(?:e|es|ing|ion)|payoff)\b", re.IGNORECASE)),
    ("video instruction", re.compile(r"\b(?:MiniMax|video|animate|animation|clip|multi[- ]shot)\b", re.IGNORECASE)),
)


class ExperimentError(RuntimeError):
    """A bounded M1 failure that must not trigger a retry."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json_new(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as output:
        json.dump(value, output, ensure_ascii=False, indent=2)
        output.write("\n")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def markdown_section(source: str, heading: str) -> str:
    """Return one exact Markdown section, stopping at an equal/higher heading."""
    lines = source.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == heading)
    except StopIteration as exc:
        raise ExperimentError(f"Required guide section not found: {heading}") from exc
    level = len(heading) - len(heading.lstrip("#"))
    end = len(lines)
    for index in range(start + 1, len(lines)):
        match = re.match(r"^(#+)\s", lines[index])
        if match and len(match.group(1)) <= level:
            end = index
            break
    return "\n".join(lines[start:end]).strip()


def extract_sections(source: str, headings: tuple[str, ...]) -> str:
    return "\n\n".join(markdown_section(source, heading) for heading in headings)


def source_context() -> tuple[dict[str, Any], dict[str, Any]]:
    library = PromptGuideLibrary()
    proposal = library.proposal_context()
    illustrious = library.illustrious_context()
    viral = proposal["guides"][0]
    illustrious_guide = illustrious["guides"][0]
    extreme_text = EXTREME_GUIDE_PATH.read_text(encoding="utf-8").strip()
    runtime_text = PREMISE_RUNTIME_PATH.read_text(encoding="utf-8").strip()
    context = {
        "active_viral_premise_excerpt": extract_sections(viral["content"], VIRAL_SECTIONS),
        "active_illustrious_excerpt": extract_sections(illustrious_guide["content"], ILLUSTRIOUS_SECTIONS),
        "extreme_diagnostic_guide": extreme_text,
        "frame_centric_runtime": runtime_text,
    }
    manifest = {
        "active_registry": str(library.config_path),
        "active_guides": library.manifest(),
        "routed_sources": [
            {
                "name": "viral_premise",
                "version": viral["version"],
                "path": str((ADA_ROOT / "config" / viral["file"]).resolve()),
                "selected_sections": list(VIRAL_SECTIONS),
                "source_sha256": sha256_text(viral["content"]),
            },
            {
                "name": "illustrious_prompt",
                "version": illustrious_guide["version"],
                "path": str((ADA_ROOT / "config" / illustrious_guide["file"]).resolve()),
                "selected_sections": list(ILLUSTRIOUS_SECTIONS),
                "source_sha256": sha256_text(illustrious_guide["content"]),
            },
            {
                "name": "viral_premise_extreme_diagnostic",
                "version": "v1",
                "path": str(EXTREME_GUIDE_PATH.resolve()),
                "selected_sections": ["entire guide"],
                "source_sha256": sha256_text(extreme_text),
            },
            {
                "name": "premise_runtime",
                "version": "v1",
                "path": str(PREMISE_RUNTIME_PATH.resolve()),
                "selected_sections": ["entire runtime instruction"],
                "source_sha256": sha256_text(runtime_text),
            },
        ],
    }
    return context, manifest


def response_schema() -> dict[str, Any]:
    value = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ExperimentError("M1 schema is not an object")
    return value


def concept_id_prefix(character: str) -> str:
    """Stable neutral identifier derived from the requested character, never a demo default."""
    slug = re.sub(r"[^a-z0-9]+", "_", character.casefold()).strip("_")
    return slug or "character"


def compile_m1_active_context(character: str, version: str, profile: dict[str, Any], user_intent: dict[str, Any] | None = None) -> dict[str, Any]:
    """Small production context; historical guides are not prompt payload."""
    return {
        "character": {"name": character, "version": version, "identity": [x for x in profile.get("characteristics", []) if isinstance(x, str)][:6], "outfit": [x for x in profile.get("clothing", []) if isinstance(x, str)][:4]},
        "locked_constraints": user_intent or {},
        "rules": ["one frozen non-explicit moment", "vary action, setting, camera and hook", "never contradict locked constraints", "no prompts or explanations"],
    }


def build_compact_prompts(character: str, version: str, profile: dict[str, Any], user_intent: dict[str, Any] | None = None, generation_mode: str = "direct") -> tuple[str, str]:
    prefix = concept_id_prefix(character)
    context = compile_m1_active_context(character, version, profile, user_intent)
    locked = context["locked_constraints"]
    locked_setting = locked.get("setting", {}).get("value") if isinstance(locked.get("setting"), dict) else None
    locked_action = locked.get("action", {}).get("value") if isinstance(locked.get("action"), dict) else None
    character_data = context["character"]

    if generation_mode == "dataset_auto_concepts":
        system = "Generate viral static-image sketches prioritizing strong visual hook and story. Output JSON only. Never copy instructions."
        task = (
            f"Mode: STOP -> STAY -> IMAGINE NEXT. Goal: hard-to-ignore viral moments.\n"
            f"Character: {character_data['name']} ({character_data['version']}). "
            f"Identity cues: {', '.join(character_data['identity'])}. Outfit cues: {', '.join(character_data['outfit'])}.\n"
            "Return exactly one object with a 'concepts' array containing 12 items. "
            f"Use concept_id m1_{prefix}_01 through m1_{prefix}_12.\n"
            "MANDATORY SCHEMA PER ITEM:\n"
            "- concept_id: string\n"
            "- action: string\n"
            "- setting: string\n"
            "- micro_location: string\n"
            "- camera: string\n"
            "- expression: string\n"
            "- primary_hook: { 'main': string, 'secondary': string (optional) }. E.g. 'bust', 'waist', 'glutes', 'thighs'. Must stop scroll.\n"
            "- context_hook: array of strings. E.g. ['implicit_teasing', 'accidental_sensuality'].\n"
            "- micro_story: string. What just happened or happens next.\n"
            "- animation_beat: string. 5-10s continuation.\n"
            "- why_it_scroll_stops: string. Justification.\n"
            "RULES:\n"
            "1. NO generic poses, NO 'looking at camera', NO wallpaper feelings.\n"
            "2. Adapt attraction strategy to the character's known personality (e.g. powerful/warrior vs playful/teasing).\n"
            "3. Enforce high batch variety across hooks, cameras, and locations."
        )
        return system, task

    system = "Generate compact static-image sketches. User-locked values are immutable. Output JSON only; never copy or summarize the instructions."
    task = (
        f"Character: {character_data['name']} ({character_data['version']}). "
        f"Identity cues: {', '.join(character_data['identity'])}. Outfit cues: {', '.join(character_data['outfit'])}. "
        f"Locked setting: {locked_setting or 'none; choose a real physical setting'}. "
        f"Locked action: {locked_action or 'none; choose freely'}. "
        "Return exactly one object with only key concepts, containing exactly 12 objects. "
        f"Use IDs m1_{prefix}_01 through m1_{prefix}_12 in order. "
        "Each object has exactly: concept_id, action, setting, micro_location, hook, camera, expression. "
        "If setting is locked, repeat it exactly in every setting field. setting is a real place; focus/body zones belong in camera. "
        "Limits: action 8 words, micro_location 5, hook 8, camera 6, expression 3. One frozen moment; no prose outside JSON."
    )
    return system, task


def build_prompts(character: str, version: str, profile: dict[str, Any], guide_context: dict[str, Any]) -> tuple[str, str]:
    return build_compact_prompts(character, version, profile)
    prefix = concept_id_prefix(character)
    system = (
        "You are ADA's isolated Creative Expansion Lab. Generate creative static-image concepts only: a layer BEFORE "
        "PremiseSpec. Do not write PremiseSpec, image prompts, seeds, scores, workflow settings, MiniMax instructions, "
        "or render instructions. The character is a clearly adult fictional character; all sensuality must remain "
        "non-explicit. Return only JSON matching the supplied schema."
    )
    task = {
        "experiment_question": (
            "Can the configured Creative Expansion model generate exactly 12 diverse, provocative static concepts genuinely worth rendering for one character?"
        ),
        "character": character,
        "version": version,
        "character_profile": profile,
        "source_of_truth_guide_excerpts": guide_context,
        "experiment_rules": [
            f"Return exactly 12 ConceptProposals in one response, with concept_id values m1_{prefix}_01 through m1_{prefix}_12.",
            "Each snapshot must describe EXACTLY ONE photographable frozen instant. The image itself is the final product.",
            "Action verbs are explicitly allowed and encouraged when visually useful: walking, bending, adjusting clothing, turning, stepping, holding, or reaching can all be frozen in one instant.",
            "Never describe then, before/after sequences, future consequences, escalation, payoff, or a miniature temporal story.",
            "Treat any temporal or animation-oriented guidance in a source guide only as support for visible energy inside the frozen instant; this static rule has precedence.",
            "Make the character herself the immediate hook. Avoid generic scenery, official-game screenshot energy, and merely pretty portraits.",
            "Preserve recognizable identity and character-appropriate restrained confidence while allowing scene-specific wardrobe states.",
            "Use provocative, teasing, erotic-suggestive impact deliberately: body-focused composition, wardrobe tension, wet fabric, intimate situations, strong silhouettes, strategic censorship, or sexy-comedic tension when coherent.",
            "Remain non-explicit: no sexual acts, genital focus, graphic nudity, or fetishized bodily fluids.",
            "A strong body-focused pin-up is valid if it has a deliberate visual hook, but the set must not become twelve variants of posing at the viewer.",
            "Make the twelve genuinely distinct across setting, visible action/pose, framing, visual emphasis, clothing state, attitude, provocative mechanism, intimate/public context, and serious/comedic tone. These are lightweight diversity checks, not fixed categories.",
            "Give every concept one dominant visible idea and concrete composition intent. Do not use physical camera-equipment language.",
            "Use the diversity_signature honestly to expose repetition; do not hide repeated concepts behind synonyms.",
        ],
        "output_semantics": {
            "snapshot": "The complete frozen instant in one or two concrete sentences.",
            "visual_hook": "Why the image stops attention immediately.",
            "provocative_mechanism": "The non-explicit teasing/body/wardrobe/intimacy mechanism, stated concretely.",
            "composition_intent": "Framing, viewpoint, silhouette, focal hierarchy, and visible spatial relationships.",
            "diversity_signature": "Short descriptive values used to compare this proposal with the other eleven.",
        },
        "literal_output_contract": {
            "return_only": "One JSON object, no Markdown and no explanatory text.",
            "top_level": {"concepts": "array of exactly 12 ConceptProposal objects"},
            "concept_fields_exactly": [
                "concept_id", "snapshot", "visual_hook", "provocative_mechanism", "composition_intent", "diversity_signature"
            ],
            "diversity_signature_fields_exactly": ["setting", "framing", "attitude", "visual_emphasis"],
            "required_ordered_ids": [f"m1_{prefix}_{index:02d}" for index in range(1, EXPECTED_COUNT + 1)],
            "example_shape": {
                "concepts": [{
                    "concept_id": f"m1_{prefix}_01",
                    "snapshot": "one frozen photographable instant",
                    "visual_hook": "concrete immediate hook",
                    "provocative_mechanism": "non-explicit concrete mechanism",
                    "composition_intent": "visible framing and focal hierarchy",
                    "diversity_signature": {
                        "setting": "...", "framing": "...", "attitude": "...", "visual_emphasis": "..."
                    }
                }]
            },
        },
    }
    return system, json.dumps(task, ensure_ascii=False, indent=2)


def http_json(url: str, *, method: str = "GET", payload: dict[str, Any] | None = None, timeout: int = 30) -> dict[str, Any]:
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    token = os.environ.get("LM_STUDIO_API_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            value = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise ExperimentError(f"LM Studio HTTP {exc.code}: {detail}") from exc
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise ExperimentError(f"LM Studio transport failed: {exc}") from exc
    if not isinstance(value, dict):
        raise ExperimentError("LM Studio returned a non-object response envelope")
    return value


def model_ids(inventory: dict[str, Any]) -> set[str]:
    items = inventory.get("data", inventory.get("models", []))
    if not isinstance(items, list):
        return set()
    result: set[str] = set()
    for item in items:
        if isinstance(item, dict):
            for key in ("id", "key", "model", "identifier"):
                value = item.get(key)
                if isinstance(value, str) and value:
                    result.add(value)
            for instance in item.get("loaded_instances", []):
                if isinstance(instance, dict):
                    for key in ("id", "identifier", "model"):
                        value = instance.get(key)
                        if isinstance(value, str) and value:
                            result.add(value)
    return result


def preflight(
    base_url: str,
    model: str,
    context_length: int | None,
    profile: dict[str, Any],
    guide_manifest: dict[str, Any],
) -> dict[str, Any]:
    if model != EXPECTED_MODEL:
        raise ExperimentError(f"Configured premise model is {model!r}; M1 requires {EXPECTED_MODEL!r}")
    if profile.get("character_profile_used") is not True or profile.get("matched_tag") is None:
        raise ExperimentError(f"Character profile did not resolve safely: {profile.get('reason', 'unknown')}")
    if profile.get("version_match") is not True:
        raise ExperimentError("Character profile did not match the requested version")
    if len(guide_manifest.get("routed_sources", [])) != 4:
        raise ExperimentError("M1 guide routing is incomplete")
    inventory = http_json(f"{base_url}/api/v1/models")
    models = inventory.get("models", [])
    loaded = []
    if isinstance(models, list):
        for item in models:
            if isinstance(item, dict) and item.get("key") == model:
                loaded.extend(instance for instance in item.get("loaded_instances", []) if isinstance(instance, dict))
    if not loaded:
        raise ExperimentError(f"Required LM Studio model is not loaded: {model}")
    loaded_config = loaded[0].get("config", {}) if isinstance(loaded[0], dict) else {}
    loaded_context = loaded_config.get("context_length") if isinstance(loaded_config, dict) else None
    if context_length is not None and loaded_context != context_length:
        raise ExperimentError(
            f"Loaded context is {loaded_context}; configured M1 role requires {context_length}. "
            "Stop instead of allowing prompt truncation to confound the experiment."
        )
    return {
        "passed": True,
        "checked_at": utc_now(),
        "lm_studio_base_url": base_url,
        "model": model,
        "configured_context_length": context_length,
        "loaded_context_length": loaded_context,
        "character_profile_resolved": True,
        "matched_tag": profile["matched_tag"],
        "version_match": profile["version_match"],
        "guide_source_count": len(guide_manifest["routed_sources"]),
        "generation_calls_planned": 1,
        "comfyui_calls_planned": 0,
        "fallback_or_retry_calls_planned": 0,
    }


def native_payload(
    model: str,
    instruction: str,
    *,
    temperature: float,
    max_output_tokens: int,
    reasoning: str | None = "off",
) -> dict[str, Any]:
    payload = {
        "model": model,
        "input": [{"type": "text", "content": instruction}],
        "temperature": temperature,
        "max_output_tokens": max_output_tokens,
        "store": False,
    }
    if reasoning is not None:
        payload["reasoning"] = reasoning
    return payload


def concept_proposal_schema() -> dict[str, Any]:
    """Strict M1→M2 boundary; context never belongs in the response."""
    fields = ["concept_id", "action", "setting", "micro_location", "hook", "camera", "expression"]
    return {"type": "object", "additionalProperties": False, "required": ["concepts"], "properties": {"concepts": {"type": "array", "minItems": EXPECTED_COUNT, "maxItems": EXPECTED_COUNT, "items": {"type": "object", "additionalProperties": False, "required": fields, "properties": {field: {"type": "string"} for field in fields}}}}}
    signature = {
        "type": "object",
        "additionalProperties": False,
        "required": ["setting", "framing", "attitude", "visual_emphasis"],
        "properties": {
            "setting": {"type": "string"}, "framing": {"type": "string"},
            "attitude": {"type": "string"}, "visual_emphasis": {"type": "string"},
        },
    }
    concept = {
        "type": "object",
        "additionalProperties": False,
        "required": ["concept_id", "snapshot", "visual_hook", "provocative_mechanism", "composition_intent", "diversity_signature"],
        "properties": {
            "concept_id": {"type": "string"}, "snapshot": {"type": "string"},
            "visual_hook": {"type": "string"}, "provocative_mechanism": {"type": "string"},
            "composition_intent": {"type": "string"}, "diversity_signature": signature,
        },
    }
    return {
        "type": "object", "additionalProperties": False, "required": ["concepts"],
        "properties": {"concepts": {"type": "array", "minItems": EXPECTED_COUNT, "maxItems": EXPECTED_COUNT, "items": concept}},
    }


def structured_concept_payload(
    model: str, system: str, task: str, *, temperature: float, max_output_tokens: int,
    reasoning: str | None = "off",
) -> dict[str, Any]:
    output_rule = (
        "Use the following context internally. Do not repeat, summarize, quote, or serialize the character profile, "
        "guides, experiment question, rules, or this contract. Your entire response must be one JSON object with only "
        "the top-level key concepts, matching the response schema."
    )
    payload: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": f"{output_rule}\n\nContext:\n{task}"},
        ],
        "temperature": temperature,
        "max_tokens": max_output_tokens,
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": "m1_concept_proposals", "strict": True, "schema": concept_proposal_schema()},
        },
    }
    if reasoning is not None:
        payload["reasoning"] = reasoning
    return payload


def native_content(raw: dict[str, Any]) -> str:
    for item in raw.get("output", []):
        if isinstance(item, dict) and item.get("type") == "message" and isinstance(item.get("content"), str):
            return item["content"].strip()
    raise ExperimentError("LM Studio native response did not contain visible message content")


def chat_completion_content(raw: dict[str, Any]) -> str:
    try:
        content = raw["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ExperimentError("LM Studio structured response did not contain choices[0].message.content") from exc
    if not isinstance(content, str) or not content.strip():
        raise ExperimentError("LM Studio structured response content was empty")
    return content.strip()


def _normalize_json_controls(text: str) -> str:
    """Escape control characters only when they occur inside a JSON string."""
    escaped = False
    in_string = False
    normalized: list[str] = []
    replacements = {"\b": "\\b", "\f": "\\f", "\n": "\\n", "\r": "\\r", "\t": "\\t"}
    for char in text:
        if in_string and ord(char) < 0x20:
            normalized.append(replacements.get(char, f"\\u{ord(char):04x}"))
            continue
        normalized.append(char)
        if char == '"' and not escaped:
            in_string = not in_string
        escaped = char == "\\" and not escaped
        if char != "\\":
            escaped = False
    return "".join(normalized)


def parse_json_object(content: str, *, boundary: str) -> dict[str, Any]:
    """Accept a JSON object wrapped in model prose while keeping the boundary strict."""
    text = content.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else ""
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3]
    start = text.find("{")
    if start < 0:
        raise ExperimentError(f"{boundary} response contains no JSON object")
    try:
        value, _ = json.JSONDecoder().raw_decode(_normalize_json_controls(text[start:]))
    except json.JSONDecodeError as exc:
        raise ExperimentError(f"{boundary} response is not valid JSON after control-character normalization: {exc}") from exc
    if not isinstance(value, dict):
        raise ExperimentError(f"{boundary} response JSON must be an object")
    return value


def execute_once(base_url: str, payload: dict[str, Any], *, endpoint: str = "/api/v1/chat") -> tuple[dict[str, Any], float]:
    started = time.perf_counter()
    raw = http_json(f"{base_url}{endpoint}", method="POST", payload=payload, timeout=900)
    latency = time.perf_counter() - started
    return raw, latency


def validate_structure(value: dict[str, Any], *, character: str) -> None:
    if set(value) != {"concepts"}:
        raise ExperimentError("Output must contain only the top-level concepts field")
    concepts = value.get("concepts")
    if not isinstance(concepts, list) or len(concepts) != EXPECTED_COUNT:
        raise ExperimentError(f"Output must contain exactly {EXPECTED_COUNT} concepts")
    
    compact_fields = {"concept_id", "action", "setting", "micro_location", "hook", "camera", "expression"}
    dataset_fields = {"concept_id", "action", "setting", "micro_location", "camera", "expression", "primary_hook", "context_hook", "micro_story", "animation_beat", "why_it_scroll_stops"}
    
    if all(isinstance(concept, dict) and (set(concept) == compact_fields or set(concept) == dataset_fields) for concept in concepts):
        prefix = concept_id_prefix(character)
        expected_ids = [f"m1_{prefix}_{index:02d}" for index in range(1, EXPECTED_COUNT + 1)]
        if [concept["concept_id"] for concept in concepts] != expected_ids:
            raise ExperimentError(f"Concept IDs must be ordered exactly as {expected_ids}")
        return
    expected_fields = {
        "concept_id", "snapshot", "visual_hook", "provocative_mechanism", "composition_intent", "diversity_signature"
    }
    expected_signature = {"setting", "framing", "attitude", "visual_emphasis"}
    ids: list[str] = []
    for index, concept in enumerate(concepts, 1):
        if not isinstance(concept, dict) or set(concept) != expected_fields:
            raise ExperimentError(f"Concept {index} has invalid fields")
        for field in expected_fields - {"diversity_signature"}:
            if not isinstance(concept[field], str) or not concept[field].strip():
                raise ExperimentError(f"Concept {index}.{field} must be non-empty text")
        signature = concept["diversity_signature"]
        if not isinstance(signature, dict) or set(signature) != expected_signature:
            raise ExperimentError(f"Concept {index}.diversity_signature has invalid fields")
        if any(not isinstance(item, str) or not item.strip() for item in signature.values()):
            raise ExperimentError(f"Concept {index}.diversity_signature values must be non-empty text")
        ids.append(concept["concept_id"])
    prefix = concept_id_prefix(character)
    expected_ids = [f"m1_{prefix}_{index:02d}" for index in range(1, EXPECTED_COUNT + 1)]
    if ids != expected_ids:
        raise ExperimentError(f"Concept IDs must be ordered exactly as {expected_ids}")
def validate_output(value: dict[str, Any], *, character: str) -> None:
    validate_structure(value, character=character)
    leakage = temporal_leakage(value)
    if leakage:
        raise ExperimentError(f"Temporal/video leakage detected: {leakage}")


def concept_text(concept: dict[str, Any]) -> str:
    if "action" in concept:
        return " ".join(str(concept.get(key, "")) for key in ("action", "setting", "micro_location", "hook", "camera", "expression"))
    signature = concept["diversity_signature"]
    return " ".join(
        [concept["snapshot"], concept["visual_hook"], concept["provocative_mechanism"], concept["composition_intent"]]
        + list(signature.values())
    )


def temporal_leakage(value: dict[str, Any]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for concept in value.get("concepts", []):
        text = concept_text(concept)
        for label, pattern in TEMPORAL_PATTERNS:
            match = pattern.search(text)
            if match:
                findings.append({"concept_id": concept.get("concept_id", "?"), "rule": label, "match": match.group(0)})
    return findings


def normalized_tokens(text: str) -> set[str]:
    stop = {"the", "a", "an", "and", "of", "to", "in", "with", "her", "she", "is", "as", "from", "on", "one"}
    return {token for token in re.findall(r"[a-z0-9]+", text.lower()) if len(token) > 2 and token not in stop}


def diversity_diagnostics(value: dict[str, Any]) -> dict[str, Any]:
    concepts = value["concepts"]
    if concepts and "action" in concepts[0]:
        dimensions = ("setting", "camera", "expression", "hook")
        return {
            "count": len(concepts),
            "unique_signature_values": {dimension: len({str(concept[dimension]).strip().casefold() for concept in concepts}) for dimension in dimensions},
            "exact_duplicate_snapshots": len({item["action"].strip().casefold() for item in concepts}) != len(concepts),
            "potentially_similar_pairs": [],
            "temporal_leakage": temporal_leakage(value),
        }
    dimensions = ("setting", "framing", "attitude", "visual_emphasis")
    unique_values = {
        dimension: len({concept["diversity_signature"][dimension].strip().casefold() for concept in concepts})
        for dimension in dimensions
    }
    similar_pairs: list[dict[str, Any]] = []
    for left_index, left in enumerate(concepts):
        left_tokens = normalized_tokens(concept_text(left))
        for right in concepts[left_index + 1:]:
            right_tokens = normalized_tokens(concept_text(right))
            union = left_tokens | right_tokens
            similarity = len(left_tokens & right_tokens) / len(union) if union else 1.0
            if similarity >= 0.45:
                similar_pairs.append({
                    "left": left["concept_id"], "right": right["concept_id"], "token_jaccard": round(similarity, 3)
                })
    return {
        "count": len(concepts),
        "unique_signature_values": unique_values,
        "exact_duplicate_snapshots": len({item["snapshot"].strip().casefold() for item in concepts}) != len(concepts),
        "potentially_similar_pairs": similar_pairs,
        "temporal_leakage": temporal_leakage(value),
    }


def telemetry(raw: dict[str, Any], latency: float) -> dict[str, Any]:
    stats = raw.get("stats", {}) if isinstance(raw.get("stats"), dict) else {}
    return {
        "model": raw.get("model_instance_id", raw.get("model")),
        "latency_seconds": round(latency, 3),
        "finish_reason": raw.get("stop_reason"),
        "usage": raw.get("usage", stats),
        "generation_calls": 1,
        "fallback_calls": 0,
        "retry_calls": 0,
        "comfyui_calls": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--character", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--max-tokens", type=int, default=1200)
    args = parser.parse_args()

    run_id = args.run_id or f"m1_{concept_id_prefix(args.character)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}", run_id):
        raise ExperimentError("run-id must be a safe 1-80 character identifier")
    run_dir = RUNS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    started_at = utc_now()
    profile = CharacterProfileDatabase().get_character_profile(args.character, args.version)
    guide_context, guide_manifest = source_context()
    controller = LMStudioController()
    # Creative Expansion is not yet a production specialist role. Reuse the
    # current production Master model/configuration without adding a new route.
    role = controller.role("master")
    system, task = build_prompts(args.character, args.version, profile, guide_context)

    write_json_new(run_dir / "character_profile.json", profile)
    write_json_new(run_dir / "guide_context.json", {"manifest": guide_manifest, "excerpts": guide_context})
    try:
        preflight_result = preflight(controller.base_url, role.model, role.context_length, profile, guide_manifest)
        write_json_new(run_dir / "preflight.json", preflight_result)

        smoke_payload = native_payload(
            role.model,
            "This is a non-creative LM Studio transport check. Return exactly the visible text READY and nothing else.",
            temperature=0.0,
            max_output_tokens=32,
        )
        write_json_new(run_dir / "transport_smoke_request.json", smoke_payload)
        smoke_raw, smoke_latency = execute_once(controller.base_url, smoke_payload)
        write_json_new(run_dir / "transport_smoke_raw_response.json", smoke_raw)
        smoke_content = native_content(smoke_raw)
        if not smoke_content:
            raise ExperimentError("Native transport smoke test returned empty visible content")
        write_json_new(run_dir / "transport_smoke.json", {
            "passed": True,
            "visible_content": smoke_content,
            "telemetry": telemetry(smoke_raw, smoke_latency),
        })

        request_payload = native_payload(role.model, system + "\n\n" + task, temperature=0.8, max_output_tokens=args.max_tokens)
        write_json_new(run_dir / "model_request.json", request_payload)
        raw, latency = execute_once(controller.base_url, request_payload)
        write_json_new(run_dir / "raw_model_response.json", raw)
        content = native_content(raw)
        output = json.loads(content)
        validate_output(output, character=args.character)
        diagnostics = diversity_diagnostics(output)
        write_json_new(run_dir / "concept_proposals.json", output)
        write_json_new(run_dir / "validation.json", {"valid": True, **diagnostics})
        write_json_new(run_dir / "telemetry.json", telemetry(raw, latency))
        manifest = {
            "experiment": "M1 — Creative Expansion Lab",
            "status": "VALID",
            "text_only": True,
            "pre_premise_spec": True,
            "character": args.character,
            "version": args.version,
            "model": role.model,
            "count": len(output["concepts"]),
            "started_at": started_at,
            "completed_at": utc_now(),
            "generation_calls": 1,
            "transport_smoke_calls": 1,
            "comfyui_executed": False,
            "minimax_executed": False,
            "production_pipeline_modified": False,
            "artifacts": {path.stem: str(path.resolve()) for path in sorted(run_dir.iterdir())},
        }
        write_json_new(run_dir / "manifest.json", manifest)
    except Exception as exc:
        # Raw output is written before parsing/validation whenever transport
        # produced a response. This record makes the terminal failure explicit.
        failure = {
            "experiment": "M1 — Creative Expansion Lab",
            "status": "INVALID_STOPPED",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "started_at": started_at,
            "stopped_at": utc_now(),
            "generation_calls_at_most": 1,
            "transport_smoke_calls_at_most": 1,
            "retry_calls": 0,
            "fallback_calls": 0,
            "comfyui_executed": False,
        }
        write_json_new(run_dir / "failure.json", failure)
        raise

    print(json.dumps({"status": "VALID", "run_dir": str(run_dir.resolve()), "count": EXPECTED_COUNT}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"M1 stopped: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1)
