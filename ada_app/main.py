from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, FileResponse
import json
import os
import subprocess
import asyncio
import httpx
from pathlib import Path
from datetime import datetime
from ada_app.run_index import RunIndex
from ada_app.asset_library import AssetLibrary
from ada_app.character_onboarding import (
    CharacterBootstrapError,
    bootstrap_character,
    registered_character_name,
)
from ada_app.model_lab import registry_view, run_model_test
from ada_app.model_benchmark import (
    benchmark_results,
    ensure_direct_generator_benchmark,
    ensure_official_benchmark,
    execute_test,
    save_human_evaluation,
)
from scripts.model_scanner import scan_models
from scripts.ada_paths import ADA_ROOT, CHARACTERS_ROOT, LOCKS_ROOT, MISSION_RUNS_ROOT

app = FastAPI(title="ADA")

# Paths
APP_DIR = ADA_ROOT / "ada_app"
app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")
templates = Jinja2Templates(directory=APP_DIR / "templates")

M2_CONFIG_PATH = ADA_ROOT / "experimental" / "m1_creative_expansion_lab" / "m2_config.json"
ADA_LOCAL_CONFIG_PATH = ADA_ROOT / "config" / "ada.local.json"
ROADMAP_PATH = ADA_ROOT / "config" / "roadmap.json"
CHARACTERS_PATH = CHARACTERS_ROOT / "catalog.json"
RUNS_DIR = MISSION_RUNS_ROOT

def read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def write_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ==================== CORE ====================

@app.get("/api/image")
async def get_image(path: str):
    p = Path(path)
    if not p.is_file():
        return JSONResponse(status_code=404, content={"error": "Not found"})
    return FileResponse(str(p))

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ==================== MODEL LAB ====================

@app.get("/api/model-lab")
async def get_model_lab():
    return registry_view()


@app.post("/api/model-lab/scan")
async def scan_model_lab():
    scan_models()
    return registry_view()


@app.post("/api/model-lab/run")
async def run_model_lab_test(request: Request):
    data = await request.json()
    try:
        receipt = await asyncio.to_thread(
            run_model_test,
            model_id=str(data.get("model_id", "")),
            source_image=str(data.get("source_image", "")),
            character=str(data.get("character", "Shihouin Yoruichi")),
            prompt=data.get("prompt"),
            seed=int(data.get("seed", 20260824)),
        )
    except (TypeError, ValueError) as exc:
        return JSONResponse(status_code=400, content={"error": str(exc)})
    return receipt


@app.get("/api/model-lab/benchmarks")
async def get_model_lab_benchmarks():
    return benchmark_results()


@app.post("/api/model-lab/benchmarks/initialize")
async def initialize_model_lab_benchmark():
    manifest = ensure_official_benchmark()
    return {"status": "success", "manifest": manifest, "benchmarks": benchmark_results()}


@app.post("/api/model-lab/benchmarks/initialize-direct")
async def initialize_direct_generator_benchmark():
    manifest = ensure_direct_generator_benchmark()
    return {"status": "success", "manifest": manifest, "benchmarks": benchmark_results()}


@app.post("/api/model-lab/benchmarks/{benchmark_id}/tests/{test_id}/run")
async def run_model_lab_benchmark(benchmark_id: str, test_id: str, request: Request):
    data = await request.json()
    try:
        receipt = await asyncio.to_thread(
            execute_test,
            benchmark_id,
            test_id,
            str(data.get("model_id", "")),
            str(data.get("recipe_id", "")) or None,
        )
    except ValueError as exc:
        return JSONResponse(status_code=400, content={"error": str(exc)})
    return receipt


@app.post("/api/model-lab/benchmarks/{benchmark_id}/tests/{test_id}/evaluate")
async def evaluate_model_lab_benchmark(benchmark_id: str, test_id: str, request: Request):
    data = await request.json()
    try:
        evaluation = save_human_evaluation(
            benchmark_id=benchmark_id,
            test_id=test_id,
            run_id=str(data.get("run_id", "")),
            scores=data.get("scores", {}),
            notes=str(data.get("notes", "")),
        )
    except ValueError as exc:
        return JSONResponse(status_code=400, content={"error": str(exc)})
    return {"status": "success", "evaluation": evaluation, "benchmarks": benchmark_results()}

