#!/usr/bin/env python3
"""Versioned, phase-specific prompt-guide loading for character datasets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

if __package__:
    from .ada_paths import CONFIG_ROOT
else:
    from ada_paths import CONFIG_ROOT


DEFAULT_CONFIG = CONFIG_ROOT / "prompt_guides.json"
GUIDE_ORDER = ("viral_premise", "illustrious_prompt", "klein_prompt", "minimax_video_prompt")


class PromptGuideLibrary:
    """Load immutable guide files once and expose only the phase-relevant text."""

    def __init__(self, config_path: Path = DEFAULT_CONFIG, viral_override: Path | None = None) -> None:
        self.config_path = config_path.resolve()
        self.config = self._load_config()
        if viral_override is not None:
            guide_path = viral_override.resolve()
            try:
                relative_path = guide_path.relative_to(CONFIG_ROOT.resolve())
            except ValueError as exc:
                raise ValueError(f"Viral override must remain inside config: {guide_path}") from exc
            version = guide_path.stem.removeprefix("viral_premise_guide_")
            if not version or not guide_path.name.endswith(f"_{version}.md"):
                raise ValueError(f"Invalid Viral override filename: {guide_path.name}")
            self.config["active_versions"]["viral_premise"] = version
            self.config["guides"]["viral_premise"] = {"file": relative_path.as_posix()}
        self._guides = self._load_guides()

    def proposal_context(self) -> dict[str, Any]:
        """Creative premise guidance: Viral plus a deliberately small MiniMax seed."""
        return self._context(
            phase="proposal",
            names=("viral_premise",),
            excerpts={"minimax_video_prompt": self._selected_video_sections()},
        )

    def prompt_context(self) -> dict[str, Any]:
        """Compatibility context for the legacy combined prompt-writing flow."""
        return self._context(
            phase="prompt_construction",
            names=("illustrious_prompt", "klein_prompt"),
        )

    def illustrious_context(self) -> dict[str, Any]:
        """Illustrious specialist context; excludes Klein and MiniMax."""
        return self._context(phase="illustrious_prompt", names=("illustrious_prompt",))

    def klein_context(self) -> dict[str, Any]:
        """Klein specialist context; supplied only after Illustrious review."""
        return self._context(phase="klein_prompt", names=("klein_prompt",))

    def minimax_context(self) -> dict[str, Any]:
        """Video-only specialist context; excluded from the image pipeline."""
        return self._context(phase="minimax_video_prompt", names=("minimax_video_prompt",))

    def manifest(self) -> dict[str, Any]:
        return {
            name: {"version": item["version"], "file": item["file"]}
            for name, item in self._guides.items()
        }

    def _context(
        self,
        phase: str,
        names: tuple[str, ...],
        excerpts: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        selected: list[dict[str, str]] = []
        for name in names:
            item = self._guides[name]
            selected.append({"name": name, "version": item["version"], "file": item["file"], "content": item["content"]})
        for name, content in (excerpts or {}).items():
            item = self._guides[name]
            selected.append({"name": name, "version": item["version"], "file": item["file"], "content": content, "excerpt": "proposal_video_seed"})
        return {"phase": phase, "guides": selected}

    def _load_config(self) -> dict[str, Any]:
        try:
            config = json.loads(self.config_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid prompt-guide config: {self.config_path}") from exc
        if not isinstance(config, dict):
            raise ValueError("Prompt-guide config must be an object")
        return config

    def _load_guides(self) -> dict[str, dict[str, str]]:
        versions = self.config.get("active_versions")
        guides = self.config.get("guides")
        if not isinstance(versions, dict) or not isinstance(guides, dict):
            raise ValueError("Prompt-guide config requires active_versions and guides")
        loaded: dict[str, dict[str, str]] = {}
        for name in GUIDE_ORDER:
            version, source = versions.get(name), guides.get(name)
            if not isinstance(version, str) or not isinstance(source, dict) or not isinstance(source.get("file"), str):
                raise ValueError(f"Prompt-guide config is missing {name}")
            if not source["file"].endswith(f"_{version}.md"):
                raise ValueError(f"Prompt-guide file/version mismatch for {name}")
            path = (CONFIG_ROOT / source["file"]).resolve()
            try:
                path.relative_to(CONFIG_ROOT.resolve())
            except ValueError as exc:
                raise ValueError(f"Prompt guide must remain inside config: {path}") from exc
            try:
                content = path.read_text(encoding="utf-8").strip()
            except OSError as exc:
                raise FileNotFoundError(f"Configured prompt guide is unavailable: {path}") from exc
            if not content:
                raise ValueError(f"Configured prompt guide is empty: {path}")
            loaded[name] = {"version": version, "file": source["file"], "content": content}
        return loaded

    def _selected_video_sections(self) -> str:
        headings = self.config.get("proposal_video_sections")
        if not isinstance(headings, list) or not all(isinstance(item, str) for item in headings):
            raise ValueError("proposal_video_sections must be a list of headings")
        source = self._guides["minimax_video_prompt"]["content"]
        chunks = [self._section(source, heading) for heading in headings]
        return "\n\n".join(chunks)

    @staticmethod
    def _section(source: str, heading: str) -> str:
        start = source.find(heading)
        if start < 0:
            raise ValueError(f"MiniMax guide section not found: {heading}")
        next_heading = source.find("\n# ", start + len(heading))
        return source[start:] if next_heading < 0 else source[start:next_heading].rstrip()
