"""Core logic: resume vs job description matching."""
import re
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# we can add our skills list in this section
SKILLS = [
    "python", "java", "javascript", "typescript", "c++", "c#", "sql", "mysql",
    "postgresql", "mongodb", "html", "css", "react", "node.js", "django",
    "flask", "fastapi", "streamlit", "pandas", "numpy", "matplotlib", "plotly",
     "tensorflow", "pytorch", "machine learning", "deep learning",
    "nlp", "data analysis", "data visualization", "statistics", "excel",
    "power bi", "tableau", "git", "github", "docker", "aws", "azure",
    "rest api", "api", "agile",  "oop", "data structures", "algorithms",
    "web scraping", "automation", "testing", "communication", "teamwork",
]

SECTIONS = {
    "Education": ["education", "academic"],
    "Experience": ["experience", "internship", "employment"],
    "Projects": ["projects", "project"],
    "Skills": ["skills", "technical skills"],
    "Contact": ["email", "@", "phone", "linkedin", "github"],
}


def read_pdf(file) -> str:
    reader = PdfReader(file)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def find_skills(text: str) -> set:
    text = clean(text)
    found = set()
    for skill in SKILLS:
        pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"
        if re.search(pattern, text):
            found.add(skill)
    return found


def text_similarity(resume: str, jd: str) -> float:
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vec.fit_transform([clean(resume), clean(jd)])
    return float(cosine_similarity(matrix[0], matrix[1])[0][0])


def check_sections(resume: str) -> dict:
    text = clean(resume)
    return {name: any(k in text for k in keys) for name, keys in SECTIONS.items()}


def analyze(resume: str, jd: str) -> dict:
    resume_skills = find_skills(resume)
    jd_skills = find_skills(jd)
    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills

    skill_score = len(matched) / len(jd_skills) if jd_skills else None
    sim_score = text_similarity(resume, jd)
    sections = check_sections(resume)
    section_score = sum(sections.values()) / len(sections)

    if skill_score is None:  # JD me known skills nahi mile
        final = 0.7 * min(sim_score * 2, 1) + 0.3 * section_score
    else:
        final = (0.5 * skill_score + 0.3 * min(sim_score * 2, 1)
                 + 0.2 * section_score)

    tips = []
    if missing:
        tips.append("These skills are in the job description but not in your resume: "
                    + ", ".join(sorted(missing)) + ". Add them if you have them.")
    for name, ok in sections.items():
        if not ok:
            tips.append(f"The'{name}' section seems to be missing.")
    if len(resume.split()) < 150:
        tips.append("Your resume is quite short. Add more detail about project and achivements.")
    if not re.search(r"\d+%|\d+\+|\d{2,}", resume):
        tips.append("Add numbers (e.g. 'improved speed by 30%') to show impact.")

    return {
        "score": round(final * 100),
        "similarity": round(sim_score * 100),
        "matched": sorted(matched),
        "missing": sorted(missing),
        "sections": sections,
        "tips": tips,
    }
