%%writefile app.py
import streamlit as st
from groq import Groq
from pypdf import PdfReader

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Career & Skill Guidance Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- STYLING ----------------
st.markdown("""
<style>
body {
    background-color: #f5f5f5;
    color: #0f1113;
}
h1, h2, h3, h4 {
    color: #1f2937;
}
.stButton>button {
    background-color: #4f46e5;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    padding: 0.5em 1em;
}
.stButton>button:hover {
    background-color: #6366f1;
    color: white;
}
.stTextInput>div>input, .stTextArea>div>textarea, .stSelectbox>div>div>div {
    border-radius: 6px;
    border: 1px solid #cbd5e1;
    padding: 0.5em;
}
.stFileUploader>div>input {
    padding: 0.4em;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🎓 AI Career Assistant")
st.sidebar.markdown("**Event:** InnovateX-2025")
st.sidebar.markdown("**Mode:** Solo Project")
st.sidebar.markdown("**Focus:** AI-powered Career Guidance")
st.sidebar.markdown("Provide your education, interests, and resume to generate a personalized career roadmap.")

# ---------------- MAIN UI ----------------
st.title("🎓 AI Career & Skill Guidance Assistant")
st.subheader("Personalized Career Paths, Skill Roadmaps & Certification Guidance")
st.markdown("---")

# ---------------- RESUME UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload Resume (PDF optional)",
    type=["pdf"],
    help="Optional: Upload your resume to provide AI with more context"
)

resume_text = ""
if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        resume_text += page.extract_text()

# ---------------- USER INPUTS ----------------
col1, col2 = st.columns(2)
with col1:
    education = st.text_input("Education (e.g., BS CS, Intermediate)")
with col2:
    experience = st.selectbox(
        "Experience Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

interests = st.text_area("Interests (AI, Cybersecurity, Web, Data, etc.)")
goal = st.text_input("Career Goal (optional)")

st.markdown("---")

# ---------------- API KEY (BACKEND ONLY) ----------------
api_key = "YOUR_API_KEY"  # Keep your Groq key private

# ---------------- AI LOGIC ----------------
def generate_guidance():
    client = Groq(api_key=api_key)

    prompt = f"""
You are an expert career mentor and professional coach.
Your task is to generate a **structured, actionable, beginner-friendly career roadmap**.

User Profile:
Education: {education}
Interests: {interests}
Experience Level: {experience}
Career Goal: {goal}

Resume Content (if provided):
{resume_text}

STRICT OUTPUT FORMAT:
1. Recommended Career Path(s) (2-3 realistic options)
2. Step-by-Step Skill Roadmap (Beginner → Advanced)
3. Certifications & Learning Resources (industry-recognized)
4. Practical Projects to Build
5. Next 90-Day Action Plan (weekly steps)

Use clear, professional, and motivating language.
Avoid buzzwords. Focus on employability and real-world relevance.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.35
    )

    return response.choices[0].message.content

# ---------------- BUTTON ----------------
if st.button("Generate Career Guidance"):
    if not education or not interests:
        st.warning("Please fill in Education and Interests.")
    else:
        with st.spinner("Generating personalized career guidance..."):
            result = generate_guidance()
            st.success("✅ Career Guidance Ready")
            st.markdown(result)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("InnovateX-2025 | AI Career & Skill Guidance Assistant | Solo Project")
