#!/usr/bin/env python3
"""Small persistent run-state layer for ADA's specialist pipeline."""

from __future__ import annotations

import json
import os
import secrets
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGES = (
    "CREATED",
    "PREMISES_READY",
    "ILLUSTRIOUS_PROMPTS_READY",
    "ILLUSTRIOUS_RENDERED",
    "ILLUSTRIOUS_REVIEWED",
    "KLEIN_PROMPTS_READY",
    "KLEIN_RENDERED",
    "FINAL_REVIEWED",
    "COMPLETE",
    "FAILED",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class AdaRunState:
    """Persist stage transitions and artifacts without a database or daemon."""

    def __init__(self, run_dir: Path) -> None:
        self.run_dir = run_dir.resolve()
        self.path = self.run_dir / "ada_run.json"

    def create(
        self, run_id: str, *, character: str, version: str | None, pipeline: str,
        review_policy: str = "strict",
    ) -> dict[str, Any]:
        # Semantic artifacts may legitimately create the candidate directory before
        # the state file. Only the state file establishes an existing ADA run.
        self.run_dir.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            raise FileExistsError(f"ADA run already exists: {self.run_dir}")
        if review_policy not in {"strict", "best_effort"}:
            raise ValueError("review_policy must be strict or best_effort")
        value = {
            "schema_version": 1,
            "run_id": run_id,
            "pipeline": pipeline,
            "character": character,
            "version": version,
            "review_policy": review_policy,
            "stage": "CREATED",
            "created_at": utc_now(),
            "updated_at": utc_now(),
            "seeds": {},
            "artifacts": {},
            "history": [{"stage": "CREATED", "at": utc_now()}],
            "error": None,
        }
        self._write(value, exclusive=True)
        return value

    def read(self) -> dict[str, Any]:
        value = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(value, dict) or value.get("stage") not in STAGES:
            raise ValueError(f"Invalid ADA run state: {self.path}")
        return value

    def allocate_seeds(self, record_ids: list[str]) -> dict[str, dict[str, int]]:
        state = self.read()
        seeds = dict(state.get("seeds", {}))
        used = {seed for pair in seeds.values() for seed in pair.values()}
        for identifier in record_ids:
            if identifier in seeds:
                continue
            pair: list[int] = []
            while len(pair) < 2:
                candidate = secrets.randbelow(2**63)
                if candidate not in used:
                    used.add(candidate)
                    pair.append(candidate)
            seeds[identifier] = {"illustrious": pair[0], "klein": pair[1]}
        state["seeds"] = seeds
        state["updated_at"] = utc_now()
        self._write(state)
        return seeds

    def advance(self, stage: str, *, artifacts: dict[str, str] | None = None) -> dict[str, Any]:
        if stage not in STAGES:
            raise ValueError(f"Unknown ADA stage: {stage}")
        state = self.read()
        current = state["stage"]
        if current in {"COMPLETE", "FAILED"}:
            raise ValueError(f"Cannot advance terminal ADA run from {current}")
        if stage != "FAILED" and STAGES.index(stage) <= STAGES.index(current):
            raise ValueError(f"ADA stage must move forward: {current} -> {stage}")
        state["stage"] = stage
        state["updated_at"] = utc_now()
        state["error"] = None
        if artifacts:
            state.setdefault("artifacts", {}).update(artifacts)
        state.setdefault("history", []).append({"stage": stage, "at": utc_now()})
        self._write(state)
        return state

    def record_recoverable_failure(
        self, exc: Exception, *, component: str, artifacts: dict[str, str] | None = None,
        details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Persist a failed boundary without discarding its last completed stage."""
        state = self.read()
        failure = {
            "component": component,
            "type": type(exc).__name__,
            "message": str(exc),
            "recoverable": True,
            "at": utc_now(),
        }
        if details:
            failure.update(details)
        state["error"] = failure
        state["updated_at"] = utc_now()
        if artifacts:
            state.setdefault("artifacts", {}).update(artifacts)
        state.setdefault("history", []).append({"stage": state["stage"], "event": "recoverable_failure", **failure})
        self._write(state)
        return state

    def attach_artifact(self, name: str, path: str) -> dict[str, Any]:
        """Register an optional artifact without changing the image-run stage."""
        state = self.read()
        state.setdefault("artifacts", {})[name] = path
        state["updated_at"] = utc_now()
        self._write(state)
        return state

    def retry_stage(self, target_stage: str, *, reason: str, max_retries: int = 3) -> dict[str, Any]:
        if target_stage not in STAGES:
            raise ValueError(f"Unknown ADA stage: {target_stage}")
        state = self.read()

        retry_key = f"retries_{target_stage}"
        count = state.get(retry_key, 0)
        if count >= max_retries:
            self.fail(RuntimeError(f"Max retries ({max_retries}) exceeded for {target_stage}. Reason: {reason}"), component="retry_limit")
            return self.read()

        state[retry_key] = count + 1
        state["stage"] = target_stage
        state["updated_at"] = utc_now()
        state["error"] = None

        # When retrying Illustrious, reallocate its seed to force a new result
        if target_stage == "PREMISES_READY" and "seeds" in state:
            for identifier in state["seeds"]:
                state["seeds"][identifier]["illustrious"] = secrets.randbelow(2**63)

        state.setdefault("history", []).append({
            "stage": target_stage,
            "event": "retry",
            "reason": reason,
            "attempt": count + 1,
            "at": utc_now()
        })
        self._write(state)
        return state

    def fail(self, exc: Exception, *, component: str) -> dict[str, Any]:
        state = self.read()
        state["stage"] = "FAILED"
        state["updated_at"] = utc_now()
        state["error"] = {"component": component, "type": type(exc).__name__, "message": str(exc), "at": utc_now()}
        state.setdefault("history", []).append({"stage": "FAILED", "component": component, "at": utc_now()})
        self._write(state)
        return state

    def _write(self, value: dict[str, Any], *, exclusive: bool = False) -> None:
        text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
        if exclusive:
            with self.path.open("x", encoding="utf-8") as output:
                output.write(text)
            return
        descriptor, temporary_name = tempfile.mkstemp(prefix=f".{self.path.name}.", suffix=".tmp", dir=self.run_dir)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as output:
                output.write(text)
            os.replace(temporary_name, self.path)
        finally:
            Path(temporary_name).unlink(missing_ok=True)
