#!/usr/bin/env python3
"""Read-only safetensors discovery for ADA Model Registry v1."""

from __future__ import annotations

import hashlib
import json
import re
import struct
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

if __package__:
    from .ada_paths import ADA_ROOT
else:
    from ada_paths import ADA_ROOT


REGISTRY_PATH = ADA_ROOT / "config" / "models_registry.json"
PROFILES_DIR = ADA_ROOT / "config" / "model_capabilities"
MODEL_ROLES = (
    "identity_constructor",
    "anime_to_real_converter",
    "photorealistic_generator",
    "style_preserver",
    "direct_anime_generator",
)
EXPECTED_FILES = {
    "lustifyNSFWCheckpoint_v10Krea2.safetensors",
    "JustifyNSFWCheckpoint_v10Krea2.safetensors",
    "Anima-3.8B.safetensors",
    "qwen35_4b.safetensors",
    "miaomiaoHarem_anima16.safetensors",
    "Anima-3.8B-expanded_adapter.safetensors",
}
EXPECTED_GROUPS = {
    "JustifyNSFWCheckpoint_v10Krea2.safetensors": {"JustifyNSFWCheckpoint_v10Krea2.safetensors", "lustifyNSFWCheckpoint_v10Krea2.safetensors"},
    "Anima-3.8B.safetensors": {"Anima-3.8B.safetensors"},
    "qwen35_4b.safetensors": {"qwen35_4b.safetensors"},
    "miaomiaoHarem_anima16.safetensors": {"miaomiaoHarem_anima16.safetensors"},
    "Anima-3.8B-expanded_adapter.safetensors": {"Anima-3.8B-expanded_adapter.safetensors"},
}
DIRECT_GENERATOR_RECIPES = {
    "lustifynsfwcheckpoint_v10krea2": "lustify_krea2_direct_v1",
    "miaomiaoharem_anima16": "miaomiao_anima16_direct_v1",
    "anima_3_8b": "anima_3_8b_direct_v1",
}


def discovery_roots() -> list[Path]:
    roots = [ADA_ROOT / "downloads", Path.home() / "Downloads"]
    return [root for index, root in enumerate(roots) if root not in roots[:index]]


def _header(path: Path) -> tuple[int, dict[str, Any]]:
    with path.open("rb") as handle:
        raw_length = handle.read(8)
        if len(raw_length) != 8:
            raise ValueError("missing safetensors header length")
        header_length = struct.unpack("<Q", raw_length)[0]
        if header_length < 2 or header_length > 256 * 1024 * 1024:
            raise ValueError(f"invalid safetensors header length: {header_length}")
        raw_header = handle.read(header_length)
    value = json.loads(raw_header)
    if not isinstance(value, dict):
        raise ValueError("safetensors header must be an object")
    return header_length, value


def _slug(filename: str) -> str:
    stem = Path(filename).stem.casefold()
    return re.sub(r"[^a-z0-9]+", "_", stem).strip("_")


def _block_count(keys: list[str], prefix: str) -> int | None:
    indices = []
    pattern = re.compile(rf"^{re.escape(prefix)}(\d+)\.")
    for key in keys:
        match = pattern.match(key)
        if match:
            indices.append(int(match.group(1)))
    return max(indices) + 1 if indices else None