@app.get("/api/system")
async def get_system_status():
    local_cfg = read_json(ADA_LOCAL_CONFIG_PATH)
    lm_url = local_cfg.get("lmstudio_base_url", "http://127.0.0.1:1234")
    comfy_url = local_cfg.get("comfyui_base_url", "http://127.0.0.1:8188")
    
    lm_status = "Offline"
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.get(f"{lm_url}/api/v1/models")
            if resp.status_code == 200:
                lm_status = "Online"
    except Exception:
        pass
        
    comfy_status = "Offline"
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.get(f"{comfy_url}/system_stats")
            if resp.status_code == 200:
                comfy_status = "Online"
    except Exception:
        pass

    m2_cfg = read_json(M2_CONFIG_PATH)
    creative_model = m2_cfg.get("creative_expansion_model", "Unknown")
    strong_model = m2_cfg.get("strong_evaluation_model", "Unknown")

    return {
        "lm_studio": lm_status,
        "comfyui": comfy_status,
        "creative_model": creative_model,
        "strong_model": strong_model,
        "overall": "Ready" if lm_status == "Online" else "Degraded"
    }

# ==================== MISSIONS ====================

@app.post("/api/missions/create")
async def create_mission(request: Request):
    data = await request.json()
    creation_mode = data.get("creation_mode", "scene")
    if creation_mode not in {"scene", "stock"}:
        return JSONResponse(status_code=400, content={"error": "invalid_creation_mode", "message": "Choose Scene or Stock."})
    if creation_mode == "scene":
        from ada_app.semantic_contracts import implies_additional_subject
        if implies_additional_subject(data.get("what_happens", "")):
            return JSONResponse(status_code=400, content={"error": "single_subject_action_conflict", "message": "Scene currently supports one main character. Describe an action that does not require another person."})
    requested_character = data.get("character")
    if not isinstance(requested_character, str) or not requested_character.strip():
        return JSONResponse(
            status_code=400,
            content={
                "error": "character_required",
                "message": "Select a registered character before creating a mission.",
            },
        )
    requested_character = requested_character.strip()
    character = registered_character_name(requested_character, CHARACTERS_PATH)
    if character is None:
        return JSONResponse(
            status_code=409,
            content={
                "error": "character_not_registered",
                "character": requested_character,
                "message": "Add the character before creating a mission.",
            },
        )

    from ada_app.mission import ProductionMission, MissionStore
    from ada_app.mission_runner import start_mission_background

    requested_assets = data.get("requested_assets", 6 if creation_mode == "scene" else 1)
    if isinstance(requested_assets, bool) or not isinstance(requested_assets, int) or not 1 <= requested_assets <= 20:
        return JSONResponse(status_code=400, content={"error": "invalid_image_count", "message": "Number of images must be between 1 and 20."})
    character_entry = read_json(CHARACTERS_PATH).get(character, {})
    renderer_routing = {}
    outfit_override = None
    if creation_mode == "stock":
        if "outfit_override" in data:
            raw_outfit = data.get("outfit_override")
            if not isinstance(raw_outfit, str) or not raw_outfit.strip():
                return JSONResponse(status_code=400, content={"error": "outfit_required", "message": "Enter an outfit or disable Custom outfit."})
            outfit_override = raw_outfit.strip()
        from ada_app.character_capabilities import resolve_stock_renderer
        try:
            renderer_routing = resolve_stock_renderer(character_entry)
        except ValueError as exc:
            return JSONResponse(status_code=409, content={"error": "stock_renderer_unavailable", "character": character, "message": str(exc)})
        renderer_choice = renderer_routing["renderer"]
    else:
        renderer_choice = data.get("renderer_choice")
        if renderer_choice is None:
            renderer_choice = "miaomiao" if bool(data.get("generate_miaomiao_alternative", False)) else "lustify"
    if renderer_choice not in {"lustify", "miaomiao"}:
        return JSONResponse(status_code=400, content={"error": "invalid_renderer", "message": "Choose Lustify or Miaomiao."})
    from ada_app.character_capabilities import character_capability_status, renderer_request_allowed
    allowed, blocked_reason = renderer_request_allowed(character_entry, renderer_choice)
    if not allowed:
        return JSONResponse(status_code=409, content={"error": "character_renderer_unavailable", "character": character, "renderer": renderer_choice, "message": blocked_reason})
    character_route = character_capability_status(character_entry)

    mission = ProductionMission(
        character=character,
        requested_assets=requested_assets,
        what_happens=data.get("what_happens", "") if creation_mode == "scene" else "",
        where=data.get("where", "") if creation_mode == "scene" else "",
        concept_multiplier=data.get("concept_multiplier", 3) if creation_mode == "scene" else 1,
        production_buffer=data.get("production_buffer", 2) if creation_mode == "scene" else 1,
        max_rounds=data.get("max_rounds", 2) if creation_mode == "scene" else 1,
        generate_miaomiao_alternative=False,
        renderer_choice=renderer_choice,
        render_intent=("anime" if renderer_choice == "miaomiao" else "semi_realistic") if creation_mode == "stock" else data.get("render_intent", "semi_realistic"),
        source_asset_id=data.get("source_asset_id", "") if creation_mode == "scene" and isinstance(data.get("source_asset_id", ""), str) else "",
        source_generation_id=data.get("source_generation_id", "") if creation_mode == "scene" and isinstance(data.get("source_generation_id", ""), str) else "",
        generation_mode=data.get("generation_mode", "direct") if creation_mode == "scene" and data.get("generation_mode") in {"direct", "alternative"} else "direct",
        alternative_mode=data.get("alternative_mode", "") if creation_mode == "scene" and data.get("alternative_mode") in {"same_idea", "change_action", "change_setting", "change_look", "custom"} else "",
        alternative_instruction=data.get("alternative_instruction", "") if creation_mode == "scene" and isinstance(data.get("alternative_instruction"), str) else "",
        source_context=data.get("source_context", {}) if creation_mode == "scene" and isinstance(data.get("source_context"), dict) else {},
        creation_mode=creation_mode,
        outfit_override=outfit_override,
        renderer_routing=renderer_routing,
    )
    
    store = MissionStore()
    store.save(mission)
    
    start_mission_background(mission.mission_id)
    
    return {"mission_id": mission.mission_id, "status": "created", "character_route": character_route}

