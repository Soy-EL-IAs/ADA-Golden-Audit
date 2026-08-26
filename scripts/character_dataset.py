#!/usr/bin/env python3
"""Prepare and persist Master-authored character prompt datasets."""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

if __package__:
    from .ada_paths import (
        ADA_ROOT, CHARACTER_DATASET_STAGING_ROOT, CHARACTER_REFS_ROOT,
        CONFIG_ROOT, PROMPTS_ROOT,
    )
    from .character_profile import CharacterProfileDatabase
    from .character_reference_manifest import load_character_reference_manifest
    from .prompt_guides import PromptGuideLibrary
    from .run_klein_jsonl_batch import (
        apply_klein_preset,
        bind_record,
        compile_api,
        load_dataset,
        load_klein_preset_plan,
    )
else:
    from ada_paths import (
        ADA_ROOT, CHARACTER_DATASET_STAGING_ROOT, CHARACTER_REFS_ROOT,
        CONFIG_ROOT, PROMPTS_ROOT,
    )
    from character_profile import CharacterProfileDatabase
    from character_reference_manifest import load_character_reference_manifest
    from prompt_guides import PromptGuideLibrary
    from run_klein_jsonl_batch import (
        apply_klein_preset,
        bind_record,
        compile_api,
        load_dataset,
        load_klein_preset_plan,
    )

DEFAULT_CONFIG = CONFIG_ROOT / "character_dataset.json"
DATASET_ID_RE = re.compile(r"[a-z0-9][a-z0-9_-]{0,79}")
RECORD_ID_RE = re.compile(r"[a-z0-9][a-z0-9_-]{0,119}")
FORBIDDEN_COMPOSITION_RE = re.compile(
    r"\b(camera|lens|photographer|filming)\b|photography equipment|filming equipment|visible lens",
    re.IGNORECASE,
)
COMPOSITION_RE = re.compile(
    r"\b(viewpoint|framing|eye-level view|low-angle view|high-angle view|"
    r"three-quarter view|profile view|tight close-up|full-body)\b",
    re.IGNORECASE,
)


