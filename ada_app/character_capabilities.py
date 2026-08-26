"""Evidence-backed character catalog and production renderer routing."""
from __future__ import annotations

import json
from pathlib import Path
import threading
from typing import Any

from scripts.ada_paths import ADA_ROOT, CHARACTERS_ROOT
from scripts.character_reference_manifest import load_character_reference_manifest


CONFIRMED = {"confirmed", "reliable", "supported"}
UNRECOGNIZED = {"unreliable", "unsupported", "not_recognized", "failed"}
HEROES_PATH = CHARACTERS_ROOT / "heroes.json"
_HEROES_LOCK = threading.Lock()

RECOMMENDED_CHARACTERS = [
    {"name": "Ada Wong", "franchise": "Resident Evil", "priority": "High", "reason": "Iconic silhouette, stable visual identity and strong semi-realistic fit."},
    {"name": "Lara Croft", "franchise": "Tomb Raider", "priority": "High", "reason": "Widely recognized identity with useful action and studio coverage."},
    {"name": "Faye Valentine", "franchise": "Cowboy Bebop", "priority": "High", "reason": "Distinct outfit, hair and color language for identity routing tests."},
    {"name": "Cammy White", "franchise": "Street Fighter", "priority": "High", "reason": "Strong canonical outfit and an excellent companion benchmark for Chun-Li."},
    {"name": "Mai Shiranui", "franchise": "Fatal Fury", "priority": "High", "reason": "Highly recognizable costume and hairstyle across anime renderers."},
    {"name": "Bayonetta", "franchise": "Bayonetta", "priority": "High", "reason": "Complex but distinctive identity, ideal for capability evaluation."},
    {"name": "Motoko Kusanagi", "franchise": "Ghost in the Shell", "priority": "Medium", "reason": "Useful cyberpunk identity with multiple canonical interpretations."},
    {"name": "Samus Aran", "franchise": "Metroid", "priority": "Medium", "reason": "Supports both Zero Suit and armored-version identity testing."},
    {"name": "Yor Forger", "franchise": "SPY×FAMILY", "priority": "Medium", "reason": "Popular modern character with clear hair, dress and accessory anchors."},
    {"name": "Lucy", "franchise": "Cyberpunk: Edgerunners", "priority": "Medium", "reason": "Distinctive modern anime design and useful neon-to-studio translation."},
    {"name": "Revy", "franchise": "Black Lagoon", "priority": "Medium", "reason": "Recognizable practical outfit and strong action-oriented identity."},
    {"name": "Morrigan Aensland", "franchise": "Darkstalkers", "priority": "Medium", "reason": "Distinct fantasy traits make a strong non-human identity benchmark."},
]


def load_character_heroes() -> dict[str, str]:
    try:
        value = json.loads(HEROES_PATH.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError, json.JSONDecodeError):
        return {}


