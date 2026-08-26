#!/usr/bin/env python3
"""Canonical runtime entry point for ADA."""

import argparse
import sys
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR / "scripts"))

from ada_paths import ADA_ROOT, LMSTUDIO_BASE_URL, COMFYUI_BASE_URL, WORKFLOWS_ROOT, CHARACTER_DB_ROOT, RUNS_ROOT
from batch_orchestrator import BatchCoordinator

def check_dependencies(mock: bool = False):
    print("[ADA][BOOTSTRAP] Checking dependencies...")
    checks = []
    
    from character_profile import CharacterProfileDatabase
    db = CharacterProfileDatabase()
    if db.dataset_path.exists():
        checks.append(("Character Database", "OK", True))
    else:
        checks.append(("Character Database", f"MISSING ({db.dataset_path})", False))
        
    production_workflows = (
        WORKFLOWS_ROOT / "production" / "illustrious_only_api.json",
        WORKFLOWS_ROOT / "production" / "klein_only_api.json",
    )
    for production_workflow in production_workflows:
        label = production_workflow.stem.replace("_api", "").upper()
        if production_workflow.exists():
            checks.append((f"{label} Workflow", "OK", True))
        else:
            checks.append((f"{label} Workflow", f"MISSING ({production_workflow})", False))
        
    presets = ADA_ROOT / "legacy" / "config" / "klein" / "klein_production_presets.json"
    if presets.exists():
        checks.append(("Klein Presets", "OK", True))
    else:
        checks.append(("Klein Presets", f"MISSING ({presets})", False))
        
    if mock:
        checks.append(("LM Studio", "MOCKED", True))
        checks.append(("ComfyUI", "MOCKED", True))
    else:
        try:
            req = urllib.request.Request(f"{LMSTUDIO_BASE_URL}/v1/models")
            with urllib.request.urlopen(req, timeout=3) as _:
                checks.append(("LM Studio", "OK", True))
        except Exception as e:
            checks.append(("LM Studio", f"UNREACHABLE ({LMSTUDIO_BASE_URL}): {e}", False))
            
        try:
            # Simple GET check for ComfyUI
            req = urllib.request.Request(f"{COMFYUI_BASE_URL}/system_stats")
            with urllib.request.urlopen(req, timeout=3) as _:
                checks.append(("ComfyUI", "OK", True))
        except urllib.error.HTTPError as e:
            # Even if it's 404, it means the server is reachable
            checks.append(("ComfyUI", "OK", True))
        except Exception as e:
            checks.append(("ComfyUI", f"UNREACHABLE ({COMFYUI_BASE_URL}): {e}", False))
            
    failed = False
    for name, status, passed in checks:
        print(f"  - {name}: {status}")
        if not passed:
            failed = True
            
    if failed:
        print("\n[ADA][BOOTSTRAP] CRITICAL: Required dependencies are missing. Exiting.")
        sys.exit(1)
        
    print("[ADA][BOOTSTRAP] All dependencies satisfied.\n")

def main():
    parser = argparse.ArgumentParser(description="ADA Autonomous Image Pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    parser_run = subparsers.add_parser("run", help="Start a new batch run")
    parser_run.add_argument("character", type=str, help="Character name to run")
    parser_run.add_argument("--count", type=int, default=1, help="Number of items to generate")
    parser_run.add_argument("--version", type=str, default=None, help="Specific character version if applicable")
    parser_run.add_argument("--mock-dependencies", action="store_true", help="Bypass dependency checks for testing")
    parser_run.add_argument("--dry-run", action="store_true", help="Stop before executing the batch (testing only)")
    
    parser_resume = subparsers.add_parser("resume", help="Resume an existing batch run")
    parser_resume.add_argument("batch_id", type=str, help="Batch ID to resume")
    parser_resume.add_argument("--mock-dependencies", action="store_true", help="Bypass dependency checks for testing")
    parser_resume.add_argument("--dry-run", action="store_true", help="Stop before executing the batch (testing only)")
    
    args = parser.parse_args()
    
    check_dependencies(mock=args.mock_dependencies)
    
    try:
        if args.command == "run":
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_char = "".join([c if c.isalnum() else "_" for c in args.character]).strip("_")
            batch_id = f"ada_{safe_char}_{timestamp}"
            print(f"[ADA] Starting new batch: {batch_id}")
            coord = BatchCoordinator.create_new(
                runs_dir=RUNS_ROOT,
                batch_id=batch_id,
                character=args.character,
                version=args.version,
                count=args.count
            )
        elif args.command == "resume":
            batch_id = args.batch_id
            print(f"[ADA] Resuming batch: {batch_id}")
            coord = BatchCoordinator.resume(runs_dir=RUNS_ROOT, batch_id=batch_id)
            
        if not args.dry_run:
            coord.run_scheduler()
        else:
            print("[ADA] Dry-run complete. Exiting.")
            
    except Exception as e:
        print(f"\n[ADA][FATAL] {type(e).__name__}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
