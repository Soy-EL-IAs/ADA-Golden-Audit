"""Versioned semantic artifacts between ADA's creative, render, and review stages."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from scripts.agent_contracts import validate_contract
from ada_app.creative_intent import environment_anchors, locked_value


def _clean_strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    seen: set[str] = set()
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            continue
        cleaned = item.strip()
        key = cleaned.casefold()
        if key not in seen:
            seen.add(key)
            result.append(cleaned)
    return result


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_")
    if not slug:
        raise ValueError("Character Contract requires a usable character identifier")
    return slug


def _first_text(*values: Any) -> str:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


_RELATIONAL_ACTION = re.compile(
    r"\b(shares?|talks?|converses?|chats?|meets?|hands?|gives?|offers?|serves?)\b.*\b(with|to)\b|\bwith\s+(a\s+)?(friend|person|someone|companion)\b",
    re.IGNORECASE,
)


def implies_additional_subject(action: str) -> bool:
    """Return true when a nominally single-subject action requests a partner."""
    return isinstance(action, str) and bool(_RELATIONAL_ACTION.search(action))


def normalize_single_subject_action(action: str) -> str:
    """Remove accidental relational wording from generated, non-locked sketches."""
    value = action.strip() if isinstance(action, str) else ""
    if not implies_additional_subject(value):
        return value
    share = re.search(r"\bshares?\s+(.+?)\s+with\b", value, flags=re.IGNORECASE)
    if share:
        subject = share.group(1).split(" and ", 1)[0].strip()
        prefix = value[:share.start()].strip()
        return " ".join(part for part in [prefix, "holds", subject, "alone"] if part)
    transfer = re.search(r"\b(?:hands?|gives?|offers?|serves?)\s+(.+?)\s+to\b", value, flags=re.IGNORECASE)
    if transfer:
        prefix = value[:transfer.start()].strip()
        return " ".join(part for part in [prefix, "holds", transfer.group(1).strip(), "alone"] if part)
    prefix = re.split(r"\b(?:talks?|converses?|chats?|meets?)\b", value, maxsplit=1, flags=re.IGNORECASE)[0].strip()
    return " ".join(part for part in [prefix, "sits alone"] if part) or "sits alone"


def build_character_contract(
    profile: dict[str, Any], registry_entry: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Resolve profile/registry evidence without converting it directly into a prompt."""
    registry = registry_entry or {}
    display_name = _first_text(profile.get("requested_character"), profile.get("name"), registry.get("name"))
    if not display_name:
        raise ValueError("Character Contract requires an explicit character name")

    canonical_tag = _first_text(profile.get("matched_tag"), profile.get("canonical_tag"), registry.get("canonical_tag"))
    character_id = _slug(canonical_tag or display_name)
    refs_manifest = _first_text(profile.get("refs_manifest"), registry.get("refs_manifest"))
    manifest_version = ""
    if refs_manifest:
        manifest_path = Path(refs_manifest)
        if manifest_path.name.casefold() == "manifest.json" and manifest_path.parent.name:
            manifest_version = manifest_path.parent.name
    profile_version = _first_text(
        profile.get("requested_version"), profile.get("version"), registry.get("version"), manifest_version, "unversioned"
    )
    classification = profile.get("taxonomy_classification") if isinstance(profile.get("taxonomy_classification"), dict) else {}
    characteristics = _clean_strings([
        *(classification.get("IDENTITY", []) if isinstance(classification.get("IDENTITY", []), list) else []),
        *(classification.get("CANONICAL_APPEARANCE", []) if isinstance(classification.get("CANONICAL_APPEARANCE", []), list) else []),
        *(classification.get("ACCESSORY", []) if isinstance(classification.get("ACCESSORY", []), list) else []),
    ]) or _clean_strings(profile.get("characteristics") or registry.get("characteristics"))
    clothing = _clean_strings(classification.get("CANONICAL_OUTFIT", [])) or _clean_strings(profile.get("clothing") or registry.get("clothing"))
    franchise = _clean_strings(profile.get("copyright") or registry.get("copyright"))
    if not franchise:
        one_franchise = _first_text(registry.get("franchise"), registry.get("universe"))
        franchise = [one_franchise] if one_franchise else []

    anchors = _clean_strings([display_name, canonical_tag, *characteristics])
    evidence = [{
        "source": _first_text(profile.get("source"), "character_registry"),
        "reference": canonical_tag,
        "supports": ["identity", "outfit"],
    }]
    if refs_manifest:
        evidence.append({"source": "character_refs_manifest", "reference": refs_manifest, "supports": ["visual_reference"]})
    if profile.get("taxonomy_evidence"):
        evidence.append({"source": "danbooru_taxonomy", "reference": canonical_tag, "supports": ["identity_taxonomy"]})

    contract = {
        "schema_version": "character_contract_v1",
        "contract_id": f"character:{character_id}:{_slug(profile_version)}",
        "character_id": character_id,
        "display_name": display_name,
        "profile_version": profile_version,
        "franchise": franchise,
        "identity": {
            "canonical_tag": canonical_tag,
            "must_preserve": anchors,
            "valid_variants": [],
            "conditional": [],
            "uncertain": [],
        },
        "outfit": {
            "canonical_default": clothing,
            "valid_variants": [],
            "conditional": [],
            "uncertain": [],
        },
        "evidence": evidence,
        "source_profile": profile,
    }
    return validate_contract("character_contract_v1", contract)


