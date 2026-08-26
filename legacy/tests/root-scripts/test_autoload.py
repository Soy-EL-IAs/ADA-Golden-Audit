import sys
from pathlib import Path
ADA_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ADA_ROOT / "scripts"))
from lmstudio_controller import LMStudioController
import time

def test_autoload():
    controller = LMStudioController()
    print("Unloading all models...")
    controller.unload_all()
    
    time.sleep(2)
    inv = controller.list_models()
    if inv["loaded"]:
        print("Failed to unload models!")
        sys.exit(1)
        
    print("Models unloaded. Now simulating mission_runner.py auto-load...")
    controller.activate_role("premise_agent")
    
    time.sleep(2)
    inv2 = controller.list_models()
    if not inv2["loaded"]:
        print("Failed to load model!")
        sys.exit(1)
        
    loaded_model = inv2["loaded"][0].get("model")
    print(f"Successfully loaded: {loaded_model}")
    assert "9b" in loaded_model.lower(), f"Expected 9B model, got {loaded_model}"
    print("Test passed.")
    
if __name__ == "__main__":
    test_autoload()