def classify(header: dict[str, Any]) -> dict[str, Any]:
    metadata = header.get("__metadata__", {})
    metadata = metadata if isinstance(metadata, dict) else {}
    keys = [key for key in header if key != "__metadata__"]
    joined = "\n".join(keys[:4000]).casefold()
    architecture_meta = str(metadata.get("architecture", "")).casefold()
    evidence: list[str] = []

    if "adapter" in architecture_meta or any(key.startswith("semantic_attentions.") for key in keys):
        evidence.extend(["adapter architecture declared in metadata", "semantic attention projection tensors without base-model blocks"])
        return {"type": "adapter", "family": "Anima", "architecture": metadata.get("architecture", "anima_semantic_adapter"), "loader": {"name": "custom Anima adapter loader", "status": "unknown"}, "confidence": "confirmed", "evidence": evidence}
    if any(token in joined for token in ("lora_up", "lora_down", ".lora_a.", ".lora_b.")):
        evidence.append("paired low-rank LoRA tensors")
        return {"type": "lora", "family": "unknown", "architecture": "low_rank_adapter", "loader": {"name": "LoraLoader", "status": "candidate"}, "confidence": "confirmed", "evidence": evidence}
    if "embed_tokens.weight" in header and any(key.startswith("layers.") for key in keys):
        evidence.extend(["token embedding matrix", "transformer language layers without diffusion input/output tensors"])
        return {"type": "text_encoder", "family": "Qwen 3.5", "architecture": "qwen3_5_4b", "loader": {"name": "CLIPLoader/text-encoder loader", "status": "candidate"}, "confidence": "confirmed", "evidence": evidence}
    if any(key.startswith("net.blocks.") for key in keys):
        count = _block_count(keys, "net.blocks.")
        evidence.extend(["Anima DiT net.blocks tensor topology", f"{count or 'unknown'} diffusion transformer blocks"])
        if metadata.get("architecture_expansion"):
            evidence.append(f"metadata: {metadata['architecture_expansion']}")
        return {"type": "checkpoint", "family": "Anima", "architecture": "anima_dit", "loader": {"name": "UNETLoader", "status": "candidate"}, "confidence": "confirmed", "evidence": evidence}
    if any(key.startswith("blocks.") for key in keys) and "blocks.0.attn.wq.weight" in header:
        count = _block_count(keys, "blocks.")
        evidence.extend(["Krea2-style transformer block tensor topology", f"{count or 'unknown'} transformer blocks", "FP8 diffusion weights"])
        return {"type": "checkpoint", "family": "Krea2", "architecture": "krea2_transformer", "loader": {"name": "UNETLoader", "status": "candidate"}, "confidence": "probable", "evidence": evidence}
    if any(key.startswith(("encoder.", "decoder.", "quant_conv.")) for key in keys):
        evidence.append("encoder/decoder latent autoencoder tensors")
        return {"type": "vae", "family": "unknown", "architecture": "latent_autoencoder", "loader": {"name": "VAELoader", "status": "candidate"}, "confidence": "probable", "evidence": evidence}
    return {"type": "unknown", "family": "unknown", "architecture": "unknown", "loader": {"name": "unknown", "status": "unknown"}, "confidence": "unknown", "evidence": ["no known structural signature matched"]}


