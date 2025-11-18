# model/scoring.py
from typing import List
from model.embeddings import compute_similarity

def compute_semantic_score(resume_text: str, jd_text: str) -> float:
    """
    Returns semantic similarity between resume and JD as a float in [0,1].
    """
    try:
        score = compute_similarity(resume_text, jd_text)
        # ensure numeric and clipped
        score = float(score)
        if score < 0:
            score = 0.0
        if score > 1:
            score = 1.0
        return score
    except Exception:
        # fallback safe value
        return 0.0

def compute_skills_match_score(jd_skills: List[str], resume_skills: List[str]) -> float:
    """
    Returns skills match as percentage between 0 and 100.
    If JD skills list is empty, returns 0.0
    """
    try:
        jd_set = set([s.strip().lower() for s in jd_skills if s and s.strip()])
        resume_set = set([s.strip().lower() for s in resume_skills if s and s.strip()])
        if not jd_set:
            return 0.0
        matched = jd_set.intersection(resume_set)
        score_percent = (len(matched) / len(jd_set)) * 100.0
        return round(score_percent, 2)
    except Exception:
        return 0.0

def compute_overall_fit_score(semantic_score: float, skills_match_percent: float,
                              semantic_weight: float = 0.6, skills_weight: float = 0.4) -> float:
    """
    Combine semantic and skills-match into an overall fit score (0-100).
    semantic_score is expected in [0,1], skills_match_percent in [0,100].
    Default weights: semantic 60%, skills 40%.
    """
    try:
        semantic_component = semantic_score * 100.0  # convert to percent
        skills_component = skills_match_percent
        overall = semantic_weight * semantic_component + skills_weight * skills_component
        return round(overall, 2)
    except Exception:
        return 0.0
