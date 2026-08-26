import sys, re
from pathlib import Path

with open('ada_app/main.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('from datetime import datetime', 'from datetime import datetime\nfrom ada_app.run_index import RunIndex\nfrom ada_app.asset_library import AssetLibrary')

run_idx_code = '''
@app.get("/api/runs")
async def get_runs():
    idx = RunIndex()
    return [r.to_dict() for r in idx.get_all_runs()]
'''
code = re.sub(r'@app\.get\("/api/runs"\).*?return runs', run_idx_code, code, flags=re.DOTALL)

last_run_code = '''
@app.get("/api/runs/last")
async def get_last_run():
    runs = await get_runs()
    if runs:
        return await get_run_details(runs[0]["run_id"])
    return None
'''
code = re.sub(r'@app\.get\("/api/runs/last"\).*?return None', last_run_code, code, flags=re.DOTALL)

library_code = '''
@app.get("/api/library/assets")
async def get_library_assets():
    lib = AssetLibrary()
    return lib.get_assets()

@app.post("/api/library/build_index")
async def rebuild_library_index():
    lib = AssetLibrary()
    lib.build_index()
    return {"status": "success"}

@app.post("/api/library/review/{asset_id}")
async def review_asset(asset_id: str, request: Request):
    data = await request.json()
    lib = AssetLibrary()
    lib.save_review(asset_id, data.get("status", "None"))
    return {"status": "success"}
'''
code = code + "\n" + library_code

run_detail_code = '''
@app.get("/api/runs/{run_id}")
async def get_run_details(run_id: str):
    idx = RunIndex()
    run_info = None
    for r in idx.get_all_runs():
        if r.run_id == run_id:
            run_info = r
            break
            
    if not run_info:
        return JSONResponse(status_code=404, content={"error": "Run not found"})
        
    run_path = Path(run_info.artifact_root)
    manifest = read_json(run_path / "manifest.json")
    records = read_json(run_path / "proposal_records.json")
    telemetry = read_json(run_path / "telemetry.json")
    human_review = read_json(run_path / "human_review.json")
    
    concepts = records.get("records", []) if records else []
    for c in concepts:
        cid = c.get("concept_id")
        if human_review and cid in human_review:
            c["human_decision"] = human_review[cid].get("decision")
            
    return {
        "id": run_id,
        "manifest": manifest,
        "telemetry": telemetry,
        "concepts": concepts,
        "valid_count": records.get("valid_count") if records else 0,
        "requested_count": records.get("requested_count") if records else 0,
        "rejected_count": records.get("semantic_guard_rejected_count") if records else 0,
        "artifact_root": run_info.artifact_root
    }
'''
code = re.sub(r'@app\.get\("/api/runs/{run_id}"\).*?rejected_count"\): records\.get\("semantic_guard_rejected_count"\) if records else 0\n    }', run_detail_code, code, flags=re.DOTALL)

with open('ada_app/main.py', 'w', encoding='utf-8') as f:
    f.write(code)
