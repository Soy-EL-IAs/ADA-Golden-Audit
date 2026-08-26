import json, time, threading, traceback, shutil
from pathlib import Path
from typing import Any, List

import sys
ADA_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ADA_ROOT / "scripts"))

from ada_paths import COMFYUI_BASE_URL
from lmstudio_controller import LMStudioController
from specialist_agents import LMStudioSpecialistClient
from specialist_orchestrator import SpecialistOrchestrator
from specialist_visual_reviewer import review_stage_image
from comparative_visual_reviewer import review_stage_comparison

# Reuse ComfyUI helpers from mini_e2e
from run_specialist_mini_e2e import submit, wait_history, output_path, upload
from production_workflows import (
    ILLUSTRIOUS_ONLY_WORKFLOW,
    KLEIN_ONLY_WORKFLOW,
    build_illustrious_workflow,
    build_klein_workflow,
    submission_provenance,
    workflow_generation_details,
)
from agent_contracts import ContractError, validate_contract
from ada_app.quality_router import QualityRouter
from ada_app.final_stage_selection import build_final_stage_decision
from ada_app.run_reconciliation import RunReconciliation
from ada_app.semantic_contracts import (
    build_character_contract,
    build_prompt_artifact,
    build_render_receipt,
    build_resolved_render_spec,
    build_review_observation,
    build_stage_render_plan,
    render_spec_to_premise_spec,
)

MAX_QUALITY_RETRIES = 2
MAX_RUNTIME_RETRIES = 2


class CandidateSetupFailure(RuntimeError):
    """A deterministic candidate failure already persisted for the Mission."""


def deterministic_failure_classification(exc: Exception) -> str | None:
    if isinstance(exc, (ContractError, ValueError)):
        return "CONTRACT_FAILURE"
    if isinstance(exc, (FileNotFoundError, FileExistsError, PermissionError, IsADirectoryError, NotADirectoryError)):
        return "SETUP_FAILURE"
    return None


def prepare_comfy_handoff(controller: LMStudioController) -> dict[str, Any]:
    return controller.prepare_for_comfy(lambda: controller.comfy_status(COMFYUI_BASE_URL))


def prepare_review_handoff(controller: LMStudioController) -> dict[str, Any]:
    return controller.handoff_comfy_to_lm(COMFYUI_BASE_URL)


def release_lm_handoff(controller: LMStudioController) -> dict[str, Any]:
    unloaded = controller.unload_all()
    released = controller.wait_for_vram_release()
    return {"unloaded": unloaded, "vram": released}

def read_json(p: Path): return json.loads(p.read_text(encoding="utf-8"))
def write_json(p: Path, v: Any): 
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def persist_once(path: Path, value: dict[str, Any]) -> dict[str, Any]:
    """Keep versioned semantic artifacts immutable once an attempt persisted them."""
    if path.exists():
        existing = read_json(path)
        if isinstance(existing, dict):
            return existing
    write_json(path, value)
    return value

def registered_character(name: str) -> dict[str, Any]:
    from scripts.ada_paths import CHARACTERS_ROOT
    path = CHARACTERS_ROOT / "catalog.json"
    if not path.exists():
        return {}
    registry = read_json(path)
    if not isinstance(registry, dict):
        return {}
    exact = registry.get(name)
    if isinstance(exact, dict):
        return exact
    folded = name.casefold()
    return next((value for key, value in registry.items() if key.casefold() == folded and isinstance(value, dict)), {})

def registered_character_contract(entry: dict[str, Any]) -> dict[str, Any] | None:
    relative = entry.get("character_contract")
    if not isinstance(relative, str) or not relative.strip():
        return None
    path = Path(relative)
    if not path.is_absolute():
        path = ADA_ROOT / path
    if not path.is_file():
        return None
    value = read_json(path)
    if not isinstance(value, dict):
        return None
    return validate_contract("character_contract_v1", value)

def correction_for_stage(run_dir: Path, concept_id: str, stage: str) -> dict[str, Any]:
    decision = get_candidate(run_dir, concept_id).get("latest_routing_decision", {})
    if not isinstance(decision, dict):
        return {}
    delta = decision.get("correction_delta", {})
    if not isinstance(delta, dict) or delta.get("target_stage") != stage:
        return {}
    return {"source_decision_id": decision.get("decision_id", ""), "instructions": delta.get("instructions", [])}

