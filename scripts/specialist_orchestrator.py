#!/usr/bin/env python3
"""Persistent orchestration core for ADA's phase-isolated specialist agents."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Protocol

if __package__:
    from .ada_run_state import AdaRunState
    from .agent_contracts import validate_contract, validate_visual_review
    from .specialist_agents import (
        SpecialistRequest, illustrious_request, klein_request, minimax_request, premise_request,
    )
else:
    from ada_run_state import AdaRunState
    from agent_contracts import validate_contract, validate_visual_review
    from specialist_agents import SpecialistRequest, illustrious_request, klein_request, minimax_request, premise_request


class SpecialistClient(Protocol):
    def execute(self, request: SpecialistRequest, *, raw_output: Path | None = None) -> dict[str, Any]: ...


def _clean_text_items(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _identity_tags(character_profile: dict[str, Any], premise: dict[str, Any]) -> list[str]:
    tags = _clean_text_items(character_profile.get("characteristics"))
    if not tags:
        tags = _clean_text_items(character_profile.get("physical_features"))
    if not tags:
        tags = _clean_text_items(premise.get("identity_elements"))
    clothing_state = premise.get("clothing_state")
    if isinstance(clothing_state, str) and clothing_state.strip():
        tags.append(clothing_state.strip())
    return tags


def _character_name(character_profile: dict[str, Any], premise: dict[str, Any]) -> str | None:
    for value in (character_profile.get("requested_character"), character_profile.get("name"), premise.get("character")):
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def build_deterministic_klein_prompt(*, character_name: str | None, identity_tags: list[str], defects: list[str]) -> str:
    tags = [tag.strip() for tag in identity_tags if isinstance(tag, str) and tag.strip()][:6]
    anchors = f", {', '.join(tags)}" if tags else ""
    parts = [
        "Create a realistic photo version of the source image.",
        (
            "Strictly preserve exact facial identity, facial proportions, expression, pose, framing, "
            f"hairstyle, outfit{anchors}."
        ),
        "Improve realism through skin texture, hair strands, realistic fabric and lighting only.",
        "Do not redesign the face or change the expression.",
    ]
    concrete_defects = [item.strip() for item in defects if isinstance(item, str) and item.strip()]
    if concrete_defects:
        parts.append(f"Correct only these observed defects: {'; '.join(concrete_defects)}.")
    return " ".join(parts)


class SpecialistOrchestrator:
    """Coordinate content specialists while code owns state, contracts and seeds."""

    def __init__(self, run_dir: Path, client: SpecialistClient) -> None:
        self.run = AdaRunState(run_dir)
        self.client = client

    def create(
        self, run_id: str, *, character: str, version: str | None, review_policy: str = "strict",
    ) -> dict[str, Any]:
        return self.run.create(
            run_id, character=character, version=version, pipeline="specialist_image_v1",
            review_policy=review_policy,
        )

    def create_premise(
        self, *, task: str, character_profile: dict[str, Any], viral_guide: str,
        diversity_history: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        state = self.run.read()
        self._require_stage(state, "CREATED")
        request = premise_request(
            character=state["character"], version=state.get("version"), character_profile=character_profile,
            viral_guide=viral_guide, task=task, diversity_history=diversity_history,
        )
        attempt = state.get("retries_CREATED", 0) + 1
        output = self.client.execute(request, raw_output=self.run.run_dir / "raw" / f"premise_attempt_{attempt:02d}.json")
        premise = {
            "id": f"{state['character'].lower().replace(' ', '_')}_{state['run_id']}",
            "category": output["category"], "premise": output["premise"],
            "identity_elements": output.get("identity_elements", []),
            "canonical_outfit": output.get("canonical_outfit", []),
            "scene_requirements": output.get("scene_requirements", []),
            "risk_notes": output["risk_notes"],
        }
        validate_contract("premise_spec_v1", premise)
        self._write_json_artifact("premise_spec.json", premise)
        self.run.allocate_seeds([premise["id"]])
        self.run.advance("PREMISES_READY", artifacts={"premise_spec": "premise_spec.json"})
        return premise

    def compile_illustrious(
        self, *, character_profile: dict[str, Any], illustrious_guide: str,
        stage_render_plan: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        state = self.run.read()
        self._require_stage(state, "PREMISES_READY")
        premise = self._read_artifact(state, "premise_spec")

        attempt = state.get("retries_PREMISES_READY", 0) + 1
        previous_review = None
        if attempt > 1:
            try:
                # Prioritize final review if it exists and caused the retry
                previous_review = self._read_artifact(state, "final_review")
            except Exception:
                try:
                    previous_review = self._read_artifact(state, "illustrious_review")
                except Exception:
                    pass

        request = illustrious_request(
            premise_spec=premise, character_profile=character_profile, illustrious_guide=illustrious_guide,
            previous_review=previous_review, stage_render_plan=stage_render_plan,
        )
        attempt = state.get("retries_PREMISES_READY", 0) + 1
        output = self.client.execute(request, raw_output=self.run.run_dir / "raw" / f"illustrious_attempt_{attempt:02d}.json")
        prompt = output["prompt"].strip()
        identity_source = stage_render_plan.get("identity", {}) if stage_render_plan else character_profile
        identities = [
            value.strip() for value in (
                identity_source.get("display_name") or character_profile.get("requested_character") or character_profile.get("name"),
                identity_source.get("canonical_tag") or character_profile.get("matched_tag") or character_profile.get("canonical_tag"),
            )
            if isinstance(value, str) and value.strip() and value.casefold() not in prompt.casefold()
        ]
        if identities:
            prompt = f"{', '.join(identities)}, {prompt}"
        result = {
            "id": premise["id"], "illustrious_prompt": prompt,
            "resolved_risks": premise["risk_notes"],
        }
        validate_contract("illustrious_result_v1", result)
        self._write_json_artifact("illustrious_result.json", result)
        self.run.advance("ILLUSTRIOUS_PROMPTS_READY", artifacts={"illustrious_result": "illustrious_result.json"})
        return result

    def record_illustrious_render(self, image_path: Path) -> dict[str, Any]:
        state = self.run.read()
        self._require_stage(state, "ILLUSTRIOUS_PROMPTS_READY")
        if not image_path.is_file():
            raise FileNotFoundError(image_path)
        return self.run.advance("ILLUSTRIOUS_RENDERED", artifacts={"illustrious_image": str(image_path.resolve())})

    def record_illustrious_review(self, review: dict[str, Any]) -> dict[str, Any]:
        state = self.run.read()
        self._require_stage(state, "ILLUSTRIOUS_RENDERED")
        validate_visual_review(review)
        premise = self._read_artifact(state, "premise_spec")
        if review["id"] != premise["id"] or review["stage"] != "illustrious":
            raise ValueError("Visual review does not match the Illustrious artifact")
        self._write_json_artifact("illustrious_review.json", review)
        return self.run.advance("ILLUSTRIOUS_REVIEWED", artifacts={"illustrious_review": "illustrious_review.json"})

    def record_review_failure(
        self, exc: Exception, *, stage: str, diagnostic_dir: Path | None = None,
    ) -> dict[str, Any]:
        """Keep the render stage resumable and block every downstream transition."""
        state = self.run.read()
        expected = "ILLUSTRIOUS_RENDERED" if stage == "illustrious" else "KLEIN_RENDERED" if stage == "klein" else None
        if expected is None:
            raise ValueError("review failure stage must be illustrious or klein")
        self._require_stage(state, expected)
        artifacts = None
        if diagnostic_dir is not None:
            artifacts = {f"{stage}_review_diagnostics": str(diagnostic_dir.resolve())}
        return self.run.record_recoverable_failure(
            exc, component=f"{stage}_visual_review", artifacts=artifacts,
        )

    def compile_klein_legacy_agent(self, *, klein_guide: str) -> dict[str, Any]:
        """Legacy 27B Klein Agent path."""
        state = self.run.read()
        self._require_stage(state, "ILLUSTRIOUS_REVIEWED")
        premise = self._read_artifact(state, "premise_spec")
        illustrious = self._read_artifact(state, "illustrious_result")
        review = self._read_artifact(state, "illustrious_review")
        image_path = state.get("artifacts", {}).get("illustrious_image")
        if not isinstance(image_path, str) or not image_path:
            raise ValueError("Klein Agent requires the persisted Illustrious image artifact")
        request = klein_request(
            premise_spec=premise, illustrious_result=illustrious, visual_review=review,
            illustrious_image=image_path, klein_guide=klein_guide,
        )
        attempt = state.get("retries_ILLUSTRIOUS_REVIEWED", 0) + 1
        output = self.client.execute(request, raw_output=self.run.run_dir / "raw" / f"klein_attempt_{attempt:02d}.json")
        result = {
            "id": premise["id"], "klein_prompt": output["prompt"],
            "preserve": review.get("identity_ok") or premise.get("identity_elements", []),
            "correct": list(review["defects"]) + list(review["drift"]),
        }
        validate_contract("klein_result_v1", result)
        self._write_json_artifact("klein_result.json", result)
        self.run.advance("KLEIN_PROMPTS_READY", artifacts={"klein_result": "klein_result.json"})
        return result

    def compile_klein_deterministic(
        self, *, character_profile: dict[str, Any], stage_render_plan: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """New deterministic compiled Klein prompt without loading a 27B LLM."""
        state = self.run.read()
        self._require_stage(state, "ILLUSTRIOUS_REVIEWED")
        premise = self._read_artifact(state, "premise_spec")

        attempt = state.get("retries_ILLUSTRIOUS_REVIEWED", 0) + 1
        review = self._read_artifact(state, "illustrious_review")
        if attempt > 1:
            try:
                review = self._read_artifact(state, "final_review")
            except Exception:
                pass

        if stage_render_plan is not None:
            validate_contract("stage_render_plan_v1", stage_render_plan)
            if stage_render_plan["stage"] != "klein":
                raise ValueError("Klein compiler requires a Klein Stage Render Plan")
            plan_identity = stage_render_plan["identity"]
            character_name = plan_identity["display_name"]
            identity_tags = plan_identity["anchors"]
            defects = stage_render_plan["correction_delta"]["instructions"]
        else:
            character_name = _character_name(character_profile, premise)
            identity_tags = _identity_tags(character_profile, premise)
            defects = list(review.get("defects", [])) + list(review.get("drift", []))
        prompt = build_deterministic_klein_prompt(
            character_name=character_name,
            identity_tags=identity_tags,
            defects=defects,
        )

        result = {
            "id": premise["id"],
            "klein_prompt": prompt,
            "preserve": identity_tags,
            "correct": defects,
        }
        validate_contract("klein_result_v1", result)
        self._write_json_artifact("klein_result.json", result)
        self.run.advance("KLEIN_PROMPTS_READY", artifacts={"klein_result": "klein_result.json"})
        return result

    def record_klein_render(self, image_path: Path) -> dict[str, Any]:
        state = self.run.read()
        self._require_stage(state, "KLEIN_PROMPTS_READY")
        if not image_path.is_file():
            raise FileNotFoundError(image_path)
        return self.run.advance("KLEIN_RENDERED", artifacts={"klein_image": str(image_path.resolve())})

    def record_final_review(self, review: dict[str, Any]) -> dict[str, Any]:
        state = self.run.read()
        self._require_stage(state, "KLEIN_RENDERED")
        validate_visual_review(review)
        premise = self._read_artifact(state, "premise_spec")
        if review["id"] != premise["id"] or review["stage"] != "klein":
            raise ValueError("Visual review does not match the Klein artifact")
        self._write_json_artifact("final_review.json", review)
        return self.run.advance("FINAL_REVIEWED", artifacts={"final_review": "final_review.json"})

    def complete(self) -> dict[str, Any]:
        state = self.run.read()
        self._require_stage(state, "FINAL_REVIEWED")
        return self.run.advance("COMPLETE")

    def compile_minimax(
        self, *, duration_seconds: int, workflow_mode: str, minimax_guide: str,
        audio_dialogue: str | None = None,
    ) -> dict[str, Any]:
        state = self.run.read()
        if state["stage"] not in {"FINAL_REVIEWED", "COMPLETE"}:
            raise ValueError("MiniMax Agent requires an approved final image")
        premise = self._read_artifact(state, "premise_spec")
        request = minimax_request(
            identifier=premise["id"], premise_spec=premise, approved_image=state["artifacts"]["klein_image"],
            duration_seconds=duration_seconds, workflow_mode=workflow_mode, minimax_guide=minimax_guide,
            audio_dialogue=audio_dialogue,
        )
        attempt = state.get("retries_KLEIN_REVIEWED", 0) + 1
        output = self.client.execute(request, raw_output=self.run.run_dir / "raw" / f"minimax_attempt_{attempt:02d}.json")
        result = {
            "id": premise["id"], "workflow_mode": workflow_mode,
            "duration_seconds": duration_seconds, "video_prompt": output["video_prompt"],
            "continuity_constraints": premise.get("identity_elements", []) + premise.get("canonical_outfit", []),
        }
        validate_contract("minimax_result_v1", result)
        self._write_json_artifact("minimax_result.json", result)
        self.run.attach_artifact("minimax_result", "minimax_result.json")
        return result

    @staticmethod
    def _require_stage(state: dict[str, Any], expected: str) -> None:
        if state["stage"] != expected:
            raise ValueError(f"Expected ADA stage {expected}, got {state['stage']}")

    def _read_artifact(self, state: dict[str, Any], name: str) -> dict[str, Any]:
        relative = state.get("artifacts", {}).get(name)
        if not isinstance(relative, str):
            raise ValueError(f"ADA run has no {name} artifact")
        path = Path(relative)
        if not path.is_absolute():
            path = self.run.run_dir / path
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError(f"ADA artifact is not an object: {path}")
        return value

    def _write_json_artifact(self, filename: str, value: dict[str, Any]) -> Path:
        path = self.run.run_dir / filename
        with path.open("w", encoding="utf-8") as output:
            json.dump(value, output, ensure_ascii=False, indent=2)
            output.write("\n")
        return path
