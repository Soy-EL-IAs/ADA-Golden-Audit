import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import re
import threading

from scripts.ada_paths import ADA_ROOT, CHARACTERS_ROOT, LIBRARY_ROOT, RENDERER_RUNS_ROOT
from ada_app.managed_assets import adopt_library_record
from ada_app.run_index import RunIndex, RunInfo
from scripts.agent_contracts import validate_contract

LIBRARY_DIR = LIBRARY_ROOT
INDEX_PATH = LIBRARY_DIR / "index.json"
REVIEW_PATH = LIBRARY_DIR / "asset_review.json"
EXPLICIT_IMAGES_PATH = LIBRARY_DIR / "explicit_images.json"
CHARACTERS_PATH = CHARACTERS_ROOT / "catalog.json"
LIBRARY_SOURCE_POLICY = {
    "auto_index": ["production_pilot_renderer_outputs", "historical_pilot_renderer_outputs"],
    "promotion_required": ["model_lab", "benchmark", "manual_benchmark"],
    "explicit_registration": ["completed_reinterpretation_output"],
    "not_images_yet": ["pending_reinterpretation_request"],
}
_EXPLICIT_IMAGES_LOCK = threading.Lock()
_REVIEWS_LOCK = threading.Lock()
_INDEX_BUILD_LOCK = threading.Lock()

_NON_VISIBLE_LIBRARY_STATUSES = frozenset({"REJECTED", "REMOVED", "DELETED", "SOFT_DELETED"})
_COLLECTION_SMALL_WORDS = frozenset({"a", "an", "and", "at", "for", "in", "no", "of", "on", "the", "to"})


def is_visible_library_asset(asset: Dict[str, Any]) -> bool:
    """Canonical visibility rule shared by Library, Home and collection summaries."""
    if not isinstance(asset, dict):
        return False
    status = _text(asset.get("library_status")).upper()
    if status in _NON_VISIBLE_LIBRARY_STATUSES:
        return False
    if bool(asset.get("hidden_from_default_gallery")):
        return False
    if any(bool(asset.get(flag)) for flag in ("soft_deleted", "removed", "deleted")):
        return False
    if any(_text(asset.get(field)) for field in ("soft_deleted_at", "removed_at", "deleted_at")):
        return False
    return True


