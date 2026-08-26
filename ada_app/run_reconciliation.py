import json
from pathlib import Path
from typing import Any, Dict, Tuple

class RunReconciliation:
    """
    Determines the real state of a candidate based on persisted artifacts
    and provides the next safe action.
    """
    
    @staticmethod
    def reconcile(pilot_dir: Path) -> Dict[str, Any]:
        result = {
            "last_valid_stage": "CREATED",
            "missing_artifact": None,
            "next_safe_action": "START_PREMISE",
            "is_terminal": False,
            "is_recoverable": True,
            "is_inconsistent": False
        }
        
        if not pilot_dir.exists():
            return result
            
        run_state_file = pilot_dir / "ada_run.json"
        if not run_state_file.exists():
            return result
            
        try:
            state = json.loads(run_state_file.read_text(encoding="utf-8"))
            reported_stage = state.get("stage", "CREATED")
        except json.JSONDecodeError:
            result["is_inconsistent"] = True
            result["missing_artifact"] = "ada_run.json_corrupted"
            return result
            
        if reported_stage in ("COMPLETE", "FAILED_RUNTIME", "RETRY_EXHAUSTED"):
            result["last_valid_stage"] = reported_stage
            result["is_terminal"] = True
            result["is_recoverable"] = False
            result["next_safe_action"] = "NONE"
            return result
            
        # Determine actual valid stage based on artifacts
        
        # 1. Check Premise
        if not (pilot_dir / "premise_spec.json").exists():
            return result
        
        try:
            json.loads((pilot_dir / "premise_spec.json").read_text(encoding="utf-8"))
            result["last_valid_stage"] = "PREMISES_READY"
            result["next_safe_action"] = "COMPILE_ILLUSTRIOUS"
        except json.JSONDecodeError:
            result["is_inconsistent"] = True
            result["missing_artifact"] = "premise_spec.json_corrupted"
            return result

        # 2. Check Illustrious Prompt
        if not (pilot_dir / "illustrious_result.json").exists():
            return result
            
        try:
            json.loads((pilot_dir / "illustrious_result.json").read_text(encoding="utf-8"))
            result["last_valid_stage"] = "ILLUSTRIOUS_PROMPTS_READY"
            result["next_safe_action"] = "RENDER_ILLUSTRIOUS"
        except json.JSONDecodeError:
            return result
            
        # 3. Check Illustrious Image
        img_path = state.get("artifacts", {}).get("illustrious_image")
        if not img_path or not Path(img_path).exists():
            return result
            
        result["last_valid_stage"] = "ILLUSTRIOUS_RENDERED"
        result["next_safe_action"] = "REVIEW_ILLUSTRIOUS"
        
        # 4. Check Illustrious Review
        if not (pilot_dir / "illustrious_review.json").exists():
            return result
            
        try:
            rev = json.loads((pilot_dir / "illustrious_review.json").read_text(encoding="utf-8"))
            result["last_valid_stage"] = "ILLUSTRIOUS_REVIEWED"
            result["next_safe_action"] = "ROUTE_ILLUSTRIOUS"
            # Note: The QualityRouter handles RETRY or ADVANCE_TO_KLEIN, but for reconciliation
            # if we are in ILLUSTRIOUS_REVIEWED, we need to check if we already routed it.
            # If the stage in ada_run.json is PREMISES_READY, it means a retry was triggered!
            # BUT if we have illustrious_review.json, we might be in the middle of a retry?
            # Actually, backup_attempt moves the old review out. So if illustrious_review exists,
            # it belongs to the CURRENT attempt.
        except json.JSONDecodeError:
            return result
            
        # If we have a review, we must check what the router says. If the router says ADVANCE_TO_KLEIN,
        # we check Klein. If it says RETRY, then we should have been reverted to PREMISES_READY.
        # But if we crashed BEFORE reverting, we should just resume at ROUTE_ILLUSTRIOUS.
        
        # 5. Check Klein Prompt (Deterministic, but we don't save a klein_result.json separately yet,
        # we just generate it on the fly in pilot_runner)
        # We know Klein was rendered if the image exists.
        img_path = state.get("artifacts", {}).get("klein_image")
        if not img_path or not Path(img_path).exists():
            # If it's ADVANCE_TO_KLEIN, then next is RENDER_KLEIN
            from ada_app.quality_router import QualityRouter
            if QualityRouter.route("illustrious", rev.get("verdict", "")) == QualityRouter.ACTION_ADVANCE_TO_KLEIN:
                result["next_safe_action"] = "RENDER_KLEIN"
            return result
            
        result["last_valid_stage"] = "KLEIN_RENDERED"
        result["next_safe_action"] = "REVIEW_KLEIN"
        
        # 6. Check Final Review
        if not (pilot_dir / "final_review.json").exists():
            return result
            
        try:
            final_rev = json.loads((pilot_dir / "final_review.json").read_text(encoding="utf-8"))
            result["last_valid_stage"] = "FINAL_REVIEWED"
            result["next_safe_action"] = "ROUTE_FINAL"
        except json.JSONDecodeError:
            return result
            
        return result