@app.get("/api/missions")
async def list_missions():
    from ada_app.mission import MissionStore
    store = MissionStore()
    return [m.to_dict() for m in store.list_all()]

@app.get("/api/missions/{mission_id}")
async def get_mission(mission_id: str):
    from ada_app.mission import MissionStore
    store = MissionStore()
    m = store.load(mission_id)
    if not m:
        return JSONResponse(status_code=404, content={"error": "Mission not found"})
    return m.to_dict()


@app.get("/api/missions/{mission_id}/funnel")
async def get_mission_funnel(mission_id: str):
    """Expose the persisted M2 → selection → production trace for one mission."""
    from ada_app.mission import MissionStore
    mission = MissionStore().load(mission_id)
    if not mission:
        return JSONResponse(status_code=404, content={"error": "Mission not found"})
    assets_by_concept = {
        asset.get("concept_id"): asset.get("asset_id")
        for asset in AssetLibrary().get_assets(mission_id=mission_id)
    }
    concepts = []
    for run_id in mission.source_runs:
        run_dir = RUNS_DIR / run_id
        records = read_json(run_dir / "proposal_records.json").get("records", [])
        m3 = read_json(run_dir / "m3_analysis.json").get("concepts", {})
        candidates = {item.get("concept_id"): item for item in read_json(run_dir / "pilot_candidates.json")}
        for record in records:
            concept_id = record.get("concept_id", "")
            candidate = candidates.get(concept_id)
            analysis = m3.get(concept_id, {})
            concepts.append({
                "run_id": run_id,
                "concept_id": concept_id,
                "snapshot": record.get("hook") or record.get("proposal", {}).get("snapshot", ""),
                "semantic_status": record.get("status", "UNKNOWN"),
                "m3": analysis,
                "selected": candidate is not None,
                "selection_rank": candidate.get("selection_rank") if candidate else None,
                "pipeline_state": candidate.get("pipeline_state", "NOT_SELECTED") if candidate else "NOT_SELECTED",
                "machine_review": candidate.get("final_review", {}) if candidate else {},
                "asset_id": assets_by_concept.get(concept_id),
            })
    return {"mission_id": mission_id, "concepts": concepts}

