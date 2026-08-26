import json, time, threading, traceback, subprocess
from pathlib import Path
from datetime import datetime
from typing import List

import sys
from scripts.ada_paths import ADA_ROOT, CHARACTERS_ROOT, LOCKS_ROOT, MISSION_RUNS_ROOT
sys.path.insert(0, str(ADA_ROOT / "scripts"))

from ada_app.mission import ProductionMission, MissionStore
from ada_app.pilot_runner import read_json, write_json
from ada_app.renderer_pipeline import run_renderer_pipeline
from ada_app.m3_filter import run_m3_analysis
from ada_app.m4_selection import select_top_candidates

RUNS_DIR = MISSION_RUNS_ROOT
M2_SCRIPT = ADA_ROOT / "experimental" / "m1_creative_expansion_lab" / "run_m2.py"
M2_CONFIG = ADA_ROOT / "experimental" / "m1_creative_expansion_lab" / "m2_config.json"
CHARACTERS_CONFIG = CHARACTERS_ROOT / "catalog.json"


def character_version(character: str) -> str:
    characters = read_json(CHARACTERS_CONFIG)
    entry = characters.get(character)
    if not isinstance(entry, dict):
        raise ValueError(f"Character is not registered: {character}")
    version = entry.get("version") or entry.get("universe")
    if not isinstance(version, str) or not version.strip():
        raise ValueError(f"Registered character has no version or universe: {character}")
    return version.strip()


