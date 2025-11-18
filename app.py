# app.py
from fastapi import FastAPI, UploadFile, File, Depends, Request, Security
from fastapi.security import APIKeyHeader
from utils.parser import extract_text_from_pdf
from utils.insights import generate_strengths, generate_gaps
from utils.auth import validate_api_key
from utils.metadata import generate_metadata
from datetime import datetime
from utils.skill_extractor import extract_skills, find_missing_skills
from model.embeddings import compute_similarity
from typing import List
from model.summarizer import summarize_text
from model.scoring import (
    compute_semantic_score,
    compute_skills_match_score,
    compute_overall_fit_score
)
import uvicorn


# -------------------- SECURITY SCHEME FOR SWAGGER --------------------
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

app = FastAPI(
    title="AI Resume Screening SaaS",
    description="Secure AI Resume Screening API with NLP scoring, insights, and SaaS metadata",
    version="1.0.4",
    swagger_ui_parameters={"persistAuthorization": True}
)


# -------------------- LOAD STATIC JOB DESCRIPTION --------------------
with open("data/job_description.txt", "r", encoding="utf-8") as f:
    JOB_DESCRIPTION = f.read()


# -------------------- HEALTH ENDPOINT --------------------
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "AI Resume Screening SaaS",
        "message": "Service running successfully"
    }


# -------------------- VERSION ENDPOINT --------------------
@app.get("/version")
def version():
    return {
        "version": "1.0.4",
        "models": {
            "semantic": "sentence-transformers/all-MiniLM-L6-v2",
            "summary": "t5-small"
        },
        "description": "AI Resume Screening System with scoring, insights, and SaaS metadata"
    }


# ======================================================================
#                 UNIFIED SINGLE + BULK ANALYSIS ENDPOINT
# ======================================================================
@app.post("/analyze/")
async def analyze(
    files: List[UploadFile] = File(...),
    jd: str = File(default=None),
    use_static_jd: bool = File(default=False),
    request: Request = None,
    auth: None = Security(validate_api_key)
):
    start_time = datetime.now()

    # -------------------- SELECT JOB DESCRIPTION --------------------
    if jd and jd.strip():
        jd_text = jd
    elif use_static_jd:
        jd_text = JOB_DESCRIPTION
    else:
        return {
            "error": "No job description provided. Use jd=<text> or use_static_jd=true"
        }

    jd_skills = extract_skills(jd_text)
    results = []

    # -------------------- PROCESS EACH RESUME --------------------
    for file in files:
        pdf_bytes = await file.read()
        resume_text = extract_text_from_pdf(pdf_bytes)

        resume_skills = extract_skills(resume_text)
        missing_skills = find_missing_skills(jd_skills, resume_skills)

        strengths = generate_strengths(resume_skills, jd_skills, resume_text)
        gaps = generate_gaps(missing_skills)

        semantic_score = compute_semantic_score(resume_text, jd_text)
        skills_match_score = compute_skills_match_score(jd_skills, resume_skills)
        overall_fit_score = compute_overall_fit_score(semantic_score, skills_match_score)

        summary = summarize_text(resume_text)

        overall_insight = (
            f"Strong in {', '.join(resume_skills[:2])} "
            f"but missing {', '.join(missing_skills[:2])}."
        )

        single_metadata = generate_metadata(start_time)

        results.append({
            **single_metadata,
            "file_name": file.filename,
            "analysis": {
                "semantic_score": round(semantic_score, 3),
                "skills_match_score": skills_match_score,
                "overall_fit_score": overall_fit_score
            },
            "insights": {
                "skills_detected": resume_skills,
                "missing_skills": missing_skills,
                "strengths": strengths,
                "gaps": gaps,
                "overall_insight": overall_insight,
                "summary": summary
            }
        })

    # -------------------- RETURN SINGLE RESUME RESULT --------------------
    if len(files) == 1:
        return results[0]

    # -------------------- RETURN SORTED BULK RESULTS --------------------
    results = sorted(results, key=lambda x: x["analysis"]["overall_fit_score"], reverse=True)

    return {
        "service": "AI Resume Screening SaaS",
        "version": "1.0.4",
        "total_resumes": len(results),
        "ranked_results": results
    }


# -------------------- RUN SERVER LOCALLY --------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
