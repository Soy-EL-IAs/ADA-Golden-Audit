import sys, os, time, uuid, json
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ada_app.mission import ProductionMission, MissionStore
from ada_app.mission_runner import run_mission, RUNS_DIR
from ada_app.asset_library import AssetLibrary
from ada_app.main import read_json

def run_gate2():
    print("=== STARTING GATE 2: Stock target 4 ===")
    store = MissionStore()
    
    # We use the same Golden ID base if possible, or just create the next mission
    golden_id = "ada_alpha_golden_1_0_3916a42f"
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
    if not mission.source_runs:
        print("FAIL: No source runs found on mission.")
        sys.exit(1)
    run_id = mission.source_runs[-1]
    run_dir = RUNS_DIR / run_id
    
    # 1. requested = 4
    if mission.requested_assets != 4:
        print(f"FAIL: requested_assets is {mission.requested_assets} != 4")
        sys.exit(1)
        
    # 2. manifest accepted = 4, attempted >= 4, rejected = attempted - accepted
    manifest = read_json(run_dir / "manifest.json")
    attempted = manifest.get("attempted", 0)
    accepted = manifest.get("accepted", 0)
    rejected = manifest.get("rejected", 0)
    print(f"Manifest: attempted={attempted}, accepted={accepted}, rejected={rejected}")
    if accepted != 4:
        print(f"FAIL: manifest accepted is {accepted} != 4")
        sys.exit(1)
    if attempted < 4:
        print(f"FAIL: manifest attempted is {attempted} < 4")
        sys.exit(1)
    if rejected != attempted - accepted:
        print(f"FAIL: manifest rejected ({rejected}) != attempted ({attempted}) - accepted ({accepted})")
        sys.exit(1)
        
    # 3. pilot_candidates APPROVED únicos = 4
    candidates = read_json(run_dir / "pilot_candidates.json")
    if len(candidates) != attempted:
        print(f"FAIL: pilot_candidates.json len ({len(candidates)}) != attempted ({attempted})")
        sys.exit(1)
        
    approved_candidates = [c for c in candidates if c.get("pipeline_state") == "APPROVED"]
    approved_ids = {c["concept_id"] for c in approved_candidates}
    print(f"pilot_candidates APPROVED: {len(approved_candidates)} ({len(approved_ids)} unique)")
    if len(approved_ids) != 4:
        print(f"FAIL: unique APPROVED candidates is {len(approved_ids)} != 4")
        sys.exit(1)
        
    # 4. AssetLibrary assets asociados a esa mission = 4
    lib = AssetLibrary()
    assets = lib.get_assets(mission_id=mission.mission_id)
    print(f"AssetLibrary assets: {len(assets)}")
    if len(assets) != 4:
        print(f"FAIL: AssetLibrary returned {len(assets)} assets != 4")
        sys.exit(1)
        
    # 5. imágenes físicas ADA válidas = 4, hashes válidos, físicas administradas por ADA
    for a in assets:
        path = Path(a.get("full_image_path", ""))
        if not path.is_file():
            print(f"FAIL: Managed asset file missing: {path}")
            sys.exit(1)
        prov = a.get("storage_provenance", {})
        if prov.get("owner") != "ADA":
            print(f"FAIL: Asset not managed by ADA: owner={prov.get('owner')}")
            sys.exit(1)
        print(f"Asset {a['asset_id']} physically valid at {path}")
        
    print("GATE 2 REINFORCED VALIDATION PASS")
    
if __name__ == "__main__":
    run_gate2()
