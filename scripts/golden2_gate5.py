import sys, os
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ada_app.asset_library import AssetLibrary
from scripts.hard_re_evaluator import evaluate_image
import json

def run_gate5():
    print("=== STARTING NEW GOLDEN GATE 5: Hard Re-Evaluate ===")
    
    golden_id = "ada_alpha_golden_1_0_6853abe7"
    gate4_mission_id = f"{golden_id}_gate4"
    
    lib = AssetLibrary()
    assets = lib.get_assets(mission_id=gate4_mission_id)
    if not assets:
        print("GATE 5 FAILED! Could not find source asset from Gate 4.")
        sys.exit(1)
        
    image_path = Path(assets[0]["full_image_path"])
    print(f"Target Image: {image_path}")
    
    if not image_path.is_file():
        print("GATE 5 FAILED! Physical image does not exist.")
        sys.exit(1)
        
    print("Executing Hard Re-Evaluate...")
    try:
        review_data = evaluate_image(image_path)
    except Exception as e:
        print(f"GATE 5 FAILED! Error during evaluation: {e}")
        sys.exit(1)
        
    print("Hard Re-Evaluate Output:")
    print(json.dumps(review_data, indent=2))
    
    score = review_data.get("final_score", 0)
    if score < 80:
        print(f"GATE 5 FAILED! Hard evaluator returned low score: {score}")
        sys.exit(1)
        
    print("GATE 5 PASS")

if __name__ == "__main__":
    run_gate5()