def persist_stage_plan(
    pilot_dir: Path, run_dir: Path, concept_id: str, render_spec: dict[str, Any], stage: str, attempt: int,
) -> dict[str, Any]:
    path = pilot_dir / "stage_render_plans" / f"{stage}_attempt_{attempt:02d}.json"
    value = build_stage_render_plan(render_spec, stage, attempt, correction_for_stage(run_dir, concept_id, stage))
    return persist_once(path, value)

def persist_prompt(
    pilot_dir: Path, stage_plan: dict[str, Any], positive_prompt: str, negative_prompt: str = "",
) -> dict[str, Any]:
    stage = stage_plan["stage"]
    attempt = stage_plan["attempt"]
    path = pilot_dir / "prompt_artifacts" / f"{stage}_attempt_{attempt:02d}.json"
    return persist_once(path, build_prompt_artifact(stage_plan, positive_prompt, negative_prompt))

def persist_comparative_review(
    pilot_dir: Path, run_dir: Path, concept_id: str, attempt: int,
    render_spec: dict[str, Any], model: str,
) -> dict[str, Any]:
    """Compare exact receipt outputs; independent stage verdicts are context, not votes."""
    path = pilot_dir / "comparative_reviews" / f"comparative_attempt_{attempt:02d}.json"
    if path.exists():
        return validate_contract("comparative_review_v1", read_json(path))
    candidate = get_candidate(run_dir, concept_id)
    receipts = {
        "illustrious": candidate.get("illustrious_render_receipt", {}),
        "klein": candidate.get("klein_render_receipt", {}),
    }
    for stage, receipt in receipts.items():
        validate_contract("render_receipt_v1", receipt)
        if receipt.get("stage") != stage:
            raise ContractError(f"Expected {stage} render receipt")
    observations = {
        "illustrious": candidate.get("illustrious_review_observation", {}),
        "klein": candidate.get("final_review_observation", {}),
    }
    for stage, observation in observations.items():
        validate_contract("review_observation_v1", observation)
        if observation.get("stage") != stage:
            raise ContractError(f"Expected {stage} review observation")
    comparison = review_stage_comparison(
        Path(receipts["illustrious"]["output_asset"]),
        Path(receipts["klein"]["output_asset"]),
        concept_id=concept_id,
        attempt=attempt,
        receipts=receipts,
        render_spec=render_spec,
        observations=observations,
        model=model,
        diagnostic_dir=pilot_dir / "comparative_review" / f"attempt_{attempt:02d}",
    )
    return persist_once(path, comparison)

def persist_final_stage_decision(
    pilot_dir: Path, run_dir: Path, concept_id: str, attempt: int,
    comparison: dict[str, Any],
) -> dict[str, Any]:
    path = pilot_dir / "final_stage_decisions" / f"automatic_attempt_{attempt:02d}.json"
    if path.exists():
        return validate_contract("final_stage_decision_v1", read_json(path))
    candidate = get_candidate(run_dir, concept_id)
    receipts = {
        "illustrious": candidate.get("illustrious_render_receipt", {}),
        "klein": candidate.get("klein_render_receipt", {}),
    }
    return persist_once(path, build_final_stage_decision(comparison, receipts))

def update_candidate_state(run_dir: Path, concept_id: str, updates: dict):
    candidates_file = run_dir / "pilot_candidates.json"
    if candidates_file.exists():
        candidates = read_json(candidates_file)
        for c in candidates:
            if c["concept_id"] == concept_id:
                c.update(updates)
                break
        write_json(candidates_file, candidates)

def persist_candidate_failure(
    run_dir: Path, pilot_dir: Path, concept_id: str, *, classification: str,
    exc: Exception, stage: str, attempt: int, traceback_text: str,
) -> dict[str, Any]:
    details = {
        "classification": classification,
        "exception_type": type(exc).__name__,
        "message": str(exc),
        "traceback": traceback_text,
        "stage": stage,
        "attempt": attempt,
        "candidate_id": concept_id,
    }
    failure_path = pilot_dir / "failures" / f"{stage.casefold()}_attempt_{attempt:02d}.json"
    try:
        write_json(failure_path, details)
        details["artifact"] = str(failure_path.resolve())
    except OSError as persist_error:
        details["failure_artifact_error"] = str(persist_error)
    update_candidate_state(run_dir, concept_id, {
        "pipeline_state": classification,
        "retry_reason": f"{classification}: {type(exc).__name__}: {exc}",
        "failure_details": details,
    })
    return details

