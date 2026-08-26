"""Renderer-specific prompt compilation from semantic specs, not shared prompt text."""
from __future__ import annotations

from typing import Any

from scripts.agent_contracts import validate_contract
from ada_app.semantic_contracts import normalize_single_subject_action


SUPPORTED_MODES = {"DIRECT_T2I", "LATENT_IMG2IMG", "REFERENCE_EDIT", "STYLE_REFERENCE", "STRUCTURE_CONTROL"}
SUPPORTED_T2I = {"DIRECT_T2I"}


def _items(value: Any) -> str:
    return ", ".join(str(item).strip() for item in value if isinstance(item, str) and item.strip()) if isinstance(value, list) else ""


def _identity_cues(identity: dict[str, Any]) -> str:
    name = str(identity.get("display_name", "")).casefold().replace(" ", "_")
    canonical = str(identity.get("canonical_tag", "")).casefold()
    anchors = [item for item in identity.get("must_preserve", identity.get("anchors", [])) if isinstance(item, str)]
    anchors = [item for item in anchors if item.casefold().replace(" ", "_") not in {name, canonical}]
    priorities = ("eyepatch", "blindfold", "skin", "grey_hair", "white_hair", "purple_hair", "red_eyes", "yellow_eyes", "cat_ears", "ears", "tattoo", "cat_tail", "tail", "hair")
    anchors.sort(key=lambda item: next((index for index, key in enumerate(priorities) if key in item.casefold()), len(priorities)))
    return ", ".join(item.replace("_", " ") for item in anchors[:6])


def _visible_outfit(outfit: dict[str, Any], composition: str) -> str:
    items = [item for item in outfit.get("required_if_visible", outfit.get("canonical_default", [])) if isinstance(item, str)]
    framing = composition.casefold().replace("_", " ")
    if any(marker in framing for marker in ("close-up", "close up", "portrait", "upper body", "torso", "chest", "head")):
        hidden = ("pant", "boot", "thigh", "leg", "shoe", "skirt", "stocking")
        items = [item for item in items if not any(marker in item.casefold() for marker in hidden)]
    return ", ".join(item.replace("_", " ") for item in items[:4])


def _semantic(spec: dict[str, Any]) -> dict[str, str]:
    hook = spec.get("hook_premise", spec.get("concept", {}))
    identity = spec.get("character", {})
    outfit = spec.get("outfit", {})
    composition = str(hook.get("composition_intent", spec.get("composition_intent", "")))
    action = str(hook.get("core_action", hook.get("provocative_mechanism", ""))).replace("_", " ")
    if int(spec.get("expected_subject_count", 1) or 1) == 1:
        action = normalize_single_subject_action(action)
    return {"name": str(identity.get("display_name", "")), "anchors": _identity_cues(identity), "outfit": _visible_outfit(outfit, composition), "action": action, "object": str(hook.get("object_interaction", "")).replace("_", " "), "setting": str(hook.get("setting", "")), "anchors_scene": _items(spec.get("environment_anchors", [])).replace("_", " "), "composition": composition.replace("_", " "), "expression": str(hook.get("expression", "")).replace("_", " "), "snapshot": str(hook.get("snapshot", "")).replace("_", " ")}


def _stock_semantic(spec: dict[str, Any]) -> dict[str, str]:
    identity = spec.get("character", {}) if isinstance(spec.get("character"), dict) else {}
    outfit = spec.get("outfit", {}) if isinstance(spec.get("outfit"), dict) else {}
    return {
        "name": str(identity.get("display_name", "")),
        "anchors": _identity_cues(identity),
        "outfit": _visible_outfit(outfit, str(spec.get("composition_intent", ""))),
        "composition": str(spec.get("composition_intent", "")),
    }


def _lustify_identity_and_medium(name: str, anchors: str, outfit: str, intent: str) -> list[str]:
    medium = {"anime": "A high-end anime illustration", "semi_realistic": "A polished semi-realistic cinematic illustration", "photorealistic": "A realistic photograph"}.get(intent, "A polished semi-realistic cinematic illustration")
    identity = f"of {name}" if name else ""
    clauses = [f"{medium} {identity}.".strip()]
    if anchors:
        clauses.append(f"She is recognizable by {anchors}.")
    if outfit:
        concise_outfit = ", ".join(outfit.split(", ")[:4])
        clauses.append(f"Visible relevant outfit: {concise_outfit}.")
    return clauses

def _lustify_style_modifiers(intent: str) -> list[str]:
    if intent == "photorealistic": return ["Natural skin texture, individual hair strands, real fabric response and physically plausible reflections."]
    if intent == "anime": return ["Clean expressive line work, detailed eyes and hair, polished modern anime aesthetics."]
    return ["Natural skin shading and fabric response while retaining recognizable illustrated identity."]