def m2_failure_detail(run_dir: Path, completed: subprocess.CompletedProcess) -> dict:
    """Return the durable M2 error, including child-process diagnostics."""
    failure_path = run_dir / "failure.json"
    failure = {}
    if failure_path.is_file():
        try:
            failure = json.loads(failure_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            failure = {}
    return {
        "stage": "GENERATING_CONCEPTS",
        "run_id": run_dir.name,
        "exit_code": completed.returncode,
        "error_type": failure.get("error_type", "M2ProcessError"),
        "message": failure.get("error") or completed.stderr.strip() or "M2 exited without an error artifact.",
        "stderr": completed.stderr.strip(),
        "stdout": completed.stdout.strip(),
    }


def m2_missing_manifest_detail(run_dir: Path, completed: subprocess.CompletedProcess) -> dict:
    """Describe a successful child exit that did not publish its expected manifest."""
    manifest_path = run_dir / "manifest.json"
    return {
        "stage": "GENERATING_CONCEPTS",
        "run_id": run_dir.name,
        "exit_code": completed.returncode,
        "error_type": "M2ManifestMissing",
        "message": f"Explicit M2 run did not complete: {run_dir}",
        "expected_manifest": str(manifest_path),
        "stderr": completed.stderr.strip(),
        "stdout": completed.stdout.strip(),
    }


def run_stock_mission(mission: ProductionMission, store: MissionStore) -> None:
    """Run Stock directly from Character Contract to renderer; no M1/M2/M3/M4."""
    run_id = f"m2_stock_{mission.mission_id}_{datetime.now().strftime('%H%M%S%f')}"
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    started_at = datetime.now().isoformat()
    manifest = {
        "run_id": run_id,
        "started_at": started_at,
        "status": "RUNNING",
        "character": mission.character,
        "creation_mode": "stock",
        "stock_policy_version": "stock_v1",
        "creative_expansion_model": "none_stock_direct",
    }
    write_json(run_dir / "manifest.json", manifest)
    write_json(run_dir / "character_profile.json", {"requested_character": mission.character})
    target_accepted = mission.requested_assets
    max_attempts = target_accepted * 3  # Configurable limit
    attempted = 0
    accepted = 0
    rejected = 0
    
    candidates_file = run_dir / "pilot_candidates.json"
    
    mission.source_runs.append(run_id)
    mission.current_round = 1
    store.update(mission, status="PRODUCING", current_stage_detail=f"Producing Stock image(s) [0/{target_accepted}]...")
    
    while accepted < target_accepted and attempted < max_attempts:
        concept_id = f"stock_{(attempted + 1):03d}"
        candidate = {
            "concept_id": concept_id,
            "pipeline_state": "PENDING",
            "character": mission.character,
            "source_mission_id": mission.mission_id,
            "creation_mode": "stock",
            "stock_policy_version": "stock_v1",
            "renderer_routing": getattr(mission, "renderer_routing", {}),
            "original_proposal": {},
            "generation_mode": "stock",
        }
        
        if candidates_file.exists():
            durable_candidates = read_json(candidates_file)
        else:
            durable_candidates = []
            
        durable_candidates.append(candidate)
        write_json(candidates_file, durable_candidates)
        
        run_renderer_pipeline(
            run_dir, [candidate], target_approvals=1,
            renderer_choice=mission.renderer_choice, render_intent=mission.render_intent,
            creation_mode="stock", outfit_override=getattr(mission, "outfit_override", None),
            renderer_routing=getattr(mission, "renderer_routing", {}), continue_on_error=True,
        )
        
        # Re-read candidate state and reconcile counters from durable truth
        refreshed_candidates = read_json(candidates_file)
        attempted = len(refreshed_candidates)
        accepted = sum(1 for c in refreshed_candidates if c.get("pipeline_state") == "APPROVED")
        rejected = sum(1 for c in refreshed_candidates if c.get("pipeline_state") not in {"APPROVED", "PENDING"})
            
        store.update(mission, current_stage_detail=f"Producing Stock image(s) [{accepted}/{target_accepted}]... (Attempt {attempted})")

    final_candidates = read_json(run_dir / "pilot_candidates.json")
    mission.selected_candidates = attempted
    mission.approved_assets = accepted
    mission.rejected_quality = sum(1 for item in final_candidates if item.get("pipeline_state") in {"REVIEW_FAILED", "REJECTED_QUALITY"})
    mission.failed_runtime = sum(1 for item in final_candidates if item.get("pipeline_state") in {"FAILED_RUNTIME", "CONTRACT_FAILURE", "SETUP_FAILURE"})
    mission.active_candidates = 0
    
    final_status = "COMPLETE" if accepted >= target_accepted else "PARTIAL" if accepted > 0 else "FAILED"
    manifest.update({
        "status": final_status, 
        "completed_at": datetime.now().isoformat(), 
        "final_assets_count": accepted,
        "requested": target_accepted,
        "attempted": attempted,
        "accepted": accepted,
        "rejected": rejected
    })
    write_json(run_dir / "manifest.json", manifest)
    try:
        from ada_app.asset_library import AssetLibrary
        from ada_app.character_capabilities import save_character_hero
        library = AssetLibrary()
        library.build_index()
        if mission.approved_assets:
            stock_assets = [
                asset for asset in library.get_assets(mission_id=mission.mission_id)
                if asset.get("creation_mode") == "stock"
                and asset.get("is_visible_library_asset") is True
                and asset.get("is_final_selection")
            ]
            if stock_assets:
                hero = max(stock_assets, key=lambda asset: asset.get("generated_at") or asset.get("created_at") or "")
                save_character_hero(mission.character, hero["asset_id"])
    except Exception:
        traceback.print_exc()
    store.update(
        mission, status=final_status, completed_at=datetime.now().isoformat(),
        current_stage_detail=f"Stock {final_status}: {mission.approved_assets}/{mission.requested_assets} approved",
    )

def run_mission(mission_id: str):
    store = MissionStore()
    mission = store.load(mission_id)
    if not mission:
        return
    
    import filelock
    LOCKS_ROOT.mkdir(parents=True, exist_ok=True)
    lock = filelock.FileLock(str(LOCKS_ROOT / "gpu_execution.lock"))
    
    try:
        store.update(mission, status="WAITING_FOR_GPU", current_stage_detail="Waiting for GPU lock...")
        with lock.acquire(timeout=86400):
            mission.started_at = datetime.now().isoformat()
            store.update(mission, status="RUNNING", current_stage_detail="Acquired GPU lock, starting...")
            _run_mission_internal(mission_id, store, mission)
    except Exception as e:
        traceback.print_exc()
        store.update(mission, status="FAILED", error_message=str(e), completed_at=datetime.now().isoformat())

def _run_mission_internal(mission_id: str, store: MissionStore, mission: ProductionMission):
    try:
        if getattr(mission, "creation_mode", "scene") == "stock":
            run_stock_mission(mission, store)
            return
        remaining_needed = mission.requested_assets
        
        for round_num in range(1, mission.max_rounds + 1):
            if mission.cancelled:
                store.update(mission, status="CANCELLED", completed_at=datetime.now().isoformat())
                return
            
            if remaining_needed <= 0:
                break
                
            mission.current_round = round_num
            
            # --- PHASE 1: Generate Concepts ---
            store.update(mission, status="GENERATING_CONCEPTS",
                        current_stage_detail=f"Round {round_num}: Generating concepts...")
            
            if round_num == 1:
                concept_count = mission.initial_concepts
                candidate_count = mission.initial_candidates
            else:
                concept_count = max(12, remaining_needed * 3)
                candidate_count = remaining_needed + max(2, remaining_needed // 2)
            
            # Update M2 config
            config = read_json(M2_CONFIG)
            config["requested_count"] = concept_count
            config["character"] = mission.character
            config["version"] = character_version(mission.character)
            if getattr(mission, "what_happens", ""):
                config["what_happens"] = mission.what_happens
            if getattr(mission, "where", ""):
                config["where"] = mission.where
            config["generation_context"] = {
                "mode": getattr(mission, "generation_mode", "direct"),
                "source_asset_id": getattr(mission, "source_asset_id", ""),
                "source_generation_id": getattr(mission, "source_generation_id", ""),
                "alternative_mode": getattr(mission, "alternative_mode", ""),
                "alternative_instruction": getattr(mission, "alternative_instruction", ""),
                "source_context": getattr(mission, "source_context", {}),
            }
            config["creative_intent"] = getattr(mission, "creative_intent", {})
            write_json(M2_CONFIG, config)
            
            # Auto-load the creative model required for M2 using existing infrastructure
            try:
                from lmstudio_controller import LMStudioController
                controller = LMStudioController()
                controller.activate_role("premise_agent")
            except Exception as e:
                traceback.print_exc()
                store.update(mission, status="FAILED", error_message=f"Failed to auto-load 9B model: {e}", completed_at=datetime.now().isoformat())
                return
            
            # Bind this subprocess to one exact run directory. Never discover its
            # result by timestamp because concurrent missions could cross-link.
            generated_run_id = (
                f"m2_{mission_id}_r{round_num:02d}_"
                f"{datetime.now().strftime('%H%M%S%f')}"
            )
            generated_run = RUNS_DIR / generated_run_id
            completed = subprocess.run(
                ["python", str(M2_SCRIPT), "--run-id", generated_run_id],
                cwd=str(ADA_ROOT), capture_output=True, text=True,
            )
            if completed.returncode:
                detail = m2_failure_detail(generated_run, completed)
                mission.failure_details = list(getattr(mission, "failure_details", [])) + [detail]
                store.update(
                    mission,
                    status="FAILED",
                    error_message=f"M2 {detail['error_type']}: {detail['message']}",
                    completed_at=datetime.now().isoformat(),
                )
                return
            if not (generated_run / "manifest.json").is_file():
                detail = m2_missing_manifest_detail(generated_run, completed)
                mission.failure_details = list(getattr(mission, "failure_details", [])) + [detail]
                store.update(
                    mission,
                    status="FAILED",
                    error_message=detail["message"],
                    failure_details=mission.failure_details,
                    completed_at=datetime.now().isoformat(),
                )
                return

            mission.source_runs.append(generated_run.name)
            
            # Read and count concepts
            records = read_json(generated_run / "proposal_records.json")
            all_records = records.get("records", [])
            mission.generated_concepts += len(all_records)
            store.update(mission, current_stage_detail=f"Round {round_num}: {len(all_records)} concepts generated. Running M3/M4...")
            
            # Reload mission in case cancelled
            mission = store.load(mission_id)
            if mission.cancelled:
                store.update(mission, status="CANCELLED", completed_at=datetime.now().isoformat())
                return
            
            # --- PHASE 2: M3 + M4 ---
            m3_analysis = run_m3_analysis(all_records)
            write_json(generated_run / "m3_analysis.json", m3_analysis)
            
            candidates = select_top_candidates(all_records, m3_analysis, top_n=candidate_count)
            
            # Add mission_id to each candidate
            for c in candidates:
                c["source_mission_id"] = mission_id
                c["source_asset_id"] = getattr(mission, "source_asset_id", "")
                c["source_generation_id"] = getattr(mission, "source_generation_id", "")
                c["generation_mode"] = getattr(mission, "generation_mode", "direct")
                c["alternative_mode"] = getattr(mission, "alternative_mode", "")
                c["alternative_instruction"] = getattr(mission, "alternative_instruction", "")
                c["source_context"] = getattr(mission, "source_context", {})
                c["creative_intent"] = getattr(mission, "creative_intent", {})
            
            write_json(generated_run / "pilot_candidates.json", candidates)
            mission.selected_candidates += len(candidates)
            
            # --- PHASE 3: Production ---
            store.update(mission, status="PRODUCING",
                        active_candidates=len(candidates),
                        current_stage_detail=f"Round {round_num}: Producing {len(candidates)} candidates...")
            
            # Run pilot pipeline synchronously within mission thread
            remaining_needed = mission.requested_assets - mission.approved_assets
            renderer_choice = getattr(
                mission,
                "renderer_choice",
                "miaomiao" if bool(getattr(mission, "generate_miaomiao_alternative", False)) else "lustify",
            )
            run_renderer_pipeline(
                generated_run,
                candidates,
                target_approvals=remaining_needed,
                renderer_choice=renderer_choice,
                render_intent=getattr(mission, "render_intent", "semi_realistic"),
            )
            
            # --- PHASE 4: Count results ---
            final_candidates = read_json(generated_run / "pilot_candidates.json")
            round_approved = sum(1 for c in final_candidates if c.get("pipeline_state") == "APPROVED")
            round_rejected = sum(1 for c in final_candidates if c.get("pipeline_state") == "REJECTED_QUALITY")
            round_exhausted = sum(1 for c in final_candidates if c.get("pipeline_state") == "RETRY_EXHAUSTED")
            failed_states = {"FAILED_RUNTIME", "SETUP_FAILURE", "CONTRACT_FAILURE"}
            round_failed = sum(1 for c in final_candidates if c.get("pipeline_state") in failed_states)
            round_failure_details = [
                detail for c in final_candidates
                if c.get("pipeline_state") in failed_states
                for detail in [c.get("failure_details")]
                if isinstance(detail, dict)
            ]
            
            mission.approved_assets += round_approved
            mission.rejected_quality += round_rejected
            mission.retry_exhausted += round_exhausted
            mission.failed_runtime += round_failed
            mission.failure_details = list(getattr(mission, "failure_details", [])) + round_failure_details
            mission.active_candidates = 0
            
            remaining_needed = mission.requested_assets - mission.approved_assets
            
            store.update(mission, current_stage_detail=f"Round {round_num} complete: {round_approved} approved. Total: {mission.approved_assets}/{mission.requested_assets}")
            
            # Check if target met
            if mission.is_target_met:
                break
        
        # --- FINAL ---
        if mission.is_target_met:
            final_status = "COMPLETE"
        elif mission.approved_assets > 0:
            final_status = "PARTIAL"
        else:
            final_status = "FAILED"
        
        # Build before exposing a terminal mission. The Library action can then
        # deterministically query this mission's freshly indexed assets.
        try:
            from ada_app.asset_library import AssetLibrary
            AssetLibrary().build_index()
        except: pass
        store.update(mission, status=final_status, completed_at=datetime.now().isoformat(),
                    current_stage_detail=f"Mission {final_status}: {mission.approved_assets}/{mission.requested_assets} approved")
        
    except Exception as e:
        traceback.print_exc()
        store.update(mission, status="FAILED", error_message=str(e),
                    completed_at=datetime.now().isoformat())

def start_mission_background(mission_id: str):
    t = threading.Thread(target=run_mission, args=(mission_id,), name=f"mission-{mission_id}")
    t.daemon = True
    t.start()
