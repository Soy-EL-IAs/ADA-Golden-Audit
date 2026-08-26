import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional

from scripts.ada_paths import MISSIONS_ROOT

MISSIONS_DIR = MISSIONS_ROOT

class ProductionMission:
    STATES = ["CREATED", "WAITING_FOR_GPU", "RUNNING", "PLANNING", "GENERATING_CONCEPTS", "PRODUCING", "RECOVERING", "COMPLETE", "PARTIAL", "FAILED", "CANCELLED"]
    
    def __init__(self, mission_id: str = None, character: str = "", requested_assets: int = 6,
                 what_happens: str = "", where: str = "",
                 creative_model: str = "qwen3.5-9b-uncensored-hauhaucs-aggressive",
                 concept_multiplier: int = 3, production_buffer: int = 2,
                 max_rounds: int = 2, generate_miaomiao_alternative: bool = False, renderer_choice: str = "lustify", render_intent: str = "semi_realistic",
                 source_asset_id: str = "", source_generation_id: str = "", generation_mode: str = "direct",
                 alternative_mode: str = "", alternative_instruction: str = "", source_context: Dict[str, Any] = None,
                 creation_mode: str = "scene", outfit_override: str | None = None, renderer_routing: Dict[str, Any] = None):
        self.mission_id = mission_id or f"mission_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        self.created_at = datetime.now().isoformat()
        self.character = character
        self.requested_assets = requested_assets
        self.what_happens = what_happens
        self.where = where
        self.status = "CREATED"
        self.creative_model = creative_model
        self.cancelled = False
        
        # Config
        self.concept_multiplier = concept_multiplier
        self.production_buffer = production_buffer
        self.max_rounds = max_rounds
        # New missions persist the explicit secondary choice.  Missing on old
        # records means false, preserving their historical execution path.
        self.generate_miaomiao_alternative = bool(generate_miaomiao_alternative)
        self.renderer_choice = renderer_choice if renderer_choice in {"lustify", "miaomiao"} else "lustify"
        self.render_intent = "anime" if self.renderer_choice == "miaomiao" else (render_intent if render_intent in {"anime", "semi_realistic", "photorealistic"} else "semi_realistic")
        self.source_asset_id = source_asset_id
        self.source_generation_id = source_generation_id
        self.generation_mode = generation_mode
        self.alternative_mode = alternative_mode
        self.alternative_instruction = alternative_instruction
        self.source_context = source_context or {}
        self.creation_mode = creation_mode if creation_mode in {"scene", "stock"} else "scene"
        self.stock_policy_version = "stock_v1" if self.creation_mode == "stock" else ""
        self.outfit_override = outfit_override.strip() if self.creation_mode == "stock" and isinstance(outfit_override, str) and outfit_override.strip() else None
        self.renderer_routing = renderer_routing or {}
        from ada_app.creative_intent import build_creative_intent_envelope
        self.creative_intent = {} if self.creation_mode == "stock" else build_creative_intent_envelope(
            character=character, setting=where, action=what_happens, render_intent=self.render_intent
        )
        
        # Tracking
        self.current_round = 0
        self.source_runs: List[str] = []
        self.generated_concepts = 0
        self.selected_candidates = 0
        self.approved_assets = 0
        self.rejected_quality = 0
        self.retry_exhausted = 0
        self.failed_runtime = 0
        self.active_candidates = 0
        self.started_at: Optional[str] = None
        self.completed_at: Optional[str] = None
        self.current_stage_detail = ""
        self.error_message = ""
        self.failure_details: List[Dict[str, Any]] = []
    
    @property
    def initial_concepts(self) -> int:
        return max(12, self.requested_assets * self.concept_multiplier)
    
    @property
    def initial_candidates(self) -> int:
        return self.requested_assets + max(2, self.requested_assets // 2)
    
    @property 
    def progress(self) -> float:
        if self.requested_assets == 0: return 0
        return min(1.0, self.approved_assets / self.requested_assets)
    
    @property
    def is_target_met(self) -> bool:
        return self.approved_assets >= self.requested_assets
    
    @property
    def duration_seconds(self) -> Optional[float]:
        if not self.started_at: return None
        end = self.completed_at or datetime.now().isoformat()
        try:
            start = datetime.fromisoformat(self.started_at)
            finish = datetime.fromisoformat(end)
            return (finish - start).total_seconds()
        except: return None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "mission_id": self.mission_id,
            "created_at": self.created_at,
            "character": self.character,
            "requested_assets": self.requested_assets,
            "what_happens": getattr(self, "what_happens", ""),
            "where": getattr(self, "where", ""),
            "status": self.status,
            "creative_model": self.creative_model,
            "cancelled": self.cancelled,
            "concept_multiplier": self.concept_multiplier,
            "production_buffer": self.production_buffer,
            "max_rounds": self.max_rounds,
            "generate_miaomiao_alternative": getattr(self, "generate_miaomiao_alternative", False),
            "renderer_choice": getattr(self, "renderer_choice", "miaomiao" if getattr(self, "generate_miaomiao_alternative", False) else "lustify"),
            "render_intent": getattr(self, "render_intent", "semi_realistic"),
            "source_asset_id": getattr(self, "source_asset_id", ""),
            "source_generation_id": getattr(self, "source_generation_id", ""),
            "generation_mode": getattr(self, "generation_mode", "direct"),
            "alternative_mode": getattr(self, "alternative_mode", ""),
            "alternative_instruction": getattr(self, "alternative_instruction", ""),
            "source_context": getattr(self, "source_context", {}),
            "creation_mode": getattr(self, "creation_mode", "scene"),
            "stock_policy_version": getattr(self, "stock_policy_version", ""),
            "outfit_override": getattr(self, "outfit_override", None),
            "renderer_routing": getattr(self, "renderer_routing", {}),
            "creative_intent": getattr(self, "creative_intent", {}),
            "current_round": self.current_round,
            "source_runs": self.source_runs,
            "generated_concepts": self.generated_concepts,
            "selected_candidates": self.selected_candidates,
            "approved_assets": self.approved_assets,
            "rejected_quality": self.rejected_quality,
            "retry_exhausted": self.retry_exhausted,
            "failed_runtime": self.failed_runtime,
            "active_candidates": self.active_candidates,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "current_stage_detail": self.current_stage_detail,
            "error_message": self.error_message,
            "failure_details": getattr(self, "failure_details", []),
            "progress": self.progress,
            "initial_concepts": self.initial_concepts,
            "initial_candidates": self.initial_candidates,
            "duration_seconds": self.duration_seconds
        }
    
    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'ProductionMission':
        m = cls.__new__(cls)
        for k, v in d.items():
            if k in ('progress', 'initial_concepts', 'initial_candidates', 'duration_seconds'):
                continue  # computed properties
            setattr(m, k, v)
        return m


