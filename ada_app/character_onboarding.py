from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any

from scripts.ada_paths import ADA_ROOT, CHARACTER_REFS_ROOT, CHARACTERS_ROOT
from scripts.character_profile import CharacterProfileDatabase
from scripts.character_ref_cache import CharacterReferenceCache
from scripts.character_reference_manifest import load_character_reference_manifest
from scripts.character_refs import CharacterReferenceFinder
from scripts.local_search import SearXNGClient
from scripts.query_booru_characters import normalized
from scripts.character_tag_resolver import CharacterTagResolver
from scripts.character_taxonomy import classify_taxonomy, taxonomy_evidence
from scripts.reference_identity_validator import CompactReferenceIdentityValidator
from ada_app.semantic_contracts import build_character_contract


CHARACTERS_PATH = CHARACTERS_ROOT / "catalog.json"
_REGISTRY_LOCK = threading.Lock()


class CharacterBootstrapError(RuntimeError):
    def __init__(self, code: str, message: str, status_code: int) -> None:
        super().__init__(message)
        self.code = code
        self.status_code = status_code


def load_characters(path: Path = CHARACTERS_PATH) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def registered_character_name(character: str, path: Path = CHARACTERS_PATH) -> str | None:
    query = normalized(character) if isinstance(character, str) else ""
    if not query:
        return None
    for name in load_characters(path):
        if normalized(name) == query:
            return name
    return None


