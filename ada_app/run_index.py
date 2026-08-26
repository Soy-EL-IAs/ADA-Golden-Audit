import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

from scripts.ada_paths import MISSION_RUNS_ROOT

class RunInfo:
    def __init__(self, run_id: str, run_type: str, created_at: str, status: str, 
                 character: Optional[str] = None, source_model: Optional[str] = None,
                 pipeline_stage: Optional[str] = None, artifact_root: Optional[str] = None,
                 final_assets_count: int = 0, error_state: Optional[str] = None,
                 duration: Optional[float] = None):
        self.run_id = run_id
        self.run_type = run_type
        self.created_at = created_at
        self.status = status
        self.character = character
        self.source_model = source_model
        self.pipeline_stage = pipeline_stage
        self.artifact_root = artifact_root
        self.final_assets_count = final_assets_count
        self.error_state = error_state
        self.duration = duration
        
    def to_dict(self):
        return {
            "run_id": self.run_id,
            "run_type": self.run_type,
            "created_at": self.created_at,
            "status": self.status,
            "character": self.character,
            "source_model": self.source_model,
            "pipeline_stage": self.pipeline_stage,
            "artifact_root": self.artifact_root,
            "final_assets_count": self.final_assets_count,
            "error_state": self.error_state,
            "duration": self.duration
        }

class BaseRunAdapter:
    def get_runs(self) -> List[RunInfo]:
        raise NotImplementedError()

class M2CreativeAdapter(BaseRunAdapter):
    def __init__(self, root: Path):
        self.root = root
        
    def get_runs(self) -> List[RunInfo]:
        runs = []
        if not self.root.exists():
            return runs
            
        for run_dir in self.root.iterdir():
            if not run_dir.is_dir() or not run_dir.name.startswith("m2_"):
                continue
                
            manifest_path = run_dir / "manifest.json"
            if not manifest_path.exists():
                continue
                
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
            except Exception:
                continue
                
            run_id = manifest.get("run_id", run_dir.name)
            
            # Check if this has Pilot extensions
            is_pilot = (run_dir / "pilot").exists() or (run_dir / "pilot_candidates.json").exists()
            run_type = "Pilot" if is_pilot else "Creative"
            
            # Count final assets (pilot)
            final_assets = 0
            if is_pilot:
                pilot_cand_path = run_dir / "pilot_candidates.json"
                if pilot_cand_path.exists():
                    try:
                        with open(pilot_cand_path, "r", encoding="utf-8") as f:
                            cands = json.load(f)
                        for c in cands:
                            visible_states = {"APPROVED", "REJECTED_QUALITY", "RETRY_EXHAUSTED", "FINAL", "COMPLETE"}
                            has_new_outputs = bool(c.get("render_outputs"))
                            has_legacy_image = "klein_image" in c or "illustrious_render_receipt" in c
                            if c.get("pipeline_state") in visible_states and (has_new_outputs or has_legacy_image):
                                final_assets += 1
                    except Exception:
                        pass

            telemetry = manifest.get("telemetry", {})
            duration = telemetry.get("duration_seconds")
            
            # Extract character if not in manifest
            character_val = manifest.get("character")
            if not character_val:
                try:
                    cp_path = run_dir / "character_profile.json"
                    if cp_path.exists():
                        with open(cp_path, "r", encoding="utf-8") as f:
                            cp = json.load(f)
                            character_val = cp.get("requested_character", cp.get("name", "Unknown"))
                    else:
                        character_val = "Unknown"
                except Exception:
                    character_val = "Unknown"
                    
            runs.append(RunInfo(
                run_id=run_id,
                run_type=run_type,
                created_at=manifest.get("started_at", "Unknown"),
                status=manifest.get("status", "Unknown"),
                character=character_val,
                source_model=manifest.get("creative_expansion_model", "Unknown"),
                pipeline_stage="COMPLETE_TEXT_ONLY" if not is_pilot else "PILOT_RUN",
                artifact_root=str(run_dir),
                final_assets_count=final_assets,
                duration=duration
            ))
            
        return runs

class LegacySpecialistAdapter(BaseRunAdapter):
    def __init__(self, root: Path):
        self.root = root
        
    def get_runs(self) -> List[RunInfo]:
        runs = []
        if not self.root.exists():
            return runs
            
        for run_dir in self.root.iterdir():
            if not run_dir.is_dir() or run_dir.name.startswith("m"):
                continue
                
            manifest_path = run_dir / "manifest.json"
            if not manifest_path.exists():
                continue
                
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
            except Exception:
                continue
                
            run_id = manifest.get("run_id", run_dir.name)
            
            # Attempt to deduce character
            character = "Unknown"
            if "2b" in run_id.lower(): character = "2B"
            elif "tifa" in run_id.lower(): character = "Tifa"
            elif "ada" in run_id.lower(): character = "Ada"

            # Check final images
            final_assets = 0
            if "klein_candidates" in manifest:
                final_assets = len(manifest["klein_candidates"])
                
            runs.append(RunInfo(
                run_id=run_id,
                run_type="Image Pipeline",
                created_at=manifest.get("created_at", "Unknown"),
                status=manifest.get("status", "Unknown"),
                character=character,
                artifact_root=str(run_dir),
                final_assets_count=final_assets
            ))
            
        return runs

class RunIndex:
    def __init__(self):
        self.adapters = [
            M2CreativeAdapter(MISSION_RUNS_ROOT),
        ]
        
    def get_all_runs(self) -> List[RunInfo]:
        runs = []
        for adapter in self.adapters:
            try:
                runs.extend(adapter.get_runs())
            except Exception as e:
                print(f"Adapter {adapter.__class__.__name__} failed: {e}")
        
        # Sort by creation date descending
        def sort_key(r: RunInfo):
            if r.created_at == "Unknown":
                return ""
            return r.created_at
            
        runs.sort(key=sort_key, reverse=True)
        return runs

if __name__ == "__main__":
    idx = RunIndex()
    for r in idx.get_all_runs():
        print(r.to_dict())
