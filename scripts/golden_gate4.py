import sys, os
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ada_app.mission import ProductionMission, MissionStore
from ada_app.mission_runner import run_mission
from ada_app.asset_library import AssetLibrary

def run_gate4(source_asset_id):
    print(f"=== STARTING GATE 4: Miaomiao -> Lustify Img2Img ===")
    print(f"Source Asset: {source_asset_id}")
    store = MissionStore()
    
    golden_id = "ada_alpha_golden_1_0_3916a42f"
    mission_id = f"{golden_id}_gate4"
    
    mission = store.load(mission_id)
    if mission and mission.status in ["COMPLETED", "COMPLETE", "FINAL"]:
        print(f"Mission {mission_id} already complete. Skipping run.")
    else:
        # Gate 4: Miaomiao source -> Lustify Img2Img
        mission = ProductionMission(
            mission_id=mission_id,
            character="2B",
            requested_assets=1,
            creation_mode="scene",
            renderer_choice="lustify",
            generation_mode="reinterpretation",
            source_asset_id=source_asset_id,
            alternative_mode="reinterpret_scene",
            what_happens="Standing in a futuristic city"
        )
        store.save(mission)
        print(f"Mission created: {mission.mission_id}")
        run_mission(mission.mission_id)
        mission = store.load(mission.mission_id)
        print(f"Gate 4 finished with status: {mission.status}")
    
    if mission.status not in ["COMPLETED", "COMPLETE", "FINAL"]:
        print(f"GATE 4 FAILED! Status={mission.status}, Error={getattr(mission, 'error_message', '')}")
        sys.exit(1)
        
    lib = AssetLibrary()
    assets = lib.get_assets(mission_id=mission.mission_id)
    print(f"Assets found in library for Gate 4: {len(assets)}")
    
    if len(assets) == 0:
        print("GATE 4 FAILED! No assets found in library.")
        sys.exit(1)
        
    print("GATE 4 PASS (Reinterpretation completed). Now need to check loss of identity.")
    return mission.mission_id, golden_id

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python golden_gate4.py <source_asset_id>")
        sys.exit(1)
    run_gate4(sys.argv[1])
