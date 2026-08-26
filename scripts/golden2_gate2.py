import sys, os
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ada_app.mission import ProductionMission, MissionStore
from ada_app.mission_runner import run_mission
from ada_app.asset_library import AssetLibrary
import json

def run_gate2():
    print("=== STARTING NEW GOLDEN GATE 2: Stock target 4 ===")
    store = MissionStore()
    
    golden_id = "ada_alpha_golden_1_0_6853abe7"
    mission_id = f"{golden_id}_gate2"
    
    mission = store.load(mission_id)
    if mission and mission.status in ["COMPLETED", "COMPLETE", "FINAL"]:
        print(f"Mission {mission_id} already complete. Skipping run.")
    else:
        mission = ProductionMission(
            mission_id=mission_id,
            character="2B",
            requested_assets=4,
            creation_mode="stock",
            renderer_choice="lustify"
        )
        store.save(mission)
        print(f"Mission created: {mission.mission_id}")
        run_mission(mission.mission_id)
        mission = store.load(mission.mission_id)
        print(f"Gate 2 finished with status: {mission.status}")
    
    if mission.status not in ["COMPLETED", "COMPLETE", "FINAL"]:
        print(f"GATE 2 FAILED! Status={mission.status}, Error={getattr(mission, 'error_message', '')}")
        sys.exit(1)
        
    print("=== STARTING REINFORCED VALIDATION ===")
    run_dir = Path("d:/IA/Ada/data/runs/missions") / mission.source_runs[-1]
    
    manifest_path = run_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    print(f"Manifest: attempted={manifest['attempted']}, accepted={manifest['accepted']}, rejected={manifest['rejected']}")
    
    candidates_path = run_dir / "pilot_candidates.json"
    candidates = json.loads(candidates_path.read_text(encoding="utf-8"))
    approved_cands = [c for c in candidates if c.get("pipeline_state") == "APPROVED"]
    unique_ids = set(c["concept_id"] for c in approved_cands)
    print(f"pilot_candidates APPROVED: {len(approved_cands)} ({len(unique_ids)} unique)")
    
    lib = AssetLibrary()
    assets = lib.get_assets(mission_id=mission.mission_id)
    print(f"AssetLibrary assets: {len(assets)}")
    
    if manifest['accepted'] != 4:
        print("GATE 2 FAILED! manifest accepted != 4")
        sys.exit(1)
        
    if len(approved_cands) != 4 or len(unique_ids) != 4:
        print("GATE 2 FAILED! candidates APPROVED != 4")
        sys.exit(1)
        
    if len(assets) != 4:
        print("GATE 2 FAILED! AssetLibrary returned != 4 assets")
        sys.exit(1)
        
    for a in assets:
        p = Path(a.get("full_image_path", ""))
        if not p.is_file():
            print(f"GATE 2 FAILED! Missing physical image for {a.get('asset_id')}: {p}")
            sys.exit(1)
        print(f"Asset {a['asset_id']} physically valid at {p}")
        
    print("GATE 2 REINFORCED VALIDATION PASS")

if __name__ == "__main__":
    run_gate2()
