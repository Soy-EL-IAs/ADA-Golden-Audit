"""Resolve a user supplied character name into taxonomy evidence.

This module deliberately knows nothing about web pages, image URLs, caching, or
renderers.  The local booru character dataset is used as a naming/taxonomy
source only; it is not a canonical visual-reference source.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

if __package__:
    from .ada_paths import CONFIG_ROOT
    from .query_booru_characters import DEFAULT_DATASET, load_records, normalized
else:
    from ada_paths import CONFIG_ROOT
    from query_booru_characters import DEFAULT_DATASET, load_records, normalized


ALIASES_PATH = CONFIG_ROOT / "character_aliases.json"


def _unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if isinstance(value, str) and value.strip()))


def _display(tag: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[_()]", " ", tag)).strip().title()


@dataclass(frozen=True)
class CharacterIdentity:
    requested_name: str
    canonical_name: str
    canonical_tag: str
    character_id: str
    franchise: list[str]
    aliases: list[str]
    characteristics: list[str]
    clothing: list[str]
    source: str = "danbooru_taxonomy"

    def to_dict(self) -> dict[str, Any]:
        return {
            "requested_name": self.requested_name,
            "canonical_name": self.canonical_name,
            "canonical_tag": self.canonical_tag,
            "character_id": self.character_id,
            "franchise": self.franchise,
            "aliases": self.aliases,
            "characteristics": self.characteristics,
            "clothing": self.clothing,
            "source": self.source,
        }


class CharacterTagResolver:
    """Deterministic resolver over the local Danbooru-derived taxonomy."""

    def __init__(self, dataset_path: Path = DEFAULT_DATASET, aliases_path: Path = ALIASES_PATH) -> None:
        self.dataset_path = dataset_path
        self.aliases_path = aliases_path
        self._records: list[dict[str, Any]] | None = None
        self._aliases: dict[str, str] | None = None

    def resolve(self, character: str, version: str | None = None) -> CharacterIdentity | None:
        requested = self._clean(character)
        version_key = normalized(version) if version else ""
        records = self._load_records()
        query = self._query_key(requested)
        alias_tag = self._load_aliases().get(query)
        candidates = [record for record in records if str(record.get("name")) == alias_tag] if alias_tag else self._matches(records, query)
        if version_key:
            versioned = [record for record in candidates if any(normalized(str(item)) == version_key for item in record.get("copyright", []))]
            if versioned:
                candidates = versioned
        if len(candidates) != 1:
            return None
        record = candidates[0]
        tag = str(record["name"])
        copyrights = _unique([str(item) for item in record.get("copyright", [])])
        aliases = _unique([requested, _display(tag), tag.replace("_", " "), *self._configured_aliases_for(tag)])
        return CharacterIdentity(
            requested_name=requested,
            canonical_name=_display(tag),
            canonical_tag=tag,
            character_id=re.sub(r"[^a-z0-9]+", "_", tag.casefold()).strip("_"),
            franchise=copyrights,
            aliases=aliases,
            characteristics=_unique([str(item) for item in record.get("characteristics", [])]),
            clothing=_unique([str(item) for item in record.get("clothing", [])]),
        )

    def candidates(self, character: str, version: str | None = None) -> list[dict[str, Any]]:
        """Diagnostic-only candidate list; it does not select a visual source."""
        query = self._query_key(character)
        version_key = normalized(version) if version else ""
        result: list[dict[str, Any]] = []
        for record in self._matches(self._load_records(), query):
            copyrights = [str(item) for item in record.get("copyright", [])]
            result.append({"canonical_tag": record.get("name"), "copyright": copyrights,
                           "version_match": bool(version_key and any(normalized(item) == version_key for item in copyrights)),
                           "post_count": record.get("post_count", 0)})
        return result

    def _matches(self, records: list[dict[str, Any]], query: str) -> list[dict[str, Any]]:
        exact = [record for record in records if normalized(str(record.get("name", ""))) == query]
        if exact:
            return exact
        query_tokens = set(query.split())
        # Parenthesized/copyright suffixes are intentional identity disambiguators.
        matched = [record for record in records if query_tokens and query_tokens.issubset(set(normalized(str(record.get("name", ""))).split()))]
        return matched

    def _load_records(self) -> list[dict[str, Any]]:
        if self._records is None:
            self._records = load_records(self.dataset_path) if self.dataset_path.is_file() else []
        return self._records

    def _load_aliases(self) -> dict[str, str]:
        if self._aliases is None:
            aliases: dict[str, str] = {}
            try:
                configured = json.loads(self.aliases_path.read_text(encoding="utf-8")).get("booru_characters", {})
                aliases = {normalized(name): tag for name, tag in configured.items() if isinstance(name, str) and isinstance(tag, str)}
            except (OSError, ValueError, json.JSONDecodeError):
                pass
            self._aliases = aliases
        return self._aliases

    def _configured_aliases_for(self, tag: str) -> list[str]:
        return [name for name, value in self._load_aliases().items() if value == tag]

    @staticmethod
    def _clean(value: str) -> str:
        cleaned = " ".join(value.split()).strip()
        if not cleaned or len(cleaned) > 120:
            raise ValueError("character must contain between 1 and 120 characters")
        return cleaned

    @staticmethod
    def _query_key(value: str) -> str:
        # Connector words are display syntax, not taxonomy identity.  This
        # keeps inputs such as "Nanally de NTE" deterministic without adding
        # an ad-hoc per-character alias.
        return " ".join(token for token in normalized(value).split() if token not in {"de", "of", "the", "from"})
