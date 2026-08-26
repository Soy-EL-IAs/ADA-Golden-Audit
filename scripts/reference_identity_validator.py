"""Small, single-purpose visual identity check for reference onboarding."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .visual_reviewer import _content_text, _parse_json_object, _request, image_data_url


class CompactReferenceIdentityValidator:
    """Ask a VL model only whether a downloaded reference matches an identity.

    It intentionally does not use the production Visual Review schema: no
    composition, anatomy, aesthetic rating, or renderer feedback is requested.
    """

    def __init__(self, model: str = "qwen/qwen3-vl-8b", base_url: str = "http://127.0.0.1:1234") -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")

    def validate(self, image_path: Path, identity: dict[str, Any]) -> dict[str, Any]:
        if not image_path.is_file():
            raise FileNotFoundError(image_path)
        traits = [str(value) for value in identity.get("characteristics", [])[:8]]
        prompt = (
            "Return JSON only: {identity_match:boolean,confidence:number,evidence:string[]}. "
            "Evaluate only whether the image depicts the requested fictional character. "
            f"Character: {identity.get('canonical_name')}; franchise: {', '.join(identity.get('franchise', []))}; "
            f"taxonomy tag: {identity.get('canonical_tag')}; known traits: {', '.join(traits)}. "
            "Do not score composition, anatomy, aesthetics, or prompt adherence."
        )
        schema = {"type": "object", "additionalProperties": False, "required": ["identity_match", "confidence", "evidence"], "properties": {
            "identity_match": {"type": "boolean"}, "confidence": {"type": "number", "minimum": 0, "maximum": 1},
            "evidence": {"type": "array", "items": {"type": "string"}, "maxItems": 4},
        }}
        payload = {"model": self.model, "messages": [{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": image_data_url(image_path)}},
        ]}], "temperature": 0, "max_tokens": 120,
                   "response_format": {"type": "json_schema", "json_schema": {"name": "compact_reference_identity_v1", "strict": True, "schema": schema}}}
        value = _parse_json_object(_content_text(_request(f"{self.base_url}/v1/chat/completions", payload, timeout=120)))
        match = value.get("identity_match")
        confidence = value.get("confidence")
        evidence = value.get("evidence", [])
        if not isinstance(match, bool) or not isinstance(confidence, (int, float)) or not 0 <= float(confidence) <= 1:
            raise ValueError("Compact identity validator returned an invalid result")
        return {"status": "visual_identity_validation", "identity_match": match, "confidence": round(float(confidence), 2),
                "evidence": [str(item) for item in evidence if isinstance(item, str)][:4]}