class CharacterDatasetBuilder:
    """Keep mechanical preparation/persistence separate from Master creativity."""

    def __init__(
        self,
        config_path: Path = DEFAULT_CONFIG,
        prompts_root: Path | None = None,
        refs_root: Path | None = None,
        workflow_path: Path | None = None,
        prompt_guides: PromptGuideLibrary | None = None,
    ) -> None:
        self.config = json.loads(config_path.read_text(encoding="utf-8"))
        self.prompts_root = (prompts_root or PROMPTS_ROOT).resolve()
        self.config_root = CONFIG_ROOT.resolve()
        self.refs_root = (refs_root or CHARACTER_REFS_ROOT).resolve()
        configured_staging = self.config.get("staging_root", "data/tmp/character_dataset_staging")
        self.staging_root = (CHARACTER_DATASET_STAGING_ROOT if configured_staging in {"character_dataset_staging", "data/tmp/character_dataset_staging"}
                             else ADA_ROOT / configured_staging).resolve()
        self.workflow_path = workflow_path.resolve() if workflow_path is not None else None
        self.character_profiles = CharacterProfileDatabase()
        self.prompt_guides = prompt_guides or PromptGuideLibrary()

    def prepare(
        self,
        character: str,
        version: str | None = None,
        count: int = 20,
        dataset_id: str | None = None,
        categories: list[str] | None = None,
    ) -> dict[str, Any]:
        """Create a new, empty staging plan and return the creative contract."""
        character, version, count, dataset_id = self._normalize_request(character, version, count, dataset_id)
        dataset_path, preset_path = self._target_paths(dataset_id)
        self._require_new_targets(dataset_path, preset_path)
        staging_dir, metadata_path, _ = self._staging_paths(dataset_id)
        if staging_dir.exists():
            raise FileExistsError(f"Staging already exists and will not be overwritten: {staging_dir}")
        category_plan = self._category_plan(count, categories)
        distribution = self._distribution_from_plan(category_plan)
        refs = self._cached_refs(character, version)
        profile = self.get_character_profile(character, version)
        metadata = {
            "schema_version": 1,
            "status": "staging",
            "character": character,
            "version": version,
            "count": count,
            "dataset_id": dataset_id,
            "dataset": self._relative(dataset_path),
            "preset_plan": self._relative(preset_path),
            "refs_cache_used": refs["used"],
            "refs_manifest": refs["manifest"],
            "character_profile_used": profile["character_profile_used"],
            "character_profile": profile,
            "categories_plan": category_plan,
            "categories_explicit": categories is not None,
            "distribution": distribution,
            "prompt_guide_manifest": self.prompt_guides.manifest(),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        try:
            staging_dir.mkdir(parents=True, exist_ok=False)
            with metadata_path.open("x", encoding="utf-8") as output:
                json.dump(metadata, output, ensure_ascii=False, indent=2)
                output.write("\n")
        except Exception:
            if staging_dir.exists() and not any(staging_dir.iterdir()):
                staging_dir.rmdir()
            raise
        return self._prepared_response(metadata, refs["refs"], staging_dir)

    def get_character_profile(self, character: str, version: str | None = None) -> dict[str, Any]:
        """Return source tags from the local character DB without writing or searching."""
        return self.character_profiles.get_character_profile(character, version)

    def proposal_brief(
        self,
        character: str,
        version: str | None = None,
        count: int = 20,
        categories: list[str] | None = None,
    ) -> dict[str, Any]:
        """Build a non-persistent premise-generation brief for a dry run."""
        character, version, count, _ = self._normalize_request(character, version, count, "dry_run")
        category_plan = self._category_plan(count, categories)
        profile = self.get_character_profile(character, version)
        return {
            "character": character,
            "version": version,
            "count": count,
            "categories_plan": category_plan,
            "distribution": self._distribution_from_plan(category_plan),
            "character_profile_used": profile["character_profile_used"],
            "character_profile": profile,
            "prompt_rules": self.config["prompt_rules"],
            "proposal_guidance": self.prompt_guides.proposal_context(),
            "prompt_guide_manifest": self.prompt_guides.manifest(),
        }

    def persist(
        self,
        character: str,
        entries: list[dict[str, Any]],
        version: str | None = None,
        count: int = 20,
        dataset_id: str | None = None,
    ) -> dict[str, Any]:
        """Compatibility path for small datasets; new Master flows should append/finalize."""
        prepared = self.prepare(character, version, count, dataset_id)
        self.append(prepared["dataset_id"], entries)
        return self.finalize(character, version, count, prepared["dataset_id"])

    def append(self, dataset_id: str, entries: list[dict[str, Any]]) -> dict[str, Any]:
        """Persist one small chunk after only local structural/duplicate checks."""
        metadata, _, entries_path = self._load_staging(dataset_id)
        if metadata.get("status") != "staging":
            raise ValueError(f"Staging is not appendable: {dataset_id}")
        maximum = int(self.config.get("maximum_chunk_size", 10))
        if not isinstance(entries, list) or not 1 <= len(entries) <= maximum:
            raise ValueError(f"entries must contain between 1 and {maximum} objects per chunk")
        existing = self._read_staged_entries(entries_path)
        if len(existing) + len(entries) > int(metadata["count"]):
            raise ValueError("chunk would exceed the planned dataset count")
        normalized = self._validate_chunk(entries, set(metadata["distribution"]), existing)
        if metadata.get("categories_explicit"):
            planned = metadata.get("categories_plan")
            if not isinstance(planned, list):
                raise ValueError("Explicit category plan is missing from staging metadata")
            staged_counts = Counter(str(entry.get("category")) for entry in [*existing, *normalized])
            allowed_counts = self._distribution_from_plan(planned)
            if any(staged_counts[category] > allowed_counts[category] for category in allowed_counts):
                raise ValueError("chunk exceeds the explicit category plan")
        with entries_path.open("a", encoding="utf-8") as output:
            for entry in normalized:
                output.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return {
            "status": "accepted",
            "dataset_id": dataset_id,
            "accepted": len(normalized),
            "total_staged": len(existing) + len(normalized),
        }

    def finalize(
        self,
        character: str,
        version: str | None,
        count: int,
        dataset_id: str,
    ) -> dict[str, Any]:
        """Run global validation and create final outputs; retain staging on every failure."""
        character, version, count, dataset_id = self._normalize_request(character, version, count, dataset_id)
        metadata, metadata_path, entries_path = self._load_staging(dataset_id)
        category_plan = metadata.get("categories_plan")
        if category_plan is None:
            # Backward compatibility for staging directories created before
            # explicit category plans existed.
            category_plan = self._category_plan(count, None)
        else:
            category_plan = self._category_plan(count, category_plan)
        expected = {
            "character": character,
            "version": version,
            "count": count,
            "dataset_id": dataset_id,
            "distribution": self._distribution_from_plan(category_plan),
        }
        for key, value in expected.items():
            if metadata.get(key) != value:
                raise ValueError(f"Staging metadata does not match finalize argument: {key}")
        if metadata.get("categories_plan") is not None and metadata["categories_plan"] != category_plan:
            raise ValueError("Staging category plan does not match its validated plan")
        if metadata.get("status") != "staging":
            raise ValueError(f"Staging is not finalizable: {dataset_id}")
        dataset_path, preset_path = self._target_paths(dataset_id)
        self._require_new_targets(dataset_path, preset_path)
        records, actual_distribution = self._validate_entries(
            character, version, count, self._read_staged_entries(entries_path), expected["distribution"]
        )
        result = self._write_final_outputs(
            character, version, dataset_id, records, actual_distribution, metadata
        )
        metadata["status"] = "finalized"
        metadata["finalized_at"] = datetime.now(timezone.utc).isoformat()
        metadata["total_staged"] = len(records)
        metadata["final_dataset"] = result["dataset"]
        metadata["final_preset_plan"] = result["preset_plan"]
        metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return result

    def _write_final_outputs(
        self,
        character: str,
        version: str | None,
        dataset_id: str,
        records: list[dict[str, Any]],
        actual_distribution: dict[str, int],
        metadata: dict[str, Any],
    ) -> dict[str, Any]:
        dataset_path, preset_path = self._target_paths(dataset_id)
        preset_document = self._preset_document(dataset_id, records)
        resolved_presets = self._resolve_presets_in_memory(preset_document, records)
        dataset_text = "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records)
        preset_text = json.dumps(preset_document, ensure_ascii=False, indent=2) + "\n"
        dataset_created = False
        preset_created = False
        try:
            dataset_path.parent.mkdir(parents=True, exist_ok=True)
            preset_path.parent.mkdir(parents=True, exist_ok=True)
            with dataset_path.open("x", encoding="utf-8") as output:
                output.write(dataset_text)
            dataset_created = True
            with preset_path.open("x", encoding="utf-8") as output:
                output.write(preset_text)
            preset_created = True
            saved_records = load_dataset(dataset_path, take=None)
            saved_presets = load_klein_preset_plan(preset_path, saved_records)
        except Exception:
            if preset_created:
                preset_path.unlink(missing_ok=True)
            if dataset_created:
                dataset_path.unlink(missing_ok=True)
            raise
        return {
            "status": "valid",
            "character": character,
            "version": version,
            "count": len(records),
            "dataset_id": dataset_id,
            "dataset": self._relative(dataset_path),
            "preset_plan": self._relative(preset_path),
            "refs_cache_used": metadata["refs_cache_used"],
            "refs_manifest": metadata["refs_manifest"],
            "distribution": actual_distribution,
            "validation": {
                "jsonl_parseable": True,
                "unique_ids": True,
                "valid_seeds": True,
                "preset_coverage_exact": True,
                "workflow_compile_all_records": True,
                "comfyui_executed": False,
            },
            "run_batch_args": {
                "dataset": self._relative(dataset_path),
                "batch_id": f"{dataset_id}_001",
                "klein_preset_plan": self._relative(preset_path),
            },
        }

    def _prepared_response(
        self,
        metadata: dict[str, Any],
        refs_context: list[dict[str, Any]],
        staging_dir: Path,
    ) -> dict[str, Any]:
        return {
            "status": "ready_for_master",
            "phase": "prepare",
            **{key: metadata[key] for key in (
                "character", "version", "count", "dataset_id", "dataset", "preset_plan",
                "refs_cache_used", "refs_manifest", "character_profile_used", "character_profile", "categories_plan",
                "categories_explicit", "distribution", "prompt_guide_manifest",
            )},
            "refs_context": refs_context,
            "staging": self._relative(staging_dir),
            "maximum_chunk_size": int(self.config.get("maximum_chunk_size", 10)),
            "categories": list(metadata["distribution"]),
            "prompt_rules": self.config["prompt_rules"],
            "proposal_guidance": self.prompt_guides.proposal_context(),
            "entry_schema": {
                "required": [
                    "id", "category", "premise", "illustrious_prompt", "klein_prompt",
                    "illustrious_seed", "klein_seed",
                ],
                "category_values": list(metadata["distribution"]),
            },
            "next_action": (
                "First author the requested premises using proposal_guidance. Then call "
                "get_character_dataset_prompt_guidance(dataset_id) before writing Illustrious and Klein prompts. "
                "The Master must author 5-10 entries at a time, call append_character_dataset_entries "
                "for each chunk, then call finalize_character_dataset once all entries are staged. "
                "When character_profile_used is true, use its characteristics and clothing as local identity "
                "facts, without mechanically concatenating tags or contradicting them. Do not call search or "
                "cache tools automatically. The returned character_profile is already the local lookup result: "
                "continue directly to authoring and append_character_dataset_entries. Call "
                "get_character_profile only when the user explicitly requests profile inspection or debugging."
            ),
        }

    def get_prompt_guidance(self, dataset_id: str) -> dict[str, Any]:
        """Return only the full guides needed after premise selection."""
        metadata, _, _ = self._load_staging(dataset_id)
        if metadata.get("status") != "staging":
            raise ValueError(f"Staging is not active: {dataset_id}")
        if metadata.get("prompt_guide_manifest") != self.prompt_guides.manifest():
            raise ValueError(
                "Active prompt-guide versions changed after this staging plan was created; "
                "start a new plan or restore the recorded versions before continuing"
            )
        return {"dataset_id": dataset_id, "character": metadata["character"], "version": metadata["version"],
                "prompt_guide_manifest": metadata["prompt_guide_manifest"],
                "prompt_guidance": self.prompt_guides.prompt_context()}

    def _staging_paths(self, dataset_id: str) -> tuple[Path, Path, Path]:
        directory = self.staging_root / dataset_id
        return directory, directory / "metadata.json", directory / "entries.jsonl"

    def _load_staging(self, dataset_id: str) -> tuple[dict[str, Any], Path, Path]:
        if not isinstance(dataset_id, str) or not DATASET_ID_RE.fullmatch(dataset_id):
            raise ValueError("dataset_id must use lowercase letters, digits, underscores or hyphens")
        _, metadata_path, entries_path = self._staging_paths(dataset_id)
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise FileNotFoundError(f"No usable staging plan for {dataset_id}") from exc
        if not isinstance(metadata, dict) or metadata.get("dataset_id") != dataset_id:
            raise ValueError(f"Invalid staging metadata for {dataset_id}")
        return metadata, metadata_path, entries_path

    @staticmethod
    def _read_staged_entries(entries_path: Path) -> list[dict[str, Any]]:
        if not entries_path.exists():
            return []
        entries: list[dict[str, Any]] = []
        for line_number, raw in enumerate(entries_path.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            try:
                entry = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{entries_path}:{line_number}: invalid staged JSON") from exc
            if not isinstance(entry, dict):
                raise ValueError(f"{entries_path}:{line_number}: staged entry must be an object")
            entries.append(entry)
        return entries

    def _validate_chunk(
        self,
        entries: list[dict[str, Any]],
        categories: set[str],
        existing: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        ids = {str(entry.get("id") or "").strip().lower() for entry in existing}
        illustrious_seeds = {entry.get("illustrious_seed") for entry in existing}
        klein_seeds = {entry.get("klein_seed") for entry in existing}
        normalized: list[dict[str, Any]] = []
        for index, entry in enumerate(entries, 1):
            if not isinstance(entry, dict):
                raise ValueError(f"entry {index} must be an object")
            if not isinstance(entry.get("id"), str) or not isinstance(entry.get("category"), str):
                raise ValueError(f"entry {index} id and category must be text")
            record_id = entry["id"].strip().lower()
            category = entry["category"].strip().lower().replace("-", "").replace("_", "")
            if not RECORD_ID_RE.fullmatch(record_id) or record_id in ids:
                raise ValueError(f"entry {index} id is invalid or already staged")
            if category not in categories:
                raise ValueError(f"entry {record_id} has invalid category {category!r}")
            normalized_entry = {
                "id": record_id,
                "category": category,
            "premise": self._entry_text(entry, "premise", index, None),
                "illustrious_prompt": self._entry_text(entry, "illustrious_prompt", index, 3000),
                "klein_prompt": self._entry_text(entry, "klein_prompt", index, 3000),
                "illustrious_seed": self._seed(entry.get("illustrious_seed"), record_id, "illustrious_seed"),
                "klein_seed": self._seed(entry.get("klein_seed"), record_id, "klein_seed"),
            }
            if normalized_entry["illustrious_seed"] in illustrious_seeds or normalized_entry["klein_seed"] in klein_seeds:
                raise ValueError(f"entry {record_id} repeats a seed already staged")
            ids.add(record_id)
            illustrious_seeds.add(normalized_entry["illustrious_seed"])
            klein_seeds.add(normalized_entry["klein_seed"])
            normalized.append(normalized_entry)
        return normalized

    def _normalize_request(
        self,
        character: str,
        version: str | None,
        count: int,
        dataset_id: str | None,
    ) -> tuple[str, str | None, int, str]:
        character = self._clean(character, "character")
        version = self._clean(version, "version") if version else None
        maximum = int(self.config.get("maximum_count", 100))
        if not isinstance(count, int) or isinstance(count, bool) or not 1 <= count <= maximum:
            raise ValueError(f"count must be an integer between 1 and {maximum}")
        generated_id = "_".join(part for part in (self._slug(character), self._slug(version) if version else None, str(count)) if part)
        if dataset_id is not None and not isinstance(dataset_id, str):
            raise ValueError("dataset_id must be text or null")
        dataset_id = generated_id if dataset_id is None else dataset_id.strip().lower()
        if not DATASET_ID_RE.fullmatch(dataset_id):
            raise ValueError("dataset_id must use 1-80 lowercase letters, digits, underscores or hyphens")
        return character, version, count, dataset_id

    def _target_paths(self, dataset_id: str) -> tuple[Path, Path]:
        return (
            self.prompts_root / f"{dataset_id}.jsonl",
            self.config_root / f"klein_presets_{dataset_id}.json",
        )

    @staticmethod
    def _require_new_targets(dataset_path: Path, preset_path: Path) -> None:
        existing = [str(path) for path in (dataset_path, preset_path) if path.exists()]
        if existing:
            raise FileExistsError("Refusing to overwrite existing dataset/config: " + ", ".join(existing))

    def _category_plan(self, count: int, categories: list[str] | None) -> list[str]:
        valid = list(self.config["category_order"])
        if categories is None:
            return [valid[index % len(valid)] for index in range(count)]
        if not isinstance(categories, list) or len(categories) != count:
            raise ValueError("categories must be a list with exactly count values")
        plan: list[str] = []
        for index, category in enumerate(categories, 1):
            if not isinstance(category, str):
                raise ValueError(f"categories[{index}] must be text")
            value = category.strip().lower()
            if value not in valid:
                raise ValueError(f"categories[{index}] must be one of {valid}")
            plan.append(value)
        return plan

    def _distribution_from_plan(self, category_plan: list[str]) -> dict[str, int]:
        distribution = {category: 0 for category in self.config["category_order"]}
        for category in category_plan:
            distribution[category] += 1
        return distribution

    def _validate_entries(
        self,
        character: str,
        version: str | None,
        count: int,
        entries: list[dict[str, Any]],
        expected_distribution: dict[str, int],
    ) -> tuple[list[dict[str, Any]], dict[str, int]]:
        if not isinstance(entries, list) or len(entries) != count:
            raise ValueError(f"entries must contain exactly {count} objects")
        categories = set(expected_distribution)
        ids: set[str] = set()
        illustrious_seeds: set[int] = set()
        klein_seeds: set[int] = set()
        premises: set[str] = set()
        prompt_pairs: set[tuple[str, str]] = set()
        distribution: Counter[str] = Counter()
        records: list[dict[str, Any]] = []
        character_label = f"{character} / {version}" if version else character
        character_tokens = [token for token in re.findall(r"[a-z0-9]+", character.lower()) if len(token) > 1]

        for index, entry in enumerate(entries, 1):
            if not isinstance(entry, dict):
                raise ValueError(f"entry {index} must be an object")
            if not isinstance(entry.get("id"), str) or not isinstance(entry.get("category"), str):
                raise ValueError(f"entry {index} id and category must be text")
            record_id = entry["id"].strip().lower()
            category = entry["category"].strip().lower().replace("-", "").replace("_", "")
            category = {"fullbody": "fullbody", "closeup": "closeup"}.get(category, category)
            premise = self._entry_text(entry, "premise", index, None)
            illustrious = self._entry_text(entry, "illustrious_prompt", index, 3000)
            klein = self._entry_text(entry, "klein_prompt", index, 3000)
            if not RECORD_ID_RE.fullmatch(record_id) or record_id in ids:
                raise ValueError(f"entry {index} id must be unique and use lowercase letters, digits, _ or -")
            if category not in categories:
                raise ValueError(f"entry {record_id} has invalid category {category!r}")
            if premise.casefold() in premises:
                raise ValueError(f"entry {record_id} repeats a premise")
            if (illustrious.casefold(), klein.casefold()) in prompt_pairs:
                raise ValueError(f"entry {record_id} repeats a prompt pair")
            for field, prompt in (("illustrious_prompt", illustrious), ("klein_prompt", klein)):
                match = FORBIDDEN_COMPOSITION_RE.search(prompt)
                if match:
                    raise ValueError(f"entry {record_id} {field} contains forbidden physical-device term: {match.group(0)}")
                if character_tokens and not any(token in prompt.casefold() for token in character_tokens):
                    raise ValueError(f"entry {record_id} {field} must name the requested character")
                if not COMPOSITION_RE.search(prompt):
                    raise ValueError(f"entry {record_id} {field} must describe viewpoint or framing")
            illustrious_seed = self._seed(entry.get("illustrious_seed"), record_id, "illustrious_seed")
            klein_seed = self._seed(entry.get("klein_seed"), record_id, "klein_seed")
            if illustrious_seed in illustrious_seeds or klein_seed in klein_seeds:
                raise ValueError(f"entry {record_id} repeats a seed within its stage")

            ids.add(record_id)
            premises.add(premise.casefold())
            prompt_pairs.add((illustrious.casefold(), klein.casefold()))
            illustrious_seeds.add(illustrious_seed)
            klein_seeds.add(klein_seed)
            distribution[category] += 1
            records.append({
                "id": record_id,
                "character": character_label,
                "category": category,
                "premise": premise,
                "illustrious_prompt": illustrious,
                "klein_prompt": klein,
                "illustrious_seed": illustrious_seed,
                "klein_seed": klein_seed,
            })

        actual = {category: distribution[category] for category in expected_distribution}
        if actual != expected_distribution:
            raise ValueError(f"category distribution must be {expected_distribution}, got {actual}")
        return records, actual

    def _preset_document(self, dataset_id: str, records: list[dict[str, Any]]) -> dict[str, Any]:
        presets = self.config["presets"]
        category_presets = self.config["category_presets"]
        return {
            "schema_version": 1,
            "dataset_id": dataset_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "presets": presets,
            "records": {record["id"]: category_presets[record["category"]] for record in records},
        }

    @staticmethod
    def _resolve_presets_in_memory(
        document: dict[str, Any],
        records: list[dict[str, Any]],
    ) -> dict[str, dict[str, Any]]:
        resolved: dict[str, dict[str, Any]] = {}
        if set(document["records"]) != {record["id"] for record in records}:
            raise ValueError("preset plan coverage is not exact")
        for record_id, preset_name in document["records"].items():
            preset = document["presets"].get(preset_name)
            if not isinstance(preset, dict):
                raise ValueError(f"unknown preset {preset_name}")
            loras = preset.get("loras")
            steps = preset.get("steps")
            if not isinstance(steps, int) or steps < 1 or not isinstance(loras, list) or not loras:
                raise ValueError(f"invalid preset {preset_name}")
            resolved[record_id] = {
                "name": preset_name,
                "steps": steps,
                "loras": [
                    {"lora": str(item["lora"]).replace("/", "\\"), "strength": float(item["strength"])}
                    for item in loras
                ],
            }
        return resolved

    def _cached_refs(self, character: str, version: str | None) -> dict[str, Any]:
        directory = self.refs_root / self._slug(character) / self._slug(version or "default")
        manifest_path = directory / "manifest.json"
        try:
            manifest = load_character_reference_manifest(manifest_path)
            refs = manifest["canonical_references"]
            if (
                manifest.get("usable") is not True
                or manifest.get("character") != character
                or manifest.get("version") != version
                or not isinstance(refs, list)
                or not refs
            ):
                raise ValueError("cache metadata mismatch")
            context = []
            for ref in refs:
                relative = Path(str(ref.get("file") or ""))
                if relative.is_absolute() or ".." in relative.parts or not (directory / relative).is_file():
                    raise ValueError("cache file missing")
                context.append({
                    "file": self._relative(directory / relative),
                    "page_url": ref.get("page_url"),
                    "source_url": ref.get("source_url"),
                    "domain": ref.get("domain"),
                    "recommendation": ref.get("recommendation"),
                })
            return {"used": True, "manifest": self._relative(manifest_path), "refs": context}
        except (OSError, ValueError, json.JSONDecodeError):
            return {"used": False, "manifest": None, "refs": []}

    def _relative(self, path: Path) -> str:
        return path.resolve().relative_to(ADA_ROOT.resolve()).as_posix()

    @staticmethod
    def _seed(value: Any, record_id: str, field: str) -> int:
        if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value < 2**63:
            raise ValueError(f"entry {record_id} {field} must be a non-negative 63-bit integer")
        return value

    @classmethod
    def _entry_text(
        cls,
        entry: dict[str, Any],
        field: str,
        index: int,
        maximum: int | None,
    ) -> str:
        value = entry.get(field)
        if not isinstance(value, str):
            raise ValueError(f"entry {index} {field} must be text")
        return cls._clean(value, f"entry {index} {field}", maximum)

    @staticmethod
    def _clean(value: str, field: str, maximum: int | None = 160) -> str:
        if not isinstance(value, str):
            raise ValueError(f"{field} must be text")
        cleaned = " ".join(value.split()).strip()
        if not cleaned:
            raise ValueError(f"{field} must not be empty")
        if maximum is not None and len(cleaned) > maximum:
            raise ValueError(f"{field} must contain between 1 and {maximum} characters")
        return cleaned

    @staticmethod
    def _slug(value: str | None) -> str:
        if not value:
            return ""
        ascii_text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
        slug = re.sub(r"[^a-z0-9]+", "_", ascii_text.lower()).strip("_")
        if not slug:
            raise ValueError("character/version cannot produce an empty slug")
        return slug