@app.post("/api/missions/{mission_id}/cancel")
async def cancel_mission(mission_id: str):
    from ada_app.mission import MissionStore
    store = MissionStore()
    m = store.load(mission_id)
    if not m:
        return JSONResponse(status_code=404, content={"error": "Mission not found"})
    store.update(m, cancelled=True, current_stage_detail="Cancelling after current stage...")
    return {"status": "cancel_requested"}

@app.post("/api/missions/{mission_id}/resume")
async def resume_mission(mission_id: str):
    from ada_app.mission import MissionStore
    from ada_app.mission_runner import start_mission_background
    
    store = MissionStore()
    m = store.load(mission_id)
    if not m:
        return JSONResponse(status_code=404, content={"error": "Mission not found"})
    
    if m.status not in ("PARTIAL", "FAILED"):
        return {"status": "not_resumable", "reason": f"Mission is {m.status}"}
    
    store.update(m, cancelled=False, status="RECOVERING", error_message="",
                current_stage_detail="Resuming mission...")
    start_mission_background(m.mission_id)
    return {"status": "resumed"}


@app.delete("/api/missions/{mission_id}")
async def delete_mission(mission_id: str):
    from ada_app.mission import MissionStore

    store = MissionStore()
    try:
        mission = store.delete(mission_id)
    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"error": "mission_not_found"})
    except ValueError:
        current = store.load(mission_id)
        return JSONResponse(
            status_code=409,
            content={
                "error": "mission_not_deletable",
                "status": current.status if current else None,
                "message": "Only FAILED, COMPLETE or CANCELLED missions can be deleted.",
            },
        )
    return {"status": "deleted", "mission_id": mission.mission_id}

# ==================== COMMAND BAR ====================

@app.post("/api/command")
async def process_command(request: Request):
    from ada_app.command_parser import parse_command
    data = await request.json()
    text = data.get("text", "")
    return parse_command(text)

# ==================== LIBRARY ====================

@app.get("/api/library/assets")
async def get_library_assets(mission_id: str | None = None, visible_only: bool = False):
    lib = AssetLibrary()
    return lib.get_visible_assets(mission_id=mission_id) if visible_only else lib.get_assets(mission_id=mission_id)

@app.get("/api/library/search")
async def search_library(q: str = ""):
    lib = AssetLibrary()
    return lib.search(q)

@app.get("/api/library/collections")
async def get_collections():
    lib = AssetLibrary()
    return lib.get_collections()

@app.get("/api/library/source-policy")
async def get_library_source_policy():
    """Exposes promotion boundaries without scanning or importing experiments."""
    from ada_app.asset_library import LIBRARY_SOURCE_POLICY
    return LIBRARY_SOURCE_POLICY

@app.get("/api/characters/heroes")
async def get_character_heroes():
    from ada_app.character_capabilities import load_character_heroes
    return load_character_heroes()

@app.post("/api/characters/{name}/hero")
async def set_character_hero(name: str, request: Request):
    data = await request.json()
    asset_id = data.get("asset_id")
    if not asset_id:
        raise HTTPException(status_code=400, detail="Missing asset_id")
    asset = next((item for item in AssetLibrary().get_assets() if item.get("asset_id") == asset_id), None)
    if asset is None:
        raise HTTPException(status_code=404, detail="Library image not found")
    if asset.get("character") != name:
        raise HTTPException(status_code=409, detail="Hero image belongs to a different character")
    if asset.get("is_visible_library_asset") is not True:
        raise HTTPException(status_code=409, detail="Hero image must be visible in Library")
    from ada_app.character_capabilities import save_character_hero
    save_character_hero(name, asset_id)
    return {"status": "success", "hero_asset_id": asset_id}