def build_resolved_render_spec(
    character_contract: dict[str, Any], concept_id: str, proposal: dict[str, Any]
) -> dict[str, Any]:
    """Resolve character + creative intent into one model-agnostic render specification."""
    if not concept_id.strip():
        raise ValueError("Resolved Render Spec requires a concept id")
    identity = character_contract["identity"]
    outfit = character_contract["outfit"]
    composition = _first_text(proposal.get("composition_intent"))
    scene = _clean_strings([
        proposal.get("provocative_mechanism"),
        proposal.get("diversity_signature", {}).get("visual_emphasis")
        if isinstance(proposal.get("diversity_signature"), dict) else "",
    ])
    requirements: list[dict[str, str]] = [
        {
            "requirement_id": "identity:canonical",
            "category": "identity",
            "statement": f"Preserve the identity of {character_contract['display_name']}",
            "applicability": "REQUIRED",
        }
    ]
    for index, item in enumerate(outfit["canonical_default"], start=1):
        requirements.append({
            "requirement_id": f"outfit:{index:02d}",
            "category": "outfit",
            "statement": item,
            "applicability": "IF_VISIBLE",
        })
    for index, item in enumerate(scene, start=1):
        requirements.append({
            "requirement_id": f"scene:{index:02d}",
            "category": "scene",
            "statement": item,
            "applicability": "REQUIRED",
        })
    if composition:
        requirements.append({
            "requirement_id": "composition:01",
            "category": "composition",
            "statement": composition,
            "applicability": "REQUIRED",
        })

    spec = {
        "schema_version": "resolved_render_spec_v1",
        "spec_id": f"render-spec:{concept_id}:v1",
        "character_contract_id": character_contract["contract_id"],
        "concept_id": concept_id,
        "character": {
            "display_name": character_contract["display_name"],
            "canonical_tag": identity["canonical_tag"],
            "must_preserve": identity["must_preserve"],
        },
        "concept": {
            "snapshot": _first_text(proposal.get("snapshot")),
            "visual_hook": _first_text(proposal.get("visual_hook")),
            "provocative_mechanism": _first_text(proposal.get("provocative_mechanism")),
            "diversity_signature": proposal.get("diversity_signature", {})
            if isinstance(proposal.get("diversity_signature"), dict) else {},
        },
        "outfit": {
            "mode": "canonical_default",
            "required_if_visible": outfit["canonical_default"],
            "valid_variants": outfit["valid_variants"],
        },
        "scene_requirements": scene,
        "composition_intent": composition,
        "validation_requirements": requirements,
        "risk_notes": ["Prevent structural collapse"],
        "render_policy_version": "render_policy_v1",
    }
    return validate_contract("resolved_render_spec_v1", spec)


