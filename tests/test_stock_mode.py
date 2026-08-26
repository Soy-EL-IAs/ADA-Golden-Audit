import inspect
import json
import unittest
from unittest.mock import patch

from starlette.requests import Request

from ada_app.character_capabilities import resolve_stock_renderer
from ada_app.main import create_mission
from ada_app.mission_runner import run_stock_mission
from ada_app.render_prompt_compilers import build_renderer_prompt_artifact
from ada_app.semantic_contracts import build_character_contract, build_stock_render_spec
from scripts.specialist_visual_reviewer import _normalize_grounded_review


def _request(payload: dict) -> Request:
    body = json.dumps(payload).encode("utf-8")

    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}

    return Request({"type": "http", "method": "POST", "path": "/api/missions/create", "headers": []}, receive)


class StockSemanticTests(unittest.TestCase):
    def setUp(self):
        self.entry = {"name": "2B", "universe": "NieR:Automata"}
        self.contract = build_character_contract({"requested_character": "2B"}, self.entry)

    def test_canonical_outfit_is_semantic_omission(self):
        spec = build_stock_render_spec(self.contract, "stock_001")
        self.assertEqual(spec["creation_mode"], "stock")
        self.assertEqual(spec["stock_policy_version"], "stock_v1")
        self.assertNotIn("outfit_override", spec)
        self.assertEqual(spec["scene_requirements"], [])

    def test_custom_outfit_reaches_renderer_compiler(self):
        outfit = "elegant fitted black cocktail dress"
        spec = build_stock_render_spec(self.contract, "stock_002", outfit_override=outfit)
        artifact = build_renderer_prompt_artifact(
            spec, renderer="lustify", recipe_id="lustify_krea2_primary_v1"
        )
        self.assertEqual(spec["outfit_override"], outfit)
        self.assertIn(outfit, artifact["prompt"])
        self.assertIn("pure seamless white background", artifact["prompt"].lower())

    def test_miaomiao_stock_compiler_returns_complete_artifact(self):
        spec = build_stock_render_spec(self.contract, "stock_miaomiao")
        artifact = build_renderer_prompt_artifact(
            spec, renderer="miaomiao", recipe_id="miaomiao_direct_v1"
        )
        self.assertEqual(artifact["compiler_version"], "miaomiao_stock_prompt_compiler_v1")
        self.assertIn("pure white seamless background", artifact["prompt"])

    def test_certification_ids_remain_metadata_and_never_reach_renderer_prompt(self):
        spec = build_stock_render_spec(self.contract, "stock_metadata")
        identifiers = {
            "mission_id": "mission_cert_123",
            "run_id": "run_cert_456",
            "receipt_id": "receipt_cert_789",
        }
        spec["certification_metadata"] = identifiers
        artifact = build_renderer_prompt_artifact(
            spec, renderer="lustify", recipe_id="lustify_krea2_primary_v1"
        )
        self.assertEqual(spec["certification_metadata"], identifiers)
        for identifier in identifiers.values():
            self.assertNotIn(identifier, artifact["prompt"])

    def test_grounded_review_normalizes_percentage_confidence_and_native_compact_shape(self):
        normalized = _normalize_grounded_review({
            "id": "stock_001",
            "stage": "lustify",
            "identity": {"result": "FAIL", "score": 2, "confidence": 98},
            "subject_count": {"expected": 1, "actual": 1},
            "anatomy": 8,
            "prompt_adherence": 5,
            "composition": 9,
            "visual_quality": 9,
        }, identifier="stock_001", stage="lustify", expected_subject_count=1)
        self.assertEqual(normalized["identity"]["confidence"], 0.98)
        self.assertEqual(normalized["scores"]["anatomy"], 8)
        self.assertTrue(normalized["defects"])

    def test_identity_routing_is_single_direct_renderer(self):
        ghislaine = {
            "renderer_capabilities": {
                "lustify": {"identity_recognition": "unreliable", "img2img": "confirmed"},
                "miaomiao": {"identity_recognition": "confirmed"},
            }
        }
        self.assertEqual(resolve_stock_renderer(ghislaine)["renderer"], "miaomiao")
        self.assertEqual(resolve_stock_renderer(self.entry)["route"], "unverified_primary_fallback")

    def test_stock_runner_has_no_creative_pipeline_invocation(self):
        source = inspect.getsource(run_stock_mission)
        for forbidden in ("M2_SCRIPT", "run_m3_analysis", "select_top_candidates", "subprocess.run"):
            self.assertNotIn(forbidden, source)


