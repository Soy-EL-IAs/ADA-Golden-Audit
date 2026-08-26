#!/usr/bin/env python3
"""Small, conservative downloader for reusable character references."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

if __package__:
    from .ada_paths import CHARACTER_REFS_ROOT
    from .character_reference_manifest import load_character_reference_manifest
    from .character_refs import CharacterReferenceFinder
else:
    from ada_paths import CHARACTER_REFS_ROOT
    from character_reference_manifest import load_character_reference_manifest
    from character_refs import CharacterReferenceFinder


class CharacterReferenceCache:
    """Cache two to five selected references without replacing prior content."""

    def __init__(self, finder: CharacterReferenceFinder, root: Path | None = None, identity_validator: Any | None = None) -> None:
        self.finder = finder
        self.root = (root or CHARACTER_REFS_ROOT).resolve()
        self.config = finder.config.get("cache", {})
        self.identity_validator = identity_validator

    def cache(self, character: str, version: str | None = None, limit: int | None = None, *, identity: dict[str, Any] | None = None, force: bool = False) -> dict[str, Any]:
        character = self._clean(character, "character")
        version = self._clean(version, "version") if version else None
        acceptance = self.finder.config.get("acceptance", {}) if isinstance(self.finder.config.get("acceptance"), dict) else {}
        # New resolved onboarding accepts one strong canonical reference.  The
        # legacy call shape retains its old two-reference requirement.
        minimum = int(acceptance.get("limited_reference_count", 1)) if identity else int(self.config.get("minimum_refs", 2))
        maximum = int(self.config.get("maximum_refs", 5))
        requested = maximum if limit is None else limit
        if not minimum <= requested <= maximum:
            raise ValueError(f"limit must be between {minimum} and {maximum}")

        canonical_id = str(identity.get("character_id") or identity.get("canonical_tag") or character) if identity else character
        target = self.root / self._slug(canonical_id) / self._slug(version or "default")
        if target.exists():
            existing = self._usable_manifest(target, character, version, minimum)
            if existing is not None and not force:
                return {
                    "status": "cached",
                    "cache_hit": True,
                    "usable": True,
                    "directory": str(target),
                    "manifest": str(target / "manifest.json"),
                    "count": len(existing["canonical_references"]),
                    "refs": existing["canonical_references"],
                }
            # Preserve the failed attempt outside the active lookup path, then
            # retry only because this bootstrap was explicitly requested.
            archived = self._archive_incomplete(target)

        found = self.finder.find_resolved(identity, requested) if identity else self.finder.find(character, version, requested)
        selected = self._select(found.get("refs", []), requested, minimum)
        if len(selected) < minimum:
            return {
                "status": "insufficient_refs",
                "cache_hit": False,
                "usable": False,
                "character": character,
                "version": version,
                "selected": len(selected),
                "required": minimum,
                "message": "reference discovery did not return enough eligible references",
            }

        refs_dir = target / "refs"
        refs_dir.mkdir(parents=True, exist_ok=False)
        created_at = self._now()
        downloaded: list[dict[str, Any]] = []
        errors: list[dict[str, str]] = []
        duplicate_hashes: list[dict[str, str]] = []
        seen_hashes: set[str] = set()

        for candidate_index, candidate in enumerate(selected, start=1):
            image_url = str(candidate["image_url"])
            try:
                data, extension = self._download_once(image_url)
                digest = hashlib.sha256(data).hexdigest()
                if digest in seen_hashes:
                    duplicate_hashes.append({"source_url": image_url, "sha256": digest})
                    continue
                filename = f"ref_{candidate_index:02d}{extension}"
                relative_file = Path("refs") / filename
                with (target / relative_file).open("xb") as output:
                    output.write(data)
                identity_validation = candidate.get("identity_validation", {"status": "legacy"})
                if identity and candidate.get("source_tier") == "unknown":
                    if self.identity_validator is None:
                        errors.append({"source_url": image_url, "page_url": str(candidate.get("source_page") or candidate.get("source_url") or ""), "error": "unknown provenance requires compact visual identity validation"})
                        continue
                    identity_validation = self.identity_validator.validate(target / relative_file, identity)
                    if not identity_validation.get("identity_match") or float(identity_validation.get("confidence", 0)) < 0.70:
                        errors.append({"source_url": image_url, "page_url": str(candidate.get("source_page") or candidate.get("source_url") or ""), "error": "compact visual identity validation rejected candidate"})
                        continue
                seen_hashes.add(digest)
                provenance = {
                    "source_page": candidate.get("source_page") or candidate.get("source_url", ""),
                    "image_url": image_url,
                    "source_tier": candidate.get("source_tier", "unknown"),
                    "trust_origin": candidate.get("trust_origin", "image_host"),
                    "discovered_via": candidate.get("discovered_via", "legacy_discovery"),
                }
                downloaded.append({
                    "file": relative_file.as_posix(),
                    "source_url": image_url,
                    "page_url": provenance["source_page"],
                    "domain": candidate["domain"],
                    "final_score": candidate["final_score"],
                    "recommendation": candidate["recommendation"],
                    "provenance": provenance,
                    "identity_confidence": identity_validation.get("confidence", candidate.get("identity_confidence", round(float(candidate.get("character_relevance", 0)) / 100, 2))),
                    "reference_utility": candidate.get("reference_utility", round(float(candidate.get("image_quality", 0)) / 100, 2)),
                    "identity_validation": identity_validation,
                    "sha256": digest,
                    "downloaded_at": self._now(),
                })
            except (OSError, RuntimeError, ValueError, urllib.error.HTTPError, urllib.error.URLError) as exc:
                errors.append({
                    "source_url": image_url,
                    "page_url": str(candidate.get("source_url") or ""),
                    "error": str(exc),
                })

        strong_threshold = float(acceptance.get("strong_reference_confidence", 0.80))
        strong = [ref for ref in downloaded if float(ref.get("identity_confidence", 0)) >= strong_threshold]
        ready_count = int(acceptance.get("ready_reference_count", 2))
        reference_status = "READY" if len(strong) >= ready_count else ("READY_WITH_LIMITED_REFERENCES" if strong else "BLOCKED")
        usable = len(downloaded) >= minimum and reference_status != "BLOCKED"
        manifest = {
            "schema_version": 2 if identity else 1,
            "character": character,
            "version": version,
            "created_at": created_at,
            "status": "downloaded" if usable else "incomplete",
            "usable": usable,
            "provider": found.get("provider", "searxng"),
            "source_query": found.get("queries_used", [None])[0] if found.get("queries_used") else None,
            "searches": found.get("queries_used", []),
            "refs": downloaded,
            "character_id": identity.get("character_id") if identity else self._slug(character),
            "canonical_name": identity.get("canonical_name") if identity else character,
            "franchise": identity.get("franchise", []) if identity else [],
            "identity_resolution": {"canonical_tag": identity.get("canonical_tag"), "source": identity.get("source", "danbooru_taxonomy"), "aliases": identity.get("aliases", [])} if identity else {},
            "canonical_references": downloaded,
            "generated_identity_references": [],
            "reference_status": reference_status,
            "reference_count": len(downloaded),
            "reference_confidence": round(sum(float(ref.get("identity_confidence", 0)) for ref in downloaded) / len(downloaded), 2) if downloaded else 0.0,
            "discovery": {key: found.get(key) for key in ("queries_used", "raw_candidate_count", "page_fetch_errors", "rejected") if key in found},
            "errors": errors,
            "duplicate_hashes": duplicate_hashes,
        }
        manifest_path = target / "manifest.json"
        with manifest_path.open("x", encoding="utf-8") as output:
            json.dump(manifest, output, ensure_ascii=False, indent=2)
            output.write("\n")

        return {
            "status": manifest["status"],
            "cache_hit": False,
            "usable": usable,
            "directory": str(target),
            "manifest": str(manifest_path),
            "count": len(downloaded),
            "failed": len(errors),
            "duplicates": len(duplicate_hashes),
            "refs": downloaded,
            "reference_status": reference_status,
            "errors": errors,
            "replaced_incomplete_cache": str(archived) if 'archived' in locals() else None,
        }

    def _archive_incomplete(self, target: Path) -> Path:
        relative = target.relative_to(self.root)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        archive = self.root / "_failed" / relative.parent / f"{relative.name}_{timestamp}"
        archive.parent.mkdir(parents=True, exist_ok=True)
        target.rename(archive)
        return archive

    @staticmethod
    def _select(refs: list[dict[str, Any]], limit: int, minimum: int) -> list[dict[str, Any]]:
        unique: list[dict[str, Any]] = []
        seen: set[str] = set()
        for ref in refs:
            image_url = str(ref.get("image_url") or "").strip()
            key = CharacterReferenceCache._normalized_url(image_url)
            if not image_url or key in seen:
                continue
            seen.add(key)
            unique.append(ref)

        # v2 discovery has already passed explicit eligibility gates.  Its
        # legacy aggregate recommendation may be "reject" solely because the
        # old trust-weighted score had an impossible unknown-source ceiling.
        v2 = [ref for ref in unique if "identity_confidence" in ref and "reference_utility" in ref]
        if v2:
            return v2[:limit]
        selected = [ref for ref in unique if ref.get("recommendation") == "auto"][:limit]
        if len(selected) < minimum:
            for ref in unique:
                if ref.get("recommendation") != "review" or ref in selected:
                    continue
                selected.append(ref)
                if len(selected) >= minimum:
                    break
        return selected

    def _download_once(self, url: str) -> tuple[bytes, str]:
        request = urllib.request.Request(
            url,
            headers={"Accept": "image/avif,image/webp,image/png,image/jpeg", "User-Agent": "illustrious-klein-ref-cache/1.0"},
        )
        timeout = int(self.config.get("timeout_seconds", 30))
        max_bytes = int(self.config.get("max_image_bytes", 20_000_000))
        with urllib.request.urlopen(request, timeout=timeout) as response:
            content_type = response.headers.get_content_type().lower()
            data = response.read(max_bytes + 1)
        if len(data) > max_bytes:
            raise ValueError(f"image exceeds {max_bytes} bytes")
        extension = self._image_extension(data)
        if extension is None:
            raise ValueError(f"unsupported or invalid image content type: {content_type}")
        return data, extension

    @staticmethod
    def _image_extension(data: bytes) -> str | None:
        if data.startswith(b"\xff\xd8\xff"):
            return ".jpg"
        if data.startswith(b"\x89PNG\r\n\x1a\n"):
            return ".png"
        if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
            return ".webp"
        if len(data) >= 12 and data[4:8] == b"ftyp" and b"avif" in data[8:32]:
            return ".avif"
        return None

    @staticmethod
    def _usable_manifest(
        target: Path,
        character: str,
        version: str | None,
        minimum: int,
    ) -> dict[str, Any] | None:
        manifest_path = target / "manifest.json"
        try:
            manifest = load_character_reference_manifest(manifest_path)
        except (OSError, ValueError, json.JSONDecodeError):
            return None
        if manifest.get("character") != character or manifest.get("version") != version:
            return None
        refs = manifest["canonical_references"]
        if not isinstance(refs, list) or len(refs) < minimum:
            return None
        for ref in refs:
            relative = Path(str(ref.get("file") or ""))
            digest = str(ref.get("sha256") or "")
            if relative.is_absolute() or ".." in relative.parts or not re.fullmatch(r"[0-9a-f]{64}", digest):
                return None
            path = target / relative
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                return None
            provenance = ref.get("provenance", {}) if isinstance(ref.get("provenance"), dict) else {}
            if manifest.get("schema_version") == 2 and provenance.get("source_tier") == "unknown":
                if ref.get("identity_validation", {}).get("status") != "visual_identity_validation":
                    return None
        return manifest

    @staticmethod
    def _slug(value: str) -> str:
        ascii_text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
        slug = re.sub(r"[^a-z0-9]+", "_", ascii_text.lower()).strip("_")
        if not slug:
            raise ValueError("character/version cannot produce an empty cache slug")
        return slug

    @staticmethod
    def _clean(value: str, field: str) -> str:
        cleaned = " ".join(value.split()).strip()
        if not cleaned or len(cleaned) > 120:
            raise ValueError(f"{field} must contain between 1 and 120 characters")
        return cleaned

    @staticmethod
    def _normalized_url(url: str) -> str:
        parsed = urllib.parse.urlsplit(url)
        host = (parsed.hostname or "").lower()
        path = re.sub(r"/+", "/", urllib.parse.unquote(parsed.path)).rstrip("/")
        return f"{host}{path}".lower()

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()