@app.post("/api/library/build_index")
async def rebuild_library_index():
    lib = AssetLibrary()
    lib.build_index()
    return {"status": "success"}

@app.post("/api/library/review/{asset_id}")
async def review_asset(asset_id: str, request: Request):
    data = await request.json()
    lib = AssetLibrary()
    try:
        review = lib.save_review(
            asset_id,
            human_status=data.get("human_status"),
            rating=data.get("human_rating", data.get("rating")),
            favorite=data.get("favorite"),
            stage=data.get("stage"),
            preference=data.get("preference"),
        )
    except ValueError as exc:
        return JSONResponse(status_code=400, content={"error": str(exc)})
    asset = next((item for item in lib.get_assets() if item.get("asset_id") == asset_id), None)
    return {"status": "success", "review": review, "asset": asset}


@app.post("/api/library/remove-selected")
async def remove_selected_library_images(request: Request):
    """Hide explicitly selected Library images while preserving files and lineage."""
    data = await request.json()
    asset_ids = data.get("asset_ids")
    if not isinstance(asset_ids, list):
        return JSONResponse(status_code=400, content={"error": "asset_ids_must_be_a_list"})
    try:
        removed = AssetLibrary().set_library_status(asset_ids, "REJECTED")
    except ValueError as exc:
        return JSONResponse(status_code=400, content={"error": str(exc)})
    return {"status": "success", "removed_asset_ids": removed, "files_deleted": False}


@app.post("/api/library/hard-reevaluate")
async def hard_reevaluate_library_images(request: Request):
    """Run Hard Re-Evaluator on selected Library images."""
    data = await request.json()
    asset_ids = data.get("asset_ids")
    if not isinstance(asset_ids, list):
        return JSONResponse(status_code=400, content={"error": "asset_ids_must_be_a_list"})
    
    lib = AssetLibrary()
    assets = [item for item in lib.get_assets() if item.get("asset_id") in asset_ids]
    if not assets:
        return JSONResponse(status_code=400, content={"error": "no_valid_assets_found"})

    from scripts.hard_re_evaluator import evaluate_image
    import filelock
    from scripts.ada_paths import ADA_ROOT
    
    LOCKS_ROOT.mkdir(parents=True, exist_ok=True)
    lock = filelock.FileLock(str(LOCKS_ROOT / "gpu_execution.lock"))
    
    results = {}
    for asset in assets:
        path = asset.get("full_image_path")
        if not path:
            continue
        try:
            with lock.acquire(timeout=600):
                hard_data = evaluate_image(Path(path))
            
            # Calculate original score out of 100
            orig = 0
            if asset.get("human_review", {}).get("rating"):
                orig = int(asset["human_review"]["rating"] * 10)
            elif asset.get("agent_rating"):
                orig = int(asset["agent_rating"] * 10)
                
            hard_data["original_score"] = orig
            hard_data["delta"] = hard_data.get("final_score", 0) - orig
            
            lib.save_hard_rating(asset["asset_id"], hard_data)
            results[asset["asset_id"]] = hard_data
        except Exception as e:
            print(f"Error evaluating {asset['asset_id']}: {e}")
            import traceback
            error_data = {"evaluation_failed": True, "error": str(e), "traceback": traceback.format_exc()}
            lib.save_hard_rating(asset["asset_id"], error_data, failed=True)
            results[asset["asset_id"]] = error_data
            continue

    return {"status": "success", "evaluated_count": len(results), "results": results}

