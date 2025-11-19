# AI Resume Screening SaaS

This project provides an API-driven resume analysis system built with FastAPI and transformer-based NLP models.
It evaluates one or multiple resumes against a job description and returns structured scoring, skill insights, summaries, and ranked results.
The system supports both static and dynamic job descriptions and exposes a unified analysis endpoint.

---

## Features

* Unified single endpoint for both single and bulk resume analysis
* Dynamic job description input (via API)
* Optional static job description from file
* PDF resume text extraction
* Skill extraction and missing skill analysis
* Semantic similarity scoring
* Skills match scoring
* Weighted overall fit score
* Strengths and improvement gaps
* One-line insight summary
* T5-based resume summarization
* Ranked output for bulk mode
* API key authentication
* Health and version endpoints
* SaaS-style request metadata (UUID, timestamp, processing time)

---

## Project Structure

```
ai-resume-screener/
│
├── app.py
│
├── utils/
│   ├── parser.py
│   ├── insights.py
│   ├── skill_extractor.py
│   ├── metadata.py
│   ├── auth.py
│
├── model/
│   ├── embeddings.py
│   ├── summarizer.py
│   ├── scoring.py
│
├── data/
│   └── job_description.txt
│
└── requirements.txt
```

---

## API Endpoints

### 1. Unified Resume Analysis

`POST /analyze/`

Supports:

* Single resume
* Multiple resumes
* Dynamic JD (text)
* Static JD (file)

**Input (multipart/form-data):**

* `files`: List of PDF resumes (required)
* `jd`: Job description text (optional)
* `use_static_jd`: Boolean to load `job_description.txt` (optional)

**Behavior:**

* If `jd` is provided → dynamic JD is used
* Else if `use_static_jd=true` → static JD is used
* Returns a single result for one resume
* Returns ranked results for multiple resumes

### 2. Health Check

`GET /health`

### 3. Version Information

`GET /version`

---

## Example Response (Single Resume)

```json
{
  "candidate_id": "uuid",
  "timestamp": "2025-11-18 22:16:04",
  "processing_time_ms": 782.5,
  "file_name": "resume.pdf",
  "analysis": {
    "semantic_score": 0.67,
    "skills_match_score": 30,
    "overall_fit_score": 52.5
  },
  "insights": {
    "skills_detected": ["python", "git"],
    "missing_skills": ["aws", "sql"],
    "strengths": [...],
    "gaps": [...],
    "overall_insight": "Strong in python, git but missing aws, sql.",
    "summary": "..."
  }
}
```

---

## Example Response (Bulk Resumes)

```json
{
  "service": "AI Resume Screening SaaS",
  "version": "1.0.4",
  "total_resumes": 5,
  "ranked_results": [ ... sorted candidates ... ]
}
```

---

## Authentication

All protected endpoints require:

```
x-api-key: your_api_key
```

Swagger UI supports authorization via the built-in “Authorize” button.

---

## Running the Project

### Create environment

```
python -m venv venv
venv\Scripts\activate   # Windows
# or
source venv/bin/activate   # Mac/Linux
```

### Install dependencies

```
pip install -r requirements.txt
```

### Run server

```
uvicorn app:app --reload
```

### Open API documentation

```
http://127.0.0.1:8000/docs
```

---

## Models Used

* Semantic similarity: `sentence-transformers/all-MiniLM-L6-v2`
* Summarization: `t5-small`

---

## Use Cases

* Automated resume shortlisting
* Candidate ranking for recruiters
* Bulk resume screening for HR teams
* Skill-gap analysis
* EdTech resume evaluation tools
* Internal hiring tools or dashboards

---