def save_character_hero(character: str, asset_id: str) -> None:
    with _HEROES_LOCK:
        heroes = load_character_heroes()
        heroes[character] = asset_id
        HEROES_PATH.parent.mkdir(parents=True, exist_ok=True)
        HEROES_PATH.write_text(json.dumps(heroes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _normalized_name(value: Any) -> str:
    return "".join(character for character in str(value or "").casefold() if character.isalnum())


def character_capability_status(entry: dict[str, Any]) -> dict[str, str]:
    capabilities = entry.get("renderer_capabilities", {}) if isinstance(entry, dict) else {}
    capabilities = capabilities if isinstance(capabilities, dict) else {}
    lustify = capabilities.get("lustify", {}) if isinstance(capabilities.get("lustify"), dict) else {}
    miaomiao = capabilities.get("miaomiao", {}) if isinstance(capabilities.get("miaomiao"), dict) else {}
    lustify_state = str(lustify.get("identity_recognition", "unknown")).casefold()
    miaomiao_state = str(miaomiao.get("identity_recognition", "unknown")).casefold()
    if lustify_state in CONFIRMED:
        return {"status": "green", "label": "Lustify direct", "route": "lustify_direct", "reason": lustify.get("note", "Lustify identity recognition is confirmed.")}
    fallback_ready = (
        lustify_state in UNRECOGNIZED
        and miaomiao_state in CONFIRMED
        and str(lustify.get("img2img", "")).casefold() in CONFIRMED
        and bool(lustify.get("fallback_recipe"))
    )
    if fallback_ready:
        return {"status": "yellow", "label": "Miaomiao → Lustify", "route": "miaomiao_then_lustify_img2img", "reason": lustify.get("note", "Miaomiao supplies identity before Lustify Img2Img.")}
    if lustify_state in UNRECOGNIZED and miaomiao_state in UNRECOGNIZED:
        return {"status": "red", "label": "No recognized renderer", "route": "blocked", "reason": "Neither Lustify nor Miaomiao has confirmed identity recognition for this character."}
    return {"status": "unknown", "label": "Not evaluated", "route": "unverified", "reason": "Renderer identity compatibility has not been evaluated yet."}


def renderer_request_allowed(entry: dict[str, Any], renderer: str) -> tuple[bool, str]:
    status = character_capability_status(entry)
    if status["status"] == "red":
        return False, status["reason"]
    capabilities = entry.get("renderer_capabilities", {}) if isinstance(entry, dict) else {}
    renderer_entry = capabilities.get(renderer, {}) if isinstance(capabilities, dict) and isinstance(capabilities.get(renderer), dict) else {}
    renderer_state = str(renderer_entry.get("identity_recognition", "unknown")).casefold()
    if renderer == "miaomiao" and renderer_state in UNRECOGNIZED:
        return False, renderer_entry.get("note", "Miaomiao does not recognize this character reliably.")
    return True, ""


def resolve_stock_renderer(entry: dict[str, Any]) -> dict[str, str]:
    """Choose one direct identity renderer for Stock and preserve the evidence.

    Confirmed direct identity recognition wins. When no direct renderer has been
    evaluated, V1 uses the production primary (Lustify) as an explicit,
    auditable fallback. A renderer known to be unreliable is never selected.
    """
    capabilities = entry.get("renderer_capabilities", {}) if isinstance(entry, dict) else {}
    capabilities = capabilities if isinstance(capabilities, dict) else {}
    states = {
        renderer: str(capabilities.get(renderer, {}).get("identity_recognition", "unknown")).casefold()
        if isinstance(capabilities.get(renderer), dict) else "unknown"
        for renderer in ("lustify", "miaomiao")
    }
    if states["lustify"] in CONFIRMED:
        return {"renderer": "lustify", "route": "confirmed_direct", "evidence": states["lustify"], "fallback": "false"}
    if states["miaomiao"] in CONFIRMED:
        return {"renderer": "miaomiao", "route": "confirmed_direct", "evidence": states["miaomiao"], "fallback": "false"}
    if states["lustify"] not in UNRECOGNIZED:
        return {"renderer": "lustify", "route": "unverified_primary_fallback", "evidence": states["lustify"], "fallback": "true"}
    if states["miaomiao"] not in UNRECOGNIZED:
        return {"renderer": "miaomiao", "route": "unverified_secondary_fallback", "evidence": states["miaomiao"], "fallback": "true"}
    raise ValueError("No direct renderer can preserve this character's identity in Stock mode.")


def _reference_from_manifest(entry: dict[str, Any]) -> str:
    relative = entry.get("refs_manifest") if isinstance(entry, dict) else None
    if not isinstance(relative, str) or not relative:
        return ""
    manifest_path = ADA_ROOT / relative
    try:
        manifest = load_character_reference_manifest(manifest_path)
    except (OSError, json.JSONDecodeError):
        return ""
    for reference in manifest["canonical_references"]:
        filename = reference.get("file") if isinstance(reference, dict) else None
        candidate = manifest_path.parent / filename if isinstance(filename, str) else None
        if candidate and candidate.is_file():
            return str(candidate.resolve())
    return ""


def build_character_catalog(characters: dict[str, Any], assets: list[dict[str, Any]], heroes: dict[str, str] | None = None) -> list[dict[str, Any]]:
    heroes = heroes or {}
    result: list[dict[str, Any]] = []
    for name, raw_entry in sorted(characters.items(), key=lambda item: item[0].casefold()):
        entry = raw_entry if isinstance(raw_entry, dict) else {}
        character_assets = [asset for asset in assets if asset.get("character") == name]
        visible_assets = [asset for asset in character_assets if asset.get("is_visible_library_asset") is True]
        stock_assets = [asset for asset in visible_assets if asset.get("creation_mode") == "stock"]
        hero_id = heroes.get(name, "")
        reference_asset = next((asset for asset in visible_assets if asset.get("asset_id") == hero_id), None)
        saved_hero_is_valid = reference_asset is not None
        cover_source = (
            "stock_hero" if reference_asset and reference_asset.get("creation_mode") == "stock"
            else "library_hero" if reference_asset else ""
        )
        if reference_asset is None and stock_assets:
            # Pick a stock asset based on valid identity/quality evidence.
            # Require a minimum rating so bad images aren't automatically used as cover.
            eligible_stock = [asset for asset in stock_assets if float(asset.get("agent_rating") or 0) >= 6.5]
            if eligible_stock:
                reference_asset = max(eligible_stock, key=lambda asset: float(asset.get("agent_rating") or 0))
                cover_source = "stock"
        manifest_reference = _reference_from_manifest(entry) if reference_asset is None else ""
        if manifest_reference:
            cover_source = "canonical_reference"
        if reference_asset is None and not manifest_reference and visible_assets:
            reference_asset = max(visible_assets, key=lambda asset: asset.get("generated_at") or asset.get("created_at") or "")
            cover_source = "library_latest"
        tags = list(dict.fromkeys(
            item for item in [entry.get("canonical_tag"), *(entry.get("tags", []) if isinstance(entry.get("tags"), list) else [])]
            if isinstance(item, str) and item.strip()
        ))
        result.append({
            "name": name,
            "display_name": entry.get("name") or name,
            "registered": True,
            "franchise": entry.get("franchise") or entry.get("universe") or "Unknown",
            "universe": entry.get("universe") or "",
            "image_count": len(visible_assets),
            "stock_image_count": len(stock_assets),
            "reference_image": reference_asset.get("full_image_path", "") if reference_asset else manifest_reference,
            "reference_asset_id": reference_asset.get("asset_id", "") if reference_asset else "",
            "cover_source": cover_source or "none",
            "has_cover": bool(reference_asset or manifest_reference),
            "stale_hero": bool(hero_id and not saved_hero_is_valid),
            "canonical_tag": entry.get("canonical_tag", ""),
            "tags": tags,
            "capability": character_capability_status(entry),
            "renderer_capabilities": entry.get("renderer_capabilities", {}),
        })
    registered_names: set[str] = set()
    for name, raw_entry in characters.items():
        entry = raw_entry if isinstance(raw_entry, dict) else {}
        candidates = [name, entry.get("name", "")]
        if isinstance(entry.get("aliases"), list):
            candidates.extend(entry["aliases"])
        registered_names.update(_normalized_name(candidate) for candidate in candidates)
    for recommendation in RECOMMENDED_CHARACTERS:
        if _normalized_name(recommendation["name"]) in registered_names:
            continue
        result.append({
            **recommendation,
            "display_name": recommendation["name"],
            "registered": False,
            "image_count": 0,
            "stock_image_count": 0,
            "reference_image": "",
            "reference_asset_id": "",
            "cover_source": "none",
            "has_cover": False,
            "stale_hero": False,
            "canonical_tag": "",
            "tags": [],
            "capability": {"status": "unknown", "label": "Not evaluated", "route": "unverified", "reason": "Add the character to resolve its identity data and renderer compatibility."},
            "renderer_capabilities": {},
        })
    return result
