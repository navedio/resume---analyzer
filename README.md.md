# 📄 Resume Analyzer

A web app that compares a resume against a job description and returns a match score, matched and missing skills, and suggestions to improve the resume.

Built with Python, Streamlit and scikit-learn.

## Screenshots

> Add screenshots here, for example:
> `![Home](screenshots/home.png)`
> `![Result](screenshots/result.png)`

## Features

- Upload a resume as PDF, or paste the text directly
- Overall match score (0–100%) against a job description
- Matched and missing skills
- Resume section check (Education, Experience, Projects, Skills, Contact)
- Actionable suggestions to improve the resume

## Tech Stack

| Purpose | Tool |
|---|---|
| Language | Python |
| Web interface | Streamlit |
| PDF text extraction | pypdf |
| Text similarity | scikit-learn (TF-IDF, cosine similarity) |
| Text processing | re (regular expressions) |

## How It Works

1. Text is extracted from the resume PDF and cleaned (lowercase, extra spaces removed).
2. Skills are detected in both the resume and the job description using a predefined skill list.
3. Matched skills (intersection) and missing skills (difference) are calculated.
4. Text similarity is computed with TF-IDF vectors and cosine similarity.
5. The final score is a weighted combination:

   **Score = 50% skill match + 30% text similarity + 20% resume sections**

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/resume-analyzer.git
cd resume-analyzer

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python -m streamlit run app.py
```

Then open `http://localhost:8501` in your browser, upload a resume, paste a job description and click **Analyze**.

## Project Structure

```
resume-analyzer/
├── app.py             # Streamlit UI
├── analyzer.py        # Core logic (parsing, matching, scoring)
├── requirements.txt   # Dependencies
└── README.md
```

## Customization

The detected skills come from the `SKILLS` list in `analyzer.py`. Edit it to match your field (for example design, finance or data science).

## Limitations

- Only skills present in the `SKILLS` list are detected.
- Scanned or image-based PDFs are not supported (no OCR).
- The score is a guide, not a replacement for human review.

## Future Improvements

- [ ] Automatic skill extraction from the job description
- [ ] DOCX resume support
- [ ] Score history using SQLite
- [ ] Detailed feedback using an LLM API
- [ ] OCR support for scanned resumes
