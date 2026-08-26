import os
import sys
import subprocess
import json
import hashlib
from pathlib import Path

def hash_file(path: Path):
    if not path.is_file(): return None
    hasher = hashlib.sha256()
    with open(path, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()

def get_library_state():
    root = Path(__file__).parent.parent / "data" / "library"
    index_path = root / "index.json"
    h = hash_file(index_path)
    count = 0
    if index_path.is_file():
        try:
            count = len(json.loads(index_path.read_text(encoding="utf-8")))
        except:
            count = -1
    
    asset_files = 0
    if (root / "assets").exists():
        asset_files = sum(1 for _ in (root / "assets").rglob("*.*") if _.is_file())
    
    return h, count, asset_files

def run():
    print("Capturing production library state...")
    hash1, count1, assets1 = get_library_state()
    print(f"Before: index hash={hash1}, count={count1}, assets={assets1}")
    
    print("Running test suite...")
    # Discover tests and run them
    result = subprocess.run(["python", "-m", "unittest", "discover", "tests"], cwd=str(Path(__file__).parent.parent))
    if result.returncode != 0:
        print("Test suite failed!")
        sys.exit(result.returncode)
        
    print("Capturing production library state after tests...")
    hash2, count2, assets2 = get_library_state()
    print(f"After: index hash={hash2}, count={count2}, assets={assets2}")
    
    if hash1 != hash2 or count1 != count2 or assets1 != assets2:
        print("ERROR: TEST SUITE MUTATED PRODUCTION DATA!")
        sys.exit(1)
        
    print("SUCCESS: Test suite isolation verified.")

if __name__ == "__main__":
    run()
