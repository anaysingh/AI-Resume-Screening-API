# utils/insights.py

def generate_strengths(resume_skills, jd_skills, resume_text):
    strengths = []

    # 1. Skill-based strengths
    matched = set(resume_skills).intersection(set(jd_skills))
    for skill in matched:
        strengths.append(f"Strong presence of {skill}")

    # 2. Keyword-based strengths
    text_lower = resume_text.lower()

    keyword_indicators = {
        "python": "Good Python coding experience",
        "api": "Experience working with APIs",
        "backend": "Backend development exposure",
        "automation": "QA automation or framework development experience",
        "ml": "Machine Learning exposure",
        "deep learning": "Deep Learning familiarity",
        "sql": "Database and SQL knowledge"
    }

    for key, message in keyword_indicators.items():
        if key in text_lower and message not in strengths:
            strengths.append(message)

    # Limit strengths to top 5 for clean output
    return strengths[:5]


def generate_gaps(missing_skills):
    gaps = []

    for skill in missing_skills:
        if skill.lower() in ["aws", "azure", "gcp"]:
            gaps.append("Cloud experience missing (AWS/Azure/GCP)")
        elif skill == "docker":
            gaps.append("Docker containerization not shown")
        elif skill == "sql":
            gaps.append("No SQL or database experience mentioned")
        elif skill == "machine learning":
            gaps.append("ML knowledge expected but not visible")
        elif skill == "nlp":
            gaps.append("NLP skills missing")
        else:
            gaps.append(f"{skill} not mentioned")

    # Limit to top 5
    return gaps[:5]
