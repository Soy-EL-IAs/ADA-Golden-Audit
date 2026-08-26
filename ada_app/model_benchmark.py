"""Controlled, append-only benchmarks for ADA Model Lab."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts.ada_paths import ADA_ROOT
from ada_app.model_lab import (
    KLEIN_BASELINE_PROMPT,
    MODEL_LAB_ROOT,
    PROFILES_DIR,
    list_test_receipts,
    run_model_test,
    suggested_yoruichi_source,
)
from ada_app.direct_generator_lab import recipe_by_id, run_direct_generator_test
from ada_app.semantic_contracts import build_character_contract
from scripts.character_profile import CharacterProfileDatabase


BENCHMARKS_ROOT = MODEL_LAB_ROOT / "benchmarks"
OFFICIAL_BENCHMARK_ID = "identity_realism_benchmark_001"
DIRECT_BENCHMARK_ID = "direct_generator_benchmark_001"
DIMENSIONS = (
    "identity_preservation", "face_similarity", "expression_preservation",
    "outfit_preservation", "composition_preservation", "realism_quality",
    "skin_quality", "overall",
)
DIRECT_DIMENSIONS = (
    "identity_preservation", "face_similarity", "hairstyle_preservation",
    "eye_color_preservation", "outfit_preservation", "pose_anatomy",
    "composition_preservation", "environment_quality", "prompt_adherence",
    "visual_appeal", "overall",
)
ROLES = (
    "identity_constructor", "anime_to_real_converter",
    "photorealistic_generator", "style_preserver",
    "direct_anime_generator",
)


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, value: Any, *, exclusive: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "x" if exclusive else "w"
    with path.open(mode, encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def benchmark_dir(benchmark_id: str) -> Path:
    if benchmark_id not in {OFFICIAL_BENCHMARK_ID, DIRECT_BENCHMARK_ID}:
        raise ValueError("Unknown Model Lab benchmark")
    return BENCHMARKS_ROOT / benchmark_id


def ensure_official_benchmark() -> dict[str, Any]:
    root = benchmark_dir(OFFICIAL_BENCHMARK_ID)
    manifest_path = root / "benchmark_manifest.json"
    source = suggested_yoruichi_source()
    contract = _latest_character_contract("Shihouin Yoruichi")
    manifest = {
        "schema_version": "model_benchmark_manifest_v1",
        "benchmark_id": OFFICIAL_BENCHMARK_ID,
        "title": "Identity and Realism Benchmark 001",
        "status": "ACTIVE_INITIAL_SLICE",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "roles": list(ROLES),
        "characters": [
            {"name": "Shihouin Yoruichi", "reasons": ["complex hair", "distinctive eyes", "dark skin", "well-known identity"]},
            {"name": "Ghislaine Dedoldia", "reasons": ["non-human traits", "ears", "tail", "tattoo", "complex outfit"]},
            {"name": "2B", "reasons": ["widely-known identity", "iconic dress", "distinctive silhouette"]},
        ],
        "candidate_models": {
            "constructors": ["illustrious_production", "anima_3_8b", "miaomiaoharem_anima16"],
            "realism_converters": ["klein_semi_realistic_baseline", "lustifynsfwcheckpoint_v10krea2"],
        },
        "active_scope": {"characters": 1, "images_per_test": 1, "models_per_execution": 1},
        "evaluation_dimensions": list(DIMENSIONS),
        "decision_question": "Should ADA retain Illustrious to Klein, or does a tested model combination perform better?",
    }
    if manifest_path.is_file():
        existing = _read(manifest_path)
        if isinstance(existing, dict):
            manifest = existing
    else:
        _write(manifest_path, manifest, exclusive=True)

    case_path = root / "test_cases" / "yoruichi_klein_converter_001" / "model_test_case.json"
    if not case_path.is_file():
        test_case = {
            "schema_version": "model_test_case_v1",
            "test_id": "yoruichi_klein_converter_001",
            "benchmark_id": OFFICIAL_BENCHMARK_ID,
            "character": "Shihouin Yoruichi",
            "character_contract": contract,
            "source_asset": source,
            "task": "anime_to_realistic_conversion",
            "role": "anime_to_real_converter",
            "models": ["klein_semi_realistic_baseline"],
            "prompt": KLEIN_BASELINE_PROMPT,
            "seed": 20260824,
            "evaluation_dimensions": list(DIMENSIONS),
            "status": "READY" if source else "BLOCKED",
        }
        _write(case_path, test_case, exclusive=True)
    else:
        test_case = _read(case_path)
        if not test_case.get("character_contract") and contract:
            test_case["character_contract"] = contract
            _write(case_path, test_case)
    return manifest


DIRECT_MODELS = (
    "lustifynsfwcheckpoint_v10krea2",
    "miaomiaoharem_anima16",
    "anima_3_8b",
)
DIRECT_RECIPES = (
    "lustify_krea2_direct_v1",
    "miaomiao_anima16_direct_v1",
    "anima_3_8b_direct_v1",
)

YORUICHI_ROOFTOP_PROMPT = (
    "Shihouin Yoruichi from Bleach, solo adult woman, deep tan skin, vivid golden-yellow eyes, "
    "long rich purple hair in a high ponytail with parted bangs, athletic build, glossy black high-cut "
    "leotard, long black gloves and black thighhighs. On a neon-lit high-rise rooftop just after rain, "
    "she crouches sideways on a narrow wet railing and twists back toward the viewer. One gloved hand "
    "grips the railing; a small black cat balances beside her and looks up at her. Wind moves wet purple "
    "hair strands. Foreground railing, Yoruichi and cat in the middle ground, deep futuristic city below. "
    "Coherent anatomy and balance, detailed hands, accurate identity, cinematic rain lighting, high-impact anime illustration."
)
YORUICHI_SHOWER_PROMPT = (
    "Shihouin Yoruichi from Bleach, solo adult woman, deep tan skin, vivid golden-yellow eyes and long "
    "purple high ponytail with parted bangs, wearing her canonical glossy black leotard, long gloves and "
    "black thighhighs. She stands fully clothed in a modern bathroom immediately after a shower, facing "
    "a large mirror while adjusting one glove. Water droplets remain on her outfit and hair; soft steam "
    "and warm mirror light shape a clear three-quarter composition. Spatially consistent reflection, "
    "recognizable identity and outfit, coherent hands and anatomy, polished high-impact anime illustration."
)
GHISLAINE_ACTION_PROMPT = (
    "Ghislaine Dedoldia from Mushoku Tensei, solo adult beastwoman, dark skin, muscular athletic body, "
    "long gray hair, red eye, eyepatch, cat ears, cat tail and visible tattoo, wearing her canonical "
    "fur-trimmed adventurer outfit. She lands from a powerful sword strike in a ruined stone courtyard, "
    "one foot braced forward and tail counterbalancing the motion. Dynamic low-angle full-body framing, "
    "readable silhouette, correct limbs and weapon grip, dust and broken stone tracing the action arc, "
    "strong identity and outfit fidelity, dramatic high-impact anime illustration."
)


def _booru_prompt(prompt: str) -> str:
    return "masterpiece, best quality, score_9, score_8_up, 1girl, solo, " + prompt


def _snapshot_character_contract(root: Path, character: str) -> str:
    slug = "_".join(character.casefold().split())
    destination = root / "character_contracts" / f"{slug}_character_contract_v1.json"
    if destination.is_file():
        return str(destination.resolve())
    source = _latest_character_contract(character)
    if source:
        contract = _read(Path(source))
    else:
        registry = _read(ADA_ROOT / "config" / "characters.json")
        entry = registry.get(character, {}) if isinstance(registry, dict) else {}
        if not isinstance(entry, dict) or not entry:
            return ""
        profile = CharacterProfileDatabase().get_character_profile(character, entry.get("version"))
        if profile.get("character_profile_used") is not True:
            return ""
        contract = build_character_contract(profile, entry)
    _write(destination, contract, exclusive=True)
    return str(destination.resolve())


def ensure_direct_generator_benchmark() -> dict[str, Any]:
    root = benchmark_dir(DIRECT_BENCHMARK_ID)
    root.mkdir(parents=True, exist_ok=True)
    manifest_path = root / "benchmark_manifest.json"
    manifest = {
        "schema_version": "model_benchmark_manifest_v1",
        "benchmark_id": DIRECT_BENCHMARK_ID,
        "title": "Direct Generator Benchmark 001",
        "status": "ACTIVE_INITIAL_SLICE",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "roles": ["direct_anime_generator"],
        "characters": [
            {"name": "Shihouin Yoruichi", "reasons": ["complex hair", "distinct eyes", "dark skin", "identity stress"]},
            {"name": "Ghislaine Dedoldia", "reasons": ["non-human traits", "body structure", "tattoo", "complex outfit"]},
        ],
        "candidate_models": {"direct_anime_generators": list(DIRECT_MODELS)},
        "recipe_ids": list(DIRECT_RECIPES),
        "active_scope": {"images_per_execution": 1, "models_per_execution": 1, "automatic_batches": False},
        "evaluation_dimensions": list(DIRECT_DIMENSIONS),
        "rankings": ["model_quality", "recipe_quality", "speed_vs_quality"],
        "decision_question": "Which tested model and explicit recipe is the strongest direct anime generator?",
        "promotion_policy": "No automatic promotion. A tested receipt and human evaluation are evidence only.",
    }
    if manifest_path.is_file():
        existing = _read(manifest_path)
        if isinstance(existing, dict):
            manifest = existing
    else:
        _write(manifest_path, manifest, exclusive=True)

    contracts = {
        "Shihouin Yoruichi": _snapshot_character_contract(root, "Shihouin Yoruichi"),
        "Ghislaine Dedoldia": _snapshot_character_contract(root, "Ghislaine Dedoldia"),
    }
    cases = (
        ("yoruichi_rooftop_neon_rain_001", "Shihouin Yoruichi", "rooftop neon rain, black cat, difficult balanced pose", YORUICHI_ROOFTOP_PROMPT, 2026082401),
        ("yoruichi_shower_mirror_001", "Shihouin Yoruichi", "mirror consistency, wet canonical outfit, steam", YORUICHI_SHOWER_PROMPT, 2026082402),
        ("ghislaine_action_identity_001", "Ghislaine Dedoldia", "action anatomy, beast traits, tattoo and outfit identity", GHISLAINE_ACTION_PROMPT, 2026082403),
    )
    for test_id, character, scene_intent, prompt, seed in cases:
        case_path = root / "test_cases" / test_id / "model_test_case.json"
        if case_path.is_file():
            continue
        snapshot = contracts[character]
        test_case = {
            "schema_version": "model_test_case_v1",
            "test_id": test_id,
            "benchmark_id": DIRECT_BENCHMARK_ID,
            "character": character,
            "character_contract": snapshot,
            "character_contract_snapshot": snapshot,
            "source_asset": "",
            "task": "direct_anime_generation",
            "role": "direct_anime_generator",
            "models": list(DIRECT_MODELS),
            "recipe_ids": list(DIRECT_RECIPES),
            "scene_intent": scene_intent,
            "prompt": prompt,
            "recipe_prompts": {
                "lustify_krea2_direct_v1": prompt,
                "miaomiao_anima16_direct_v1": _booru_prompt(prompt),
                "anima_3_8b_direct_v1": _booru_prompt(prompt),
            },
            "seed": seed,
            "evaluation_dimensions": list(DIRECT_DIMENSIONS),
            "status": "READY" if snapshot else "BLOCKED",
        }
        _write(case_path, test_case, exclusive=True)
    return manifest


def _latest_character_contract(character: str) -> str:
    from scripts.ada_paths import MISSION_RUNS_ROOT
    roots = MISSION_RUNS_ROOT
    paths = sorted(roots.glob("m2_*/character_contract_v1.json"), key=lambda path: path.stat().st_mtime, reverse=True) if roots.is_dir() else []
    for path in paths:
        try:
            value = _read(path)
            display_name = value.get("identity", {}).get("display_name") or value.get("display_name")
            if display_name == character:
                return str(path.resolve())
        except Exception:
            continue
    return ""


def _test_case(benchmark_id: str, test_id: str) -> tuple[Path, dict[str, Any]]:
    path = benchmark_dir(benchmark_id) / "test_cases" / test_id / "model_test_case.json"
    if not path.is_file():
        raise ValueError("Unknown Model Lab test case")
    value = _read(path)
    if not isinstance(value, dict):
        raise ValueError("Invalid Model Lab test case")
    return path, value


def execute_test(benchmark_id: str, test_id: str, model_id: str, recipe_id: str | None = None) -> dict[str, Any]:
    case_path, test_case = _test_case(benchmark_id, test_id)
    if model_id not in test_case.get("models", []):
        raise ValueError("Model is not part of this test case")
    if test_case.get("status") == "BLOCKED":
        raise ValueError("Test case is blocked")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    execution_dir = benchmark_dir(benchmark_id) / "executions" / test_id / f"{stamp}_{model_id}"
    if test_case.get("role") == "direct_anime_generator":
        selected_recipe = recipe_id or ""
        if selected_recipe not in test_case.get("recipe_ids", []):
            raise ValueError("Recipe is not part of this test case")
        recipe = recipe_by_id(selected_recipe)
        if recipe.get("model_id") != model_id:
            raise ValueError("Selected recipe does not belong to the selected model")
        prompt = test_case.get("recipe_prompts", {}).get(selected_recipe) or test_case["prompt"]
        receipt = run_direct_generator_test(
            model_id=model_id,
            recipe_id=selected_recipe,
            character=test_case["character"],
            prompt=prompt,
            seed=int(test_case["seed"]),
            character_contract=test_case["character_contract_snapshot"],
            artifact_root=execution_dir,
        )
    else:
        receipt = run_model_test(
            model_id=model_id,
            source_image=test_case["source_asset"],
            character=test_case["character"],
            prompt=test_case["prompt"],
            seed=int(test_case["seed"]),
            artifact_root=execution_dir,
        )
    receipt.update({
        "benchmark_id": benchmark_id, "test_id": test_id, "role": test_case["role"],
        "character_contract": test_case["character_contract"],
    })
    _write(execution_dir / "model_test_receipt.json", receipt)
    test_case["status"] = "IN_PROGRESS" if receipt.get("status") == "COMPLETE" else "FAILED"
    _write(case_path, test_case)
    return receipt


def adopt_existing_receipt(benchmark_id: str, test_id: str) -> dict[str, Any] | None:
    """Link one compatible prior controlled run into the official benchmark without rendering again."""
    case_path, test_case = _test_case(benchmark_id, test_id)
    existing = list((benchmark_dir(benchmark_id) / "executions" / test_id).glob("*/model_test_receipt.json"))
    if existing:
        receipt = _read(existing[0])
        if not receipt.get("character_contract"):
            receipt["character_contract"] = test_case["character_contract"]
            _write(existing[0], receipt)
        return receipt
    match = next((
        receipt for receipt in list_test_receipts()
        if receipt.get("status") == "COMPLETE"
        and receipt.get("model_id") in test_case.get("models", [])
        and receipt.get("character") == test_case.get("character")
        and receipt.get("input_asset") == test_case.get("source_asset")
    ), None)
    if match is None:
        return None
    source_receipt = MODEL_LAB_ROOT / match["run_id"] / "model_test_receipt.json"
    execution_dir = benchmark_dir(benchmark_id) / "executions" / test_id / f"adopted_{match['run_id']}"
    execution_dir.mkdir(parents=True, exist_ok=False)
    adopted = dict(match)
    configuration = adopted.get("configuration", {})
    adopted.update({
        "benchmark_id": benchmark_id,
        "test_id": test_id,
        "role": test_case["role"],
        "character_contract": test_case["character_contract"],
        "model_version": adopted.get("model_version") or "production_baseline_v1",
        "checkpoint": adopted.get("checkpoint") or configuration.get("checkpoint"),
        "adapters": adopted.get("adapters") or configuration.get("loras", []),
        "workflow": adopted.get("workflow") or configuration.get("workflow"),
        "adopted_from": str(source_receipt.resolve()),
    })
    _write(execution_dir / "model_test_receipt.json", adopted, exclusive=True)
    test_case["status"] = "COMPLETE"
    _write(case_path, test_case)
    return adopted


def save_human_evaluation(
    *, benchmark_id: str, test_id: str, run_id: str,
    scores: dict[str, Any], notes: str = "",
) -> dict[str, Any]:
    _, test_case = _test_case(benchmark_id, test_id)
    execution_receipts = list((benchmark_dir(benchmark_id) / "executions" / test_id).glob("*/model_test_receipt.json"))
    receipt_path = next((path for path in execution_receipts if _read(path).get("run_id") == run_id), None)
    if receipt_path is None:
        raise ValueError("Unknown benchmark execution")
    execution = _read(receipt_path)
    normalized: dict[str, int] = {}
    dimensions = tuple(test_case.get("evaluation_dimensions") or DIMENSIONS)
    for dimension in dimensions:
        value = scores.get(dimension)
        if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 10:
            raise ValueError(f"{dimension} must be an integer from 1 to 10")
        normalized[dimension] = value
    created = datetime.now(timezone.utc)
    evaluation_id = f"evaluation_{created.strftime('%Y%m%dT%H%M%S%fZ')}_{uuid.uuid4().hex[:6]}"
    evaluation = {
        "schema_version": "model_evaluation_receipt_v1",
        "evaluation_id": evaluation_id,
        "benchmark_id": benchmark_id,
        "test_id": test_id,
        "run_id": run_id,
        "model_id": execution["model_id"],
        "character": execution["character"],
        "role": test_case["role"],
        "recipe_id": execution.get("recipe_id"),
        "recipe_version": execution.get("recipe_version"),
        "created_at": created.isoformat(),
        "evaluator": "human",
        "scores": normalized,
        "notes": str(notes or ""),
    }
    evaluation_path = benchmark_dir(benchmark_id) / "evaluations" / test_id / f"{evaluation_id}.json"
    _write(evaluation_path, evaluation, exclusive=True)
    _update_role_profile(execution["model_id"], test_case["role"])
    return evaluation


def _update_role_profile(model_id: str, role: str) -> None:
    profile_path = PROFILES_DIR / f"{model_id}.json"
    if not profile_path.is_file():
        raise ValueError("Capability profile is unavailable")
    profile = _read(profile_path)
    evaluations = []
    for path in BENCHMARKS_ROOT.glob("*/evaluations/*/*.json"):
        try:
            value = _read(path)
            if value.get("model_id") == model_id and value.get("role") == role:
                evaluations.append((path, value))
        except Exception:
            continue
    if not evaluations:
        return
    score = round(sum(value["scores"]["overall"] for _, value in evaluations) / len(evaluations), 2)
    roles = profile.setdefault("role_evaluations", {})
    previous = roles.get(role, {})
    roles[role] = {
        "state": "confirmed" if previous.get("state") == "confirmed" else "tested",
        "score": score,
        "sample_count": len(evaluations),
        "evidence_receipts": [str(path.resolve()) for path, _ in evaluations],
    }
    dimension_scores = profile.setdefault("benchmark_dimensions", {})
    all_dimensions = sorted({dimension for _, value in evaluations for dimension in value.get("scores", {})})
    for dimension in all_dimensions:
        matching = [(path, value) for path, value in evaluations if dimension in value.get("scores", {})]
        dimension_scores[dimension] = {
            "state": "tested",
            "score": round(sum(value["scores"][dimension] for _, value in matching) / len(matching), 2),
            "sample_count": len(matching),
            "evidence_receipts": [str(path.resolve()) for path, _ in matching],
        }
    profile["test_status"] = "production_baseline" if profile.get("test_status") == "production_baseline" else "tested"
    _write(profile_path, profile)


def benchmark_results() -> list[dict[str, Any]]:
    if not BENCHMARKS_ROOT.is_dir():
        return []
    results = []
    for root in sorted(BENCHMARKS_ROOT.iterdir()):
        manifest_path = root / "benchmark_manifest.json"
        if not manifest_path.is_file():
            continue
        cases = []
        for case_path in root.glob("test_cases/*/model_test_case.json"):
            case = _read(case_path)
            executions = []
            for receipt_path in root.glob(f"executions/{case['test_id']}/*/model_test_receipt.json"):
                receipt = _read(receipt_path)
                evaluations = [
                    _read(path) for path in root.glob(f"evaluations/{case['test_id']}/*.json")
                    if _read(path).get("run_id") == receipt.get("run_id")
                ]
                executions.append({"receipt": receipt, "evaluations": evaluations})
            cases.append({"test_case": case, "executions": executions})
        rankings = {}
        for role in ROLES:
            rows = []
            for path in root.glob("evaluations/*/*.json"):
                value = _read(path)
                if value.get("role") == role:
                    rows.append(value)
            by_model: dict[str, list[int]] = {}
            for value in rows:
                by_model.setdefault(value["model_id"], []).append(value["scores"]["overall"])
            rankings[role] = sorted([
                {"model_id": model_id, "score": round(sum(scores) / len(scores), 2), "samples": len(scores)}
                for model_id, scores in by_model.items()
            ], key=lambda item: item["score"], reverse=True)
        recipe_scores: dict[str, list[int]] = {}
        evaluated_runs: dict[str, dict[str, Any]] = {}
        for item in cases:
            for execution in item["executions"]:
                evaluated_runs[execution["receipt"].get("run_id", "")] = execution["receipt"]
                for evaluation in execution["evaluations"]:
                    recipe_id = evaluation.get("recipe_id")
                    if recipe_id:
                        recipe_scores.setdefault(recipe_id, []).append(evaluation["scores"]["overall"])
        recipe_rankings = sorted([
            {"recipe_id": recipe_id, "score": round(sum(scores) / len(scores), 2), "samples": len(scores)}
            for recipe_id, scores in recipe_scores.items()
        ], key=lambda item: item["score"], reverse=True)
        speed_quality = []
        for recipe_id, scores in recipe_scores.items():
            timings = [
                receipt.get("inference_seconds") or receipt.get("duration_seconds")
                for receipt in evaluated_runs.values() if receipt.get("recipe_id") == recipe_id
            ]
            timings = [float(value) for value in timings if isinstance(value, (int, float))]
            speed_quality.append({
                "recipe_id": recipe_id,
                "quality": round(sum(scores) / len(scores), 2),
                "average_seconds": round(sum(timings) / len(timings), 3) if timings else None,
                "samples": len(scores),
            })
        speed_quality.sort(key=lambda item: (-item["quality"], item["average_seconds"] or float("inf")))
        manifest = _read(manifest_path)
        recipes = []
        if manifest.get("benchmark_id") == DIRECT_BENCHMARK_ID:
            from ada_app.direct_generator_lab import recipe_catalog
            allowed = set(manifest.get("recipe_ids", []))
            recipes = [recipe for recipe in recipe_catalog() if recipe.get("recipe_id") in allowed]
        results.append({
            "manifest": manifest,
            "cases": cases,
            "rankings": rankings,
            "recipe_rankings": recipe_rankings,
            "speed_quality": speed_quality,
            "recipes": recipes,
        })
    return results
