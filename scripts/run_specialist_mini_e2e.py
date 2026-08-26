"""Real three-image specialist E2E. Stops on the first invalid boundary."""
from __future__ import annotations
import copy, json, time, uuid, urllib.request, urllib.error, mimetypes
from pathlib import Path
from typing import Any

from ada_paths import ADA_ROOT, COMFYUI_BASE_URL, COMFYUI_ROOT, CONFIG_ROOT, WORKFLOWS_ROOT
from ada_run_state import AdaRunState
from character_profile import CharacterProfileDatabase
from lmstudio_controller import LMStudioController
from specialist_agents import LMStudioSpecialistClient
from specialist_orchestrator import SpecialistOrchestrator
from specialist_visual_reviewer import review_stage_image
from production_workflows import build_illustrious_workflow, build_klein_workflow

from ada_paths import LEGACY_RUNS_ROOT
ROOT = LEGACY_RUNS_ROOT / "e2e" / "specialist_mini_e2e_008"
CHARACTER, VERSION = "2B", "NieR:Automata"
TASKS = [
    "Create a restrained strategic-censorship scene with a sudden interruption and a clear visual consequence.",
    "Create an organic-occlusion scene where an interrupted wardrobe action changes the character's next movement.",
    "Create a moving-veil scene where an environmental obstruction opens and changes the visible silhouette.",
]
ILL_WORKFLOW = WORKFLOWS_ROOT / "illustrious_4x_api.json"