def visible_library_assets(assets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [asset for asset in assets if is_visible_library_asset(asset)]


def humanize_collection_id(value: str) -> str:
    """Human fallback for booru-style franchise slugs."""
    raw = _text(value) or "Unknown"
    if not re.fullmatch(r"[a-z0-9_()\-]+", raw):
        return raw
    words = re.sub(r"[_\-]+", " ", raw).split()
    rendered = []
    for index, word in enumerate(words):
        match = re.fullmatch(r"\(([^)]+)\)", word)
        core = match.group(1) if match else word
        titled = core.lower() if index > 0 and core.lower() in _COLLECTION_SMALL_WORDS else core.capitalize()
        rendered.append(f"({titled})" if match else titled)
    return " ".join(rendered) or "Unknown"


def collection_display_name(collection_id: str, character_entry: Dict[str, Any] | None = None) -> str:
    entry = character_entry if isinstance(character_entry, dict) else {}
    for field in ("collection_display_name", "franchise_display_name", "franchise_name"):
        candidate = _text(entry.get(field))
        if candidate:
            return candidate
    return humanize_collection_id(collection_id)


def summarize_visible_collections(assets: List[Dict[str, Any]], characters: Dict[str, Any] | None = None) -> Dict[str, Dict[str, Any]]:
    registry = characters if isinstance(characters, dict) else {}
    result: Dict[str, Dict[str, Any]] = {}
    for asset in visible_library_assets(assets):
        collection_id = _text(asset.get("collection_id")) or _text(asset.get("franchise")) or "Unknown"
        character = _text(asset.get("character")) or "Unknown"
        entry = registry.get(character, {}) if isinstance(registry.get(character), dict) else {}
        summary = result.setdefault(collection_id, {
            "collection_id": collection_id,
            "display_name": _text(asset.get("collection_display_name")) or collection_display_name(collection_id, entry),
            "characters": {},
            "character_count": 0,
            "total_images": 0,
        })
        summary["characters"][character] = summary["characters"].get(character, 0) + 1
        summary["total_images"] += 1
    for summary in result.values():
        summary["character_count"] = len(summary["characters"])
    return result


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _words(value: Any, limit: int = 5) -> str:
    """Return a short excerpt made only from persisted semantic text."""
    words = re.findall(r"[\w'-]+", _text(value), flags=re.UNICODE)
    return " ".join(words[:limit])


def _display_metadata(character: str, spec: Dict[str, Any], snapshot: str) -> tuple[str, str]:
    hook = spec.get("hook_premise", spec.get("concept", {})) if isinstance(spec, dict) else {}
    hook = hook if isinstance(hook, dict) else {}
    signature = hook.get("diversity_signature", {}) if isinstance(hook.get("diversity_signature"), dict) else {}
    setting = _text(hook.get("setting")) or _text(signature.get("setting")) or _text(hook.get("hook_type"))
    if "/" in setting:
        setting = setting.rsplit("/", 1)[-1].strip()
    title_subject = _words(setting, 3).title() or "Image"
    description_source = _text(hook.get("snapshot")) or _text(snapshot) or _text(hook.get("core_action"))
    description = _words(description_source, 5) or _words(f"{_text(character) or 'Character'} image", 5)
    return f"{_text(character) or 'Unknown'} — {title_subject}", description


def _agent_rating(review: Dict[str, Any]) -> float | None:
    """Expose only an explicit image-review score; never infer one from PASS/FAIL."""
    value = review.get("agent_rating") if isinstance(review, dict) else None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return round(float(value), 1) if 1.0 <= float(value) <= 10.0 else None


def _generated_at(image_path: str, fallback: str) -> str:
    """Prefer the individual render file timestamp over the enclosing run timestamp."""
    try:
        return datetime.fromtimestamp(Path(image_path).stat().st_mtime, timezone.utc).isoformat()
    except (OSError, ValueError):
        return fallback

class Asset:
    def __init__(self, asset_id: str, character: str, thumbnail_path: str, full_image_path: str,
                 source_run_id: str, concept_snapshot: str, final_status: str,
                 final_review_verdict: str, created_at: str, creative_model: str,
                 concept_id: str = "", illustrious_image: str = "",
                 illustrious_review: Dict = None, final_review: Dict = None,
                 favorite: bool = False, franchise: str = "Unknown", universe: str = "Unknown",
                 tags: List[str] = None, source_mission_id: str = "", asset_type: str = "illustration",
                 parent_asset_id: str = "", derived_from: str = "", transformation: str = "",
                 constructor_model: str = "illustrious", finalizer_model: str = "klein",
                  character_profile: Dict = None, illustrious_generation: Dict = None,
                  klein_generation: Dict = None, m3_scores: Dict = None, selection_rank: int = None,
                  selection_reason: str = "", human_review: Dict = None, creative_layer: Dict = None,
                  character_contract: Dict = None, resolved_render_spec: Dict = None,
                  stage_render_plans: Dict = None, prompt_artifacts: Dict = None,
                  render_receipts: Dict = None, review_observations: Dict = None,
                  routing_decisions: Dict = None, semantic_contract_versions: Dict = None,
                  stage_images: Dict = None, comparative_review: Dict = None,
                  automatic_final_stage_decision: Dict = None,
                  effective_final_stage_decision: Dict = None,
                  human_stage_overrides: List[Dict] = None,
                  source_artifact_root: str = "", render_outputs: List[Dict] = None,
                  comparison_outputs: List[Dict] = None,
                  generation_id: str = "", renderer: str = "", preset: str = "",
                  is_final_selection: bool = False, source_asset_id: str = "",
                  render_intent: str = "", lineage: Dict = None,
                  display_title: str = "", short_description: str = "",
                  agent_rating: float | None = None, agent_scores: Dict = None,
                  creation_mode: str = "scene", hard_rating: Dict = None):
        self.asset_id = asset_id
        self.character = character
        self.thumbnail_path = thumbnail_path
        self.full_image_path = full_image_path
        self.source_run_id = source_run_id
        self.concept_snapshot = concept_snapshot
        self.final_status = final_status
        self.final_review_verdict = final_review_verdict
        self.created_at = created_at
        self.creative_model = creative_model
        self.concept_id = concept_id
        self.illustrious_image = illustrious_image
        self.illustrious_review = illustrious_review or {}
        self.final_review = final_review or {}
        self.favorite = favorite
        self.franchise = franchise
        self.universe = universe
        self.tags = tags or []
        self.source_mission_id = source_mission_id
        self.asset_type = asset_type
        self.hard_rating = hard_rating
        self.parent_asset_id = parent_asset_id
        self.derived_from = derived_from
        self.transformation = transformation
        self.constructor_model = constructor_model
        self.finalizer_model = finalizer_model
        self.character_profile = character_profile or {}
        self.illustrious_generation = illustrious_generation or {}
        self.klein_generation = klein_generation or {}
        self.m3_scores = m3_scores or {}
        self.selection_rank = selection_rank
        self.selection_reason = selection_reason
        self.human_review = human_review or {"status": "UNREVIEWED", "rating": None, "favorite": False}
        self.creative_layer = creative_layer or {}
        self.character_contract = character_contract or {}
        self.resolved_render_spec = resolved_render_spec or {}
        self.stage_render_plans = stage_render_plans or {}
        self.prompt_artifacts = prompt_artifacts or {}
        self.render_receipts = render_receipts or {}
        self.review_observations = review_observations or {}
        self.routing_decisions = routing_decisions or {}
        self.semantic_contract_versions = semantic_contract_versions or {}
        self.stage_images = stage_images or {}
        self.comparative_review = comparative_review or {}
        self.automatic_final_stage_decision = automatic_final_stage_decision or {}
        self.effective_final_stage_decision = effective_final_stage_decision or {}
        self.human_stage_overrides = human_stage_overrides or []
        self.source_artifact_root = source_artifact_root
        self.render_outputs = render_outputs or []
        self.comparison_outputs = comparison_outputs or []
        self.record_type = "library_image_v2"
        self.generation_id = generation_id or asset_id
        self.renderer = renderer
        self.preset = preset
        self.is_final_selection = bool(is_final_selection)
        self.source_asset_id = source_asset_id
        self.render_intent = render_intent
        self.lineage = lineage or {}
        self.display_title = display_title
        self.short_description = short_description
        self.agent_rating = agent_rating
        self.agent_scores = agent_scores or {}
        self.creation_mode = creation_mode if creation_mode in {"scene", "stock"} else "scene"
        
    def to_dict(self):
        return {
            "asset_id": self.asset_id,
            "character": self.character,
            "thumbnail_path": self.thumbnail_path,
            "full_image_path": self.full_image_path,
            "source_run_id": self.source_run_id,
            "source_mission_id": self.source_mission_id,
            "parent_asset_id": self.parent_asset_id,
            "concept_snapshot": self.concept_snapshot,
            "final_status": self.final_status,
            "final_review_verdict": self.final_review_verdict,
            "created_at": self.created_at,
            "creative_model": self.creative_model,
            "concept_id": self.concept_id,
            "illustrious_image": self.illustrious_image,
            "illustrious_review": self.illustrious_review,
            "final_review": self.final_review,
            "character_profile": self.character_profile,
            "illustrious_generation": self.illustrious_generation,
            "klein_generation": self.klein_generation,
            "m3_scores": self.m3_scores,
            "selection_rank": self.selection_rank,
            "selection_reason": self.selection_reason,
            "human_review": self.human_review,
            "creative_layer": self.creative_layer,
            "character_contract": self.character_contract,
            "resolved_render_spec": self.resolved_render_spec,
            "stage_render_plans": self.stage_render_plans,
            "prompt_artifacts": self.prompt_artifacts,
            "render_receipts": self.render_receipts,
            "review_observations": self.review_observations,
            "routing_decisions": self.routing_decisions,
            "semantic_contract_versions": self.semantic_contract_versions,
            "stage_images": self.stage_images,
            "comparative_review": self.comparative_review,
            "automatic_final_stage_decision": self.automatic_final_stage_decision,
            "effective_final_stage_decision": self.effective_final_stage_decision,
            "human_stage_overrides": self.human_stage_overrides,
            "source_artifact_root": self.source_artifact_root,
            "render_outputs": self.render_outputs,
            "comparison_outputs": self.comparison_outputs,
            "record_type": self.record_type,
            "generation_id": self.generation_id,
            "renderer": self.renderer,
            "preset": self.preset,
            "is_final_selection": self.is_final_selection,
            "source_asset_id": self.source_asset_id,
            "render_intent": self.render_intent,
            "lineage": self.lineage,
            "display_title": self.display_title,
            "short_description": self.short_description,
            "agent_rating": self.agent_rating,
            "agent_scores": self.agent_scores,
            "creation_mode": self.creation_mode,
        }

class AssetLibrary:
    def __init__(self):
        LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
        self.reviews = self._load_reviews()
        self.index = self._load_index()
        
    def _load_reviews(self) -> Dict[str, Dict[str, Any]]:
        if not REVIEW_PATH.exists():
            return {}
        try:
            with open(REVIEW_PATH, "r", encoding="utf-8") as f:
                raw = json.load(f)
                if not isinstance(raw, dict):
                    return {}
                return {
                    asset_id: value if isinstance(value, dict) else {
                        "status": "REJECTED" if value == "Reject" else "UNREVIEWED",
                        "rating": None,
                        "favorite": value == "Favorite",
                    }
                    for asset_id, value in raw.items()
                }
        except Exception:
            return {}

    @staticmethod
    def _default_review() -> Dict[str, Any]:
        return {
            "status": "UNREVIEWED", "rating": None, "favorite": False,
            "stages": {},
            "preference": "NONE", "preference_history": [], "stage_review_history": [],
        }

    def save_review(self, asset_id: str, *, human_status: str | None = None,
                    rating: int | None = None, favorite: bool | None = None,
                    stage: str | None = None, preference: str | None = None):
        if not self.index:
            self.build_index()
        asset = next((item for item in self.index if item.get("asset_id") == asset_id), None)
        if asset is None:
            raise ValueError("Unknown Library asset")
        review = dict(self.reviews.get(asset_id, {"status": "UNREVIEWED", "rating": None, "favorite": False}))
        stages = review.get("stages")
        if not isinstance(stages, dict):
            stages = self._default_review()["stages"]
        else:
            stages = {key: dict(value) for key, value in stages.items() if isinstance(value, dict)}
        available_renderers = {str(output.get("renderer", "")).casefold() for output in asset.get("render_outputs", []) if isinstance(output, dict)}
        available_renderers.update(str(key).casefold() for key in asset.get("stage_images", {}) if isinstance(key, str))
        if stage is not None and stage.casefold() not in available_renderers:
            raise ValueError("Renderer is not available on this asset")
        if stage:
            stage = stage.casefold()
            stages.setdefault(stage, {"status": "UNREVIEWED", "rating": None})
        if human_status is not None:
            if human_status not in {"UNREVIEWED", "APPROVED", "REJECTED"}:
                raise ValueError("Invalid human review status")
            if stage:
                stages[stage]["status"] = human_status
            else:
                review["status"] = human_status
        if rating is not None:
            if not isinstance(rating, int) or not 1 <= rating <= 10:
                raise ValueError("Rating must be an integer from 1 to 10")
            if stage:
                stages[stage]["rating"] = rating
            else:
                review["rating"] = rating
        if favorite is not None:
            review["favorite"] = bool(favorite)
        review["stages"] = stages
        history = review.get("preference_history", [])
        history = list(history) if isinstance(history, list) else []
        stage_history = review.get("stage_review_history", [])
        stage_history = list(stage_history) if isinstance(stage_history, list) else []
        root = Path(asset.get("source_artifact_root", ""))
        candidate_dir = root / "pilot" / asset.get("concept_id", "")
        if stage is not None and (human_status is not None or rating is not None):
            if not root.is_dir() or not candidate_dir.is_dir():
                raise ValueError("Source candidate directory is unavailable")
            created_at = datetime.now(timezone.utc).isoformat()
            event = {
                "schema_version": "human_stage_review_v1",
                "review_id": f"human-review:{asset_id}:{stage}:{created_at}",
                "asset_id": asset_id,
                "created_at": created_at,
                "stage": stage,
                "status": stages[stage].get("status", "UNREVIEWED"),
                "rating": stages[stage].get("rating") or 0,
                "supersedes_review_id": next((item.get("review_id", "") for item in reversed(stage_history) if isinstance(item, dict) and item.get("stage") == stage), ""),
            }
            validate_contract("human_stage_review_v1", event)
            event_dir = candidate_dir / "human_stage_reviews"
            event_dir.mkdir(parents=True, exist_ok=True)
            filename = datetime.now(timezone.utc).strftime(f"{stage}_review_%Y%m%dT%H%M%S%fZ.json")
            with (event_dir / filename).open("x", encoding="utf-8") as handle:
                json.dump(event, handle, ensure_ascii=False, indent=2)
                handle.write("\n")
            stage_history.append(event)
        if preference is not None:
            normalized = preference.upper()
            if normalized != "NONE" and normalized.casefold() not in available_renderers:
                raise ValueError("Preference must name an available renderer or NONE")
            created_at = datetime.now(timezone.utc).isoformat()
            override = {
                "schema_version": "human_stage_override_v1",
                "override_id": f"human-stage:{asset_id}:{created_at}",
                "asset_id": asset_id,
                "created_at": created_at,
                # The v1 field name is retained only for historical on-disk compatibility;
                # its value is now any renderer present in generic lineage.
                "selected_stage": normalized.casefold(),
                "reason": "Manual Library stage preference",
                "automatic_decision_id": asset.get("automatic_final_stage_decision", {}).get("decision_id", ""),
                "supersedes_override_id": history[-1].get("override_id", "") if history and isinstance(history[-1], dict) else "",
            }
            validate_contract("human_stage_override_v1", override)
            if not root.is_dir() or not candidate_dir.is_dir():
                raise ValueError("Source candidate directory is unavailable")
            override_dir = candidate_dir / "human_stage_overrides"
            override_dir.mkdir(parents=True, exist_ok=True)
            filename = datetime.now(timezone.utc).strftime("human_override_%Y%m%dT%H%M%S%fZ.json")
            with (override_dir / filename).open("x", encoding="utf-8") as handle:
                json.dump(override, handle, ensure_ascii=False, indent=2)
                handle.write("\n")
            history.append(override)
            review["preference"] = normalized
        review["preference_history"] = history
        review["stage_review_history"] = stage_history
        self.reviews[asset_id] = review
        with open(REVIEW_PATH, "w", encoding="utf-8") as f:
            json.dump(self.reviews, f, indent=2)
        return review

    def set_library_status(self, asset_ids: List[str], status: str) -> List[str]:
        """Atomically update gallery visibility metadata without deleting image files."""
        if status not in {"UNREVIEWED", "REJECTED"}:
            raise ValueError("Invalid Library status")
        if not self.index:
            self.build_index()
        unique_ids = list(dict.fromkeys(asset_id for asset_id in asset_ids if isinstance(asset_id, str) and asset_id))
        if not unique_ids:
            raise ValueError("No Library images selected")
        known_ids = {item.get("asset_id") for item in self.index}
        unknown = [asset_id for asset_id in unique_ids if asset_id not in known_ids]
        if unknown:
            raise ValueError(f"Unknown Library image: {unknown[0]}")
        with _REVIEWS_LOCK:
            updated = dict(self.reviews)
            for asset_id in unique_ids:
                review = dict(updated.get(asset_id, self._default_review()))
                review["status"] = status
                updated[asset_id] = review
            temporary = REVIEW_PATH.with_suffix(".json.tmp")
            temporary.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            temporary.replace(REVIEW_PATH)
            self.reviews = updated
        return unique_ids

    def save_hard_rating(self, asset_id: str, hard_rating_data: dict, failed: bool = False) -> dict:
        if not self.index:
            self.build_index()
        with _REVIEWS_LOCK:
            updated = dict(self.reviews)
            review = dict(updated.get(asset_id, self._default_review()))
            
            history = list(review.get("hard_rating_history", []))
            if "hard_rating" in review and not history:
                history.append(review["hard_rating"])
            
            history.append(hard_rating_data)
            review["hard_rating_history"] = history
            
            if not failed:
                review["hard_rating"] = hard_rating_data
                
            updated[asset_id] = review
            temporary = REVIEW_PATH.with_suffix(".json.tmp")
            temporary.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            temporary.replace(REVIEW_PATH)
            self.reviews = updated
        return review

    def _load_index(self) -> List[Dict]:
        if not INDEX_PATH.exists():
            return self._load_explicit_images()
        try:
            with open(INDEX_PATH, "r", encoding="utf-8") as f:
                value = json.load(f)
            if not isinstance(value, list):
                return self._load_explicit_images()
            # Historical Image Pipeline entries were generated by legacy adapters
            # and are intentionally outside the production Library surface.
            clean = [asset for asset in value if asset.get("concept_snapshot") != "Legacy Image Pipeline Result"]
            if len(clean) != len(value):
                with open(INDEX_PATH, "w", encoding="utf-8") as f:
                    json.dump(clean, f, indent=2)
            if clean and any(asset.get("record_type") != "library_image_v2" for asset in clean):
                return self._load_explicit_images()
            explicit = self._load_explicit_images()
            explicit_ids = {item.get("asset_id") for item in explicit}
            return [item for item in clean if item.get("asset_id") not in explicit_ids] + explicit
        except Exception:
            return self._load_explicit_images()

    @staticmethod
    def _load_explicit_images() -> List[Dict[str, Any]]:
        if not EXPLICIT_IMAGES_PATH.is_file():
            return []
        try:
            value = json.loads(EXPLICIT_IMAGES_PATH.read_text(encoding="utf-8"))
            return [item for item in value if isinstance(item, dict) and item.get("record_type") == "library_image_v2"] if isinstance(value, list) else []
        except Exception:
            return []

    @staticmethod
    def _save_explicit_images(images: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        images = [adopt_library_record(image) for image in images]
        temp = EXPLICIT_IMAGES_PATH.with_suffix(".json.tmp")
        temp.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temp.replace(EXPLICIT_IMAGES_PATH)
        return images

    @staticmethod
    def _write_index_records(records: List[Dict[str, Any]]) -> None:
        temporary = INDEX_PATH.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(INDEX_PATH)
            
    def _save_index(self, assets: List[Asset]) -> List[Dict[str, Any]]:
        records = [adopt_library_record(asset.to_dict()) for asset in assets]
        self._write_index_records(records)
        return records

    def _build_generation_index_legacy(self):
        try:
            with open(CHARACTERS_PATH, "r", encoding="utf-8") as f:
                characters_data = json.load(f)
        except Exception:
            characters_data = {}
            
        run_idx = RunIndex()
        runs = run_idx.get_all_runs()
        
        assets = []
        for run in runs:
            if run.final_assets_count == 0:
                continue
                
            run_dir = Path(run.artifact_root)
            
            if run.run_type == "Pilot":
                # Parse pilot candidates
                pilot_cand_path = run_dir / "pilot_candidates.json"
                if not pilot_cand_path.exists(): continue
                try:
                    cands = json.loads(pilot_cand_path.read_text(encoding="utf-8"))
                except Exception:
                    continue
                creative_layer = {
                    "model": run.source_model,
                    "guide_context": self._read_json(run_dir / "guide_context.json"),
                }
                for cand in cands:
                    try:
                        generic_outputs = cand.get("render_outputs", [])
                        generic_decision = cand.get("automatic_final_renderer_decision", {})
                        visible_states = {"APPROVED", "REJECTED_QUALITY", "RETRY_EXHAUSTED", "FINAL", "COMPLETE"}
                        if cand.get("pipeline_state") in visible_states and isinstance(generic_outputs, list) and generic_outputs:
                            asset_id = f"{run.run_id}_{cand['concept_id']}"
                            char_name = cand.get("character", run.character)
                            char_info = characters_data.get(char_name, {})
                            human_review = self.reviews.get(asset_id, self._default_review())
                            output_map = {item.get("renderer"): item for item in generic_outputs if isinstance(item, dict) and isinstance(item.get("renderer"), str)}
                            selected_renderer = generic_decision.get("selected_renderer") if isinstance(generic_decision, dict) else ""
                            selected = output_map.get(selected_renderer) or next(iter(output_map.values()))
                            selected_image = selected.get("receipt", {}).get("output_asset", "")
                            if not selected_image:
                                continue
                            stage_images = {renderer: item.get("receipt", {}).get("output_asset", "") for renderer, item in output_map.items()}
                            assets.append(Asset(asset_id=asset_id, character=char_name, thumbnail_path=selected_image, full_image_path=selected_image, source_run_id=run.run_id, concept_snapshot=cand.get("original_proposal", {}).get("snapshot", ""), final_status="MACHINE_PASS", final_review_verdict=selected.get("review", {}).get("verdict", "UNKNOWN"), created_at=run.created_at, creative_model=cand.get("source_model", run.source_model), concept_id=cand.get("concept_id", ""), favorite=bool(human_review.get("favorite")), franchise=char_info.get("franchise", "Unknown"), universe=char_info.get("universe", "Unknown"), tags=char_info.get("tags", []), source_mission_id=cand.get("source_mission_id", ""), human_review=human_review, character_contract=cand.get("character_contract", {}), resolved_render_spec=cand.get("resolved_render_spec", {}), stage_render_plans={item.get("renderer", ""): {} for item in generic_outputs if isinstance(item, dict)}, prompt_artifacts={}, render_receipts={renderer: item.get("receipt", {}) for renderer, item in output_map.items()}, review_observations={renderer: item.get("review_observation", {}) for renderer, item in output_map.items()}, stage_images=stage_images, automatic_final_stage_decision=generic_decision, effective_final_stage_decision=generic_decision, source_artifact_root=str(run_dir.resolve()), render_outputs=generic_outputs))
                            continue
                        receipts = {
                            "illustrious": cand.get("illustrious_render_receipt", {}),
                            "klein": cand.get("klein_render_receipt", {}),
                        }
                        receipt_images = {
                            stage: receipt.get("output_asset", "") if isinstance(receipt, dict) else ""
                            for stage, receipt in receipts.items()
                        }
                        receipt_pair_valid = True
                        for stage, receipt in receipts.items():
                            try:
                                validate_contract("render_receipt_v1", receipt)
                                if receipt.get("stage") != stage:
                                    raise ValueError("receipt stage mismatch")
                            except (ValueError, TypeError):
                                receipt_pair_valid = False
                                break
                        legacy_final_image = cand.get("klein_image", "")
                        # Compare uses exact receipt outputs; the old final image remains visible for legacy Missions.
                        visible_states = {"APPROVED", "REJECTED_QUALITY", "RETRY_EXHAUSTED", "FINAL", "COMPLETE"}
                        if cand.get("pipeline_state") in visible_states and (receipt_pair_valid or legacy_final_image):
                            asset_id = f"{run.run_id}_{cand['concept_id']}"
                            char_name = cand.get("character", run.character)
                            char_info = characters_data.get(char_name, {})
                             
                            human_review = self.reviews.get(asset_id, self._default_review())
                            automatic_decision = cand.get("automatic_final_stage_decision") or cand.get("final_stage_decision")
                            valid_final_images = {value for value in receipt_images.values() if value} if receipt_pair_valid else set()
                            if legacy_final_image:
                                valid_final_images.add(legacy_final_image)
                            if not isinstance(automatic_decision, dict) or automatic_decision.get("selected_image") not in valid_final_images:
                                automatic_decision = {
                                    "schema_version": "legacy_final_stage_decision",
                                    "decision_id": f"legacy-final-stage:{cand['concept_id']}",
                                    "selected_stage": "klein",
                                    "selected_image": receipt_images["klein"] if receipt_pair_valid else legacy_final_image,
                                    "reason": "Compatibility selection for an asset completed before comparative_review_v1.",
                                    "source": "legacy_compatibility",
                                    "requires_human_review": False,
                                    "automatic": True,
                                }
                            assets.append(Asset(
                                asset_id=asset_id,
                                character=char_name,
                                thumbnail_path=automatic_decision["selected_image"],
                                full_image_path=automatic_decision["selected_image"],
                                source_run_id=run.run_id,
                                concept_snapshot=cand.get("original_proposal", {}).get("snapshot", ""),
                                final_status="MACHINE_PASS",
                                final_review_verdict=cand.get("final_review", {}).get("verdict", "UNKNOWN"),
                                created_at=run.created_at,
                                creative_model=cand.get("source_model", run.source_model),
                                concept_id=cand.get("concept_id", ""),
                                illustrious_image=receipt_images["illustrious"],
                                illustrious_review=cand.get("illustrious_review", {}),
                                final_review=cand.get("final_review", {}),
                                favorite=bool(human_review.get("favorite")),
                                franchise=char_info.get("franchise", "Unknown"),
                                universe=char_info.get("universe", "Unknown"),
                                tags=char_info.get("tags", []),
                                source_mission_id=cand.get("source_mission_id", ""),
                                character_profile=cand.get("character_profile", {}),
                                illustrious_generation=cand.get("illustrious_generation", {}),
                                klein_generation=cand.get("klein_generation", {}),
                                m3_scores=cand.get("m3_scores", {}),
                                selection_rank=cand.get("selection_rank"),
                                selection_reason=cand.get("selection_reason", ""),
                                human_review=human_review,
                                creative_layer=creative_layer,
                                character_contract=cand.get("character_contract", {}),
                                resolved_render_spec=cand.get("resolved_render_spec", {}),
                                stage_render_plans={
                                    "illustrious": cand.get("illustrious_stage_render_plan", {}),
                                    "klein": cand.get("klein_stage_render_plan", {}),
                                },
                                prompt_artifacts={
                                    "illustrious": cand.get("illustrious_prompt_artifact", {}),
                                    "klein": cand.get("klein_prompt_artifact", {}),
                                },
                                render_receipts=receipts,
                                review_observations={
                                    "illustrious": cand.get("illustrious_review_observation", {}),
                                    "klein": cand.get("final_review_observation", {}),
                                },
                                routing_decisions={
                                    "illustrious": cand.get("illustrious_routing_decision", {}),
                                    "klein": cand.get("final_routing_decision", {}),
                                },
                                semantic_contract_versions=cand.get("semantic_contract_versions", {}),
                                stage_images=receipt_images if receipt_pair_valid else {},
                                comparative_review=cand.get("comparative_review", {}),
                                automatic_final_stage_decision=automatic_decision,
                                effective_final_stage_decision=automatic_decision,
                                human_stage_overrides=human_review.get("preference_history", []),
                                source_artifact_root=str(run_dir.resolve()),
                                render_outputs=[
                                    {"renderer": "illustrious", "preset": "illustrious_historical", "receipt": receipts["illustrious"], "review": cand.get("illustrious_review", {})},
                                    {"renderer": "klein", "preset": "klein_historical", "receipt": receipts["klein"], "review": cand.get("final_review", {})}
                                ]
                            ))
                    except Exception as e:
                        import traceback
                        print(f"[AssetLibrary] Skipping candidate {cand.get('concept_id', '?')} in {run.run_id}: {e}")
                        continue
            
        assets.sort(key=lambda a: a.created_at, reverse=True)
        self.index = self._save_index(assets)
        return self.index

    def build_index(self):
        with _INDEX_BUILD_LOCK:
            return self._build_index_unlocked()

    def _build_index_unlocked(self):
        """Index one Library Image per renderer output; generations remain lineage containers."""
        try:
            characters_data = json.loads(CHARACTERS_PATH.read_text(encoding="utf-8"))
        except Exception:
            characters_data = {}
        assets: list[Asset] = []
        visible_states = {"APPROVED", "REJECTED_QUALITY", "RETRY_EXHAUSTED", "FINAL", "COMPLETE", "RENDERED_PENDING_REVIEW", "REVIEW_FAILED"}
        for run in RunIndex().get_all_runs():
            if run.run_type != "Pilot":
                continue
            run_dir = Path(run.artifact_root)
            candidates_path = run_dir / "pilot_candidates.json"
            if not candidates_path.is_file():
                continue
            try:
                candidates = json.loads(candidates_path.read_text(encoding="utf-8"))
            except Exception:
                continue
            for candidate in candidates if isinstance(candidates, list) else []:
                if not isinstance(candidate, dict) or candidate.get("pipeline_state") not in visible_states:
                    continue
                generation_id = f"{run.run_id}_{candidate.get('concept_id', 'unknown')}"
                normalized: list[dict[str, Any]] = []
                reference_outputs: list[dict[str, Any]] = []
                seen: set[tuple[str, str]] = set()
                for output in candidate.get("render_outputs", []) if isinstance(candidate.get("render_outputs"), list) else []:
                    if not isinstance(output, dict):
                        continue
                    if output.get("role") == "identity_reference":
                        receipt = output.get("receipt", {}) if isinstance(output.get("receipt"), dict) else {}
                        path = receipt.get("output_asset", "")
                        if isinstance(path, str) and path and Path(path).is_file():
                            reference_outputs.append({**output, "receipt": receipt})
                        continue
                    renderer = str(output.get("renderer", "")).casefold()
                    receipt = output.get("receipt", {}) if isinstance(output.get("receipt"), dict) else {}
                    path = receipt.get("output_asset", "")
                    if renderer and isinstance(path, str) and path and (renderer, path) not in seen:
                        normalized.append({**output, "renderer": renderer, "receipt": receipt})
                        seen.add((renderer, path))
                legacy = {
                    "illustrious": (candidate.get("illustrious_image", ""), candidate.get("illustrious_render_receipt", {}), candidate.get("illustrious_review", {}), "illustrious_historical"),
                    "klein": (candidate.get("klein_image", ""), candidate.get("klein_render_receipt", {}), candidate.get("final_review", {}), "klein_historical"),
                }
                for renderer, (image, receipt, review, preset) in legacy.items():
                    receipt = receipt if isinstance(receipt, dict) else {}
                    path = receipt.get("output_asset") or image
                    if isinstance(path, str) and path and (renderer, path) not in seen:
                        normalized.append({"renderer": renderer, "preset": preset, "receipt": {**receipt, "output_asset": path}, "review": review if isinstance(review, dict) else {}})
                        seen.add((renderer, path))
                normalized = [output for output in normalized if Path(output["receipt"]["output_asset"]).is_file()]
                if not normalized:
                    continue
                decision = candidate.get("automatic_final_renderer_decision") or candidate.get("automatic_final_stage_decision") or candidate.get("final_stage_decision") or {}
                selected_path = decision.get("selected_image", "") if isinstance(decision, dict) else ""
                if not selected_path and candidate.get("pipeline_state") == "APPROVED":
                    selected_path = candidate.get("selected_image") or candidate.get("klein_image") or normalized[0]["receipt"]["output_asset"]
                image_ids = [f"{generation_id}::{output['renderer']}" for output in normalized]
                char_name = candidate.get("character") or run.character or "Unknown"
                char_info = characters_data.get(char_name, {}) if isinstance(characters_data, dict) else {}
                spec = candidate.get("resolved_render_spec", {}) if isinstance(candidate.get("resolved_render_spec"), dict) else {}
                creation_mode = candidate.get("creation_mode") or spec.get("creation_mode") or "scene"
                render_intent = spec.get("render_intent") or spec.get("hook_premise", {}).get("render_intent", "") if isinstance(spec, dict) else ""
                display_title, short_description = _display_metadata(
                    char_name, spec, candidate.get("original_proposal", {}).get("snapshot", "")
                )
                for ordinal, output in enumerate(normalized):
                    renderer = output["renderer"]
                    image_id = image_ids[ordinal]
                    image_path = output["receipt"]["output_asset"]
                    is_selected = image_path == selected_path
                    review = self.reviews.get(image_id)
                    if not isinstance(review, dict) and is_selected:
                        review = self.reviews.get(generation_id)
                    if not isinstance(review, dict):
                        review = self._default_review()
                    machine = output.get("review", {}) if isinstance(output.get("review"), dict) else {}
                    assets.append(Asset(
                        asset_id=image_id, generation_id=generation_id, renderer=renderer,
                        preset=str(output.get("preset") or output.get("receipt", {}).get("preset") or f"{renderer}_historical"),
                        is_final_selection=is_selected, character=char_name,
                        thumbnail_path=image_path, full_image_path=image_path,
                        source_run_id=run.run_id, source_mission_id=candidate.get("source_mission_id", ""),
                        concept_id=candidate.get("concept_id", ""), concept_snapshot=candidate.get("original_proposal", {}).get("snapshot", ""),
                        final_status="MACHINE_PASS" if machine.get("verdict") == "PASS" else candidate.get("pipeline_state", "UNKNOWN"),
                        final_review_verdict=machine.get("verdict", "UNKNOWN"), created_at=run.created_at,
                        creative_model=candidate.get("source_model", run.source_model), favorite=bool(review.get("favorite")),
                        franchise=char_info.get("franchise", "Unknown"), universe=char_info.get("universe", "Unknown"), tags=char_info.get("tags", []),
                        human_review=review, character_profile=candidate.get("character_profile", {}),
                        character_contract=candidate.get("character_contract", {}), resolved_render_spec=spec,
                        stage_render_plans={item["renderer"]: item.get("stage_render_plan", {}) for item in normalized},
                        prompt_artifacts={item["renderer"]: item.get("prompt_artifact", {}) for item in normalized},
                        render_receipts={item["renderer"]: item.get("receipt", {}) for item in normalized},
                        review_observations={item["renderer"]: item.get("review_observation", {}) for item in normalized},
                        stage_images={item["renderer"]: item["receipt"]["output_asset"] for item in normalized},
                        comparative_review=candidate.get("comparative_review", {}), automatic_final_stage_decision=decision,
                        effective_final_stage_decision=decision, source_artifact_root=str(run_dir.resolve()),
                        render_outputs=normalized,
                        comparison_outputs=reference_outputs + [output] if reference_outputs else [],
                        source_asset_id=candidate.get("source_asset_id", ""), render_intent=render_intent,
                        lineage={"generation_id": generation_id, "image_id": image_id, "renderer": renderer, "sibling_image_ids": image_ids, "selected_image_id": image_id if is_selected else next((iid for iid, item in zip(image_ids, normalized) if item["receipt"]["output_asset"] == selected_path), ""), "source_asset_id": candidate.get("source_asset_id", ""), "source_generation_id": candidate.get("source_generation_id", ""), "generation_mode": candidate.get("generation_mode", "direct"), "alternative_mode": candidate.get("alternative_mode", ""), "source_context": candidate.get("source_context", {}), "creation_mode": creation_mode, "stock_policy_version": candidate.get("stock_policy_version", "")},
                        display_title=display_title, short_description=short_description,
                        agent_rating=_agent_rating(machine), agent_scores=machine.get("agent_scores", {}) if isinstance(machine.get("agent_scores"), dict) else {},
                        creation_mode=creation_mode,
                    ))
        assets.sort(key=lambda asset: (asset.created_at, asset.generation_id, asset.renderer), reverse=True)
        derived = self._save_index(assets)
        explicit = self._load_explicit_images()
        explicit_ids = {item.get("asset_id") for item in explicit}
        self.index = [item for item in derived if item.get("asset_id") not in explicit_ids] + explicit
        self._write_index_records(self.index)
        return self.index

    def register_reinterpretation(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Register one explicitly requested completed render; never scans request folders."""
        if record.get("status") != "COMPLETE" or not Path(record.get("output_asset", "")).is_file():
            raise ValueError("Only a completed reinterpretation with a real output can enter Library")
        request_id = _text(record.get("request_id"))
        renderer = _text(record.get("renderer"))
        receipt = record.get("render_receipt", {}) if isinstance(record.get("render_receipt"), dict) else {}
        resolved = record.get("reinterpreted_render_spec", {}).get("resolved_scene", {})
        resolved = resolved if isinstance(resolved, dict) else {}
        snapshot = _text(record.get("scene_template_spec", {}).get("snapshot"))
        title, description = _display_metadata(record.get("target_character", "Unknown"), resolved, snapshot)
        asset_id = f"{request_id}::{renderer}"
        review = self.reviews.get(asset_id, self._default_review())
        image = Asset(
            asset_id=asset_id, generation_id=request_id, renderer=renderer,
            preset=_text(receipt.get("preset")), is_final_selection=True,
            character=record.get("target_character", "Unknown"),
            thumbnail_path=record["output_asset"], full_image_path=record["output_asset"],
            source_run_id=request_id, source_mission_id="", concept_id=f"reinterpret:{request_id}",
            concept_snapshot=snapshot, final_status="UNREVIEWED", final_review_verdict="UNKNOWN",
            created_at=record.get("completed_at") or record.get("created_at", ""),
            creative_model=f"{renderer}_direct_reinterpret", favorite=bool(review.get("favorite")),
            human_review=review, character_contract=record.get("target_character_contract", {}),
            resolved_render_spec=resolved, prompt_artifacts={renderer:record.get("renderer_prompt_artifact", {})},
            render_receipts={renderer:receipt}, stage_images={renderer:record["output_asset"]},
            source_artifact_root=str((RENDERER_RUNS_ROOT / "reinterpretations" / request_id).resolve()),
            render_outputs=[{"renderer":renderer, "preset":receipt.get("preset", ""), "receipt":receipt, "review":{}}],
            source_asset_id=record.get("source_asset_id", ""), render_intent=record.get("render_intent", ""),
            lineage={"generation_id":request_id, "image_id":asset_id, "renderer":renderer, "sibling_image_ids":[asset_id], "selected_image_id":asset_id, "source_asset_id":record.get("source_asset_id", ""), "source_generation_id":record.get("source_generation_id", ""), "generation_mode":"reinterpretation", "template_mode":record.get("template_mode", "")},
            display_title=title, short_description=description, agent_rating=None,
        ).to_dict()
        with _EXPLICIT_IMAGES_LOCK:
            explicit = self._load_explicit_images()
            explicit = [item for item in explicit if item.get("asset_id") != asset_id] + [image]
            explicit = self._save_explicit_images(explicit)
            image = next(item for item in explicit if item.get("asset_id") == asset_id)
        self.index = [item for item in self.index if item.get("asset_id") != asset_id] + [image]
        self._write_index_records(self.index)
        return image

    def get_assets(self, mission_id: Optional[str] = None) -> List[Dict]:
        if not self.index:
            self.build_index()
        # Apply human state dynamically while preserving the automatic decision.
        try:
            characters = json.loads(CHARACTERS_PATH.read_text(encoding="utf-8"))
        except Exception:
            characters = {}
        for a in self.index:
            review = self.reviews.get(a["asset_id"], self._default_review())
            a["favorite"] = bool(review.get("favorite"))
            a["human_review"] = review
            a["human_rating"] = review.get("rating") if isinstance(review.get("rating"), int) else None
            human_status = review.get("status", "UNREVIEWED")
            a["library_status"] = (
                "REJECTED" if human_status == "REJECTED" else
                "APPROVED" if human_status == "APPROVED" or a.get("final_review_verdict") == "PASS" else
                "UNREVIEWED"
            )
            a["hidden_from_default_gallery"] = a["library_status"] == "REJECTED"
            entry = characters.get(a.get("character"), {}) if isinstance(characters, dict) else {}
            entry = entry if isinstance(entry, dict) else {}
            current_franchise = _text(a.get("franchise"))
            if not current_franchise or current_franchise.casefold() == "unknown":
                a["franchise"] = _text(entry.get("franchise")) or _text(entry.get("universe")) or "Unknown"
            current_universe = _text(a.get("universe"))
            if not current_universe or current_universe.casefold() == "unknown":
                a["universe"] = _text(entry.get("universe")) or a["franchise"]
            if not a.get("tags") and isinstance(entry.get("tags"), list):
                a["tags"] = entry["tags"]
            raw_character = _text(a.get("character")) or "Unknown"
            a["character_display_name"] = _text(entry.get("name")) or raw_character
            stored_title = _text(a.get("display_title"))
            if stored_title.startswith(f"{raw_character} —") and a["character_display_name"] != raw_character:
                a["display_title"] = a["character_display_name"] + stored_title[len(raw_character):]
            collection_id = _text(a.get("franchise")) or "Unknown"
            a["collection_id"] = collection_id
            a["collection_display_name"] = collection_display_name(collection_id, entry)
            a["is_visible_library_asset"] = is_visible_library_asset(a)
            a["generated_at"] = _generated_at(a.get("full_image_path", ""), a.get("created_at", ""))
            if not a.get("display_title") or not a.get("short_description"):
                title, description = _display_metadata(
                    a.get("character_display_name", "Unknown"), a.get("resolved_render_spec", {}), a.get("concept_snapshot", "")
                )
                a["display_title"] = a.get("display_title") or title
                a["short_description"] = a.get("short_description") or description
            # Old reviews remain unscored unless they contain a real numeric image score.
            output = next((item for item in a.get("render_outputs", []) if item.get("renderer") == a.get("renderer")), {})
            a["agent_rating"] = _agent_rating(output.get("review", {}))
            a["human_stage_overrides"] = review.get("preference_history", [])
            automatic = a.get("automatic_final_stage_decision", {})
            effective = dict(automatic) if isinstance(automatic, dict) else {}
            preference = str(review.get("preference", "NONE")).casefold()
            stage_images = a.get("stage_images", {})
            if preference != "none" and stage_images.get(preference):
                latest = a["human_stage_overrides"][-1] if a["human_stage_overrides"] else {}
                effective = {
                    "schema_version": "final_stage_decision_v1_human_effective",
                    "decision_id": latest.get("override_id", ""),
                    "selected_stage": preference,
                    "selected_image": stage_images[preference],
                    "reason": latest.get("reason", "Manual Library stage preference"),
                    "source": "human_override",
                    "automatic_decision_id": automatic.get("decision_id", ""),
                    "automatic": False,
                }
            a["effective_final_stage_decision"] = effective
            # A Library Image is immutable as an individual renderer output. A
            # generation-level selection never changes which pixels this record shows.
        if mission_id:
            return [a for a in self.index if a.get("source_mission_id") == mission_id]
        return self.index

    def get_visible_assets(self, mission_id: Optional[str] = None) -> List[Dict]:
        return visible_library_assets(self.get_assets(mission_id=mission_id))

    @staticmethod
    def _read_json(path: Path) -> Dict[str, Any]:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
            return value if isinstance(value, dict) else {}
        except Exception:
            return {}

    def search(self, query: str) -> List[Dict]:
        if not self.index:
            self.build_index()
        query_lower = query.lower()
        return [a for a in self.index if 
                query_lower in a.get("character", "").lower() or
                query_lower in a.get("franchise", "").lower() or
                query_lower in a.get("universe", "").lower() or
                query_lower in a.get("concept_snapshot", "").lower() or
                any(query_lower in t.lower() for t in a.get("tags", []))]
    
    def get_collections(self) -> Dict[str, Dict[str, Any]]:
        try:
            characters = json.loads(CHARACTERS_PATH.read_text(encoding="utf-8"))
        except Exception:
            characters = {}
        return summarize_visible_collections(self.get_assets(), characters)
