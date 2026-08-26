"""Current production renderer path: Lustify primary, optional Miaomiao peer output.

The legacy specialist pipeline remains untouched for existing runs.  This module writes
generic renderer lineage and never repurposes historic Illustrious/Klein fields.
"""
from __future__ import annotations

import hashlib
import traceback
from pathlib import Path
from typing import Any

from ada_app.pilot_runner import read_json, write_json, registered_character, registered_character_contract
from ada_app.semantic_contracts import build_character_contract, build_resolved_render_spec, build_resolved_render_spec_v3, build_stock_render_spec, build_stage_render_plan, ConstraintViolation
from ada_app.semantic_contracts import build_review_observation
from scripts.lmstudio_controller import LMStudioController
from scripts.specialist_visual_reviewer import review_stage_image
from scripts.ada_paths import COMFYUI_BASE_URL
from scripts.agent_contracts import validate_contract
from scripts.production_workflows import configured_renderers, build_renderer_workflow, build_lustify_img2img_workflow, production_renderer_preset, renderer_generation_details, renderer_workflow_path
from scripts.run_specialist_mini_e2e import submit, wait_history, output_path, upload
from ada_app.render_prompt_compilers import build_renderer_prompt_artifact
from ada_app.character_capabilities import character_capability_status


def _join(values: list[str]) -> str:
    return ", ".join(value.strip() for value in values if isinstance(value, str) and value.strip())


def compile_renderer_prompt(plan: dict[str, Any], renderer: str) -> str:
    """Two renderers share intent, not a prompt string or a hidden persona default."""
    identity = _join(plan["identity"]["anchors"])
    outfit = _join(plan["outfit_constraints"])
    scene = _join(plan["scene_constraints"])
    composition = plan.get("composition_intent", "")
    snapshot = plan["concept_intent"].get("snapshot", "")
    if renderer == "miaomiao":
        return _join([identity, outfit, scene, composition, snapshot, "single adult woman, coherent everyday scene, detailed anime illustration"])
    return ". ".join(part for part in [f"{identity}." if identity else "", outfit, scene, composition, snapshot, "High-quality coherent image; preserve the resolved character identity and visible outfit."] if part)


