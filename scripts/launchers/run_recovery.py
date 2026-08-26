import sys
import json
from pathlib import Path
from ada_app.pilot_runner import run_pilot_pipeline
from ada_app.mission import MissionStore
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]

mission_id = "mission_20260823_190018_437422"
store = MissionStore()
mission = store.load(mission_id)

run_dir = ROOT / "data" / "runs" / "missions" / "m2_2b_20260823_190609"
candidates = json.loads((run_dir / "pilot_candidates.json").read_text(encoding="utf-8"))

print(f"Resuming run_pilot_pipeline for {run_dir.name} ...")
# remaining needed
target_approvals = mission.requested_assets - mission.approved_assets
run_pilot_pipeline(run_dir, candidates, target_approvals=target_approvals)

# Tally results to update mission progress
final_candidates = json.loads((run_dir / "pilot_candidates.json").read_text(encoding="utf-8"))
round_approved = sum(1 for c in final_candidates if c.get("pipeline_state") == "APPROVED")
print(f"Newly approved assets: {round_approved}")

mission.approved_assets += round_approved
if mission.approved_assets >= mission.requested_assets:
    store.update(mission, status="COMPLETE", completed_at=datetime.now().isoformat())
else:
    store.update(mission, status="PRODUCING")
    
print(f"Mission updated: status={mission.status}, approved={mission.approved_assets}")
