import sys, os
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ada_app.mission import ProductionMission, MissionStore
from ada_app.mission_runner import run_mission
from ada_app.asset_library import AssetLibrary

def run_gate1():
    print("=== STARTING NEW GOLDEN GATE 1: Lustify Direct ===")
    store = MissionStore()
    
    golden_id = "ada_alpha_golden_1_0_6853abe7"
    mission_id = f"{golden_id}_gate1"
    
    mission = store.load(mission_id)
    if mission and mission.status in ["COMPLETED", "COMPLETE", "FINAL"]:
        print(f"Mission {mission_id} already complete. Skipping run.")
    else:
        mission = ProductionMission(
            mission_id=mission_id,
            character="2B",
            requested_assets=1,
            creation_mode="scene",
            renderer_choice="lustify",
            what_happens="Standing in a futuristic city"
        )
        store.save(mission)
        print(f"Mission created: {mission.mission_id}")
        run_mission(mission.mission_id)
        mission = store.load(mission.mission_id)
        print(f"Gate 1 finished with status: {mission.status}")
    
    if mission.status not in ["COMPLETED", "COMPLETE", "FINAL"]:
        print(f"GATE 1 FAILED! Status={mission.status}, Error={getattr(mission, 'error_message', '')}")
        sys.exit(1)
        
    lib = AssetLibrary()
    assets = lib.get_assets(mission_id=mission.mission_id)
    print(f"Assets found in library for Gate 1: {len(assets)}")
    
    if len(assets) == 0:
        print("GATE 1 FAILED! No assets found in library.")
        sys.exit(1)
        
    print("GATE 1 PASS")
    return mission.mission_id, golden_id

if __name__ == "__main__":
    run_gate1()