def scan_file(path: Path) -> dict[str, Any]:
    header_length, header = _header(path)
    tensors = {key: value for key, value in header.items() if key != "__metadata__" and isinstance(value, dict)}
    keys = list(tensors)
    metadata = header.get("__metadata__", {})
    metadata = metadata if isinstance(metadata, dict) else {}
    dtypes = Counter(str(value.get("dtype", "unknown")) for value in tensors.values())
    classification = classify(header)
    stat = path.stat()
    return {
        "id": _slug(path.name),
        "file": path.name,
        "version": str(metadata.get("modelspec.version") or metadata.get("version") or Path(path.name).stem),
        "path": str(path.resolve()),
        "size_bytes": stat.st_size,
        "size_gib": round(stat.st_size / (1024 ** 3), 3),
        "modified_at": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
        "header_bytes": header_length,
        "header_sha256": hashlib.sha256(json.dumps(header, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest(),
        "file_sha256": None,
        "metadata": {str(key): str(value) for key, value in metadata.items()},
        "tensor_summary": {
            "count": len(tensors),
            "dtypes": dict(sorted(dtypes.items())),
            "block_count": _block_count(keys, "net.blocks.") or _block_count(keys, "blocks."),
            "principal_keys": keys[:32],
        },
        "classification": classification,
        "status": "discovered",
        "discovery_source": "safetensors_header",
    }


def _capability_profile(model: dict[str, Any]) -> dict[str, Any]:
    model_type = model["classification"]["type"]
    can_generate = "confirmed" if model_type == "checkpoint" else "unknown"
    direct_recipe = DIRECT_GENERATOR_RECIPES.get(model["id"])
    return {
        "schema_version": "model_capability_profile_v1",
        "model_id": model["id"],
        "physical_type": model_type,
        "family": model["classification"]["family"],
        "architecture": model["classification"]["architecture"],
        "loader": model["classification"]["loader"],
        "capabilities": {
            "image_generation": {"state": can_generate, "evidence": "checkpoint structure" if can_generate == "confirmed" else "not independently runnable"},
            "image_to_image": {"state": "unknown", "evidence": "requires controlled test"},
            "identity_preservation": {"state": "unknown", "evidence": "requires controlled test"},
            "realism_conversion": {"state": "unknown", "evidence": "requires controlled test"},
            "anime_generation": {"state": "unknown", "evidence": "requires controlled test"},
        },
        "test_status": "not_tested",
        "test_recipe": (
            {"status": "ready", "runner": "direct_generator_benchmark_v1", "recipe_id": direct_recipe}
            if direct_recipe else
            {"status": "blocked", "reason": "loader/dependency recipe has not been confirmed in Model Lab"}
        ),
        "role_evaluations": {
            role: {"state": "unknown", "score": None, "sample_count": 0, "evidence_receipts": []}
            for role in MODEL_ROLES
        },
    }


def apply_pipeline_decision(model: dict[str, Any]) -> dict[str, Any]:
    """Keep discovery factual while preserving the current product decision on rescans."""
    decisions = {
        "lustifynsfwcheckpoint_v10krea2": ("production_primary", "lustify_krea2_primary_v1", "Validated direct general renderer."),
        "miaomiaoharem_anima16": ("production_secondary_optional", "miaomiao_anima16_secondary_v1", "Validated fast optional anime alternative."),
        "anima_3_8b": ("discarded", "lustify_krea2_primary_v1", "Experimental candidate not selected for the primary pipeline."),
        "anima_3_8b_expanded_adapter": ("discarded", "lustify_krea2_primary_v1", "Experimental candidate not selected for the primary pipeline."),
    }
    decision = decisions.get(model.get("id"))
    if decision:
        status, superseded_by, reason = decision
        model["status"] = status
        model["pipeline_decision"] = {"reason": reason, "superseded_by": superseded_by, "decision_date": "2026-08-24", "evidence": "manual_controlled_benchmark_20260824"}
    return model


def production_klein_entry() -> tuple[dict[str, Any], dict[str, Any]]:
    model = {
        "id": "klein_semi_realistic_baseline",
        "file": "flux-2-klein-9b-fp8.safetensors",
        "version": "production_baseline_v1",
        "path": None,
        "size_bytes": None,
        "size_gib": None,
        "metadata": {},
        "tensor_summary": {},
        "classification": {"type": "checkpoint", "family": "Flux 2 Klein", "architecture": "flux2_klein", "loader": {"name": "UNETLoader", "status": "confirmed"}, "confidence": "confirmed", "evidence": ["active production workflow"]},
        "status": "deprecated_for_primary_pipeline",
        "pipeline_decision": {"reason": "Retained as specialized source-preserving converter, not default generation.", "superseded_by": "lustify_krea2_primary_v1", "decision_date": "2026-08-24", "evidence": "manual_controlled_benchmark_20260824"},
        "discovery_source": "production_configuration",
    }
    profile = {
        "schema_version": "model_capability_profile_v1",
        "model_id": model["id"],
        "physical_type": "checkpoint",
        "family": "Flux 2 Klein",
        "architecture": "flux2_klein",
        "loader": {"name": "UNETLoader", "status": "confirmed"},
        "capabilities": {
            "image_generation": {"state": "confirmed", "evidence": "production runs"},
            "image_to_image": {"state": "confirmed", "evidence": "production ReferenceLatent workflow"},
            "identity_preservation": {"state": "tested", "evidence": "current semi-realistic baseline"},
            "realism_conversion": {"state": "tested", "evidence": "current semi-realistic baseline"},
            "anime_generation": {"state": "unknown", "evidence": "not the production role"},
        },
        "test_status": "production_baseline",
        "test_recipe": {"status": "ready", "runner": "klein_production_baseline_v1"},
        "role_evaluations": {
            "identity_constructor": {"state": "unknown", "score": None, "sample_count": 0, "evidence_receipts": []},
            "anime_to_real_converter": {"state": "confirmed", "score": None, "sample_count": 0, "evidence_receipts": ["production Klein render/review receipts"]},
            "photorealistic_generator": {"state": "unknown", "score": None, "sample_count": 0, "evidence_receipts": []},
            "style_preserver": {"state": "unknown", "score": None, "sample_count": 0, "evidence_receipts": []},
            "direct_anime_generator": {"state": "unknown", "score": None, "sample_count": 0, "evidence_receipts": []},
        },
    }
    return model, profile


def production_illustrious_entry() -> tuple[dict[str, Any], dict[str, Any]]:
    model = {
        "id": "illustrious_production",
        "file": "waiIllustriousSDXL_v160.safetensors",
        "version": "v160",
        "path": None,
        "size_bytes": None,
        "size_gib": None,
        "metadata": {},
        "tensor_summary": {},
        "classification": {"type": "checkpoint", "family": "Illustrious SDXL", "architecture": "sdxl", "loader": {"name": "CheckpointLoaderSimple", "status": "confirmed"}, "confidence": "confirmed", "evidence": ["active production constructor workflow"]},
        "status": "deprecated_for_primary_pipeline",
        "pipeline_decision": {"reason": "Historical identity-constructor baseline; no longer selected by Create Images.", "superseded_by": "lustify_krea2_primary_v1", "decision_date": "2026-08-24", "evidence": "manual_controlled_benchmark_20260824"},
        "discovery_source": "production_configuration",
    }
    profile = {
        "schema_version": "model_capability_profile_v1",
        "model_id": model["id"],
        "physical_type": "checkpoint",
        "family": "Illustrious SDXL",
        "architecture": "sdxl",
        "loader": {"name": "CheckpointLoaderSimple", "status": "confirmed"},
        "capabilities": {
            "image_generation": {"state": "confirmed", "evidence": "production constructor receipts"},
            "image_to_image": {"state": "unknown", "evidence": "not the production role"},
            "identity_preservation": {"state": "tested", "evidence": "production review observations"},
            "realism_conversion": {"state": "unknown", "evidence": "not tested"},
            "anime_generation": {"state": "confirmed", "evidence": "production constructor receipts"},
        },
        "test_status": "production_baseline",
        "test_recipe": {"status": "blocked", "reason": "direct constructor benchmark recipe awaits an isolated concept compiler"},
        "role_evaluations": {
            "identity_constructor": {"state": "confirmed", "score": None, "sample_count": 0, "evidence_receipts": ["production Illustrious render/review receipts"]},
            "anime_to_real_converter": {"state": "unknown", "score": None, "sample_count": 0, "evidence_receipts": []},
            "photorealistic_generator": {"state": "unknown", "score": None, "sample_count": 0, "evidence_receipts": []},
            "style_preserver": {"state": "unknown", "score": None, "sample_count": 0, "evidence_receipts": []},
            "direct_anime_generator": {"state": "unknown", "score": None, "sample_count": 0, "evidence_receipts": []},
        },
    }
    return model, profile


def scan_models() -> dict[str, Any]:
    found: dict[str, Path] = {}
    roots = discovery_roots()
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.glob("*.safetensors"):
            if path.name in EXPECTED_FILES:
                found[path.name.casefold()] = path
    scanned = [apply_pipeline_decision(scan_file(path)) for _, path in sorted(found.items())]
    production, production_profile = production_klein_entry()
    illustrious, illustrious_profile = production_illustrious_entry()
    previous_profiles = {}
    if PROFILES_DIR.is_dir():
        for path in PROFILES_DIR.glob("*.json"):
            try:
                value = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(value, dict) and isinstance(value.get("model_id"), str):
                    previous_profiles[value["model_id"]] = value
            except Exception:
                continue
    profiles = {item["id"]: _capability_profile(item) for item in scanned}
    profiles[production["id"]] = production_profile
    profiles[illustrious["id"]] = illustrious_profile
    for model_id, profile in profiles.items():
        previous_roles = previous_profiles.get(model_id, {}).get("role_evaluations")
        if isinstance(previous_roles, dict):
            for role in MODEL_ROLES:
                previous = previous_roles.get(role)
                if isinstance(previous, dict) and previous.get("sample_count", 0):
                    profile["role_evaluations"][role] = previous
                    if profile.get("test_status") != "production_baseline":
                        profile["test_status"] = previous_profiles[model_id].get("test_status", "tested")
        previous_recipe = previous_profiles.get(model_id, {}).get("test_recipe")
        if isinstance(previous_recipe, dict) and previous_recipe.get("status") == "ready":
            profile["test_recipe"] = previous_recipe
        previous_dimensions = previous_profiles.get(model_id, {}).get("benchmark_dimensions")
        if isinstance(previous_dimensions, dict):
            profile["benchmark_dimensions"] = previous_dimensions
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    for model_id, profile in profiles.items():
        (PROFILES_DIR / f"{model_id}.json").write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    now = datetime.now(timezone.utc).isoformat()
    registry = {
        "schema_version": "models_registry_v1",
        "registry_version": 1,
        "discovered_at": now,
        "scan_roots": [{"path": str(root), "available": root.is_dir()} for root in roots],
        "expected_files": sorted(EXPECTED_GROUPS),
        "missing_files": sorted([
            expected for expected, aliases in EXPECTED_GROUPS.items()
            if not aliases.intersection({item["file"] for item in scanned})
        ], key=str.casefold),
        "filename_discrepancies": [
            {"requested": "JustifyNSFWCheckpoint_v10Krea2.safetensors", "found": "lustifyNSFWCheckpoint_v10Krea2.safetensors"}
            for item in scanned if item["file"] == "lustifyNSFWCheckpoint_v10Krea2.safetensors"
        ],
        "models": [illustrious, production, *scanned],
        "capability_profiles": {model_id: f"config/model_capabilities/{model_id}.json" for model_id in profiles},
    }
    REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return registry


if __name__ == "__main__":
    result = scan_models()
    print(json.dumps({"models": len(result["models"]), "missing": result["missing_files"], "registry": str(REGISTRY_PATH)}, ensure_ascii=False))
