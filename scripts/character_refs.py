#!/usr/bin/env python3
"""Deterministic two-stage selection of character-reference candidates.

One SearXNG web search discovers trusted pages. Their HTML metadata is inspected
for associated images. One general image search is used only as fallback. Image
files are never downloaded and no LLM participates in filtering or ranking.
"""

from __future__ import annotations

import json
import re
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

if __package__:
    from .local_search import SearXNGClient
else:
    from local_search import SearXNGClient


if __package__:
    from .ada_paths import CONFIG_ROOT
else:
    from ada_paths import CONFIG_ROOT


DEFAULT_CONFIG = CONFIG_ROOT / "character_refs.json"


class _PageImageParser(HTMLParser):
    def __init__(self, page_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.page_url = page_url
        self.page_title = ""
        self._inside_title = False
        self._last_meta: dict[str, Any] | None = None
        self._active_link: dict[str, str] | None = None
        self.images: list[dict[str, Any]] = []
        self.links: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        if tag.lower() == "title":
            self._inside_title = True
            return
        if tag.lower() == "meta":
            name = (values.get("property") or values.get("name") or "").lower()
            content = values.get("content", "").strip()
            if name in {"og:image", "og:image:url", "twitter:image", "twitter:image:src"} and content:
                item = {"url": urllib.parse.urljoin(self.page_url, content), "kind": name, "text": name}
                self.images.append(item)
                self._last_meta = item
            elif self._last_meta is not None and name in {"og:image:width", "twitter:image:width"}:
                self._last_meta["width"] = content
            elif self._last_meta is not None and name in {"og:image:height", "twitter:image:height"}:
                self._last_meta["height"] = content
            return
        if tag.lower() == "link":
            rel = self._normalize_rel(values.get("rel", ""))
            href = values.get("href", "").strip()
            if href and "image_src" in rel:
                self.images.append({
                    "url": urllib.parse.urljoin(self.page_url, href),
                    "kind": "image_src",
                    "text": values.get("title", "") or "image_src",
                })
            return
        if tag.lower() == "a":
            href = values.get("href", "").strip()
            self._active_link = (
                {
                    "url": urllib.parse.urljoin(self.page_url, href),
                    "text": " ".join((values.get("title", ""), values.get("aria-label", ""))).strip(),
                }
                if href
                else None
            )
            return
        if tag.lower() not in {"img", "source"}:
            return
        source = values.get("src") or values.get("data-src") or values.get("data-original")
        descriptive = " ".join(values.get(key, "") for key in ("alt", "title", "class", "id")).strip()
        srcset_sources: list[tuple[int, str]] = []
        for srcset_item in values.get("srcset", "").split(","):
            parts = srcset_item.strip().split()
            srcset_url = parts[0] if parts else ""
            if srcset_url:
                descriptor = int(re.sub(r"\D", "", parts[1])) if len(parts) > 1 and re.search(r"\d", parts[1]) else 0
                srcset_sources.append((descriptor, srcset_url))
        # srcset entries are size variants of one visual, not distinct assets.
        # Keep only the largest advertised variant and otherwise use src.
        sources = [max(srcset_sources)[1]] if srcset_sources else ([source] if source else [])
        for image_source in sources:
            self.images.append({
                "url": urllib.parse.urljoin(self.page_url, image_source),
                "kind": tag.lower(),
                "text": descriptive,
                "width": values.get("width"),
                "height": values.get("height"),
            })

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._inside_title = False
        elif tag.lower() == "a" and self._active_link is not None:
            self._active_link["text"] = " ".join(self._active_link["text"].split())
            self.links.append(self._active_link)
            self._active_link = None

    def handle_data(self, data: str) -> None:
        if self._inside_title:
            self.page_title += data
        if self._active_link is not None:
            self._active_link["text"] += f" {data}"

    @staticmethod
    def _normalize_rel(value: str) -> set[str]:
        return {item.strip().lower() for item in value.split() if item.strip()}


class CharacterReferenceFinder:
    def __init__(self, search: SearXNGClient, config_path: Path = DEFAULT_CONFIG) -> None:
        self.search = search
        self.config = json.loads(config_path.read_text(encoding="utf-8"))

    def find(
        self, character: str, version: str | None = None, limit: int = 6, *,
        _allow_name_fallback: bool = True,
    ) -> dict[str, Any]:
        character = self._clean_input(character, "character")
        version = self._clean_input(version, "version") if version else None
        if not 1 <= limit <= self.config["max_returned_refs"]:
            raise ValueError(f"limit must be between 1 and {self.config['max_returned_refs']}")

        character_variants = self._character_variants(character)
        version_variants = self._text_variants(version) if version else []
        subject = " ".join(part for part in (character, version) if part)
        web_query = f'"{subject}" official character'
        queries_used = [web_query]
        web_response = self.search.web(web_query, self.config["results_per_search"])

        trusted_pages = self._trusted_pages(web_response.get("results", []), character_variants, version_variants)
        candidates: list[dict[str, Any]] = []
        page_fetch_errors = 0
        pages_inspected = 0
        queued_pages: set[str] = set()
        page_queue: list[tuple[dict[str, Any], str]] = []
        for page in trusted_pages:
            ecosystem = self._trusted_ecosystem(page["page_url"])
            page_key = self._normalized_url(page["page_url"])
            if ecosystem and page_key not in queued_pages:
                queued_pages.add(page_key)
                page_queue.append((page, ecosystem))

        while page_queue and pages_inspected < self.config["page_fetch"]["max_pages"]:
            page, ecosystem = page_queue.pop(0)
            pages_inspected += 1
            try:
                extracted, discovered_links = self._extract_page_images(page, character_variants)
            except (RuntimeError, ValueError):
                page_fetch_errors += 1
                continue
            for result in extracted:
                candidate = self._candidate(result, character_variants, version_variants, origin="trusted_page")
                if candidate is not None:
                    candidates.append(candidate)
            if not self.config["page_fetch"].get("follow_same_ecosystem_links", True):
                continue
            followable: list[tuple[dict[str, Any], str]] = []
            for link in discovered_links:
                link_url = link["url"]
                link_key = self._normalized_url(link_url)
                if link_key in queued_pages:
                    continue
                if not self._same_trusted_ecosystem(link_url, ecosystem):
                    continue
                if not self._followable_page_link(link, character_variants, version_variants):
                    continue
                queued_pages.add(link_key)
                followable.append(({
                    "page_url": link_url,
                    "title": link.get("text", ""),
                    "content": page.get("content"),
                    "source": page.get("source"),
                }, ecosystem))
            followable.sort(
                key=lambda item: self._canonical_link_priority(
                    item[0]["page_url"], item[0].get("title", ""), character_variants, version_variants
                ),
                reverse=True,
            )
            # Follow links from the strongest canonical page before consuming
            # the remaining inspection budget on unrelated search results.
            page_queue[0:0] = followable

        candidates = self._deduplicate(candidates)
        used_image_fallback = len(candidates) < limit
        if used_image_fallback:
            image_query = f'"{subject}" official artwork render'
            queries_used.append(image_query)
            image_response = self.search.images(image_query, self.config["results_per_search"])
            fallback_candidates: list[dict[str, Any]] = []
            for result in image_response.get("results", []):
                candidate = self._candidate(result, character_variants, version_variants, origin="image_fallback")
                if candidate is not None:
                    fallback_candidates.append(candidate)
            fallback_candidates = self._deduplicate(fallback_candidates)
            fallback_candidates.sort(
                key=lambda item: (item["domain"], -item["final_score"], -item["source_trust"], item["source_url"])
            )
            fallback_domain_counts: dict[str, int] = {}
            for candidate in fallback_candidates:
                domain = candidate["domain"]
                if fallback_domain_counts.get(domain, 0) < self.config["fallback_max_results_per_domain"]:
                    fallback_domain_counts[domain] = fallback_domain_counts.get(domain, 0) + 1
                    candidates.append(candidate)
            candidates = self._deduplicate(candidates)

        selected = self._select_diverse(candidates, limit)
        result = {
            "character": character,
            "version": version,
            "provider": "searxng",
            "queries_used": queries_used,
            "search_count": len(queries_used),
            "used_image_fallback": used_image_fallback,
            "trusted_pages_considered": len(trusted_pages),
            "trusted_pages_inspected": pages_inspected,
            "page_fetch_errors": page_fetch_errors,
            "eligible_candidate_count": sum(
                item["final_score"] >= self.config["minimum_return_score"] for item in candidates
            ),
            "count": len(selected),
            "refs": selected,
            "downloaded": False,
            "mechanical_filter": True,
        }
        # A profile/booru spelling can differ from the search-index spelling.
        # Retry only after the full requested name produced no usable refs.
        if len(selected) < min(2, limit) and _allow_name_fallback:
            for fallback_name in self._fallback_search_names(character):
                fallback = self.find(
                    fallback_name, version, limit, _allow_name_fallback=False,
                )
                result["queries_used"].extend(fallback["queries_used"])
                result["search_count"] = len(result["queries_used"])
                result["trusted_pages_considered"] += fallback["trusted_pages_considered"]
                result["trusted_pages_inspected"] += fallback["trusted_pages_inspected"]
                result["page_fetch_errors"] += fallback["page_fetch_errors"]
                if fallback["refs"]:
                    result["refs"] = fallback["refs"]
                    result["count"] = fallback["count"]
                    result["eligible_candidate_count"] = fallback["eligible_candidate_count"]
                    result["used_image_fallback"] = result["used_image_fallback"] or fallback["used_image_fallback"]
                    break
        return result

    def find_resolved(self, identity: dict[str, Any], limit: int = 5) -> dict[str, Any]:
        """Discover references after taxonomy resolution.

        Eligibility is intentionally separate from ranking.  A direct image
        result inherits the tier of the *page that exposed it*, never the CDN
        host, and records that observed relationship in the artifact.
        """
        canonical_name = str(identity.get("canonical_name") or identity.get("requested_name") or "").strip()
        canonical_tag = str(identity.get("canonical_tag") or "").strip()
        franchises = [str(value) for value in identity.get("franchise", []) if isinstance(value, str)]
        if not canonical_name or not canonical_tag:
            raise ValueError("Resolved identity requires canonical_name and canonical_tag")
        franchise = franchises[0].replace("_", " ") if franchises else ""
        discovery = self.config.get("discovery", {}) if isinstance(self.config.get("discovery"), dict) else {}
        templates = discovery.get("query_templates", []) if isinstance(discovery.get("query_templates"), list) else []
        if not templates:
            templates = ["\"{canonical_name}\" \"{franchise}\"", "\"{canonical_name}\" official artwork", "\"{canonical_tag}\""]
        max_queries = int(discovery.get("max_queries", 6))
        query_values = {"canonical_name": canonical_name, "canonical_tag": canonical_tag, "franchise": franchise}
        queries = list(dict.fromkeys(template.format(**query_values).strip() for template in templates if template.format(**query_values).strip()))[:max_queries]
        variants = [value for value in identity.get("aliases", []) if isinstance(value, str)]
        if len(queries) < max_queries:
            for alias in variants:
                query = f'"{alias}" "{franchise}" character'.strip()
                if query not in queries:
                    queries.append(query)
                if len(queries) >= max_queries:
                    break
        variants = self._character_variants(canonical_tag) + self._character_variants(canonical_name)
        version_variants = [value for value in self._text_variants(franchise) if value]
        raw: list[dict[str, Any]] = []
        queries_used: list[str] = []
        page_fetch_errors = 0
        per_query = int(discovery.get("results_per_query", self.config.get("results_per_search", 20)))
        for query in queries:
            queries_used.append(query)
            try:
                images = self.search.images(query, per_query).get("results", [])
            except RuntimeError:
                images = []
            for result in images:
                raw.append({**result, "discovered_via": "image_search", "source_page": result.get("page_url", "")})
            try:
                pages = self.search.web(query, per_query).get("results", [])
            except RuntimeError:
                pages = []
            for page in self._trusted_pages(pages, variants, version_variants):
                try:
                    extracted, _ = self._extract_page_images(page, variants)
                except (RuntimeError, ValueError):
                    page_fetch_errors += 1
                    continue
                for result in extracted:
                    raw.append({**result, "discovered_via": "source_page_crawl", "source_page": page["page_url"]})

        eligible: list[dict[str, Any]] = []
        rejected: list[dict[str, Any]] = []
        seen: set[str] = set()
        for result in raw:
            candidate = self._candidate(result, variants, version_variants, origin=str(result.get("discovered_via") or "discovery"))
            if candidate is None:
                rejected.append({"image_url": str(result.get("image_url") or ""), "reason": "invalid_or_irrelevant_candidate"})
                continue
            source_page = str(result.get("source_page") or candidate["source_url"])
            key = self._asset_identity(candidate["image_url"])
            if key in seen:
                rejected.append({"image_url": candidate["image_url"], "reason": "duplicate_url"})
                continue
            seen.add(key)
            tier = self._source_tier(source_page, candidate["image_url"])
            identity_confidence = round(candidate["character_relevance"] / 100, 2)
            utility = round(candidate["image_quality"] / 100, 2)
            validation = self.config.get("validation", {}) if isinstance(self.config.get("validation"), dict) else {}
            minimum_identity = float(validation.get("minimum_identity_confidence", 0.70))
            minimum_utility = float(validation.get("minimum_reference_utility", 0.45))
            reasons: list[str] = []
            if identity_confidence < minimum_identity:
                reasons.append("identity_relevance_below_gate")
            if utility < minimum_utility:
                reasons.append("reference_utility_below_gate")
            if reasons:
                rejected.append({"image_url": candidate["image_url"], "reason": ",".join(reasons)})
                continue
            eligible.append({
                **candidate,
                "source_page": source_page,
                "source_tier": tier,
                "trust_origin": "source_page",
                "discovered_via": result.get("discovered_via", "discovery"),
                "identity_confidence": identity_confidence,
                "reference_utility": utility,
                "identity_validation": {"status": "textual_provenance", "identity_match": True, "confidence": identity_confidence, "evidence": [candidate["trust_reason"]]},
            })
        tier_trust = self._tier_trust
        eligible.sort(key=lambda item: (-item["identity_confidence"], -item["reference_utility"], -tier_trust(item["source_tier"]), item["source_page"]))
        return {
            "schema_version": "character_reference_discovery_v2",
            "identity": identity,
            "provider": "searxng",
            "queries_used": queries_used,
            "raw_candidate_count": len(raw),
            "page_fetch_errors": page_fetch_errors,
            "rejected": rejected,
            "eligible": eligible[:limit],
            "refs": eligible[:limit],
            "count": len(eligible[:limit]),
        }

    def _source_tier(self, source_page: str, image_url: str) -> str:
        policy = self.config.get("source_policy", {}) if isinstance(self.config.get("source_policy"), dict) else {}
        overrides = policy.get("domain_overrides", {}) if isinstance(policy.get("domain_overrides"), dict) else {}
        page_domain = self._domain(source_page)
        image_domain = self._domain(image_url)
        for domain, tier in overrides.items():
            if self._domain_matches(page_domain, str(domain)) or self._domain_matches(image_domain, str(domain)):
                return str(tier)
        if self._official_label(page_domain):
            return "official"
        if any(self._domain_matches(page_domain, domain) for domain in self.config.get("trusted_domains", {})):
            return "trusted"
        return "unknown"

    def _tier_trust(self, tier: str) -> int:
        policy = self.config.get("source_policy", {}) if isinstance(self.config.get("source_policy"), dict) else {}
        tiers = policy.get("tiers", {}) if isinstance(policy.get("tiers"), dict) else {}
        entry = tiers.get(tier, {}) if isinstance(tiers.get(tier), dict) else {}
        return int(entry.get("trust", 0))

    def _trusted_pages(
        self,
        results: list[dict[str, Any]],
        character_variants: list[str],
        version_variants: list[str],
    ) -> list[dict[str, Any]]:
        pages: list[dict[str, Any]] = []
        seen: set[str] = set()
        for result in results:
            source_url = str(result.get("page_url") or "").strip()
            if not self._http_url(source_url):
                continue
            domain = self._domain(source_url)
            if self._excluded(result, domain, ""):
                continue
            source_trust, source_reason = self._source_trust(domain, "", result)
            if source_trust < min(self.config["trusted_domains"].values(), default=70):
                continue
            relevance, relevance_reason = self._relevance(result, character_variants, version_variants)
            if relevance < self.config["minimum_character_relevance"]:
                continue
            key = self._normalized_url(source_url)
            if key in seen:
                continue
            seen.add(key)
            pages.append({
                **result,
                "source_trust": source_trust,
                "source_reason": source_reason,
                "character_relevance": relevance,
                "relevance_reason": relevance_reason,
            })
        pages.sort(key=lambda item: (-item["source_trust"], -item["character_relevance"], item["page_url"]))
        return pages

    def _extract_page_images(
        self,
        page: dict[str, Any],
        character_variants: list[str],
    ) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
        page_url = page["page_url"]
        request = urllib.request.Request(
            page_url,
            headers={"Accept": "text/html,application/xhtml+xml", "User-Agent": "illustrious-klein-ref-selector/1.0"},
        )
        try:
            with urllib.request.urlopen(request, timeout=self.config["page_fetch"]["timeout_seconds"]) as response:
                content_type = response.headers.get_content_type()
                if content_type not in {"text/html", "application/xhtml+xml"}:
                    raise ValueError(f"Unsupported page content type: {content_type}")
                html = response.read(self.config["page_fetch"]["max_bytes"] + 1)
        except (urllib.error.HTTPError, urllib.error.URLError) as exc:
            raise RuntimeError(f"Could not inspect trusted page {page_url}: {exc}") from exc
        if len(html) > self.config["page_fetch"]["max_bytes"]:
            raise ValueError(f"Trusted page exceeds metadata inspection limit: {page_url}")

        parser = _PageImageParser(page_url)
        parser.feed(html.decode("utf-8", errors="replace"))
        results: list[dict[str, Any]] = []
        for image in parser.images:
            image_url = image.get("url", "")
            if not self._http_url(image_url):
                continue
            evidence = " ".join([parser.page_title, image.get("text", ""), page.get("title") or ""])
            if image.get("kind") in {"img", "source"} and not self._looks_like_character_asset(
                evidence, image_url, character_variants
            ):
                continue
            width = self._integer(image.get("width"))
            height = self._integer(image.get("height"))
            resolution = f"{width}x{height}" if width and height else None
            results.append({
                "page_url": page_url,
                "image_url": image_url,
                "resolution": resolution,
                "title": evidence,
                "content": page.get("content"),
                "source": page.get("source"),
            })
        return results, parser.links

    def _candidate(
        self,
        result: dict[str, Any],
        character_variants: list[str],
        version_variants: list[str],
        origin: str,
    ) -> dict[str, Any] | None:
        source_url = str(result.get("page_url") or "").strip()
        image_url = str(result.get("image_url") or "").strip()
        if not self._http_url(source_url) or not self._http_url(image_url):
            return None
        source_domain = self._domain(source_url)
        image_domain = self._domain(image_url)
        if self._excluded(result, source_domain, image_domain):
            return None
        if urllib.parse.urlsplit(image_url).path.lower().endswith(".svg"):
            return None
        normalized_asset_url = self._normalize_text(
            f"{image_url} {result.get('title') or ''}"
        )
        if any(
            re.search(rf"(?<!\w){re.escape(term)}(?!\w)", normalized_asset_url)
            for term in self.config["excluded_asset_terms"]
        ):
            return None

        source_trust, source_reason = self._source_trust(source_domain, image_domain, result)
        relevance, relevance_reason = self._relevance(result, character_variants, version_variants)
        if relevance < self.config["minimum_character_relevance"]:
            return None
        image_quality, quality_reason = self._image_quality(result.get("resolution"))
        weights = self.config["score_weights"]
        final_score = round(
            source_trust * weights["source_trust"]
            + relevance * weights["character_relevance"]
            + image_quality * weights["image_quality"]
        )
        final_score = max(0, min(100, final_score))
        return {
            "source_url": source_url,
            "image_url": image_url,
            "resolution": result.get("resolution"),
            "domain": source_domain,
            "source_trust": source_trust,
            "character_relevance": relevance,
            "image_quality": image_quality,
            "final_score": final_score,
            "recommendation": self._recommendation(final_score),
            "trust_reason": f"{source_reason}; {relevance_reason}; {quality_reason}; origin:{origin}",
            "_origin": origin,
        }

    def _source_trust(self, source_domain: str, image_domain: str, result: dict[str, Any]) -> tuple[int, str]:
        official = self._official_label(source_domain) or self._official_label(image_domain)
        if official:
            return self.config["source_scores"]["official"], f"official_domain:{official}"
        for domain, score in self.config["trusted_domains"].items():
            if self._domain_matches(source_domain, domain) or self._domain_matches(image_domain, domain):
                return score, f"trusted_domain:{domain}"
        text = self._normalize_text(" ".join(str(result.get(key) or "") for key in ("title", "source")))
        score = self.config["source_scores"]["unverified"]
        if "official" in text:
            score = min(30, score + 10)
            return score, "unverified_domain_claims_official"
        return score, "unverified_domain"

    def _relevance(
        self,
        result: dict[str, Any],
        character_variants: list[str],
        version_variants: list[str],
    ) -> tuple[int, str]:
        primary = self._normalize_text(" ".join(str(result.get(key) or "") for key in ("title", "page_url", "image_url")))
        secondary = self._normalize_text(" ".join(str(result.get(key) or "") for key in ("content", "source")))
        primary_score, match = self._variant_match(primary, character_variants)
        if primary_score:
            score = primary_score
            reason = f"character_in_title_or_url:{match}"
        else:
            secondary_score, match = self._variant_match(secondary, character_variants)
            if not secondary_score:
                return 0, "character_not_found_in_title_url_or_metadata"
            # Secondary snippets are not enough: the configured minimum causes
            # these candidates to be discarded unless title/URL identifies the character.
            score = min(35, secondary_score)
            reason = f"character_only_in_secondary_metadata:{match}"
        if version_variants:
            version_score, version_match = self._variant_match(f"{primary} {secondary}", version_variants)
            if version_score:
                reason += f",version_match:{version_match}"
            else:
                score -= 25
                reason += ",version_not_found"
        return max(0, min(100, score)), reason

    @staticmethod
    def _variant_match(text: str, variants: list[str]) -> tuple[int, str]:
        compact_text = text.replace(" ", "")
        for index, variant in enumerate(variants):
            if re.search(rf"(?<!\w){re.escape(variant)}(?!\w)", text):
                return (100 if index == 0 else 80), variant
            if len(variant) >= 4 and variant.replace(" ", "") in compact_text:
                return (95 if index == 0 else 75), variant
        return 0, ""

    def _image_quality(self, value: Any) -> tuple[int, str]:
        width, height = self._parse_resolution(value)
        pixels = width * height
        settings = self.config["resolution"]
        if width >= settings["preferred_min_width"] and height >= settings["preferred_min_height"]:
            return 90, f"preferred_resolution:{width}x{height}"
        if pixels >= settings["minimum_pixels"]:
            return 65, f"acceptable_resolution:{width}x{height}"
        if pixels:
            return 20, f"low_resolution:{width}x{height}"
        return 35, "resolution_unknown"

    def _excluded(self, result: dict[str, Any], source_domain: str, image_domain: str) -> bool:
        if self._matches_domain(source_domain, self.config["excluded_domains"]):
            return True
        if image_domain and self._matches_domain(image_domain, self.config["excluded_domains"]):
            return True
        searchable = " ".join(
            [str(result.get("page_url") or ""), str(result.get("image_url") or "")]
            + [str(result.get(key) or "") for key in ("title", "content", "source")]
        ).lower()
        return any(term.lower() in searchable for term in self.config["excluded_terms"])

    @staticmethod
    def _looks_like_character_asset(evidence: str, image_url: str, character_variants: list[str]) -> bool:
        text = CharacterReferenceFinder._normalize_text(f"{evidence} {image_url}")
        if CharacterReferenceFinder._variant_match(text, character_variants)[0]:
            return True
        return any(token in text for token in ("character", "render", "portrait", "key art", "keyart", "hero"))

    @staticmethod
    def _deduplicate(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
        candidates.sort(key=lambda item: (-item["final_score"], item["source_url"]))
        seen_images: set[str] = set()
        unique: list[dict[str, Any]] = []
        for candidate in candidates:
            image_key = CharacterReferenceFinder._asset_identity(candidate["image_url"])
            if image_key in seen_images:
                continue
            seen_images.add(image_key)
            unique.append(candidate)
        return unique

    def _select_diverse(self, candidates: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
        eligible = [
            item for item in candidates
            if item["final_score"] >= self.config["minimum_return_score"]
        ]
        eligible.sort(key=lambda item: (-item["final_score"], -item["source_trust"], item["source_url"]))
        by_domain: dict[str, list[dict[str, Any]]] = {}
        for item in eligible:
            by_domain.setdefault(item["domain"], []).append(item)

        domain_order = sorted(
            by_domain,
            key=lambda domain: (
                -by_domain[domain][0]["final_score"],
                -by_domain[domain][0]["source_trust"],
                domain,
            ),
        )
        selected: list[dict[str, Any]] = []
        max_per_domain = self.config["final_max_results_per_domain"]
        for position in range(max_per_domain):
            for domain in domain_order:
                items = by_domain[domain]
                if position < len(items):
                    selected.append(items[position])
                    if len(selected) >= limit:
                        return self._public_candidates(selected)

        # Diversity remains the first pass. Extra slots may only be filled by
        # assets discovered while inspecting configured official/trusted pages;
        # the general image fallback stays capped at two results per domain.
        selected_images = {self._normalized_url(item["image_url"]) for item in selected}
        trusted_floor = min(self.config["trusted_domains"].values(), default=70)
        canonical_extras = [
            item for item in eligible
            if item.get("_origin") == "trusted_page"
            and item["source_trust"] >= trusted_floor
            and self._normalized_url(item["image_url"]) not in selected_images
        ]
        for item in canonical_extras:
            selected.append(item)
            selected_images.add(self._normalized_url(item["image_url"]))
            if len(selected) >= limit:
                break
        return self._public_candidates(selected)

    @staticmethod
    def _public_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [{key: value for key, value in item.items() if not key.startswith("_")} for item in candidates]

    def _trusted_ecosystem(self, url: str) -> str | None:
        domain = self._domain(url)
        configured = list(self.config["official_domains"]) + list(self.config["trusted_domains"])
        return next((root for root in configured if self._domain_matches(domain, root)), None)

    def _same_trusted_ecosystem(self, url: str, ecosystem: str) -> bool:
        return self._http_url(url) and self._domain_matches(self._domain(url), ecosystem)

    def _followable_page_link(
        self,
        link: dict[str, str],
        character_variants: list[str],
        version_variants: list[str],
    ) -> bool:
        url = link.get("url", "")
        parsed = urllib.parse.urlsplit(url)
        if re.search(r"\.(?:avif|gif|jpe?g|png|svg|webp|pdf|zip)(?:$|\?)", parsed.path, re.IGNORECASE):
            return False
        evidence = self._normalize_text(f"{url} {link.get('text', '')}")
        if any(term in evidence for term in ("fanart", "fan art", "wallpaper", "cosplay")):
            return False
        if self._variant_match(evidence, character_variants)[0]:
            return True
        if version_variants and self._variant_match(evidence, version_variants)[0]:
            return True
        return any(term in evidence for term in self.config["page_fetch"].get("canonical_link_terms", []))

    def _canonical_link_priority(
        self,
        url: str,
        text: str,
        character_variants: list[str],
        version_variants: list[str],
    ) -> tuple[int, int, int]:
        evidence = self._normalize_text(f"{url} {text}")
        character_match = self._variant_match(evidence, character_variants)[0]
        version_match = self._variant_match(evidence, version_variants)[0] if version_variants else 0
        canonical_terms = sum(
            term in evidence for term in self.config["page_fetch"].get("canonical_link_terms", [])
        )
        return character_match, version_match, canonical_terms

    def _recommendation(self, final_score: int) -> str:
        thresholds = self.config["recommendation_thresholds"]
        if final_score >= thresholds["auto"]:
            return "auto"
        if final_score >= thresholds["review"]:
            return "review"
        return "reject"

    def _character_variants(self, character: str) -> list[str]:
        normalized = self._normalize_text(character)
        variants = [normalized]
        variants.extend(self._normalize_text(item) for item in self.config["character_aliases"].get(normalized, []))
        tokens = normalized.split()
        generic = set(self.config["generic_name_tokens"])
        if len(tokens) > 1:
            for token in (tokens[0], tokens[-1]):
                if len(token) >= 4 and token not in generic:
                    variants.append(token)
        return list(dict.fromkeys(item for item in variants if item))

    def _fallback_search_names(self, character: str) -> list[str]:
        """Try common alternate name order, then one distinctive name token."""
        tokens = self._normalize_text(character).split()
        if len(tokens) < 2:
            return []
        generic = set(self.config["generic_name_tokens"])
        alternatives = [" ".join(reversed(tokens))]
        alternatives.extend(token for token in reversed(tokens) if len(token) >= 4 and token not in generic)
        original = self._normalize_text(character)
        return list(dict.fromkeys(value for value in alternatives if value and value != original))

    def _text_variants(self, value: str) -> list[str]:
        normalized = self._normalize_text(value)
        return [normalized] if normalized else []

    @staticmethod
    def _clean_input(value: str, field: str) -> str:
        cleaned = " ".join(value.split()).strip()
        if not cleaned or len(cleaned) > 120:
            raise ValueError(f"{field} must contain between 1 and 120 characters")
        return cleaned

    def _official_label(self, domain: str) -> str | None:
        for official_domain, label in self.config["official_domains"].items():
            if self._domain_matches(domain, official_domain):
                return label
        return None

    @staticmethod
    def _domain_matches(domain: str, expected: str) -> bool:
        return domain == expected or domain.endswith(f".{expected}")

    def _matches_domain(self, domain: str, domains: list[str]) -> bool:
        return any(self._domain_matches(domain, blocked) for blocked in domains)

    @staticmethod
    def _domain(url: str) -> str:
        return (urllib.parse.urlsplit(url).hostname or "").lower().removeprefix("www.")

    @staticmethod
    def _http_url(url: str) -> bool:
        parsed = urllib.parse.urlsplit(url)
        return parsed.scheme in {"http", "https"} and bool(parsed.hostname)

    @staticmethod
    def _normalized_url(url: str) -> str:
        parsed = urllib.parse.urlsplit(url)
        host = (parsed.hostname or "").lower()
        path = re.sub(r"/+", "/", urllib.parse.unquote(parsed.path)).rstrip("/")
        return f"{host}{path}".lower()

    @staticmethod
    def _asset_identity(url: str) -> str:
        """Collapse obvious size/name variants without changing candidate ranking."""
        normalized = CharacterReferenceFinder._normalized_url(url)
        normalized = re.sub(r"\.(?:avif|gif|jpe?g|png|webp)$", "", normalized)
        normalized = re.sub(
            r"(?:[-_.](?:\d{2,5}x\d{2,5}|thumb(?:nail)?|small|medium|large|full|[23]x))+$",
            "",
            normalized,
        )
        normalized = re.sub(
            r"/(?:thumbs?|thumbnails?|small|medium|large|\d{2,5}x\d{2,5})/",
            "/",
            normalized,
        )
        return normalized

    @staticmethod
    def _normalize_text(value: str) -> str:
        ascii_text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
        return re.sub(r"[^a-z0-9]+", " ", ascii_text.lower()).strip()

    @staticmethod
    def _parse_resolution(value: Any) -> tuple[int, int]:
        match = re.search(r"(\d{2,5})\s*[x×]\s*(\d{2,5})", str(value or ""), flags=re.IGNORECASE)
        return (int(match.group(1)), int(match.group(2))) if match else (0, 0)

    @staticmethod
    def _integer(value: Any) -> int:
        match = re.search(r"\d+", str(value or ""))
        return int(match.group()) if match else 0