def backup_attempt(pilot_dir: Path, attempt_num: int):
    target = pilot_dir / "attempts" / f"{attempt_num:02d}"
    target.mkdir(parents=True, exist_ok=True)
    for p in pilot_dir.iterdir():
        if p.name == "attempts": continue
        if p.name.startswith("_prev_"): continue  # Skip previous backups
        if p.is_file() and p.name != "ada_run.json":
            shutil.copy2(p, target / p.name)
        elif p.is_dir():
            shutil.copytree(p, target / p.name, dirs_exist_ok=True)
            # Rename instead of delete to preserve provenance
            archived = pilot_dir / f"_prev_{attempt_num:02d}_{p.name}"
            if archived.exists():
                shutil.rmtree(archived)  # Only remove previous _prev_ archives, never originals
            p.rename(archived)

def get_candidate(run_dir: Path, concept_id: str):
    candidates = read_json(run_dir / "pilot_candidates.json")
    return next(c for c in candidates if c["concept_id"] == concept_id)

def submission_identity(run_dir: Path, candidate: dict, cid: str, attempt: int) -> dict[str, str]:
    return {
        "mission_id": str(candidate.get("source_mission_id") or f"standalone:{run_dir.name}"),
        "run_id": run_dir.name,
        "concept_id": cid,
        "candidate_id": str(candidate.get("candidate_id") or cid),
        "attempt_id": f"{cid}:attempt:{attempt:02d}",
    }

def persist_submission(pilot_dir: Path, stage: str, attempt: int, value: dict[str, Any]) -> Path:
    path = pilot_dir / "submissions" / f"{stage}_attempt_{attempt:02d}.json"
    write_json(path, value)
    return path

def require_single_output(history: dict[str, Any], node_id: str) -> None:
    images = history.get("outputs", {}).get(node_id, {}).get("images", [])
    if len(images) != 1:
        raise RuntimeError(f"ComfyUI {node_id} must produce exactly one image; found {len(images)}")

def validate_integrity(cid: str, premise_spec: dict, char_profile: dict, prop: dict):
    if premise_spec["id"] != cid:
        raise ValueError(f"CROSS_CANDIDATE_CONTAMINATION: ID mismatch {premise_spec['id']} != {cid}")
    if prop.get("concept_id") and prop.get("concept_id") != cid:
        raise ValueError(f"CROSS_CANDIDATE_CONTAMINATION: Source Concept ID mismatch {prop.get('concept_id')} != {cid}")
    
    char_name = str(char_profile.get("requested_character") or char_profile.get("name") or "").lower()
    prompt_content = json.dumps(premise_spec).lower()
    
    # Strong foreign-character identifiers check
    if "tifa" in char_name:
        foreign = ["2b", "nier", "yorha", "pod 042", "pod"]
        for f in foreign:
            if f in prompt_content:
                raise ValueError(f"CROSS_CANDIDATE_CONTAMINATION: Foreign identifier {f} found in {char_name} candidate {cid}")
    elif "2b" in char_name:
        foreign = ["tifa", "lockhart", "seventh heaven", "strife"]
        for f in foreign:
            if f in prompt_content:
                raise ValueError(f"CROSS_CANDIDATE_CONTAMINATION: Foreign identifier {f} found in {char_name} candidate {cid}")

