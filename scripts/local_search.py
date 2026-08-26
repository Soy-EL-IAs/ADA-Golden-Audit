#!/usr/bin/env python3
"""Metadata-only client for an opt-in local SearXNG instance.

No request is made at import time. This client only returns URLs and metadata;
the separate character-reference cache performs explicit downloads.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

if __package__:
    from .ada_paths import CONFIG_ROOT
else:
    from ada_paths import CONFIG_ROOT


DEFAULT_CONFIG = CONFIG_ROOT / "search.json"


class SearXNGClient:
    def __init__(self, config_path: Path = DEFAULT_CONFIG) -> None:
        self.config = json.loads(config_path.read_text(encoding="utf-8"))
        self.base_url = os.environ.get("SEARXNG_URL", self.config["searxng_url"]).rstrip("/")

    @property
    def enabled(self) -> bool:
        default = "1" if self.config.get("enabled_by_default") else "0"
        return os.environ.get("PIPELINE_LOCAL_SEARCH", default) == "1"

    def search(self, query: str, category: str, limit: int | None = None) -> dict[str, Any]:
        if not self.enabled:
            raise RuntimeError("Local search is disabled; set PIPELINE_LOCAL_SEARCH=1 after starting SearXNG")
        query = query.strip()
        if not query:
            raise ValueError("query must not be empty")
        if category not in {"general", "images"}:
            raise ValueError("category must be general or images")
        result_limit = self.config["default_limit"] if limit is None else limit
        if not 1 <= result_limit <= self.config["max_limit"]:
            raise ValueError(f"limit must be between 1 and {self.config['max_limit']}")

        params = urllib.parse.urlencode({
            "q": query,
            "format": "json",
            "categories": category,
            "language": self.config["language"],
            "safesearch": self.config["safe_search"],
        })
        request = urllib.request.Request(
            f"{self.base_url}/search?{params}",
            headers={"Accept": "application/json", "User-Agent": "illustrious-klein-local-search/1.0"},
        )
        try:
            with urllib.request.urlopen(request, timeout=self.config["timeout_seconds"]) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"SearXNG HTTP {exc.code}: {body}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"SearXNG unavailable at {self.base_url}: {exc.reason}") from exc

        results = [self._normalize(item, category) for item in payload.get("results", [])[:result_limit]]
        return {
            "provider": "searxng",
            "category": category,
            "query": query,
            "count": len(results),
            "results": results,
            "suggestions": payload.get("suggestions", []),
            "unresponsive_engines": payload.get("unresponsive_engines", []),
            "downloaded": False,
        }

    @staticmethod
    def _normalize(item: dict[str, Any], category: str) -> dict[str, Any]:
        normalized = {
            "title": item.get("title"),
            "page_url": item.get("url"),
            "content": item.get("content"),
            "source": item.get("source"),
            "engine": item.get("engine"),
            "engines": item.get("engines", []),
            "published_date": item.get("publishedDate") or item.get("pubdate"),
        }
        if category == "images":
            normalized.update({
                "image_url": item.get("img_src"),
                "thumbnail_url": item.get("thumbnail_src") or item.get("thumbnail"),
                "resolution": item.get("resolution"),
                "image_format": item.get("img_format"),
                "filesize": item.get("filesize"),
            })
        return normalized

    def web(self, query: str, limit: int | None = None) -> dict[str, Any]:
        return self.search(query, "general", limit)

    def images(self, query: str, limit: int | None = None) -> dict[str, Any]:
        return self.search(query, "images", limit)
