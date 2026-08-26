import sys, os
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ada_app.mission import ProductionMission, MissionStore
from ada_app.mission_runner import run_mission
from ada_app.asset_library import AssetLibrary

def run_gate4():
    print("=== STARTING NEW GOLDEN GATE 4: Miaomiao -> Lustify Img2Img ===")
    store = MissionStore()
    
    golden_id = "ada_alpha_golden_1_0_6853abe7"
    gate3_mission_id = f"{golden_id}_gate3"
    mission_id = f"{golden_id}_gate4"
    
    lib = AssetLibrary()
    assets = lib.get_assets(mission_id=gate3_mission_id)
    if not assets:
        print("GATE 4 FAILED! Could not find source asset from Gate 3.")
        sys.exit(1)
        
    source_asset_id = assets[0]["asset_id"]
    print(f"Source Asset: {source_asset_id}")
    
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
            generation_mode="reinterpretation",
            source_asset_id=source_asset_id,
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
        
    print("GATE 4 PASS (Reinterpretation completed).")

if __name__ == "__main__":
    run_gate4()