def build_hook_premise_v2(proposal: dict[str, Any], concept_id: str, *, render_intent: str = "semi_realistic") -> dict[str, Any]:
    """Normalize M2 intent into a model-neutral visual moment, never a prompt."""
    if render_intent not in {"anime", "semi_realistic", "photorealistic"}:
        raise ValueError("Unsupported render intent")
    diversity = proposal.get("diversity_signature", {}) if isinstance(proposal.get("diversity_signature"), dict) else {}
    hook = {
        "schema_version": "hook_premise_v2",
        "hook_id": f"hook:{concept_id}:v2",
        "hook_type": _first_text(proposal.get("hook_type"), diversity.get("setting"), "everyday_moment").casefold().replace(" ", "_"),
        "snapshot": _first_text(proposal.get("snapshot")),
        "core_action": _first_text(proposal.get("core_action"), proposal.get("provocative_mechanism")),
        "visual_hook": _first_text(proposal.get("visual_hook")),
        "provocative_mechanism": _first_text(proposal.get("provocative_mechanism")),
        "object_interaction": _first_text(proposal.get("object_interaction")),
        "setting": _first_text(proposal.get("setting"), diversity.get("setting")),
        "composition_intent": _first_text(proposal.get("composition_intent"), diversity.get("framing")),
        "expression": _first_text(proposal.get("expression"), diversity.get("attitude")),
        "render_intent": render_intent,
    }
    return validate_contract("hook_premise_v2", hook)


def build_resolved_render_spec_v2(character_contract: dict[str, Any], concept_id: str, proposal: dict[str, Any], *, render_intent: str = "semi_realistic", render_mode: str = "DIRECT_T2I") -> dict[str, Any]:
    """Current semantic source for renderer-specific compilers; v1 remains readable."""
    if render_mode not in ("DIRECT_T2I", "LATENT_IMG2IMG"):
        raise ValueError(f"Render mode {render_mode} is not currently supported")
    v1 = build_resolved_render_spec(character_contract, concept_id, proposal)
    hook = build_hook_premise_v2(proposal, concept_id, render_intent=render_intent)
    value = {
        "schema_version": "resolved_render_spec_v2", "spec_id": f"render-spec:{concept_id}:v2",
        "character_contract_id": character_contract["contract_id"], "concept_id": concept_id,
        "character": v1["character"], "hook_premise": hook, "outfit": v1["outfit"],
        "scene_requirements": v1["scene_requirements"], "composition_intent": v1["composition_intent"],
        "validation_requirements": v1["validation_requirements"], "risk_notes": v1["risk_notes"],
        "render_intent": render_intent, "render_mode": render_mode, "render_policy_version": "render_policy_v2",
    }
    return validate_contract("resolved_render_spec_v2", value)


class ConstraintViolation(ValueError):
    """A deterministic contradiction between Create and a resolved render spec."""


def expand_compact_sketch(sketch: dict[str, Any]) -> dict[str, Any]:
    """Expand only a selected compact M1 sketch into the legacy premise vocabulary."""
    action = _first_text(sketch.get("action"))
    micro_location = _first_text(sketch.get("micro_location"))
    hook = _first_text(sketch.get("hook"))
    camera = _first_text(sketch.get("camera"))
    expression = _first_text(sketch.get("expression"))
    setting = _first_text(sketch.get("setting"))
    snapshot = ", ".join(part for part in [action, micro_location] if part)
    return {
        "concept_id": _first_text(sketch.get("concept_id")),
        "snapshot": snapshot,
        "visual_hook": hook,
        "provocative_mechanism": hook,
        "composition_intent": camera,
        "diversity_signature": {"setting": setting, "framing": camera, "attitude": expression, "visual_emphasis": hook},
        "setting": setting,
        "micro_location": micro_location,
        "core_action": action,
        "expression": expression,
    }


def expected_visibility(render_spec: dict[str, Any]) -> list[str]:
    composition = _first_text(render_spec.get("composition_intent"), render_spec.get("hook_premise", {}).get("composition_intent")).casefold()
    character = render_spec.get("character", {}) if isinstance(render_spec.get("character"), dict) else {}
    identity_anchors = _clean_strings(character.get("must_preserve"))
    priorities = ("eyepatch", "blindfold", "skin", "grey_hair", "white_hair", "purple_hair", "red_eyes", "yellow_eyes", "cat_ears", "ears", "tattoo", "hair", "tail")
    distinctive = [item for item in identity_anchors if any(word in item.casefold() for word in priorities)]
    distinctive.sort(key=lambda item: next((index for index, key in enumerate(priorities) if key in item.casefold()), len(priorities)))
    upper_crop = any(marker in composition.replace("_", " ") for marker in ("close-up", "close up", "portrait", "upper body", "torso", "chest", "head"))
    if upper_crop:
        distinctive = [item for item in distinctive if "tail" not in item.casefold()]
    visible = ["face", *(distinctive[:6] or identity_anchors[:2])]
    outfit = _clean_strings(render_spec.get("outfit", {}).get("required_if_visible"))
    if upper_crop:
        outfit = [item for item in outfit if not any(marker in item.casefold() for marker in ("pant", "boot", "thigh", "leg", "shoe", "skirt", "stocking"))]
    visible.extend(outfit[:4])
    hook = render_spec.get("hook_premise", {}) if isinstance(render_spec.get("hook_premise"), dict) else {}
    visible.extend(_clean_strings([hook.get("core_action"), hook.get("setting")]))
    return _clean_strings(visible)