def read_json(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def http_json(url: str, method: str="GET", payload: Any|None=None, timeout: int=60) -> Any:
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type":"application/json"}, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as res: return json.loads(res.read().decode())

def submit(server: str, prompt: dict[str, Any], label: str) -> str:
    result = http_json(server + "/prompt", "POST", {"prompt":prompt, "client_id":f"ada-mini-{label}-{uuid.uuid4().hex}"})
    if result.get("node_errors"): raise RuntimeError(json.dumps(result["node_errors"], ensure_ascii=False))
    return str(result["prompt_id"])

def wait_history(server: str, prompt_id: str, timeout: int=1200) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        data = http_json(f"{server}/history/{prompt_id}")
        if prompt_id in data:
            item = data[prompt_id]
            if item.get("status", {}).get("status_str") == "error": raise RuntimeError(json.dumps(item, ensure_ascii=False))
            if item.get("outputs"): return item
        time.sleep(2)
    raise TimeoutError(f"ComfyUI timeout: {prompt_id}")

def output_path(history: dict[str, Any], node: str) -> Path:
    images = history.get("outputs", {}).get(node, {}).get("images", [])
    if not images: raise RuntimeError(f"ComfyUI node {node} produced no image")
    d = images[0]
    return (COMFYUI_ROOT / "output" / d.get("subfolder", "") / d["filename"]).resolve()

def upload(server: str, path: Path, name: str) -> str:
    boundary = ("----Ada" + uuid.uuid4().hex).encode(); body = bytearray()
    body.extend(b"--"+boundary+b"\r\nContent-Disposition: form-data; name=\"image\"; filename=\""+name.encode()+b"\"\r\nContent-Type: "+(mimetypes.guess_type(name)[0] or "image/png").encode()+b"\r\n\r\n")
    body.extend(path.read_bytes()); body.extend(b"\r\n--"+boundary+b"--\r\n")
    req = urllib.request.Request(server+"/upload/image", data=bytes(body), headers={"Content-Type":f"multipart/form-data; boundary={boundary.decode()}"}, method="POST")
    with urllib.request.urlopen(req, timeout=120) as res: result=json.loads(res.read().decode())
    return str(result.get("name", name))

def compiled_from_ui(workflow: dict[str, Any]) -> dict[str, Any]:
    links={int(x[0]):(str(x[1]),int(x[2])) for x in workflow["links"]}; inputs={
        1:{"ckpt_name":0},2:{"text":0},3:{"text":0},4:{"width":0,"height":1,"batch_size":2},5:{"seed":0,"steps":2,"cfg":3,"sampler_name":4,"scheduler":5,"denoise":6},7:{"filename_prefix":0},13:{"upscale_method":0,"width":1,"height":2,"crop":3},20:{"filename_prefix":0},21:{"direction":0,"match_image_size":1},22:{"filename_prefix":0},
        37:{"vae_name":0},38:{"noise_seed":0},39:{"text":0},41:{"sampler_name":0},43:{"steps":0,"width":1,"height":2},45:{"unet_name":0,"weight_dtype":1},46:{"clip_name":0,"type":1,"device":2},47:{"guidance":0},50:{"sage_attention":0,"allow_compile":1},52:{"enable_fp16_accumulation":0},53:{"cfg":0}}
    result={}
    for node in workflow["nodes"]:
        nid=str(node["id"]); vals=node.get("widgets_values") or []; ins={}
        for item in node.get("inputs",[]):
            if item.get("link") is not None: ins[item["name"]]=list(links[int(item["link"])])
        for name,index in inputs.get(int(node["id"]),{}).items():
            if index < len(vals): ins[name]=vals[index]
        result[nid]={"class_type":node["type"],"inputs":ins}
    return result

def main() -> int:
    ROOT.mkdir(parents=True, exist_ok=False); write_json(ROOT/"run_config.json", {"character":CHARACTER,"version":VERSION,"review_policy":"strict","tasks":TASKS})
    profile=CharacterProfileDatabase().get_character_profile(CHARACTER, VERSION); write_json(ROOT/"character_profile.json", profile)
    controller=LMStudioController(); controller.unload_all(); orchestrator=None; evidence={"results":[],"model_events":[],"comfy_events":[]}
    for index, task in enumerate(TASKS,1):
        run_dir=ROOT/f"image_{index:02d}"; orchestrator=SpecialistOrchestrator(run_dir, client=None)
        orchestrator.create(f"mini_{index:02d}", character=CHARACTER, version=VERSION, review_policy="strict")
        try:
            t=time.perf_counter(); client=LMStudioSpecialistClient.for_role(controller,"premise_agent"); evidence["model_events"].append({"event":"load","agent":"premise","seconds":round(time.perf_counter()-t,3),"role":"premise_agent"})
            orchestrator.client=client; premise=orchestrator.create_premise(task=task, character_profile=profile, viral_guide="runtime")
            write_json(run_dir/"request.json", {"task":task})
            t=time.perf_counter(); client=LMStudioSpecialistClient.for_role(controller,"illustrious_agent"); evidence["model_events"].append({"event":"load","agent":"illustrious","seconds":round(time.perf_counter()-t,3),"role":"illustrious_agent"})
            orchestrator.client=client; illustrious=orchestrator.compile_illustrious(character_profile=profile, illustrious_guide="runtime")
            workflow=build_illustrious_workflow(positive_prompt=illustrious["illustrious_prompt"],seed=orchestrator.run.read()["seeds"][premise["id"]]["illustrious"],width=768,height=1376,output_prefix=f"AdaMiniE2E/{ROOT.name}/{premise['id']}/illustrious"); write_json(run_dir/"illustrious_workflow.json",workflow)
            t=time.perf_counter(); pid=submit(COMFYUI_BASE_URL,workflow,f"ill-{index}"); path=output_path(wait_history(COMFYUI_BASE_URL,pid),"7"); evidence["comfy_events"].append({"stage":"illustrious_render","seconds":round(time.perf_counter()-t,3),"path":str(path)}); orchestrator.record_illustrious_render(path)
            t=time.perf_counter(); controller.activate_role("visual_review_worker"); review=review_stage_image(path,identifier=premise["id"],stage="illustrious",premise_spec=premise,model=controller.role("visual_review_worker").model,diagnostic_dir=run_dir/"visual_review",context_length=8192); evidence["comfy_events"].append({"stage":"visual_review","seconds":round(time.perf_counter()-t,3)}); orchestrator.record_illustrious_review(review)
            t=time.perf_counter(); client=LMStudioSpecialistClient.for_role(controller,"klein_agent"); evidence["model_events"].append({"event":"load","agent":"klein","seconds":round(time.perf_counter()-t,3),"role":"klein_agent"}); orchestrator.client=client; klein=orchestrator.compile_klein(klein_guide="runtime")
            uploaded=upload(COMFYUI_BASE_URL,path,f"ada_{index:02d}_{premise['id']}.png"); workflow=build_klein_workflow(input_image=uploaded,positive_prompt=klein["klein_prompt"],seed=orchestrator.run.read()["seeds"][premise["id"]]["klein"],output_prefix=f"AdaMiniE2E/{ROOT.name}/{premise['id']}/klein"); write_json(run_dir/"klein_workflow.json",workflow)
            t=time.perf_counter(); kpath=output_path(wait_history(COMFYUI_BASE_URL,submit(COMFYUI_BASE_URL,workflow,f"klein-{index}")),"20"); evidence["comfy_events"].append({"stage":"klein_render","seconds":round(time.perf_counter()-t,3),"path":str(kpath)}); orchestrator.record_klein_render(kpath)
            t=time.perf_counter(); controller.activate_role("visual_review_worker"); final=review_stage_image(kpath,identifier=premise["id"],stage="klein",premise_spec=premise,model=controller.role("visual_review_worker").model,diagnostic_dir=run_dir/"final_review",context_length=8192); evidence["comfy_events"].append({"stage":"final_review","seconds":round(time.perf_counter()-t,3)}); orchestrator.record_final_review(final); orchestrator.complete()
            write_json(run_dir/"prompts.json", {"premise":premise,"illustrious":illustrious,"klein":klein}); write_json(run_dir/"reviews.json", {"illustrious":review,"final":final}); evidence["results"].append({"id":premise["id"],"status":"COMPLETE","illustrious":str(path),"klein":str(kpath)})
        except Exception as exc:
            write_json(ROOT/"evidence_partial.json", {**evidence,"failed_image":index,"error":{"type":type(exc).__name__,"message":str(exc)},"last_state":orchestrator.run.read() if orchestrator else None}); raise
    controller.unload_all(); write_json(ROOT/"evidence.json", evidence); print(json.dumps({"status":"complete","root":str(ROOT)},ensure_ascii=False)); return 0

if __name__ == "__main__": raise SystemExit(main())
