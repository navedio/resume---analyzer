import streamlit as st
from analyzer import analyze, read_pdf

st.set_page_config(page_title="Resume Analyzer", page_icon="📄")
st.title("📄 Resume Analyzer")
st.caption("Match your resume against a job description and improve it.")

uploaded = st.file_uploader("upload your resume (PDF)", type=["pdf"])
pasted = st.text_area("or paste your resume text here", height=150)
jd = st.text_area("paste the job description", height=200)

if st.button("Analyze", type="primary"):
    resume = read_pdf(uploaded) if uploaded else pasted
    if not resume.strip() or not jd.strip():
        st.warning("Both resume and job description are required.")
        st.stop()

    r = analyze(resume, jd)

    st.metric("Match Score", f"{r['score']}%")
    st.progress(r["score"] / 100)
    st.caption(f"Text similarity: {r['similarity']}%")

    c1, c2 = st.columns(2)
    c1.subheader("✅ Matched skills")
    c1.write(", ".join(r["matched"]) or "none")
    c2.subheader("❌ Missing skills")
    c2.write(", ".join(r["missing"]) or "No missing skills!")

    st.subheader("Sections")
    for name, ok in r["sections"].items():
        st.write(("✅ " if ok else "❌ ") + name)

    st.subheader("💡 Suggestions")
    for t in r["tips"] or ["Your resume looks good!"]:
        st.write("- " + t)
