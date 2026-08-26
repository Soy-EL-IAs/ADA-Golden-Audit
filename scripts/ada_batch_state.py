#!/usr/bin/env python3
"""Batch manifest for ADA's stage-scheduled pipeline."""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

class AdaBatchState:
    """Lightweight manifest for a batch run wrapping independent AdaRunState items."""

    def __init__(self, batch_dir: Path) -> None:
        self.batch_dir = batch_dir.resolve()
        self.path = self.batch_dir / "batch_run.json"

    def create(
        self, batch_id: str, *, character: str, version: str | None, count: int,
        item_run_ids: list[str]
    ) -> dict[str, Any]:
        if self.path.exists():
            raise FileExistsError(f"ADA batch already exists: {self.batch_dir}")
        self.batch_dir.mkdir(parents=True, exist_ok=True)
        value = {
            "schema_version": 1,
            "batch_id": batch_id,
            "character": character,
            "version": version,
            "count": count,
            "items": item_run_ids,
            "created_at": utc_now(),
            "updated_at": utc_now(),
        }
        self._write(value, exclusive=True)
        return value

    def read(self) -> dict[str, Any]:
        value = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(value, dict) or "items" not in value:
            raise ValueError(f"Invalid ADA batch state: {self.path}")
        return value

    def _write(self, value: dict[str, Any], *, exclusive: bool = False) -> None:
        text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
        if exclusive:
            with self.path.open("x", encoding="utf-8") as output:
                output.write(text)
            return
        descriptor, temporary_name = tempfile.mkstemp(prefix=f".{self.path.name}.", suffix=".tmp", dir=self.batch_dir)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as output:
                output.write(text)
            os.replace(temporary_name, self.path)
        finally:
            Path(temporary_name).unlink(missing_ok=True)