@app.post("/api/library/reinterpret/{asset_id}")
async def reinterpret_asset(asset_id: str, request: Request):
    """Create one explicit semantic request and queue its renderer execution."""
    data = await request.json()
    target = data.get("target_character")
    if not isinstance(target, str) or not target.strip():
        return JSONResponse(status_code=400, content={"error":"target_character_required"})
    character = registered_character_name(target.strip(), CHARACTERS_PATH)
    if character is None:
        return JSONResponse(status_code=409, content={"error":"character_not_registered", "character":target})
    asset = next((item for item in AssetLibrary().get_assets() if item.get("asset_id") == asset_id), None)
    if asset is None:
        return JSONResponse(status_code=404, content={"error":"asset_not_found"})
    registry = read_json(CHARACTERS_PATH)
    try:
        from ada_app.reinterpretation import create_reinterpretation, start_reinterpretation
        record = create_reinterpretation(asset, character, registry[character], renderer=data.get("renderer", "lustify"), render_intent=data.get("render_intent", "semi_realistic"), template_mode=data.get("template_mode", "balanced"))
        record = start_reinterpretation(record["request_id"])
    except ValueError as exc:
        return JSONResponse(status_code=400, content={"error":str(exc)})
    return {"status":"queued", "request":record}


@app.get("/api/library/reinterpretation/{request_id}")
async def reinterpretation_status(request_id: str):
    try:
        from ada_app.reinterpretation import get_reinterpretation
        return get_reinterpretation(request_id)
    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"error":"reinterpretation_not_found"})
    except ValueError as exc:
        return JSONResponse(status_code=400, content={"error":str(exc)})

# ==================== CHARACTERS ====================

@app.get("/api/characters")
async def get_characters():
    return read_json(CHARACTERS_PATH)


@app.get("/api/characters/catalog")
async def get_character_catalog():
    from ada_app.character_capabilities import build_character_catalog
    heroes = await get_character_heroes()
    return build_character_catalog(read_json(CHARACTERS_PATH), AssetLibrary().get_assets(), heroes)


@app.post("/api/characters/bootstrap")
async def add_character(request: Request):
    data = await request.json()
    try:
        return await asyncio.to_thread(
            bootstrap_character,
            data.get("character", ""),
            data.get("version"),
            CHARACTERS_PATH,
        )
    except CharacterBootstrapError as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.code, "message": str(exc)},
        )


@app.post("/api/characters/revalidate")
async def revalidate_character(request: Request):
    data = await request.json()
    try:
        from ada_app.character_onboarding import CharacterBootstrapService
        return await asyncio.to_thread(
            CharacterBootstrapService().revalidate,
            data.get("character", ""),
            data.get("version"),
        )
    except CharacterBootstrapError as exc:
        return JSONResponse(status_code=exc.status_code, content={"error": exc.code, "message": str(exc)})

# ==================== RUNS (ADVANCED) ====================

@app.get("/api/runs")
async def get_runs():
    idx = RunIndex()
    return [r.to_dict() for r in idx.get_all_runs()]

@app.get("/api/runs/last")
async def get_last_run():
    runs = await get_runs()
    if runs:
        return await get_run_details(runs[0]["run_id"])
    return None

@app.get("/api/runs/{run_id}/m3_analysis")
async def get_m3_analysis(run_id: str):
    run_path = RUNS_DIR / run_id
    if not run_path.exists():
        return JSONResponse(status_code=404, content={"error": "Run not found"})
    
    m3_file = run_path / "m3_analysis.json"
    if m3_file.exists():
        return read_json(m3_file)
        
    records = read_json(run_path / "proposal_records.json")
    if not records or "records" not in records:
        return JSONResponse(status_code=404, content={"error": "No concepts found to analyze"})
    
    import sys
    sys.path.append(str(APP_DIR))
    try:
        from m3_filter import run_m3_analysis
    except ImportError:
        return JSONResponse(status_code=500, content={"error": "M3 filter not available"})
        
    analysis = run_m3_analysis(records["records"])
    write_json(m3_file, analysis)
    return analysis

