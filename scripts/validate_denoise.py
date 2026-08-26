import sys, os, json
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.run_specialist_mini_e2e import upload, submit, wait_history, output_path
from scripts.production_workflows import build_lustify_img2img_workflow

def generate_with_workflow(url, workflow, prefix):
    prompt_id = submit(url, workflow, prefix)
    history = wait_history(url, prompt_id)
    out_file = output_path(history, "14")
    return out_file

def run_validation():
    source_img_path = Path("D:/IA/ComfyUI_windows_portable_nvidia/ComfyUI_windows_portable/ComfyUI/output/AdaProduction/m2_ada_alpha_golden_1_0_3916a42f_gate3_r01_103149296032/m1_2b_01/miaomiao_00001_.png")
    if not source_img_path.is_file():
        print("Source image not found.")
        sys.exit(1)

    print("Uploading source image...")
    uploaded = upload("http://127.0.0.1:8188", source_img_path, "ada_validation_source.png")

    # Read the prompt from the 0.55 run
    run_dir = Path("D:/IA/Ada/data/runs/missions/m2_ada_alpha_golden_1_0_3916a42f_gate4_rerun2_r01_105200874955")
    prompt_file = run_dir / "pilot" / "m1_2b_02" / "prompt_artifacts" / "lustify_attempt_01.json"
    if not prompt_file.is_file():
        # Fallback to hardcoded prompt from the receipt
        prompt = "Create the requested semi-realistic version from the source image. Strictly preserve the source character identity, face, eyepatch and other species traits, pose, framing, scene, and visible outfit. Do not redesign the character. A polished semi-realistic cinematic illustration of 2B. She is recognizable by blindfold, white hair, short hair. Visible relevant outfit: hairband, clothing cutout, gloves, puffy sleeves. Standing in a futuristic city. subtle, unreadable stare. Inside Tokyo Tower observation deck floor. close up on hands and lower face Coherent anatomy, believable materials, intentional lighting and a clear readable action. Natural skin shading and fabric response while retaining recognizable illustrated identity."
    else:
        prompt = json.loads(prompt_file.read_text())["prompt"]
    
    seed = 855570053 # Exact same seed from 0.55 run
    
    print("Running denoise 0.40...")
    # I already modified pipeline.json to 0.40, but let's be explicit and override it in the workflow.
    # build_lustify_img2img_workflow reads from pipeline.json
    workflow = build_lustify_img2img_workflow(
        source_image=uploaded,
        positive_prompt=prompt,
        seed=seed,
        output_prefix="AdaValidation/denoise_0_40"
    )
    # Force denoise to 0.40 in the workflow
    for node in workflow.values():
        if node.get("class_type") == "KSampler":
            node["inputs"]["denoise"] = 0.40
            
    out_40 = generate_with_workflow("http://127.0.0.1:8188", workflow, "AdaValidation/denoise_0_40")
    print("Denoise 0.40 completed:", out_40)
    
    print("Running denoise 0.55...")
    workflow_55 = build_lustify_img2img_workflow(
        source_image=uploaded,
        positive_prompt=prompt,
        seed=seed,
        output_prefix="AdaValidation/denoise_0_55"
    )
    for node in workflow_55.values():
        if node.get("class_type") == "KSampler":
            node["inputs"]["denoise"] = 0.55
            
    out_55 = generate_with_workflow("http://127.0.0.1:8188", workflow_55, "AdaValidation/denoise_0_55")
    print("Denoise 0.55 completed:", out_55)

if __name__ == "__main__":
    run_validation()