def build_resolved_render_spec_v3(character_contract: dict[str, Any], concept_id: str, proposal: dict[str, Any], *, creative_intent: dict[str, Any] | None = None, render_intent: str = "semi_realistic", render_mode: str = "DIRECT_T2I") -> dict[str, Any]:
    """Deterministically merge locked Create intent above concept creativity."""
    intent = creative_intent or {}
    expanded = expand_compact_sketch(proposal) if "action" in proposal else dict(proposal)
    locked_character = locked_value(intent, "character")
    if locked_character and locked_character.casefold() != character_contract["display_name"].casefold():
        raise ConstraintViolation("Locked character does not match the Character Contract")
    locked_setting = locked_value(intent, "setting")
    locked_action = locked_value(intent, "action")
    locked_render_intent = locked_value(intent, "render_intent")
    if locked_setting:
        expanded["setting"] = locked_setting
        expanded["diversity_signature"]["setting"] = locked_setting
    if locked_action:
        if implies_additional_subject(locked_action):
            raise ConstraintViolation("Single-subject Scene cannot use a relational action that implies another person")
        expanded["core_action"] = locked_action
        expanded["provocative_mechanism"] = locked_action
        expanded["snapshot"] = ", ".join(part for part in [locked_action, _first_text(expanded.get("micro_location"))] if part)
    elif implies_additional_subject(_first_text(expanded.get("core_action"), expanded.get("action"))):
        safe_action = normalize_single_subject_action(_first_text(expanded.get("core_action"), expanded.get("action")))
        expanded["core_action"] = safe_action
        expanded["provocative_mechanism"] = safe_action
        expanded["snapshot"] = ", ".join(part for part in [safe_action, _first_text(expanded.get("micro_location"))] if part)
    effective_intent = locked_render_intent or render_intent
    v2 = build_resolved_render_spec_v2(character_contract, concept_id, expanded, render_intent=effective_intent, render_mode=render_mode)
    hook = dict(v2["hook_premise"])
    hook["setting"] = _first_text(locked_setting, hook.get("setting"))
    hook["core_action"] = _first_text(locked_action, hook.get("core_action"))
    anchors = environment_anchors(hook["setting"]) if isinstance(intent.get("setting"), dict) and intent["setting"].get("must_be_visible") else []
    value = {**v2, "schema_version": "resolved_render_spec_v3", "spec_id": f"render-spec:{concept_id}:v3", "hook_premise": hook,
             "scene_requirements": _clean_strings([hook["setting"], *anchors, *v2["scene_requirements"]]),
             "creative_intent": intent, "environment_anchors": anchors, "render_policy_version": "render_policy_v3", "expected_subject_count": 1}
    value["validation_requirements"].append({"requirement_id": "subject_count:01", "category": "composition", "statement": "Exactly one main person", "applicability": "REQUIRED"})
    value["expected_visibility"] = expected_visibility(value)
    lint_resolved_render_spec(value)
    return validate_contract("resolved_render_spec_v3", value)


