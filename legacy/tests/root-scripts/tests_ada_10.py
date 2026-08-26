import sys
from pathlib import Path
import json

ADA_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ADA_ROOT))

from ada_app.mission import ProductionMission, MissionStore
from ada_app.command_parser import parse_command
from ada_app.asset_library import AssetLibrary

def test_mission_lifecycle():
    print("Testing Mission Lifecycle...")
    store = MissionStore()
    
    # Create
    m = ProductionMission(character="2B", requested_assets=5)
    assert m.character == "2B"
    assert m.requested_assets == 5
    assert m.status == "CREATED"
    
    # Save/Load
    store.save(m)
    loaded = store.load(m.mission_id)
    assert loaded is not None
    assert loaded.character == "2B"
    assert loaded.status == "CREATED"
    
    # Update and State Check
    store.update(loaded, approved_assets=5)
    assert loaded.is_target_met == True
    assert loaded.progress == 1.0

def test_command_parser():
    print("Testing Command Parser...")
    
    # CREATE_IMAGES
    c1 = parse_command("create 6 images of 2B")
    assert c1["intent"] == "CREATE_IMAGES"
    assert c1["character"] == "2B"
    assert c1["count"] == 6

    c2 = parse_command("create images of 2B")
    assert c2["intent"] == "CREATE_IMAGES"
    assert c2["count"] == 6
    
    # OPEN_CHARACTER_LIBRARY
    c3 = parse_command("show 2B")
    assert c3["intent"] == "OPEN_CHARACTER_LIBRARY"
    assert c3["character"] == "2B"
    
    # OPEN_COLLECTION
    c4 = parse_command("show NieR")
    assert c4["intent"] == "OPEN_COLLECTION"
    assert c4["franchise"] == "NieR"

    # SHOW_ACTIVE_MISSIONS
    c5 = parse_command("missions")
    assert c5["intent"] == "SHOW_ACTIVE_MISSIONS"
    
    # UNKNOWN
    c6 = parse_command("asdfghjkl")
    assert c6["intent"] == "UNKNOWN"

def test_provenance():
    print("Testing Provenance...")
    pilot_runner_path = ADA_ROOT / "ada_app" / "pilot_runner.py"
    content = pilot_runner_path.read_text(encoding="utf-8")
    
    assert "shutil.rmtree(p)" not in content, "Provenance Violation: shutil.rmtree(p) found!"
    assert ".rename(archived)" in content, "Provenance Violation: rename missing for archives!"

if __name__ == "__main__":
    try:
        test_mission_lifecycle()
        test_command_parser()
        test_provenance()
        print("ALL TESTS PASSED")
    except AssertionError as e:
        print(f"TEST FAILED: {e}")
        sys.exit(1)
