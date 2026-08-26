import json
from typing import List, Dict, Any
from ada_app.semantic_contracts import expand_compact_sketch

def calculate_dataset_score(proposal: Dict[str, Any]) -> int:
    score = 0
    # Base points based on presence and strength
    primary = proposal.get("primary_hook", {})
    if isinstance(primary, dict) and primary.get("main"):
        score += 35
    
    context = proposal.get("context_hook", [])
    if isinstance(context, list) and context:
        score += 25
    
    if proposal.get("micro_story"):
        score += 20
        
    if proposal.get("animation_beat"):
        score += 10
        
    score += 10 # Base personality fit assuming prompt handled it
    
    # Heuristic penalties
    action = str(proposal.get("action", "")).lower()
    setting = str(proposal.get("setting", "")).lower()
    why = str(proposal.get("why_it_scroll_stops", "")).lower()
    
    if "generic" in why or "standing" in action or "posing" in action:
        score -= 20
    if "just" in why or "location" in why or not context:
        score -= 15
    if not context or "none" in str(context).lower() or "look" in action and "camera" in action:
        score -= 20
    if "wallpaper" in why or "beautiful" in why or "portrait" in action:
        score -= 25
        
    return score

def select_top_candidates(records: List[Dict[str, Any]], m3_analysis: Dict[str, Any], top_n: int = 3) -> List[Dict[str, Any]]:
    candidates = []
    m3_concepts = m3_analysis.get("concepts", {})
    
    for r in records:
        cid = r.get("concept_id")
        m3_data = m3_concepts.get(cid)
        if not m3_data: continue
        rec = m3_data.get("recommendation")
        if rec in ("INVALID", "Duplicate", "Weak"): continue
        
        q_score = m3_data.get("quality", {}).get("score", 0)
        d_score = m3_data.get("diversity", {}).get("score", 0)
        
        proposal = r.get("proposal", {})
        is_dataset = "primary_hook" in proposal
        viral_score = calculate_dataset_score(proposal) if is_dataset else 0
        
        candidates.append({
            "record": r, "m3_data": m3_data, "q_score": q_score, "d_score": d_score, 
            "is_dataset": is_dataset, "viral_score": viral_score
        })
        
    candidates.sort(key=lambda x: (x["viral_score"] if x["is_dataset"] else x["q_score"], x["d_score"]), reverse=True)
    selected = []
    for idx, c in enumerate(candidates[:top_n]):
        r = c["record"]
        m3_data = c["m3_data"]
        selected.append({
            "concept_id": r.get("concept_id"),
            "character": r.get("character"),
            "source_model": r.get("source_model"),
            "concept_sketch": r.get("proposal", {}),
            "original_proposal": expand_compact_sketch(r.get("proposal", {})) if isinstance(r.get("proposal"), dict) and "action" in r.get("proposal", {}) else r.get("proposal", {}),
            "m3_scores": {
                "quality": m3_data.get("quality", {}).get("score"),
                "diversity": m3_data.get("diversity", {}).get("score")
            },
            "recommendation": m3_data.get("recommendation"),
            "selection_rank": idx + 1,
            "selection_reason": f"Top {idx + 1} candidate based on Viral Score ({c['viral_score']}) and Diversity ({c['d_score']})" if c["is_dataset"] else f"Top {idx + 1} candidate based on Quality ({c['q_score']}) and Diversity ({c['d_score']})",
            "pipeline_state": "SELECT",
            "run_id": r.get("run_id")  # Should inject if missing, will handle in main.py
        })
    return selected