def build_stock_render_spec(
    character_contract: dict[str, Any], concept_id: str, *,
    outfit_override: str | None = None, render_intent: str = "semi_realistic",
) -> dict[str, Any]:
    """Resolve a non-narrative Stock request without a premise or scene fields."""
    if not isinstance(concept_id, str) or not concept_id.strip():
        raise ValueError("Stock Render Spec requires a concept id")
    override = outfit_override.strip() if isinstance(outfit_override, str) else ""
    identity = character_contract["identity"]
    canonical_outfit = _clean_strings(character_contract["outfit"].get("canonical_default"))
    resolved_outfit = [override] if override else canonical_outfit
    composition = "Full-body or three-quarter body, slight natural three-quarter angle, looking generally toward camera, neutral relaxed standing pose"
    requirements: list[dict[str, str]] = [
        {"requirement_id": "identity:canonical", "category": "identity", "statement": f"Preserve the identity of {character_contract['display_name']}", "applicability": "REQUIRED"},
        {"requirement_id": "stock:white_background", "category": "composition", "statement": "Pure seamless white background with no environment or scenery", "applicability": "REQUIRED"},
        {"requirement_id": "stock:one_character", "category": "composition", "statement": "Exactly one character and no other people", "applicability": "REQUIRED"},
        {"requirement_id": "stock:canonical_attire", "category": "outfit", "statement": "Canonical signature attire with no unintended nudity", "applicability": "REQUIRED"},
        {"requirement_id": "stock:composition", "category": "composition", "statement": composition, "applicability": "REQUIRED"},
    ]
    if override:
        requirements.append({"requirement_id": "outfit:override", "category": "outfit", "statement": override, "applicability": "REQUIRED"})
    else:
        requirements.extend(
            {"requirement_id": f"outfit:{index:02d}", "category": "outfit", "statement": item, "applicability": "IF_VISIBLE"}
            for index, item in enumerate(canonical_outfit, start=1)
        )
    value: dict[str, Any] = {
        "schema_version": "resolved_render_spec_stock_v1",
        "spec_id": f"render-spec:{concept_id}:stock:v1",
        "character_contract_id": character_contract["contract_id"],
        "concept_id": concept_id,
        "creation_mode": "stock",
        "character_id": character_contract["character_id"],
        "character": {
            "display_name": character_contract["display_name"],
            "canonical_tag": identity["canonical_tag"],
            "must_preserve": identity["must_preserve"],
        },
        "outfit": {
            "mode": "override" if override else "canonical_default",
            "required_if_visible": resolved_outfit,
            "valid_variants": [] if override else character_contract["outfit"].get("valid_variants", []),
        },
        "stock_policy_version": "stock_v1",
        "stock_render_policy": {
            "subject_count": 1,
            "background": "pure seamless white",
            "environment": "none",
            "props": "none",
            "other_people": "none",
            "lighting": "clean studio lighting",
            "pose": "natural neutral standing pose",
            "face": "clear and unobstructed",
            "hands": "visible when reasonable",
            "text_and_logos": "none",
        },
        "scene_requirements": [],
        "composition_intent": composition,
        "validation_requirements": requirements,
        "risk_notes": ["Prevent structural collapse", "Reject multiple people", "Reject non-white or complex backgrounds"],
        "render_intent": render_intent,
        "render_mode": "DIRECT_T2I",
        "render_policy_version": "stock_v1",
        "environment_anchors": [],
        "expected_visibility": _clean_strings(["face", *identity["must_preserve"], *resolved_outfit, "hands when reasonably framed"]),
        "expected_subject_count": 1,
    }
    if override:
        value["outfit_override"] = override
    return validate_contract("resolved_render_spec_stock_v1", value)


def lint_resolved_render_spec(spec: dict[str, Any]) -> None:
    """Cheap pre-render guard; violations never spend a renderer retry."""
    intent = spec.get("creative_intent", {}) if isinstance(spec.get("creative_intent"), dict) else {}
    hook = spec.get("hook_premise", {}) if isinstance(spec.get("hook_premise"), dict) else {}
    setting = locked_value(intent, "setting")
    if setting and hook.get("setting", "").casefold() != setting.casefold():
        raise ConstraintViolation("Locked setting was not preserved")
    if setting and intent.get("setting", {}).get("must_be_visible") and not spec.get("environment_anchors"):
        raise ConstraintViolation("Locked visible setting requires environmental anchors")
    required_intent = locked_value(intent, "render_intent")
    if required_intent and spec.get("render_intent") != required_intent:
        raise ConstraintViolation("Locked render intent was not preserved")
    character = locked_value(intent, "character")
    if character and spec.get("character", {}).get("display_name", "").casefold() != character.casefold():
        raise ConstraintViolation("Locked character was not preserved")