class CharacterBootstrapService:
    def __init__(
        self,
        characters_path: Path = CHARACTERS_PATH,
        refs_root: Path = CHARACTER_REFS_ROOT,
        profiles: CharacterProfileDatabase | None = None,
        cache: CharacterReferenceCache | None = None,
        resolver: CharacterTagResolver | None = None,
    ) -> None:
        self.characters_path = characters_path
        self.refs_root = refs_root.resolve()
        self.profiles = profiles or CharacterProfileDatabase()
        self.resolver = resolver or CharacterTagResolver()
        if cache is None:
            finder = CharacterReferenceFinder(SearXNGClient())
            cache = CharacterReferenceCache(finder, root=self.refs_root, identity_validator=CompactReferenceIdentityValidator())
        self.cache = cache

    def _storage_relative(self, path: Path) -> str:
        """Persist project-relative paths in production and equivalent paths in tests."""
        try:
            if self.characters_path.resolve() != CHARACTERS_PATH.resolve() or self.refs_root != CHARACTER_REFS_ROOT.resolve():
                raise ValueError("isolated storage roots")
            base = ADA_ROOT
        except ValueError:
            base = self.characters_path.resolve().parents[2]
        return path.resolve().relative_to(base).as_posix()

    def bootstrap(self, character: str, version: str | None = None) -> dict[str, Any]:
        character = self._clean(character, "character")
        version = self._clean(version, "version") if version else None

        existing = registered_character_name(character, self.characters_path)
        if existing:
            return {"status": "already_registered", "character": existing, "registered": False, "duplicate": True}

        profile = self.profiles.get_character_profile(character, version)
        if not profile.get("character_profile_used") or not profile.get("matched_tag"):
            reason = str(profile.get("reason") or "not_found")
            raise CharacterBootstrapError(
                "character_not_found" if reason == "not_found" else "character_profile_unresolved",
                f"Character profile could not be resolved: {reason}",
                404 if reason == "not_found" else 409,
            )

        identity = profile.get("identity_resolution") if isinstance(profile.get("identity_resolution"), dict) else None
        if identity is None:
            resolved = self.resolver.resolve(character, version)
            identity = resolved.to_dict() if resolved is not None else None
        if identity is None:
            raise CharacterBootstrapError("character_identity_unresolved", "Character taxonomy could not be resolved.", 409)
        profile["identity_resolution"] = identity
        profile["taxonomy_classification"] = classify_taxonomy(identity.get("characteristics", []), identity.get("clothing", []))
        profile["taxonomy_evidence"] = taxonomy_evidence(identity)
        try:
            try:
                cached = self.cache.cache(character, version, identity=identity)
            except TypeError:  # lightweight legacy/test cache adapters
                cached = self.cache.cache(character, version)
        except Exception as exc:
            raise CharacterBootstrapError(
                "character_cache_failed", f"Character references could not be cached: {exc}", 503
            ) from exc

        if cached.get("usable") is not True or not cached.get("manifest"):
            raise CharacterBootstrapError(
                "character_cache_failed", "Character references did not produce a usable manifest.", 503
            )

        manifest_path = Path(str(cached["manifest"])).resolve()
        self._require_usable_manifest(manifest_path, character, version)
        entry = self._registry_entry(character, version, profile, manifest_path)
        contract = build_character_contract(profile, entry)
        contract_path = manifest_path.parent / "character_contract_v1.json"
        self._write_json_atomic(contract_path, contract)
        entry["character_contract"] = self._storage_relative(contract_path)

        with _REGISTRY_LOCK:
            characters = load_characters(self.characters_path)
            for name in characters:
                if normalized(name) == normalized(character):
                    return {"status": "already_registered", "character": name, "registered": False, "duplicate": True}
            characters[character] = entry
            self._write_registry(characters)

        return {
            "status": "registered",
            "character": character,
            "registered": True,
            "duplicate": False,
            "profile": profile,
            "identity_resolution": identity,
            "manifest": entry["refs_manifest"],
            "character_contract": entry["character_contract"],
            "reference_status": entry.get("reference_status", "READY"),
        }

    def revalidate(self, character: str, version: str | None = None) -> dict[str, Any]:
        """Refresh registered characters through normal identity and reference stages."""
        character = self._clean(character, "character")
        version = self._clean(version, "version") if version else None
        profile = self.profiles.get_character_profile(character, version)
        identity = profile.get("identity_resolution") if isinstance(profile.get("identity_resolution"), dict) else None
        if identity is None:
            resolved = self.resolver.resolve(character, version)
            identity = resolved.to_dict() if resolved else None
        if identity is None:
            raise CharacterBootstrapError("character_identity_unresolved", "Character taxonomy could not be resolved.", 409)
        profile["identity_resolution"] = identity
        profile["taxonomy_classification"] = classify_taxonomy(identity.get("characteristics", []), identity.get("clothing", []))
        profile["taxonomy_evidence"] = taxonomy_evidence(identity)
        cached = self.cache.cache(character, version, identity=identity, force=True)
        if not cached.get("usable") or not cached.get("manifest"):
            raise CharacterBootstrapError("character_cache_failed", "Character references did not produce a usable manifest.", 503)
        manifest_path = Path(str(cached["manifest"])).resolve()
        self._require_usable_manifest(manifest_path, character, version)
        entry = self._registry_entry(character, version, profile, manifest_path)
        contract = build_character_contract(profile, entry)
        contract_path = manifest_path.parent / "character_contract_v1.json"
        self._write_json_atomic(contract_path, contract)
        entry["character_contract"] = self._storage_relative(contract_path)
        with _REGISTRY_LOCK:
            characters = load_characters(self.characters_path)
            existing = registered_character_name(character, self.characters_path)
            if existing is None:
                raise CharacterBootstrapError("character_not_registered", "Character must be registered before revalidation.", 404)
            characters[existing] = entry
            self._write_registry(characters)
        return {"status": "revalidated", "character": existing, "registered": True, "manifest": entry["refs_manifest"], "character_contract": entry["character_contract"], "reference_status": entry.get("reference_status", "READY"), "identity_resolution": identity}

    def _require_usable_manifest(self, path: Path, character: str, version: str | None) -> None:
        try:
            path.relative_to(self.refs_root)
            manifest = load_character_reference_manifest(path)
            refs = manifest["canonical_references"]
            required = 1 if manifest.get("schema_version") == 2 else 2
            if not (
                manifest.get("usable") is True
                and manifest.get("character") == character
                and manifest.get("version") == version
                and isinstance(refs, list)
                and len(refs) >= required
            ):
                raise ValueError("manifest metadata mismatch")
            directory = path.parent
            for ref in refs:
                relative = Path(str(ref.get("file") or ""))
                if relative.is_absolute() or ".." in relative.parts or not (directory / relative).is_file():
                    raise ValueError("manifest reference file missing")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            raise CharacterBootstrapError(
                "character_cache_failed", f"Character reference manifest is not usable: {exc}", 503
            ) from exc

    def _registry_entry(
        self, character: str, version: str | None, profile: dict[str, Any], manifest_path: Path
    ) -> dict[str, Any]:
        identity = profile.get("identity_resolution", {}) if isinstance(profile.get("identity_resolution"), dict) else {}
        copyright_tags = self._strings(identity.get("franchise") or profile.get("copyright"))
        characteristics = self._strings(identity.get("characteristics") or profile.get("characteristics"))
        clothing = self._strings(identity.get("clothing") or profile.get("clothing"))
        manifest = load_character_reference_manifest(manifest_path)
        return {
            "name": identity.get("canonical_name") or character,
            "franchise": copyright_tags[0] if copyright_tags else "",
            "universe": copyright_tags[0] if copyright_tags else "",
            "tags": list(dict.fromkeys(characteristics + clothing)),
            "canonical_tag": identity.get("canonical_tag") or profile["matched_tag"],
            "aliases": self._strings(identity.get("aliases")),
            "copyright": copyright_tags,
            "characteristics": characteristics,
            "clothing": clothing,
            "version": version,
            "refs_manifest": self._storage_relative(manifest_path),
            "reference_status": manifest.get("reference_status", "READY"),
            "reference_count": manifest.get("reference_count", len(manifest["canonical_references"])),
            "reference_confidence": manifest.get("reference_confidence", 0.0),
        }

    def _write_registry(self, characters: dict[str, Any]) -> None:
        self._write_json_atomic(self.characters_path, characters)

    @staticmethod
    def _write_json_atomic(path: Path, value: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(path)

    @staticmethod
    def _strings(value: Any) -> list[str]:
        if not isinstance(value, list):
            return []
        return [item for item in value if isinstance(item, str) and item.strip()]

    @staticmethod
    def _clean(value: str, field: str) -> str:
        if not isinstance(value, str):
            raise CharacterBootstrapError("invalid_character", f"{field} must be text", 400)
        cleaned = " ".join(value.split()).strip()
        if not cleaned or len(cleaned) > 120:
            raise CharacterBootstrapError(
                "invalid_character", f"{field} must contain between 1 and 120 characters", 400
            )
        return cleaned


def bootstrap_character(
    character: str,
    version: str | None = None,
    characters_path: Path = CHARACTERS_PATH,
) -> dict[str, Any]:
    return CharacterBootstrapService(characters_path=characters_path).bootstrap(character, version)
