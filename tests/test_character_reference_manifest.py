import base64
import contextlib
import json
import shutil
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

from scripts.ada_paths import TMP_ROOT
from scripts.character_reference_manifest import (
    load_character_reference_manifest,
    normalize_character_reference_manifest,
)
from scripts.specialist_visual_reviewer import (
    canonical_reference_paths,
    review_stage_image,
)


def _compact_review() -> dict:
    return {
        "id": "candidate_01",
        "stage": "lustify",
        "identity": {"result": "PASS", "score": 9, "confidence": 0.95},
        "subject_count": {"expected": 1, "actual": 1, "result": "PASS"},
        "scores": {"anatomy": 9, "prompt_adherence": 9, "composition": 9, "visual_quality": 9},
        "defects": [],
        "hard_constraint_failures": [],
        "outfit_design_adherence": "Canonical outfit is preserved.",
        "identity_comparison": "Candidate matches the canonical reference.",
        "reference_observations": "Distinctive canonical identity anchors are visible.",
        "candidate_observations": "One coherent subject is visible.",
        "summary": "Identity and requested scene pass.",
    }


class CharacterReferenceManifestTests(unittest.TestCase):
    @staticmethod
    @contextlib.contextmanager
    def temporary_directory():
        TMP_ROOT.mkdir(parents=True, exist_ok=True)
        path = TMP_ROOT / f"character-reference-manifest-{uuid.uuid4().hex}"
        path.mkdir()
        try:
            yield str(path)
        finally:
            shutil.rmtree(path)

    def test_v1_refs_normalize_to_canonical_references(self):
        normalized = normalize_character_reference_manifest({
            "schema_version": 1,
            "refs": [{"file": "refs/ref_01.jpg"}],
        })
        self.assertEqual(normalized["canonical_references"], [{"file": "refs/ref_01.jpg"}])

    def test_v2_canonical_references_remain_authoritative(self):
        canonical = [{"file": "refs/ref_v2.jpg"}]
        normalized = normalize_character_reference_manifest({
            "schema_version": 2,
            "canonical_references": canonical,
            "refs": [{"file": "refs/legacy_alias.jpg"}],
        })
        self.assertEqual(normalized["canonical_references"], canonical)

    def test_v1_and_v2_resolve_physical_canonical_references(self):
        for schema_version, field in ((1, "refs"), (2, "canonical_references")):
            with self.subTest(schema_version=schema_version), self.temporary_directory() as temporary:
                root = Path(temporary)
                reference = root / "refs" / "ref_01.jpg"
                reference.parent.mkdir()
                reference.write_bytes(b"reference-image")
                manifest_path = root / "manifest.json"
                manifest_path.write_text(json.dumps({
                    "schema_version": schema_version,
                    field: [{"file": "refs/ref_01.jpg"}],
                }), encoding="utf-8")
                contract = {"evidence": [{
                    "source": "character_refs_manifest",
                    "reference": str(manifest_path),
                }]}
                loaded = load_character_reference_manifest(manifest_path)
                self.assertGreater(len(loaded["canonical_references"]), 0)
                self.assertEqual(canonical_reference_paths({}, contract), [reference.resolve()])

    def test_visual_review_payload_contains_candidate_then_image_2_reference(self):
        with self.temporary_directory() as temporary:
            root = Path(temporary)
            candidate = root / "candidate.png"
            candidate.write_bytes(b"candidate-image")
            reference = root / "refs" / "ref_01.jpg"
            reference.parent.mkdir()
            reference.write_bytes(b"reference-image")
            manifest_path = root / "manifest.json"
            manifest_path.write_text(json.dumps({
                "schema_version": 1,
                "refs": [{"file": "refs/ref_01.jpg"}],
            }), encoding="utf-8")
            contract = {
                "character_id": "test_character",
                "display_name": "Test Character",
                "identity": {},
                "outfit": {},
                "evidence": [{
                    "source": "character_refs_manifest",
                    "reference": str(manifest_path),
                }],
            }
            spec = {
                "schema_version": "resolved_render_spec_v3",
                "character": {"display_name": "Test Character", "canonical_tag": "test_character", "must_preserve": []},
                "expected_visibility": ["face"],
                "expected_subject_count": 1,
                "validation_requirements": [],
                "render_intent": "semi_realistic",
            }
            captured = {}

            def fake_request(url, payload, timeout=600):
                captured["url"] = url
                captured["payload"] = payload
                return {"choices": [{"finish_reason": "stop", "message": {"content": json.dumps(_compact_review())}}]}

            with patch("scripts.specialist_visual_reviewer._request", side_effect=fake_request):
                result = review_stage_image(
                    candidate,
                    identifier="candidate_01",
                    stage="lustify",
                    premise_spec=spec,
                    character_contract=contract,
                    model="test-vlm",
                )

            content = captured["payload"]["messages"][0]["content"]
            images = [item for item in content if item.get("type") == "image_url"]
            self.assertEqual(len(images), 2)
            self.assertEqual(base64.b64decode(images[0]["image_url"]["url"].split(",", 1)[1]), b"candidate-image")
            self.assertEqual(base64.b64decode(images[1]["image_url"]["url"].split(",", 1)[1]), b"reference-image")
            self.assertEqual(content[0]["text"].rsplit("\n", 1)[-1], "IMAGE UNDER REVIEW:")
            self.assertEqual(content[2]["text"], "CANONICAL REFERENCE 1:")
            self.assertGreater(result["canonical_reference_count"], 0)
            self.assertEqual(result["provenance"]["reference_paths"], [str(reference.resolve())])
