"""Four-scene validation of the registered Klein balanced production default."""
from __future__ import annotations
import json, shutil
from pathlib import Path

import run_full_pipeline as full
from run_full_pipeline import FullPipeline, VERSION, write_json
from ada_paths import ADA_ROOT

from ada_paths import LEGACY_RUNS_ROOT
ROOT = LEGACY_RUNS_ROOT / "balanced-default-validations" / "balanced_v1_scene_set_001"
SCENES = [
    ("closeup", "Create a close-up scene of adult 2B reacting to a sudden interruption, with a readable facial identity anchor and restrained strategic occlusion."),
    ("fullbody", "Create a full-body scene of adult 2B crossing a quiet industrial threshold after an interruption, with clear silhouette, clothing and a visible consequence."),
    ("dynamic", "Create a dynamic scene of adult 2B turning sharply as an environmental obstruction shifts, preserving a clear cause, movement and animation hook."),
    ("cinematic", "Create a complex cinematic scene of adult 2B in a layered industrial environment with foreground occlusion, changing light, a causal interruption and a precise visual consequence."),
]

def main() -> int:
    ROOT.mkdir(parents=True, exist_ok=False)
    gallery_assets = ROOT / "gallery_assets"; gallery_assets.mkdir()
    cases=[]
    for name, task in SCENES:
        run_id=f"balanced_v1_{name}_001"; run_dir=ROOT/run_id
        pipeline=FullPipeline(run_dir, character=full.CHARACTER, version=VERSION, video=False)
        pipeline.orchestrator.create(run_id, character=full.CHARACTER, version=VERSION, review_policy="strict")
        full.TASK = task
        evidence=pipeline.run()
        state=evidence["state"]
        initial=json.loads((run_dir/"illustrious_review.json").read_text(encoding="utf-8"))
        final=json.loads((run_dir/"final_review.json").read_text(encoding="utf-8"))
        drift_items=list(initial.get("drift", []))+list(final.get("drift", []))
        drift_severity="none" if not drift_items else "low" if len(drift_items)==1 else "medium" if len(drift_items)<=3 else "high"
        ill=Path(state["artifacts"]["illustrious_image"]); klein=Path(state["artifacts"]["klein_image"])
        shutil.copy2(ill, gallery_assets/f"{name}_illustrious.png"); shutil.copy2(klein, gallery_assets/f"{name}_klein.png")
        case={"scene":name,"run_id":run_id,"status":state["stage"],"illustrious_source":str(ill),"klein_result":str(klein),"visual_quality":final,"illustrious_preservation":initial,"drift_severity":drift_severity,"render_time":evidence.get("comfy_events", []),"loaded_instances_before_render":[x for x in evidence.get("comfy_model_events", []) if x.get("block") in {"before_illustrious_render","before_klein_render"}],"preset":evidence.get("klein_preset")}
        write_json(run_dir/"case_evidence.json",case); cases.append(case)
    cards=[]
    for case in cases:
        cards.append(f"<section><h2>{case['scene']}</h2><div><figure><img src='gallery_assets/{case['scene']}_illustrious.png'><figcaption>Illustrious source</figcaption></figure><figure><img src='gallery_assets/{case['scene']}_klein.png'><figcaption>Klein result</figcaption></figure></div><p>drift_severity: {case['drift_severity']}</p></section>")
    html="<!doctype html><meta charset='utf-8'><title>Balanced Klein validation</title><style>body{font-family:sans-serif;background:#202124;color:#eee}section{margin:24px 0}section>div{display:flex;gap:18px}figure{margin:0;width:46%}img{width:100%;height:auto}figcaption{padding:6px 0}</style>"+"".join(cards)
    (ROOT/"gallery.html").write_text(html,encoding="utf-8")
    write_json(ROOT/"validation_manifest.json",{"status":"complete","preset":"klein_balanced_v1","cases":cases,"gallery":str(ROOT/"gallery.html")})
    print(json.dumps({"status":"complete","root":str(ROOT),"cases":len(cases)},ensure_ascii=False)); return 0

if __name__ == "__main__": raise SystemExit(main())
