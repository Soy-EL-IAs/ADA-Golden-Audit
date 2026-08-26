import re
import json
from pathlib import Path
from typing import Dict, Any, Optional

from scripts.ada_paths import CHARACTERS_ROOT

CHARACTERS_PATH = CHARACTERS_ROOT / "catalog.json"

def _load_characters() -> Dict[str, Any]:
    try:
        return json.loads(CHARACTERS_PATH.read_text(encoding="utf-8"))
    except: return {}

def _fuzzy_match_character(text: str, characters: Dict) -> Optional[str]:
    text_lower = text.lower().strip()
    for name in characters:
        if text_lower == name.lower():
            return name
    # Partial match
    for name in characters:
        if text_lower in name.lower() or name.lower() in text_lower:
            return name
    return None

def _fuzzy_match_franchise(text: str, characters: Dict) -> Optional[str]:
    text_lower = text.lower().strip()
    franchises = set()
    for info in characters.values():
        franchises.add(info.get("franchise", ""))
    for f in franchises:
        if text_lower == f.lower() or text_lower in f.lower() or f.lower() in text_lower:
            return f
    return None

def parse_command(text: str) -> Dict[str, Any]:
    text = text.strip()
    if not text:
        return {"intent": "UNKNOWN", "suggestion": "Try: create 6 images of 2B"}
    
    characters = _load_characters()
    
    # Intent: CREATE_IMAGES
    # Patterns: "create/generate/make N images of CHARACTER"
    create_match = re.match(
        r'(?:create|generate|make|produce)\s+(\d+)\s+(?:images?|photos?|pictures?|assets?)\s+(?:of|for)\s+(.+)',
        text, re.IGNORECASE
    )
    if create_match:
        count = int(create_match.group(1))
        char_text = create_match.group(2).strip()
        character = _fuzzy_match_character(char_text, characters)
        if character:
            return {"intent": "CREATE_IMAGES", "character": character, "count": count}
        else:
            return {"intent": "CHARACTER_NOT_REGISTERED", "error": "character_not_registered",
                    "character": char_text, "count": count,
                    "message": f"Character '{char_text}' is not registered. Add it before creating images."}
    
    # Pattern without count: "create images of CHARACTER"
    create_no_count = re.match(
        r'(?:create|generate|make|produce)\s+(?:images?|photos?|pictures?|assets?)\s+(?:of|for)\s+(.+)',
        text, re.IGNORECASE
    )
    if create_no_count:
        char_text = create_no_count.group(1).strip()
        character = _fuzzy_match_character(char_text, characters)
        if character:
            return {"intent": "CREATE_IMAGES", "character": character, "count": 6,
                    "note": "No count specified, defaulting to 6"}
        return {"intent": "CHARACTER_NOT_REGISTERED", "error": "character_not_registered",
                "character": char_text, "count": 6,
                "message": f"Character '{char_text}' is not registered. Add it before creating images."}
    
    # Intent: SHOW_ACTIVE_MISSIONS
    if re.match(r'(?:missions?|status|active|what.*running)', text, re.IGNORECASE):
        return {"intent": "SHOW_ACTIVE_MISSIONS"}
    
    # Intent: OPEN_CHARACTER_LIBRARY or OPEN_COLLECTION
    show_match = re.match(r'(?:show|open|view|browse)\s+(.+)', text, re.IGNORECASE)
    if show_match:
        target = show_match.group(1).strip()
        
        # Try character first
        character = _fuzzy_match_character(target, characters)
        if character:
            return {"intent": "OPEN_CHARACTER_LIBRARY", "character": character}
        
        # Try franchise
        franchise = _fuzzy_match_franchise(target, characters)
        if franchise:
            return {"intent": "OPEN_COLLECTION", "franchise": franchise}
        
        return {"intent": "OPEN_CHARACTER_LIBRARY", "character": target,
                "warning": f"'{target}' not found in taxonomy"}
    
    # Bare character name
    character = _fuzzy_match_character(text, characters)
    if character:
        return {"intent": "OPEN_CHARACTER_LIBRARY", "character": character}
    
    franchise = _fuzzy_match_franchise(text, characters)
    if franchise:
        return {"intent": "OPEN_COLLECTION", "franchise": franchise}
    
    return {"intent": "UNKNOWN", "suggestion": "Try: create 6 images of 2B, or: show 2B, or: show NieR"}
