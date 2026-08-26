import json
from pathlib import Path
from ada_app.run_reconciliation import RunReconciliation
from ada_app.quality_router import QualityRouter

def test_reconciliation_empty_dir(tmp_path):
    pilot = tmp_path / "pilot"
    res = RunReconciliation.reconcile(pilot)
    assert res["next_safe_action"] == "START_PREMISE"
    assert not res["is_terminal"]

def test_reconciliation_corrupted_json(tmp_path):
    pilot = tmp_path / "pilot"
    pilot.mkdir()
    (pilot / "ada_run.json").write_text("{corrupt: json", encoding="utf-8")
    res = RunReconciliation.reconcile(pilot)
    assert res["is_inconsistent"]
    assert res["missing_artifact"] == "ada_run.json_corrupted"

def test_reconciliation_resume_illustrious_render(tmp_path):
    pilot = tmp_path / "pilot"
    pilot.mkdir()
    (pilot / "ada_run.json").write_text(json.dumps({"stage": "ILLUSTRIOUS_PROMPTS_READY", "artifacts": {}}), encoding="utf-8")
    (pilot / "premise_spec.json").write_text("{}", encoding="utf-8")
    (pilot / "illustrious_result.json").write_text("{}", encoding="utf-8")
    
    res = RunReconciliation.reconcile(pilot)
    assert res["next_safe_action"] == "RENDER_ILLUSTRIOUS"
    assert res["last_valid_stage"] == "ILLUSTRIOUS_PROMPTS_READY"

def test_reconciliation_resume_after_review(tmp_path):
    pilot = tmp_path / "pilot"
    pilot.mkdir()
    (pilot / "ada_run.json").write_text(json.dumps({"stage": "ILLUSTRIOUS_REVIEWED", "artifacts": {"illustrious_image": "img.png"}}), encoding="utf-8")
    (pilot / "premise_spec.json").write_text("{}", encoding="utf-8")
    (pilot / "illustrious_result.json").write_text("{}", encoding="utf-8")
    (pilot / "img.png").write_text("dummy", encoding="utf-8")
    (pilot / "illustrious_review.json").write_text(json.dumps({"verdict": "PASS"}), encoding="utf-8")
    
    res = RunReconciliation.reconcile(pilot)
    # The review is there, but since no Klein image exists, it goes to ROUTE_ILLUSTRIOUS (which will lead to KLEIN if PASS)
    assert res["next_safe_action"] == "ROUTE_ILLUSTRIOUS"