class MissionStore:
    DELETABLE_STATUSES = frozenset({"FAILED", "COMPLETE", "CANCELLED"})

    def __init__(self):
        MISSIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    def _path(self, mission_id: str) -> Path:
        return MISSIONS_DIR / f"{mission_id}.json"
    
    def save(self, mission: ProductionMission):
        self._path(mission.mission_id).write_text(
            json.dumps(mission.to_dict(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8"
        )
    
    def load(self, mission_id: str) -> Optional[ProductionMission]:
        p = self._path(mission_id)
        if not p.exists(): return None
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            return ProductionMission.from_dict(d)
        except: return None
    
    def list_all(self) -> List[ProductionMission]:
        missions = []
        for p in sorted(MISSIONS_DIR.glob("mission_*.json"), reverse=True):
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
                missions.append(ProductionMission.from_dict(d))
            except: continue
        return missions
    
    def update(self, mission: ProductionMission, **kwargs):
        for k, v in kwargs.items():
            setattr(mission, k, v)
        self.save(mission)

    def delete(self, mission_id: str) -> ProductionMission:
        mission = self.load(mission_id)
        if mission is None:
            raise FileNotFoundError(mission_id)
        if mission.status not in self.DELETABLE_STATUSES:
            raise ValueError(f"Mission status {mission.status} cannot be deleted")
        self._path(mission_id).unlink()
        return mission
