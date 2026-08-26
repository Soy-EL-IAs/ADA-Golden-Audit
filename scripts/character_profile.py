#!/usr/bin/env python3
"""Conservative local identity profiles from Sn0w123/booru-characters."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

if __package__:
    from .ada_paths import CONFIG_ROOT
    from .query_booru_characters import DEFAULT_DATASET, load_records, normalized
else:
    from ada_paths import CONFIG_ROOT
    from query_booru_characters import DEFAULT_DATASET, load_records, normalized

try:
    from .character_tag_resolver import CharacterTagResolver
except ImportError:
    from character_tag_resolver import CharacterTagResolver

DEFAULT_ALIASES = CONFIG_ROOT / "character_aliases.json"


class CharacterProfileDatabase:
    """Read the local booru dataset without adding or interpreting visual facts."""

    def __init__(
        self,
        dataset_path: Path = DEFAULT_DATASET,
        aliases_path: Path = DEFAULT_ALIASES,
    ) -> None:
        self.dataset_path = dataset_path
        self.aliases_path = aliases_path
        self._records: list[dict[str, Any]] | None = None
        self._aliases: dict[str, str] | None = None
        self._resolver = CharacterTagResolver(dataset_path=dataset_path, aliases_path=aliases_path)

    def get_character_profile(self, character: str, version: str | None = None) -> dict[str, Any]:
        requested_character = self._clean(character, "character")
        requested_version = self._clean(version, "version") if version else None
        # Compatibility facade: callers of the old profile API now consume the
        # resolved taxonomy, while web/reference discovery stays elsewhere.
        resolved = self._resolver.resolve(requested_character, requested_version)
        if resolved is not None:
            value = resolved.to_dict()
            return {
                "requested_character": requested_character,
                "requested_version": requested_version,
                "matched_tag": value["canonical_tag"],
                "canonical_name": value["canonical_name"],
                "character_id": value["character_id"],
                "aliases": value["aliases"],
                "character_profile_used": True,
                "gender": None,
                "copyright": value["franchise"],
                "characteristics": value["characteristics"],
                "clothing": value["clothing"],
                "relationships": {},
                "version_match": True if requested_version else None,
                "candidates": [],
                "source": "danbooru_taxonomy",
                "identity_resolution": value,
            }
        records = self._load_records()
        if records is None:
            return self._empty(requested_character, requested_version, "dataset_unavailable")

        candidates = self._matching_records(records, requested_character)
        if requested_version:
            versioned = [record for record in candidates if self._version_match(record, requested_version)]
            if versioned:
                candidates = versioned
            elif candidates:
                return self._empty(
                    requested_character,
                    requested_version,
                    "version_not_matched",
                    self._candidate_summaries(candidates, requested_version),
                )

        if len(candidates) != 1:
            return self._empty(
                requested_character,
                requested_version,
                "ambiguous" if candidates else "not_found",
                self._candidate_summaries(candidates, requested_version),
            )

        record = candidates[0]
        return {
            "requested_character": requested_character,
            "requested_version": requested_version,
            "matched_tag": record.get("name"),
            "character_profile_used": True,
            "gender": record.get("gender"),
            "copyright": record.get("copyright", []),
            "characteristics": record.get("characteristics", []),
            "clothing": record.get("clothing", []),
            "relationships": record.get("relationships", {}),
            "version_match": self._version_match(record, requested_version) if requested_version else None,
            "candidates": [],
            "source": "booru-characters",
        }

    def _load_records(self) -> list[dict[str, Any]] | None:
        if self._records is None and self.dataset_path.is_file():
            self._records = load_records(self.dataset_path)
        return self._records

    def _matching_records(self, records: list[dict[str, Any]], character: str) -> list[dict[str, Any]]:
        query = normalized(character)
        aliases = self._load_aliases()
        alias_tag = aliases.get(query)
        if alias_tag:
            return [record for record in records if record.get("name") == alias_tag]

        exact = [record for record in records if normalized(str(record.get("name", ""))) == query]
        if exact:
            return exact

        # A Danbooru tag can carry a parenthesized copyright suffix. This accepts
        # only an exact base-tag match, not fuzzy similarity.
        base_matches = [
            record for record in records
            if normalized(re.sub(r"_\([^)]*\)$", "", str(record.get("name", "")))) == query
        ]
        return base_matches

    def _load_aliases(self) -> dict[str, str]:
        if self._aliases is not None:
            return self._aliases
        aliases: dict[str, str] = {}
        try:
            data = json.loads(self.aliases_path.read_text(encoding="utf-8"))
            configured = data.get("booru_characters", {})
            if isinstance(configured, dict):
                for name, tag in configured.items():
                    if isinstance(name, str) and isinstance(tag, str):
                        aliases[normalized(name)] = tag
        except (OSError, json.JSONDecodeError):
            pass
        self._aliases = aliases
        return aliases

    @staticmethod
    def _version_match(record: dict[str, Any], version: str | None) -> bool:
        if not version:
            return False
        requested = normalized(version)
        return any(normalized(str(item)) == requested for item in record.get("copyright", []))

    def _candidate_summaries(self, records: list[dict[str, Any]], version: str | None) -> list[dict[str, Any]]:
        return [
            {
                "matched_tag": record.get("name"),
                "copyright": record.get("copyright", []),
                "version_match": self._version_match(record, version) if version else None,
            }
            for record in records
        ]

    @staticmethod
    def _empty(
        character: str,
        version: str | None,
        reason: str,
        candidates: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        return {
            "requested_character": character,
            "requested_version": version,
            "matched_tag": None,
            "character_profile_used": False,
            "gender": None,
            "copyright": [],
            "characteristics": [],
            "clothing": [],
            "relationships": {},
            "version_match": False if version else None,
            "candidates": candidates or [],
            "source": "booru-characters",
            "reason": reason,
        }

    @staticmethod
    def _clean(value: str, field: str) -> str:
        if not isinstance(value, str):
            raise ValueError(f"{field} must be text")
        cleaned = " ".join(value.split()).strip()
        if not cleaned or len(cleaned) > 120:
            raise ValueError(f"{field} must contain between 1 and 120 characters")
        return cleaned
