from __future__ import annotations
import json, time
from pathlib import Path
from ada_paths import COMFYUI_BASE_URL, COMFYUI_ROOT
from lmstudio_controller import LMStudioController
from specialist_agents import LMStudioSpecialistClient
from specialist_orchestrator import SpecialistOrchestrator
from specialist_visual_reviewer import review_stage_image
from run_specialist_mini_e2e import output_path, submit, wait_history, upload, read_json, write_json
from production_workflows import build_klein_workflow

from ada_paths import LEGACY_RUNS_ROOT
ROOT = LEGACY_RUNS_ROOT / "e2e" / "specialist_mini_e2e_008"
RUN = ROOT / "image_01"

def main() -> None:
    orchestrator = SpecialistOrchestrator(RUN, client=None)
    state = orchestrator.run.read()
    if state["stage"] != "ILLUSTRIOUS_REVIEWED": raise RuntimeError(f"Expected ILLUSTRIOUS_REVIEWED, got {state['stage']}")
    controller = LMStudioController(); evidence = {"resume_from": state["stage"], "model_events": [], "comfy_events": []}
    t=time.perf_counter(); client=LMStudioSpecialistClient.for_role(controller,"klein_agent"); evidence["model_events"].append({"event":"activate_klein","seconds":round(time.perf_counter()-t,3),"unload":controller.last_unload_diagnostic}); orchestrator.client=client
    klein=orchestrator.compile_klein(klein_guide="runtime")
    write_json(RUN/"klein_prompt_resumed.json", klein)
    image_path=Path(state["artifacts"]["illustrious_image"]); uploaded=upload(COMFYUI_BASE_URL,image_path,"ada_resume_2b_mini_01.png")
    workflow=build_klein_workflow(input_image=uploaded,positive_prompt=klein["klein_prompt"],seed=state["seeds"]["2b_mini_01"]["klein"],output_prefix="AdaMiniE2E/specialist_mini_e2e_008/2b_mini_01/klein"); write_json(RUN/"klein_workflow_resumed.json",workflow)
    t=time.perf_counter(); kpath=output_path(wait_history(COMFYUI_BASE_URL,submit(COMFYUI_BASE_URL,workflow,"klein-resume")),"20"); evidence["comfy_events"].append({"stage":"klein_render","seconds":round(time.perf_counter()-t,3),"path":str(kpath)}); orchestrator.record_klein_render(kpath)
    t=time.perf_counter(); controller.activate_role("visual_review_worker"); evidence["model_events"].append({"event":"activate_final_review","seconds":round(time.perf_counter()-t,3),"unload":controller.last_unload_diagnostic}); final=review_stage_image(kpath,identifier="2b_mini_01",stage="klein",premise_spec=json.loads((RUN/"premise_spec.json").read_text()),model=controller.role("visual_review_worker").model,diagnostic_dir=RUN/"final_review",context_length=8192); evidence["comfy_events"].append({"stage":"final_review","seconds":round(time.perf_counter()-t,3)}); orchestrator.record_final_review(final); orchestrator.complete()
    write_json(RUN/"final_review_resumed.json", final); write_json(ROOT/"resume_evidence.json", evidence); print(json.dumps({"status":"complete","state":orchestrator.run.read(),"evidence":evidence},ensure_ascii=False))

if __name__ == "__main__": main()
