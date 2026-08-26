import sys, os, time, uuid
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ada_app.mission import ProductionMission, MissionStore
from ada_app.mission_runner import run_mission
from ada_app.asset_library import AssetLibrary

def run_gate1():
    print("=== STARTING GATE 1: Lustify Direct ===")
    store = MissionStore()
    # Create a unique Golden ID as requested
    golden_id = f"ada_alpha_golden_1_0_{uuid.uuid4().hex[:8]}"
    print(f"Golden ID: {golden_id}")
    
    mission = ProductionMission(
        mission_id=f"{golden_id}_gate1",
        character="2B",
        requested_assets=1,
        what_happens="Walking in a futuristic city",
        creation_mode="scene",
        renderer_choice="lustify"
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
