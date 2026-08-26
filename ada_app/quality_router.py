from typing import Dict, Any

from ada_app.semantic_contracts import build_routing_decision

class QualityRouter:
    """
    Interprets the verdict from a Visual Review (illustrious or klein stage)
    and produces an actionable pipeline routing decision.
    """
    
    ACTION_ADVANCE_TO_KLEIN = "ADVANCE_TO_KLEIN"
    ACTION_RETRY_ILLUSTRIOUS = "RETRY_ILLUSTRIOUS"
    ACTION_RETRY_KLEIN = "RETRY_KLEIN"
    ACTION_APPROVE = "APPROVE"
    ACTION_REJECT = "REJECT"

    @classmethod
    def route(cls, stage: str, verdict: str) -> str:
        """
        Map stage and schema verdict to a deterministic internal action.
        Accept renderer-agnostic v2 verdicts and persisted v1 verdicts.
        """
        stage = stage.lower()
        verdict = verdict.upper()
        
        if stage == "illustrious":
            if verdict in ("PASS", "MINOR_DEFECT"):
                return cls.ACTION_ADVANCE_TO_KLEIN
            elif verdict in ("RETRY_RENDER", "RETRY_ILLUSTRIOUS", "REVIEW", "REVIEW_REQUIRED"):
                return cls.ACTION_RETRY_ILLUSTRIOUS
            elif verdict in ("FAIL", "REJECT"):
                return cls.ACTION_REJECT
                
        elif stage == "klein":
            if verdict in ("PASS", "MINOR_DEFECT"):
                return cls.ACTION_APPROVE
            elif verdict == "RETRY_ILLUSTRIOUS":
                return cls.ACTION_RETRY_ILLUSTRIOUS
            elif verdict in ("RETRY_RENDER", "REVIEW", "REVIEW_REQUIRED"):
                return cls.ACTION_RETRY_KLEIN
            elif verdict in ("FAIL", "REJECT"):
                return cls.ACTION_REJECT
                
        # Fallback if unknown
        return cls.ACTION_REJECT

    @classmethod
    def decide(cls, observation: Dict[str, Any]) -> Dict[str, Any]:
        """Produce a persisted decision from an observation without changing legacy routing."""
        action = cls.route(observation["stage"], observation["source_review_verdict"])
        return build_routing_decision(observation, action)
