#!/usr/bin/env python3
"""Run the isolated Master-authored render validation from selected premises."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

if __package__:
    from .ada_paths import ADA_ROOT, COMFYUI_ROOT, CONFIG_ROOT, KLEIN_BATCH_RUNS_ROOT, PROMPTS_ROOT
    from .ada_evolution_runner import LocalLMStudio
    from .lmstudio_controller import LMStudioController
    from .run_klein_jsonl_batch import load_dataset
    from .visual_reviewer import review_master_image
else:
    from ada_paths import ADA_ROOT, COMFYUI_ROOT, CONFIG_ROOT, KLEIN_BATCH_RUNS_ROOT, PROMPTS_ROOT
    from ada_evolution_runner import LocalLMStudio
    from lmstudio_controller import LMStudioController
    from run_klein_jsonl_batch import load_dataset
    from visual_reviewer import review_master_image


from ada_paths import LEGACY_RUNS_ROOT
DEFAULT_SOURCE = LEGACY_RUNS_ROOT / "evolution" / "directed_validation" / "render_validation_001" / "selected" / "premises.jsonl"
DEFAULT_RUN_DIR = LEGACY_RUNS_ROOT / "evolution" / "directed_validation" / "render_validation_001" / "master_full_run_001"
DEFAULT_EROTIC_GUIDE = Path(r"C:\Users\ELIAS\Downloads\Ada_Erotic_Suggestive_Hook_Guide_v2.md")
ILLUSTRIOUS_GUIDE = CONFIG_ROOT / "prompt_guides" / "illustrious_prompt_guide_v1.md"
KLEIN_GUIDE = CONFIG_ROOT / "prompt_guides" / "klein_prompt_guide_v1.md"
PROFILE_DB = ADA_ROOT / "data" / "character_db" / "booru_characters" / "characters.jsonl"
WORKFLOW: Path | None = None
RUNNER = ADA_ROOT / "scripts" / "run_klein_jsonl_batch.py"
GALLERY = ADA_ROOT / "scripts" / "build_klein_gallery.py"

MASTER_KEYS = {
    "id", "category", "illustrious_prompt", "preserved_elements", "risk_notes",
    "klein_prompt", "illustrious_seed", "klein_seed",
}
PHYSICAL_CAMERA_RE = re.compile(r"\b(camera|lens|photographer|filming|filming equipment)\b", re.I)
NEGATIVE_IN_POSITIVE_RE = re.compile(
    r"\bno\s+(glamour|generic|action|explicit|sexual|nudity|fanart|spectacle|trailer)", re.I
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{number}: expected a JSON object")
        rows.append(value)
    if not rows:
        raise ValueError(f"No records in {path}")
    return rows


def write_json_new(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as output:
        json.dump(value, output, ensure_ascii=False, indent=2)
        output.write("\n")


def write_jsonl_new(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as output:
        for row in rows:
            output.write(json.dumps(row, ensure_ascii=False) + "\n")


def parse_json_response(content: str) -> Any:
    text = content.strip()
    if text.startswith("```"):
        text = text[3:].lstrip()
        if text.startswith("json"):
            text = text[4:].lstrip()
        text = text.removesuffix("```").strip()
    start = min((index for index in (text.find("["), text.find("{")) if index >= 0), default=-1)
    if start < 0:
        raise ValueError("Master response contains no JSON")
    value, _ = json.JSONDecoder().raw_decode(text[start:])
    return value


def character_profile() -> dict[str, Any]:
    for row in read_jsonl(PROFILE_DB):
        if row.get("name") == "2b_(nier:automata)":
            return row
    raise ValueError("Local 2B character profile is unavailable")


def validate_master_batch(value: Any, expected: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not isinstance(value, list) or len(value) != len(expected):
        raise ValueError(f"Expected exactly {len(expected)} translated records")
    expected_by_id = {row["id"]: row for row in expected}
    if len(expected_by_id) != len(expected):
        raise ValueError("Source premise IDs are not unique")
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, row in enumerate(value, 1):
        if not isinstance(row, dict) or set(row) != MASTER_KEYS:
            raise ValueError(f"Record {index} must contain exactly {sorted(MASTER_KEYS)}")
        identifier = row.get("id")
        if identifier not in expected_by_id or identifier in seen:
            raise ValueError(f"Unexpected or duplicate id: {identifier!r}")
        source = expected_by_id[identifier]
        if row.get("category") != source.get("category"):
            raise ValueError(f"{identifier}: category changed")
        for field in ("illustrious_prompt", "klein_prompt"):
            prompt = row.get(field)
            if not isinstance(prompt, str) or not prompt.strip() or len(prompt) > 3000:
                raise ValueError(f"{identifier}: invalid {field}")
            if PHYSICAL_CAMERA_RE.search(prompt):
                raise ValueError(f"{identifier}: {field} uses physical camera language")
        if NEGATIVE_IN_POSITIVE_RE.search(row["illustrious_prompt"]):
            raise ValueError(f"{identifier}: anti-pattern instruction embedded in positive prompt")
        for field, minimum in (("preserved_elements", 5), ("risk_notes", 1)):
            items = row.get(field)
            if not isinstance(items, list) or len(items) < minimum or not all(
                isinstance(item, str) and item.strip() for item in items
            ):
                raise ValueError(f"{identifier}: invalid {field}")
        for field in ("illustrious_seed", "klein_seed"):
            seed = row.get(field)
            if isinstance(seed, bool) or not isinstance(seed, int) or not 0 <= seed <= 2**63 - 1:
                raise ValueError(f"{identifier}: invalid {field}")
        seen.add(identifier)
        result.append(row)
    if seen != set(expected_by_id):
        raise ValueError("Master output does not cover all requested IDs")
    return sorted(result, key=lambda row: list(expected_by_id).index(row["id"]))


def master_prompt(
    batch: list[dict[str, Any]], erotic_guide: str, illustrious_guide: str,
    klein_guide: str, profile: dict[str, Any], batch_number: int,
) -> str:
    source = [
        {"id": row["id"], "category": row["category"], "premise": row["premise"]}
        for row in batch
    ]
    return f"""You are Ada's local MASTER running an isolated end-to-end visual validation.
