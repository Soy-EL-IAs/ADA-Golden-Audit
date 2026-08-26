#!/usr/bin/env python3
"""Hard Visual Reviewer."""

import json
from pathlib import Path
from typing import Any

from scripts.ada_paths import ADA_ROOT
from scripts.visual_reviewer import _request, image_data_url

RUNTIME_INSTRUCTION = (ADA_ROOT / "config" / "runtime_instructions" / "hard_visual_review_v1.md").read_text(encoding="utf-8").strip()

def evaluate_image(image_path: Path) -> dict[str, Any]:
    url = "http://127.0.0.1:1234/v1/chat/completions" # Default LM Studio URL
    try:
        from scripts.ada_paths import LMSTUDIO_BASE_URL
        if LMSTUDIO_BASE_URL:
            url = f"{LMSTUDIO_BASE_URL}/v1/chat/completions"
    except ImportError:
        pass
        
    payload = {
        "model": "local-model",
        "messages": [
            {
                "role": "system",
                "content": RUNTIME_INSTRUCTION
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Execute the hard visual review for this image."},
                    {"type": "image_url", "image_url": {"url": image_data_url(image_path)}}
                ]
            }
        ],
        "temperature": 0.0,
        "max_tokens": 512
    }
    
    response = _request(url, payload, timeout=120)
    
    choices = response.get("choices", [])
    if not choices:
        raise RuntimeError("No choices in response")
        
    content = choices[0].get("message", {}).get("content", "")
    from scripts.visual_reviewer import _parse_json_object
    try:
        data = _parse_json_object(content)
        return data
    except Exception as e:
        raise RuntimeError(f"Could not parse JSON: {content} - {e}")