def execute_candidate(controller: LMStudioController, run_dir: Path, cid: str, prop: dict, char_profile: dict):
    # Ensure prop is the nested proposal dict if it exists
    if "proposal" in prop:
        prop = prop["proposal"]
        
    profile_name = str(char_profile.get("requested_character") or char_profile.get("name") or "").strip()
    registry_entry = registered_character(profile_name)
    pilot_dir = run_dir / "pilot" / cid
    orchestrator = SpecialistOrchestrator(pilot_dir, client=None)

    # Initialize state before writing candidate-local semantic artifacts. Existing
    # CREATED state is resumable; an existing state file is never overwritten.
    try:
        source_contract = registered_character_contract(registry_entry) or build_character_contract(char_profile, registry_entry)
        recon = RunReconciliation.reconcile(pilot_dir)
        if recon["is_terminal"]:
            return
        initialize_state = recon["next_safe_action"] == "START_PREMISE"
        if initialize_state:
            if orchestrator.run.path.exists():
                existing_state = orchestrator.run.read()
                if existing_state["stage"] != "CREATED":
                    raise RuntimeError(
                        f"Candidate setup is incomplete at unexpected ADA stage: {existing_state['stage']}"
                    )
            else:
                orchestrator.create(
                    cid,
                    character=source_contract["display_name"],
                    version=source_contract["profile_version"],
                    review_policy="strict",
                )

        character_contract = persist_once(run_dir / "character_contract_v1.json", source_contract)
        render_spec = persist_once(
            pilot_dir / "resolved_render_spec_v1.json",
            build_resolved_render_spec(character_contract, cid, prop),
        )
        premise_spec = render_spec_to_premise_spec(render_spec)
        validate_integrity(cid, premise_spec, char_profile, prop)
        update_candidate_state(run_dir, cid, {
            "character_profile": char_profile,
            "character_contract": character_contract,
            "resolved_render_spec": render_spec,
            "semantic_contract_versions": {
                "character": character_contract["schema_version"],
                "render_spec": render_spec["schema_version"],
                "stage_plan": "stage_render_plan_v1",
                "prompt": "prompt_artifact_v1",
                "render_receipt": "render_receipt_v1",
                "review_observation": "review_observation_v1",
                "routing_decision": "routing_decision_v1",
            },
        })

        if initialize_state:
            orchestrator.run.allocate_seeds([cid])
            write_json(pilot_dir / "premise_spec.json", premise_spec)
            orchestrator.run.advance("PREMISES_READY", artifacts={
                "premise_spec": "premise_spec.json",
                "character_contract": str((run_dir / "character_contract_v1.json").resolve()),
                "resolved_render_spec": "resolved_render_spec_v1.json",
            })
    except Exception as exc:
        details = persist_candidate_failure(
            run_dir, pilot_dir, cid,
            classification=deterministic_failure_classification(exc) or "SETUP_FAILURE",
            exc=exc,
            stage="INITIALIZE_RUN",
            attempt=1,
            traceback_text=traceback.format_exc(),
        )
        if orchestrator.run.path.exists():
            try:
                orchestrator.run.record_recoverable_failure(exc, component="setup", details=details)
            except Exception:
                pass
        raise CandidateSetupFailure(f"{details['classification']} for {cid}: {exc}") from exc
    
    # Reload candidate state
    cand_state = get_candidate(run_dir, cid)
    quality_retries = cand_state.get("quality_retries", 0)
    runtime_retries = cand_state.get("runtime_retries", 0)
    attempt = quality_retries + 1
    
    while True:
        try:
            recon = RunReconciliation.reconcile(pilot_dir)
            if recon["is_terminal"]:
                break
                
            action = recon["next_safe_action"]
            run_state = orchestrator.run.read()
            
            if action == "COMPILE_ILLUSTRIOUS":
                update_candidate_state(run_dir, cid, {"pipeline_state": "ILLUSTRIOUS", "quality_retries": quality_retries, "max_retries": MAX_QUALITY_RETRIES})
                stage_plan = persist_stage_plan(pilot_dir, run_dir, cid, render_spec, "illustrious", attempt)
                client = LMStudioSpecialistClient.for_role(controller, "illustrious_agent")
                orchestrator.client = client
                illustrious = orchestrator.compile_illustrious(
                    character_profile=char_profile,
                    illustrious_guide="runtime",
                    stage_render_plan=stage_plan,
                )
                prompt_artifact = persist_prompt(pilot_dir, stage_plan, illustrious["illustrious_prompt"])
                orchestrator.run.attach_artifact("illustrious_stage_render_plan", str((pilot_dir / "stage_render_plans" / f"illustrious_attempt_{attempt:02d}.json").resolve()))
                orchestrator.run.attach_artifact("illustrious_prompt_artifact", str((pilot_dir / "prompt_artifacts" / f"illustrious_attempt_{attempt:02d}.json").resolve()))
                update_candidate_state(run_dir, cid, {
                    "illustrious_stage_render_plan": stage_plan,
                    "illustrious_prompt_artifact": prompt_artifact,
                })
                
            elif action == "RENDER_ILLUSTRIOUS":
                update_candidate_state(run_dir, cid, {"pipeline_state": "ILLUSTRIOUS_RENDER", "quality_retries": quality_retries})
                illustrious = read_json(pilot_dir / "illustrious_result.json")
                stage_plan = persist_stage_plan(pilot_dir, run_dir, cid, render_spec, "illustrious", attempt)
                prompt_artifact = persist_prompt(pilot_dir, stage_plan, illustrious["illustrious_prompt"])
                output_prefix = f"AdaPilot/{run_dir.name}/{cid}/illustrious_{attempt}"
                workflow = build_illustrious_workflow(
                    positive_prompt=illustrious["illustrious_prompt"],
                    seed=run_state["seeds"][cid]["illustrious"],
                    width=768,
                    height=1376,
                    output_prefix=output_prefix,
                )
                workflow_artifact = pilot_dir / f"illustrious_workflow_attempt_{attempt:02d}.json"
                write_json(workflow_artifact, workflow)
                generation = workflow_generation_details("illustrious", workflow)
                candidate = get_candidate(run_dir, cid)
                provenance = submission_provenance(
                    **submission_identity(run_dir, candidate, cid, attempt),
                    stage="illustrious",
                    workflow_path=ILLUSTRIOUS_ONLY_WORKFLOW,
                    input_asset=str((pilot_dir / "illustrious_result.json").resolve()),
                )
                
                prepare_comfy_handoff(controller)
                
                pid = submit(COMFYUI_BASE_URL, workflow, f"ill-{cid}")
                provenance["prompt_id"] = pid
                submission_path = persist_submission(pilot_dir, "illustrious", attempt, provenance)
                orchestrator.run.attach_artifact("illustrious_prompt_id", pid)
                orchestrator.run.attach_artifact("illustrious_submission", str(submission_path.resolve()))
                history = wait_history(COMFYUI_BASE_URL, pid)
                require_single_output(history, "7")
                ill_path = output_path(history, "7")
                provenance["output_asset"] = str(ill_path.resolve())
                persist_submission(pilot_dir, "illustrious", attempt, provenance)
                receipt = build_render_receipt(
                    render_spec=render_spec,
                    stage_plan=stage_plan,
                    prompt_artifact=prompt_artifact,
                    workflow=str(ILLUSTRIOUS_ONLY_WORKFLOW),
                    generation=generation,
                    submission=provenance,
                    output_asset=str(ill_path.resolve()),
                )
                receipt_path = pilot_dir / "render_receipts" / f"illustrious_attempt_{attempt:02d}.json"
                receipt = persist_once(receipt_path, receipt)
                orchestrator.record_illustrious_render(ill_path)
                orchestrator.run.attach_artifact("illustrious_output_path", str(ill_path.resolve()))
                orchestrator.run.attach_artifact("illustrious_render_receipt", str(receipt_path.resolve()))
                update_candidate_state(run_dir, cid, {
                    "illustrious_prompt_id": pid,
                    "illustrious_image": str(ill_path.resolve()),
                    "illustrious_submission": str(submission_path.resolve()),
                    "illustrious_generation": generation,
                    "illustrious_stage_render_plan": stage_plan,
                    "illustrious_prompt_artifact": prompt_artifact,
                    "illustrious_render_receipt": receipt,
                })
                
            elif action == "REVIEW_ILLUSTRIOUS":
                update_candidate_state(run_dir, cid, {"pipeline_state": "REVIEW"})
                ill_path = Path(run_state["artifacts"]["illustrious_image"])
                prepare_review_handoff(controller)
                try:
                    controller.activate_role("visual_review_worker")
                    review = review_stage_image(
                        ill_path, identifier=cid, stage="illustrious", premise_spec=render_spec,
                        model=controller.role("visual_review_worker").model,
                        diagnostic_dir=pilot_dir / "visual_review", context_length=8192
                    )
                finally:
                    release_lm_handoff(controller)
                orchestrator.record_illustrious_review(review)
                observation = build_review_observation(review, render_spec, "illustrious", attempt)
                observation_path = pilot_dir / "review_observations" / f"illustrious_attempt_{attempt:02d}.json"
                observation = persist_once(observation_path, observation)
                orchestrator.run.attach_artifact("illustrious_review_observation", str(observation_path.resolve()))
                update_candidate_state(run_dir, cid, {
                    "illustrious_review": review,
                    "illustrious_review_observation": observation,
                })
                
            elif action == "ROUTE_ILLUSTRIOUS":
                review = read_json(pilot_dir / "illustrious_review.json")
                observation_path = pilot_dir / "review_observations" / f"illustrious_attempt_{attempt:02d}.json"
                observation = persist_once(
                    observation_path,
                    build_review_observation(review, render_spec, "illustrious", attempt),
                )
                decision = QualityRouter.decide(observation)
                decision_path = pilot_dir / "routing_decisions" / f"illustrious_attempt_{attempt:02d}.json"
                decision = persist_once(decision_path, decision)
                route_action = decision["action"]
                orchestrator.run.attach_artifact("illustrious_routing_decision", str(decision_path.resolve()))
                update_candidate_state(run_dir, cid, {
                    "illustrious_routing_decision": decision,
                    "latest_routing_decision": decision,
                })
                
                if route_action == QualityRouter.ACTION_ADVANCE_TO_KLEIN:
                    pass # Just loop, reconcile will say RENDER_KLEIN
                elif route_action == QualityRouter.ACTION_RETRY_ILLUSTRIOUS:
                    quality_retries += 1
                    backup_attempt(pilot_dir, attempt)
                    attempt += 1
                    if quality_retries > MAX_QUALITY_RETRIES:
                        update_candidate_state(run_dir, cid, {"pipeline_state": "RETRY_EXHAUSTED", "retry_reason": review["summary"]})
                        break
                    else:
                        update_candidate_state(run_dir, cid, {"pipeline_state": "RETRY_ILLUSTRIOUS", "retry_reason": review["summary"], "quality_retries": quality_retries})
                        orchestrator.run.retry_stage("PREMISES_READY", reason=review["summary"], max_retries=MAX_QUALITY_RETRIES)
                elif route_action == QualityRouter.ACTION_REJECT:
                    update_candidate_state(run_dir, cid, {"pipeline_state": "REJECTED_QUALITY", "retry_reason": review["summary"]})
                    break
                    
            elif action == "RENDER_KLEIN":
                update_candidate_state(run_dir, cid, {"pipeline_state": "KLEIN"})
                stage_plan = persist_stage_plan(pilot_dir, run_dir, cid, render_spec, "klein", attempt)
                klein = orchestrator.compile_klein_deterministic(
                    character_profile=char_profile,
                    stage_render_plan=stage_plan,
                )
                prompt_artifact = persist_prompt(pilot_dir, stage_plan, klein["klein_prompt"])
                ill_path = Path(run_state["artifacts"]["illustrious_image"]).resolve()
                if not ill_path.is_file():
                    raise FileNotFoundError(f"Approved Illustrious artifact is missing: {ill_path}")
                
                uploaded = upload(COMFYUI_BASE_URL, ill_path, f"pilot_{cid}_{attempt}.png")
                klein_seed = run_state["seeds"][cid]["klein"] + quality_retries
                output_prefix = f"AdaPilot/{run_dir.name}/{cid}/klein_{attempt}"
                workflow = build_klein_workflow(
                    input_image=uploaded,
                    positive_prompt=klein["klein_prompt"],
                    seed=klein_seed,
                    output_prefix=output_prefix,
                )
                workflow_artifact = pilot_dir / f"klein_workflow_attempt_{attempt:02d}.json"
                write_json(workflow_artifact, workflow)
                generation = workflow_generation_details("klein", workflow)
                candidate = get_candidate(run_dir, cid)
                provenance = submission_provenance(
                    **submission_identity(run_dir, candidate, cid, attempt),
                    stage="klein",
                    workflow_path=KLEIN_ONLY_WORKFLOW,
                    input_asset=str(ill_path),
                    comfyui_input_name=uploaded,
                )
                
                prepare_comfy_handoff(controller)
                
                pid = submit(COMFYUI_BASE_URL, workflow, f"klein-{cid}")
                provenance["prompt_id"] = pid
                submission_path = persist_submission(pilot_dir, "klein", attempt, provenance)
                orchestrator.run.attach_artifact("klein_prompt_id", pid)
                orchestrator.run.attach_artifact("klein_submission", str(submission_path.resolve()))
                history = wait_history(COMFYUI_BASE_URL, pid)
                require_single_output(history, "20")
                klein_path = output_path(history, "20")
                provenance["output_asset"] = str(klein_path.resolve())
                persist_submission(pilot_dir, "klein", attempt, provenance)
                receipt = build_render_receipt(
                    render_spec=render_spec,
                    stage_plan=stage_plan,
                    prompt_artifact=prompt_artifact,
                    workflow=str(KLEIN_ONLY_WORKFLOW),
                    generation=generation,
                    submission=provenance,
                    output_asset=str(klein_path.resolve()),
                )
                receipt_path = pilot_dir / "render_receipts" / f"klein_attempt_{attempt:02d}.json"
                receipt = persist_once(receipt_path, receipt)
                orchestrator.record_klein_render(klein_path)
                orchestrator.run.attach_artifact("klein_output_path", str(klein_path.resolve()))
                orchestrator.run.attach_artifact("klein_stage_render_plan", str((pilot_dir / "stage_render_plans" / f"klein_attempt_{attempt:02d}.json").resolve()))
                orchestrator.run.attach_artifact("klein_prompt_artifact", str((pilot_dir / "prompt_artifacts" / f"klein_attempt_{attempt:02d}.json").resolve()))
                orchestrator.run.attach_artifact("klein_render_receipt", str(receipt_path.resolve()))
                update_candidate_state(run_dir, cid, {
                    "klein_prompt_id": pid,
                    "klein_image": str(klein_path.resolve()),
                    "klein_input_image": str(ill_path),
                    "klein_submission": str(submission_path.resolve()),
                    "klein_generation": generation,
                    "klein_stage_render_plan": stage_plan,
                    "klein_prompt_artifact": prompt_artifact,
                    "klein_render_receipt": receipt,
                })
                
            elif action == "REVIEW_KLEIN":
                update_candidate_state(run_dir, cid, {"pipeline_state": "FINAL"})
                klein_path = Path(run_state["artifacts"]["klein_image"])
                prepare_review_handoff(controller)
                try:
                    controller.activate_role("visual_review_worker")
                    final_review = review_stage_image(
                        klein_path, identifier=cid, stage="klein", premise_spec=render_spec,
                        model=controller.role("visual_review_worker").model,
                        diagnostic_dir=pilot_dir / "final_review", context_length=8192
                    )
                finally:
                    release_lm_handoff(controller)
                orchestrator.record_final_review(final_review)
                observation = build_review_observation(final_review, render_spec, "klein", attempt)
                observation_path = pilot_dir / "review_observations" / f"klein_attempt_{attempt:02d}.json"
                observation = persist_once(observation_path, observation)
                orchestrator.run.attach_artifact("final_review_observation", str(observation_path.resolve()))
                update_candidate_state(run_dir, cid, {
                    "final_review": final_review,
                    "final_review_observation": observation,
                })
                
            elif action == "ROUTE_FINAL":
                final_review = read_json(pilot_dir / "final_review.json")
                observation_path = pilot_dir / "review_observations" / f"klein_attempt_{attempt:02d}.json"
                observation = persist_once(
                    observation_path,
                    build_review_observation(final_review, render_spec, "klein", attempt),
                )
                decision = QualityRouter.decide(observation)
                decision_path = pilot_dir / "routing_decisions" / f"klein_attempt_{attempt:02d}.json"
                decision = persist_once(decision_path, decision)
                route_action = decision["action"]
                orchestrator.run.attach_artifact("final_routing_decision", str(decision_path.resolve()))
                update_candidate_state(run_dir, cid, {
                    "final_routing_decision": decision,
                    "latest_routing_decision": decision,
                })
                
                if route_action == QualityRouter.ACTION_APPROVE:
                    comparison_path = pilot_dir / "comparative_reviews" / f"comparative_attempt_{attempt:02d}.json"
                    if comparison_path.exists():
                        comparison = validate_contract("comparative_review_v1", read_json(comparison_path))
                    else:
                        prepare_review_handoff(controller)
                        try:
                            controller.activate_role("visual_review_worker")
                            comparison = persist_comparative_review(
                                pilot_dir, run_dir, cid, attempt, render_spec,
                                controller.role("visual_review_worker").model,
                            )
                        finally:
                            release_lm_handoff(controller)
                    final_decision = persist_final_stage_decision(
                        pilot_dir, run_dir, cid, attempt, comparison,
                    )
                    final_decision_path = pilot_dir / "final_stage_decisions" / f"automatic_attempt_{attempt:02d}.json"
                    orchestrator.run.attach_artifact("comparative_review", str(comparison_path.resolve()))
                    orchestrator.run.attach_artifact("final_stage_decision", str(final_decision_path.resolve()))
                    update_candidate_state(run_dir, cid, {
                        "comparative_review": comparison,
                        "automatic_final_stage_decision": final_decision,
                        "final_stage_decision": final_decision,
                        "selected_stage": final_decision["selected_stage"],
                        "selected_image": final_decision["selected_image"],
                        "semantic_contract_versions": {
                            **get_candidate(run_dir, cid).get("semantic_contract_versions", {}),
                            "comparative_review": "comparative_review_v1",
                            "final_stage_decision": "final_stage_decision_v1",
                        },
                    })
                    orchestrator.complete()
                    update_candidate_state(run_dir, cid, {"pipeline_state": "APPROVED"})
                    break
                elif route_action == QualityRouter.ACTION_RETRY_KLEIN:
                    quality_retries += 1
                    backup_attempt(pilot_dir, attempt)
                    attempt += 1
                    if quality_retries > MAX_QUALITY_RETRIES:
                        update_candidate_state(run_dir, cid, {"pipeline_state": "RETRY_EXHAUSTED", "retry_reason": final_review["summary"]})
                        break
                    else:
                        update_candidate_state(run_dir, cid, {"pipeline_state": "RETRY_KLEIN", "retry_reason": final_review["summary"], "quality_retries": quality_retries})
                        orchestrator.run.retry_stage("ILLUSTRIOUS_REVIEWED", reason=final_review["summary"], max_retries=MAX_QUALITY_RETRIES)
                elif route_action == QualityRouter.ACTION_RETRY_ILLUSTRIOUS:
                    quality_retries += 1
                    backup_attempt(pilot_dir, attempt)
                    attempt += 1
                    if quality_retries > MAX_QUALITY_RETRIES:
                        update_candidate_state(run_dir, cid, {"pipeline_state": "RETRY_EXHAUSTED", "retry_reason": final_review["summary"]})
                        break
                    else:
                        update_candidate_state(run_dir, cid, {"pipeline_state": "RETRY_ILLUSTRIOUS", "retry_reason": final_review["summary"], "quality_retries": quality_retries})
                        orchestrator.run.retry_stage("PREMISES_READY", reason=final_review["summary"], max_retries=MAX_QUALITY_RETRIES)
                elif route_action == QualityRouter.ACTION_REJECT:
                    update_candidate_state(run_dir, cid, {"pipeline_state": "REJECTED_QUALITY", "retry_reason": final_review["summary"]})
                    break
                    
            # Reset runtime retries on success
            if runtime_retries > 0:
                runtime_retries = 0
                update_candidate_state(run_dir, cid, {"runtime_retries": 0})
                
        except Exception as exc:
            traceback.print_exc()
            traceback_text = traceback.format_exc()
            classification = deterministic_failure_classification(exc)
            if classification:
                details = persist_candidate_failure(
                    run_dir, pilot_dir, cid,
                    classification=classification,
                    exc=exc,
                    stage=action,
                    attempt=attempt,
                    traceback_text=traceback_text,
                )
                try:
                    orchestrator.run.record_recoverable_failure(exc, component="deterministic", details=details)
                except Exception:
                    pass
                break
            runtime_retries += 1
            update_candidate_state(run_dir, cid, {"runtime_retries": runtime_retries})
            
            if runtime_retries > MAX_RUNTIME_RETRIES:
                details = persist_candidate_failure(
                    run_dir, pilot_dir, cid,
                    classification="FAILED_RUNTIME",
                    exc=exc,
                    stage=action,
                    attempt=attempt,
                    traceback_text=traceback_text,
                )
                try:
                    orchestrator.run.record_recoverable_failure(exc, component="runtime", details=details)
                except Exception:
                    pass
                break
            else:
                update_candidate_state(run_dir, cid, {
                    "pipeline_state": f"RETRYING_RUNTIME ({runtime_retries}/{MAX_RUNTIME_RETRIES})",
                    "retry_reason": f"Operational retry due to: {type(exc).__name__}"
                })
                time.sleep(2) # Backoff
                
