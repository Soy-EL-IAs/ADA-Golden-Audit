"""Explicit user intent carried unchanged from Create to the render contract."""
from __future__ import annotations

from typing import Any


def _field(value: Any, *, locked: bool, must_be_visible: bool = False) -> dict[str, Any]:
    text = value.strip() if isinstance(value, str) else ""
    return {"value": text or None, "locked": bool(locked and text), "must_be_visible": bool(must_be_visible and text)}


def build_creative_intent_envelope(*, character: str, setting: str = "", action: str = "", render_intent: str = "semi_realistic") -> dict[str, Any]:
    """Create's explicit values are authoritative; blank fields remain creative freedom."""
    return {
        "schema_version": "creative_intent_envelope_v1",
        "character": _field(character, locked=True),
        "setting": _field(setting, locked=True, must_be_visible=True),
        "action": _field(action, locked=True),
        "render_intent": _field(render_intent, locked=True),
    }


def locked_value(intent: dict[str, Any] | None, field: str) -> str:
    value = (intent or {}).get(field, {})
    return str(value.get("value", "")).strip() if isinstance(value, dict) and value.get("locked") else ""


def environment_anchors(setting: str) -> list[str]:
    """Small, deterministic visual anchors for a locked, recognizable setting."""
    normalized = setting.casefold()
    known = {
        "classroom": ["chalkboard", "wooden desk"],
        "kitchen": ["countertop", "kitchen cabinets"],
        "bathroom": ["mirror", "sink"],
        "bedroom": ["bed", "bedside furniture"],
    }
    for key, anchors in known.items():
        if key in normalized:
            return anchors
    return [f"recognizable {setting} context"] if setting else []