This is translation and execution preparation, not premise ideation. Treat every supplied premise as frozen.
Create the complete Illustrious and Klein prompt data for batch {batch_number}. Return ONLY one JSON array.

Each object must contain exactly:
id, category, illustrious_prompt, preserved_elements, risk_notes, klein_prompt, illustrious_seed, klein_seed.

Rules:
- Copy id and category exactly. Produce one object per supplied premise and no others.
- Preserve the premise's non-graphic sensual tension, composition, strategic censorship, character identity,
  visible trigger/reaction/consequence, dominant hook, and animation potential.
- Translate invisible meaning into concrete visible relationships. One dominant visual idea and one primary action.
- Do not turn the scene into a glamour shot, generic fanart, static pose, or cinematic action spectacle.
- Those anti-patterns belong in risk_notes. Do not insert negative commands such as 'no glamour pose' into
  illustrious_prompt. Never use physical camera/lens/photographer/filming language; use viewpoint and framing.
- The Illustrious prompt is positive, concrete, tag-oriented and starts with identity anchors. Do not invent facts.
- The Klein prompt is preservation-first and concise. It must preserve the source image rather than reconstruct it.
- preserved_elements must list at least five scene-specific invariants. risk_notes must contain at least one risk.
- Choose unique non-negative integer seeds. All characters are fictional adults. Visible output remains non-graphic.

LOCAL CHARACTER PROFILE (factual source):
{json.dumps(profile, ensure_ascii=False, indent=2)}

EROTIC SUGGESTIVE GUIDE (intent-preservation rubric; do not use it to rewrite premises):
{erotic_guide}

ILLUSTRIOUS TRANSLATION GUIDE (prompt construction authority):
{illustrious_guide}

KLEIN REFINEMENT GUIDE (preservation authority):
{klein_guide}

