import json
import re

# Load skills list at module import
with open("data/skills_list.json", "r") as f:
    SKILLS = json.load(f)["skills"]

def normalize_text(text: str) -> str:
    """Lowercase and remove special characters for matching."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9+.# ]', ' ', text)
    return text

def extract_skills(text: str):
    """
    Extract skills from resume or JD text
    using simple keyword matching.
    """
    text = normalize_text(text)
    found = []

    for skill in SKILLS:
        # Match whole words or phrases
        if skill in text:
            found.append(skill)

    return list(set(found))  # remove duplicates

def find_missing_skills(jd_skills, resume_skills):
    """Identify skills required in JD but not in resume."""
    missing = [skill for skill in jd_skills if skill not in resume_skills]
    return missing
