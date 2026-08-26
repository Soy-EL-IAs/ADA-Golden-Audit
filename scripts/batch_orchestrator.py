#!/usr/bin/env python3
"""Batch Coordinator and Stage Scheduler for ADA."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from ada_batch_state import AdaBatchState
from run_full_pipeline import FullPipeline
from character_dataset import CharacterProfileDatabase

class BatchCoordinator:
    def __init__(self, batch_dir: Path):
        self.batch_dir = batch_dir.resolve()
        self.state = AdaBatchState(self.batch_dir)
        self.pipelines: dict[str, FullPipeline] = {}
        self.profile: dict[str, Any] | None = None
        self.blocked_items: set[str] = set()
        
    @classmethod
    def create_new(cls, runs_dir: Path, batch_id: str, character: str, version: str | None, count: int) -> BatchCoordinator:
        batch_dir = runs_dir / batch_id
        state = AdaBatchState(batch_dir)
        item_ids = [f"{batch_id}_{i:02d}" for i in range(1, count + 1)]
        state.create(batch_id, character=character, version=version, count=count, item_run_ids=item_ids)
        return cls(batch_dir)
        
    @classmethod
    def resume(cls, runs_dir: Path, batch_id: str) -> BatchCoordinator:
        batch_dir = runs_dir / batch_id
        if not batch_dir.exists() or not (batch_dir / "batch_run.json").exists():
            raise FileNotFoundError(f"Batch {batch_id} not found at {batch_dir}")
        return cls(batch_dir)
        
    def _init_pipelines(self) -> None:
        batch = self.state.read()
        self.profile = CharacterProfileDatabase().get_character_profile(batch["character"], batch["version"])
        for item_id in batch["items"]:
            item_dir = self.batch_dir / item_id
            
            # Initialize pipeline wrapper (doesn't overwrite state if it exists)
            pipeline = FullPipeline(item_dir, character=batch["character"], version=batch["version"], video=False)
            
            # If the item doesn't have an ada_run.json yet, create it
            if not (item_dir / "ada_run.json").exists():
                pipeline.orchestrator.create(item_id, character=batch["character"], version=batch["version"], review_policy="strict")
                
            # Create character_profile.json if missing so FullPipeline._premise works
            import json
            profile_path = item_dir / "character_profile.json"
            if not profile_path.exists():
                with profile_path.open("w", encoding="utf-8") as f:
                    json.dump(self.profile, f, ensure_ascii=False, indent=2)

            if not self.profile.get("character_profile_used", False):
                pipeline.orchestrator.run.fail(
                    RuntimeError(
                        f'Character profile not found locally for "{batch["character"]}". Generation was not started.'
                    ),
                    component="character_profile",
                )
                    
            self.pipelines[item_id] = pipeline

    def run_scheduler(self) -> None:
        self._init_pipelines()
        batch = self.state.read()
        items = batch["items"]
        
        while True:
            # Group items by their actionable stage to minimize model swapping
            groups = {
                "LLM_27B": [],       # CREATED, PREMISES_READY
                "COMFY_ILL": [],     # ILLUSTRIOUS_PROMPTS_READY
                "VL_8B_ILL": [],     # ILLUSTRIOUS_RENDERED
                "PYTHON": [],        # ILLUSTRIOUS_REVIEWED
                "COMFY_KLEIN": [],   # KLEIN_PROMPTS_READY
                "VL_8B_KLEIN": [],   # KLEIN_RENDERED
                "FINALIZE": []       # FINAL_REVIEWED
            }
            
            completed_or_failed_or_blocked = 0
            
            for item_id in items:
                state = self.pipelines[item_id].orchestrator.run.read()
                stage = state["stage"]
                
                if stage in {"COMPLETE", "FAILED"} or item_id in self.blocked_items:
                    completed_or_failed_or_blocked += 1
                elif stage in {"CREATED", "PREMISES_READY"}:
                    groups["LLM_27B"].append((item_id, stage))
                elif stage == "ILLUSTRIOUS_PROMPTS_READY":
                    groups["COMFY_ILL"].append((item_id, stage))
                elif stage == "ILLUSTRIOUS_RENDERED":
                    groups["VL_8B_ILL"].append((item_id, stage))
                elif stage == "ILLUSTRIOUS_REVIEWED":
                    groups["PYTHON"].append((item_id, stage))
                elif stage == "KLEIN_PROMPTS_READY":
                    groups["COMFY_KLEIN"].append((item_id, stage))
                elif stage == "KLEIN_RENDERED":
                    groups["VL_8B_KLEIN"].append((item_id, stage))
                elif stage == "FINAL_REVIEWED":
                    groups["FINALIZE"].append((item_id, stage))
                    
            if completed_or_failed_or_blocked == len(items):
                completed = [i for i in items if self.pipelines[i].orchestrator.run.read()["stage"] == "COMPLETE"]
                failed = [i for i in items if self.pipelines[i].orchestrator.run.read()["stage"] == "FAILED"]
                blocked = [i for i in items if i in self.blocked_items]
                
                if len(completed) == len(items):
                    status = "COMPLETE"
                elif len(failed) + len(blocked) == len(items):
                    status = "FAILED"
                else:
                    status = "PARTIAL"
                    
                print(f"\n[ADA][BATCH TERMINAL] Batch {batch['batch_id']} finished with status: {status}")
                print(f"  - Total items: {len(items)}")
                print(f"  - Completed:   {len(completed)}")
                print(f"  - Failed:      {len(failed)}")
                print(f"  - Blocked:     {len(blocked)}")
                print(f"  - Outputs:     {self.batch_dir.resolve()}")
                
                total_illus_attempts = 0
                first_attempt_pass = 0
                first_attempt_minor = 0
                first_attempt_retry = 0
                total_retries = 0
                exhaustion = 0
                for i in items:
                    st = self.pipelines[i].orchestrator.run.read()
                    retries = st.get("retries_PREMISES_READY", 0)
                    total_illus_attempts += (retries + 1)
                    total_retries += retries
                    if retries >= 3 and st["stage"] == "FAILED":
                        exhaustion += 1
                    
                    diag_path = self.batch_dir / i / "diagnostics" / "review_illustrious_attempt_01" / "attempt_01_schema.json"
                    if not diag_path.exists():
                        diag_path = self.batch_dir / i / "diagnostics" / "review_illustrious" / "attempt_01_schema.json"
                        
                    if diag_path.exists():
                        import json
                        try:
                            rev = json.loads(diag_path.read_text(encoding="utf-8"))
                            val = json.loads(rev["choices"][0]["message"]["content"])
                            if val.get("verdict") == "PASS": first_attempt_pass += 1
                            elif val.get("verdict") == "MINOR_DEFECT": first_attempt_minor += 1
                            elif val.get("verdict") in {"RETRY_RENDER", "RETRY_ILLUSTRIOUS"}: first_attempt_retry += 1
                        except Exception:
                            pass
                
                print(f"\n[ADA][QUALITY]")
                print(f"  - First-attempt accepted (PASS/MINOR): {first_attempt_pass + first_attempt_minor}/{len(items)}")
                print(f"  - First-attempt RETRY: {first_attempt_retry}/{len(items)}")
                print(f"  - Total Illustrious attempts: {total_illus_attempts}")
                print(f"  - Total retries: {total_retries}")
                print(f"  - Retry exhaustion: {exhaustion}")
                break
                
            # Execute the first actionable group we find (ordered to flush later stages first ideally, 
            # or grouped by heavy models).
            # We'll execute strictly by checking heavy model groups to batch loads.
            
            executed_any = False
            
            # Map group names to display labels
            display = {
                "LLM_27B": "27B",
                "COMFY_ILL": "COMFY",
                "VL_8B_ILL": "VL",
                "PYTHON": "ADA",
                "COMFY_KLEIN": "COMFY",
                "VL_8B_KLEIN": "VL",
                "FINALIZE": "ADA"
            }
            
            for group_name in ["FINALIZE", "PYTHON", "LLM_27B", "COMFY_ILL", "VL_8B_ILL", "COMFY_KLEIN", "VL_8B_KLEIN"]:
                if groups[group_name]:
                    agent = display[group_name]
                    
                    # Consolidate items by stage for cleaner logging
                    stage_items = {}
                    for item_id, stage in groups[group_name]:
                        stage_items.setdefault(stage, []).append(item_id)
                        
                    for stage, items_in_stage in stage_items.items():
                        item_names = ",".join([i.split("_")[-1] for i in items_in_stage])
                        print(f"[{agent}][{stage}] items {item_names}")
                        
                    for item_id, stage in groups[group_name]:
                        p = self.pipelines[item_id]
                        
                        try:
                            if stage == "CREATED":
                                p._premise(self.profile)
                            elif stage == "PREMISES_READY":
                                p._illustrious(self.profile)
                            elif stage == "ILLUSTRIOUS_PROMPTS_READY":
                                p._illustrious_render()
                            elif stage == "ILLUSTRIOUS_RENDERED":
                                p._illustrious_review()
                                # Special logging for visual review verdicts
                                review_path = p.orchestrator.run.run_dir / "illustrious_review.json"
                                if review_path.exists():
                                    with open(review_path, "r") as f:
                                        rev = __import__("json").load(f)
                                        print(f"[{agent}][REVIEW] item {item_id.split('_')[-1]} -> {rev.get('verdict')}")
                            elif stage == "ILLUSTRIOUS_REVIEWED":
                                p._klein(self.profile)
                            elif stage == "KLEIN_PROMPTS_READY":
                                p._klein_render()
                            elif stage == "KLEIN_RENDERED":
                                p._final_review()
                            elif stage == "FINAL_REVIEWED":
                                p.orchestrator.complete()
                        except Exception as e:
                            print(f"[ADA][ERROR] Item {item_id} failed at {stage}: {e}")
                            self.blocked_items.add(item_id)
                            
                    executed_any = True
                    break # Break out of group loop to re-evaluate state across all items
                    
            if not executed_any:
                print("Stalled: No actionable items found but batch not complete.")
                break

if __name__ == '__main__':
    pass