def run_pilot_pipeline(run_dir: Path, candidates: List[dict], target_approvals: int = None):
    try:
        controller = LMStudioController()
        release_lm_handoff(controller)
        char_profile = read_json(run_dir / "character_profile.json")
        
        for c in candidates:
            cid = c["concept_id"]
            if target_approvals is not None:
                current_cands = read_json(run_dir / "pilot_candidates.json")
                if sum(1 for cand in current_cands if cand.get("pipeline_state") == "APPROVED") >= target_approvals:
                    # Target met. Only skip if this candidate hasn't started yet.
                    if not (run_dir / "pilot" / cid / "ada_run.json").exists():
                        break
            prop = c["original_proposal"]
            # Skip candidates already terminal
            if c.get("pipeline_state") in {"APPROVED", "REJECTED_QUALITY", "RETRY_EXHAUSTED", "FAILED_RUNTIME", "SETUP_FAILURE", "CONTRACT_FAILURE"}:
                continue
            try:
                execute_candidate(controller, run_dir, cid, prop, char_profile)
            except CandidateSetupFailure:
                traceback.print_exc()
                continue
            
    except Exception as e:
        traceback.print_exc()
    finally:
        try:
            release_lm_handoff(controller)
        except:
            pass
            
    # Check if run globally complete (all candidates in terminal states)
    try:
        candidates_file = run_dir / "pilot_candidates.json"
        if candidates_file.exists():
            cands = read_json(candidates_file)
            terminals = {"APPROVED", "REJECTED_QUALITY", "RETRY_EXHAUSTED", "FAILED_RUNTIME", "SETUP_FAILURE", "CONTRACT_FAILURE"}
            all_terminal = all(c.get("pipeline_state") in terminals for c in cands)
            if all_terminal:
                # Refresh Library Index only when run is complete
                from ada_app.asset_library import AssetLibrary
                AssetLibrary().build_index()
    except Exception:
        pass

def start_pilot_background(run_dir: Path, candidates: List[dict]):
    t = threading.Thread(target=run_pilot_pipeline, args=(run_dir, candidates))
    t.daemon = True
    t.start()
