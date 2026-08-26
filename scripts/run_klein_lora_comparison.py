"""Prepare or execute a fixed-source Klein second-LoRA comparison."""
from __future__ import annotations
import argparse, copy, json, time, shutil, uuid
from pathlib import Path
from typing import Any

from ada_paths import ADA_ROOT, COMFYUI_ROOT, COMFYUI_BASE_URL
from production_workflows import KLEIN_ONLY_WORKFLOW, build_klein_workflow, validate_klein_workflow
from run_klein_jsonl_batch import apply_klein_preset, http_json, wait_history
from run_specialist_mini_e2e import upload

CONFIG = ADA_ROOT / "legacy" / "config" / "klein" / "klein_lora_comparison_2b_v1.json"
BASE_WORKFLOW = KLEIN_ONLY_WORKFLOW

def read(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def prepare() -> tuple[Path, dict[str, Any]]:
    plan=read(CONFIG); source=ADA_ROOT / plan["source_run"]
    state=read(source/"ada_run.json"); image=Path(state["artifacts"][plan["source_image_artifact"]])
    result=read(source/"klein_result.json"); seed=state["seeds"][result["id"]][plan["seed_artifact"]]
    if not image.is_file(): raise FileNotFoundError(image)
    base=plan["fixed"]; cases=[]
    for index, variant in enumerate(plan["variants"],1):
        preset={"steps":base["steps"],"loras":[{"lora":base["base_lora"],"strength":base["base_lora_strength"]},{"lora":variant["lora"],"strength":variant["strength"]}]}
        workflow=build_klein_workflow(input_image="__PENDING_APPROVED_ILLUSTRIOUS__",positive_prompt=result["klein_prompt"],seed=seed,output_prefix=f"KleinLoRAComparison/{plan['comparison_id']}/{index:02d}_{variant['family']}_{variant['strength']:.2f}"); apply_klein_preset(workflow,preset)
        cases.append({"index":index,"family":variant["family"],"second_lora":variant["lora"],"second_strength":variant["strength"],"base_lora":base["base_lora"],"base_strength":base["base_lora_strength"],"source_image":str(image.resolve()),"klein_prompt":result["klein_prompt"],"klein_seed":seed,"fixed":base,"workflow":workflow,"evaluation":{"visual_quality":None,"illustrious_preservation":None}})
    out=ADA_ROOT/"klein_comparisons"/plan["comparison_id"]; write(out/"comparison_manifest.json",{"schema_version":1,"comparison_id":plan["comparison_id"],"source_image":str(image.resolve()),"klein_prompt":result["klein_prompt"],"klein_seed":seed,"fixed":base,"cases":cases,"evaluation":plan["evaluation"],"status":"prepared_not_executed"}); return out, read(out/"comparison_manifest.json")

def execute(out: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    source = Path(manifest["source_image"]); assets = out / "gallery_assets"; workflows = out / "workflows"; histories = out / "histories"
    assets.mkdir(exist_ok=True); workflows.mkdir(exist_ok=True); histories.mkdir(exist_ok=True)
    shutil.copy2(source, assets / "00_illustrious_source.png")
    uploaded = upload(COMFYUI_BASE_URL, source, f"klein_compare_{manifest['comparison_id']}_source.png")
    ordered = [{"label":"Illustrious source", "asset":"gallery_assets/00_illustrious_source.png"}]
    for case in manifest["cases"]:
        index = int(case["index"]); workflow = copy.deepcopy(case["workflow"])
        workflow["900"]["inputs"]["image"] = uploaded
        validate_klein_workflow(workflow, expected_input_image=uploaded)
        started = time.perf_counter()
        response = http_json(f"{COMFYUI_BASE_URL}/prompt", "POST", {"prompt":workflow, "client_id":f"klein-compare-{uuid.uuid4().hex}"})
        if response.get("node_errors"): raise RuntimeError(json.dumps(response["node_errors"], ensure_ascii=False))
        prompt_id = str(response["prompt_id"]); history = wait_history(COMFYUI_BASE_URL, prompt_id, timeout_seconds=1200)
        images = history.get("outputs", {}).get("20", {}).get("images", [])
        if len(images) != 1: raise RuntimeError(f"Expected one Klein output for case {index}, got {len(images)}")
        descriptor = images[0]; image = (COMFYUI_ROOT / "output" / descriptor.get("subfolder", "") / descriptor["filename"]).resolve()
        if not image.is_file(): raise FileNotFoundError(image)
        asset_name = f"{index:02d}_{case['family']}_{case['second_strength']:.2f}.png"; shutil.copy2(image, assets / asset_name)
        case.update({"status":"complete", "prompt_id":prompt_id, "output_image":str(image), "render_seconds":round(time.perf_counter()-started,3), "visual_quality":None, "illustrious_preservation":None, "drift_severity":None, "workflow_executed":f"workflows/{index:02d}.json", "history_artifact":f"histories/{index:02d}.json"})
        write(workflows / f"{index:02d}.json", workflow); write(histories / f"{index:02d}.json", history)
        ordered.append({"label":f"{case['family']} {case['second_strength']:.2f}", "asset":f"gallery_assets/{asset_name}"})
    manifest["status"] = "rendered_pending_review"; manifest["gallery_order"] = ordered
    write(out / "comparison_manifest.json", manifest); build_gallery(out, manifest); return manifest

def build_gallery(out: Path, manifest: dict[str, Any]) -> None:
    cards=[]
    for item in manifest["gallery_order"]:
        cards.append(f"<article><h2>{item['label']}</h2><img src='{item['asset']}'><p>visual_quality: pending<br>illustrious_preservation: pending<br>drift_severity: pending</p></article>")
    html="<!doctype html><meta charset='utf-8'><title>Klein LoRA comparison</title><style>body{font-family:sans-serif;background:#202124;color:#eee}main{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}article{background:#303134;padding:12px}img{width:100%;height:auto}h2{font-size:18px}</style><main>"+"".join(cards)+"</main>"
    (out / "gallery.html").write_text(html, encoding="utf-8")

def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--execute",action="store_true"); args=parser.parse_args(); out,manifest=prepare();
    if args.execute: manifest=execute(out, manifest)
    print(json.dumps({"status":manifest["status"],"executed":args.execute,"output":str(out),"cases":len(manifest["cases"])},ensure_ascii=False));
    return 0
if __name__ == "__main__": raise SystemExit(main())
