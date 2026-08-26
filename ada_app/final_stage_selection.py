"""Deterministic final-stage selection from a persisted comparative review."""

from __future__ import annotations

from typing import Any

from scripts.agent_contracts import validate_contract


def build_final_stage_decision(
    comparison: dict[str, Any], receipts: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Select an exact receipt output; PASS verdicts are intentionally not inputs."""
    validate_contract("comparative_review_v1", comparison)
    for stage, receipt in receipts.items():
        validate_contract("render_receipt_v1", receipt)
        if receipt.get("stage") != stage or comparison["stages"].get(f"{stage}_receipt_id") != receipt.get("receipt_id"):
            raise ValueError(f"Comparative lineage does not match the {stage} render receipt")
    preferred = comparison["preferred_stage"]
    requires_human = preferred in {"TIE", "HUMAN_REVIEW_REQUIRED"}
    if preferred == "ILLUSTRIOUS":
        selected_stage = "illustrious"
        source = "comparative_review"
        reason = comparison["comparison"]["overall_preference"]["reason"]
    elif preferred == "KLEIN":
        selected_stage = "klein"
        source = "comparative_review"
        reason = comparison["comparison"]["overall_preference"]["reason"]
    else:
        selected_stage = "klein"
        source = "comparative_review_fallback"
        reason = (
            f"Comparative result was {preferred}; Klein remains the explicit compatibility selection "
            "until a human stage preference is recorded."
        )
    receipt = receipts.get(selected_stage, {})
    selected_image = receipt.get("output_asset")
    if not isinstance(selected_image, str) or not selected_image.strip():
        raise ValueError(f"{selected_stage} render receipt has no output_asset")
    value = {
        "schema_version": "final_stage_decision_v1",
        "decision_id": f"final-stage:{comparison['concept_id']}:{comparison['attempt']:02d}:automatic",
        "concept_id": comparison["concept_id"],
        "attempt": comparison["attempt"],
        "selected_stage": selected_stage,
        "selected_image": selected_image,
        "reason": reason,
        "source": source,
        "comparative_review_id": comparison["comparison_id"],
        "requires_human_review": requires_human,
        "automatic": True,
    }
    return validate_contract("final_stage_decision_v1", value)