class StockApiTests(unittest.IsolatedAsyncioTestCase):
    async def test_stock_payload_drops_hidden_scene_fields_and_empty_outfit(self):
        saved = []

        def capture(mission):
            saved.append(mission)

        with patch("ada_app.main.registered_character_name", return_value="2B"), \
             patch("ada_app.main.read_json", return_value={"2B": self._entry()}), \
             patch("ada_app.mission.MissionStore.save", side_effect=capture), \
             patch("ada_app.mission_runner.start_mission_background"):
            result = await create_mission(_request({
                "creation_mode": "stock", "character": "2B", "requested_assets": 1,
                "where": "Classroom", "what_happens": "drinking coffee",
                "renderer_choice": "miaomiao", "outfit_override": None,
            }))
        self.assertEqual(result.status_code, 400)
        self.assertEqual(saved, [])

        with patch("ada_app.main.registered_character_name", return_value="2B"), \
             patch("ada_app.main.read_json", return_value={"2B": self._entry()}), \
             patch("ada_app.mission.MissionStore.save", side_effect=capture), \
             patch("ada_app.mission_runner.start_mission_background"):
            result = await create_mission(_request({
                "creation_mode": "stock", "character": "2B", "requested_assets": 1,
                "where": "Classroom", "what_happens": "drinking coffee",
                "renderer_choice": "miaomiao",
            }))
        self.assertEqual(result["status"], "created")
        mission = saved[-1]
        self.assertEqual(mission.creation_mode, "stock")
        self.assertEqual(mission.where, "")
        self.assertEqual(mission.what_happens, "")
        self.assertIsNone(mission.outfit_override)
        self.assertEqual(mission.renderer_choice, "lustify")

    async def test_scene_payload_ignores_residual_stock_outfit(self):
        saved = []
        with patch("ada_app.main.registered_character_name", return_value="2B"), \
             patch("ada_app.main.read_json", return_value={"2B": self._entry()}), \
             patch("ada_app.mission.MissionStore.save", side_effect=saved.append), \
             patch("ada_app.mission_runner.start_mission_background"):
            result = await create_mission(_request({
                "creation_mode": "scene", "character": "2B", "requested_assets": 1,
                "where": "rooftop", "what_happens": "drinking coffee",
                "outfit_override": "residual stock outfit",
            }))
        self.assertEqual(result["status"], "created")
        mission = saved[-1]
        self.assertEqual(mission.creation_mode, "scene")
        self.assertEqual(mission.where, "rooftop")
        self.assertEqual(mission.what_happens, "drinking coffee")
        self.assertIsNone(mission.outfit_override)

    @staticmethod
    def _entry():
        return {"name": "2B", "universe": "NieR:Automata"}

import tempfile
from pathlib import Path
from unittest.mock import MagicMock

from ada_app.mission import ProductionMission
from ada_app.main import read_json

class StockPersistenceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.runs_dir = Path(self.temp_dir.name) / 'runs'
        self.runs_dir.mkdir()
        self.patchers = [
            patch('ada_app.mission_runner.RUNS_DIR', self.runs_dir),
            patch('ada_app.run_index.MISSION_RUNS_ROOT', self.runs_dir),
            patch('ada_app.asset_library.LIBRARY_DIR', Path(self.temp_dir.name) / 'library'),
            patch('ada_app.managed_assets.LIBRARY_ASSETS_ROOT', Path(self.temp_dir.name) / 'library_assets'),
        ]
        for p in self.patchers: p.start()

    def tearDown(self):
        for p in self.patchers: p.stop()
        self.temp_dir.cleanup()

    @patch('ada_app.mission_runner.run_renderer_pipeline')
    def test_durable_persistence(self, mock_pipeline):
        mission = ProductionMission(
            mission_id='test_persistence',
            character='2B',
            requested_assets=4,
            creation_mode='stock',
            renderer_choice='lustify'
        )
        mission.status = 'PENDING'
        mission.source_runs = []
        mission.approved_assets = 0
        mission.active_candidates = 0
        
        store = MagicMock()

        outcomes = ['APPROVED', 'REJECTED_QUALITY', 'APPROVED', 'APPROVED', 'APPROVED']
        call_count = [0]
        run_dirs = []

        def side_effect(run_dir, candidates, *args, **kwargs):
            if run_dir not in run_dirs:
                run_dirs.append(run_dir)
                
            candidate = candidates[0]
            candidate['pipeline_state'] = outcomes[call_count[0]]
            if candidate['pipeline_state'] == 'APPROVED':
                fake_jpg = self.runs_dir / 'fake.jpg'
                fake_jpg.touch()
                candidate['render_outputs'] = [{'renderer': 'lustify', 'receipt': {'output_asset': str(fake_jpg)}, 'review': {'verdict': 'PASS'}}]
                
            # simulate what a real pipeline does
            disk_candidates = read_json(run_dir / 'pilot_candidates.json')
            for i, c in enumerate(disk_candidates):
                if c['concept_id'] == candidate['concept_id']:
                    disk_candidates[i] = candidate
            with open(run_dir / 'pilot_candidates.json', 'w') as f:
                json.dump(disk_candidates, f)
                
            reloaded = read_json(run_dir / 'pilot_candidates.json')
            expected_len = call_count[0] + 1
            if len(reloaded) != expected_len:
                raise RuntimeError(f'Expected {expected_len} candidates durably, found {len(reloaded)}')
                
            call_count[0] += 1

        mock_pipeline.side_effect = side_effect

        import tempfile
        import shutil
        from pathlib import Path
        temp_dir = tempfile.mkdtemp()
        temp_lib = Path(temp_dir)
        temp_assets = temp_lib / "assets"
        temp_records = temp_lib / "records"
        
        try:
            with patch('ada_app.character_capabilities.save_character_hero'), \
                 patch('ada_app.asset_library.LIBRARY_DIR', temp_lib), \
                 patch('ada_app.asset_library.INDEX_PATH', temp_lib / "index.json"), \
                 patch('ada_app.asset_library.REVIEW_PATH', temp_lib / "asset_review.json"), \
                 patch('ada_app.asset_library.EXPLICIT_IMAGES_PATH', temp_lib / "explicit_images.json"), \
                 patch('ada_app.managed_assets.LIBRARY_ASSETS_ROOT', temp_assets), \
                 patch('ada_app.managed_assets.LIBRARY_RECORDS_ROOT', temp_records):
                run_stock_mission(mission, store)
                
                from ada_app.asset_library import AssetLibrary
                lib = AssetLibrary()
                lib.build_index()
                accepted_assets = [a for a in lib.get_assets(mission_id='test_persistence') if a.get('is_visible_library_asset') and a.get('creation_mode') == 'stock']
                self.assertEqual(len(accepted_assets), 4)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

        self.assertEqual(call_count[0], 5)
        
        run_dir = run_dirs[0]
        manifest = read_json(run_dir / 'manifest.json')
        self.assertEqual(manifest['attempted'], 5)
        self.assertEqual(manifest['accepted'], 4)
        self.assertEqual(manifest['rejected'], 1)

        final_candidates = read_json(run_dir / 'pilot_candidates.json')
        self.assertEqual(len(final_candidates), 5)
        
        approved_count = sum(1 for c in final_candidates if c['pipeline_state'] == 'APPROVED')
        rejected_count = sum(1 for c in final_candidates if c['pipeline_state'] == 'REJECTED_QUALITY')
        
        self.assertEqual(approved_count, 4)
        self.assertEqual(rejected_count, 1)

        ids = [c['concept_id'] for c in final_candidates]
        self.assertEqual(len(set(ids)), 5)
        self.assertEqual(ids, ['stock_001', 'stock_002', 'stock_003', 'stock_004', 'stock_005'])