def _persist(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    write_json(path, value)


def _record_failure(run_dir: Path, concept_id: str, exc: Exception) -> None:
    candidates = read_json(run_dir / "pilot_candidates.json")
    for candidate in candidates:
        if candidate.get("concept_id") == concept_id:
            if candidate.get("pipeline_state") == "RENDERED_PENDING_REVIEW":
                state = "REVIEW_FAILED"
            else:
                state = "CONTRACT_FAILURE" if isinstance(exc, ConstraintViolation) else "FAILED_RUNTIME"
            candidate.update({"pipeline_state": state, "failure_details": {"stage": "CONSTRAINT_LINTER" if state == "CONTRACT_FAILURE" else "RENDERER_PIPELINE", "exception_type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc(), "candidate_id": concept_id}})
    write_json(run_dir / "pilot_candidates.json", candidates)


def execute_renderer_candidate(run_dir: Path, candidate: dict[str, Any], character_profile: dict[str, Any], *, include_secondary: bool = False, renderer_choice: str | None = None, render_intent: str = "semi_realistic", creation_mode: str = "scene", outfit_override: str | None = None, renderer_routing: dict[str, Any] | None = None) -> None:
    concept_id = candidate["concept_id"]
    proposal = candidate.get("original_proposal", {})
    creative_intent = candidate.get("creative_intent")
    
    generation_mode = candidate.get("generation_mode", "direct")
    source_asset_id = candidate.get("source_asset_id", "")
    explicit_img2img = (generation_mode == "reinterpretation")
    render_mode = "LATENT_IMG2IMG" if explicit_img2img else "DIRECT_T2I"
    
    candidate_dir = run_dir / "pilot" / concept_id
    try:
        entry = registered_character(character_profile.get("requested_character", ""))
        # Onboarding owns the normalized contract.  Rebuilding here from the
        # registry's raw taxonomy would reintroduce contextual booru tags into
        # production prompts, defeating the contract boundary.
        contract = registered_character_contract(entry) or build_character_contract(character_profile, entry)
        # Scene keeps its existing v1/v3 lineage. Stock has its own non-narrative
        # semantic contract and never fabricates a premise to enter this pipeline.
        if creation_mode == "stock":
            spec = build_stock_render_spec(contract, concept_id, outfit_override=outfit_override, render_intent=render_intent)
            legacy_spec = None
        else:
            legacy_spec = build_resolved_render_spec(contract, concept_id, proposal)
            spec = build_resolved_render_spec_v3(contract, concept_id, proposal, creative_intent=creative_intent, render_intent=render_intent, render_mode=render_mode)
        _persist(candidate_dir / "character_contract_v1.json", contract)
        if legacy_spec is not None:
            _persist(candidate_dir / "resolved_render_spec_v1.json", legacy_spec)
            _persist(candidate_dir / "resolved_render_spec_v3.json", spec)
        else:
            _persist(candidate_dir / "resolved_render_spec_stock_v1.json", spec)
            _persist(candidate_dir / "stock_renderer_routing.json", renderer_routing or {})
        selected_renderer = renderer_choice or ("miaomiao" if include_secondary else "lustify")
        capability = entry.get("renderer_capabilities", {}).get("lustify", {}) if isinstance(entry, dict) else {}
        character_route = character_capability_status(entry)
        if character_route["status"] == "red":
            raise ConstraintViolation(character_route["reason"])
        guarded_img2img = creation_mode != "stock" and selected_renderer == "lustify" and character_route["status"] == "yellow"
        
        if explicit_img2img:
            fallback_id = capability.get("fallback_recipe", "lustify_krea2_img2img_v1")
            configured = [(fallback_id, production_renderer_preset(fallback_id))]
        else:
            configured = configured_renderers(renderer_choice="miaomiao" if guarded_img2img else selected_renderer)
            if guarded_img2img:
                fallback_id = capability.get("fallback_recipe", "lustify_krea2_img2img_v1")
                configured.append((fallback_id, production_renderer_preset(fallback_id)))
        
        outputs: list[dict[str, Any]] = []
        source_image: Path | None = None
        
        if explicit_img2img and source_asset_id:
            from ada_app.asset_library import AssetLibrary
            lib = AssetLibrary()
            src_assets = lib.get_assets()
            matched = next((a for a in src_assets if a.get("asset_id") == source_asset_id), None)
            if matched and matched.get("full_image_path"):
                source_image = Path(matched["full_image_path"])
        
        for index, (preset_id, preset) in enumerate(configured, start=1):
            renderer = preset["renderer"]
            existing_outputs = candidate.get("render_outputs", [])
            recovered = next((out for out in existing_outputs if out.get("preset") == preset_id), None)
            
            if recovered and "receipt" in recovered and Path(recovered["receipt"]["output_asset"]).is_file():
                # Skip generation, use existing
                plan = recovered["stage_render_plan"]
                prompt_artifact = recovered["prompt_artifact"]
                effective_renderer = recovered["renderer"]
                role = recovered["role"]
                receipt = recovered["receipt"]
                image = Path(receipt["output_asset"])
                current_output = recovered
                if "review" not in current_output:
                    current_output["review"] = {}
                if "review_observation" not in current_output:
                    current_output["review_observation"] = {}
                outputs.append(current_output)
            else:
                plan = build_stage_render_plan(spec, renderer, 1)
                reference_images = [{"path": str(source_image), "role": "identity_and_composition_reference"}] if source_image else []
                mode = "LATENT_IMG2IMG" if preset_id == "lustify_krea2_img2img_v1" else "DIRECT_T2I"
                prompt_artifact = build_renderer_prompt_artifact(spec, renderer=renderer, recipe_id=preset_id, mode=mode, reference_images=reference_images)
                prompt = prompt_artifact["prompt"]
                _persist(candidate_dir / "stage_render_plans" / f"{renderer}_attempt_01.json", plan)
                _persist(candidate_dir / "prompt_artifacts" / f"{renderer}_attempt_01.json", prompt_artifact)
                seed = int.from_bytes(hashlib.sha256(f"{run_dir.name}:{concept_id}:{renderer}".encode("utf-8")).digest()[:8], "big") & 0x7fffffff
                if preset_id == "lustify_krea2_img2img_v1":
                    if source_image is None:
                        raise RuntimeError("Lustify latent Img2Img requires a trusted Miaomiao source image")
                    if not explicit_img2img:
                        prior = outputs[-1].get("review", {}) if outputs else {}
                        if prior.get("identity_failures") or float(prior.get("agent_scores", {}).get("identity", 0)) < 7:
                            break
                    uploaded = upload(COMFYUI_BASE_URL, source_image, f"ada_{run_dir.name}_{concept_id}_miaomiao.png")
                    workflow = build_lustify_img2img_workflow(source_image=uploaded, positive_prompt=prompt, seed=seed, output_prefix=f"AdaProduction/{run_dir.name}/{concept_id}/lustify_img2img")
                    workflow_path = renderer_workflow_path(preset_id)
                else:
                    workflow = build_renderer_workflow(preset_id=preset_id, positive_prompt=prompt, seed=seed, output_prefix=f"AdaProduction/{run_dir.name}/{concept_id}/{renderer}")
                    workflow_path = renderer_workflow_path(preset_id)
                _persist(candidate_dir / "workflows" / f"{renderer}_attempt_01.json", workflow)
                prompt_id = submit(COMFYUI_BASE_URL, workflow, f"{renderer}-{concept_id}")
                history = wait_history(COMFYUI_BASE_URL, prompt_id)
                image = output_path(history, str(preset["output_node"]))
                generation = renderer_generation_details(preset_id, workflow)
                if preset_id == "lustify_krea2_img2img_v1" and source_image is not None:
                    generation["reference_source_asset"] = str(source_image.resolve())
                    generation["requested_route"] = "lustify"
                generation["semantic_render_spec_v2_id"] = spec["spec_id"]
                generation["creation_mode"] = creation_mode
                if creation_mode == "stock":
                    generation["stock_policy_version"] = "stock_v1"
                    generation["renderer_routing"] = renderer_routing or {}
                effective_renderer = "lustify_img2img" if preset_id == "lustify_krea2_img2img_v1" else renderer
                receipt = {"schema_version": "render_receipt_v2", "receipt_id": f"render:{plan['plan_id']}:{preset_id}", "renderer": effective_renderer, "preset": preset_id, "attempt": 1, "render_spec_id": plan["render_spec_id"], "stage_render_plan_id": plan["plan_id"], "prompt_artifact_id": prompt_artifact["prompt_id"], "workflow": str(workflow_path.resolve()), "generation": generation, "submission": {"prompt_id": prompt_id, "run_id": run_dir.name, "concept_id": concept_id}, "output_asset": str(image.resolve())}
                validate_contract("render_receipt_v2", receipt)
                _persist(candidate_dir / "render_receipts" / f"{renderer}_attempt_01.json", receipt)
                
                role = "identity_reference" if guarded_img2img and preset_id != "lustify_krea2_img2img_v1" else "requested_output"
                current_output = {"renderer": effective_renderer, "review_stage": renderer, "preset": preset_id, "role": role, "receipt": receipt, "stage_render_plan": plan, "prompt_artifact": prompt_artifact, "review": {}, "review_observation": {}}
                outputs.append(current_output)
            
            candidates_tmp = read_json(run_dir / "pilot_candidates.json")
            for c in candidates_tmp:
                if c.get("concept_id") == concept_id:
                    c.update({"pipeline_state": "RENDERED_PENDING_REVIEW", "render_outputs": list(outputs)})
            write_json(run_dir / "pilot_candidates.json", candidates_tmp)

            controller = LMStudioController()
            controller.handoff_comfy_to_lm(COMFYUI_BASE_URL)
            try:
                controller.activate_role("visual_review_worker")
                review = review_stage_image(image, identifier=concept_id, stage=renderer, premise_spec=spec, character_contract=contract, model=controller.role("visual_review_worker").model, diagnostic_dir=candidate_dir / "visual_review" / renderer, context_length=8192)
            finally:
                controller.unload_all()
                controller.wait_for_vram_release()
            observation = build_review_observation(review, spec, renderer, 1)
            _persist(candidate_dir / "review_observations" / f"{renderer}_attempt_01.json", observation)
            
            outputs[-1]["review"] = review
            outputs[-1]["review_observation"] = observation
            
            # Update candidate again with review results
            candidates_tmp = read_json(run_dir / "pilot_candidates.json")
            for c in candidates_tmp:
                if c.get("concept_id") == concept_id:
                    c.update({"render_outputs": list(outputs)})
            write_json(run_dir / "pilot_candidates.json", candidates_tmp)
            
            if role == "identity_reference":
                source_image = image
        passed = [output for output in outputs if output.get("role") != "identity_reference" and output.get("review", {}).get("verdict") == "PASS"]
        if not passed:
            candidates = read_json(run_dir / "pilot_candidates.json")
            for candidate in candidates:
                if candidate.get("concept_id") == concept_id:
                    candidate.update({"pipeline_state": "REJECTED_QUALITY", "render_outputs": outputs, "character_contract": contract, "resolved_render_spec": spec, "creation_mode": creation_mode, "stock_policy_version": "stock_v1" if creation_mode == "stock" else ""})
            write_json(run_dir / "pilot_candidates.json", candidates)
            return
        preferred = passed[0]
        comparison = None
        if len(outputs) > 1:
            comparison = {"schema_version": "comparative_review_v2", "comparison_id": f"renderer-comparison:{concept_id}:01", "concept_id": concept_id, "attempt": 1, "renderers": {output["renderer"]: {"receipt_id": output["receipt"]["receipt_id"], "output_asset": output["receipt"]["output_asset"]} for output in outputs}, "preferred_renderer": preferred["renderer"] if len(passed) == 1 else "HUMAN_REVIEW_REQUIRED", "confidence": 1.0 if len(passed) == 1 else 0.0, "requires_human_review": len(passed) != 1}
            validate_contract("comparative_review_v2", comparison)
            _persist(candidate_dir / "comparative_reviews" / "renderers_attempt_01.json", comparison)
        selected = preferred
        decision = {"schema_version": "final_renderer_decision_v2", "decision_id": f"final-renderer:{concept_id}:01", "concept_id": concept_id, "attempt": 1, "selected_renderer": selected["renderer"], "selected_image": selected["receipt"]["output_asset"], "reason": "Primary renderer passed review." if comparison is None else ("Only one renderer passed review." if len(passed) == 1 else "Both renderers passed independently; human comparison is required before overriding the primary default."), "source": "primary_renderer_default" if comparison is None or len(passed) != 1 else "renderer_comparison", "automatic": True}
        validate_contract("final_renderer_decision_v2", decision)
        _persist(candidate_dir / "final_renderer_decision_v2.json", decision)
        candidates = read_json(run_dir / "pilot_candidates.json")
        for candidate in candidates:
            if candidate.get("concept_id") == concept_id:
                candidate.update({"pipeline_state": "APPROVED", "character_contract": contract, "resolved_render_spec": spec, "render_outputs": outputs, "comparative_review": comparison or {}, "automatic_final_renderer_decision": decision, "selected_renderer": selected["renderer"], "selected_image": selected["receipt"]["output_asset"], "creation_mode": creation_mode, "stock_policy_version": "stock_v1" if creation_mode == "stock" else ""})
        write_json(run_dir / "pilot_candidates.json", candidates)
    except Exception as exc:
        _record_failure(run_dir, concept_id, exc)
        raise


def run_renderer_pipeline(run_dir: Path, candidates: list[dict[str, Any]], target_approvals: int | None = None, *, include_secondary: bool = False, renderer_choice: str | None = None, render_intent: str = "semi_realistic", creation_mode: str = "scene", outfit_override: str | None = None, renderer_routing: dict[str, Any] | None = None, continue_on_error: bool = False) -> None:
    profile = read_json(run_dir / "character_profile.json")
    approved = 0
    for candidate in candidates:
        if target_approvals is not None and approved >= target_approvals:
            break
        if candidate.get("pipeline_state") in {"APPROVED", "FAILED_RUNTIME"}:
            continue
        try:
            execute_renderer_candidate(run_dir, candidate, profile, include_secondary=include_secondary, renderer_choice=renderer_choice, render_intent=render_intent, creation_mode=creation_mode, outfit_override=outfit_override, renderer_routing=renderer_routing)
        except Exception:
            if not continue_on_error:
                raise
            continue
        refreshed = read_json(run_dir / "pilot_candidates.json")
        current = next((item for item in refreshed if item.get("concept_id") == candidate.get("concept_id")), {})
        if current.get("pipeline_state") == "APPROVED":
            approved += 1
