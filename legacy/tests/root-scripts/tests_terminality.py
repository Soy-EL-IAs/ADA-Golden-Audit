import json
import shutil
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from ada_app.run_reconciliation import RunReconciliation
from ada_app.mission_runner import run_mission
from ada_app.mission import ProductionMission

class TestTerminality(unittest.TestCase):
    def setUp(self):
        self.tmp_path = Path("test_terminality_tmp")
        self.tmp_path.mkdir(exist_ok=True)
        self.run_dir = self.tmp_path / "test_run"
        self.run_dir.mkdir(exist_ok=True)
        (self.run_dir / "character_profile.json").write_text('{"name":"2B"}', encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp_path, ignore_errors=True)

    def setup_candidate(self, cid, state_overrides=None, final_review_verdict=None):
        c_dir = self.run_dir / "pilot" / cid
        c_dir.mkdir(parents=True, exist_ok=True)
        
        run_state = {"stage": "FINAL_REVIEWED"}
        if state_overrides:
            run_state.update(state_overrides)
        (c_dir / "ada_run.json").write_text(json.dumps(run_state), encoding="utf-8")
        
        (c_dir / "premise_spec.json").write_text("{}", encoding="utf-8")
        (c_dir / "illustrious_result.json").write_text("{}", encoding="utf-8")
        
        dummy_img = c_dir / "dummy.png"
        dummy_img.write_text("fake image", encoding="utf-8")
        
        run_state["artifacts"] = {"illustrious_image": str(dummy_img.absolute()), "klein_image": str(dummy_img.absolute())}
        (c_dir / "illustrious_review.json").write_text("{}", encoding="utf-8")
        (c_dir / "ada_run.json").write_text(json.dumps(run_state), encoding="utf-8")
        
        if final_review_verdict:
            (c_dir / "final_review.json").write_text(json.dumps({"verdict": final_review_verdict, "summary": "Test"}), encoding="utf-8")
        return c_dir

    def test_final_reviewed_pass_is_not_terminal(self):
        pilot_dir = self.setup_candidate("m1_2b_01", final_review_verdict="PASS")
        recon = RunReconciliation.reconcile(pilot_dir)
        self.assertFalse(recon["is_terminal"])
        self.assertEqual(recon["next_safe_action"], "ROUTE_FINAL")

    def test_approved_is_terminal(self):
        pilot_dir = self.setup_candidate("m1_2b_01", state_overrides={"stage": "COMPLETE"})
        recon = RunReconciliation.reconcile(pilot_dir)
        self.assertTrue(recon["is_terminal"])
        self.assertEqual(recon["next_safe_action"], "NONE")

    def test_retry_exhausted_is_terminal(self):
        pilot_dir = self.setup_candidate("m1_2b_01", state_overrides={"stage": "RETRY_EXHAUSTED"})
        recon = RunReconciliation.reconcile(pilot_dir)
        self.assertTrue(recon["is_terminal"])
        self.assertEqual(recon["next_safe_action"], "NONE")

    def test_failed_runtime_is_terminal(self):
        pilot_dir = self.setup_candidate("m1_2b_01", state_overrides={"stage": "FAILED_RUNTIME"})
        recon = RunReconciliation.reconcile(pilot_dir)
        self.assertTrue(recon["is_terminal"])
        self.assertEqual(recon["next_safe_action"], "NONE")

    @patch("ada_app.mission_runner.run_pilot_pipeline")
    @patch("ada_app.mission_runner.read_json")
    @patch("ada_app.mission_runner.subprocess.run")
    @patch("ada_app.mission_runner.run_m3_analysis", return_value={"m1_2b_01": {}, "m1_2b_02": {}, "m1_2b_03": {}})
    @patch("ada_app.mission_runner.select_top_candidates", return_value=[{"concept_id": "m1_2b_01"}, {"concept_id": "m1_2b_02"}, {"concept_id": "m1_2b_03"}])
    @patch("ada_app.mission_runner.MissionStore")
    def test_mission_target_met_stops_early(self, mock_store_cls, mock_select_top, mock_run_m3, mock_subprocess, mock_read_json, mock_pipeline):
        mock_store = mock_store_cls.return_value
        mission = ProductionMission(character="2B", requested_assets=2)
        mission.status = "PRODUCING"
        mock_store.load.return_value = mission
        
        def side_effect_read_json(path):
            p = str(path)
            if "pilot_candidates.json" in p:
                try:
                    return json.loads(Path(p).read_text(encoding="utf-8"))
                except:
                    return []
            if "concept_proposals_raw.json" in p:
                return [{"concept_id": "m1_2b_01"}, {"concept_id": "m1_2b_02"}, {"concept_id": "m1_2b_03"}]
            # Fall back to real file for everything else (like characters.json)
            try:
                return json.loads(Path(p).read_text(encoding="utf-8"))
            except:
                return {}
            
        mock_read_json.side_effect = side_effect_read_json
        
        def side_effect_pipeline(run_dir, cands, target_approvals=None):
            print("DEBUG PIPELINE RUNNING", len(cands))
            for c in cands[:2]:
                c["pipeline_state"] = "APPROVED"
            if len(cands) > 2:
                cands[2]["pipeline_state"] = "PENDING"
            print("DEBUG WRITING CANDS:", cands)
            (run_dir / "pilot_candidates.json").write_text(json.dumps(cands), encoding="utf-8")
            
        mock_pipeline.side_effect = side_effect_pipeline
        
        run_dir = self.tmp_path / "mission_run"
        run_dir.mkdir(exist_ok=True)
        mission._mission_dir = run_dir
        
        def side_effect_update(m, **kwargs):
            for k, v in kwargs.items():
                setattr(m, k, v)
        mock_store.update.side_effect = side_effect_update
        
        run_mission(mission.mission_id)
        
        print(f"DEBUG: mission.approved_assets={mission.approved_assets}, mission.status={mission.status}")
        
        self.assertEqual(mission.approved_assets, 2)
        self.assertEqual(mission.status, "COMPLETE")

if __name__ == "__main__":
    unittest.main()
