"""Classify booru taxonomy into structured character-contract inputs."""
from __future__ import annotations

from typing import Any


IDENTITY = {"hair", "eyes", "eye", "skin", "ears", "tail", "ahoge", "tattoo", "glasses", "heterochromia", "fang", "horn"}
ACCESSORY = {"earring", "jewelry", "bracelet", "hair_ornament", "hairclip", "ribbon", "choker", "headband"}
CONTEXTUAL = {"bikini", "swimsuit", "dress", "school_uniform", "nude", "maid", "beach", "sitting", "looking_at_viewer"}
IGNORE = {"sitting", "standing", "looking_at_viewer", "solo", "1girl", "1boy", "smile"}
BODY_MORPHOLOGY = {
    "large_breasts", "small_breasts", "medium_breasts", "breasts",
}
# These remain raw taxonomy evidence. They describe a generic garment or a
# transient state, not an identity requirement or canonical outfit by themselves.
GENERIC_OR_CONTEXTUAL_CLOTHING = {
    "torn_clothes", "pants", "shirt", "jacket", "long_sleeves",
}


def classify_tag(tag: str, *, group: str = "characteristics") -> str:
    key = tag.casefold().strip()
    if key in IGNORE:
        return "IGNORE"
    if key in BODY_MORPHOLOGY:
        return "BODY_MORPHOLOGY"
    if key in GENERIC_OR_CONTEXTUAL_CLOTHING:
        return "CONTEXTUAL"
    if any(token in key for token in IDENTITY):
        return "IDENTITY"
    if any(token in key for token in ACCESSORY):
        return "ACCESSORY"
    if key in CONTEXTUAL:
        return "CONTEXTUAL"
    if group == "clothing":
        return "CANONICAL_OUTFIT" if key not in CONTEXTUAL else "CONTEXTUAL"
    return "CANONICAL_APPEARANCE"


def classify_taxonomy(characteristics: list[str], clothing: list[str]) -> dict[str, list[str]]:
    buckets = {name: [] for name in ("IDENTITY", "CANONICAL_APPEARANCE", "CANONICAL_OUTFIT", "ACCESSORY", "BODY_MORPHOLOGY", "CONTEXTUAL", "POSE_ACTION", "IGNORE")}
    for tag in characteristics:
        buckets[classify_tag(tag, group="characteristics")].append(tag)
    for tag in clothing:
        buckets[classify_tag(tag, group="clothing")].append(tag)
    return {name: list(dict.fromkeys(values)) for name, values in buckets.items()}


def taxonomy_evidence(identity: dict[str, Any]) -> list[dict[str, Any]]:
    classification = classify_taxonomy(identity.get("characteristics", []), identity.get("clothing", []))
    result = []
    for category in ("IDENTITY", "CANONICAL_APPEARANCE", "ACCESSORY", "CANONICAL_OUTFIT", "BODY_MORPHOLOGY", "CONTEXTUAL"):
        for trait in classification[category]:
            result.append({"trait": trait, "classification": category, "confidence": 0.98, "sources": ["danbooru_taxonomy"]})
    return result
