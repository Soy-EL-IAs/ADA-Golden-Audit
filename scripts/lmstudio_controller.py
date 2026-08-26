#!/usr/bin/env python3
"""Deterministic LM Studio model/VRAM control for the local pipeline.

This module deliberately performs no work at import time.  It uses LM Studio's
native v1 model-management endpoints when they are available; older servers
remain observable, but cannot be used for a VRAM-safe batch preflight.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

if __package__:
    from .ada_paths import CONFIG_ROOT, LMSTUDIO_BASE_URL
else:
    from ada_paths import CONFIG_ROOT, LMSTUDIO_BASE_URL


DEFAULT_CONFIG = CONFIG_ROOT / "orchestration.json"


class PipelineState(str, Enum):
    IDLE_CHAT = "IDLE_CHAT"
    PREPARING_BATCH = "PREPARING_BATCH"
    GENERATING = "GENERATING"
    REVIEWING = "REVIEWING"
    DEEP_REVIEW = "DEEP_REVIEW"
    WAITING = "WAITING"


@dataclass(frozen=True)
class RoleConfig:
    name: str
    model: str
    context_length: int | None = None
    eval_batch_size: int | None = None
    flash_attention: bool | None = None
    offload_kv_cache_to_gpu: bool | None = None
    ttl_seconds: int | None = None
    reasoning_budget: int | None = None
    mtp: bool | None = None


class LMStudioController:
    """Small, explicit controller. It never relies on TTL to free VRAM."""

    def __init__(self, config_path: Path = DEFAULT_CONFIG) -> None:
        self.config = json.loads(config_path.read_text(encoding="utf-8"))
        self.base_url = LMSTUDIO_BASE_URL
        self.token = os.environ.get(self.config.get("api_token_env", "LM_STUDIO_API_TOKEN"))
        self.state = PipelineState.IDLE_CHAT
        self._active_signature: tuple[str, int | None] | None = None
        self.last_unload_diagnostic: dict[str, Any] | None = None

    @property
    def enabled(self) -> bool:
        return os.environ.get("PIPELINE_ORCHESTRATION", "0") == "1"

    def role(self, name: str) -> RoleConfig:
        raw = self.config["models"][name]
        return RoleConfig(
            name=name,
            model=raw["model"],
            context_length=raw.get("context_length"),
            eval_batch_size=raw.get("eval_batch_size"),
            flash_attention=raw.get("flash_attention"),
            offload_kv_cache_to_gpu=raw.get("offload_kv_cache_to_gpu"),
            ttl_seconds=raw.get("ttl_seconds"),
            reasoning_budget=raw.get("reasoning_budget"),
            mtp=raw.get("mtp"),
        )

    def _request(self, path: str, method: str = "GET", payload: Any | None = None, timeout: int = 60) -> Any:
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = urllib.request.Request(f"{self.base_url}{path}", data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read().decode("utf-8")
                return json.loads(body) if body else {}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"LM Studio HTTP {exc.code} {path}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"LM Studio unavailable at {self.base_url}: {exc.reason}") from exc

    def list_models(self) -> dict[str, Any]:
        """Return v1 inventory; falls back to a read-only v0 inventory."""
        try:
            response = self._request("/api/v1/models")
            return {"api": "v1", "response": response, "loaded": self._loaded_instances(response)}
        except RuntimeError as v1_error:
            try:
                response = self._request("/api/v0/models")
            except RuntimeError:
                raise v1_error
            return {"api": "v0", "response": response, "loaded": self._loaded_instances(response)}

    @staticmethod
    def _loaded_instances(response: Any) -> list[dict[str, Any]]:
        # Native v1 returns model definitions with nested `loaded_instances`.
        # Preserve a small, normalized record so unload always receives the
        # instance id rather than the model key.
        candidates = response.get("data", response.get("models", response if isinstance(response, list) else [])) if isinstance(response, dict) else response
        if not isinstance(candidates, list):
            return []
        loaded: list[dict[str, Any]] = []
        for item in candidates:
            if not isinstance(item, dict):
                continue
            for instance in item.get("loaded_instances", []):
                if isinstance(instance, dict) and instance.get("id"):
                    loaded.append({"instance_id": instance["id"], "model": item.get("key"), "raw": instance})
            # Legacy v0 has a flat loaded/status record.
            if item.get("loaded") is True or item.get("status") == "loaded":
                loaded.append(item)
        return loaded

    def load(self, role_name: str) -> dict[str, Any]:
        role = self.role(role_name)
        payload: dict[str, Any] = {"model": role.model, "echo_load_config": True}
        if role.context_length is not None:
            payload["context_length"] = role.context_length
        if role.eval_batch_size is not None:
            payload["eval_batch_size"] = role.eval_batch_size
        if role.flash_attention is not None:
            payload["flash_attention"] = role.flash_attention
        if role.offload_kv_cache_to_gpu is not None:
            payload["offload_kv_cache_to_gpu"] = role.offload_kv_cache_to_gpu
        # LM Studio's documented /api/v1/models/load schema does not currently
        # accept physical_batch_size, parallel (desired as 1 for the worker), speculative_draft_mtp,
        # speculative_draft_max_tokens, speculative_draft_min_tokens or
        # speculative_draft_min_continue_probability. They remain recorded in
        # orchestration.json as the known-good target, but are intentionally not
        # sent until LM Studio exposes them in the public load API.
        # TTL is sent only with OpenAI-compatible inference requests (where LM
        # Studio documents it). The native v1 load endpoint does not document a
        # TTL field, so do not send an unsupported load option here.
        result = self._request("/api/v1/models/load", "POST", payload, timeout=300)
        return {"role": role_name, "model": role.model, "result": result}

    def ensure_loaded(self, role_name: str) -> dict[str, Any]:
        """Return an existing role instance or load it with configured settings."""
        role = self.role(role_name)
        signature = (role.model, role.context_length)
        if self._active_signature == signature:
            return {"role": role_name, "model": role.model, "already_loaded": True, "same_configuration": True}
        inventory = self.list_models()
        for instance in inventory["loaded"]:
            if instance.get("model") == role.model:
                return {"role": role_name, "model": role.model, "already_loaded": True}
        return self.load(role_name)

    def activate_role(self, role_name: str) -> dict[str, Any]:
        """Load a role with its own context window, replacing a shared model instance.

        Specialist roles may use the same model key as Master but must not
        silently inherit Master's larger context allocation.
        """
        role = self.role(role_name)
        signature = (role.model, role.context_length)
        if self._active_signature == signature:
            return {"role": role_name, "model": role.model, "already_loaded": True, "same_configuration": True}
        inventory = self.list_models()
        matching = [item for item in inventory["loaded"] if item.get("model") == role.model]
        if matching:
            configured = matching[0].get("raw", {}).get("config", {})
            if configured.get("context_length") == role.context_length:
                self._active_signature = signature
                return {"role": role_name, "model": role.model, "already_loaded": True, "same_configuration": True}
            for instance in matching:
                instance_id = instance.get("instance_id") or instance.get("id")
                if not instance_id:
                    raise RuntimeError(f"Loaded model without instance_id: {instance}")
                diagnostic = self.unload_instance(instance_id, loaded_before=inventory["response"])
                self.last_unload_diagnostic = diagnostic
                if not diagnostic["released"]:
                    raise TimeoutError(f"LM Studio instance remained loaded: {diagnostic}")
        result = self.load(role_name)
        self._active_signature = signature
        return result

    def unload_instance(self, instance_id: str, *, loaded_before: Any | None = None) -> dict[str, Any]:
        """Unload exactly one v1 loaded instance and wait for that id to vanish."""
        started = time.monotonic()
        before = loaded_before if loaded_before is not None else self.list_models()["response"]
        request = urllib.request.Request(
            f"{self.base_url}/api/v1/models/unload",
            data=json.dumps({"instance_id": instance_id}).encode(),
            headers={"Content-Type": "application/json"}, method="POST",
        )
        status: int | None = None
        response_body: Any = None
        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                status = response.status
                raw = response.read().decode()
                response_body = json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            status = exc.code
            response_body = exc.read().decode("utf-8", errors="replace")
            after = self.list_models()["response"]
            diagnostic = {"requested_unload_instance_id": instance_id, "unload_http_status": status, "unload_response": response_body, "loaded_instances_before": before, "loaded_instances_after": after, "unload_elapsed_seconds": round(time.monotonic()-started, 3), "released": False}
            self.last_unload_diagnostic = diagnostic
            return diagnostic
        settings = self.config["vram_release"]
        deadline = time.monotonic() + settings["timeout_seconds"]
        after: Any = None
        while True:
            inventory = self.list_models()
            after = inventory["response"]
            if not any(item.get("instance_id") == instance_id for item in inventory["loaded"]):
                break
            if time.monotonic() >= deadline: break
            time.sleep(settings["poll_seconds"])
        diagnostic = {"requested_unload_instance_id": instance_id, "unload_http_status": status, "unload_response": response_body, "loaded_instances_before": before, "loaded_instances_after": after, "unload_elapsed_seconds": round(time.monotonic()-started, 3), "released": not any(item.get("instance_id") == instance_id for item in self.list_models()["loaded"])}
        self.last_unload_diagnostic = diagnostic
        return diagnostic

    def unload_all(self) -> list[dict[str, Any]]:
        inventory = self.list_models()
        if inventory["api"] != "v1":
            raise RuntimeError("LM Studio v1 model API is required for deterministic unload_all")
        results: list[dict[str, Any]] = []
        for instance in inventory["loaded"]:
            instance_id = instance.get("instance_id") or instance.get("id")
            if not instance_id:
                raise RuntimeError(f"Loaded model without instance_id: {instance}")
            results.append(self._request("/api/v1/models/unload", "POST", {"instance_id": instance_id}))
        self._active_signature = None
        return results

    def unload_role(self, role_name: str) -> list[dict[str, Any]]:
        """Unload instances that unambiguously belong to one configured role."""
        role = self.role(role_name)
        inventory = self.list_models()
        if inventory["api"] != "v1":
            raise RuntimeError("LM Studio v1 model API is required for deterministic unload")
        results: list[dict[str, Any]] = []
        for instance in inventory["loaded"]:
            identity = str(instance.get("model") or instance.get("model_key") or instance.get("id") or "")
            if identity != role.model:
                continue
            instance_id = instance.get("instance_id") or instance.get("id")
            if not instance_id:
                raise RuntimeError(f"Loaded model without instance_id: {instance}")
            results.append(self._request("/api/v1/models/unload", "POST", {"instance_id": instance_id}))
        return results

    def wait_for_vram_release(self) -> dict[str, Any]:
        settings = self.config["vram_release"]
        deadline = time.monotonic() + settings["timeout_seconds"]
        while True:
            inventory = self.list_models()
            if not inventory["loaded"]:
                return {"released": True, "api": inventory["api"]}
            if time.monotonic() >= deadline:
                raise TimeoutError(f"LM Studio still reports loaded models: {inventory['loaded']}")
            time.sleep(settings["poll_seconds"])

    def wait_for_comfy_vram_release(self, comfy_status: Any) -> dict[str, Any]:
        settings = self.config["vram_release"]
        minimum_free_ratio = float(settings["comfy_min_free_ratio"])
        deadline = time.monotonic() + settings["timeout_seconds"]
        while True:
            status = comfy_status()
            total = status.get("vram_total")
            free = status.get("vram_free")
            free_ratio = (free / total) if isinstance(free, (int, float)) and isinstance(total, (int, float)) and total > 0 else None
            if status.get("idle") is True and free_ratio is not None and free_ratio >= minimum_free_ratio:
                return {"released": True, "free_ratio": free_ratio, "status": status}
            if time.monotonic() >= deadline:
                raise TimeoutError(f"ComfyUI VRAM was not released: {status}")
            time.sleep(settings["poll_seconds"])

    def prepare_for_lm(self, comfy_unload: Any, comfy_status: Any) -> dict[str, Any]:
        self.state = PipelineState.WAITING
        requested = comfy_unload()
        released = self.wait_for_comfy_vram_release(comfy_status)
        return {"unload": requested, "vram": released}

    @staticmethod
    def comfy_status(base_url: str) -> dict[str, Any]:
        def request_json(path: str) -> dict[str, Any]:
            request = urllib.request.Request(f"{base_url.rstrip('/')}{path}", headers={"Accept": "application/json"})
            with urllib.request.urlopen(request, timeout=30) as response:
                raw = response.read().decode("utf-8")
                value = json.loads(raw) if raw else {}
                return value if isinstance(value, dict) else {}

        queue = request_json("/queue")
        stats = request_json("/system_stats")
        devices = stats.get("devices", [])
        totals = [item.get("vram_total") for item in devices if isinstance(item, dict)]
        frees = [item.get("vram_free") for item in devices if isinstance(item, dict)]
        valid_totals = [value for value in totals if isinstance(value, (int, float))]
        valid_frees = [value for value in frees if isinstance(value, (int, float))]
        return {
            "idle": not queue.get("queue_running", []) and not queue.get("queue_pending", []),
            "running": len(queue.get("queue_running", [])),
            "pending": len(queue.get("queue_pending", [])),
            "vram_total": sum(valid_totals) if valid_totals else None,
            "vram_free": sum(valid_frees) if valid_frees else None,
        }

    def wait_for_comfyui_idle(self, base_url: str, timeout: int = 600) -> dict[str, Any]:
        import time
        start = time.time()
        while time.time() - start < timeout:
            status = self.comfy_status(base_url)
            if status["idle"]:
                return status
            time.sleep(5)
        raise RuntimeError(f"ComfyUI is busy and did not become idle within {timeout}s: {status}")

    def request_comfy_unload(self, base_url: str) -> dict[str, Any]:
        status = self.wait_for_comfyui_idle(base_url)
        payload = json.dumps({"unload_models": True, "free_memory": True}).encode("utf-8")
        request = urllib.request.Request(
            f"{base_url.rstrip('/')}/free", data=payload,
            headers={"Content-Type": "application/json"}, method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                raw = response.read().decode("utf-8")
                result = json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"ComfyUI HTTP {exc.code} /free: {detail}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"ComfyUI unavailable during /free: {exc.reason}") from exc
        return {"requested": True, "before": status, "response": result}

    def handoff_comfy_to_lm(self, base_url: str) -> dict[str, Any]:
        return self.prepare_for_lm(
            lambda: self.request_comfy_unload(base_url),
            lambda: self.comfy_status(base_url),
        )

    def prepare_for_comfy(self, comfy_status: Any) -> dict[str, Any]:
        self.state = PipelineState.PREPARING_BATCH
        try:
            unloaded = self.unload_all()
            released = self.wait_for_vram_release()
            status = comfy_status()
            if not status.get("idle"):
                raise RuntimeError(f"ComfyUI is busy after VRAM release: {status}")
            self.state = PipelineState.GENERATING
            return {"unloaded": unloaded, "vram": released, "comfy": status}
        except Exception:
            self.state = PipelineState.WAITING
            raise

    def begin_review(self, deep: bool = False) -> RoleConfig:
        self.unload_all()
        self.wait_for_vram_release()
        role = self.role("master" if deep else "worker")
        self.load(role.name)
        self.state = PipelineState.DEEP_REVIEW if deep else PipelineState.REVIEWING
        return role

    def finish_work(self) -> None:
        self.state = PipelineState.IDLE_CHAT