def render_spec_to_premise_spec(render_spec: dict[str, Any]) -> dict[str, Any]:
    """Compatibility adapter for persisted specialist_image_v1 Missions."""
    return {
        "id": render_spec["concept_id"],
        "category": "Creative Expansion",
        "premise": render_spec["concept"]["snapshot"],
        "identity_elements": render_spec["character"]["must_preserve"],
        "canonical_outfit": render_spec["outfit"]["required_if_visible"],
        "scene_requirements": render_spec["scene_requirements"] + (
            [render_spec["composition_intent"]] if render_spec["composition_intent"] else []
        ),
        "risk_notes": render_spec["risk_notes"],
    }


def build_stage_render_plan(
    render_spec: dict[str, Any], stage: str, attempt: int,
    correction_delta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    stage = stage.casefold()
    profiles = {
        "illustrious": ("illustrious_constructor_v1", "construct the resolved image", "none", "illustrious_stage_compiler_v1"),
        "klein": ("klein_finalizer_v1", "finalize the source image without reinterpretation", "preserve", "klein_stage_compiler_v1"),
        "lustify": ("lustify_krea2_general_renderer_v1", "directly render the resolved image", "none", "lustify_stage_compiler_v1"),
        "miaomiao": ("miaomiao_anima16_fast_anime_renderer_v1", "directly render the resolved image", "none", "miaomiao_stage_compiler_v1"),
    }
    if stage not in profiles:
        raise ValueError(f"Unsupported render stage: {stage}")
    capability_profile, task, source_image_mode, compiler_version = profiles[stage]
    correction = correction_delta or {}
    concept = render_spec.get("concept")
    if render_spec.get("creation_mode") == "stock":
        concept = {
            "snapshot": "",
            "visual_hook": "",
            "provocative_mechanism": "",
            "diversity_signature": {},
        }
    if not isinstance(concept, dict):
        hook = render_spec.get("hook_premise", {}) if isinstance(render_spec.get("hook_premise"), dict) else {}
        concept = {
            "snapshot": _first_text(hook.get("snapshot")),
            "visual_hook": _first_text(hook.get("visual_hook")),
            "provocative_mechanism": _first_text(hook.get("provocative_mechanism"), hook.get("core_action")),
            "diversity_signature": {},
        }
    plan = {
        "schema_version": "stage_render_plan_v1",
        "plan_id": f"stage-plan:{render_spec['concept_id']}:{stage}:{attempt:02d}",
        "render_spec_id": render_spec["spec_id"],
        "stage": stage,
        "attempt": attempt,
        "capability_profile": capability_profile,
        "task": task,
        "concept_intent": concept,
        "identity": {
            "display_name": render_spec["character"]["display_name"],
            "canonical_tag": render_spec["character"]["canonical_tag"],
            "anchors": render_spec["character"]["must_preserve"],
        },
        "outfit_constraints": render_spec["outfit"]["required_if_visible"],
        "scene_constraints": render_spec["scene_requirements"],
        "composition_intent": render_spec["composition_intent"],
        "risk_notes": render_spec["risk_notes"],
        "source_image_mode": source_image_mode,
        "correction_delta": {
            "source_decision_id": _first_text(correction.get("source_decision_id"), correction.get("decision_id")),
            "instructions": _clean_strings(correction.get("instructions")),
        },
        "compiler_version": compiler_version,
    }
    return validate_contract("stage_render_plan_v1", plan)


def build_prompt_artifact(stage_plan: dict[str, Any], positive_prompt: str, negative_prompt: str = "") -> dict[str, Any]:
    artifact = {
        "schema_version": "prompt_artifact_v1",
        "prompt_id": f"prompt:{stage_plan['plan_id']}",
        "stage_render_plan_id": stage_plan["plan_id"],
        "stage": stage_plan["stage"],
        "attempt": stage_plan["attempt"],
        "compiler_version": stage_plan["compiler_version"],
        "positive_prompt": positive_prompt.strip(),
        "negative_prompt": negative_prompt.strip(),
    }
    return validate_contract("prompt_artifact_v1", artifact)


def build_render_receipt(
    *, render_spec: dict[str, Any], stage_plan: dict[str, Any], prompt_artifact: dict[str, Any],
    workflow: str, generation: dict[str, Any], submission: dict[str, Any], output_asset: str,
) -> dict[str, Any]:
    receipt = {
        "schema_version": "render_receipt_v1",
        "receipt_id": f"render:{stage_plan['plan_id']}",
        "stage": stage_plan["stage"],
        "attempt": stage_plan["attempt"],
        "render_spec_id": render_spec["spec_id"],
        "stage_render_plan_id": stage_plan["plan_id"],
        "prompt_artifact_id": prompt_artifact["prompt_id"],
        "workflow": workflow,
        "generation": generation,
        "submission": submission,
        "output_asset": output_asset,
    }
    return validate_contract("render_receipt_v1", receipt)


def build_review_observation(
    review: dict[str, Any], render_spec: dict[str, Any], stage: str, attempt: int
) -> dict[str, Any]:
    if isinstance(review.get("agent_scores"), dict):
        observation = {
            "schema_version": "review_observation_v2",
            "observation_id": f"observation:{render_spec['concept_id']}:{stage}:{attempt:02d}",
            "render_spec_id": render_spec["spec_id"], "stage": stage, "attempt": attempt,
            "expected_visibility": _clean_strings(render_spec.get("expected_visibility")),
            "identity_failures": _clean_strings(review.get("identity_failures")),
            "defects": _clean_strings(review.get("defects")),
            "hard_constraint_failures": _clean_strings(review.get("hard_constraint_failures")),
            "summary": _first_text(review.get("summary")),
            "source_review_verdict": _first_text(review.get("verdict"), "FAIL"),
            "agent_scores": review["agent_scores"], "agent_rating": float(review["agent_rating"]),
        }
        return validate_contract("review_observation_v2", observation)
    requirements = []
    defects = _clean_strings(review.get("defects"))
    drift = _clean_strings(review.get("drift"))
    reviewed_requirements = {
        item.get("requirement_id"): item
        for item in review.get("requirements", [])
        if isinstance(item, dict) and isinstance(item.get("requirement_id"), str)
    }
    for requirement in render_spec["validation_requirements"]:
        category = requirement["category"]
        reviewed = reviewed_requirements.get(requirement["requirement_id"])
        if reviewed:
            result = reviewed.get("result", "UNKNOWN")
            evidence = _clean_strings(reviewed.get("evidence"))
        elif category == "identity":
            confirmed = bool(review.get("preserved_ok")) or bool(review.get("identity_ok"))
            result = "PASS" if confirmed or review.get("verdict") == "PASS" else "UNKNOWN"
            evidence = []
        elif category == "scene":
            confirmed = bool(review.get("scene_requirements_ok"))
            result = "PASS" if confirmed or review.get("verdict") == "PASS" else "UNKNOWN"
            evidence = []
        else:
            result = "UNKNOWN"
            evidence = []
        requirements.append({
            "requirement_id": requirement["requirement_id"],
            "category": category,
            "result": result,
            "evidence": evidence or (defects + drift if result == "FAIL" else []),
        })
    observation = {
        "schema_version": "review_observation_v1",
        "observation_id": f"observation:{render_spec['concept_id']}:{stage}:{attempt:02d}",
        "render_spec_id": render_spec["spec_id"],
        "stage": stage,
        "attempt": attempt,
        "requirements": requirements,
        "defects": defects,
        "drift": drift,
        "summary": _first_text(review.get("summary")),
        "source_review_verdict": _first_text(review.get("verdict"), "REJECT"),
    }
    rating = review.get("agent_rating")
    if not isinstance(rating, bool) and isinstance(rating, (int, float)) and 1 <= float(rating) <= 10:
        observation["agent_rating"] = float(rating)
    return validate_contract("review_observation_v1", observation)


def build_routing_decision(observation: dict[str, Any], action: str) -> dict[str, Any]:
    target_stage = {
        "ADVANCE_TO_KLEIN": "klein",
        "RETRY_ILLUSTRIOUS": "illustrious",
        "RETRY_KLEIN": "klein",
    }.get(action, "none")
    instructions = _clean_strings(observation.get("defects")) + _clean_strings(observation.get("drift"))
    decision = {
        "schema_version": "routing_decision_v1",
        "decision_id": f"decision:{observation['observation_id']}",
        "observation_id": observation["observation_id"],
        "stage": observation["stage"],
        "attempt": observation["attempt"],
        "action": action,
        "reason": observation["summary"],
        "correction_delta": {"target_stage": target_stage, "instructions": _clean_strings(instructions)},
        "routing_policy_version": "quality_router_v1",
    }
    return validate_contract("routing_decision_v1", decision)