@app.post("/api/pilot/resume/{run_id}")
async def resume_pilot(run_id: str):
    from ada_app.pilot_runner import start_pilot_background
    if Path(run_id).name != run_id:
        return {"error": "Invalid run id"}
    run_dir = RUNS_DIR / run_id
    if not run_dir.is_dir(): return {"error": "Run not found"}
    
    candidates_file = run_dir / "pilot_candidates.json"
    if candidates_file.exists():
        cands = read_json(candidates_file)
        resumed = False
        for c in cands:
            if c.get("pipeline_state") == "FAILED_RUNTIME" or c.get("pipeline_state", "").startswith("RETRYING_RUNTIME"):
                c["pipeline_state"] = "PENDING"
                c["runtime_retries"] = 0
                resumed = True
        if resumed:
            write_json(candidates_file, cands)
            start_pilot_background(run_dir, cands)
            return {"status": "Resumed"}
    return {"status": "No candidates needed resume"}

@app.post("/api/pilot/generate")
async def generate_pilot(request: Request):
    data = await request.json()
    from ada_app.m3_filter import run_m3_analysis
    from ada_app.m4_selection import select_top_candidates
    from ada_app.pilot_runner import start_pilot_background
    import subprocess
    import time
    
    script_path = ADA_ROOT / "experimental" / "m1_creative_expansion_lab" / "run_m2.py"
    config_path = ADA_ROOT / "experimental" / "m1_creative_expansion_lab" / "m2_config.json"
    
    config = read_json(config_path)
    config["requested_count"] = data.get("conceptCount", 12)
    write_json(config_path, config)
    
    generated_run_id = f"m2_api_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    generated_run = RUNS_DIR / generated_run_id
    subprocess.run(
        ["python", str(script_path), "--run-id", generated_run_id],
        cwd=str(ADA_ROOT), check=True,
    )
    if not (generated_run / "manifest.json").is_file():
        return JSONResponse(status_code=500, content={"error": f"Explicit run did not complete: {generated_run_id}"})
    
    records = read_json(generated_run / "proposal_records.json")
    m3_analysis = run_m3_analysis(records.get("records", []))
    write_json(generated_run / "m3_analysis.json", m3_analysis)
    
    pilot_count = data.get("pilotCount", 3)
    candidates = select_top_candidates(records.get("records", []), m3_analysis, top_n=pilot_count)
    write_json(generated_run / "pilot_candidates.json", candidates)
    
    start_pilot_background(generated_run, candidates)
    
    return {"status": "started", "run_id": generated_run.name}

@app.get("/api/runs/{run_id}/pilot")
async def get_pilot_status(run_id: str):
    candidates_file = RUNS_DIR / run_id / "pilot_candidates.json"
    if candidates_file.exists():
        return read_json(candidates_file)
    return []

@app.get("/api/runs/{run_id}")
async def get_run_details(run_id: str):
    run_path = RUNS_DIR / run_id
    if not run_path.exists():
        return JSONResponse(status_code=404, content={"error": "Run not found"})
    
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
        "rejected_count": records.get("semantic_guard_rejected_count") if records else 0
    }

@app.post("/api/runs/{run_id}/concepts/{concept_id}/review")
async def review_concept(run_id: str, concept_id: str, request: Request):
    data = await request.json()
    decision = data.get("decision")
    run_path = RUNS_DIR / run_id
    if not run_path.exists():
        return JSONResponse(status_code=404, content={"error": "Run not found"})
    
    review_file = run_path / "human_review.json"
    reviews = read_json(review_file)
    
    reviews[concept_id] = {
        "decision": decision,
        "timestamp": datetime.now().isoformat()
    }
    
    write_json(review_file, reviews)
    return {"status": "success"}

@app.get("/api/roadmap")
async def get_roadmap():
    return read_json(ROADMAP_PATH)

@app.post("/api/creative_expansion")
async def start_creative_expansion(background_tasks: BackgroundTasks):
    script_path = ADA_ROOT / "experimental" / "m1_creative_expansion_lab" / "run_m2.py"
    
    def run_m2_script():
        subprocess.run(["python", str(script_path)], cwd=str(ADA_ROOT))
        
    background_tasks.add_task(run_m2_script)
    return {"status": "started"}