def compile_lustify_stock(spec: dict[str, Any]) -> str:
    value = _stock_semantic(spec)
    intent = spec.get("render_intent", "semi_realistic")
    clauses = _lustify_identity_and_medium(value["name"], value["anchors"], value["outfit"], intent)
    clauses.extend([
        value["composition"] + ".",
        "Exactly one character on a pure seamless white background, with no environment, scenery, props, or other people.",
        "Clean soft studio lighting, clear unobstructed face, natural relaxed posture, hands visible when reasonable.",
        "No text and no logos. High visual quality and coherent anatomy."
    ])
    clauses.extend(_lustify_style_modifiers(intent))
    return " ".join(clause.strip() for clause in clauses if clause and clause.strip())

def compile_miaomiao_stock(spec: dict[str, Any]) -> str:
    value = _stock_semantic(spec)
    intent = spec.get("render_intent", "anime")
    style = {"anime": "polished modern anime illustration", "semi_realistic": "semi-realistic anime illustration", "photorealistic": "realistic material detail, anime identity retained"}.get(intent, "polished modern anime illustration")
    parts = ["masterpiece", "best quality", "1girl", "solo", value["name"], value["anchors"], value["outfit"], "full body", "three-quarter view", "standing", "neutral relaxed pose", "looking at viewer", "clear unobstructed face", "visible hands", "pure white seamless background", "no background", "no scenery", "no props", "studio lighting", style, "detailed face", "coherent anatomy", "no text", "no logo"]
    return ", ".join(part.strip() for part in parts if part and part.strip())

def compile_lustify(spec: dict[str, Any], *, mode: str) -> str:
    if mode not in {"DIRECT_T2I", "LATENT_IMG2IMG", "REFERENCE_EDIT"}:
        raise ValueError(f"Lustify {mode} is declared but not integrated without a verified local recipe")
    value = _semantic(spec); intent = spec.get("render_intent", "semi_realistic")
    clauses = _lustify_identity_and_medium(value["name"], value["anchors"], value["outfit"], intent)
    clauses.extend([f"{value['action'].rstrip(' .')}." if value["action"] else "", f"{value['expression'].rstrip(' .')}." if value["expression"] else "", f"Inside {value['setting']}." if value["setting"] else "", f"{value['anchors_scene']} remain recognizable in the softly blurred background." if value["anchors_scene"] else "", value["composition"], "Coherent anatomy, believable materials, intentional lighting and a clear readable action."])
    clauses.extend(_lustify_style_modifiers(intent))
    prompt = " ".join(clause.strip() for clause in clauses if clause and clause.strip())
    if mode in {"LATENT_IMG2IMG", "REFERENCE_EDIT"}:
        return "Create the requested semi-realistic version from the source image. Strictly preserve the source character identity, face, eyepatch and other species traits, pose, framing, scene, and visible outfit. Do not redesign the character. " + prompt
    return prompt

def compile_miaomiao(spec: dict[str, Any], *, mode: str) -> str:
    if mode not in {"DIRECT_T2I"}:
        raise ValueError(f"Miaomiao {mode} is not integrated")
    value = _semantic(spec); intent = spec.get("render_intent", "anime")
    style = {"anime": "polished modern anime illustration", "semi_realistic": "semi-realistic anime illustration", "photorealistic": "realistic material detail, anime identity retained"}.get(intent, "polished modern anime illustration")
    parts = ["masterpiece", "best quality", "1girl", "solo", value["name"], value["anchors"], value["outfit"], value["action"], value["object"], value["setting"], value["expression"], value["composition"], style, "detailed face", "detailed eyes", "detailed hair", "coherent anatomy", "soft lighting"]
    return ", ".join(part.strip() for part in parts if part and part.strip())


def build_renderer_prompt_artifact(spec: dict[str, Any], *, renderer: str, recipe_id: str, mode: str = "DIRECT_T2I", reference_images: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    is_stock = spec.get("creation_mode") == "stock"
    if renderer == "lustify" and is_stock: prompt, compiler, negative = compile_lustify_stock(spec), "lustify_stock_prompt_compiler_v1", "nude, naked, topless, nipples, explicit, multiple people, scenery, props, text, logo, complex background"
    elif renderer == "miaomiao" and is_stock: prompt, compiler, negative = compile_miaomiao_stock(spec), "miaomiao_stock_prompt_compiler_v1", "worst quality, low quality, nude, naked, topless, nipples, explicit, multiple girls, multiple people, scenery, props, complex background, text, logo, watermark"
    elif renderer == "lustify": prompt, compiler, negative = compile_lustify(spec, mode=mode), "lustify_prompt_compiler_v4", ""
    elif renderer == "miaomiao": prompt, compiler, negative = compile_miaomiao(spec, mode=mode), "miaomiao_prompt_compiler_v1", "worst quality, low quality, score_1, score_2, score_3, artist name, backlit subject"
    else: raise ValueError(f"Unsupported renderer compiler: {renderer}")
    artifact = {"schema_version":"renderer_prompt_artifact_v1", "prompt_id":f"renderer-prompt:{spec['spec_id']}:{renderer}", "renderer_id":renderer, "recipe_id":recipe_id, "mode":mode, "render_intent":spec.get("render_intent", "semi_realistic"), "source_spec_id":spec["spec_id"], "prompt":prompt, "negative_prompt":negative, "reference_images":reference_images or [], "compiler_version":compiler}
    return validate_contract("renderer_prompt_artifact_v1", artifact)
