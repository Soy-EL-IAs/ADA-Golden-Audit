#!/usr/bin/env python3
"""Phase-isolated specialist prompts for ADA's shared local Master model."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

if __package__:
    from .agent_contracts import load_contract, validate_contract, validate_visual_review
else:
    from agent_contracts import load_contract, validate_contract, validate_visual_review


RUNTIME_GUIDE_ROOT = Path(__file__).resolve().parents[1] / "config" / "runtime_instructions"


def _runtime_guide(name: str) -> str:
    return (RUNTIME_GUIDE_ROOT / name).read_text(encoding="utf-8").strip()


@dataclass(frozen=True)
class SpecialistRequest:
    role: str
    contract: str
    system_prompt: str
    task_prompt: str
    max_output_tokens: int = 1000

    @property
    def schema(self) -> dict[str, Any]:
        return load_contract(self.contract)

    def validate(self, value: Any) -> Any:
        return validate_contract(self.contract, value)


class LMStudioSpecialistClient:
    """Execute one fresh, schema-constrained LM Studio call per specialist role."""

    def __init__(self, *, base_url: str, model: str, context_length: int | None = None, timeout_seconds: int = 900) -> None:
        if not base_url.startswith(("http://127.0.0.1", "http://localhost")):
            raise ValueError("ADA specialist calls must use loopback LM Studio")
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.context_length = context_length
        self.timeout_seconds = timeout_seconds
        self.token = os.environ.get("LM_STUDIO_API_TOKEN", "").strip()

    @classmethod
    def for_role(cls, controller: Any, role_name: str, *, timeout_seconds: int = 900) -> "LMStudioSpecialistClient":
        """Activate the role-specific context window before a specialist call."""
        controller.activate_role(role_name)
        role = controller.role(role_name)
        return cls(
            base_url=controller.base_url, model=role.model,
            context_length=role.context_length, timeout_seconds=timeout_seconds,
        )

    def execute(self, request: SpecialistRequest, *, raw_output: Path | None = None) -> dict[str, Any]:
        if self.model != "qwen/qwen3-vl-8b":
            return self._execute_native_primary(request, raw_output=raw_output)
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.task_prompt},
            ],
            "temperature": 0.1,
            "max_tokens": request.max_output_tokens,
            "response_format": {
                "type": "json_schema",
                "json_schema": {"name": request.contract, "strict": True, "schema": request.schema},
            },
        }
        # The vision worker rejects this parameter, while Master accepts it and
        # otherwise spends the whole completion budget in hidden reasoning.
        if self.model != "qwen/qwen3-vl-8b":
            payload["reasoning"] = "off"
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        http_request = urllib.request.Request(
            f"{self.base_url}/v1/chat/completions",
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        started = time.perf_counter()
        try:
            with urllib.request.urlopen(http_request, timeout=self.timeout_seconds) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"LM Studio specialist HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"LM Studio specialist unavailable: {exc.reason}") from exc
        if raw_output is not None:
            raw_output.parent.mkdir(parents=True, exist_ok=True)
            with raw_output.open("x", encoding="utf-8") as output:
                json.dump(body, output, ensure_ascii=False, indent=2)
                output.write("\n")
            self._write_telemetry(raw_output, request, body, time.perf_counter() - started, transport="openai")
        try:
            content = body["choices"][0]["message"]["content"]
            value = json.loads(content)
            request.validate(value)
            return value
        except (KeyError, IndexError, TypeError, json.JSONDecodeError, ValueError) as first_error:
            # Native chat is a bounded recovery path for models that consume
            # the OpenAI completion budget in reasoning and return empty content.
            native_payload = {
                "model": self.model,
                "input": [{"type": "text", "content": (
                    request.system_prompt + "\nReturn only one JSON object matching the contract; no reasoning text.\n" + request.task_prompt
                )}],
                "temperature": 0.1,
                "max_output_tokens": request.max_output_tokens,
                "store": False,
            }
            if self.model != "qwen/qwen3-vl-8b":
                native_payload["reasoning"] = "off"
            native_request = urllib.request.Request(
                f"{self.base_url}/api/v1/chat",
                data=json.dumps(native_payload, ensure_ascii=False).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            try:
                with urllib.request.urlopen(native_request, timeout=self.timeout_seconds) as response:
                    native_body = json.loads(response.read().decode("utf-8"))
                if raw_output is not None:
                    native_path = raw_output.with_name(raw_output.stem + "_native_fallback" + raw_output.suffix)
                    with native_path.open("x", encoding="utf-8") as output:
                        json.dump(native_body, output, ensure_ascii=False, indent=2)
                        output.write("\n")
                    self._write_telemetry(raw_output.with_name(raw_output.stem + "_native_fallback" + raw_output.suffix), request, native_body, time.perf_counter() - started, transport="native")
                native_text = ""
                for item in native_body.get("output", []):
                    if isinstance(item, dict) and item.get("type") == "message" and isinstance(item.get("content"), str):
                        native_text = item["content"].strip()
                        if native_text:
                            break
                start = native_text.find("{")
                if start < 0:
                    raise ValueError("native response contains no JSON object")
                native_value, _ = json.JSONDecoder().raw_decode(native_text[start:])
                request.validate(native_value)
                return native_value
            except (urllib.error.HTTPError, urllib.error.URLError, KeyError, TypeError, ValueError, json.JSONDecodeError) as native_error:
                raise ValueError(f"LM Studio returned no valid {request.contract} JSON after OpenAI and native transports: {first_error}; {native_error}") from native_error

    def _execute_native_primary(self, request: SpecialistRequest, *, raw_output: Path | None = None) -> dict[str, Any]:
        started = time.perf_counter()
        headers = {"Content-Type": "application/json"}
        if self.token: headers["Authorization"] = f"Bearer {self.token}"
        payload = {"model": self.model, "input": [{"type": "text", "content": request.system_prompt + "\n" + request.task_prompt}], "temperature": 0.1, "max_output_tokens": request.max_output_tokens, "reasoning": "off", "store": False}
        req = urllib.request.Request(f"{self.base_url}/api/v1/chat", data=json.dumps(payload, ensure_ascii=False).encode(), headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_seconds) as response: body = json.loads(response.read().decode())
            if raw_output is not None:
                raw_output.parent.mkdir(parents=True, exist_ok=True)
                with raw_output.open("x", encoding="utf-8") as output: json.dump(body, output, ensure_ascii=False, indent=2); output.write("\n")
                self._write_telemetry(raw_output, request, body, time.perf_counter()-started, transport="native")
            content = next(item.get("content", "") for item in body.get("output", []) if item.get("type") == "message")
            start = content.find("{")
            if start < 0: raise ValueError("native response contains no JSON object")
            value, _ = json.JSONDecoder().raw_decode(content[start:]); request.validate(value); return value
        except (urllib.error.HTTPError, urllib.error.URLError, KeyError, StopIteration, TypeError, ValueError, json.JSONDecodeError) as native_error:
            return self._execute_openai_fallback(request, raw_output=raw_output, native_error=native_error)

    def _execute_openai_fallback(self, request: SpecialistRequest, *, raw_output: Path | None, native_error: Exception) -> dict[str, Any]:
        started = time.perf_counter(); headers = {"Content-Type": "application/json"}
        if self.token: headers["Authorization"] = f"Bearer {self.token}"
        payload = {"model": self.model, "messages": [{"role":"system","content":request.system_prompt},{"role":"user","content":request.task_prompt}], "temperature": 0.1, "max_tokens": request.max_output_tokens, "reasoning": "off", "response_format": {"type":"json_schema","json_schema":{"name":request.contract,"strict":True,"schema":request.schema}}}
        req = urllib.request.Request(f"{self.base_url}/v1/chat/completions", data=json.dumps(payload, ensure_ascii=False).encode(), headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_seconds) as response: body=json.loads(response.read().decode())
            if raw_output is not None:
                path=raw_output.with_name(raw_output.stem+"_openai_fallback"+raw_output.suffix)
                with path.open("x", encoding="utf-8") as output: json.dump(body, output, ensure_ascii=False, indent=2); output.write("\n")
                self._write_telemetry(path, request, body, time.perf_counter()-started, transport="openai_fallback")
            value=json.loads(body["choices"][0]["message"]["content"]); request.validate(value); return value
        except (urllib.error.HTTPError, urllib.error.URLError, KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError) as openai_error:
            raise ValueError(f"LM Studio returned no valid {request.contract} JSON after native and OpenAI fallback: {native_error}; {openai_error}") from openai_error

    def _write_telemetry(self, raw_output: Path, request: SpecialistRequest, body: dict[str, Any], latency: float, *, transport: str) -> None:
        """Persist the one-call measurement needed by the upcoming mini E2E."""
        usage = body.get("usage", {}) if isinstance(body, dict) else {}
        stats = body.get("stats", {}) if isinstance(body, dict) else {}
        details = usage.get("completion_tokens_details", {}) if isinstance(usage, dict) else {}
        choices = body.get("choices", []) if isinstance(body, dict) else []
        finish_reason = choices[0].get("finish_reason") if choices and isinstance(choices[0], dict) else body.get("stop_reason")
        telemetry = {
            "model": self.model, "agent": request.role,
            "prompt_tokens": usage.get("prompt_tokens", stats.get("input_tokens")), "completion_tokens": usage.get("completion_tokens", stats.get("total_output_tokens")),
            "reasoning_tokens": details.get("reasoning_tokens", stats.get("reasoning_output_tokens", 0)), "context_length": self.context_length,
            "latency_seconds": round(latency, 3), "finish_reason": finish_reason, "transport": transport,
            "time_to_first_token_seconds": (body.get("stats", {}) or {}).get("time_to_first_token_seconds") if isinstance(body, dict) else None,
        }
        path = raw_output.with_name(raw_output.stem + "_telemetry.json")
        with path.open("x", encoding="utf-8") as output:
            json.dump(telemetry, output, ensure_ascii=False, indent=2)
            output.write("\n")


def premise_request(
    *, character: str, version: str | None, character_profile: dict[str, Any],
    viral_guide: str, task: str, diversity_history: list[dict[str, Any]] | None = None,
) -> SpecialistRequest:
    system = (
        "You are ADA's Premise Agent. Create only one structured premise. "
        "Do not write Illustrious, Klein, MiniMax, seeds, workflow settings, or render instructions. "
        "The character profile is the factual identity source. Return only JSON matching the supplied contract."
    )
    payload = {
        "character": character,
        "version": version,
        "character_profile": character_profile,
        "diversity_history": diversity_history or [],
        "user_task": task,
        "runtime_instruction": _runtime_guide("premise_runtime_v1.md"),
    }
    return SpecialistRequest("premise", "premise_output_v1", system, json.dumps(payload, ensure_ascii=False, indent=2), 1000)


def illustrious_request(
    *, premise_spec: dict[str, Any], character_profile: dict[str, Any], illustrious_guide: str,
    previous_review: dict[str, Any] | None = None,
    stage_render_plan: dict[str, Any] | None = None,
) -> SpecialistRequest:
    validate_contract("premise_spec_v1", premise_spec)
    system = (
        "You are ADA's Illustrious Agent. Translate an approved premise into concrete visible information. "
        "Do not rewrite the premise, create seeds, write a Klein prompt, discuss MiniMax, or add physical camera language. "
        "Use risk_notes actively: resolve each ambiguity through positive visual construction. Return only contract JSON."
    )
    if stage_render_plan is not None:
        validate_contract("stage_render_plan_v1", stage_render_plan)
        if stage_render_plan["stage"] != "illustrious":
            raise ValueError("Illustrious compiler requires an Illustrious Stage Render Plan")
        payload = {
            "stage_render_plan": stage_render_plan,
            "runtime_instruction": _runtime_guide("illustrious_runtime_v1.md"),
        }
    else:
        payload = {
            "premise_spec": premise_spec,
            "character_profile": character_profile,
            "runtime_instruction": _runtime_guide("illustrious_runtime_v1.md"),
        }
    if previous_review and stage_render_plan is None:
        payload["previous_rejection_feedback"] = {
            "defects_to_fix": previous_review.get("defects", []),
            "drift_to_fix": previous_review.get("drift", []),
            "instruction": "Your previous attempt failed visual review for the reasons above. Rewrite the prompt to correct these specific visible structural/rendering failures. CRITICAL: If the failure is about canonical outfit elements missing, but the premise/scene_requirements explicitly requested them removed, DO NOT restore them. Only fix true identity failures and missing explicit scene requirements."
        }
    return SpecialistRequest("illustrious", "illustrious_output_v1", system, json.dumps(payload, ensure_ascii=False, indent=2), 700)


def klein_request(
    *, premise_spec: dict[str, Any], illustrious_result: dict[str, Any],
    visual_review: dict[str, Any], illustrious_image: str, klein_guide: str,
) -> SpecialistRequest:
    validate_contract("premise_spec_v1", premise_spec)
    validate_contract("illustrious_result_v1", illustrious_result)
    validate_visual_review(visual_review)
    if visual_review["stage"] != "illustrious":
        raise ValueError("Klein Agent requires an Illustrious-stage visual review")
    system = (
        "You are ADA's Klein Agent. The rendered Illustrious image and its visual review are the source of truth. "
        "Preserve correct identity, pose, framing, composition, clothing state, obstruction, and hook. "
        "Correct only observed defects or drift. Do not reconstruct the premise, create seeds, or discuss MiniMax. "
        "Return only JSON matching the supplied contract."
    )
    payload = {
        "premise": premise_spec["premise"],
        "identity_elements": premise_spec.get("identity_elements", []),
        "canonical_outfit": premise_spec.get("canonical_outfit", []),
        "scene_requirements": premise_spec.get("scene_requirements", []),
        "risk_notes": premise_spec["risk_notes"],
        "illustrious_prompt": illustrious_result["illustrious_prompt"],
        "illustrious_image": illustrious_image,
        "illustrious_visual_review": visual_review,
        "runtime_instruction": _runtime_guide("klein_runtime_v1.md"),
    }
    return SpecialistRequest("klein", "klein_output_v1", system, json.dumps(payload, ensure_ascii=False, indent=2), 500)


def minimax_request(
    *, identifier: str, premise_spec: dict[str, Any], approved_image: str,
    duration_seconds: int, workflow_mode: str, minimax_guide: str,
    audio_dialogue: str | None = None,
) -> SpecialistRequest:
    validate_contract("premise_spec_v1", premise_spec)
    system = (
        "You are ADA's MiniMax Agent. Work only on temporal continuity and video prompting from one approved image. "
        "Do not create image prompts, change identity, or redesign the approved first frame. Return only contract JSON."
    )
    payload = {
        "premise": premise_spec["premise"],
        "approved_image": approved_image,
        "duration_seconds": duration_seconds,
        "workflow_mode": workflow_mode,
        "audio_dialogue": audio_dialogue,
        "runtime_instruction": _runtime_guide("minimax_runtime_v1.md"),
    }
    return SpecialistRequest("minimax", "minimax_output_v1", system, json.dumps(payload, ensure_ascii=False, indent=2), 1800)
