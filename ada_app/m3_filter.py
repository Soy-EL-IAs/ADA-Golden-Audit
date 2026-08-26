import re
from collections import Counter
from typing import List, Dict, Any

def tokenize(text: str) -> set:
    text = text.lower()
    words = re.findall(r'\b[a-z]{3,}\b', text)
    stop_words = {'the', 'and', 'with', 'her', 'she', 'for', 'from', 'this', 'that', 'has'}
    return set(words) - stop_words

def jaccard(set1: set, set2: set) -> float:
    if not set1 and not set2:
        return 0.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union

def run_m3_analysis(concepts: List[Dict[str, Any]]) -> Dict[str, Any]:
    # Extract combined text per concept
    texts = []
    tokens_list = []
    
    # Track word frequencies across the batch to penalize overused tropes
    all_tokens = []
    
    for c in concepts:
        prop = c.get('proposal', c)
        combined = " ".join(str(prop.get(key, "")) for key in ("action", "setting", "micro_location", "hook", "camera", "expression")) if "action" in prop else f"{prop.get('snapshot', '')} {prop.get('visual_hook', '')} {prop.get('provocative_mechanism', '')} {prop.get('composition_intent', '')}"
        toks = tokenize(combined)
        texts.append(combined)
        tokens_list.append(toks)
        all_tokens.extend(list(toks))
        
    token_counts = Counter(all_tokens)
    
    results = {}
    
    unique_count = 0
    duplicate_count = 0
    recommended_count = 0
    weak_count = 0
    
    for i, c in enumerate(concepts):
        cid = c.get("concept_id")
        toks = tokens_list[i]
        
        max_sim = 0.0
        similar_to = []
        
        for j in range(i):
            sim = jaccard(toks, tokens_list[j])
            if sim > 0.4:
                similar_to.append({
                    "id": concepts[j].get("concept_id"),
                    "score": int(sim * 100)
                })
            if sim > max_sim:
                max_sim = sim
                
        similar_to.sort(key=lambda x: x["score"], reverse=True)
        
        diversity_score = max(0, 100 - int(max_sim * 100))
        
        # Penalize quality if it uses too many highly frequent terms (batch tropes)
        trope_penalty = sum(1 for t in toks if token_counts[t] > len(concepts) * 0.4) * 2
        base_quality = 90
        quality_score = max(0, min(100, base_quality - trope_penalty))
        
        status = c.get("status", "PASS")
        
        if status != "PASS":
            recommendation = "INVALID"
            reason = "Failed structural or semantic validation."
        elif max_sim > 0.85:
            recommendation = "Duplicate"
            reason = f"Duplicate of {similar_to[0]['id']}."
            quality_score = max(0, quality_score - 30)
            duplicate_count += 1
        elif max_sim > 0.60:
            recommendation = "Weak"
            reason = "High repetition of previous concepts."
            weak_count += 1
            unique_count += 1
        elif diversity_score < 70:
            recommendation = "Acceptable"
            reason = "Somewhat similar to other concepts."
            unique_count += 1
        else:
            recommendation = "Recommended"
            reason = "Strong readable visual hook." if quality_score > 80 else "Good diversity."
            recommended_count += 1
            unique_count += 1
            
        results[cid] = {
            "concept_id": cid,
            "quality": {
                "score": quality_score,
                "reason": reason
            },
            "diversity": {
                "score": diversity_score,
                "similar_to": similar_to[:2]
            },
            "recommendation": recommendation
        }
        
    return {
        "summary": {
            "generated": len(concepts),
            "unique": unique_count,
            "duplicates": duplicate_count,
            "recommended": recommended_count,
            "weak": weak_count
        },
        "concepts": results
    }