FROZEN PREMISES:
{json.dumps(source, ensure_ascii=False, indent=2)}
"""


def comfy_idle(base_url: str = "http://127.0.0.1:8188") -> dict[str, Any]:
    import urllib.request

    with urllib.request.urlopen(f"{base_url}/queue", timeout=15) as response:
        queue = json.loads(response.read().decode("utf-8"))
    running = len(queue.get("queue_running", []))
    pending = len(queue.get("queue_pending", []))
    return {"idle": running == 0 and pending == 0, "running": running, "pending": pending}


def main() -> int:
    raise RuntimeError("Legacy combined workflow validation is disabled; use the isolated production pipeline.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--erotic-guide", type=Path, default=DEFAULT_EROTIC_GUIDE)
    parser.add_argument("--dataset-id", default="render_validation_001_master_full_001")
    parser.add_argument("--batch-id", default="render_validation_001_master_full_001")
    parser.add_argument("--model", default="qwen3.8-27b-uncensored")
    parser.add_argument("--lm-studio-url", default="http://127.0.0.1:1234")
    args = parser.parse_args()

    source = read_jsonl(args.source.resolve())
    if len(source) != 12:
        raise ValueError(f"Expected the selected 12-premise set, got {len(source)}")
    run_dir = args.run_dir.resolve()
    dataset_path = PROMPTS_ROOT / f"{args.dataset_id}.jsonl"
    batch_dir = KLEIN_BATCH_RUNS_ROOT / args.batch_id
    for target in (run_dir, dataset_path, batch_dir):
        if target.exists():
            raise FileExistsError(f"Refusing to overwrite existing target: {target}")
    raw_dir = run_dir / "raw_master"
    raw_dir.mkdir(parents=True)

    erotic_text = args.erotic_guide.resolve().read_text(encoding="utf-8").strip()
    illustrious_text = ILLUSTRIOUS_GUIDE.read_text(encoding="utf-8").strip()
    klein_text = KLEIN_GUIDE.read_text(encoding="utf-8").strip()
    profile = character_profile()
    state: dict[str, Any] = {
        "schema_version": 1, "status": "master_authoring", "started_at": utc_now(),
        "model": args.model, "source": str(args.source.resolve()), "count": len(source),
        "openai_used": False, "work_used": False, "worker_used": False,
        "guides": {
            "erotic_v2": {"path": str(args.erotic_guide.resolve()), "sha256": sha256_text(erotic_text)},
            "illustrious_v1": {"path": str(ILLUSTRIOUS_GUIDE), "sha256": sha256_text(illustrious_text)},
            "klein_v1": {"path": str(KLEIN_GUIDE), "sha256": sha256_text(klein_text)},
        },
    }
    write_json_new(run_dir / "state.json", state)

    controller = LMStudioController()
    controller.ensure_loaded("master")
    client = LocalLMStudio(args.lm_studio_url, args.model, 900, 2, 0)
    master_rows: list[dict[str, Any]] = []
    for offset in range(0, len(source), 4):
        batch = source[offset:offset + 4]
        number = offset // 4 + 1

        def validator(content: str, expected: list[dict[str, Any]] = batch) -> list[dict[str, Any]]:
            return validate_master_batch(parse_json_response(content), expected)

        translated = client.generate_text(
            master_prompt(batch, erotic_text, illustrious_text, klein_text, profile, number),
            raw_dir, f"translation_batch_{number:02d}", temperature=0.2,
            max_output_tokens=7000, validator=validator,
        )
        master_rows.extend(translated)
        print(json.dumps({"event": "master_batch_complete", "batch": number, "records": len(translated)}), flush=True)

    seeds = [row[field] for row in master_rows for field in ("illustrious_seed", "klein_seed")]
    if len(seeds) != len(set(seeds)):
        raise ValueError("Master repeated one or more seeds across batches")

    translation_rows = []
    render_rows = []
    source_by_id = {row["id"]: row for row in source}
    for row in master_rows:
        premise = source_by_id[row["id"]]["premise"]
        translation_rows.append({
            "id": row["id"], "category": row["category"], "original_premise": premise,
            "illustrious_prompt": row["illustrious_prompt"],
            "preserved_elements": row["preserved_elements"], "risk_notes": row["risk_notes"],
        })
        render_rows.append({
            "id": row["id"], "character": "2B", "category": row["category"], "premise": premise,
            "illustrious_prompt": row["illustrious_prompt"], "klein_prompt": row["klein_prompt"],
            "illustrious_seed": row["illustrious_seed"], "klein_seed": row["klein_seed"],
        })
    write_jsonl_new(run_dir / "illustrious_prompts.jsonl", translation_rows)
    write_jsonl_new(run_dir / "master_records.jsonl", master_rows)
    write_jsonl_new(dataset_path, render_rows)
    load_dataset(dataset_path, take=None)

    validate_command = [
        sys.executable, str(RUNNER), "--workflow", str(WORKFLOW), "--dataset", str(dataset_path),
        "--expected-count", str(len(render_rows)), "--batch-id", args.batch_id, "--validate-only",
    ]
    subprocess.run(validate_command, cwd=ADA_ROOT, check=True)
    state.update(status="rendering", dataset=str(dataset_path), batch_id=args.batch_id, master_records=len(master_rows))
    (run_dir / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    controller.prepare_for_comfy(comfy_idle)
    try:
        render_command = [
            sys.executable, str(RUNNER), "--workflow", str(WORKFLOW), "--dataset", str(dataset_path),
            "--expected-count", str(len(render_rows)), "--batch-id", args.batch_id, "--progress-every", "1",
        ]
        subprocess.run(render_command, cwd=ADA_ROOT, check=True)
    finally:
        controller.ensure_loaded("master")

    manifest_path = batch_dir / "manifest.json"
    gallery_path = batch_dir / "gallery.html"
    subprocess.run([
        sys.executable, str(GALLERY), "--manifest", str(manifest_path),
        "--comfy-output", str(COMFYUI_ROOT / "output"), "--output", str(gallery_path),
    ], cwd=ADA_ROOT, check=True)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    render_by_id = {row["id"]: row for row in render_rows}
    reviews: list[dict[str, Any]] = []
    try:
        for entry in manifest["records"]:
            ill = entry["illustrious"][0]
            klein = entry["klein"][0]
            compare = entry["compare"][0]
            def image_path(descriptor: dict[str, Any]) -> Path:
                return COMFYUI_ROOT / "output" / descriptor.get("subfolder", "") / descriptor["filename"]
            record = render_by_id[entry["id"]]
            review = review_master_image(
                image_path(klein), model=args.model, illustrious_image=image_path(ill),
                comparison_image=image_path(compare), context={
                    "character": "2B", "version": "NieR:Automata", "category": record["category"],
                    "premise": record["premise"], "illustrious_prompt": record["illustrious_prompt"],
                    "klein_prompt": record["klein_prompt"],
                }, ttl_seconds=900, diagnostic_dir=run_dir / "review_diagnostics" / entry["id"],
            )
            reviews.append({"id": entry["id"], **review})
            print(json.dumps({"event": "master_review_complete", "id": entry["id"], "verdict": review["verdict"]}), flush=True)
    except Exception as exc:
        state.update(
            status="review_failed", manifest=str(manifest_path), gallery=str(gallery_path),
            review_completed=len(reviews), comfyui_used=True,
            error={"component": "master_visual_review", "type": type(exc).__name__, "message": str(exc)},
        )
        (run_dir / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if reviews:
            write_json_new(run_dir / "master_visual_review_partial.json", reviews)
        raise
    write_json_new(run_dir / "master_visual_review.json", reviews)

    state.update(
        status="complete", completed_at=utc_now(), manifest=str(manifest_path), gallery=str(gallery_path),
        review=str(run_dir / "master_visual_review.json"), comfyui_used=True,
    )
    (run_dir / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"event": "complete", "run_dir": str(run_dir), "gallery": str(gallery_path)}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
